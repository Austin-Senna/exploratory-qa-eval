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
from typing import Any, Dict, List, Optional

from strands import Agent
from strands import Plugin
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.tools.executors import SequentialToolExecutor, ConcurrentToolExecutor
from strands.hooks import AfterToolCallEvent, AgentInitializedEvent, BeforeToolCallEvent
from strands.plugins import hook
from strands.vended_plugins.skills import AgentSkills
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

import logging

from strands_evaluation.config import AgentConfig, ConditionConfig, RunConfig
from strands_evaluation.instrumentation import TracePlugin, set_trace_context
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
    peek_files,
    query_file,
    read_file,
    set_sandbox_dir,
)
from strands_evaluation.tools.agent_tools import download
from strands_evaluation.tools.external.plan_tools import plan

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
    )
    _CONDITION_B_TOOLS_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# CallbackHandler
# ---------------------------------------------------------------------------

_turn_count = 0
_run_start_time = 0.0
_reasoning_buf: List[str] = []
_text_buf: List[str] = []


def _flush_buffers() -> None:
    global _reasoning_buf, _text_buf
    if _reasoning_buf:
        full_reasoning = "".join(_reasoning_buf)
        logger.debug(f"Reasoning: {full_reasoning}")
        _reasoning_buf = []
    if _text_buf:
        full_text = "".join(_text_buf)
        logger.debug(f"LLM content: {full_text}")
        _text_buf = []


def event_loop_tracker(**kwargs):
    global _turn_count, _run_start_time, _reasoning_buf, _text_buf

    if kwargs.get("init_event_loop", False):
        _turn_count = 0
        _run_start_time = time.time()
        _reasoning_buf = []
        _text_buf = []
        logger.debug("Event loop initialized")
        return

    if kwargs.get("start_event_loop", False):
        _flush_buffers()
        _turn_count += 1
        elapsed = time.time() - _run_start_time
        logger.info(f"\n--- Turn {_turn_count} (elapsed: {elapsed:.1f}s) ---")
        return

    # Accumulate reasoning text (incremental chunks)
    if kwargs.get("reasoning") and kwargs.get("reasoningText"):
        _reasoning_buf.append(kwargs["reasoningText"])
        return

    # Accumulate response text (incremental chunks)
    if "data" in kwargs and not kwargs.get("reasoning"):
        _text_buf.append(kwargs["data"])
        return

    # contentBlockStop signals end of a content block — flush buffers
    raw_event = kwargs.get("event", {})
    if raw_event.get("contentBlockStop") is not None:
        _flush_buffers()
        return

    if kwargs.get("force_stop", False):
        _flush_buffers()
        logger.debug(f"Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown')}")

# ---------------------------------------------------------------------------
# ToolLimitSteeringHandler
# ---------------------------------------------------------------------------

class ToolLimitSteeringHandler(SteeringHandler):
    """Guide the agent to call submit_answer when tool limit or timeout is reached.

    On first trigger: returns Guide so the agent gets a chance to call submit_answer.
    On second trigger (agent still hasn't submitted): hard-stops as a fallback.
    """

    name = "tool-limit"

    def __init__(self, max_tool_calls: int = 30, timeout_seconds: int = 300) -> None:
        super().__init__()
        self._max = max_tool_calls
        self._timeout = timeout_seconds
        self._count = 0
        self._start_time = 0.0
        self._guided = False  # True after we've already sent one Guide

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._count = 0
        self._start_time = time.time()
        self._guided = False

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        if event.tool_use.get("name") != "skills":
            self._count += 1

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        # Never intercept submit_answer itself
        if tool_use.get("name") == "submit_answer":
            return Proceed(reason="submit_answer is always allowed")

        elapsed = time.time() - self._start_time

        if elapsed >= self._timeout:
            reason = f"Timeout reached ({elapsed:.1f}s elapsed)."
        elif self._count >= self._max:
            reason = f"Tool limit reached ({self._count}/{self._max} calls used)."
        else:
            return Proceed(reason="within limits")

        if self._guided:
            # Already guided once — hard-stop now as a fallback
            logger.warning(f"Hard-stopping after second limit trigger: {reason}")
            return Guide(
                reason=(
                    f"{reason} You have already been warned. "
                    "Call submit_answer NOW with your best current answer. No other tools are permitted."
                )
            )

        self._guided = True
        return Guide(
            reason=(
                f"{reason} You must stop using other tools and immediately call submit_answer "
                "with your best current answer and reasoning. "
                "Do not call any other tool before submit_answer."
            )
        )


