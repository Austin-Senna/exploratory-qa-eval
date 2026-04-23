import contextlib
import io
import unittest

from strands_evaluation.config import RunConfig
from strands_evaluation.preflight import run_preflight


class PreflightModeTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
