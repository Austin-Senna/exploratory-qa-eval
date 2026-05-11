import importlib.util
import sys
import types
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest import mock


_MODULE_NAMES = [
    "strands",
    "boto3",
    "botocore",
    "botocore.config",
    "botocore.exceptions",
    "duckdb",
    "dotenv",
    "requests",
    "strands_evaluation",
    "strands_evaluation.tools",
    "strands_evaluation.tools.helper",
    "strands_evaluation.tools.helper.detect",
    "strands_evaluation.tools.agent_tools",
    "strands_evaluation.tools.agent_tools_v2",
]


class _Config:
    def __init__(self, *_args, **_kwargs):
        pass


class _ClientError(Exception):
    pass


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_agent_tools_v2_module():
    repo_root = Path(__file__).resolve().parents[1]
    previous = {name: sys.modules.get(name) for name in _MODULE_NAMES}

    fake_strands = types.ModuleType("strands")
    fake_strands.tool = lambda func: func
    sys.modules["strands"] = fake_strands

    fake_boto3 = types.ModuleType("boto3")
    fake_boto3.client = lambda *_args, **_kwargs: object()
    sys.modules["boto3"] = fake_boto3

    fake_botocore = types.ModuleType("botocore")
    fake_botocore.UNSIGNED = "UNSIGNED"
    sys.modules["botocore"] = fake_botocore

    fake_config = types.ModuleType("botocore.config")
    fake_config.Config = _Config
    sys.modules["botocore.config"] = fake_config

    fake_exceptions = types.ModuleType("botocore.exceptions")
    fake_exceptions.ClientError = _ClientError
    sys.modules["botocore.exceptions"] = fake_exceptions

    fake_duckdb = types.ModuleType("duckdb")
    fake_duckdb.DuckDBPyConnection = object
    fake_duckdb.connect = lambda *_args, **_kwargs: None
    sys.modules["duckdb"] = fake_duckdb

    fake_dotenv = types.ModuleType("dotenv")
    fake_dotenv.load_dotenv = lambda: None
    sys.modules["dotenv"] = fake_dotenv

    fake_requests = types.ModuleType("requests")
    sys.modules["requests"] = fake_requests

    package = types.ModuleType("strands_evaluation")
    package.__path__ = [str(repo_root / "strands_evaluation")]
    sys.modules["strands_evaluation"] = package

    tools_package = types.ModuleType("strands_evaluation.tools")
    tools_package.__path__ = [str(repo_root / "strands_evaluation" / "tools")]
    sys.modules["strands_evaluation.tools"] = tools_package

    helper_package = types.ModuleType("strands_evaluation.tools.helper")
    helper_package.__path__ = [str(repo_root / "strands_evaluation" / "tools" / "helper")]
    sys.modules["strands_evaluation.tools.helper"] = helper_package

    _load_module(
        "strands_evaluation.tools.helper.detect",
        repo_root / "strands_evaluation" / "tools" / "helper" / "detect.py",
    )
    _load_module(
        "strands_evaluation.tools.agent_tools",
        repo_root / "strands_evaluation" / "tools" / "agent_tools.py",
    )
    module = _load_module(
        "strands_evaluation.tools.agent_tools_v2",
        repo_root / "strands_evaluation" / "tools" / "agent_tools_v2.py",
    )

    def restore():
        for name, old_value in previous.items():
            if old_value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old_value

    return module, restore


class AgentToolsV2EmptyS3Tests(unittest.TestCase):
    def setUp(self):
        self.mod, self.restore_modules = _load_agent_tools_v2_module()
        self.ref = {
            "dataset_id": "datagov/empty-dataset",
            "file_path": "files/empty.txt",
            "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/empty-dataset/files/empty.txt",
            "key": "datagov/empty-dataset/files/empty.txt",
        }

    def tearDown(self):
        self.restore_modules()

    def _apply_empty_object_patches(self, stack: ExitStack):
        stack.enter_context(
            mock.patch.object(self.mod, "_resolve_file_reference", return_value=self.ref)
        )
        stack.enter_context(mock.patch.object(self.mod, "_get_s3_client", return_value=object()))
        stack.enter_context(mock.patch.object(self.mod, "_s3_head", return_value=0))
        return stack.enter_context(
            mock.patch.object(
                self.mod,
                "_s3_range_get",
                side_effect=AssertionError("range GET should not run for empty objects"),
            )
        )

    def test_peek_file_handles_empty_object_without_range_get(self):
        with ExitStack() as stack:
            range_get = self._apply_empty_object_patches(stack)
            result = self.mod.peek_file(s3_uri=self.ref["s3_uri"])

        self.assertNotIn("error", result)
        self.assertEqual(result["family"], "text")
        self.assertEqual(result["size_bytes"], 0)
        self.assertEqual(result["preview_text"], "")
        self.assertEqual(result["row_count_estimate"], 0)
        range_get.assert_not_called()

    def test_parse_xml_records_reports_empty_object_as_non_xml_without_range_get(self):
        with ExitStack() as stack:
            range_get = self._apply_empty_object_patches(stack)
            result = self.mod._parse_xml_records_impl(s3_uri=self.ref["s3_uri"])

        self.assertIn("error", result)
        self.assertIn("Detected 'text'", result["error"])
        self.assertNotIn("Range", result["error"])
        range_get.assert_not_called()

    def test_query_file_reports_empty_object_as_unqueryable_without_range_get(self):
        with ExitStack() as stack:
            range_get = self._apply_empty_object_patches(stack)
            result = self.mod._query_file_impl(
                s3_uri=self.ref["s3_uri"],
                sql="SELECT COUNT(*) FROM t",
            )

        self.assertIn("error", result)
        self.assertIn("plain text", result["error"])
        self.assertNotIn("Could not detect file family", result["error"])
        range_get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
