import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from strands_evaluation.config import RunConfig
from strands_evaluation.agent_with_mode import build_mode_bundle
from strands_evaluation.tools.external.ideal.plan_store import set_plans_root


class TestModeWrapper(unittest.TestCase):
    def tearDown(self) -> None:
        set_plans_root("plans_mini")

    def test_naive_modes_disable_skills(self):
        cfg = RunConfig(
            search_tool_mode="naive",
            search_results_mode="naive",
            agent_management_mode="naive",
            system_prompt="BASE_PROMPT",
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertEqual(bundle.modes["search_tool"], "naive")
        self.assertEqual(bundle.modes["search_results"], "naive")
        self.assertEqual(bundle.modes["agent_management"], "naive")
        self.assertFalse(bundle.enable_skills)
        self.assertFalse(bundle.enable_stagnation)
        self.assertIn("search_value", bundle.search_tool_names)

    def test_ideal_management_injects_reasoning_chain(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["foo_dataset", "bar_dataset"],
                        "reasoning_chain_text": "Step 1\nStep 2",
                    }
                )
            )
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="ideal",
                system_prompt="BASE_PROMPT",
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={
                    "task_id": "tasks_mini/k-1-d-1/task_1.json",
                },
            )
            self.assertIn("GOLD REASONING CHAIN", bundle.system_prompt)
            self.assertIn("Step 1", bundle.system_prompt)
            self.assertIn("Step 2", bundle.system_prompt)
            self.assertIn("IDEAL SEARCH TOOLING OVERRIDE", bundle.system_prompt)
            self.assertIn("search_ideal", bundle.search_tool_names)
            self.assertNotIn("search_value", bundle.search_tool_names)
            self.assertFalse(bundle.enable_skills)

    def test_ideal_management_hard_fails_without_plan_file(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            plans_root.mkdir(parents=True, exist_ok=True)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="ideal",
                system_prompt="BASE_PROMPT",
            )
            with self.assertRaises(FileNotFoundError):
                build_mode_bundle(
                    cfg,
                    data_tools=[],
                    task_context={
                        "task_id": "tasks_mini/k-1-d-1/task_missing.json",
                    },
                )


if __name__ == "__main__":
    unittest.main()
