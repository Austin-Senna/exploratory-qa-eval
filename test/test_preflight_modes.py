import io
import json
import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from strands_evaluation.config import RunConfig
import strands_evaluation.preflight as preflight
from strands_evaluation.preflight import PreflightError, run_preflight
from strands_evaluation.tools.external.ideal import search_wrapper
from strands_evaluation.tools.external.ideal.plan_store import set_plans_root


class PreflightModeTests(unittest.TestCase):
    def tearDown(self) -> None:
        set_plans_root("plans_mini")
        search_wrapper._DESC_CACHE_LOADED = False
        search_wrapper._DESC_BY_URI = {}
        search_wrapper._DESC_ROW_BY_URI = {}

    def test_search_results_ideal_checks_profile_and_fallback_artifacts(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            db_path = root / "lance_data"
            (db_path / "lakeqa.lance").mkdir(parents=True)
            desc_path = root / "table_descriptions.jsonl"
            snippet_path = root / "snippet.jsonl"
            schemas_path = root / "datagov_tables_schemas_full.jsonl"
            profiles_path = root / "datagov_tables_profiles.jsonl"
            uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
            desc_path.write_text(json.dumps({"dataset_uri": uri, "description": "desc"}) + "\n")
            snippet_path.write_text(json.dumps({"dataset_uri": uri, "dataset_snippet": "snippet"}) + "\n")
            schemas_path.write_text(
                json.dumps(
                    {
                        "dataset_slug": "foo",
                        "tables": [
                            {
                                "relative_path": "files/rows.csv",
                                "table_kind": "delimited_text",
                                "columns": ["a"],
                            }
                        ],
                    }
                )
                + "\n"
            )
            profiles_path.write_text(json.dumps({"s3_uri": uri, "slug": "foo", "filename": "rows"}) + "\n")
            cfg = RunConfig(
                search_tool_mode="standard",
                search_results_mode="ideal",
                plan_mode="naive",
                search_db_path=str(db_path),
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", desc_path))
                stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
                stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schemas_path))
                stack.enter_context(patch.object(preflight, "_PROFILES_PATH", profiles_path))
                checks = run_preflight(cfg, [], stream=io.StringIO())

        names = [check.name for check in checks]
        self.assertIn("datagov_tables_profiles.jsonl", names)
        self.assertIn("snippet.jsonl", names)
        self.assertIn("datagov_tables_schemas_full.jsonl", names)

    def test_search_results_ideal_fails_when_profiles_missing(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            db_path = root / "lance_data"
            (db_path / "lakeqa.lance").mkdir(parents=True)
            desc_path = root / "table_descriptions.jsonl"
            snippet_path = root / "snippet.jsonl"
            schemas_path = root / "datagov_tables_schemas_full.jsonl"
            profiles_path = root / "missing_profiles.jsonl"
            uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
            desc_path.write_text(json.dumps({"dataset_uri": uri, "description": "desc"}) + "\n")
            snippet_path.write_text(json.dumps({"dataset_uri": uri, "dataset_snippet": "snippet"}) + "\n")
            schemas_path.write_text(
                json.dumps({"dataset_slug": "foo", "tables": []}) + "\n"
            )
            cfg = RunConfig(
                search_tool_mode="standard",
                search_results_mode="ideal",
                plan_mode="naive",
                search_db_path=str(db_path),
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", desc_path))
                stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
                stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schemas_path))
                stack.enter_context(patch.object(preflight, "_PROFILES_PATH", profiles_path))
                with self.assertRaises(PreflightError):
                    run_preflight(cfg, [], stream=io.StringIO())

    def test_ideal_computation_preflight_allows_missing_code_and_query_records(self):
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
                plan_mode="naive",
                computation_tool_mode="ideal",
            )

            checks = run_preflight(
                cfg,
                ["tasks_mini/k-1-d-1/task_1.json"],
                stream=io.StringIO(),
            )

        by_name = {check.name: check for check in checks}
        self.assertIn("ideal_query:tasks_mini/k-1-d-1/task_1.json", by_name)
        self.assertIn("ideal_code:tasks_mini/k-1-d-1/task_1.json", by_name)
        self.assertIn("no authored ideal_query records", by_name["ideal_query:tasks_mini/k-1-d-1/task_1.json"].detail)
        self.assertIn("no authored ideal_code records", by_name["ideal_code:tasks_mini/k-1-d-1/task_1.json"].detail)

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
                plan_mode="naive",
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

    def test_ideal_search_preflight_checks_tasks_mini_source_description_coverage(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plans_root = root / "plans_mini"
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
            table_desc_path = root / "table_descriptions.jsonl"
            table_desc_path.write_text(
                json.dumps(
                    {
                        "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_one/files/rows.txt",
                        "description": "Task mini source description",
                    }
                )
                + "\n"
            )
            set_plans_root(plans_root)
            cfg = RunConfig(
                search_tool_mode="ideal",
                search_results_mode="naive",
                plan_mode="naive",
            )

            with patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", table_desc_path):
                checks = run_preflight(
                    cfg,
                    ["tasks_mini/k-1-d-1/task_1.json"],
                    stream=io.StringIO(),
                )

        by_name = {check.name: check for check in checks}
        self.assertEqual(
            by_name["tasks_mini plan source description coverage"].detail,
            "covered 1 planned source(s)",
        )


if __name__ == "__main__":
    unittest.main()
