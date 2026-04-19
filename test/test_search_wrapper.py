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
from strands_evaluation.tools.external.ideal.search_wrapper import (
    reshape_search_payload,
    search_tool_names_in,
)


class TestSearchWrapperPayload(unittest.TestCase):
    def tearDown(self) -> None:
        search_wrapper._DESC_CACHE_LOADED = False
        search_wrapper._DESC_BY_URI = {}
        search_wrapper._SNIPPET_CACHE_LOADED = False
        search_wrapper._SNIPPET_BY_URI = {}
        search_wrapper._SCHEMAS_CACHE_LOADED = False
        search_wrapper._SCHEMA_BY_SLUG_FILENAME = {}

    def _patch_support_files(
        self,
        root: Path,
        *,
        uri: str,
        desc: str = "LLM description",
        snippet: str = "dataset snippet words",
        schema_kind: str = "csv",
        columns: list[str] | None = None,
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

        stack = ExitStack()
        stack.enter_context(patch.object(search_wrapper, "_TABLE_DESCRIPTIONS_PATH", desc_path))
        stack.enter_context(patch.object(search_wrapper, "_SNIPPETS_PATH", snippet_path))
        stack.enter_context(patch.object(search_wrapper, "_SCHEMAS_PATH", schema_path))
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

    def test_source_driven_naive_mode_strips_noise(self):
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
        self.assertNotIn("ideal_source_driven", out)
        self.assertNotIn("task_id", out)

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
