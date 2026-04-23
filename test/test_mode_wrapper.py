import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from strands_evaluation.config import RunConfig
from strands_evaluation.agent_with_mode import build_mode_bundle
from strands_evaluation.helper.prompting import (
    compose_baseline_prompt,
    compose_managed_prompt,
    compose_preloaded_block,
    inject_debug_prompt,
    normalize_debug_mode,
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
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertIn("search_reranked", bundle.search_tool_names)
        self.assertNotIn("search_ideal", bundle.search_tool_names)

    def test_managed_naive_prompt_mentions_sparse_search_only(self):
        prompt = compose_managed_prompt("naive")
        self.assertIn("search_value", prompt)
        self.assertIn("search_schema", prompt)
        self.assertIn("search_prefix", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_managed_standard_prompt_mentions_reranked_search(self):
        prompt = compose_managed_prompt("standard")
        self.assertIn("search_reranked", prompt)
        self.assertIn("search_schema", prompt)
        self.assertIn("search_prefix", prompt)
        self.assertNotIn("search_value", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_managed_ideal_prompt_mentions_only_search_ideal(self):
        prompt = compose_managed_prompt("ideal")
        self.assertIn("search_ideal", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("search_value", prompt)
        self.assertNotIn("search_schema", prompt)
        self.assertNotIn("search_prefix", prompt)
        self.assertNotIn("reasoning chain", prompt.lower())

    def test_managed_preloaded_prompt_mentions_authoritative_preloaded_regime(self):
        prompt = compose_managed_prompt("preloaded")
        self.assertIn("PRELOADED DATASETS", prompt)
        self.assertIn("Do not search", prompt)
        self.assertNotIn("search_ideal", prompt)
        self.assertNotIn("search_reranked", prompt)

    def test_baseline_prompt_mentions_reranked_search_in_standard_mode(self):
        prompt = compose_baseline_prompt("standard")
        self.assertIn("search_reranked", prompt)
        self.assertIn("search_schema", prompt)
        self.assertNotIn("search_value", prompt)
        self.assertNotIn("search_ideal", prompt)

    def test_baseline_prompt_mentions_only_search_ideal_in_ideal_mode(self):
        prompt = compose_baseline_prompt("ideal")
        self.assertIn("search_ideal", prompt)
        self.assertNotIn("search_reranked", prompt)
        self.assertNotIn("reasoning chain", prompt.lower())

    def test_compose_preloaded_block_lists_dataset_ids_and_uris(self):
        block = compose_preloaded_block(
            [
                "datagov/ds_one/files/rows.txt",
                "wikipedia/Cameron_County,_Texas/content.txt",
            ]
        )
        self.assertIn("dataset_id: ds_one | uri: datagov/ds_one/files/rows.txt", block)
        self.assertIn(
            "dataset_id: Cameron_County,_Texas | uri: wikipedia/Cameron_County,_Texas/content.txt",
            block,
        )

    def test_skill_paths_are_search_and_management_aware(self):
        standard_paths = skill_paths_for_modes("standard", "standard")
        ideal_paths = skill_paths_for_modes("ideal", "ideal")
        preloaded_paths = skill_paths_for_modes("preloaded", "standard")
        self.assertIn("strands_evaluation/tools/skills/plan-agent", standard_paths)
        self.assertIn("strands_evaluation/tools/skills/discover-data-standard", standard_paths)
        self.assertIn("strands_evaluation/tools/skills/plan-ideal", ideal_paths)
        self.assertIn("strands_evaluation/tools/skills/discover-data-ideal", ideal_paths)
        self.assertIn("strands_evaluation/tools/skills/plan-agent", preloaded_paths)
        self.assertIn("strands_evaluation/tools/skills/query-data", preloaded_paths)
        self.assertFalse(any("discover-data" in path for path in preloaded_paths))

    def test_ideal_management_uses_managed_stack_with_plan_swap(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            self._write_valid_plan(plans_root)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="ideal",
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
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )
            self.assertIn("search_ideal", bundle.system_prompt)
            self.assertNotIn("search_reranked", bundle.system_prompt)
            self.assertNotIn("reasoning chain", bundle.system_prompt.lower())

    def test_debug_decision_notes_are_injected_for_mode_bundle(self):
        cfg = RunConfig(
            search_tool_mode="standard",
            search_results_mode="naive",
            agent_management_mode="naive",
            debug_mode="decision_notes",
        )
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertIn("## DEBUG DECISION NOTES", bundle.system_prompt)
        self.assertIn("goal:", bundle.system_prompt)
        self.assertIn("why_this_tool:", bundle.system_prompt)
        self.assertIn("what_success_looks_like:", bundle.system_prompt)
        self.assertIn("confidence: <low|medium|high>", bundle.system_prompt)

    def test_inject_debug_prompt_noops_when_disabled(self):
        self.assertEqual("BASE_PROMPT", inject_debug_prompt("BASE_PROMPT", None))
        self.assertEqual("BASE_PROMPT", inject_debug_prompt("BASE_PROMPT", "none"))

    def test_normalize_debug_mode_rejects_unknown_value(self):
        self.assertEqual("decision_notes", normalize_debug_mode("decision_notes"))
        self.assertIsNone(normalize_debug_mode(None))
        with self.assertRaises(ValueError):
            normalize_debug_mode("full_cot")

    def test_ideal_management_fails_fast_without_plan_file(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            plans_root.mkdir(parents=True, exist_ok=True)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="ideal",
                agent_management_mode="ideal",
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
            )
            with self.assertRaises(ValueError):
                build_mode_bundle(
                    cfg,
                    data_tools=[],
                    task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
                )

    def test_preloaded_mode_disables_search_tools_and_injects_authoritative_sources(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            self._write_valid_plan(plans_root)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="preloaded",
                search_results_mode="ideal",
                agent_management_mode="standard",
            )
            bundle = build_mode_bundle(
                cfg,
                data_tools=[],
                task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
            )

            tool_names = [tool_obj.tool_spec["name"] for tool_obj in bundle.tools]
            self.assertEqual(bundle.search_tool_names, ())
            self.assertNotIn("search_ideal", tool_names)
            self.assertIn("plan", tool_names)
            self.assertIn("summarize_context", tool_names)
            self.assertIn("## PRELOADED DATASETS", bundle.system_prompt)
            self.assertIn("dataset_id: ds_one | uri: datagov/ds_one/files/rows.txt", bundle.system_prompt)

    def test_preloaded_mode_fails_fast_without_plan_file(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            plans_root.mkdir(parents=True, exist_ok=True)
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="preloaded",
                search_results_mode="naive",
                agent_management_mode="naive",
            )
            with self.assertRaises(FileNotFoundError):
                build_mode_bundle(
                    cfg,
                    data_tools=[],
                    task_context={"task_id": "tasks_mini/k-1-d-1/task_missing.json"},
                )

    def test_preloaded_mode_fails_fast_with_empty_source_sequence(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "source_sequence": [],
                        "reasoning_chain_text": "Step 1",
                    }
                )
            )
            set_plans_root(plans_root)

            cfg = RunConfig(
                search_tool_mode="preloaded",
                search_results_mode="naive",
                agent_management_mode="standard",
            )
            with self.assertRaises(ValueError):
                build_mode_bundle(
                    cfg,
                    data_tools=[],
                    task_context={"task_id": "tasks_mini/k-1-d-1/task_1.json"},
                )


class TestSanaLevel(unittest.TestCase):
    """SANA Agent 0 (labeling) and Agent 1 (enriched peek_file).

    After the paper's preloaded-operationalization revision, SANA Agent 0 =
    preloaded/naive/naive (Oracle-Sources baseline per experimental.md §6).
    Preloaded mode requires a valid plan for source_sequence injection; set
    that up here so build_mode_bundle can compose the PRELOADED DATASETS block.
    """

    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        plans_root = Path(self._tmp.name) / "plans_mini"
        target = plans_root / "k-1-d-1"
        target.mkdir(parents=True, exist_ok=True)
        (target / "task_1.json").write_text(
            json.dumps({
                "dataset_sequence": ["ds_one"],
                "source_sequence": ["datagov/ds_one/files/rows.txt"],
                "reasoning_chain_text": "Step 1",
            })
        )
        set_plans_root(plans_root)
        self._task_context = {"task_id": "tasks_mini/k-1-d-1/task_1.json"}

    def tearDown(self) -> None:
        from strands_evaluation.tools.agent_tools_v2 import set_peek_enrichment
        set_peek_enrichment(False)
        set_plans_root("plans_mini")
        set_task_context({})
        self._tmp.cleanup()

    def test_sana_0_fills_axis_defaults_when_unset(self):
        cfg = RunConfig(sana_level=0)
        bundle = build_mode_bundle(cfg, data_tools=[], task_context=self._task_context)
        self.assertEqual(bundle.modes["search_tool"], "preloaded")
        self.assertEqual(bundle.modes["search_results"], "naive")
        self.assertEqual(bundle.modes["agent_management"], "naive")

    def test_sana_0_respects_explicit_axis_override(self):
        cfg = RunConfig(sana_level=0, search_tool_mode="naive")
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertEqual(bundle.modes["search_tool"], "naive")

    def test_sana_1_enables_peek_enrichment_flag(self):
        import strands_evaluation.tools.agent_tools_v2 as atv2
        cfg = RunConfig(sana_level=1)
        build_mode_bundle(cfg, data_tools=[], task_context=self._task_context)
        self.assertTrue(atv2._PEEK_ENRICHMENT_ENABLED)

    def test_sana_none_leaves_peek_enrichment_disabled(self):
        import strands_evaluation.tools.agent_tools_v2 as atv2
        cfg = RunConfig(sana_level=None, search_tool_mode="naive", search_results_mode="naive",
                        agent_management_mode="naive")
        build_mode_bundle(cfg, data_tools=[])
        self.assertFalse(atv2._PEEK_ENRICHMENT_ENABLED)

    def test_sana_1_injects_profile_section_into_system_prompt(self):
        cfg = RunConfig(sana_level=1)
        bundle = build_mode_bundle(cfg, data_tools=[], task_context=self._task_context)
        self.assertIn("DATASET PROFILE", bundle.system_prompt)
        self.assertIn("profile", bundle.system_prompt)
        self.assertIn("row_count", bundle.system_prompt)
        self.assertIn("top_2_rows", bundle.system_prompt)
        self.assertIn("null_rate", bundle.system_prompt)
        # SANA section is an 8-line appendage; bound the injection to ~12 extra lines.
        self.assertLessEqual(
            len(bundle.system_prompt.splitlines()),
            len(compose_baseline_prompt("preloaded").splitlines()) + 60,
        )

    def test_sana_0_does_not_inject_profile_section(self):
        cfg = RunConfig(sana_level=0)
        bundle = build_mode_bundle(cfg, data_tools=[], task_context=self._task_context)
        self.assertNotIn("DATASET PROFILE", bundle.system_prompt)

    def test_sana_level_none_does_not_inject_profile_section(self):
        cfg = RunConfig(search_tool_mode="naive", search_results_mode="naive",
                        agent_management_mode="naive")
        bundle = build_mode_bundle(cfg, data_tools=[])
        self.assertNotIn("DATASET PROFILE", bundle.system_prompt)


class TestPeekFileEnrichment(unittest.TestCase):
    """Direct tests of the peek_file enrichment path (no agent build)."""

    def tearDown(self) -> None:
        from strands_evaluation.tools.agent_tools_v2 import set_peek_enrichment
        set_peek_enrichment(False)

    def test_profile_lookup_returns_none_when_uri_not_cached(self):
        from strands_evaluation.tools.agent_tools_v2 import _load_dataset_profile
        profile = _load_dataset_profile("s3://nonexistent-bucket/not-a-dataset/files/foo.txt")
        self.assertIsNone(profile)

    def test_profile_lookup_returns_dict_when_uri_is_cached(self):
        # Use a URI known to be in snippet.jsonl / table_descriptions.jsonl.
        from strands_evaluation.tools.agent_tools_v2 import _load_dataset_profile
        uri = ("s3://lakeqa-yc4103-datalake/datagov/"
               "building-and-safety-electrical-permits-submitted-before-2010-n/files/rows.txt")
        profile = _load_dataset_profile(uri)
        self.assertIsNotNone(profile, "expected cached profile for known URI")
        # At minimum snippet and description should be present; schema may or may not be keyed.
        self.assertTrue(
            "snippet" in profile or "llm_description" in profile,
            f"expected snippet or description in profile, got keys: {list(profile.keys())}",
        )


if __name__ == "__main__":
    unittest.main()
