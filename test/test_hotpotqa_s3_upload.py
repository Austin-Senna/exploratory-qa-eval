import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
UPLOAD_PATH = REPO / "scripts" / "upload_hotpotqa_context_to_s3.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_raw_hotpotqa(path: Path) -> None:
    payload = [
        {
            "_id": "abc123",
            "question": "Which group uses the Ida?",
            "answer": "The Yoruba",
            "supporting_facts": [["Ida (sword)", 1], ["Yoruba people", 0]],
            "type": "bridge",
            "level": "hard",
            "context": [
                [
                    "Ida (sword)",
                    [
                        "The Ida is a kind of sword.",
                        "It is a long sword with a narrow to wide blade and sheathe.",
                    ],
                ],
                [
                    "Yoruba people",
                    [
                        "The Yoruba are a West African ethnic group.",
                        "Significant Yoruba populations can be found in Ghana.",
                    ],
                ],
            ],
        }
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")


class HotpotQAContextS3UploadTests(unittest.TestCase):
    def test_parse_bucket_uri_accepts_bucket_and_optional_prefix(self):
        upload = load_module(UPLOAD_PATH, "hotpotqa_upload_for_test_parse")

        self.assertEqual("s3://sana-hotpotqa-2", upload.DEFAULT_BUCKET_URI)
        self.assertEqual(("lakeqa-yc4103-datalake", ""), upload.parse_bucket_uri("s3://lakeqa-yc4103-datalake"))
        self.assertEqual(
            ("lakeqa-yc4103-datalake", "pilot/hotpotqa"),
            upload.parse_bucket_uri("s3://lakeqa-yc4103-datalake/pilot/hotpotqa/"),
        )

    def test_materializes_context_files_and_manifest_without_labels(self):
        upload = load_module(UPLOAD_PATH, "hotpotqa_upload_for_test_materialize")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            raw_path = tmp / "hotpot.json"
            manifest_path = tmp / "manifest.jsonl"
            write_raw_hotpotqa(raw_path)

            items = upload.materialize_uploads(
                bucket_uri="s3://lakeqa-yc4103-datalake/pilot",
                raw_path=raw_path,
                staging_dir=tmp / "staging",
                manifest_path=manifest_path,
            )

            self.assertEqual(
                [
                    "pilot/wikipedia/hotpotqa__abc123/files/Ida_(sword).txt",
                    "pilot/wikipedia/hotpotqa__abc123/files/Yoruba_people.txt",
                ],
                [item.key for item in items],
            )
            for item in items:
                text = item.local_path.read_text(encoding="utf-8")
                self.assertIn("HotpotQA Source ID: abc123", text)
                self.assertIn("[0]", text)
                self.assertNotIn("supporting_facts", text)
                self.assertNotIn("answer", text.lower())

            rows = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([item.s3_uri for item in items], [row["s3_uri"] for row in rows])
            self.assertEqual(["abc123", "abc123"], [row["source_id"] for row in rows])

    def test_upload_uses_injected_client(self):
        upload = load_module(UPLOAD_PATH, "hotpotqa_upload_for_test_upload")

        calls = []

        class FakeClient:
            def upload_file(self, filename, bucket, key):
                calls.append((Path(filename).name, bucket, key))

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            raw_path = tmp / "hotpot.json"
            write_raw_hotpotqa(raw_path)
            items = upload.materialize_uploads(
                bucket_uri="s3://bucket-name/prefix",
                raw_path=raw_path,
                staging_dir=tmp / "staging",
                manifest_path=tmp / "manifest.jsonl",
            )
            uploaded = upload.upload_materialized_files(items, s3_client=FakeClient())

        self.assertEqual(items, uploaded)
        self.assertEqual(
            [
                ("Ida_(sword).txt", "bucket-name", "prefix/wikipedia/hotpotqa__abc123/files/Ida_(sword).txt"),
                ("Yoruba_people.txt", "bucket-name", "prefix/wikipedia/hotpotqa__abc123/files/Yoruba_people.txt"),
            ],
            calls,
        )

    def test_upload_can_use_aws_cli_backend(self):
        upload = load_module(UPLOAD_PATH, "hotpotqa_upload_for_test_aws_cli")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            raw_path = tmp / "hotpot.json"
            write_raw_hotpotqa(raw_path)
            items = upload.materialize_uploads(
                bucket_uri="s3://bucket-name/prefix",
                raw_path=raw_path,
                staging_dir=tmp / "staging",
                manifest_path=tmp / "manifest.jsonl",
            )
            calls = []

            uploaded = upload.upload_materialized_files(
                items,
                uploader="aws-cli",
                run_command=calls.append,
            )

        self.assertEqual(items, uploaded)
        self.assertEqual(
            [
                ["aws", "s3", "cp", str(items[0].local_path), items[0].s3_uri],
                ["aws", "s3", "cp", str(items[1].local_path), items[1].s3_uri],
            ],
            calls,
        )

    def test_reads_source_ids_from_task_directory(self):
        upload = load_module(UPLOAD_PATH, "hotpotqa_upload_for_test_tasks_dir")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            task_dir = root / "k-2-d-1"
            task_dir.mkdir()
            (task_dir / "task_1.json").write_text(
                json.dumps({"_provenance": {"source_id": "abc123"}}),
                encoding="utf-8",
            )
            (task_dir / "task_2.json").write_text(
                json.dumps(
                    {
                        "datasets_used": [
                            "other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json#5a74a8fa55429929fddd8497:Title"
                        ]
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual({"abc123", "5a74a8fa55429929fddd8497"}, upload._source_ids_from_tasks_dir(root))


if __name__ == "__main__":
    unittest.main()
