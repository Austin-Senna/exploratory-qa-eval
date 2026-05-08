import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.search_analysis import generate_search_bottleneck_figures, run_analysis


class TestSearchAnalysisBottleneck(unittest.TestCase):
    def _write_task(self, path: Path, datasets_used: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"datasets_used": datasets_used}))

    def _write_agent_results(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for row in rows:
                handle.write(json.dumps(row))
                handle.write("\n")

    def _write_trace(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for row in rows:
                handle.write(json.dumps(row))
                handle.write("\n")

    def test_run_analysis_writes_search_bottleneck_outputs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results"
            traces_root = results_root / "traces"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_search"

            variant = "search_i_results_i_plani_k5"
            base_condition = "a"
            model = "openai_gpt-5.2-xhigh"
            condition_model = f"{variant}/{base_condition}/{model}"

            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["gold1"])
            self._write_task(tasks_root / "k-1-d-1" / "task_2.json", ["gold2"])
            self._write_task(tasks_root / "k-1-d-1" / "task_3.json", ["gold3"])
            self._write_task(tasks_root / "k-1-d-1" / "task_4.json", ["gold4"])

            self._write_agent_results(
                results_root / variant / base_condition / model / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "exact_match": 1,
                        "f1_score": 1.0,
                        "cost_usd": 0.1,
                        "ideal_subagent_cost_usd": 0.01,
                        "total_cost_with_ideal_subagents_usd": 0.11,
                        "tool_calls_total": 2,
                        "time": 1.0,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 1, "success_count": 1},
                            {"name": "search_schema", "call_count": 1, "success_count": 1},
                        ],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "exact_match": 0,
                        "f1_score": 0.0,
                        "cost_usd": 0.2,
                        "ideal_subagent_cost_usd": 0.02,
                        "tool_calls_total": 2,
                        "time": 2.0,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 2, "success_count": 2},
                        ],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_3.json",
                        "exact_match": 1,
                        "f1_score": 1.0,
                        "cost_usd": 0.15,
                        "tool_calls_total": 1,
                        "time": 1.5,
                        "tool_counts": [
                            {"name": "search_schema", "call_count": 1, "success_count": 1},
                        ],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_4.json",
                        "exact_match": 0,
                        "f1_score": 0.0,
                        "cost_usd": 0.05,
                        "tool_calls_total": 0,
                        "time": 0.5,
                        "tool_counts": [],
                    },
                ],
            )

            self._write_trace(
                traces_root / variant / base_condition / model / "k-1-d-1" / "task_1.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "turn": 1,
                        "tool": "search_ideal",
                        "result_dataset_ids": ["x", "y", "gold1"],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "turn": 1,
                        "tool": "query_file",
                        "read_dataset_ids": ["gold1"],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "turn": 2,
                        "tool": "search_schema",
                        "result_dataset_ids": ["gold1"],
                    },
                ],
            )
            self._write_trace(
                traces_root / variant / base_condition / model / "k-1-d-1" / "task_2.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "turn": 1,
                        "tool": "search_ideal",
                        "result_dataset_ids": ["a"],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "turn": 2,
                        "tool": "search_ideal",
                        "result_dataset_ids": ["b"],
                    },
                ],
            )
            self._write_trace(
                traces_root / variant / base_condition / model / "k-1-d-1" / "task_3.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_3.json",
                        "turn": 1,
                        "tool": "search_schema",
                        "result_dataset_ids": ["gold3", "other"],
                    }
                ],
            )
            self._write_trace(
                traces_root / variant / base_condition / model / "k-1-d-1" / "task_4.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_4.json",
                        "turn": 1,
                        "tool": "submit_answer",
                    }
                ],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=True,
            )

            self.assertTrue((output_root / "search_first_hit_condition.json").exists())
            self.assertTrue((output_root / "search_first_hit_tool.json").exists())
            self.assertTrue((output_root / "search_topk_miss_tool.json").exists())
            self.assertTrue((output_root / "search_tool_efficiency.json").exists())
            self.assertTrue((output_root / "per_task_search_bottleneck.csv").exists())
            self.assertTrue((output_root / "per_task_search_tool_bottleneck.csv").exists())

            summary = outputs["summary"]
            self.assertEqual(len(summary), 1)
            summary_row = summary[0]
            self.assertEqual(summary_row["condition_model"], condition_model)
            self.assertEqual(summary_row["n_tasks_with_search"], 3)
            self.assertEqual(summary_row["total_cost_usd"], 0.5)
            self.assertEqual(summary_row["total_ideal_subagent_cost_usd"], 0.03)
            self.assertEqual(summary_row["total_cost_with_ideal_subagents_usd"], 0.53)
            self.assertEqual(summary_row["avg_total_cost_with_ideal_subagents_usd"], 0.1325)
            self.assertEqual(summary_row["n_tasks_without_search"], 1)
            self.assertEqual(summary_row["found_tasks_top_1"], 2)
            self.assertEqual(summary_row["not_found_tasks_top_1"], 1)
            self.assertAlmostEqual(summary_row["top1_not_found_rate"], 1 / 3, places=4)
            self.assertAlmostEqual(summary_row["avg_first_hit_round_top_1"], 1.5, places=4)
            self.assertAlmostEqual(summary_row["avg_wasted_rounds_top_5"], 2 / 3, places=4)

            condition_rows = outputs["search_bottleneck"]["condition_summary_rows"]
            top1_condition = next(row for row in condition_rows if row["cutoff"] == 1)
            self.assertEqual(top1_condition["found_tasks"], 2)
            self.assertEqual(top1_condition["not_found_tasks"], 1)
            self.assertEqual(top1_condition["n_tasks_with_search"], 3)
            self.assertEqual(top1_condition["n_tasks_without_search"], 1)
            self.assertEqual(top1_condition["round_counts"], {"1": 1, "2": 1})
            self.assertEqual(top1_condition["cumulative_found_rates"], {"1": 0.3333, "2": 0.6667})

            tool_rows = outputs["search_bottleneck"]["tool_first_hit_rows"]
            schema_top1 = next(
                row for row in tool_rows if row["search_tool"] == "search_schema" and row["cutoff"] == 1
            )
            self.assertEqual(schema_top1["tasks_with_tool"], 2)
            self.assertEqual(schema_top1["found_tasks"], 2)
            self.assertEqual(schema_top1["avg_first_hit_round_found_only"], 1.0)

            ideal_top1 = next(
                row for row in tool_rows if row["search_tool"] == "search_ideal" and row["cutoff"] == 1
            )
            self.assertEqual(ideal_top1["tasks_with_tool"], 2)
            self.assertEqual(ideal_top1["found_tasks"], 0)
            self.assertEqual(ideal_top1["not_found_rate"], 1.0)

            miss_rows = outputs["search_bottleneck"]["tool_miss_rows"]
            ideal_top3 = next(
                row for row in miss_rows if row["search_tool"] == "search_ideal" and row["cutoff"] == 3
            )
            self.assertEqual(ideal_top3["n_calls"], 3)
            self.assertEqual(ideal_top3["hit_calls"], 1)
            self.assertEqual(ideal_top3["miss_calls"], 2)
            self.assertAlmostEqual(ideal_top3["miss_rate"], 2 / 3, places=4)

            schema_top1_miss = next(
                row for row in miss_rows if row["search_tool"] == "search_schema" and row["cutoff"] == 1
            )
            self.assertEqual(schema_top1_miss["n_calls"], 2)
            self.assertEqual(schema_top1_miss["hit_calls"], 2)
            self.assertEqual(schema_top1_miss["miss_calls"], 0)

            tool_task_rows = outputs["search_bottleneck"]["per_task_tool_rows"]
            task1_schema = next(
                row
                for row in tool_task_rows
                if row["task_id"] == "k-1-d-1/task_1" and row["search_tool"] == "search_schema"
            )
            self.assertEqual(task1_schema["first_hit_round_top_1"], 1)

            task_rows = outputs["search_bottleneck"]["per_task_rows"]
            task1_global = next(row for row in task_rows if row["task_id"] == "k-1-d-1/task_1")
            self.assertEqual(task1_global["first_hit_round_top_1"], 2)

            per_call_rows = outputs["search_bottleneck"]["per_call_rows"]
            task1_second_call = next(
                row
                for row in per_call_rows
                if row["task_id"] == "k-1-d-1/task_1" and row["search_call_index"] == 2
            )
            self.assertEqual(task1_second_call["search_tool"], "search_schema")
            self.assertEqual(task1_second_call["gold_hits_top_1"], 1)
            self.assertAlmostEqual(task1_second_call["gold_recall_top_5"], 1.0, places=4)
            self.assertAlmostEqual(task1_second_call["cumulative_search_gold_recall"], 1.0, places=4)
            self.assertAlmostEqual(task1_second_call["cumulative_read_gold_recall"], 1.0, places=4)

            task1_first_call = next(
                row
                for row in per_call_rows
                if row["task_id"] == "k-1-d-1/task_1" and row["search_call_index"] == 1
            )
            self.assertAlmostEqual(task1_first_call["cumulative_search_gold_recall"], 1.0, places=4)
            self.assertAlmostEqual(task1_first_call["cumulative_read_gold_recall"], 1.0, places=4)

    def test_generate_search_bottleneck_figures(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            figure_root = root / "analysis_results_search"
            figure_root.mkdir(parents=True, exist_ok=True)
            search_bottleneck = {
                "condition_summary_rows": [
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "cutoff": 1,
                        "max_round": 2,
                        "not_found_rate": 0.3333,
                        "cumulative_found_rates": {"1": 0.3333, "2": 0.6667},
                    },
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "cutoff": 3,
                        "max_round": 2,
                        "not_found_rate": 0.3333,
                        "cumulative_found_rates": {"1": 0.6667, "2": 0.6667},
                    },
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "cutoff": 5,
                        "max_round": 2,
                        "not_found_rate": 0.3333,
                        "cumulative_found_rates": {"1": 0.6667, "2": 0.6667},
                    },
                ],
                "tool_first_hit_rows": [
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 1,
                        "max_round": 2,
                        "not_found_rate": 1.0,
                        "cumulative_found_rates": {"1": 0.0, "2": 0.0},
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 1,
                        "max_round": 1,
                        "not_found_rate": 0.0,
                        "cumulative_found_rates": {"1": 1.0},
                    },
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 3,
                        "max_round": 2,
                        "not_found_rate": 0.5,
                        "cumulative_found_rates": {"1": 0.5, "2": 0.5},
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 3,
                        "max_round": 1,
                        "not_found_rate": 0.0,
                        "cumulative_found_rates": {"1": 1.0},
                    },
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 5,
                        "max_round": 2,
                        "not_found_rate": 0.5,
                        "cumulative_found_rates": {"1": 0.5, "2": 0.5},
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 5,
                        "max_round": 1,
                        "not_found_rate": 0.0,
                        "cumulative_found_rates": {"1": 1.0},
                    },
                ],
                "tool_miss_rows": [
                    {"search_tool": "search_ideal", "cutoff": 1, "miss_rate": 1.0},
                    {"search_tool": "search_schema", "cutoff": 1, "miss_rate": 0.0},
                    {"search_tool": "search_ideal", "cutoff": 3, "miss_rate": 0.5},
                    {"search_tool": "search_schema", "cutoff": 3, "miss_rate": 0.0},
                    {"search_tool": "search_ideal", "cutoff": 5, "miss_rate": 0.5},
                    {"search_tool": "search_schema", "cutoff": 5, "miss_rate": 0.0},
                ],
                "tool_efficiency_rows": [
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 1,
                        "ever_found_rate": 0.0,
                        "avg_wasted_rounds": 2.0,
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 1,
                        "ever_found_rate": 1.0,
                        "avg_wasted_rounds": 0.0,
                    },
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 3,
                        "ever_found_rate": 0.5,
                        "avg_wasted_rounds": 1.0,
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 3,
                        "ever_found_rate": 1.0,
                        "avg_wasted_rounds": 0.0,
                    },
                    {
                        "search_tool": "search_ideal",
                        "cutoff": 5,
                        "ever_found_rate": 0.5,
                        "avg_wasted_rounds": 1.0,
                    },
                    {
                        "search_tool": "search_schema",
                        "cutoff": 5,
                        "ever_found_rate": 1.0,
                        "avg_wasted_rounds": 0.0,
                    },
                ],
                "per_call_rows": [
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "task_id": "k-1-d-1/task_1",
                        "variant": "search_i_results_i_plani_k5",
                        "base_condition": "a",
                        "search_call_index": 1,
                        "cumulative_search_gold_recall": 0.3333,
                        "cumulative_read_gold_recall": 0.0,
                    },
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "task_id": "k-1-d-1/task_1",
                        "variant": "search_i_results_i_plani_k5",
                        "base_condition": "a",
                        "search_call_index": 2,
                        "cumulative_search_gold_recall": 0.6667,
                        "cumulative_read_gold_recall": 0.3333,
                    },
                    {
                        "condition": "search_i_results_i_plani_k5/a",
                        "task_id": "k-1-d-1/task_2",
                        "variant": "search_i_results_i_plani_k5",
                        "base_condition": "a",
                        "search_call_index": 1,
                        "cumulative_search_gold_recall": 1.0,
                        "cumulative_read_gold_recall": 1.0,
                    },
                ],
            }
            generate_search_bottleneck_figures(search_bottleneck, figure_root)
            figure_dir = figure_root / "figures"
            self.assertTrue((figure_dir / "fig15_search_cumulative_retrieval_recall_condition.pdf").exists())
            self.assertTrue((figure_dir / "fig16_search_cumulative_access_recall_condition.pdf").exists())
            self.assertTrue((figure_dir / "fig17_search_topk_miss_by_tool.pdf").exists())
            self.assertTrue((figure_dir / "fig18_search_tool_coverage_waste.pdf").exists())


if __name__ == "__main__":
    unittest.main()
