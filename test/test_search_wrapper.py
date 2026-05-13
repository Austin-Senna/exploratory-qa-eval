import json
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from strands import tool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import strands_evaluation.tools.external.ideal.search_wrapper as search_wrapper
import strands_evaluation.helper.peek_profile as profile_loader
from strands_evaluation.tools.external.ideal.search_wrapper import (
    reshape_search_payload,
    search_tool_names_in,
)


class TestSearchWrapperPayload(unittest.TestCase):
    def setUp(self) -> None:
        self._reset_caches()

    def tearDown(self) -> None:
        self._reset_caches()

    def _reset_caches(self) -> None:
        search_wrapper._DESC_CACHE_LOADED = False
        search_wrapper._DESC_BY_URI = {}
        search_wrapper._DESC_ROW_BY_URI = {}
        search_wrapper._SNIPPET_CACHE_LOADED = False
        search_wrapper._SNIPPET_BY_URI = {}
        search_wrapper._SCHEMAS_CACHE_LOADED = False
        search_wrapper._SCHEMA_BY_SLUG_FILENAME = {}
        profile_loader._PROFILES_LOADED = False
        profile_loader._PROFILE_BY_URI = {}
        profile_loader._PROFILE_BY_SLUG_FILENAME = {}

    def _patch_support_files(
        self,
        root: Path,
        *,
        uri: str,
        desc: str = "LLM description",
        snippet: str = "dataset snippet words",
        schema_kind: str = "csv",
        columns: list[str] | None = None,
        profile_rows: list[dict] | None = None,
    ) -> ExitStack:
        desc_path = root / "table_descriptions.jsonl"
        desc_path.write_text(json.dumps({"dataset_uri": uri, "description": desc}) + "\n")

        snippet_path = root / "snippet.jsonl"
        snippet_path.write_text(json.dumps({"dataset_uri": uri, "dataset_snippet": snippet}) + "\n")

        schema_path = root / "datagov_tables_schemas_full.jsonl"
        schema_path.write_text(
            json.dumps(
                {
                    "dataset_slug": "foo",
                    "tables": [
                        {
                            "relative_path": "files/rows.csv",
                            "table_kind": schema_kind,
                            "columns": columns if columns is not None else ["col_a", "col_b"],
                        }
                    ],
                }
            )
            + "\n"
        )

        profiles_path = root / "datagov_tables_profiles.jsonl"
        profiles_path.write_text(
            "".join(json.dumps(row) + "\n" for row in (profile_rows or []))
        )

        stack = ExitStack()
        stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", desc_path))
        stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
        stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schema_path))
        stack.enter_context(patch.object(profile_loader, "_PROFILES_PATH", profiles_path))
        return stack

    def test_naive_mode_returns_dataset_id_and_s3_uri(self):
        payload = {
            "results": [
                {
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                    "document": "hello world",
                    "score": "0.123",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "naive")
        self.assertEqual(out["count"], 1)
        self.assertEqual(
            out["results"][0],
            {
                "dataset_id": "foo",
                "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
            },
        )

    def test_naive_mode_preserves_unrelated_payload_keys(self):
        payload = {
            "ideal_source_driven": True,
            "task_id": "tasks_mini/k-1-d-1/task_1.json",
            "results": [
                {
                    "dataset_id": "foo",
                    "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "naive")
        self.assertEqual(
            out["results"][0],
            {
                "dataset_id": "foo",
                "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
            },
        )
        self.assertTrue(out["ideal_source_driven"])
        self.assertEqual(out["task_id"], "tasks_mini/k-1-d-1/task_1.json")

    def test_ideal_mode_enriches_results_from_sidecar_files(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt"
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(Path(tmpdir), uri=uri):
                payload = {
                    "results": [
                        {
                            "uri": uri,
                            "document": "ignored fallback text",
                        }
                    ],
                    "count": 1,
                }
                out = reshape_search_payload(payload, "ideal")

        self.assertEqual(
            out["results"][0],
            {
                "dataset_id": "foo",
                "s3_uri": uri,
                "llm_desc": "LLM description",
                "columns": ["col_a", "col_b"],
                "dataset_snippet": "dataset snippet words",
            },
        )

    def test_ideal_mode_uses_merged_table_descriptions_for_task_specific_rows(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt"
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            table_desc_path = root / "table_descriptions.jsonl"
            table_desc_path.write_text(
                json.dumps(
                    {
                        "dataset_uri": uri,
                        "description": "Merged task-specific description",
                    }
                )
                + "\n"
            )
            snippet_path = root / "snippet.jsonl"
            snippet_path.write_text(json.dumps({"dataset_uri": uri, "dataset_snippet": "snippet"}) + "\n")
            schema_path = root / "datagov_tables_schemas_full.jsonl"
            schema_path.write_text(
                json.dumps(
                    {
                        "dataset_slug": "foo",
                        "tables": [
                            {
                                "relative_path": "files/rows.txt",
                                "table_kind": "delimited_text",
                                "columns": ["name"],
                            }
                        ],
                    }
                )
                + "\n"
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", table_desc_path))
                stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
                stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schema_path))
                out = reshape_search_payload(
                    {"results": [{"uri": uri}], "count": 1},
                    "ideal",
                )

        self.assertEqual(out["results"][0]["llm_desc"], "Merged task-specific description")

    def test_ideal_mode_rejects_tasks_mini_manifest_fallback_descriptions(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt"
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            table_desc_path = root / "table_descriptions.jsonl"
            table_desc_path.write_text(
                json.dumps(
                    {
                        "dataset_uri": uri,
                        "description": "fake fallback",
                        "description_source": "tasks_mini_manifest_fallback",
                    }
                )
                + "\n"
            )

            with ExitStack() as stack:
                stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", table_desc_path))
                with self.assertRaisesRegex(ValueError, "tasks_mini_manifest_fallback"):
                    search_wrapper._load_desc_cache()

    def test_ideal_mode_uses_type_when_schema_has_no_columns(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt"
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                schema_kind="json",
                columns=[],
            ):
                payload = {
                    "results": [
                        {
                            "uri": uri,
                        }
                    ],
                    "count": 1,
                }
                out = reshape_search_payload(payload, "ideal")

        row = out["results"][0]
        self.assertEqual(row["type"], "json")
        self.assertNotIn("columns", row)

    def test_ideal_mode_prefers_profile_columns_over_schema_jsonl(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        profile = {
            "s3_uri": uri,
            "slug": "foo",
            "filename": "rows",
            "family": "csv",
            "columns": [{"name": "profile_col_a"}, {"name": "profile_col_b"}],
        }
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                columns=["schema_col"],
                profile_rows=[profile],
            ):
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        self.assertEqual(out["results"][0]["columns"], ["profile_col_a", "profile_col_b"])

    def test_ideal_mode_falls_back_to_schema_jsonl_when_profile_has_no_columns(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        profile = {
            "s3_uri": uri,
            "slug": "foo",
            "filename": "rows",
            "family": "csv",
        }
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                columns=["schema_col"],
                profile_rows=[profile],
            ):
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        self.assertEqual(out["results"][0]["columns"], ["schema_col"])

    def test_ideal_mode_prefers_profile_snippet_over_snippet_jsonl(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        profile = {
            "s3_uri": uri,
            "slug": "foo",
            "filename": "rows",
            "family": "csv",
            "snippet": "profile snippet text",
        }
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                snippet="snippet jsonl text",
                profile_rows=[profile],
            ):
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        self.assertEqual(out["results"][0]["dataset_snippet"], "profile snippet text")

    def test_ideal_mode_compacts_profile_top_rows_when_profile_snippet_missing(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        profile = {
            "s3_uri": uri,
            "slug": "foo",
            "filename": "rows",
            "family": "csv",
            "top_2_rows": [{"name": "Ada", "value": 1}, {"name": "Grace", "value": 2}],
        }
        with TemporaryDirectory() as tmpdir:
            with self._patch_support_files(
                Path(tmpdir),
                uri=uri,
                snippet="snippet jsonl text",
                profile_rows=[profile],
            ):
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        snippet = out["results"][0]["dataset_snippet"]
        self.assertIn("Ada", snippet)
        self.assertIn("Grace", snippet)
        self.assertNotEqual(snippet, "snippet jsonl text")

    def test_ideal_mode_uses_profile_description_when_table_description_missing(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        profile = {
            "s3_uri": uri,
            "slug": "foo",
            "filename": "rows",
            "family": "csv",
            "llm_description": "profile llm description",
        }
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            with self._patch_support_files(root, uri=uri, profile_rows=[profile]):
                (root / "table_descriptions.jsonl").write_text("")
                search_wrapper._DESC_CACHE_LOADED = False
                search_wrapper._DESC_BY_URI = {}
                search_wrapper._DESC_ROW_BY_URI = {}
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        self.assertEqual(out["results"][0]["llm_desc"], "profile llm description")

    def test_ideal_mode_uses_table_description_content_after_search_text_fallbacks(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.csv"
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            with self._patch_support_files(root, uri=uri):
                (root / "snippet.jsonl").write_text("")
                (root / "table_descriptions.jsonl").write_text(
                    json.dumps(
                        {
                            "dataset_uri": uri,
                            "description": "table description",
                            "content": "table description content",
                        }
                    )
                    + "\n"
                )
                search_wrapper._DESC_CACHE_LOADED = False
                search_wrapper._DESC_BY_URI = {}
                search_wrapper._DESC_ROW_BY_URI = {}
                search_wrapper._SNIPPET_CACHE_LOADED = False
                search_wrapper._SNIPPET_BY_URI = {}
                out = reshape_search_payload({"results": [{"uri": uri}], "count": 1}, "ideal")

        self.assertEqual(out["results"][0]["dataset_snippet"], "table description content")

    def test_ideal_mode_falls_back_to_search_text_when_snippet_missing(self):
        uri = "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt"
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            with self._patch_support_files(root, uri=uri):
                (root / "snippet.jsonl").write_text("")
                search_wrapper._SNIPPET_CACHE_LOADED = False
                search_wrapper._SNIPPET_BY_URI = {}
                payload = {
                    "results": [
                        {
                            "uri": uri,
                            "document": " ".join(f"w{i}" for i in range(250)),
                        }
                    ],
                    "count": 1,
                }
                out = reshape_search_payload(payload, "ideal")

        self.assertEqual(len(out["results"][0]["dataset_snippet"].split()), 100)

    def test_search_tool_names_includes_search_ideal(self):
        @tool(name="search_ideal")
        def _dummy(query: str, top_k: int = 10) -> dict:
            _ = (query, top_k)
            return {"results": [], "count": 0}

        names = search_tool_names_in([_dummy])
        self.assertIn("search_ideal", names)


if __name__ == "__main__":
    unittest.main()
