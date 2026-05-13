import contextlib
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PROMOTE_PATH = REPO / "other-benchmarks" / "data-imports" / "kramabench" / "promote_sample.py"
BUCKET_RE = re.compile(r"^k-(\d+)-d-(\d+)$")
EXPECTED_SOURCE_IDS = {
    "biomedical-hard-3",
    "biomedical-hard-4",
    "biomedical-hard-7",
    "legal-hard-6",
    "legal-hard-7",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_fact(fact: str) -> str:
    ns = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(fact, ns)
    return (buf.getvalue().strip() or str(ns.get("result", "")).strip())


class KramabenchPromotionSampleTests(unittest.TestCase):
    def test_promotes_five_kramabench_mini_tasks_to_fair_kd_sample(self):
        promote = load_module(PROMOTE_PATH, "kramabench_promote_sample_for_test")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "tasks-mini-kramabench-sample"
            written = promote.promote_sample_tasks(output_root=output_root)

            self.assertEqual(5, len(written))
            task_files = sorted(output_root.glob("k-*-d-*/task_*.json"))
            self.assertEqual(written, task_files)

            source_ids = set()
            for task_path in task_files:
                match = BUCKET_RE.match(task_path.parent.name)
                self.assertIsNotNone(match, task_path.parent.name)
                k, d = map(int, match.groups())
                payload = json.loads(task_path.read_text(encoding="utf-8"))

                source_ids.add(payload["_provenance"]["source_id"])
                self.assertTrue(payload["question"].endswith("Write your answer as [ANSWER]."))
                self.assertEqual(k, len(payload["reasoning_hops"]))
                self.assertEqual(d, max(len(hop["node_ids"]) for hop in payload["reasoning_hops"]))
                self.assertNotIn("-j-", task_path.parent.name)
                self.assertNotIn("-f-", task_path.parent.name)

                for node_id, node in payload["nodes"].items():
                    produced = run_fact(node["fact"])
                    self.assertEqual(node["answer"], produced, (task_path, node_id))

            self.assertEqual(EXPECTED_SOURCE_IDS, source_ids)

    def test_biomedical_hard_4_collapses_import_bucket_to_k_2_d_1(self):
        promote = load_module(PROMOTE_PATH, "kramabench_promote_sample_for_test_bio4")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir) / "tasks-mini-kramabench-sample"
            promote.promote_sample_tasks(output_root=output_root)
            task_path = output_root / "k-2-d-1" / "task_2.json"
            payload = json.loads(task_path.read_text(encoding="utf-8"))

        self.assertEqual("biomedical-hard-4", payload["_provenance"]["source_id"])
        self.assertEqual(
            "other-benchmarks/tasks-kramabench-mini/k-3-d-2-j-3-f-2/task_1.json",
            payload["_provenance"]["sample_source"],
        )
        self.assertEqual(["biomedical-mmc4", "biomedical-mmc1"], payload["datasets_used"])
        self.assertEqual([1], payload["reasoning_hops"][0]["node_ids"])
        self.assertEqual([2], payload["reasoning_hops"][1]["node_ids"])
        self.assertEqual("[\"S028\", \"S034\", \"S040\"]", payload["nodes"]["1"]["answer"])
        self.assertEqual("[\"FIGO Grade 2\"]", payload["answer"])


if __name__ == "__main__":
    unittest.main()
