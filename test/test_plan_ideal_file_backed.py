import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands_evaluation.tools.external.ideal.plan_ideal import plan_ideal
from strands_evaluation.tools.external.ideal.plan_store import (
    set_plans_root,
    set_task_context,
)


class _FakeAgent:
    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt


class _FakeToolContext:
    def __init__(self, agent: _FakeAgent) -> None:
        self.agent = agent


class TestPlanIdealFileBacked(unittest.TestCase):
    def tearDown(self) -> None:
        set_plans_root("plans_mini")
        set_task_context({})

    def test_plan_ideal_uses_file_backed_reasoning_chain(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_2.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_a", "ds_b"],
                        "source_sequence": [
                            "datagov/ds_a/files/rows.txt",
                            "datagov/ds_b/files/rows.txt",
                        ],
                        "reasoning_chain_text": "File-backed plan text.",
                    }
                )
            )

            set_plans_root(plans_root)
            set_task_context({"task_id": "tasks_mini/k-1-d-1/task_2.json"})

            fake_agent = _FakeAgent("BASE")
            fake_ctx = _FakeToolContext(fake_agent)
            msg = plan_ideal("manual should be ignored", tool_context=fake_ctx)

            self.assertIn("loaded", msg.lower())
            self.assertIn("File-backed plan text.", fake_agent.system_prompt)
            self.assertIn("STEP-BY-STEP PLANNING DIRECTIVE", fake_agent.system_prompt)
            self.assertIn("You may copy chain steps when they are already correct.", fake_agent.system_prompt)
            self.assertIn("Prefer improving the plan with clearer execution actions", fake_agent.system_prompt)
            self.assertIn("copying is allowed", msg.lower())
            self.assertNotIn("Path:", fake_agent.system_prompt)
            self.assertNotIn("Dataset sequence:", fake_agent.system_prompt)
            self.assertNotIn("manual should be ignored", fake_agent.system_prompt)

    def test_plan_ideal_joins_list_backed_reasoning_chain(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_3.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_a", "ds_b"],
                        "source_sequence": [
                            "datagov/ds_a/files/rows.txt",
                            "datagov/ds_b/files/rows.txt",
                        ],
                        "reasoning_chain_text": [
                            "1. First file-backed step.",
                            "2. Second file-backed step.",
                        ],
                    }
                )
            )

            set_plans_root(plans_root)
            set_task_context({"task_id": "tasks_mini/k-1-d-1/task_3.json"})

            fake_agent = _FakeAgent("BASE")
            fake_ctx = _FakeToolContext(fake_agent)
            plan_ideal("manual should be ignored", tool_context=fake_ctx)

            self.assertIn("1. First file-backed step.\n2. Second file-backed step.", fake_agent.system_prompt)


if __name__ == "__main__":
    unittest.main()
