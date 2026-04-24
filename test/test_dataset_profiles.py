import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import strands_evaluation.tools.agent_tools_v2 as agent_tools_v2
from strands_evaluation.tools.external.ideal import search_wrapper


class DatasetProfilesTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self._root = Path(self._tmp.name)
        self._profiles_path = self._root / "datagov_tables_profiles.jsonl"
        self._desc_path = self._root / "table_descriptions.jsonl"
        self._manifest_desc_path = self._root / "tasks_core_quality_file_manifest_descriptions.jsonl"
        self._snippet_path = self._root / "snippet.jsonl"
        self._schemas_path = self._root / "datagov_tables_schemas_full.jsonl"

        self._orig_agent_tools_state = {
            "profiles_path": agent_tools_v2._PROFILES_PATH,
            "profiles_loaded": agent_tools_v2._PROFILES_LOADED,
            "profile_by_uri": agent_tools_v2._PROFILE_BY_URI,
            "profile_by_slug_filename": agent_tools_v2._PROFILE_BY_SLUG_FILENAME,
        }
        self._orig_search_wrapper_state = {
            "desc_path": search_wrapper._TABLE_DESCRIPTIONS_PATH,
            "manifest_desc_path": search_wrapper._MANIFEST_DESCRIPTIONS_PATH,
            "snippet_path": search_wrapper._SNIPPETS_PATH,
            "schemas_path": search_wrapper._SCHEMAS_PATH,
            "desc_loaded": search_wrapper._DESC_CACHE_LOADED,
            "desc_by_uri": search_wrapper._DESC_BY_URI,
            "desc_row_by_uri": search_wrapper._DESC_ROW_BY_URI,
            "snippet_loaded": search_wrapper._SNIPPET_CACHE_LOADED,
            "snippet_by_uri": search_wrapper._SNIPPET_BY_URI,
            "schemas_loaded": search_wrapper._SCHEMAS_CACHE_LOADED,
            "schema_by_slug_filename": search_wrapper._SCHEMA_BY_SLUG_FILENAME,
        }

        agent_tools_v2._PROFILES_PATH = self._profiles_path
        agent_tools_v2._PROFILES_LOADED = False
        agent_tools_v2._PROFILE_BY_URI = {}
        agent_tools_v2._PROFILE_BY_SLUG_FILENAME = {}

        search_wrapper._TABLE_DESCRIPTIONS_PATH = self._desc_path
        search_wrapper._MANIFEST_DESCRIPTIONS_PATH = self._manifest_desc_path
        search_wrapper._SNIPPETS_PATH = self._snippet_path
        search_wrapper._SCHEMAS_PATH = self._schemas_path
        self._reset_search_wrapper_caches()

        self._tabular_uri = (
            "s3://lakeqa-yc4103-datalake/datagov/example-dataset/v1/files/rows.csv"
        )
        self._text_uri = (
            "s3://lakeqa-yc4103-datalake/datagov/example-dataset/v1/files/notes.txt"
        )

        self._write_jsonl(
            self._desc_path,
            [
                {
                    "dataset_uri": self._tabular_uri,
                    "description": "Legacy description",
                }
            ],
        )
        self._write_jsonl(
            self._snippet_path,
            [
                {
                    "dataset_uri": self._tabular_uri,
                    "dataset_snippet": "Legacy snippet",
                }
            ],
        )
        self._write_jsonl(
            self._schemas_path,
            [
                {
                    "dataset_slug": "example-dataset",
                    "tables": [
                        {
                            "relative_path": "rows.csv",
                            "table_kind": "delimited_text",
                            "columns": ["name", "value"],
                            "delimiter": ",",
                        }
                    ],
                }
            ],
        )

    def tearDown(self) -> None:
        agent_tools_v2._PROFILES_PATH = self._orig_agent_tools_state["profiles_path"]
        agent_tools_v2._PROFILES_LOADED = self._orig_agent_tools_state["profiles_loaded"]
        agent_tools_v2._PROFILE_BY_URI = self._orig_agent_tools_state["profile_by_uri"]
        agent_tools_v2._PROFILE_BY_SLUG_FILENAME = self._orig_agent_tools_state["profile_by_slug_filename"]

        search_wrapper._TABLE_DESCRIPTIONS_PATH = self._orig_search_wrapper_state["desc_path"]
        search_wrapper._MANIFEST_DESCRIPTIONS_PATH = self._orig_search_wrapper_state["manifest_desc_path"]
        search_wrapper._SNIPPETS_PATH = self._orig_search_wrapper_state["snippet_path"]
        search_wrapper._SCHEMAS_PATH = self._orig_search_wrapper_state["schemas_path"]
        search_wrapper._DESC_CACHE_LOADED = self._orig_search_wrapper_state["desc_loaded"]
        search_wrapper._DESC_BY_URI = self._orig_search_wrapper_state["desc_by_uri"]
        search_wrapper._DESC_ROW_BY_URI = self._orig_search_wrapper_state["desc_row_by_uri"]
        search_wrapper._SNIPPET_CACHE_LOADED = self._orig_search_wrapper_state["snippet_loaded"]
        search_wrapper._SNIPPET_BY_URI = self._orig_search_wrapper_state["snippet_by_uri"]
        search_wrapper._SCHEMAS_CACHE_LOADED = self._orig_search_wrapper_state["schemas_loaded"]
        search_wrapper._SCHEMA_BY_SLUG_FILENAME = self._orig_search_wrapper_state["schema_by_slug_filename"]
        self._tmp.cleanup()

    def _reset_search_wrapper_caches(self) -> None:
        search_wrapper._DESC_CACHE_LOADED = False
        search_wrapper._DESC_BY_URI = {}
        search_wrapper._DESC_ROW_BY_URI = {}
        search_wrapper._SNIPPET_CACHE_LOADED = False
        search_wrapper._SNIPPET_BY_URI = {}
        search_wrapper._SCHEMAS_CACHE_LOADED = False
        search_wrapper._SCHEMA_BY_SLUG_FILENAME = {}

    def _write_jsonl(self, path: Path, rows: list[dict]) -> None:
        with path.open("w") as f:
            for row in rows:
                f.write(json.dumps(row))
                f.write("\n")

    def test_profile_lookup_prefers_precomputed_profiles_jsonl(self):
        expected = {
            "s3_uri": self._tabular_uri,
            "slug": "example-dataset",
            "filename": "rows",
            "family": "csv",
            "size_bytes": 123,
            "row_count": 2,
            "top_2_rows": [{"name": "Ada", "value": 1}, {"name": "Grace", "value": 2}],
            "columns": [
                {
                    "name": "name",
                    "type": "string",
                    "null_rate": 0.0,
                    "distinct_count": 2,
                    "min": None,
                    "max": None,
                    "mean": None,
                }
            ],
        }
        self._write_jsonl(self._profiles_path, [expected])
        agent_tools_v2._PROFILES_LOADED = False
        agent_tools_v2._PROFILE_BY_URI = {}
        agent_tools_v2._PROFILE_BY_SLUG_FILENAME = {}

        profile = agent_tools_v2._load_dataset_profile(self._tabular_uri)

        self.assertEqual(profile, expected)

    def test_profile_lookup_falls_back_to_legacy_bundle_when_profile_missing(self):
        profile = agent_tools_v2._load_dataset_profile(self._tabular_uri)

        self.assertEqual(
            profile,
            {
                "schema_columns": ["name", "value"],
                "table_kind": "delimited_text",
                "llm_description": "Legacy description",
                "snippet": "Legacy snippet",
            },
        )

    def test_profile_lookup_uses_manifest_description_fields_when_present(self):
        self._write_jsonl(
            self._manifest_desc_path,
            [
                {
                    "dataset_uri": self._tabular_uri,
                    "description": "Manifest description",
                    "metadata": "Manifest metadata",
                    "generated_metadata": "Generated title",
                    "original_metadata": "Original title",
                    "content": "Manifest content block",
                }
            ],
        )
        self._reset_search_wrapper_caches()

        profile = agent_tools_v2._load_dataset_profile(self._tabular_uri)

        self.assertEqual(profile["llm_description"], "Manifest description")
        self.assertNotIn("description_metadata", profile)
        self.assertNotIn("description_generated_metadata", profile)
        self.assertNotIn("description_original_metadata", profile)
        self.assertNotIn("description_content", profile)
        self.assertNotIn("description_source_file", profile)

    def test_profile_lookup_returns_none_when_uri_missing_everywhere(self):
        profile = agent_tools_v2._load_dataset_profile(
            "s3://lakeqa-yc4103-datalake/datagov/missing-dataset/v1/files/rows.csv"
        )

        self.assertIsNone(profile)

    def test_profiles_cache_supports_tabular_and_non_tabular_entries(self):
        tabular = {
            "s3_uri": self._tabular_uri,
            "slug": "example-dataset",
            "filename": "rows",
            "family": "csv",
            "size_bytes": 123,
            "row_count": 2,
            "top_2_rows": [{"name": "Ada", "value": 1}, {"name": "Grace", "value": 2}],
            "columns": [
                {
                    "name": "value",
                    "type": "integer",
                    "null_rate": 0.0,
                    "distinct_count": 2,
                    "min": 1,
                    "max": 2,
                    "mean": 1.5,
                }
            ],
        }
        non_tabular = {
            "s3_uri": self._text_uri,
            "slug": "example-dataset",
            "filename": "notes",
            "family": "text",
            "size_bytes": 55,
            "llm_description": "Some plain text notes",
            "snippet": "First line of notes",
        }
        self._write_jsonl(self._profiles_path, [tabular, non_tabular])
        agent_tools_v2._PROFILES_LOADED = False
        agent_tools_v2._PROFILE_BY_URI = {}
        agent_tools_v2._PROFILE_BY_SLUG_FILENAME = {}

        tabular_profile = agent_tools_v2._load_dataset_profile(self._tabular_uri)
        text_profile = agent_tools_v2._load_dataset_profile(self._text_uri)

        self.assertIn("row_count", tabular_profile)
        self.assertIn("top_2_rows", tabular_profile)
        self.assertIn("columns", tabular_profile)
        self.assertNotIn("snippet", tabular_profile)
        self.assertEqual(text_profile["family"], "text")
        self.assertIn("snippet", text_profile)
        self.assertNotIn("top_2_rows", text_profile)
        self.assertNotIn("columns", text_profile)

    def test_profile_lookup_prefers_exact_uri_over_slug_filename_fallback(self):
        canonical = {
            "s3_uri": self._tabular_uri,
            "slug": "example-dataset",
            "filename": "rows",
            "family": "csv",
            "row_count": 2,
        }
        conflicting = {
            "slug": "example-dataset",
            "filename": "rows",
            "family": "csv",
            "row_count": 999,
        }
        self._write_jsonl(self._profiles_path, [canonical, conflicting])
        agent_tools_v2._PROFILES_LOADED = False
        agent_tools_v2._PROFILE_BY_URI = {}
        agent_tools_v2._PROFILE_BY_SLUG_FILENAME = {}

        profile = agent_tools_v2._load_dataset_profile(self._tabular_uri)

        self.assertEqual(profile["row_count"], 2)


if __name__ == "__main__":
    unittest.main()
