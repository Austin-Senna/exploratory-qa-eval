import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import strands_evaluation.tools.external.ideal.search_ideal as search_ideal


class TestSearchIdealPlanLoading(unittest.TestCase):
    def tearDown(self) -> None:
        search_ideal.set_plans_root("plans_mini")
        search_ideal.reset_state()

    def test_set_task_context_hard_fails_when_source_sequence_missing(self):
        with TemporaryDirectory() as tmpdir:
            plans_root = Path(tmpdir) / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one"],
                        "reasoning_chain_text": "Step 1",
                    }
                )
            )

            search_ideal.set_plans_root(plans_root)
            with self.assertRaisesRegex(ValueError, "source_sequence"):
                search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})

    def test_search_ideal_returns_up_to_top_k_file_results_then_exhausts(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plans_root = root / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text(
                json.dumps(
                    {
                        "dataset_sequence": ["ds_one", "ds_two", "ds_three"],
                        "source_sequence": [
                            "datagov/ds_one/files/rows.txt",
                            "datagov/ds_two/files/rows.txt",
                            "datagov/ds_three/files/rows.txt",
                        ],
                        "reasoning_chain_text": "1. Step one\n2. Step two\n3. Step three",
                    }
                )
            )

            long_content = " ".join(f"w{i}" for i in range(250))
            table_path = root / "table_descriptions.jsonl"
            table_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_one/files/rows.txt",
                                "description": "Rows description one",
                                "content": long_content,
                            }
                        ),
                        json.dumps(
                            {
                                "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_two/files/rows.txt",
                                "description": "Rows description two",
                                "content": "alpha beta gamma",
                            }
                        ),
                        json.dumps(
                            {
                                "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_three/files/rows.txt",
                                "description": "Rows description three",
                                "content": "delta epsilon zeta",
                            }
                        ),
                    ]
                )
                + "\n"
            )

            search_ideal.set_plans_root(plans_root)
            search_ideal.reset_state()
            with patch.object(search_ideal, "_TABLE_DESCRIPTIONS_PATH", table_path):
                search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_1.json"})
                first = search_ideal.search_ideal("ignored query", top_k=2)
                second = search_ideal.search_ideal("another query", top_k=999)
                third = search_ideal.search_ideal("exhausted")

            self.assertEqual(first.get("count"), 2)
            self.assertEqual(first.get("dataset_id"), "ds_one")
            self.assertEqual(first.get("dataset_ids"), ["ds_one", "ds_two"])
            self.assertEqual(first.get("plan_step_number"), 1)
            self.assertEqual(first.get("plan_step_numbers"), [1, 2])
            self.assertFalse(first.get("plan_exhausted"))
            first_row, second_row = first["results"]
            self.assertEqual(first_row["dataset_id"], "ds_one")
            self.assertEqual(
                first_row["uri"],
                "s3://lakeqa-yc4103-datalake/datagov/ds_one/files/rows.txt",
            )
            self.assertEqual(first_row["description"], "Rows description one")
            self.assertEqual(len(first_row["content"].split()), 200)
            self.assertEqual(second_row["dataset_id"], "ds_two")
            self.assertEqual(
                second_row["uri"],
                "s3://lakeqa-yc4103-datalake/datagov/ds_two/files/rows.txt",
            )
            self.assertEqual(second_row["description"], "Rows description two")

            self.assertEqual(second.get("count"), 1)
            self.assertEqual(second.get("dataset_id"), "ds_three")
            self.assertEqual(second.get("dataset_ids"), ["ds_three"])
            self.assertEqual(second.get("plan_step_number"), 3)
            self.assertEqual(second.get("plan_step_numbers"), [3])
            self.assertTrue(second.get("plan_exhausted"))
            last_row = second["results"][0]
            self.assertEqual(last_row["dataset_id"], "ds_three")
            self.assertEqual(
                last_row["uri"],
                "s3://lakeqa-yc4103-datalake/datagov/ds_three/files/rows.txt",
            )

            self.assertEqual(third.get("count"), 0)
            self.assertTrue(third.get("plan_exhausted"))
            self.assertIn("exhausted", str(third.get("note", "")).lower())

    def test_search_ideal_ignores_query_but_uses_top_k_for_batch_size(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            plans_root = root / "plans_mini"
            target = plans_root / "k-1-d-1"
            target.mkdir(parents=True, exist_ok=True)
            plan_payload = {
                "dataset_sequence": ["ds_one", "ds_two"],
                "source_sequence": [
                    "datagov/ds_one/files/rows.txt",
                    "datagov/ds_two/files/rows.txt",
                ],
                "reasoning_chain_text": "1. Step one\n2. Step two",
            }
            (target / "task_2.json").write_text(json.dumps(plan_payload))

            table_path = root / "table_descriptions.jsonl"
            table_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_one/files/rows.txt",
                                "description": "Rows description one",
                                "content": "alpha beta gamma",
                            }
                        ),
                        json.dumps(
                            {
                                "dataset_uri": "s3://lakeqa-yc4103-datalake/datagov/ds_two/files/rows.txt",
                                "description": "Rows description two",
                                "content": "delta epsilon zeta",
                            }
                        ),
                    ]
                )
                + "\n"
            )

            with patch.object(search_ideal, "_TABLE_DESCRIPTIONS_PATH", table_path):
                search_ideal.set_plans_root(plans_root)
                search_ideal.reset_state()
                search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_2.json"})
                first = search_ideal.search_ideal("first query", top_k=1)

                search_ideal.reset_state()
                search_ideal.set_plans_root(plans_root)
                search_ideal.set_task_context({"task_id": "tasks_mini/k-1-d-1/task_2.json"})
                second = search_ideal.search_ideal("second query", top_k=2)

            self.assertEqual(first["count"], 1)
            self.assertEqual(second["count"], 2)
            self.assertEqual(first["results"][0], second["results"][0])
            self.assertEqual(first["dataset_id"], second["dataset_id"])
            self.assertEqual(second["dataset_ids"], ["ds_one", "ds_two"])


if __name__ == "__main__":
    unittest.main()
