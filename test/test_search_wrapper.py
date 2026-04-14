import json
import sys
import unittest
from pathlib import Path

from strands import tool

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands_evaluation.tools.external.ideal.search_wrapper import (
    reshape_search_payload,
    search_tool_names_in,
)


class TestSearchWrapperPayload(unittest.TestCase):
    def test_naive_mode_returns_uri_only(self):
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
        self.assertEqual(list(out["results"][0].keys()), ["uri"])

    def test_source_driven_naive_mode_returns_dataset_id_only(self):
        payload = {
            "ideal_source_driven": True,
            "results": [
                {
                    "dataset_id": "foo",
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                    "description": "desc",
                    "content": "content here",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "naive")
        self.assertEqual(out["results"][0], {"dataset_id": "foo"})

    def test_standard_mode_truncates_to_200_words(self):
        long_text = " ".join([f"w{i}" for i in range(400)])
        payload = {
            "results": [
                {
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                    "document": long_text,
                    "score": "0.123",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "standard")
        snippet = out["results"][0]["snippet"]
        self.assertEqual(len(snippet.split()), 200)
        self.assertIn("uri", out["results"][0])
        self.assertEqual(out["results"][0]["score"], "0.123")

    def test_source_driven_standard_truncates_content_to_200_words(self):
        payload = {
            "ideal_source_driven": True,
            "results": [
                {
                    "dataset_id": "foo",
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                    "description": "desc",
                    "content": " ".join([f"w{i}" for i in range(400)]),
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "standard")
        self.assertEqual(out["results"][0]["dataset_id"], "foo")
        self.assertNotIn("description", out["results"][0])
        self.assertEqual(len(out["results"][0]["content"].split()), 200)
        self.assertNotIn("dataset_snippet", out["results"][0])
        self.assertNotIn("ideal_source_driven", out)

    def test_source_driven_ideal_emits_dataset_snippet_at_100_words(self):
        payload = {
            "ideal_source_driven": True,
            "results": [
                {
                    "dataset_id": "foo",
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                    "description": "desc",
                    "content": " ".join([f"w{i}" for i in range(400)]),
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "ideal")
        self.assertEqual(out["results"][0]["dataset_id"], "foo")
        self.assertEqual(out["results"][0]["description"], "desc")
        self.assertEqual(len(out["results"][0]["dataset_snippet"].split()), 100)
        self.assertNotIn("content", out["results"][0])

    def test_source_driven_standard_preserves_uri_without_optional_fields(self):
        payload = {
            "ideal_source_driven": True,
            "results": [
                {
                    "dataset_id": "foo",
                    "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "standard")
        self.assertEqual(
            out["results"][0],
            {
                "dataset_id": "foo",
                "uri": "s3://lakeqa-yc4103-datalake/datagov/foo/files/rows.txt",
            },
        )

    def test_ideal_mode_adds_description_when_available(self):
        first = json.loads(Path("table_descriptions.jsonl").read_text().splitlines()[0])
        uri = first["dataset_uri"]
        payload = {
            "results": [
                {
                    "uri": uri,
                    "document": "dummy",
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "ideal")
        self.assertIn("uri", out["results"][0])
        self.assertIn("description", out["results"][0])
        self.assertTrue(out["results"][0]["description"])

    def test_ideal_mode_emits_dataset_snippet_from_document(self):
        first = json.loads(Path("table_descriptions.jsonl").read_text().splitlines()[0])
        uri = first["dataset_uri"]
        long_text = " ".join([f"w{i}" for i in range(250)])
        payload = {
            "results": [
                {
                    "uri": uri,
                    "document": long_text,
                }
            ],
            "count": 1,
        }
        out = reshape_search_payload(payload, "ideal")
        row = out["results"][0]
        self.assertIn("dataset_snippet", row)
        self.assertEqual(len(row["dataset_snippet"].split()), 100)
        self.assertIn("description", row)

    def test_search_tool_names_includes_search_ideal(self):
        @tool(name="search_ideal")
        def _dummy(query: str, top_k: int = 10) -> dict:
            _ = (query, top_k)
            return {"results": [], "count": 0}

        names = search_tool_names_in([_dummy])
        self.assertIn("search_ideal", names)


if __name__ == "__main__":
    unittest.main()
