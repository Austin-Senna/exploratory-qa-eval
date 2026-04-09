"""
Tests for the JSON-safe row conversion used by query_file.

Regression: query_file was passing DuckDB row tuples directly to json.dumps,
which crashes with `Object of type date is not JSON serializable` whenever a
result set contains DATE / TIMESTAMP / TIME / UUID / DECIMAL / BLOB columns.
This is the largest single platform-side bug in tool_error_findings.md
(~93 query_file errors fired on plain `SELECT * FROM t LIMIT N`).
"""

import datetime
import decimal
import json
import unittest
import uuid

from strands_evaluation.tools.agent_tools_v2 import (
    _rewrite_query_error,
    _rewrite_unqueryable_family_error,
    _to_json_safe,
)


class TestToJsonSafe(unittest.TestCase):
    def test_passthrough_primitives(self):
        for v in [None, True, False, 0, 1, -3, 1.5, "abc", ""]:
            self.assertEqual(_to_json_safe(v), v)

    def test_date_converts_to_iso_string(self):
        self.assertEqual(_to_json_safe(datetime.date(2024, 7, 4)), "2024-07-04")

    def test_datetime_converts_to_iso_string(self):
        self.assertEqual(
            _to_json_safe(datetime.datetime(2024, 7, 4, 13, 5, 9)),
            "2024-07-04T13:05:09",
        )

    def test_time_converts_to_iso_string(self):
        self.assertEqual(_to_json_safe(datetime.time(13, 5, 9)), "13:05:09")

    def test_timedelta_converts_to_total_seconds(self):
        self.assertEqual(
            _to_json_safe(datetime.timedelta(hours=1, minutes=30)), 5400.0
        )

    def test_decimal_converts_to_string(self):
        # str preserves precision; float would lose it
        self.assertEqual(_to_json_safe(decimal.Decimal("12345.6789")), "12345.6789")

    def test_uuid_converts_to_string(self):
        u = uuid.UUID("12345678-1234-5678-1234-567812345678")
        self.assertEqual(_to_json_safe(u), "12345678-1234-5678-1234-567812345678")

    def test_bytes_converts_to_base64_string(self):
        result = _to_json_safe(b"hello")
        self.assertIsInstance(result, str)
        # round-trippable as base64
        import base64
        self.assertEqual(base64.b64decode(result), b"hello")

    def test_bytearray_converts_to_base64_string(self):
        result = _to_json_safe(bytearray(b"world"))
        self.assertIsInstance(result, str)

    def test_list_recurses(self):
        self.assertEqual(
            _to_json_safe([datetime.date(2024, 1, 1), 1, "x"]),
            ["2024-01-01", 1, "x"],
        )

    def test_tuple_recurses_and_becomes_list(self):
        self.assertEqual(
            _to_json_safe((datetime.date(2024, 1, 1), 1)),
            ["2024-01-01", 1],
        )

    def test_dict_recurses(self):
        self.assertEqual(
            _to_json_safe({"d": datetime.date(2024, 1, 1), "n": 1}),
            {"d": "2024-01-01", "n": 1},
        )

    def test_nested_structures(self):
        # Mimics a DuckDB STRUCT column with a date inside
        value = {"created": datetime.datetime(2024, 1, 1, 0, 0, 0), "tags": [b"a", b"b"]}
        result = _to_json_safe(value)
        # Must be JSON-serializable end-to-end
        json.dumps(result)

    def test_full_row_set_serializes(self):
        # Simulates the exact shape that crashes query_file at line 515
        rows = [
            (1, "Alice", datetime.date(2024, 1, 15), decimal.Decimal("100.50")),
            (2, "Bob",   datetime.date(2024, 2, 28), decimal.Decimal("200.75")),
        ]
        safe_rows = [[_to_json_safe(v) for v in r] for r in rows]
        result = {
            "columns": ["id", "name", "created", "amount"],
            "rows": safe_rows,
            "row_count": len(safe_rows),
            "truncated": False,
        }
        # Pre-fix this raised TypeError; post-fix it must succeed.
        json.dumps(result)


