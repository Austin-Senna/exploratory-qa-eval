import json
import logging
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from tempfile import TemporaryDirectory
from unittest.mock import patch

from strands.hooks.events import (
    AfterModelCallEvent,
    AfterToolCallEvent,
    AgentInitializedEvent,
    BeforeModelCallEvent,
    BeforeToolCallEvent,
)

from strands_evaluation.agent_with_mode import build_mode_bundle
from strands_evaluation.config import RunConfig
from strands_evaluation.instrumentation.trace_plugin import set_trace_context
from strands_evaluation.instrumentation.agent_plugins import LoggingPlugin
from strands_evaluation.tools.agent_tools import execute_code
from strands_evaluation.tools.agent_tools_v2 import query_file
from strands_evaluation.tools.external.ideal import computation_ideal
from strands_evaluation.tools.external.ideal.plan_store import (
    load_plan_for_task,
    set_plans_root,
    set_task_context,
)

_COMPUTATION_LOG_PATH = Path("test_logs/ideal_computation_tools.jsonl")
_COMPUTATION_TRANSCRIPT_LOG_PATH = Path("test_logs/ideal_computation_tool_transcript.log")
_CORE_QUALITY_TASK_ID = "tasks_core_quality/k-1-d-1/task_2.json"


class IdealComputationToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self._plans_root = Path(self._tmp.name) / "plans_mini"
        target = self._plans_root / "k-1-d-1"
        target.mkdir(parents=True, exist_ok=True)
        (target / "task_1.json").write_text(
            json.dumps(
                {
                    "dataset_sequence": ["ds_a"],
                    "source_sequence": ["datagov/ds_a/files/rows.txt"],
                    "reasoning_chain_text": "1. Compute the answer.",
                    "ideal_query": [
                        {
                            "node_id": "1",
                            "dataset_id": "ds_a",
                            "intent": "count all rows",
                            "sql": "SELECT COUNT(*) AS n FROM t",
                            "answer": 7,
                        }
                    ],
                    "ideal_code": [
                        {
                            "node_id": "2",
                            "dataset_id": "ds_a",
                            "intent": "sum values",
                            "code": "print(3 + 4)",
                            "answer": "7",
                        }
                    ],
                }
            )
        )
        set_plans_root(self._plans_root)
        computation_ideal.reset_state()
        computation_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})

    def tearDown(self) -> None:
        computation_ideal.reset_state()
        set_plans_root("plans_mini")
        set_task_context({})
        self._tmp.cleanup()

    def test_query_ideal_returns_plan_answer_on_match(self):
        result = computation_ideal.query_ideal._tool_func(
            dataset_id="ds_a",
            file_path="files/rows.txt",
            sql="SELECT COUNT(*) AS n FROM t",
            intent="count all rows",
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["columns"], ["answer"])
        self.assertEqual(result["rows"], [[7]])
        self.assertEqual(result["row_count"], 1)
        self.assertFalse(result["truncated"])
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("intent", result)
        self.assertNotIn("source", result)
        self.assertNotIn("node_id", result)

    def test_execute_ideal_returns_plan_answer_on_match(self):
        result = computation_ideal.execute_ideal._tool_func(
            code="print(3 + 4)",
            intent="sum values",
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["output"], "7")
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("intent", result)
        self.assertNotIn("source", result)
        self.assertNotIn("node_id", result)

    def test_query_ideal_uses_repair_fallback_when_no_oracle_match(self):
        with patch.object(
            computation_ideal,
            "_repair_query",
            return_value={"sql": "SELECT 7 AS n", "reason": "matched intent"},
        ) as repair, patch.object(
            computation_ideal,
            "_base_query_file",
            return_value={"success": True, "rows": [[7]], "columns": ["n"]},
        ) as base:
            result = computation_ideal.query_ideal._tool_func(
                dataset_id="ds_a",
                file_path="files/rows.txt",
                sql="SELECT bad FROM t",
                intent="not in the plan",
        )

        self.assertTrue(result["success"])
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("repair_attempts", result)
        self.assertNotIn("repairs", result)
        repair.assert_called_once()
        base.assert_called_once()
        self.assertEqual(base.call_args.kwargs["sql"], "SELECT 7 AS n")

    def test_query_ideal_blocked_record_returns_tool_error_without_repair(self):
        target = self._plans_root / "k-1-d-1"
        (target / "task_blocked.json").write_text(
            json.dumps(
                {
                    "dataset_sequence": ["ds_huge"],
                    "source_sequence": ["datagov/ds_huge/files/huge.csv"],
                    "reasoning_chain_text": "1. Use code against the large file.",
                    "ideal_query": [
                        {
                            "node_id": "1",
                            "dataset_id": "ds_huge",
                            "intent": "count all rows",
                            "answer": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit).",
                        }
                    ],
                    "ideal_code": [
                        {
                            "node_id": "1",
                            "dataset_id": "ds_huge",
                            "intent": "count all rows",
                            "code": "print(7)",
                            "answer": "7",
                        }
                    ],
                }
            )
        )
        computation_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_blocked.json"})

        with patch.object(computation_ideal, "_repair_query") as repair:
            result = computation_ideal.query_ideal._tool_func(
                dataset_id="ds_huge",
                file_path="files/huge.csv",
                sql="SELECT COUNT(*) FROM t",
                intent="count all rows",
            )

        self.assertFalse(result["success"])
        self.assertIn("Cannot execute SQL", result["error"])
        self.assertIn("execute_ideal", result["recommendation"])
        self.assertEqual(result["dataset_id"], "ds_huge")
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("intent", result)
        self.assertNotIn("source", result)
        repair.assert_not_called()

    def test_query_ideal_retries_after_repair_failure(self):
        with patch.object(
            computation_ideal,
            "_repair_query",
            side_effect=[
                RuntimeError("transient"),
                {"sql": "SELECT 7 AS n", "reason": "second attempt"},
            ],
        ) as repair, patch.object(
            computation_ideal,
            "_base_query_file",
            return_value={"success": True, "rows": [[7]], "columns": ["n"]},
        ):
            result = computation_ideal.query_ideal._tool_func(
                dataset_id="ds_a",
                file_path="files/rows.txt",
                sql="SELECT bad FROM t",
                intent="not in the plan",
            )

        self.assertTrue(result["success"])
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("repair_attempts", result)
        self.assertNotIn("repairs", result)
        self.assertEqual(repair.call_count, 2)

    def test_query_ideal_does_not_oracle_match_wrong_dataset(self):
        with patch.object(
            computation_ideal,
            "_repair_query",
            return_value={"sql": "SELECT 0 AS n", "reason": "wrong source"},
        ) as repair, patch.object(
            computation_ideal,
            "_base_query_file",
            return_value={"success": True, "rows": [[0]], "columns": ["n"]},
        ):
            result = computation_ideal.query_ideal._tool_func(
                dataset_id="other_ds",
                file_path="files/rows.txt",
                sql="SELECT COUNT(*) AS n FROM t",
                intent="count all rows",
            )

        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("repair_attempts", result)
        self.assertNotIn("repairs", result)
        repair.assert_called_once()

    def test_execute_ideal_returns_failure_after_repair_exhaustion(self):
        with patch.object(
            computation_ideal,
            "_repair_code",
            side_effect=[
                {"code": "raise ValueError('one')", "reason": "first"},
                {"code": "raise ValueError('two')", "reason": "second"},
            ],
        ), patch.object(
            computation_ideal,
            "_base_execute_code",
            return_value={"success": False, "error": "ValueError: still bad"},
        ):
            result = computation_ideal.execute_ideal._tool_func(
                code="raise ValueError('bad')",
                intent="not in the plan",
            )

        self.assertFalse(result["success"])
        self.assertNotIn("ideal_oracle", result)
        self.assertNotIn("repair_attempts", result)
        self.assertNotIn("repairs", result)
        self.assertIn("ValueError", result["error"])

    def test_repair_agent_calls_are_counted_and_traced(self):
        trace_root = Path(self._tmp.name) / "traces"
        set_trace_context(
            "tasks_mini/k-1-d-1/task_1.json",
            [],
            str(trace_root),
        )

        class _RepairAgent:
            def __init__(self, *args, **kwargs):
                self.tools = kwargs["tools"]
                self.plugins = kwargs.get("plugins", [])
                self.__class__.last_plugins = self.plugins

            def __call__(self, prompt: str) -> None:
                _ = prompt
                self.tools[0](code="print(7)", reason="matched authored computation")

        with patch.object(computation_ideal, "Agent", _RepairAgent), patch.object(
            computation_ideal,
            "_repair_model",
            return_value="fake-model",
        ), patch.object(
            computation_ideal,
            "_base_execute_code",
            return_value={"success": True, "output": "7"},
        ):
            result = computation_ideal.execute_ideal._tool_func(
                code="print('not a plan match')",
                intent="not in the plan",
            )

        self.assertEqual(result, {"success": True, "output": "7"})
        self.assertTrue(
            any(isinstance(plugin, LoggingPlugin) for plugin in _RepairAgent.last_plugins)
        )
        self.assertEqual(
            computation_ideal.get_stats(),
            {
                "execute_ideal_agent_repair_calls": 1,
                "query_ideal_agent_repair_calls": 0,
            },
        )
        trace_path = trace_root / "k-1-d-1" / "task_1.jsonl"
        events = [json.loads(line) for line in trace_path.read_text().splitlines()]
        self.assertEqual(
            [event["event"] for event in events],
            ["repair_agent_invoked", "repair_agent_completed"],
        )
        self.assertEqual(events[0]["tool"], "execute_ideal")
        self.assertEqual(events[0]["attempt"], 1)
        self.assertEqual(events[1]["repair_reason"], "matched authored computation")
        self.assertIn("submitted_code", events[1])

    def test_repair_stats_reset_with_task_context(self):
        with patch.object(
            computation_ideal,
            "_repair_code",
            return_value={"code": "print(7)", "reason": "fixed"},
        ), patch.object(
            computation_ideal,
            "_base_execute_code",
            return_value={"success": True, "output": "7"},
        ):
            computation_ideal.execute_ideal._tool_func(
                code="print('not a plan match')",
                intent="not in the plan",
            )

        self.assertEqual(computation_ideal.get_stats()["execute_ideal_agent_repair_calls"], 1)
        computation_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})
        self.assertEqual(
            computation_ideal.get_stats(),
            {
                "execute_ideal_agent_repair_calls": 0,
                "query_ideal_agent_repair_calls": 0,
            },
        )

    def test_execute_repair_prompt_includes_target_dataset_context(self):
        captured: dict[str, str] = {}

        class _PromptCapturingAgent:
            def __init__(self, *args, **kwargs):
                self.tools = kwargs["tools"]

            def __call__(self, prompt: str) -> None:
                captured["prompt"] = prompt
                self.tools[0](code="print(7)", reason="context was sufficient")

        with patch.object(computation_ideal, "Agent", _PromptCapturingAgent), patch.object(
            computation_ideal,
            "_repair_model",
            return_value="fake-model",
        ), patch.object(
            computation_ideal,
            "_base_execute_code",
            return_value={"success": True, "output": "7"},
        ), patch.object(
            computation_ideal,
            "_enhanced_peek_context",
            return_value='{"dataset_description": "Target dataset description", "enhanced_peek_file": {"header_columns": ["value"]}}',
        ):
            computation_ideal.execute_ideal._tool_func(
                code="print('not a plan match')",
                intent="not in the plan",
            )

        self.assertIn("Target dataset context", captured["prompt"])
        self.assertIn("Target dataset description", captured["prompt"])
        self.assertIn("enhanced_peek_file", captured["prompt"])

    def test_query_repair_prompt_includes_enhanced_peek_context(self):
        captured: dict[str, str] = {}

        class _PromptCapturingAgent:
            def __init__(self, *args, **kwargs):
                self.tools = kwargs["tools"]

            def __call__(self, prompt: str) -> None:
                captured["prompt"] = prompt
                self.tools[0](sql="SELECT 7 AS answer", reason="context was sufficient")

        with patch.object(computation_ideal, "Agent", _PromptCapturingAgent), patch.object(
            computation_ideal,
            "_repair_model",
            return_value="fake-model",
        ), patch.object(
            computation_ideal,
            "_base_query_file",
            return_value={"success": True, "rows": [[7]], "columns": ["answer"]},
        ), patch.object(
            computation_ideal,
            "_enhanced_peek_context",
            return_value='{"dataset_description": "Target query description", "enhanced_peek_file": {"header_columns": ["n"]}}',
        ):
            computation_ideal.query_ideal._tool_func(
                dataset_id="ds_a",
                file_path="files/rows.txt",
                sql="SELECT bad FROM t",
                intent="not in the plan",
            )

        self.assertIn("Target dataset context", captured["prompt"])
        self.assertIn("Target query description", captured["prompt"])
        self.assertIn("enhanced_peek_file", captured["prompt"])

    def test_ideal_computation_tools_log_results(self):
        plan = load_plan_for_task(_CORE_QUALITY_TASK_ID)
        query_record = plan.ideal_query[0]
        code_record = plan.ideal_code[0]
        query_file_path = query_record.source.split(f"/{query_record.dataset_id}/", 1)[-1]

        cfg = RunConfig(
            search_tool_mode="preloaded",
            search_results_mode="naive",
            agent_management_mode="naive",
            computation_tool_mode="ideal",
        )
        bundle = build_mode_bundle(
            cfg,
            data_tools=[query_file, execute_code],
            task_context={"task_id": _CORE_QUALITY_TASK_ID},
        )
        tool_by_name = {
            tool_obj.tool_spec["name"]: tool_obj
            for tool_obj in bundle.tools
            if hasattr(tool_obj, "tool_spec")
        }

        plugin = LoggingPlugin()
        agent = SimpleNamespace()
        log_logger = logging.getLogger("strands_evaluation.instrumentation.agent_plugins")
        previous_level = log_logger.level
        _COMPUTATION_TRANSCRIPT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(_COMPUTATION_TRANSCRIPT_LOG_PATH, mode="w", encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
        log_logger.setLevel(logging.DEBUG)
        log_logger.addHandler(handler)

        def run_logged_tool(tool_name: str, tool_input: dict) -> dict:
            tool_use = {
                "name": tool_name,
                "toolUseId": f"{tool_name}-1",
                "input": tool_input,
            }
            plugin.on_before_model(BeforeModelCallEvent(agent=agent, invocation_state={}))
            plugin.on_after_model(
                AfterModelCallEvent(
                    agent=agent,
                    invocation_state={},
                    stop_response=AfterModelCallEvent.ModelStopResponse(
                        message={
                            "role": "assistant",
                            "content": [{"toolUse": tool_use}],
                        },
                        stop_reason="tool_use",
                    ),
                )
            )
            plugin.on_before_tool(
                BeforeToolCallEvent(
                    agent=agent,
                    selected_tool=tool_by_name[tool_name],
                    tool_use=tool_use,
                    invocation_state={},
                )
            )
            result = tool_by_name[tool_name](**tool_input)
            plugin.on_after_tool(
                AfterToolCallEvent(
                    agent=agent,
                    selected_tool=tool_by_name[tool_name],
                    tool_use=tool_use,
                    invocation_state={},
                    result={
                        "toolUseId": tool_use["toolUseId"],
                        "status": "success",
                        "content": [{"text": json.dumps(result, sort_keys=True)}],
                    },
                )
            )
            return result

        try:
            plugin.on_agent_initialized(AgentInitializedEvent(agent=agent))
            query_result = run_logged_tool(
                "query_ideal",
                {
                    "dataset_id": query_record.dataset_id,
                    "file_path": query_file_path,
                    "sql": query_record.payload,
                    "intent": query_record.intent,
                },
            )
            execute_result = run_logged_tool(
                "execute_ideal",
                {
                    "code": code_record.payload,
                    "intent": code_record.intent,
                },
            )
        finally:
            log_logger.removeHandler(handler)
            log_logger.setLevel(previous_level)
            handler.close()

        self.assertEqual(bundle.modes["computation_tool"], "ideal")
        self.assertIn("query_ideal", tool_by_name)
        self.assertIn("execute_ideal", tool_by_name)
        self.assertNotIn("query_file", tool_by_name)
        self.assertNotIn("execute_code", tool_by_name)
        self.assertTrue(query_result["success"])
        self.assertEqual(query_result["columns"], ["answer"])
        self.assertEqual(query_result["rows"], [[query_record.answer]])
        self.assertEqual(query_result["row_count"], 1)
        self.assertFalse(query_result["truncated"])
        self.assertNotIn("ideal_oracle", query_result)
        self.assertNotIn("intent", query_result)
        self.assertNotIn("source", query_result)
        self.assertTrue(execute_result["success"])
        self.assertEqual(execute_result["output"], str(code_record.answer))
        self.assertNotIn("ideal_oracle", execute_result)
        self.assertNotIn("intent", execute_result)
        self.assertNotIn("source", execute_result)

        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": _CORE_QUALITY_TASK_ID,
            "plan_path": str(plan.plan_path),
            "modes": dict(bundle.modes),
            "tool_names": sorted(tool_by_name),
            "results": {
                "query_ideal": {
                    "success": query_result.get("success"),
                    "dataset_id": query_result.get("dataset_id"),
                    "s3_uri": query_result.get("s3_uri"),
                    "columns": query_result.get("columns"),
                    "rows": query_result.get("rows"),
                    "row_count": query_result.get("row_count"),
                    "result_keys": sorted(query_result.keys()),
                },
                "execute_ideal": {
                    "success": execute_result.get("success"),
                    "output": execute_result.get("output"),
                    "result_keys": sorted(execute_result.keys()),
                },
            },
        }
        _COMPUTATION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _COMPUTATION_LOG_PATH.write_text(json.dumps(row, sort_keys=True) + "\n")
        transcript = _COMPUTATION_TRANSCRIPT_LOG_PATH.read_text()
        self.assertIn("[role=assistant block=1 tool_use] query_ideal(", transcript)
        self.assertIn("Executing: query_ideal(", transcript)
        self.assertIn("Tool result:", transcript)
        self.assertIn("[role=assistant block=1 tool_use] execute_ideal(", transcript)
        self.assertIn(query_record.dataset_id, transcript)
        self.assertIn(str(query_record.answer), transcript)


if __name__ == "__main__":
    unittest.main()
