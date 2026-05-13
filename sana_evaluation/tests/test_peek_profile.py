"""Tests for the shared dataset-profile loader and SANA compatibility wrappers."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import sana_evaluation.helper.peek_profile as sana_peek_profile
import strands_evaluation.helper.peek_profile as peek_profile


def test_default_profiles_path_points_to_repo_root_data_file() -> None:
    assert peek_profile._PROFILES_PATH.name == "datagov_tables_profiles.jsonl"
    assert peek_profile._PROFILES_PATH.parent.name == "exploratory-qa-eval"
    assert peek_profile._PROFILES_PATH.exists()


class DatasetProfilesTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self._root = Path(self._tmp.name)
        self._profiles_path = self._root / "datagov_tables_profiles.jsonl"

        self._orig_peek_state = {
            "profiles_path": peek_profile._PROFILES_PATH,
            "profiles_loaded": peek_profile._PROFILES_LOADED,
            "profile_by_uri": peek_profile._PROFILE_BY_URI,
            "profile_by_slug_filename": peek_profile._PROFILE_BY_SLUG_FILENAME,
        }

        peek_profile._PROFILES_PATH = self._profiles_path
        peek_profile._PROFILES_LOADED = False
        peek_profile._PROFILE_BY_URI = {}
        peek_profile._PROFILE_BY_SLUG_FILENAME = {}

        self._tabular_uri = (
            "s3://lakeqa-yc4103-datalake/datagov/example-dataset/v1/files/rows.csv"
        )
        self._text_uri = (
            "s3://lakeqa-yc4103-datalake/datagov/example-dataset/v1/files/notes.txt"
        )

    def tearDown(self) -> None:
        peek_profile._PROFILES_PATH = self._orig_peek_state["profiles_path"]
        peek_profile._PROFILES_LOADED = self._orig_peek_state["profiles_loaded"]
        peek_profile._PROFILE_BY_URI = self._orig_peek_state["profile_by_uri"]
        peek_profile._PROFILE_BY_SLUG_FILENAME = self._orig_peek_state["profile_by_slug_filename"]
        self._tmp.cleanup()

    def _write_jsonl(self, path: Path, rows: list[dict]) -> None:
        with path.open("w") as f:
            for row in rows:
                f.write(json.dumps(row))
                f.write("\n")

    def _reset_profile_cache(self) -> None:
        peek_profile._PROFILES_LOADED = False
        peek_profile._PROFILE_BY_URI = {}
        peek_profile._PROFILE_BY_SLUG_FILENAME = {}

    def test_profile_lookup_prefers_precomputed_profiles_jsonl(self) -> None:
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
        self._reset_profile_cache()
        profile = peek_profile.load_dataset_profile(self._tabular_uri)
        self.assertEqual(profile, expected)

    def test_profile_lookup_returns_none_when_profile_missing(self) -> None:
        profile = peek_profile.load_dataset_profile(self._tabular_uri)
        self.assertIsNone(profile)

    def test_profile_lookup_returns_none_when_uri_missing_everywhere(self) -> None:
        profile = peek_profile.load_dataset_profile(
            "s3://lakeqa-yc4103-datalake/datagov/missing-dataset/v1/files/rows.csv"
        )
        self.assertIsNone(profile)

    def test_profiles_cache_supports_tabular_and_non_tabular_entries(self) -> None:
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
        self._reset_profile_cache()
        tabular_profile = peek_profile.load_dataset_profile(self._tabular_uri)
        text_profile = peek_profile.load_dataset_profile(self._text_uri)
        self.assertIn("row_count", tabular_profile)
        self.assertIn("top_2_rows", tabular_profile)
        self.assertIn("columns", tabular_profile)
        self.assertNotIn("snippet", tabular_profile)
        self.assertEqual(text_profile["family"], "text")
        self.assertIn("snippet", text_profile)
        self.assertNotIn("top_2_rows", text_profile)
        self.assertNotIn("columns", text_profile)

    def test_profile_lookup_prefers_exact_uri_over_slug_filename_fallback(self) -> None:
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
        self._reset_profile_cache()
        profile = peek_profile.load_dataset_profile(self._tabular_uri)
        self.assertEqual(profile["row_count"], 2)

    def test_profile_lookup_uses_slug_filename_fallback(self) -> None:
        fallback = {
            "slug": "example-dataset",
            "filename": "rows",
            "family": "csv",
            "row_count": 7,
        }
        self._write_jsonl(self._profiles_path, [fallback])
        self._reset_profile_cache()
        profile = peek_profile.load_dataset_profile(self._tabular_uri)
        self.assertEqual(profile, fallback)

    def test_sana_helper_reexports_shared_profile_loader(self) -> None:
        self.assertIs(sana_peek_profile.load_dataset_profile, peek_profile.load_dataset_profile)


class SanaPeekFileWrapperTests(unittest.TestCase):
    """Verify SANA's peek_file wrapper merges profile into the baseline result."""

    def test_wrapper_merges_profile_when_loader_returns_one(self) -> None:
        from sana_evaluation.tools import peek_file_with_profile as mod

        original_impl = mod._baseline_peek_file_impl
        original_loader = mod.load_dataset_profile

        def stub_impl(**kwargs):
            return {
                "dataset_id": "ex",
                "file_path": "files/x.csv",
                "s3_uri": "s3://b/x.csv",
                "family": "csv",
            }

        def stub_loader(uri):
            return {"family": "csv", "row_count": 42}

        try:
            mod._baseline_peek_file_impl = stub_impl
            mod.load_dataset_profile = stub_loader
            result = mod.peek_file._tool_func(dataset_id="ex", file_path="files/x.csv")
        finally:
            mod._baseline_peek_file_impl = original_impl
            mod.load_dataset_profile = original_loader

        self.assertIn("profile", result)
        self.assertEqual(result["profile"]["row_count"], 42)

    def test_wrapper_skips_profile_when_loader_returns_none(self) -> None:
        from sana_evaluation.tools import peek_file_with_profile as mod

        original_impl = mod._baseline_peek_file_impl
        original_loader = mod.load_dataset_profile

        def stub_impl(**kwargs):
            return {
                "dataset_id": "ex",
                "file_path": "files/x.csv",
                "s3_uri": "s3://b/x.csv",
                "family": "csv",
            }

        def stub_loader(uri):
            return None

        try:
            mod._baseline_peek_file_impl = stub_impl
            mod.load_dataset_profile = stub_loader
            result = mod.peek_file._tool_func(dataset_id="ex", file_path="files/x.csv")
        finally:
            mod._baseline_peek_file_impl = original_impl
            mod.load_dataset_profile = original_loader

        self.assertNotIn("profile", result)

    def test_wrapper_skips_profile_on_baseline_error(self) -> None:
        from sana_evaluation.tools import peek_file_with_profile as mod

        original_impl = mod._baseline_peek_file_impl
        original_loader = mod.load_dataset_profile

        loader_called = {"count": 0}

        def stub_impl(**kwargs):
            return {"error": "HeadObject failed"}

        def stub_loader(uri):
            loader_called["count"] += 1
            return {"row_count": 1}

        try:
            mod._baseline_peek_file_impl = stub_impl
            mod.load_dataset_profile = stub_loader
            result = mod.peek_file._tool_func(dataset_id="ex", file_path="files/x.csv")
        finally:
            mod._baseline_peek_file_impl = original_impl
            mod.load_dataset_profile = original_loader

        self.assertEqual(result, {"error": "HeadObject failed"})
        self.assertEqual(loader_called["count"], 0)