class TestRewriteQueryError(unittest.TestCase):
    """
    Regression: when DuckDB's read_json_auto rejects a >100MB JSON object, the
    raw error tells the agent "Try increasing maximum_object_size" — which it
    cannot do. The agent then thrashes (retries the same query, malforms a
    download, etc.). _rewrite_query_error must convert it into the same
    actionable hint that the pre-check at line 483 uses: "use download +
    execute_code instead".
    """

    def test_maximum_object_size_error_is_rewritten_with_actionable_hint(self):
        raw = (
            'Invalid Input Error: "maximum_object_size" of 104857600 bytes '
            'exceeded while reading file '
            '"s3://lakeqa-yc4103-datalake/datagov/parking-violations-issued-in-january-2019/files/data.txt" '
            '(>115079012 bytes).\n Try increasing "maximum_object_size".'
        )
        rewritten = _rewrite_query_error(raw)
        self.assertIn("download", rewritten.lower())
        self.assertIn("execute_code", rewritten)
        # The misleading "Try increasing" hint must NOT be passed through.
        self.assertNotIn("increasing", rewritten.lower())

    def test_maximum_object_size_error_includes_observed_size(self):
        raw = (
            'Invalid Input Error: "maximum_object_size" of 104857600 bytes '
            'exceeded while reading file "s3://b/k.json" (>115079012 bytes).'
        )
        rewritten = _rewrite_query_error(raw)
        # Tells the agent how big the object actually was so it can plan
        self.assertIn("115079012", rewritten)

    def test_unrecognized_error_is_passed_through(self):
        raw = "Binder Error: Referenced column \"foo\" not found"
        self.assertEqual(_rewrite_query_error(raw), raw)

    def test_io_timeout_error_is_rewritten(self):
        raw = (
            "IO Error: Timeout was reached error for HTTP GET to "
            "'https://lakeqa-yc4103-datalake.s3.amazonaws.com/foo/bar.csv'"
        )
        rewritten = _rewrite_query_error(raw)
        # Should hint at the download path for big files that time out too
        self.assertIn("download", rewritten.lower())

    def test_parser_error_backtick_is_rewritten_with_quote_hint(self):
        # DuckDB rejects backtick identifiers with a Parser Error. The agent
        # has been observed using `column name` style ~17 times. Tell it the
        # actual fix: double quotes.
        raw = (
            'Parser Error: syntax error at or near "`OVERALL GRADE`"\n'
            'LINE 1: SELECT `OVERALL GRADE`, COUNT(*) FROM t GROUP BY 1'
        )
        rewritten = _rewrite_query_error(raw)
        # Must explicitly tell it to use double quotes
        self.assertIn('double quotes', rewritten.lower())
        self.assertIn('"', rewritten)
        # Original error context still surfaced for debugging
        self.assertIn('Parser Error', rewritten)

    def test_parser_error_without_backticks_is_passed_through(self):
        # A parser error that ISN'T about backticks should pass through
        # unchanged so we don't mislead the agent.
        raw = "Parser Error: syntax error at or near \"FRUM\""
        self.assertEqual(_rewrite_query_error(raw), raw)


class TestRewriteUnqueryableFamilyError(unittest.TestCase):
    """
    Regression: query_file rejects non-CSV/JSON files with the bare message
    "File family 'text' is not queryable with SQL". The agent then doesn't
    know what to do — observed 22 times. Replace with an actionable hint
    naming the right tool for each family.
    """

    def test_text_family_message_suggests_text_tools(self):
        msg = _rewrite_unqueryable_family_error("text")
        self.assertIn("text", msg.lower())
        # Names the right alternative tools
        self.assertIn("peek_file", msg)
        self.assertIn("grep_file", msg)
        self.assertIn("read_file", msg)
        # Explicitly says query_file doesn't apply
        self.assertIn("query_file", msg)

    def test_unknown_family_message_still_useful(self):
        msg = _rewrite_unqueryable_family_error("binary")
        self.assertIn("binary", msg)
        self.assertIn("query_file", msg)


if __name__ == "__main__":
    unittest.main()
