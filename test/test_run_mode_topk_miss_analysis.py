import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.run_mode_topk_miss_analysis import run_analysis


class TestRunModeTopkMissAnalysis(unittest.TestCase):
    def _write_task(self, path: Path, datasets_used: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"datasets_used": datasets_used}))

    def _write_trace(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for record in records:
                handle.write(json.dumps(record))
                handle.write("\n")

    def test_run_analysis_counts_topk_misses_per_tool_and_mode(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_topk_miss"
            variant = "search_n_results_i_plani_k5"

            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_task(tasks_root / "k-1-d-1" / "task_2.json", ["ds2"])

            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "turn": 1,
                        "tool": "search_value",
                        "query": "query one",
                        "result_dataset_ids": ["a", "b", "c", "d", "e", "ds1"],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "turn": 2,
                        "tool": "search_schema",
                        "query": "query one schema",
                        "result_dataset_ids": ["ds1", "z"],
                    },
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_2.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "turn": 1,
                        "tool": "search_value",
                        "query": "query two",
                        "result_dataset_ids": ["x", "ds2"],
                    }
                ],
            )

            outputs = run_analysis(
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                top_k=5,
            )

            summary = outputs["summary"]
            self.assertEqual(len(summary), 2)

            search_value = next(row for row in summary if row["search_call_tool"] == "search_value")
            self.assertEqual(search_value["search_calls"], 2)
            self.assertEqual(search_value["top_k_hits"], 1)
            self.assertEqual(search_value["top_k_misses"], 1)
            self.assertEqual(search_value["top_k_miss_rate"], 0.5)
            self.assertEqual(search_value["returned_anywhere_hits"], 2)
            self.assertEqual(search_value["returned_anywhere_misses"], 0)
            self.assertEqual(search_value["tasks_with_calls"], 2)
            self.assertEqual(search_value["tasks_with_any_top_k_miss"], 1)
            self.assertEqual(search_value["tasks_with_all_top_k_miss"], 1)

            search_schema = next(row for row in summary if row["search_call_tool"] == "search_schema")
            self.assertEqual(search_schema["search_calls"], 1)
            self.assertEqual(search_schema["top_k_misses"], 0)

            variant_summary = outputs["variant_summary"]
            self.assertEqual(len(variant_summary), 2)
            first_hit_rows = outputs["first_hit_rounds_variant"]
            self.assertEqual(len(first_hit_rows), 3)
            self.assertTrue((output_root / "summary.csv").exists())
            self.assertTrue((output_root / "variant_summary.csv").exists())
            self.assertTrue((output_root / "first_hit_rounds_variant.csv").exists())
            self.assertTrue((output_root / "per_call.csv").exists())
            self.assertTrue((output_root / "figures" / "fig_topk_miss_rate_variant.pdf").exists())
            self.assertTrue((output_root / "figures" / "fig_topk_miss_count_variant.pdf").exists())
            self.assertTrue((output_root / "figures" / "fig_first_hit_rounds_variant.pdf").exists())
            self.assertFalse((output_root / "figures" / "fig_topk_miss_rate_model_variant.pdf").exists())
            self.assertFalse((output_root / "figures" / "fig_topk_miss_count_model_variant.pdf").exists())

            top1_row = next(row for row in first_hit_rows if row["cutoff"] == 1)
            self.assertEqual(top1_row["n_tasks"], 2)
            self.assertEqual(top1_row["found_tasks"], 1)
            self.assertEqual(top1_row["not_found_tasks"], 1)
            self.assertEqual(top1_row["round_counts"], {"2": 1})
            self.assertEqual(top1_row["cumulative_found_rates"], {"1": 0.0, "2": 0.5})

            top3_row = next(row for row in first_hit_rows if row["cutoff"] == 3)
            self.assertEqual(top3_row["n_tasks"], 2)
            self.assertEqual(top3_row["found_tasks"], 2)
            self.assertEqual(top3_row["not_found_tasks"], 0)
            self.assertEqual(top3_row["round_counts"], {"1": 1, "2": 1})
            self.assertEqual(top3_row["cumulative_found_rates"], {"1": 0.5, "2": 1.0})

            miss_call = next(row for row in outputs["per_call"] if row["search_call_tool"] == "search_value" and row["turn"] == 1)
            self.assertEqual(miss_call["search_round"], 1)
            self.assertEqual(miss_call["gold_rank"], 6)
            self.assertEqual(miss_call["gold_in_top_k"], 0)
            self.assertEqual(miss_call["gold_in_top_1"], 0)
            self.assertEqual(miss_call["gold_in_top_3"], 0)
            self.assertEqual(miss_call["gold_in_top_5"], 0)
            self.assertEqual(miss_call["gold_returned_anywhere"], 1)

            hit_call = next(row for row in outputs["per_call"] if row["search_call_tool"] == "search_schema")
            self.assertEqual(hit_call["search_round"], 2)
            self.assertEqual(hit_call["gold_in_top_1"], 1)

    def test_run_analysis_uses_file_order_for_first_hit_when_turn_missing(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_topk_miss"
            variant = "search_i_results_i_plani_k5"

            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "tool": "search_ideal",
                        "query": "first query",
                        "result_dataset_ids": ["other"],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "tool": "search_ideal",
                        "query": "second query",
                        "result_dataset_ids": ["ds1"],
                    },
                ],
            )

            outputs = run_analysis(
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                top_k=5,
                no_figures=True,
            )

            top5_row = next(row for row in outputs["first_hit_rounds_variant"] if row["cutoff"] == 5)
            self.assertEqual(top5_row["n_tasks"], 1)
            self.assertEqual(top5_row["round_counts"], {"2": 1})

            per_calls = outputs["per_call"]
            self.assertEqual(per_calls[0]["search_round"], 1)
            self.assertEqual(per_calls[1]["search_round"], 2)


if __name__ == "__main__":
    unittest.main()
