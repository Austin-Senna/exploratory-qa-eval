import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from strands_evaluation.config import RunConfig
from strands_evaluation.preflight import run_preflight
from strands_evaluation.tools.external.ideal.plan_store import set_plans_root, set_task_context


class IdealComputationPreflightTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_plans_root("plans_mini")
        set_task_context({})

    def test_text_only_plan_with_no_computation_records_passes(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_text.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["Text_Source"],
                        "source_sequence": ["wikipedia/Text_Source/content.txt"],
                        "reasoning_chain_text": "1. Read the text source and extract the fact.",
                        "ideal_query": [],
                        "ideal_code": [],
                    }
                )
            )
            set_plans_root(plans_root)

            stream = io.StringIO()
            checks = run_preflight(
                RunConfig(
                    search_tool_mode="preloaded",
                    search_results_mode="naive",
                    plan_mode="naive",
                    computation_tool_mode="ideal",
                ),
                ["tasks_mini/k-1-d-1/task_text.json"],
                stream=stream,
            )

            self.assertTrue(all(check.ok for check in checks), stream.getvalue())
            self.assertIn("no authored ideal_query records", stream.getvalue())
            self.assertIn("no authored ideal_code records", stream.getvalue())

