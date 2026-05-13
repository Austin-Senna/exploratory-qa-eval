import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def _load_profile_datasets_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "scripts" / "profile_datasets.py"
    spec = importlib.util.spec_from_file_location("_test_profile_datasets_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


profile_datasets = _load_profile_datasets_module()


class ProfileDatasetsScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self._root = Path(self._tmp.name)
        self._input_path = self._root / "schemas.jsonl"
        self._output_path = self._root / "profiles.jsonl"
        self._descriptions_path = self._root / "descriptions.jsonl"
        self._snippets_path = self._root / "snippets.jsonl"
        self._csv_path = self._root / "rows.csv"
        self._jsonl_path = self._root / "rows.jsonl"
        self._csv_path.write_text(
            "name,value,day\n"
            "Ada,1,2020-01-01\n"
            "Grace,2,2020-01-03\n"
            ",2,2020-01-05\n"
        )
        self._jsonl_path.write_text(
            '{"id":1,"payload":{"nested":{"message":"'
            + ("x" * 120)
            + '"}}}\n'
            '{"id":2,"payload":{"nested":{"message":"ok"}}}\n'
        )
        self._write_jsonl(
            self._input_path,
            [
                {
                    "dataset_slug": "example-dataset",
                    "tables": [
                        {
                            "relative_path": "rows.csv",
                            "local_path": str(self._csv_path),
                            "table_kind": "delimited_text",
                            "columns": ["name", "value", "day"],
                            "delimiter": ",",
                        }
                    ],
                }
            ],
        )
        self._write_jsonl(
            self._descriptions_path,
            [{"dataset_uri": str(self._csv_path), "description": "Local example dataset"}],
        )
        self._snippets_path.write_text("")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_jsonl(self, path: Path, rows: list[dict]) -> None:
        with path.open("w") as f:
            for row in rows:
                f.write(json.dumps(row))
                f.write("\n")

    def _read_output_rows(self) -> list[dict]:
        with self._output_path.open() as f:
            return [json.loads(line) for line in f if line.strip()]

    def test_build_profiles_computes_expected_local_csv_stats(self):
        summary = profile_datasets.build_profiles(
            input_path=self._input_path,
            output_path=self._output_path,
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=False,
            bucket="unused",
        )

        self.assertEqual(summary, {"written": 1, "skipped": 0, "errors": 0})
        rows = self._read_output_rows()
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["slug"], "example-dataset")
        self.assertEqual(row["filename"], "rows")
        self.assertEqual(row["family"], "csv")
        self.assertEqual(row["row_count"], 3)
        self.assertGreater(row["size_bytes"], 0)
        self.assertEqual(row["llm_description"], "Local example dataset")
        self.assertEqual(row["top_2_rows"][0], {"name": "Ada", "value": 1, "day": "2020-01-01"})
        self.assertEqual(row["top_2_rows"][1], {"name": "Grace", "value": 2, "day": "2020-01-03"})

        columns = {col["name"]: col for col in row["columns"]}
        self.assertEqual(columns["name"]["type"], "string")
        self.assertEqual(columns["name"]["null_rate"], 0.33)
        self.assertEqual(columns["name"]["distinct_count"], 2)
        self.assertIsNone(columns["name"]["min"])
        self.assertIsNone(columns["name"]["max"])
        self.assertIsNone(columns["name"]["mean"])

        self.assertEqual(columns["value"]["type"], "integer")
        self.assertEqual(columns["value"]["distinct_count"], 2)
        self.assertEqual(columns["value"]["min"], 1)
        self.assertEqual(columns["value"]["max"], 2)
        self.assertAlmostEqual(columns["value"]["mean"], 5 / 3, places=6)

        self.assertEqual(columns["day"]["type"], "date")
        self.assertEqual(columns["day"]["min"], "2020-01-01")
        self.assertEqual(columns["day"]["max"], "2020-01-05")
        self.assertEqual(columns["day"]["mean"], "2020-01-03")

    def test_build_profiles_resume_skips_existing_entries(self):
        first = profile_datasets.build_profiles(
            input_path=self._input_path,
            output_path=self._output_path,
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=False,
            bucket="unused",
        )
        second = profile_datasets.build_profiles(
            input_path=self._input_path,
            output_path=self._output_path,
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=True,
            bucket="unused",
        )

        self.assertEqual(first["written"], 1)
        self.assertEqual(second, {"written": 0, "skipped": 1, "errors": 0})
        self.assertEqual(len(self._read_output_rows()), 1)

    def test_build_profiles_accepts_manifest_rows(self):
        manifest_path = self._root / "manifest.jsonl"
        local_uri = f"s3://lakeqa-yc4103-datalake/datagov/example-dataset/files/rows.csv"
        self._write_jsonl(
            manifest_path,
            [
                {
                    "dataset_id": "example-dataset",
                    "folder": "datagov",
                    "file_path": "files/rows.csv",
                    "s3_uri": local_uri,
                    "source_ref": str(self._csv_path),
                    "local_path": str(self._csv_path),
                    "size_bytes": self._csv_path.stat().st_size,
                }
            ],
        )
        self._write_jsonl(
            self._descriptions_path,
            [{"dataset_uri": local_uri, "description": "Manifest description"}],
        )

        summary = profile_datasets.build_profiles(
            input_path=manifest_path,
            output_path=self._output_path,
            input_kind="manifest",
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=False,
            bucket="unused",
        )

        self.assertEqual(summary, {"written": 1, "skipped": 0, "errors": 0})
        row = self._read_output_rows()[0]
        self.assertEqual(row["s3_uri"], local_uri)
        self.assertEqual(row["dataset_id"], "example-dataset")
        self.assertEqual(row["file_path"], "files/rows.csv")
        self.assertEqual(row["llm_description"], "Manifest description")

    def test_build_profiles_accepts_uri_list_input(self):
        uri_list_path = self._root / "table_profiles_needed.txt"
        uri_list_path.write_text(str(self._csv_path) + "\n")
        self._write_jsonl(
            self._descriptions_path,
            [
                {
                    "dataset_uri": str(self._csv_path),
                    "description": "Canonical description from merged table_descriptions",
                }
            ],
        )

        summary = profile_datasets.build_profiles(
            input_path=uri_list_path,
            output_path=self._output_path,
            input_kind="uri-list",
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=False,
            bucket="unused",
        )

        self.assertEqual(summary, {"written": 1, "skipped": 0, "errors": 0})
        row = self._read_output_rows()[0]
        self.assertEqual(row["llm_description"], "Canonical description from merged table_descriptions")
        self.assertEqual(row["filename"], "rows")

    def test_build_profiles_stringifies_nested_top_rows(self):
        manifest_path = self._root / "manifest_nested.jsonl"
        local_uri = f"s3://lakeqa-yc4103-datalake/datagov/example-dataset/files/rows.jsonl"
        self._write_jsonl(
            manifest_path,
            [
                {
                    "dataset_id": "example-dataset",
                    "folder": "datagov",
                    "file_path": "files/rows.jsonl",
                    "s3_uri": local_uri,
                    "source_ref": str(self._jsonl_path),
                    "local_path": str(self._jsonl_path),
                    "size_bytes": self._jsonl_path.stat().st_size,
                    "table_kind": "json",
                }
            ],
        )

        summary = profile_datasets.build_profiles(
            input_path=manifest_path,
            output_path=self._output_path,
            input_kind="manifest",
            descriptions_path=self._descriptions_path,
            snippets_path=self._snippets_path,
            parallel=1,
            resume=False,
            bucket="unused",
        )

        self.assertEqual(summary, {"written": 1, "skipped": 0, "errors": 0})
        row = self._read_output_rows()[0]
        self.assertEqual(row["family"], "json")
        self.assertIsInstance(row["top_2_rows"][0]["payload"], str)
        self.assertTrue(row["top_2_rows"][0]["payload"].endswith("…"))


if __name__ == "__main__":
    unittest.main()
