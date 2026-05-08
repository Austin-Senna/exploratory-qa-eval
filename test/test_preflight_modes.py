import contextlib
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from strands_evaluation.config import RunConfig
import strands_evaluation.preflight as preflight
from strands_evaluation.preflight import run_preflight
from strands_evaluation.tools.external.ideal.plan_store import set_plans_root


class PreflightModeTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_plans_root("plans_mini")

    def test_preloaded_mode_ignores_ideal_search_result_artifacts(self):
        cfg = RunConfig(
            search_tool_mode="preloaded",
            search_results_mode="ideal",
            agent_management_mode="ideal",
        )
        output = io.StringIO()
        checks = run_preflight(
            cfg,
            ["tasks_core_quality/k-1-d-1/task_2.json"],
            stream=output,
        )

        names = [check.name for check in checks]
        self.assertIn("prompt:managed.txt", names)
        self.assertIn("prompt:search_preloaded.txt", names)
        self.assertIn("plan:tasks_core_quality/k-1-d-1/task_2.json", names)
        self.assertNotIn("datagov_tables_schemas_full.jsonl", names)
        self.assertIn("Preflight OK", output.getvalue())

    def test_ideal_computation_preflight_requires_code_and_query_records(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "source_sequence": ["datagov/ds_one/files/rows.txt"],
                        "reasoning_chain_text": "Step 1",
                    }
                )
            )
            set_plans_root(plans_root)
            cfg = RunConfig(
                search_tool_mode="preloaded",
                search_results_mode="naive",
                agent_management_mode="naive",
                computation_tool_mode="ideal",
            )

            with self.assertRaises(preflight.PreflightError):
                run_preflight(
                    cfg,
                    ["tasks_mini/k-1-d-1/task_1.json"],
                    stream=io.StringIO(),
                )

    def test_ideal_computation_preflight_accepts_code_and_query_records(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "source_sequence": ["datagov/ds_one/files/rows.txt"],
                        "reasoning_chain_text": "Step 1",
                        "ideal_query": [
                            {
                                "node_id": "1",
                                "dataset_id": "ds_one",
                                "intent": "count rows",
                                "sql": "SELECT COUNT(*) FROM t",
                                "answer": 3,
                            }
                        ],
                        "ideal_code": [
                            {
                                "node_id": "2",
                                "dataset_id": "ds_one",
                                "intent": "sum rows",
                                "code": "print(3)",
                                "answer": 3,
                            }
                        ],
                    }
                )
            )
            set_plans_root(plans_root)
            cfg = RunConfig(
                search_tool_mode="preloaded",
                search_results_mode="naive",
                agent_management_mode="naive",
                computation_tool_mode="ideal",
            )

            checks = run_preflight(
                cfg,
                ["tasks_mini/k-1-d-1/task_1.json"],
                stream=io.StringIO(),
            )

        names = [check.name for check in checks]
        self.assertIn("ideal_query:tasks_mini/k-1-d-1/task_1.json", names)
        self.assertIn("ideal_code:tasks_mini/k-1-d-1/task_1.json", names)


if __name__ == "__main__":
    unittest.main()
