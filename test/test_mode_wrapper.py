import json
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
from strands_evaluation.tools.external.ideal.plan_store import (
    get_task_context,
    set_plans_root,
    set_task_context,
)


class TestModeWrapper(unittest.TestCase):
    def _write_valid_plan(
        self,
        plans_root: Path,
        *,
        task_name: str = "task_1.json",
        reasoning_chain_text: str = "1. Gold reasoning step.",
    ) -> None:
        target = plans_root / "k-1-d-1"
        target.mkdir(parents=True, exist_ok=True)
        (target / task_name).write_text(
            json.dumps(
                {
                    "dataset_sequence": ["ds_one"],
                    "source_sequence": ["datagov/ds_one/files/rows.txt"],
                    "reasoning_chain_text": reasoning_chain_text,
                }
            )
        )

    def tearDown(self) -> None:
        set_plans_root("plans_mini")
        set_task_context({})

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
            search_results_mode="naive",
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
        self.assertIn("search_schema", prompt)
        self.assertIn("search_prefix", prompt)
        self.assertNotIn("search_value", prompt)
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
        self.assertIn("search_schema", prompt)
        self.assertNotIn("search_value", prompt)
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
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            self._write_valid_plan(plans_root)
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
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )
            tool_names = [tool_obj.tool_spec["name"] for tool_obj in bundle.tools]
            self.assertIn("plan_ideal", tool_names)
            self.assertNotIn("plan", tool_names)
            self.assertIn("summarize_context", tool_names)
            self.assertIn("search_ideal", bundle.search_tool_names)
            self.assertTrue(bundle.enable_skills)
            self.assertTrue(bundle.enable_stagnation)

    def test_ideal_management_stores_task_context_for_plan_loading(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            self._write_valid_plan(plans_root, task_name="task_6.json")
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="ideal",
                system_prompt="BASE_PROMPT",
            )
            build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_6.json"},
            )
            self.assertEqual(
                get_task_context().get("task_id"),
                "tasks_mini/k-1-d-1/task_6.json",
            )

    def test_ideal_management_preloads_gold_reasoning_chain_into_prompt(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            self._write_valid_plan(
                plans_root,
                reasoning_chain_text="1. Gold reasoning step.\n2. Gold reasoning step two.",
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
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )

            self.assertIn("## GOLD REASONING CHAIN", bundle.system_prompt)
            self.assertIn("1. Gold reasoning step.", bundle.system_prompt)
            self.assertIn("2. Gold reasoning step two.", bundle.system_prompt)
            self.assertNotIn("## IDEAL EXECUTION PLAN", bundle.system_prompt)

    def test_standard_management_prompt_matches_standard_search_tools(self):
        cfg = RunConfig(
            search_tool_mode="standard",
            search_results_mode="naive",
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
                '{"dataset_sequence":["ds_one"],"source_sequence":["datagov/ds_one/files/rows.txt"],"reasoning_chain_text":"Step 1"}'
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
            search_results_mode="naive",
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
                '{"dataset_sequence":["ds_one"],"source_sequence":["datagov/ds_one/files/rows.txt"],"reasoning_chain_text":"Step 1"}'
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

    def test_ideal_management_fails_fast_without_plan_file(self):
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
                    task_context={"task_id": "tasks_mini/k-1-d-1/task_missing.json"},
                )

    def test_ideal_management_fails_fast_with_invalid_plan_file(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "reasoning_chain_text": "Step 1",
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
            with self.assertRaises(ValueError):
                build_mode_bundle(
                    cfg,
                    data_tools=[],
                    task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
                )


if __name__ == "__main__":
    unittest.main()
