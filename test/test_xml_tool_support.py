import unittest
from unittest.mock import Mock, patch

from strands_evaluation.helper import constants
from strands_evaluation.tools import agent_tools_v2
from strands_evaluation.tools.helper.detect import detect_family


class TestDetectFamilyXml(unittest.TestCase):
    def test_xml_declaration_returns_xml(self):
        content = '<?xml version="1.0" encoding="UTF-8"?><root><item>1</item></root>'
        self.assertEqual(detect_family(content), "xml")

    def test_kml_root_returns_xml(self):
        content = '<kml xmlns="http://www.opengis.net/kml/2.2"><Document /></kml>'
        self.assertEqual(detect_family(content), "xml")

    def test_json_detection_unchanged(self):
        self.assertEqual(detect_family('{"name": "alice"}'), "json")

    def test_csv_detection_unchanged(self):
        self.assertEqual(detect_family("name,city\nAlice,Boston\nBob,Denver\n"), "csv")

    def test_plain_text_with_angle_bracket_later_is_not_xml(self):
        content = "Plain text first.\nA later snippet uses <tag>inline markup</tag>."
        self.assertEqual(detect_family(content), "text")


class TestPeekFileXmlSupport(unittest.TestCase):
    def _call_peek(self, text: str, size_bytes: int | None = None):
        fn = getattr(agent_tools_v2.peek_file, "original_function", agent_tools_v2.peek_file)
        payload = text.encode("utf-8")
        reported_size = len(payload) if size_bytes is None else size_bytes
        with (
            patch.object(agent_tools_v2, "_resolve_dataset_folder", return_value="datagov"),
            patch.object(agent_tools_v2, "_get_s3_client", return_value=Mock()),
            patch.object(agent_tools_v2, "_s3_head", return_value=reported_size),
            patch.object(agent_tools_v2, "_s3_range_get", return_value=payload),
        ):
            return fn("demo-dataset", "files/data.xml", max_rows=20)

    def test_complete_small_xml_uses_parsed_preview_mode(self):
        text = (
            '<?xml version="1.0"?>\n'
            '<root xmlns="urn:test">\n'
            '  <record><name>Alice</name></record>\n'
            '  <record><name>Bob</name></record>\n'
            '</root>\n'
        )
        result = self._call_peek(text)
        self.assertEqual(result["family"], "xml")
        self.assertEqual(result["xml_preview_mode"], "parsed")
        self.assertEqual(result["xml_root_tag"], "root")
        self.assertEqual(result["xml_namespaces"], {"default": "urn:test"})
        self.assertIn("record", result["xml_record_tag_candidates"])

    def test_truncated_xml_snippet_uses_heuristic_mode_without_crashing(self):
        text = (
            '<?xml version="1.0"?>\n'
            '<root xmlns="urn:test">\n'
            '  <record><name>Alice</name></record>\n'
            '  <record>\n'
        )
        result = self._call_peek(text, size_bytes=agent_tools_v2._PEEK_BYTES + 128)
        self.assertEqual(result["family"], "xml")
        self.assertEqual(result["xml_preview_mode"], "heuristic")
        self.assertEqual(result["xml_root_tag"], "root")
        self.assertEqual(result["xml_namespaces"], {"default": "urn:test"})
        self.assertIn("record", result["xml_record_tag_candidates"])

    def test_kml_preview_extracts_schema_fields_and_placemark(self):
        text = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
            '  <Document>\n'
            '    <Schema name="schools" id="schools">\n'
            '      <SimpleField name="NCESSCH" type="string"/>\n'
            '      <SimpleField name="CITY" type="string"/>\n'
            '    </Schema>\n'
            '    <Placemark>\n'
            '      <name>School A</name>\n'
            '      <ExtendedData>\n'
            '        <SchemaData>\n'
            '          <SimpleData name="NCESSCH">0001</SimpleData>\n'
            '          <SimpleData name="CITY">Austin</SimpleData>\n'
            '        </SchemaData>\n'
            '      </ExtendedData>\n'
            '    </Placemark>\n'
            '  </Document>\n'
            '</kml>\n'
        )
        result = self._call_peek(text)
        self.assertEqual(result["family"], "xml")
        self.assertEqual(result["xml_preview_mode"], "parsed")
        self.assertEqual(result["xml_root_tag"], "kml")
        self.assertEqual(result["xml_schema_fields"], ["NCESSCH", "CITY"])
        self.assertIn("Placemark", result["xml_record_tag_candidates"])


class TestQueryFileXmlSupport(unittest.TestCase):
    def test_xml_family_error_is_actionable(self):
        msg = agent_tools_v2._rewrite_unqueryable_family_error("xml")
        self.assertIn("XML/KML", msg)
        self.assertIn("peek_file", msg)
        self.assertIn("grep_file", msg)
        self.assertIn("download", msg)
        self.assertIn("execute_code", msg)
        self.assertIn("xml.etree.ElementTree", msg)

    def test_query_file_detects_xml_and_returns_xml_specific_hint(self):
        fn = getattr(agent_tools_v2.query_file, "original_function", agent_tools_v2.query_file)
        text = '<?xml version="1.0"?><root><record>1</record></root>'
        with (
            patch.object(agent_tools_v2, "_resolve_dataset_folder", return_value="datagov"),
            patch.object(agent_tools_v2, "_get_s3_client", return_value=Mock()),
            patch.object(agent_tools_v2, "_s3_head", return_value=len(text.encode("utf-8"))),
            patch.object(agent_tools_v2, "_s3_range_get", return_value=text.encode("utf-8")),
        ):
            result = fn("demo-dataset", "files/data.xml", "SELECT * FROM t LIMIT 1")

        self.assertIn("error", result)
        self.assertIn("XML/KML", result["error"])
        self.assertNotIn("plain text", result["error"].lower())

    def test_query_file_docstring_mentions_xml_detection_behavior(self):
        fn = getattr(agent_tools_v2.query_file, "original_function", agent_tools_v2.query_file)
        doc = fn.__doc__ or ""
        self.assertIn("Supported file types: CSV", doc)
        self.assertIn("XML/KML is detected but not queryable", doc)


class TestPromptContract(unittest.TestCase):
    def test_system_prompt_mentions_xml_preview_and_query_limit(self):
        prompt = constants.SYSTEM_PROMPT
        self.assertIn("CSV/JSON/XML/text", prompt)
        self.assertIn("XML/KML is detected but not queryable here", prompt)
        self.assertIn("xml.etree.ElementTree", prompt)


if __name__ == "__main__":
    unittest.main()
