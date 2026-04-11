import json
import unittest
from pathlib import Path

from strands import tool

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

    def test_search_tool_names_includes_search_ideal(self):
        @tool(name="search_ideal")
        def _dummy(query: str, top_k: int = 10) -> dict:
            _ = (query, top_k)
            return {"results": [], "count": 0}

        names = search_tool_names_in([_dummy])
        self.assertIn("search_ideal", names)


if __name__ == "__main__":
    unittest.main()
