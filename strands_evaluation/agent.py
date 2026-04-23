"""
Strands-native agent runner for the Data Lake benchmark.

Replaces the hand-rolled agent_runner.py with a clean Strands Agent skeleton
that wires together:
  - built-in conversation management  (summarizing or sliding-window)
  - ToolLimitPlugin                   (stops after max_tool_calls)
  - LoggingCallbackHandler            (structured per-turn logging)
"""

import concurrent.futures
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from strands import Agent
from strands.tools.executors import SequentialToolExecutor, ConcurrentToolExecutor
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
from strands_evaluation.helper.logger import configure_worker_logging
from strands_evaluation.helper.prompting import (
    compose_baseline_prompt,
    compose_managed_prompt,
    inject_debug_prompt,
    skill_paths_for_modes,
)
from strands_evaluation.helper.agent_runtime import invoke_with_watchdog
from strands_evaluation.helper.conversation import build_conversation_manager
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
from strands_evaluation.tools.external.search_eval_tools import (
    build_search_tools,
    search_tool_names_in,
)

logger = logging.getLogger(__name__)

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


# Shared callback tracking and plugin classes are defined in
# strands_evaluation.instrumentation.agent_plugins.


# ---------------------------------------------------------------------------
# DataLakeAgent
# ---------------------------------------------------------------------------

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
    ) -> tuple:
        cond = self.run_config.condition_config
        condition = _resolve_condition(cond)
        if condition in {"baseline", "b"} and not _CONDITION_B_TOOLS_AVAILABLE:
            raise RuntimeError("Condition B/Baseline search tools are unavailable (import failed).")

        # Core data-manipulation tools shared across all conditions
        _data_tools = [
            list_files, peek_file, peek_multiple, read_file, grep_file,
            query_file, download, execute_code, get_sandbox_info, cleanup_sandbox,
            submit_answer,
        ]

        if condition == "b" and _CONDITION_B_TOOLS_AVAILABLE:
            # Condition B (planning-rich): sparse search + prefix + plan tool + skills
            # summarize_context only given to B — longer planning loops benefit from manual context control
            raw_search_tools = [search_value_b, search_schema_b, search_prefix]
            system_prompt = compose_managed_prompt("naive")
            search_tools = build_search_tools(
                raw_search_tools,
                fixed_k=self.run_config.search_k,
                search_descriptions=self.run_config.search_descriptions,
            )
            tools = search_tools + [plan] + _data_tools + [summarize_context]

        else:
            # Baseline: Condition B search tools (BM25 + schema + prefix) without any context tools
            raw_search_tools = [search_value_b, search_schema_b, search_prefix]
            system_prompt = compose_baseline_prompt("naive")
            search_tools = build_search_tools(
                raw_search_tools,
                fixed_k=self.run_config.search_k,
                search_descriptions=self.run_config.search_descriptions,
            )
            tools = search_tools + _data_tools

        search_tool_names = search_tool_names_in(search_tools)

        system_prompt = _inject_search_budget_prompt(
            system_prompt,
            self.run_config.search_calls_limit,
            search_tool_names,
        )
        system_prompt = inject_debug_prompt(system_prompt, self.run_config.debug_mode)

        conv_manager = build_conversation_manager(self.run_config)

        if self.run_config.tool_executor == "sequential":
            tool_executor = SequentialToolExecutor()
        else:
            tool_executor = ConcurrentToolExecutor()

        _tool_limit_handler = ToolLimitSteeringHandler(
            self.run_config.max_tool_calls,
            self.run_config.timeout_seconds,
            submit_only_max_tokens=self.run_config.submit_only_max_tokens,
        )

        def _callback(**kwargs):
            telemetry(**kwargs)
            event_loop_tracker(**kwargs)
            if kwargs.get("force_stop", False):
                reason = kwargs.get("force_stop_reason", "")
                if "ValidationException" in reason or "too long" in reason:
                    _tool_limit_handler.signal_context_overflow()

        cond = self.run_config.condition_config
        plugins = [_tool_limit_handler, telemetry]
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
        if condition == "b":
            plugins.append(AgentSkills(skills=skill_paths_for_modes("naive", "standard")))
            if self.run_config.max_consecutive_category > 0:
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
            agent, read_tracer = self._build_agent(telemetry, trace_attributes=trace_attributes)
            hard_deadline = (
                start
                + self.run_config.timeout_seconds
                + self.run_config.submit_grace_seconds
            )
            outcome = invoke_with_watchdog(
                agent,
                question,
                hard_deadline=hard_deadline,
                timeout_seconds=self.run_config.timeout_seconds,
                submit_grace_seconds=self.run_config.submit_grace_seconds,
            )
            response = outcome.response

            submitted = get_submitted_answer()
            if outcome.timed_out and not submitted:
                elapsed = time.time() - start
                return AgentResult(
                    answer="",
                    model="",
                    model_name=self.agent_config.model_name,
                    metrics=response.metrics if response is not None else telemetry.partial_metrics,
                    elapsed_time=elapsed,
                    success=False,
                    error=outcome.timeout_reason or "Timeout reached",
                )
            retries = 0
            while not submitted and retries < 2:
                logger.warning(
                    f"Agent finished without submit_answer. Nudging (attempt {retries + 1}/2)..."
                )
                outcome = invoke_with_watchdog(
                    agent,
                    "You provided a text response but you MUST use the `submit_answer` tool "
                    "to submit your final answer. Please call the tool now.",
                    hard_deadline=hard_deadline,
                    timeout_seconds=self.run_config.timeout_seconds,
                    submit_grace_seconds=self.run_config.submit_grace_seconds,
                )
                response = outcome.response
                submitted = get_submitted_answer()
                if outcome.timed_out and not submitted:
                    elapsed = time.time() - start
                    return AgentResult(
                        answer="",
                        model="",
                        model_name=self.agent_config.model_name,
                        metrics=response.metrics if response is not None else telemetry.partial_metrics,
                        elapsed_time=elapsed,
                        success=False,
                        error=outcome.timeout_reason or "Timeout reached",
                    )
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
            unique_tool_suffix = (
                f" across {telemetry.unique_tool_calls} tool uses"
                if telemetry.unique_tool_calls and telemetry.unique_tool_calls != telemetry.tool_calls
                else ""
            )
            logger.error(
                f"Agent crashed after {telemetry.tool_calls} tool starts{unique_tool_suffix} "
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

    configure_worker_logging(
        run_config,
        model=log_model_name,
        condition=run_config.condition_config.condition,
        task_id=task.get("id"),
    )

    # Eagerly load the hybrid search DB + embedding model + cross-encoder reranker once
    # per worker process (singletons in api.py guard against re-loading on subsequent tasks).
    condition = _resolve_condition(run_config.condition_config)

    if condition == "b" and _CONDITION_B_TOOLS_AVAILABLE:
        try:
            import strands_evaluation.tools.external.search_b_tools as _sb
            if run_config.search_db_path:
                _sb.set_db_path(run_config.search_db_path)
            _sb.setup()
        except Exception as e:
            logger.warning(f"Sparse search setup failed: {e}")

    try:
        logger.info(f"Starting task {task_index + 1}: {task.get('question', '')[:80]}...")

        da = DataLakeAgent(agent_config, run_config)

        cond = run_config.condition_config
        gold_ids = task.get("datasets_used", [])
        task_id = task.get("id", str(task_index))
        set_trace_context(task_id, gold_ids, cond.trace_output_dir)

        result = da.run(task["question"])

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
        result_dict["cached_input_tokens"] = result.cached_input_tokens
        result_dict["uncached_input_tokens"] = result.uncached_input_tokens
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
                f"input={result.input_tokens} cached_input={result.cached_input_tokens} "
                f"uncached_input={result.uncached_input_tokens} output={result.output_tokens} "
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
