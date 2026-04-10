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

    def test_standard_search_includes_reranked(self):
        cfg = RunConfig(
            search_tool_mode="standard",
            search_results_mode="standard",
            agent_management_mode="naive",
            system_prompt="BASE_PROMPT",
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertIn("search_reranked", bundle.search_tool_names)
        self.assertNotIn("search_ideal", bundle.search_tool_names)

    def test_ideal_management_uses_condition_b_stack_with_plan_swap(self):
        cfg = RunConfig(
            search_tool_mode="naive",
            search_results_mode="naive",
            agent_management_mode="ideal",
            system_prompt="BASE_PROMPT",
        )
        bundle = build_mode_bundle(
            cfg,
            data_tools=[],
            task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
        )
        tool_names = [tool_obj.tool_spec["name"] for tool_obj in bundle.tools]
        self.assertIn("plan_ideal", tool_names)
        self.assertNotIn("plan", tool_names)
        self.assertIn("summarize_context", tool_names)
        self.assertIn("search_value", bundle.search_tool_names)
        self.assertTrue(bundle.enable_skills)
        self.assertTrue(bundle.enable_stagnation)

    def test_ideal_management_does_not_fail_without_plan_file(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            plans_root.mkdir(parents=True, exist_ok=True)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="naive",
                search_results_mode="naive",
                agent_management_mode="ideal",
                system_prompt="BASE_PROMPT",
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_missing.json"},
            )
            tool_names = [tool_obj.tool_spec["name"] for tool_obj in bundle.tools]
            self.assertIn("plan_ideal", tool_names)


if __name__ == "__main__":
    unittest.main()
