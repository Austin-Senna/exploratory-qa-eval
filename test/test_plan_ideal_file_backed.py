import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands_evaluation.tools.external.ideal.plan_ideal import (
    inject_reasoning_chain_prompt,
    plan_ideal,
)
from strands_evaluation.tools.external.ideal.plan_store import (
    load_plan_for_context,
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

    def test_inject_reasoning_chain_prompt_uses_file_backed_reasoning_chain(self):
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

            plan = load_plan_for_context()
            prompt = inject_reasoning_chain_prompt("BASE", plan.reasoning_chain_text)

            self.assertIn("## GOLD REASONING CHAIN", prompt)
            self.assertIn("File-backed plan text.", prompt)
            self.assertIn("brief and action-oriented", prompt)
            self.assertNotIn("Path:", prompt)
            self.assertNotIn("Dataset sequence:", prompt)
            self.assertNotIn("dataset_sequence", prompt)

    def test_inject_reasoning_chain_prompt_joins_list_backed_reasoning_chain(self):
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

            plan = load_plan_for_context()
            prompt = inject_reasoning_chain_prompt("BASE", plan.reasoning_chain_text)

            self.assertIn("1. First file-backed step.\n2. Second file-backed step.", prompt)

    def test_plan_ideal_records_execution_plan_and_preserves_gold_chain(self):
        gold_prompt = inject_reasoning_chain_prompt("BASE", "1. Gold step.")
        fake_agent = _FakeAgent(gold_prompt)
        fake_ctx = _FakeToolContext(fake_agent)

        plan_text = "1. Find the dataset | search_ideal\n2. Run the aggregation | query_file"
        msg = plan_ideal(plan_text, tool_context=fake_ctx)

        self.assertEqual("Ideal execution plan recorded.", msg)
        self.assertIn("## GOLD REASONING CHAIN", fake_agent.system_prompt)
        self.assertIn("1. Gold step.", fake_agent.system_prompt)
        self.assertIn("## IDEAL EXECUTION PLAN", fake_agent.system_prompt)
        self.assertIn(plan_text, fake_agent.system_prompt)

    def test_plan_ideal_overwrites_only_execution_plan_section(self):
        gold_prompt = inject_reasoning_chain_prompt("BASE", "1. Gold step.")
        fake_agent = _FakeAgent(gold_prompt)
        fake_ctx = _FakeToolContext(fake_agent)

        plan_ideal("1. First pass | search_ideal", tool_context=fake_ctx)
        plan_ideal("1. Revised pass | query_file", tool_context=fake_ctx)

        self.assertEqual(1, fake_agent.system_prompt.count("## GOLD REASONING CHAIN"))
        self.assertEqual(1, fake_agent.system_prompt.count("## IDEAL EXECUTION PLAN"))
        self.assertIn("1. Gold step.", fake_agent.system_prompt)
        self.assertIn("1. Revised pass | query_file", fake_agent.system_prompt)
        self.assertNotIn("1. First pass | search_ideal", fake_agent.system_prompt)


if __name__ == "__main__":
    unittest.main()
