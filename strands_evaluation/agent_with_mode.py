"""
Strands-native agent runner for the Data Lake benchmark.

Replaces the hand-rolled agent_runner.py with a clean Strands Agent skeleton
that wires together:
  - SlidingWindowConversationManager  (keeps last-k turns in context)
  - ToolLimitPlugin                   (stops after max_tool_calls)
  - LoggingCallbackHandler            (structured per-turn logging)
"""

import concurrent.futures
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.tools.executors import SequentialToolExecutor, ConcurrentToolExecutor
from strands.tools.decorator import DecoratedFunctionTool
from strands.vended_plugins.skills import AgentSkills

import logging

from strands_evaluation.config import AgentConfig, ConditionConfig, RunConfig
from strands_evaluation.instrumentation import (
    TracePlugin,
    ReadTracePlugin,
    SearchCallBudgetHandler,
    set_trace_context,
    event_loop_tracker,
    ToolLimitSteeringHandler,
    SubmitAnswerPlugin,
    LoggingPlugin,
    TelemetryTracker,
)
from strands_evaluation.instrumentation.loop_plugin import CategoryStagnationHandler
from strands_evaluation.helper.logger import configure_logging
from strands_evaluation.helper.result import AgentResult
from strands_evaluation.helper.sandbox import (
    _cleanup_isolated_sandbox,
    _create_isolated_sandbox,
)
from strands_evaluation.helper.text_utils import _clean_answer
from strands_evaluation.llm.llm_factory import build_model
from strands_evaluation.tools.agent_tools import (
    clear_submitted_answer,
    get_submitted_answer,
    submit_answer,
    search,
    search_keyword,
    search_prefix,
)
from strands_evaluation.tools.agent_tools_v2 import (
    cleanup_sandbox,
    execute_code,
    get_sandbox_info,
    grep_file,
    list_files,
    peek_file,
    peek_multiple,
    query_file,
    read_file,
    set_sandbox_dir,
    summarize_context,
)
from strands_evaluation.tools.agent_tools import download
from strands_evaluation.tools.external.plan_tools import plan
from strands_evaluation.tools.external.ideal.plan_ideal import plan_ideal
from strands_evaluation.tools.external.ideal.plan_store import (
    set_task_context as set_ideal_plan_task_context,
)
from strands_evaluation.tools.external.ideal.search_wrapper import (
    build_search_tools as build_search_tools_by_mode,
    search_tool_names_in as search_tool_names_in_mode,
)
from strands_evaluation.tools.external.search_eval_tools import (
    build_search_tools,
    search_tool_names_in as search_tool_names_in_legacy,
)

logger = logging.getLogger(__name__)

# Condition A search tools
_CONDITION_A_TOOLS_AVAILABLE = False
try:
    from strands_evaluation.tools.external.search_a_tools import (
        search_value as search_value_a,
        search_schema,
        search_reranked,
    )
    _CONDITION_A_TOOLS_AVAILABLE = True
except ImportError:
    pass

# Condition B search tools
_CONDITION_B_TOOLS_AVAILABLE = False
try:
    from strands_evaluation.tools.external.search_b_tools import (
        search_value as search_value_b,
        search_schema as search_schema_b,
    )
    _CONDITION_B_TOOLS_AVAILABLE = True
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Mode composition (inlined in this module)
# ---------------------------------------------------------------------------

_MODES = {"naive", "standard", "ideal"}


@dataclass
class ModeBundle:
    tools: List[Any]
    system_prompt: str
    search_tool_names: Tuple[str, ...]
    enable_skills: bool
    enable_stagnation: bool
    modes: Dict[str, str]


def _normalize_mode(value: Optional[str], default: str, label: str) -> str:
    mode = (value or default).strip().lower()
    if mode not in _MODES:
        raise ValueError(f"Unsupported {label} mode '{value}'. Expected one of: {', '.join(sorted(_MODES))}")
    return mode


