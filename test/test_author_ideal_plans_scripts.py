import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


_SCRIPT_DIR = (
    Path(__file__).resolve().parent.parent
    / ".agents"
    / "skills"
    / "author-ideal-plans"
    / "scripts"
)


def _load_module(filename: str, module_name: str):
    module_path = _SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


init_plan_file = _load_module("init_plan_file.py", "author_ideal_init")
check_plan_cleanliness = _load_module("check_plan_cleanliness.py", "author_ideal_checker")


class TestAuthorIdealPlanScripts(unittest.TestCase):
    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + "\n")

    def test_build_scaffold_resolves_txt_and_v1_normalization(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            task_path = root / "tasks_mini" / "k-1-d-1" / "task_1.json"
            self._write_json(
                task_path,
                {
                    "question": "Q?",
                    "datasets_used": ["example-dataset"],
                    "reasoning_chain": ["Node 1: ..."],
                    "nodes": {
                        "1": {
                            "source": "datagov/example-dataset/v1/files/rows.csv",
                        }
                    },
                },
            )
            (root / "plans_mini" / "k-1-d-1").mkdir(parents=True, exist_ok=True)
            (root / "table_descriptions.jsonl").write_text(
                json.dumps(
                    {
                        "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/example-dataset/files/rows.txt",
                        "description": "desc",
                        "content": "content",
                    }
                )
                + "\n"
            )

            plan_path, scaffold = init_plan_file.build_scaffold(task_path)

            self.assertEqual(plan_path.resolve(), (root / "plans_mini" / "k-1-d-1" / "task_1.json").resolve())
            self.assertEqual(scaffold["dataset_sequence"], ["example-dataset"])
            self.assertEqual(
                scaffold["source_sequence"],
                ["datagov/example-dataset/files/rows.txt"],
            )

    def test_build_scaffold_uses_first_file_candidate_when_source_is_unindexed(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            task_path = root / "tasks_mini" / "k-1-d-1" / "task_2.json"
            self._write_json(
                task_path,
                {
                    "question": "Q?",
                    "datasets_used": ["example-dataset"],
                    "reasoning_chain": ["Node 1: ..."],
                    "nodes": {
                        "1": {
                            "source": "datagov/example-dataset/files/raw.csv",
                        }
                    },
                },
            )
            (root / "plans_mini" / "k-1-d-1").mkdir(parents=True, exist_ok=True)
            (root / "table_descriptions.jsonl").write_text("")

            _plan_path, scaffold = init_plan_file.build_scaffold(task_path)
            self.assertEqual(
                scaffold["source_sequence"],
                ["datagov/example-dataset/files/raw.txt"],
            )

    def test_check_plan_cleanliness_flags_source_sequence_mismatch(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            task_path = root / "tasks_mini" / "k-1-d-1" / "task_3.json"
            plan_path = root / "plans_mini" / "k-1-d-1" / "task_3.json"
            self._write_json(
                task_path,
                {
                    "question": "Q?",
                    "answer": "2020",
                    "datasets_used": ["example-dataset"],
                    "reasoning_chain": ["Node 1: ..."],
                    "nodes": {
                        "1": {
                            "source": "datagov/example-dataset/files/rows.csv",
                        }
                    },
                },
            )
            self._write_json(
                plan_path,
                {
                    "dataset_sequence": ["example-dataset"],
                    "source_sequence": ["datagov/example-dataset/files/wrong.txt"],
                    "reasoning_chain_text": ["1. Determine the answer."],
                },
            )
            (root / "table_descriptions.jsonl").write_text(
                json.dumps(
                    {
                        "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/example-dataset/files/rows.txt",
                        "description": "desc",
                        "content": "content",
                    }
                )
                + "\n"
            )

            result = check_plan_cleanliness.evaluate_plan(plan_path)
            codes = {issue["code"] for issue in result["issues"]}
            self.assertIn("source_sequence_mismatch", codes)

    def test_k_1_d_1_scaffolds_all_resolve_to_file_paths(self):
        repo_root = Path(__file__).resolve().parent.parent
        task_dir = repo_root / "tasks_mini" / "k-1-d-1"
        for task_path in sorted(task_dir.glob("task_*.json")):
            _plan_path, scaffold = init_plan_file.build_scaffold(task_path)
            self.assertTrue(scaffold["source_sequence"])
            self.assertTrue(all("/" in item for item in scaffold["source_sequence"]))


if __name__ == "__main__":
    unittest.main()
