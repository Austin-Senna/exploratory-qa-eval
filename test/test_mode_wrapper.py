import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from strands_evaluation.config import RunConfig
from strands_evaluation.agent_with_mode import build_mode_bundle
from strands_evaluation.helper.prompting import (
    compose_baseline_prompt,
    compose_condition_b_prompt,
    skill_paths_for_modes,
)
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

    def test_condition_b_naive_prompt_mentions_sparse_search_only(self):
        prompt = compose_condition_b_prompt("naive", fallback="BASE_PROMPT")
        self.assertIn("search_value", prompt)
        self.assertIn("search_schema", prompt)
        self.assertIn("search_prefix", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_condition_b_standard_prompt_mentions_reranked_search(self):
        prompt = compose_condition_b_prompt("standard", fallback="BASE_PROMPT")
        self.assertIn("search_reranked", prompt)
        self.assertIn("search_value", prompt)
        self.assertIn("search_schema", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_condition_b_ideal_prompt_mentions_only_search_ideal(self):
        prompt = compose_condition_b_prompt("ideal", fallback="BASE_PROMPT")
        self.assertIn("search_ideal", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("search_value", prompt)
        self.assertNotIn("search_schema", prompt)
        self.assertNotIn("search_prefix", prompt)
        self.assertNotIn("reasoning chain", prompt.lower())

    def test_baseline_prompt_mentions_reranked_search_in_standard_mode(self):
        prompt = compose_baseline_prompt("standard", fallback="BASE_PROMPT")
        self.assertIn("search_reranked", prompt)
        self.assertIn("search_value", prompt)
        self.assertIn("search_schema", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_baseline_prompt_mentions_only_search_ideal_in_ideal_mode(self):
        prompt = compose_baseline_prompt("ideal", fallback="BASE_PROMPT")
        self.assertIn("search_ideal", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("reasoning chain", prompt.lower())

    def test_skill_paths_are_search_and_management_aware(self):
        standard_paths = skill_paths_for_modes("standard", "standard")
        ideal_paths = skill_paths_for_modes("ideal", "ideal")
        self.assertIn("strands_evaluation/tools/skills/plan-agent", standard_paths)
        self.assertIn("strands_evaluation/tools/skills/discover-data-standard", standard_paths)
        self.assertIn("strands_evaluation/tools/skills/plan-ideal", ideal_paths)
        self.assertIn("strands_evaluation/tools/skills/discover-data-ideal", ideal_paths)

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

    def test_standard_management_prompt_matches_standard_search_tools(self):
        cfg = RunConfig(
            search_tool_mode="standard",
            search_results_mode="standard",
            agent_management_mode="standard",
            system_prompt="BASE_PROMPT",
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertIn("search_reranked", bundle.system_prompt)
        self.assertNotIn("search_ideal", bundle.system_prompt)

    def test_standard_management_prompt_matches_ideal_search_tools(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                '{"dataset_sequence":["ds_one"],"reasoning_chain_text":"Step 1"}'
            )
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="standard",
                system_prompt="BASE_PROMPT",
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )
            self.assertIn("search_ideal", bundle.system_prompt)
            self.assertNotIn("search_reranked", bundle.system_prompt)
            self.assertNotIn("search_value", bundle.system_prompt)

    def test_naive_management_prompt_matches_standard_search_tools(self):
        cfg = RunConfig(
            search_tool_mode="standard",
            search_results_mode="standard",
            agent_management_mode="naive",
            system_prompt="BASE_PROMPT",
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertIn("search_reranked", bundle.system_prompt)
        self.assertNotIn("search_ideal", bundle.system_prompt)

    def test_naive_management_prompt_matches_ideal_search_tools(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                '{"dataset_sequence":["ds_one"],"reasoning_chain_text":"Step 1"}'
            )
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="naive",
                system_prompt="BASE_PROMPT",
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )
            self.assertIn("search_ideal", bundle.system_prompt)
            self.assertNotIn("search_reranked", bundle.system_prompt)
            self.assertNotIn("reasoning chain", bundle.system_prompt.lower())

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