class SanaPeekMultipleWrapperTests(unittest.TestCase):
    """Verify SANA's peek_multiple wrapper reuses enriched peek_file for each entry."""

    def test_wrapper_merges_profiles_for_each_file(self) -> None:
        from sana_evaluation.tools import peek_file_with_profile as mod

        original_impl = mod._baseline_peek_file_impl
        original_loader = mod.load_dataset_profile

        def stub_impl(**kwargs):
            uri = kwargs.get("s3_uri") or f"s3://b/{kwargs.get('dataset_id')}/{kwargs.get('file_path')}"
            return {
                "dataset_id": kwargs.get("dataset_id") or "from-uri",
                "file_path": kwargs.get("file_path") or "files/uri.csv",
                "s3_uri": uri,
                "family": "csv",
            }

        def stub_loader(uri):
            return {"row_count": 10 if uri.endswith("a.csv") else 20}

        try:
            mod._baseline_peek_file_impl = stub_impl
            mod.load_dataset_profile = stub_loader
            result = mod.peek_multiple._tool_func(
                files=[
                    {"dataset_id": "ds", "file_path": "files/a.csv"},
                    {"s3_uri": "s3://b/ds/files/b.csv"},
                ],
                max_rows=3,
            )
        finally:
            mod._baseline_peek_file_impl = original_impl
            mod.load_dataset_profile = original_loader

        self.assertEqual(result["count"], 2)
        self.assertEqual(result["results"][0]["profile"]["row_count"], 10)
        self.assertEqual(result["results"][1]["profile"]["row_count"], 20)

    def test_wrapper_preserves_validation_error_shape(self) -> None:
        from sana_evaluation.tools import peek_file_with_profile as mod

        result = mod.peek_multiple._tool_func(files=None)

        self.assertIn("error", result)
        self.assertIn("peek_multiple requires", result["error"])
        self.assertNotIn("list_files", result["error"])


if __name__ == "__main__":
    unittest.main()
