import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SAMPLE_PATH = REPO / "other-benchmarks" / "data-imports" / "_shared" / "sample_hard.py"
PROMOTE_PATH = REPO / "other-benchmarks" / "data-imports" / "hotpotqa" / "promote_sample.py"
EXPECTED_SOURCE_IDS = [
    "5a70eee85542994082a3e3f0",
    "5a70f0a75542994082a3e403",
    "5a70f1685542994082a3e40f",
    "5a70f39c5542994082a3e429",
    "5a70f4c45542994082a3e437",
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def normalize(value: str) -> str:
    return " ".join(str(value).casefold().split())


class HotpotQAMiniPromotionTests(unittest.TestCase):
    def test_hotpotqa_mini_sampler_writes_first_five_bridge_tasks(self):
        sample = load_module(SAMPLE_PATH, "sample_hard_for_hotpotqa_test")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "tasks-hotpotqa-mini"
            written = sample.hotpotqa_mini(output_root=output_root)

            self.assertEqual(5, len(written))
            self.assertEqual(
                [output_root / "k-2-d-2" / f"task_{i}.json" for i in range(1, 6)],
                written,
            )
            source_ids = []
            for task_path in written:
                payload = json.loads(task_path.read_text(encoding="utf-8"))
                source_ids.append(payload["_provenance"]["source_id"])
                self.assertEqual(
                    str(Path("other-benchmarks/tasks/hotpotqa/k-2-d-2") / task_path.name),
                    payload["_provenance"]["sample_source"],
                )

            self.assertEqual(EXPECTED_SOURCE_IDS, source_ids)

    def test_promotes_five_hotpotqa_mini_tasks_to_lakeqa_compliant_tasks(self):
        sample = load_module(SAMPLE_PATH, "sample_hard_for_hotpotqa_promote_test")
        promote = load_module(PROMOTE_PATH, "hotpotqa_promote_sample_for_test")

        with tempfile.TemporaryDirectory() as tmpdir:
            input_root = Path(tmpdir) / "tasks-hotpotqa-mini-raw"
            output_root = Path(tmpdir) / "tasks-hotpotqa-mini-promoted"
            sample.hotpotqa_mini(output_root=input_root)

            written = promote.promote_sample_tasks(input_root=input_root, output_root=output_root)

            self.assertEqual(5, len(written))
            self.assertEqual(
                [output_root / "k-2-d-2" / f"task_{i}.json" for i in range(1, 6)],
                written,
            )
            self.assertTrue((output_root / "SKIPPED.md").exists())

            for task_path in written:
                self.assertEqual("k-2-d-2", task_path.parent.name)
                payload = json.loads(task_path.read_text(encoding="utf-8"))
                self.assertTrue(payload["question"].endswith("Write your answer as [ANSWER]."))
                self.assertEqual({"1", "2"}, set(payload["nodes"]))
                self.assertEqual(payload["answer"], payload["nodes"]["2"]["answer"])
                self.assertEqual(2, len(payload["reasoning_hops"]))
                self.assertEqual(EXPECTED_SOURCE_IDS[written.index(task_path)], payload["_provenance"]["source_id"])
                self.assertIn("transform_run_id", payload["_provenance"])
                self.assertIn("verified_at", payload["_provenance"])

                for node_id, node in payload["nodes"].items():
                    self.assertEqual({"source", "fact", "subquestion", "answer"}, set(node))
                    self.assertFalse(node["source"].startswith("hotpotqa://"))
                    self.assertTrue(node["source"].startswith("other-benchmarks/raw/hotpotqa/"))
                    self.assertNotIn("import json", node["fact"])
                    self.assertNotIn("print(", node["fact"])
                    self.assertIn(normalize(node["answer"]), normalize(node["fact"]))


if __name__ == "__main__":
    unittest.main()