def build_search(
    mode: str,
    *,
    task_context: Optional[Dict[str, Any]] = None,
) -> List[DecoratedFunctionTool]:
    """Return the base search tool surface for a mode."""
    search_mode = _normalize_mode(mode, "standard", "search_tool")

    if search_mode == "naive":
        if not _CONDITION_B_TOOLS_AVAILABLE:
            raise RuntimeError("Condition B search tools are unavailable (import failed).")
        from strands_evaluation.tools.external.search_b_tools import (
            search_schema as search_schema_sparse,
            search_value as search_value_sparse,
        )

        return [search_value_sparse, search_schema_sparse, search_prefix]

    if search_mode == "standard":
        if not _CONDITION_A_TOOLS_AVAILABLE:
            raise RuntimeError("Condition A search tools are unavailable (import failed).")
        from strands_evaluation.tools.external.search_a_tools import (
            search_schema as search_schema_hybrid,
            search_value as search_value_hybrid,
            search_reranked as search_reranked_hybrid,
        )

        return [search_value_hybrid, search_schema_hybrid, search_reranked_hybrid, search_prefix]

    import strands_evaluation.tools.external.ideal.search_ideal as search_ideal

    search_ideal.set_task_context(task_context or {})
    return [search_ideal.search_ideal]


def build_management(
    mode: str,
    *,
    base_prompt: str,
    task_context: Optional[Dict[str, Any]],
) -> tuple[str, List[Any], bool, bool]:
    """Return prompt, management tools, and behavior toggles for a mode."""
    management_mode = _normalize_mode(mode, "standard", "agent_management")

    if management_mode == "naive":
        return base_prompt, [], False, False

    prompt = _load_condition_prompt("b", fallback=base_prompt)
    if management_mode == "standard":
        return prompt, [plan, summarize_context], True, True

    # ideal = Condition-B management with plan swapped to plan_ideal.
    set_ideal_plan_task_context(task_context or {})
    return prompt, [plan_ideal, summarize_context], True, True


def build_results(
    mode: str,
    *,
    base_search_tools: Sequence[DecoratedFunctionTool],
    fixed_k: Optional[int],
) -> List[DecoratedFunctionTool]:
    """Apply fixed-k and payload-shaping wrappers to search tools."""
    results_mode = _normalize_mode(mode, "standard", "search_results")
    return build_search_tools_by_mode(
        base_search_tools,
        fixed_k=fixed_k,
        results_mode=results_mode,
    )


def build_mode_bundle(
    run_config: RunConfig,
    *,
    data_tools: Sequence[Any],
    task_context: Optional[Dict[str, Any]] = None,
) -> ModeBundle:
    """Build final tools/prompt/plugin toggles from multi-axis ablation modes."""
    search_tool_mode = _normalize_mode(run_config.search_tool_mode, "standard", "search_tool")
    search_results_mode = _normalize_mode(run_config.search_results_mode, "standard", "search_results")
    agent_management_mode = _normalize_mode(run_config.agent_management_mode, "standard", "agent_management")

    if search_tool_mode == "ideal" or agent_management_mode == "ideal":
        set_ideal_plan_task_context(task_context or {})

    raw_search_tools = build_search(search_tool_mode, task_context=task_context)
    search_tools = build_results(
        search_results_mode,
        base_search_tools=raw_search_tools,
        fixed_k=run_config.search_k,
    )
    system_prompt, management_tools, enable_skills, enable_stagnation = build_management(
        agent_management_mode,
        base_prompt=run_config.system_prompt,
        task_context=task_context,
    )

    tools = list(search_tools) + list(management_tools) + list(data_tools)
    return ModeBundle(
        tools=tools,
        system_prompt=system_prompt,
        search_tool_names=search_tool_names_in_mode(search_tools),
        enable_skills=enable_skills,
        enable_stagnation=enable_stagnation,
        modes={
            "search_tool": search_tool_mode,
            "search_results": search_results_mode,
            "agent_management": agent_management_mode,
        },
    )


# Shared callback tracking and plugin classes are defined in
# strands_evaluation.instrumentation.agent_plugins.


# ---------------------------------------------------------------------------
# DataLakeAgent
# ---------------------------------------------------------------------------

def _load_condition_prompt(condition: str, fallback: str = "") -> str:
    """Load system prompt for a condition."""
    path = f"prompts/condition_{condition}.txt"
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"{path} not found — using default system prompt")
        return fallback


def _base_condition(condition_label: str) -> str:
    """Strip optional experimental suffix from condition label."""
    if not condition_label:
        return "baseline"
    return str(condition_label).split("__", 1)[0]


def _resolve_condition(cond_cfg: ConditionConfig) -> str:
    """Resolve the actual experiment condition (baseline/a/b)."""
    if getattr(cond_cfg, "base_condition", None):
        return str(cond_cfg.base_condition)
    return _base_condition(cond_cfg.condition)