class SubmitAnswerPlugin(Plugin):
    """Stop the agent loop immediately after submit_answer is executed."""

    name = "submit-answer"

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = getattr(event, "tool_use", {}).get("name", "")
        
        if tool_name == "submit_answer" or get_submitted_answer() is not None:
            logger.info("Answer submitted! Triggering native agent cancellation.")
            # Trigger the native Strands kill switch
            event.agent.cancel()

class LoggingPlugin(Plugin):
    """Logs tool calls (with args) and tool results via BeforeToolCallEvent/AfterToolCallEvent hooks."""

    name = "logging"

    @hook
    def on_before_tool(self, event: BeforeToolCallEvent) -> None:
        tool_name = event.tool_use.get("name", "?")
        tool_input = event.tool_use.get("input", {})
        try:
            args_str = json.dumps(tool_input, ensure_ascii=False)
        except Exception:
            args_str = str(tool_input)
        logger.info(f"Executing: {tool_name}({args_str})")

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        result = event.result
        content = result.get("content", [])
        parts = []
        is_logical_error = False

        for block in content:
            if isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
                # Detect logical errors structurally: parse the JSON payload and
                # check for a top-level "error" key or success=False.
                if not is_logical_error:
                    try:
                        parsed = json.loads(block["text"])
                        if isinstance(parsed, dict) and (
                            "error" in parsed or parsed.get("success") is False
                        ):
                            is_logical_error = True
                    except (json.JSONDecodeError, TypeError):
                        pass

        # Mark the result as an error so Strands records it correctly in metrics.
        if is_logical_error:
            event.result["status"] = "error"

        result_str = " ".join(parts) if parts else str(result)
        if len(result_str) > 2000:
            result_str = result_str[:2000] + "..."

        if is_logical_error:
            logger.warning(f"Tool logical error (status=error): {result_str}")
        else:
            logger.debug(f"Tool result: {result_str}")



