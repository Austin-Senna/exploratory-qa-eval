import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import strands_evaluation.tools.external.ideal.search_ideal as search_ideal


class TestSearchIdealPlanLoading(unittest.TestCase):
    def tearDown(self) -> None:
        search_ideal.set_plans_root("plans_mini")
        search_ideal.reset_state()

    def test_set_task_context_hard_fails_when_plan_missing(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            plans_root.mkdir(parents=True, exist_ok=True)

            search_ideal.set_plans_root(plans_root)
            with self.assertRaises(FileNotFoundError):
                search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})

    def test_search_ideal_consumes_dataset_sequence_in_batches_of_five_and_exhausts(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": [
                            "ds_one",
                            "ds_two",
                            "ds_three",
                            "ds_four",
                            "ds_five",
                            "ds_six",
                        ],
                        "reasoning_chain_text": "Step 1 then Step 2 then Step 3 then Step 4 then Step 5 then Step 6",
                    }
                )
            )

            search_ideal.set_plans_root(plans_root)
            search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})

            with patch.object(search_ideal, "_search_dataset") as mock_search:
                mock_search.side_effect = [
                    [{"uri": "s3://x/datagov/ds_one/files/rows.txt", "dataset_id": "ds_one", "document": "a"}],
                    [{"uri": "s3://x/datagov/ds_two/files/rows.txt", "dataset_id": "ds_two", "document": "b"}],
                    [{"uri": "s3://x/datagov/ds_three/files/rows.txt", "dataset_id": "ds_three", "document": "c"}],
                    [{"uri": "s3://x/datagov/ds_four/files/rows.txt", "dataset_id": "ds_four", "document": "d"}],
                    [{"uri": "s3://x/datagov/ds_five/files/rows.txt", "dataset_id": "ds_five", "document": "e"}],
                    [{"uri": "s3://x/datagov/ds_six/files/rows.txt", "dataset_id": "ds_six", "document": "f"}],
                ]

                first = search_ideal.search_ideal("q1")
                second = search_ideal.search_ideal("q2")
                third = search_ideal.search_ideal("q3")

            self.assertEqual(first.get("dataset_id"), "ds_one")
            self.assertEqual(
                first.get("dataset_ids"),
                ["ds_one", "ds_two", "ds_three", "ds_four", "ds_five"],
            )
            self.assertEqual(first.get("plan_step_number"), 1)
            self.assertEqual(first.get("plan_step_numbers"), [1, 2, 3, 4, 5])
            self.assertEqual(first.get("count"), 5)
            self.assertFalse(first.get("plan_exhausted"))

            self.assertEqual(second.get("dataset_id"), "ds_six")
            self.assertEqual(second.get("dataset_ids"), ["ds_six"])
            self.assertEqual(second.get("plan_step_number"), 6)
            self.assertEqual(second.get("count"), 1)
            self.assertTrue(second.get("plan_exhausted"))

            self.assertEqual(third.get("count"), 0)
            self.assertTrue(third.get("plan_exhausted"))
            self.assertIn("exhausted", str(third.get("note", "")).lower())


if __name__ == "__main__":
    unittest.main()