def _inject_search_budget_prompt(
    system_prompt: str,
    search_calls_limit: Optional[int],
    search_tool_names: tuple[str, ...],
) -> str:
    """Append search-call budget instructions when configured."""
    if search_calls_limit is None:
        return system_prompt
    names = ", ".join(search_tool_names) if search_tool_names else "search tools"
    budget_note = (
        "\n\n## SEARCH CALL BUDGET\n"
        f"- You have at most {search_calls_limit} total calls to: {names}.\n"
        "- When this budget is exhausted, do not call search tools again.\n"
        "- Continue with non-search tools (list/read/query/grep/download/execute_code), "
        "then call submit_answer."
    )
    return system_prompt.rstrip() + budget_note


class DataLakeAgent:
    """Strands-based agent for the Data Lake benchmark."""

    def __init__(
        self,
        agent_config: AgentConfig,
        run_config: Optional[RunConfig] = None,
    ) -> None:
        self.agent_config = agent_config
        self.run_config = run_config or RunConfig()
        self._model = build_model(agent_config)

    def _build_agent(
        self,
        telemetry: "TelemetryTracker",
        trace_attributes: Optional[Dict[str, Any]] = None,
        task_context: Optional[Dict[str, Any]] = None,
    ) -> tuple:
        cond = self.run_config.condition_config
        condition = _resolve_condition(cond)
        mode_overrides_enabled = any(
            [
                self.run_config.search_tool_mode,
                self.run_config.search_results_mode,
                self.run_config.agent_management_mode,
            ]
        )

        if not mode_overrides_enabled:
            if condition == "a" and not _CONDITION_A_TOOLS_AVAILABLE:
                raise RuntimeError("Condition A search tools are unavailable (import failed).")
            if condition in {"baseline", "b"} and not _CONDITION_B_TOOLS_AVAILABLE:
                raise RuntimeError("Condition B/Baseline search tools are unavailable (import failed).")

        # Core data-manipulation tools shared across all conditions
        _data_tools = [
            list_files, peek_file, peek_multiple, read_file, grep_file,
            query_file, download, execute_code, get_sandbox_info, cleanup_sandbox,
            submit_answer,
        ]

        if mode_overrides_enabled:
            mode_bundle = build_mode_bundle(
                self.run_config,
                data_tools=_data_tools,
                task_context=task_context,
            )
            tools = mode_bundle.tools
            system_prompt = mode_bundle.system_prompt
            search_tool_names = mode_bundle.search_tool_names
            enable_skills = mode_bundle.enable_skills
            enable_stagnation = mode_bundle.enable_stagnation
            logger.info(
                "Ablation modes active: search_tool=%s search_results=%s agent_management=%s",
                mode_bundle.modes["search_tool"],
                mode_bundle.modes["search_results"],
                mode_bundle.modes["agent_management"],
            )
        else:
            if condition == "a" and _CONDITION_A_TOOLS_AVAILABLE:
                # Condition A (tools-rich): hybrid RRF + schema + reranked + shared baseline tools
                raw_search_tools = [search_value_a, search_schema, search_reranked, search_prefix]
                system_prompt = _load_condition_prompt("a", fallback=self.run_config.system_prompt)
                search_tools = build_search_tools(
                    raw_search_tools,
                    fixed_k=self.run_config.search_k,
                    search_descriptions=self.run_config.search_descriptions,
                )
                tools = search_tools + _data_tools
                enable_skills = False
                enable_stagnation = False

            elif condition == "b" and _CONDITION_B_TOOLS_AVAILABLE:
                # Condition B (planning-rich): sparse search + prefix + plan tool + skills
                # summarize_context only given to B — longer planning loops benefit from manual context control
                raw_search_tools = [search_value_b, search_schema_b, search_prefix]
                system_prompt = _load_condition_prompt("b", fallback=self.run_config.system_prompt)
                search_tools = build_search_tools(
                    raw_search_tools,
                    fixed_k=self.run_config.search_k,
                    search_descriptions=self.run_config.search_descriptions,
                )
                tools = search_tools + [plan] + _data_tools + [summarize_context]
                enable_skills = True
                enable_stagnation = True

            else:
                # Baseline: Condition B search tools (BM25 + schema + prefix) without any context tools
                raw_search_tools = [search_value_b, search_schema_b, search_prefix]
                system_prompt = self.run_config.system_prompt
                search_tools = build_search_tools(
                    raw_search_tools,
                    fixed_k=self.run_config.search_k,
                    search_descriptions=self.run_config.search_descriptions,
                )
                tools = search_tools + _data_tools
                enable_skills = False
                enable_stagnation = False

            search_tool_names = search_tool_names_in_legacy(search_tools)

        system_prompt = _inject_search_budget_prompt(
            system_prompt,
            self.run_config.search_calls_limit,
            search_tool_names,
        )

        conv_manager = SlidingWindowConversationManager(
            window_size=self.run_config.sliding_window_k,
            per_turn=True,  # proactively trim before every LLM call to prevent overflow
        )

        if self.run_config.tool_executor == "sequential":
            tool_executor = SequentialToolExecutor()
        else:
            tool_executor = ConcurrentToolExecutor()

        _tool_limit_handler = ToolLimitSteeringHandler(
            self.run_config.max_tool_calls, self.run_config.timeout_seconds
        )

        def _callback(**kwargs):
            telemetry(**kwargs)
            event_loop_tracker(**kwargs)
            if kwargs.get("force_stop", False):
                reason = kwargs.get("force_stop_reason", "")
                if "ValidationException" in reason or "too long" in reason:
                    _tool_limit_handler.signal_context_overflow()

        cond = self.run_config.condition_config
        plugins = [_tool_limit_handler]
        if self.run_config.search_calls_limit is not None:
            plugins.append(
                SearchCallBudgetHandler(
                    max_search_calls=self.run_config.search_calls_limit,
                    search_tools=search_tool_names,
                )
            )
        plugins.extend([
            SubmitAnswerPlugin(),
            LoggingPlugin(),
        ])
        if enable_skills:
            plugins.append(AgentSkills(skills=[
                "strands_evaluation/tools/skills/plan-agent",
                "strands_evaluation/tools/skills/discover-data",
                "strands_evaluation/tools/skills/query-data",
            ]))
            if enable_stagnation and self.run_config.max_consecutive_category > 0:
                plugins.append(
                    CategoryStagnationHandler(self.run_config.max_consecutive_category)
                )
        read_tracer = ReadTracePlugin()
        plugins.append(read_tracer)
        plugins.append(TracePlugin(cond.trace_output_dir))

        return Agent(
            model=self._model,
            tools=tools,
            tool_executor=tool_executor,
            system_prompt=system_prompt,
            conversation_manager=conv_manager,
            plugins=plugins,
            callback_handler=_callback,
            trace_attributes=trace_attributes,
        ), read_tracer

    def run(
        self,
        question: str,
        session_id: Optional[str] = None,
        task_context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        start = time.time()

        logger.info("=" * 60)
        logger.info(f"NEW TASK: {self.agent_config.model_id}")
        logger.debug(f"QUESTION: {question}")
        logger.info("=" * 60)

        sandbox = _create_isolated_sandbox(str(os.getpid()))
        set_sandbox_dir(sandbox)
        clear_submitted_answer()

        telemetry = TelemetryTracker()
        trace_attributes = (
            {
                "gen_ai.conversation.id": session_id,
                "session.id": session_id,
            }
            if session_id
            else None
        )

        try:
            agent, read_tracer = self._build_agent(
                telemetry,
                trace_attributes=trace_attributes,
                task_context=task_context,
            )
            response = agent(question)

            submitted = get_submitted_answer()
            retries = 0
            while not submitted and retries < 2:
                logger.warning(
                    f"Agent finished without submit_answer. Nudging (attempt {retries + 1}/2)..."
                )
                response = agent(
                    "You provided a text response but you MUST use the `submit_answer` tool "
                    "to submit your final answer. Please call the tool now."
                )
                submitted = get_submitted_answer()
                retries += 1

            answer = submitted["answer"] if submitted else _clean_answer(str(response))
            elapsed = time.time() - start
            sources = list(read_tracer.gold_datasets_read)

            logger.info(f"ANSWER: {answer} ({elapsed:.1f}s)")
            return AgentResult(
                answer=answer,
                model=agent.model.config,
                model_name=self.agent_config.model_name,
                reasoning=submitted["reasoning"] if submitted else "",
                sources=sources,
                metrics=response.metrics,
                elapsed_time=elapsed,
                success=True,
            )
        except Exception as e:
            elapsed = time.time() - start
            logger.error(
                f"Agent crashed after {telemetry.tool_calls} tools "
                f"({elapsed:.1f}s): {type(e).__name__}: {e}",
                exc_info=True,
            )

            # Return the Error as a Result, including the partial metrics!
            return AgentResult(
                answer="",
                model="",
                model_name=self.agent_config.model_name,
                metrics=telemetry.partial_metrics, # Salvaged metrics!
                elapsed_time=elapsed,
                success=False,
                error=f"{type(e).__name__}: {e}",
            )

        finally:
            try:
                cleanup_sandbox()
            except Exception as e:
                logger.warning(f"Sandbox cleanup failed: {e}")
            try:
                _cleanup_isolated_sandbox(sandbox)
            except Exception as e:
                logger.warning(f"Isolated sandbox cleanup failed: {e}")


# ---------------------------------------------------------------------------
# Worker function (must be module-level for ProcessPoolExecutor pickling)
# ---------------------------------------------------------------------------

def _run_task_worker(
    task: Dict[str, Any],
    task_index: int,
    agent_config: AgentConfig,
    run_config: RunConfig,
    run_id: str,
    batch_name: Optional[str],
) -> Dict[str, Any]:
    """Run a single task in a worker process."""
    from strands_evaluation.helper.metrics import compute_exact_match, compute_f1_score, normalize_text

    log_model_name = agent_config.model_name or agent_config.model_id
    effort = (agent_config.extra_model_kwargs or {}).get("reasoning_effort")
    if effort:
        log_model_name = f"{log_model_name}-{effort}"

    configure_logging(
        model=log_model_name,
        condition=run_config.condition_config.condition,
        task_id=task.get("id"),
    )

    # Eagerly load search backend state once per worker process.
    # For ablation runs, mode overrides drive setup. For legacy runs, condition drives setup.
    mode_search_tool = (run_config.search_tool_mode or "").strip().lower() or None
    condition = _resolve_condition(run_config.condition_config)
    if mode_search_tool is None:
        mode_search_tool = "standard" if condition == "a" else "naive"

    if mode_search_tool == "standard" and _CONDITION_A_TOOLS_AVAILABLE:
        try:
            import strands_evaluation.tools.external.search_a_tools as _sa
            if run_config.search_db_path:
                _sa.set_db_path(run_config.search_db_path)
            _sa.setup()
        except Exception as e:
            logger.warning(f"Hybrid search setup failed: {e}")

    if mode_search_tool == "naive" and _CONDITION_B_TOOLS_AVAILABLE:
        # NOTE: do not call search_b_tools.setup() for naive mode.
        # setup() triggers external-tools/hybrid_search/api.setup(), which eagerly
        # loads embedding/reranker models that are unnecessary for sparse-only
        # search paths and can heavily impact worker startup and memory.
        if run_config.search_db_path:
            try:
                import strands_evaluation.tools.external.search_b_tools as _sb

                _sb.set_db_path(run_config.search_db_path)
            except Exception as e:
                logger.warning(f"Sparse search path override failed: {e}")

    if mode_search_tool == "ideal":
        if run_config.search_db_path:
            import strands_evaluation.tools.external.ideal.search_ideal as _si

            _si.set_db_path(run_config.search_db_path)

    try:
        logger.info(f"Starting task {task_index + 1}: {task.get('question', '')[:80]}...")

        da = DataLakeAgent(agent_config, run_config)

        cond = run_config.condition_config
        gold_ids = task.get("datasets_used", [])
        task_id = task.get("id", str(task_index))
        set_trace_context(task_id, gold_ids, cond.trace_output_dir)

        task_context = {
            "task_id": task_id,
            "datasets_used": gold_ids,
            "reasoning_chain": task.get("reasoning_chain", []),
        }
        if mode_search_tool == "ideal":
            import strands_evaluation.tools.external.ideal.search_ideal as _si

            _si.set_task_context(task_context)

        result = da.run(task["question"], task_context=task_context)

        result_dict: Dict[str, Any] = {
            "task_id": task.get("id", task_index),
            "model": agent_config.model_id,
            "question": task.get("question", ""),
            "ground_truth": task.get("answer", ""),
            "predicted_answer": result.answer,
            "reasoning": result.reasoning,
            "sources_used": result.sources,
            "time": result.elapsed_time,
            "success": result.success,
            "error": result.error,
        }

        # Tokens
        result_dict["input_tokens"]     = result.input_tokens
        result_dict["output_tokens"]    = result.output_tokens
        result_dict["total_tokens"]     = result.total_tokens
        result_dict["cost_usd"]         = result.cost_usd

        # Tool counts
        _, total_calls = result.get_cumulative_tool_counts()
        result_dict["tool_calls_total"] = total_calls
        result_dict["api_tool_calls"]   = result.get_api_tool_calls()

        # Cycle count
        result_dict["cycle_count"]      = result.cycle_count

        # Per-tool breakdown (for tools CSV) — List[Dict], pickle-safe
        result_dict["tool_counts"]      = result.get_tool_counts()

        # Compute accuracy metrics if ground truth available
        if task.get("answer"):
            gt = str(task["answer"])
            pred = result.answer
            result_dict["exact_match"] = compute_exact_match(pred, gt)
            result_dict["f1_score"] = compute_f1_score(pred, gt)
            result_dict["normalized_prediction"] = normalize_text(pred)
            result_dict["normalized_ground_truth"] = normalize_text(gt)


        result_dict["task_metadata"] = {
            "num_nodes": len(task.get("nodes", {})),
            "has_reasoning_chain": "reasoning_chain" in task,
        }

        if result.success:
            logger.info(
                f"Completed task {task_index + 1}: "
                f"tokens={result.total_tokens} cost=${result.cost_usd:.4f} "
                f"tools={total_calls} cycles={result.cycle_count}"
            )
        else:
            logger.warning(
                f"Task {task_index + 1} finished with failure: {result.error}"
            )
        return result_dict

    except Exception as e:
        logger.error(
            f"Worker error for task {task_index + 1} ({type(e).__name__}): {e}",
            exc_info=True,
        )
        return {
            "task_id": task.get("id", task_index),
            "model": agent_config.model_id,
            "question": task.get("question", ""),
            "ground_truth": task.get("answer", ""),
            "predicted_answer": "",
            "success": False,
            "error": f"{type(e).__name__}: {e}",
        }


# ---------------------------------------------------------------------------
# BatchRunner
# ---------------------------------------------------------------------------

class BatchRunner:
    """Run DataLakeAgent on multiple tasks with parallel ProcessPoolExecutor."""

    def __init__(
        self,
        agent_config: AgentConfig,
        run_config: Optional[RunConfig] = None,
        max_workers: Optional[int] = None,
    ) -> None:
        self.agent_config = agent_config
        self.run_config = run_config or RunConfig()
        self.max_workers = max_workers or min(6, os.cpu_count() or 1)

    def run_tasks(
        self,
        tasks: List[Dict[str, Any]],
        verbose: bool = False,
        max_workers: Optional[int] = None,
        batch_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Run agent on a list of tasks in parallel."""
        num_workers = max_workers or self.max_workers
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_label = batch_name or "batch"

        if verbose:
            print(f"\nRunning {len(tasks)} tasks with {num_workers} workers...")

        results: List[tuple] = []

        import multiprocessing as _mp
        mp_ctx = _mp.get_context("spawn")
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=mp_ctx) as executor:
            future_to_index = {
                executor.submit(
                    _run_task_worker,
                    task,
                    i,
                    self.agent_config,
                    self.run_config,
                    run_id,
                    batch_label,
                ): i
                for i, task in enumerate(tasks)
            }

            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                    if verbose:
                        em = result.get("exact_match")
                        status = f" EM={em:.2f}" if em is not None else ""
                        print(f"  Task {idx + 1}/{len(tasks)} done{status}")
                except Exception as e:
                    logger.error(
                        f"Future for task {idx + 1} raised {type(e).__name__}: {e}",
                        exc_info=True,
                    )
                    results.append((idx, {
                        "task_id": tasks[idx].get("id", idx),
                        "model": self.agent_config.model_id,
                        "question": tasks[idx].get("question", ""),
                        "ground_truth": tasks[idx].get("answer", ""),
                        "predicted_answer": "",
                        "success": False,
                        "error": f"{type(e).__name__}: {e}",
                    }))
                    if verbose:
                        print(f"  Task {idx + 1}/{len(tasks)} FAILED: {type(e).__name__}: {e}")

        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]

    def run_from_files(
        self,
        task_files: List[str],
        verbose: bool = False,
        max_workers: Optional[int] = None,
        batch_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Load tasks from JSON files and run them."""
        import json

        tasks = []
        for path in task_files:
            with open(path) as f:
                task = json.load(f)
                task["id"] = path
                tasks.append(task)

        if not batch_name and task_files:
            try:
                batch_name = Path(os.path.commonpath(task_files)).name
            except Exception:
                pass

        return self.run_tasks(
            tasks, verbose=verbose, max_workers=max_workers, batch_name=batch_name
        )
