import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from strands_evaluation.tools.external.ideal import computation_ideal
from strands_evaluation.tools.external.ideal.plan_store import (
    set_plans_root,
    set_task_context,
)


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
        self.assertTrue(result["ideal_oracle"])
        self.assertEqual(result["answer"], 7)
        self.assertEqual(result["node_id"], "1")

    def test_execute_ideal_returns_plan_answer_on_match(self):
        result = computation_ideal.execute_ideal._tool_func(
            code="print(3 + 4)",
            intent="sum values",
        )

        self.assertTrue(result["success"])
        self.assertTrue(result["ideal_oracle"])
        self.assertEqual(result["answer"], "7")
        self.assertEqual(result["node_id"], "2")

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
        self.assertFalse(result["ideal_oracle"])
        self.assertEqual(result["repair_attempts"], 1)
        repair.assert_called_once()
        base.assert_called_once()
        self.assertEqual(base.call_args.kwargs["sql"], "SELECT 7 AS n")

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
        self.assertFalse(result["ideal_oracle"])
        self.assertEqual(result["repair_attempts"], 2)
        self.assertEqual(repair.call_count, 2)
        self.assertIn("transient", result["repairs"][0]["error"])

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

        self.assertFalse(result["ideal_oracle"])
        self.assertEqual(result["repair_attempts"], 1)
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
        self.assertFalse(result["ideal_oracle"])
        self.assertEqual(result["repair_attempts"], 2)
        self.assertIn("ValueError", result["error"])


if __name__ == "__main__":
    unittest.main()