class TelemetryTracker:
    def __init__(self):
        self.tool_calls = 0
        self.partial_metrics = None # If strands passes metrics in the loop
        
    def __call__(self, **kwargs):
        # This is your new event_loop_tracker
        if "current_tool_use" in kwargs:
            self.tool_calls += 1
            
        # If the SDK broadcasts token usage mid-loop, catch it here
        if "metrics" in kwargs:
            self.partial_metrics = kwargs["metrics"]


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
    ) -> Agent:
        cond = self.run_config.condition_config
        condition = cond.condition

        # Core data-manipulation tools shared across all conditions
        _data_tools = [
            list_files, peek_file, peek_files, read_file, grep_file,
            query_file, download, execute_code, get_sandbox_info, cleanup_sandbox,
            submit_answer,
        ]

        if condition == "a" and _CONDITION_A_TOOLS_AVAILABLE:
            # Condition A (tools-rich): hybrid RRF + schema + reranked + shared baseline tools
            tools = [search_value_a, search_schema, search_reranked, search_prefix] + _data_tools
            system_prompt = _load_condition_prompt("a", fallback=self.run_config.system_prompt)

        elif condition == "b" and _CONDITION_B_TOOLS_AVAILABLE:
            # Condition B (planning-rich): sparse search + prefix + plan tool + skills
            tools = [search_value_b, search_prefix, plan] + _data_tools
            system_prompt = _load_condition_prompt("b", fallback=self.run_config.system_prompt)

        else:
            # Baseline: original tool set + sparse search + prefix
            tools = [search_value_b, search_prefix, search, search_keyword] + _data_tools
            system_prompt = self.run_config.system_prompt

        conv_manager = SlidingWindowConversationManager(
            window_size=self.run_config.sliding_window_k
        )

        if self.run_config.tool_executor == "sequential":
            tool_executor = SequentialToolExecutor()
        else:
            tool_executor = ConcurrentToolExecutor()

        def _callback(**kwargs):
            telemetry(**kwargs)
            event_loop_tracker(**kwargs)

        cond = self.run_config.condition_config
        plugins = [
            ToolLimitSteeringHandler(self.run_config.max_tool_calls, self.run_config.timeout_seconds),
            SubmitAnswerPlugin(),
            LoggingPlugin(),
        ]
        if condition == "b":
            plugins.append(AgentSkills(skills=[
                "strands_evaluation/tools/skills/plan-agent",
                "strands_evaluation/tools/skills/discover-data",
                "strands_evaluation/tools/skills/query-data",
            ]))
        if cond.enable_traces:
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
        )

    def run(self, question: str, session_id: Optional[str] = None) -> AgentResult:
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
            agent = self._build_agent(telemetry, trace_attributes=trace_attributes)
            response = agent(question)

            submitted = get_submitted_answer()
            retries = 0
            while not submitted and retries < 2:
                logger.warning(
                    f"Agent finished without submit_answer. Nudging (attempt {retries + 1}/2)..."
                )
                response = agent(
                    "You provided a text response but you MUST use the `submit_answer` tool "
                    "to submit your final answer and sources. Please call the tool now."
                )
                submitted = get_submitted_answer()
                retries += 1

            answer = submitted["answer"] if submitted else _clean_answer(str(response))
            elapsed = sum(response.metrics.cycle_durations)

            logger.info(f"ANSWER: {answer} ({elapsed:.1f}s)")
            return AgentResult(
                answer=answer,
                model=agent.model.config,
                model_name=self.agent_config.model_name,
                reasoning=submitted["reasoning"] if submitted else "",
                sources=submitted["sources"] if submitted else [],
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

    configure_logging(
        model=agent_config.model_name or agent_config.model_id,
        condition=run_config.condition_config.condition,
        task_id=task.get("id"),
    )

    try:
        logger.info(f"Starting task {task_index + 1}: {task.get('question', '')[:80]}...")

        da = DataLakeAgent(agent_config, run_config)

        # Wire trace context before running if traces are enabled
        cond = run_config.condition_config
        if cond.enable_traces:
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

        # Source recall/precision from task graph nodes
        if task.get("nodes"):
            expected_sources = [
                node.get("source", "") for node in task["nodes"].values()
            ]
            result_dict["expected_sources"] = expected_sources
            if result.sources:
                # Normalize to dataset_id: strip folder prefix (wikipedia/, datagov/)
                # and everything from /files/ onward, then lowercase.
                # e.g. "datagov/public-school-locations-current-23297/files/data.txt"
                #   -> "public-school-locations-current-23297"
                # e.g. "wikipedia/Sal_Khan/content.txt" -> "sal_khan"
                def _norm_source(s: str) -> str:
                    s = str(s).lower()
                    for prefix in ("wikipedia/", "datagov/"):
                        if s.startswith(prefix):
                            s = s[len(prefix):]
                            break
                    s = s.split("/")[0]
                    return s

                pred_set = {_norm_source(s) for s in result.sources}
                exp_set = {_norm_source(s) for s in expected_sources if s}
                overlap = pred_set & exp_set
                result_dict["source_recall"] = (
                    len(overlap) / len(exp_set) if exp_set else 0.0
                )
                result_dict["source_precision"] = (
                    len(overlap) / len(pred_set) if pred_set else 0.0
                )

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

        with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
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
