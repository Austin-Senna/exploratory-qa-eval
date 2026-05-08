import csv
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.run_mode_analysis_semantic import _parse_variant, run_analysis


class TestRunModeAnalysisSemantic(unittest.TestCase):
    def test_parse_variant_exposes_plan_and_skills_axes(self):
        axes = _parse_variant("search_p_results_i_pland_computei_skills_on")
        self.assertEqual(axes["plan"], "standard")
        self.assertEqual(axes["skills"], "on")
        self.assertNotIn("agent_management", axes)
        self.assertNotIn("plan_skills", axes)

    def _write_eval_results(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "task_id",
            "model",
            "expected_answer",
            "predicted_answer",
            "exact_match",
            "semantic_match",
            "semantic_reason",
            "semantic_bucket",
            "log_error_bucket",
            "log_error_evidence",
            "runtime_seconds",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "cost_usd",
            "ideal_subagent_cost_usd",
            "total_cost_with_ideal_subagents_usd",
            "tool_calls_total",
            "api_tool_calls",
            "error",
        ]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_grouped_turn_waste_results(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "task_id",
            "model",
            "expected_answer",
            "predicted_answer",
            "exact_match",
            "semantic_match",
            "semantic_reason",
            "semantic_bucket",
            "log_error_bucket",
            "log_error_evidence",
            "runtime_seconds",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "cost_usd",
            "ideal_subagent_cost_usd",
            "total_cost_with_ideal_subagents_usd",
            "tool_calls_total",
            "api_tool_calls",
            "error",
            "turn_waste_summary",
            "turn_repeated_behavior",
            "turn_progress_stop_point",
            "productive_turn_ranges",
            "wasted_turn_ranges",
            "estimated_wasted_turns",
            "turn_budget_failure_reason",
            "turn_waste_evidence",
            "turn_waste_local_group",
            "turn_waste_local_group_reason",
            "turn_waste_global_group",
            "turn_waste_global_group_reason",
        ]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_agent_results(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for row in rows:
                handle.write(json.dumps(row))
                handle.write("\n")

    def _write_trace(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for record in records:
                handle.write(json.dumps(record))
                handle.write("\n")

    def _write_task(self, path: Path, datasets_used: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"datasets_used": datasets_used}))

    def test_run_analysis_restores_search_style_semantic_outputs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            grouped_turn_waste_root = root / "results-ec2_semantic_turn_waste_grouped" / "modes"
            base_results_root = root / "results-ec2" / "modes"
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_semantic"

            variant_a = "search_i_results_i_plani_k5"
            variant_b = "search_n_results_i_pland_k5"

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant_a / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "ideal_subagent_cost_usd": "0.01",
                        "total_cost_with_ideal_subagents_usd": "0.11",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2021",
                        "predicted_answer": "unknown",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "blank answer",
                        "semantic_bucket": "answer_unknown_blank",
                        "log_error_bucket": "error_tokens_reached",
                        "log_error_evidence": "MaxTokensReachedException",
                        "runtime_seconds": "20",
                        "input_tokens": "200",
                        "output_tokens": "30",
                        "total_tokens": "230",
                        "cost_usd": "0.20",
                        "ideal_subagent_cost_usd": "0.03",
                        "total_cost_with_ideal_subagents_usd": "0.23",
                        "tool_calls_total": "6",
                        "api_tool_calls": "3",
                        "error": "MaxTokensReachedException",
                    },
                ],
            )
            self._write_grouped_turn_waste_results(
                grouped_turn_waste_root / "openai_gpt-5.2-xhigh" / variant_a / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                        "turn_waste_summary": "",
                        "turn_repeated_behavior": "",
                        "turn_progress_stop_point": "",
                        "productive_turn_ranges": "",
                        "wasted_turn_ranges": "",
                        "estimated_wasted_turns": "",
                        "turn_budget_failure_reason": "",
                        "turn_waste_evidence": "",
                        "turn_waste_local_group": "",
                        "turn_waste_local_group_reason": "",
                        "turn_waste_global_group": "",
                        "turn_waste_global_group_reason": "",
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2021",
                        "predicted_answer": "unknown",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "blank answer",
                        "semantic_bucket": "answer_unknown_blank",
                        "log_error_bucket": "error_tokens_reached",
                        "log_error_evidence": "MaxTokensReachedException",
                        "runtime_seconds": "20",
                        "input_tokens": "200",
                        "output_tokens": "30",
                        "total_tokens": "230",
                        "cost_usd": "0.20",
                        "tool_calls_total": "6",
                        "api_tool_calls": "3",
                        "error": "MaxTokensReachedException",
                        "turn_waste_summary": "spent budget repeating probes",
                        "turn_repeated_behavior": "repeated probe queries",
                        "turn_progress_stop_point": "before final answer",
                        "productive_turn_ranges": "1-2",
                        "wasted_turn_ranges": "3-4",
                        "estimated_wasted_turns": "2",
                        "turn_budget_failure_reason": "token limit",
                        "turn_waste_evidence": "probe loop",
                        "turn_waste_local_group": "probe_loop",
                        "turn_waste_local_group_reason": "local",
                        "turn_waste_global_group": "query_reformulation_loop",
                        "turn_waste_global_group_reason": "canonical",
                    },
                ],
            )

            self._write_eval_results(
                results_root / "openai_gpt-5.4-mini" / variant_a / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.4-mini",
                        "expected_answer": "2020",
                        "predicted_answer": "2022",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "wrong year",
                        "semantic_bucket": "semantic_incorrect",
                        "log_error_bucket": "error_turns_exhausted",
                        "log_error_evidence": "Timeout reached",
                        "runtime_seconds": "30",
                        "input_tokens": "300",
                        "output_tokens": "40",
                        "total_tokens": "340",
                        "cost_usd": "0.30",
                        "tool_calls_total": "8",
                        "api_tool_calls": "5",
                        "error": "Timeout reached",
                    }
                ],
            )
            self._write_grouped_turn_waste_results(
                grouped_turn_waste_root / "openai_gpt-5.4-mini" / variant_a / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.4-mini",
                        "expected_answer": "2020",
                        "predicted_answer": "2022",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "wrong year",
                        "semantic_bucket": "semantic_incorrect",
                        "log_error_bucket": "error_turns_exhausted",
                        "log_error_evidence": "Timeout reached",
                        "runtime_seconds": "30",
                        "input_tokens": "300",
                        "output_tokens": "40",
                        "total_tokens": "340",
                        "cost_usd": "0.30",
                        "tool_calls_total": "8",
                        "api_tool_calls": "5",
                        "error": "Timeout reached",
                        "turn_waste_summary": "kept inspecting same files",
                        "turn_repeated_behavior": "repeated inspect targets",
                        "turn_progress_stop_point": "mid-analysis",
                        "productive_turn_ranges": "1-3",
                        "wasted_turn_ranges": "4-6",
                        "estimated_wasted_turns": "3",
                        "turn_budget_failure_reason": "turn budget",
                        "turn_waste_evidence": "inspection loop",
                        "turn_waste_local_group": "inspection_loop",
                        "turn_waste_local_group_reason": "local",
                        "turn_waste_global_group": "schema_file_inspection_loop",
                        "turn_waste_global_group_reason": "canonical",
                    }
                ],
            )

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant_b / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "2020",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "15",
                        "input_tokens": "150",
                        "output_tokens": "25",
                        "total_tokens": "175",
                        "cost_usd": "0.15",
                        "tool_calls_total": "5",
                        "api_tool_calls": "2",
                        "error": "",
                    }
                ],
            )
            self._write_grouped_turn_waste_results(
                grouped_turn_waste_root / "openai_gpt-5.2-xhigh" / variant_b / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "2020",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "15",
                        "input_tokens": "150",
                        "output_tokens": "25",
                        "total_tokens": "175",
                        "cost_usd": "0.15",
                        "tool_calls_total": "5",
                        "api_tool_calls": "2",
                        "error": "",
                        "turn_waste_summary": "",
                        "turn_repeated_behavior": "",
                        "turn_progress_stop_point": "",
                        "productive_turn_ranges": "",
                        "wasted_turn_ranges": "",
                        "estimated_wasted_turns": "",
                        "turn_budget_failure_reason": "",
                        "turn_waste_evidence": "",
                        "turn_waste_local_group": "",
                        "turn_waste_local_group_reason": "",
                        "turn_waste_global_group": "",
                        "turn_waste_global_group_reason": "",
                    }
                ],
            )

            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant_a / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.10,
                        "time": 10,
                        "tool_calls_total": 4,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 1, "success_count": 1},
                            {"name": "query_file", "call_count": 2, "success_count": 2},
                            {"name": "submit_answer", "call_count": 1, "success_count": 1},
                        ],
                    },
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "cost_usd": 0.20,
                        "time": 20,
                        "tool_calls_total": 6,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 1, "success_count": 1},
                            {"name": "query_file", "call_count": 1, "success_count": 0},
                            {"name": "peek_file", "call_count": 1, "success_count": 1},
                            {"name": "submit_answer", "call_count": 1, "success_count": 1},
                        ],
                    },
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.4-mini" / variant_a / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.30,
                        "time": 30,
                        "tool_calls_total": 8,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 1, "success_count": 1},
                            {"name": "execute_code", "call_count": 1, "success_count": 0},
                            {"name": "submit_answer", "call_count": 1, "success_count": 1},
                        ],
                    }
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant_b / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.15,
                        "time": 15,
                        "tool_calls_total": 5,
                        "tool_counts": [
                            {"name": "search_value", "call_count": 1, "success_count": 1},
                            {"name": "query_file", "call_count": 1, "success_count": 1},
                            {"name": "submit_answer", "call_count": 1, "success_count": 1},
                        ],
                    }
                ],
            )

            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_task(tasks_root / "k-1-d-1" / "task_2.json", ["ds2"])

            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_a / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search_ideal", "result_dataset_ids": ["ds1", "other"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_a / "k-1-d-1" / "task_2.jsonl",
                [
                    {"tool": "search_ideal", "result_dataset_ids": ["other"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.4-mini" / variant_a / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search_ideal", "result_dataset_ids": ["ds1"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_b / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search_value", "result_dataset_ids": ["ds1"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                base_results_dir=str(base_results_root),
                turn_waste_grouped_dir=str(grouped_turn_waste_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=True,
            )

            self.assertTrue((output_root / "search_first_hit_condition.json").exists())
            self.assertTrue((output_root / "search_first_hit_condition.csv").exists())
            self.assertTrue((output_root / "search_first_hit_tool.json").exists())
            self.assertTrue((output_root / "search_first_hit_tool.csv").exists())
            self.assertTrue((output_root / "search_topk_miss_tool.json").exists())
            self.assertTrue((output_root / "search_topk_miss_tool.csv").exists())
            self.assertTrue((output_root / "search_tool_efficiency.json").exists())
            self.assertTrue((output_root / "search_tool_efficiency.csv").exists())
            self.assertTrue((output_root / "per_task_search_bottleneck.csv").exists())
            self.assertTrue((output_root / "per_task_search_tool_bottleneck.csv").exists())

            summary = outputs["summary"]
            self.assertEqual(len(summary), 3)

            row = next(item for item in summary if item["condition_model"] == f"openai_gpt-5.2-xhigh/{variant_a}")
            self.assertEqual(row["n"], 2)
            self.assertEqual(row["semantic_match"], 0.5)
            self.assertEqual(row["semantic_correct"], 1)
            self.assertEqual(row["answer_unknown_blank"], 1)
            self.assertEqual(row["no_error"], 1)
            self.assertEqual(row["error_tokens_reached"], 1)
            self.assertEqual(row["D_ret"], 0.5)
            self.assertEqual(row["D_acc"], 0.5)
            self.assertEqual(row["avg_runtime_seconds"], 15.0)
            self.assertEqual(row["avg_total_tokens"], 175.0)
            self.assertEqual(row["avg_cost_usd"], 0.15)
            self.assertEqual(row["total_cost_usd"], 0.3)
            self.assertEqual(row["avg_ideal_subagent_cost_usd"], 0.02)
            self.assertEqual(row["total_ideal_subagent_cost_usd"], 0.04)
            self.assertEqual(row["avg_total_cost_with_ideal_subagents_usd"], 0.17)
            self.assertEqual(row["total_cost_with_ideal_subagents_usd"], 0.34)
            self.assertEqual(row["avg_query_file_calls"], 1.5)
            self.assertEqual(row["query_file_error_rate"], 0.3333)
            self.assertEqual(row["n_tasks_with_search"], 2)
            self.assertEqual(row["n_tasks_without_search"], 0)
            self.assertEqual(row["found_tasks_top_1"], 1)
            self.assertEqual(row["found_tasks_top1"], 1)
            self.assertEqual(row["not_found_tasks_top_1"], 1)
            self.assertEqual(row["not_found_tasks_top1"], 1)
            self.assertEqual(row["top1_not_found_rate"], 0.5)
            self.assertEqual(row["avg_first_hit_round_top_1"], 1.0)
            self.assertEqual(row["avg_first_hit_round_top1"], 1.0)
            self.assertEqual(row["avg_wasted_rounds_top_5"], 0.5)
            self.assertEqual(row["avg_wasted_rounds_top5"], 0.5)
            self.assertEqual(
                row["semantic_correct"] + row["semantic_incorrect"] + row["answer_unknown_blank"],
                row["n"],
            )

            variant_summary = outputs["variant_summary"]
            variant_row = next(item for item in variant_summary if item["variant"] == variant_a)
            self.assertEqual(variant_row["n_total"], 3)
            self.assertEqual(variant_row["semantic_correct"], 1)
            self.assertEqual(variant_row["semantic_incorrect"], 1)
            self.assertEqual(variant_row["answer_unknown_blank"], 1)
            self.assertEqual(variant_row["avg_ideal_subagent_cost_usd"], 0.0133)
            self.assertEqual(variant_row["total_ideal_subagent_cost_usd"], 0.04)
            self.assertEqual(variant_row["avg_total_cost_with_ideal_subagents_usd"], 0.2133)
            self.assertEqual(variant_row["total_cost_with_ideal_subagents_usd"], 0.64)
            self.assertEqual(variant_row["error_turns_exhausted"], 1)
            self.assertEqual(variant_row["error_tokens_reached"], 1)
            self.assertNotIn("search_avg_recall", variant_row)
            self.assertEqual(variant_row["n_tasks_with_search"], 3)
            self.assertEqual(variant_row["n_tasks_without_search"], 0)
            self.assertEqual(variant_row["found_tasks_top_1"], 2)
            self.assertEqual(variant_row["not_found_tasks_top_1"], 1)
            self.assertEqual(variant_row["top1_not_found_rate"], 0.3333)
            self.assertEqual(variant_row["avg_first_hit_round_top_1"], 1.0)
            self.assertEqual(variant_row["avg_wasted_rounds_top_5"], 0.3333)
            self.assertEqual(
                variant_row["semantic_correct"] + variant_row["semantic_incorrect"] + variant_row["answer_unknown_blank"],
                variant_row["n_total"],
            )

            turn_waste_groups = outputs["turn_waste_global_groups"]
            self.assertEqual(turn_waste_groups[variant_a]["n_total_rows"], 3)
            self.assertEqual(turn_waste_groups[variant_a]["n_failed_rows"], 2)
            self.assertEqual(turn_waste_groups[variant_a]["groups"]["query_reformulation_loop"]["n"], 1)
            self.assertEqual(turn_waste_groups[variant_a]["groups"]["schema_file_inspection_loop"]["n"], 1)
            self.assertEqual(turn_waste_groups[variant_b]["n_failed_rows"], 0)

            self.assertIn("search_bottleneck", outputs)
            search_bottleneck = outputs["search_bottleneck"]
            condition_rows = search_bottleneck["condition_summary_rows"]
            top1_condition = next(
                row for row in condition_rows if row["condition"] == variant_a and row["cutoff"] == 1
            )
            self.assertEqual(top1_condition["n_tasks_with_search"], 3)
            self.assertEqual(top1_condition["n_tasks_without_search"], 0)
            self.assertEqual(top1_condition["found_tasks"], 2)
            self.assertEqual(top1_condition["not_found_tasks"], 1)
            self.assertEqual(top1_condition["not_found_rate"], 0.3333)
            self.assertEqual(top1_condition["avg_first_hit_round_found_only"], 1)
            self.assertEqual(top1_condition["avg_wasted_rounds"], 0.3333)

            tool_rows = search_bottleneck["tool_first_hit_rows"]
            ideal_top1 = next(
                row for row in tool_rows if row["search_tool"] == "search_ideal" and row["cutoff"] == 1
            )
            self.assertEqual(ideal_top1["tasks_with_tool"], 3)
            self.assertEqual(ideal_top1["found_tasks"], 2)
            self.assertEqual(ideal_top1["not_found_tasks"], 1)
            self.assertEqual(ideal_top1["not_found_rate"], 0.3333)
            self.assertEqual(ideal_top1["avg_first_hit_round_found_only"], 1)

            miss_rows = search_bottleneck["tool_miss_rows"]
            ideal_top1_miss = next(
                row for row in miss_rows if row["search_tool"] == "search_ideal" and row["cutoff"] == 1
            )
            self.assertEqual(ideal_top1_miss["n_calls"], 3)
            self.assertEqual(ideal_top1_miss["hit_calls"], 2)
            self.assertEqual(ideal_top1_miss["miss_calls"], 1)
            self.assertEqual(ideal_top1_miss["miss_rate"], 0.3333)

            per_task_search_rows = search_bottleneck["per_task_rows"]
            task_2_search = next(row for row in per_task_search_rows if row["task_id"] == "k-1-d-1/task_2")
            self.assertEqual(task_2_search["found_top_1"], 0)
            self.assertEqual(task_2_search["wasted_rounds_top_5"], 1)

            per_task_tool_rows = search_bottleneck["per_task_tool_rows"]
            task_1_tool = next(
                row
                for row in per_task_tool_rows
                if row["task_id"] == "k-1-d-1/task_1" and row["search_tool"] == "search_ideal"
            )
            self.assertEqual(task_1_tool["first_hit_round_top_1"], 1)

            self.assertIn("failure", outputs)
            runtime_row = outputs["runtime"][f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertEqual(runtime_row["total_cost_with_ideal_subagents_usd"], 0.34)
            failure_row = outputs["failure"][f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertEqual(failure_row["primary"]["semantic_correct"]["n"], 1)
            self.assertEqual(failure_row["primary"]["error_tokens_reached"]["n"], 1)
            self.assertEqual(failure_row["log_error_buckets"]["error_tokens_reached"]["n"], 1)

            tools_discovery = outputs["tools_discovery"][f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertIn("search_ideal", tools_discovery)
            self.assertNotIn("avg_recall", tools_discovery["search_ideal"])
            folder_stats = next(iter(tools_discovery["search_ideal"]["per_folder"].values()))
            self.assertNotIn("avg_recall", folder_stats)
            task_stats = next(iter(folder_stats["per_task"].values()))
            self.assertNotIn("recall", task_stats)

            self.assertIn("tool_errors", outputs)
            tool_errors = outputs["tool_errors"][f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertEqual(tool_errors["query_file"]["total_calls"], 3)
            self.assertEqual(tool_errors["query_file"]["total_errors"], 1)
            self.assertEqual(tool_errors["query_file"]["error_rate"], 0.3333)

            search_depth = outputs["search_depth"]
            self.assertEqual(search_depth[variant_a]["1"]["n"], 3)
            self.assertEqual(search_depth[variant_a]["1"]["mean_semantic_match"], 0.3333)

            reasoning_density = outputs["reasoning_density"]
            self.assertEqual(reasoning_density[variant_a]["<=2"]["n"], 3)
            self.assertEqual(reasoning_density[variant_a]["<=2"]["mean_semantic_match"], 0.3333)

            crosstab = outputs["semantic_error_crosstab"]
            variant_cross = next(
                item
                for item in crosstab
                if item["level"] == "variant"
                and item["variant"] == variant_a
                and item["semantic_bucket"] == "semantic_correct"
                and item["log_error_bucket"] == "no_error"
            )
            self.assertEqual(variant_cross["n"], 1)

            per_task_path = output_root / "per_task_semantic.csv"
            self.assertTrue(per_task_path.exists())
            with per_task_path.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 4)
            joined_row = next(row for row in rows if row["task_id"] == "tasks_mini/k-1-d-1/task_2.json")
            self.assertEqual(joined_row["log_error_bucket_display"], "error_tokens_reached")
            self.assertEqual(joined_row["D_ret"], "0.0")
            self.assertEqual(joined_row["D_acc"], "0.0")
            self.assertNotIn("search_recall", joined_row)

            per_task_retrieval_path = output_root / "per_task_retrieval.csv"
            self.assertTrue(per_task_retrieval_path.exists())
            with per_task_retrieval_path.open(newline="") as handle:
                retrieval_rows = list(csv.DictReader(handle))
            self.assertEqual(len(retrieval_rows), 4)
            retrieval_row = next(
                row for row in retrieval_rows if row["condition_model"] == f"openai_gpt-5.2-xhigh/{variant_a}" and row["task_id"] == "k-1-d-1/task_2"
            )
            self.assertEqual(retrieval_row["retrieval_recall"], "0.0")
            self.assertEqual(retrieval_row["retrieval_precision"], "0.0")

            expected_jsons = {
                "semantic_match.json",
                "discovery.json",
                "runtime.json",
                "efficiency.json",
                "failure.json",
                "tools_discovery.json",
                "tool_errors.json",
                "semantic_buckets.json",
                "log_error_buckets.json",
                "semantic_error_crosstab.json",
                "turn_waste_global_groups.json",
                "search_depth.json",
                "reasoning_density.json",
                "summary.json",
                "variant_summary.json",
            }
            for filename in expected_jsons:
                self.assertTrue((output_root / filename).exists(), filename)
            self.assertTrue((output_root / "turn_waste_global_groups.csv").exists())
            self.assertTrue((output_root / "turn_waste_grouped_failures_joined.csv").exists())

    def test_run_analysis_requires_grouped_turn_waste_root(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            base_results_root = root / "results-ec2" / "modes"
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_semantic"
            variant = "search_i_results_i_plani_k5"

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                    }
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.10,
                        "time": 10,
                        "tool_calls_total": 4,
                        "tool_counts": [],
                    }
                ],
            )
            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [{"tool": "submit_answer"}],
            )

            with self.assertRaises(FileNotFoundError):
                run_analysis(
                    results_dir=str(results_root),
                    base_results_dir=str(base_results_root),
                    turn_waste_grouped_dir=str(root / "missing_grouped" / "modes"),
                    traces_dir=str(traces_root),
                    tasks_dir=str(tasks_root),
                    output_dir=str(output_root),
                    no_figures=True,
                )

    def test_run_analysis_skips_turn_waste_when_grouped_dir_none(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            base_results_root = root / "results-ec2" / "modes"
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_semantic"
            variant = "search_i_results_i_plani_k5"

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                    }
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.10,
                        "time": 10,
                        "tool_calls_total": 4,
                        "tool_counts": [],
                    }
                ],
            )
            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [{"tool": "submit_answer"}],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                base_results_dir=str(base_results_root),
                turn_waste_grouped_dir=None,
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=True,
            )

            self.assertTrue((output_root / "semantic_match.json").exists())
            self.assertFalse((output_root / "turn_waste_global_groups.json").exists())
            self.assertFalse((output_root / "turn_waste_global_groups.csv").exists())
            self.assertFalse((output_root / "turn_waste_grouped_failures_joined.csv").exists())
            self.assertEqual(outputs["turn_waste_global_groups"], {})
            self.assertEqual(outputs["turn_waste_global_group_rows"], [])
            self.assertEqual(outputs["turn_waste_joined_failed_rows"], [])

    def test_run_analysis_allows_blank_grouped_turn_waste_label_on_failed_row(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            grouped_turn_waste_root = root / "results-ec2_semantic_turn_waste_grouped" / "modes"
            base_results_root = root / "results-ec2" / "modes"
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_semantic"
            variant = "search_i_results_i_plani_k5"

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "unknown",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "blank answer",
                        "semantic_bucket": "answer_unknown_blank",
                        "log_error_bucket": "error_event_loop",
                        "log_error_evidence": "EventLoopException",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "EventLoopException",
                    }
                ],
            )
            self._write_grouped_turn_waste_results(
                grouped_turn_waste_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "unknown",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "blank answer",
                        "semantic_bucket": "answer_unknown_blank",
                        "log_error_bucket": "error_event_loop",
                        "log_error_evidence": "EventLoopException",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "EventLoopException",
                        "turn_waste_summary": "",
                        "turn_repeated_behavior": "",
                        "turn_progress_stop_point": "",
                        "productive_turn_ranges": "",
                        "wasted_turn_ranges": "",
                        "estimated_wasted_turns": "",
                        "turn_budget_failure_reason": "",
                        "turn_waste_evidence": "",
                        "turn_waste_local_group": "",
                        "turn_waste_local_group_reason": "",
                        "turn_waste_global_group": "",
                        "turn_waste_global_group_reason": "",
                    }
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.10,
                        "time": 10,
                        "tool_calls_total": 4,
                        "tool_counts": [],
                    }
                ],
            )
            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [{"tool": "submit_answer"}],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                base_results_dir=str(base_results_root),
                turn_waste_grouped_dir=str(grouped_turn_waste_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=True,
            )

            variant_groups = outputs["turn_waste_global_groups"][variant]
            self.assertEqual(variant_groups["n_failed_rows"], 1)
            self.assertEqual(variant_groups["n_grouped_failed_rows"], 0)
            self.assertEqual(variant_groups["n_unassigned_failed_rows"], 1)
            self.assertEqual(variant_groups["groups"], {})
            joined_rows = outputs["turn_waste_joined_failed_rows"]
            self.assertEqual(len(joined_rows), 1)
            self.assertEqual(joined_rows[0]["turn_waste_global_group"], "")

    def test_run_analysis_generates_expected_figures_and_cleans_stale_pdfs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            grouped_turn_waste_root = root / "results-ec2_semantic_turn_waste_grouped" / "modes"
            base_results_root = root / "results-ec2" / "modes"
            traces_root = root / "results-ec2" / "traces" / "modes"
            tasks_root = root / "tasks_mini"
            output_root = root / "analysis_results_mode_semantic"
            variant = "search_i_results_i_plani_k5"

            self._write_eval_results(
                results_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                    }
                ],
            )
            self._write_grouped_turn_waste_results(
                grouped_turn_waste_root / "openai_gpt-5.2-xhigh" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "expected_answer": "2020",
                        "predicted_answer": "[2020]",
                        "exact_match": "1.0",
                        "semantic_match": "1",
                        "semantic_reason": "same answer",
                        "semantic_bucket": "semantic_correct",
                        "log_error_bucket": "",
                        "log_error_evidence": "",
                        "runtime_seconds": "10",
                        "input_tokens": "100",
                        "output_tokens": "20",
                        "total_tokens": "120",
                        "cost_usd": "0.10",
                        "tool_calls_total": "4",
                        "api_tool_calls": "2",
                        "error": "",
                        "turn_waste_summary": "",
                        "turn_repeated_behavior": "",
                        "turn_progress_stop_point": "",
                        "productive_turn_ranges": "",
                        "wasted_turn_ranges": "",
                        "estimated_wasted_turns": "",
                        "turn_budget_failure_reason": "",
                        "turn_waste_evidence": "",
                        "turn_waste_local_group": "",
                        "turn_waste_local_group_reason": "",
                        "turn_waste_global_group": "",
                        "turn_waste_global_group_reason": "",
                    }
                ],
            )
            self._write_agent_results(
                base_results_root / "openai_gpt-5.2-xhigh" / variant / "agent_results.jsonl",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "cost_usd": 0.10,
                        "time": 10,
                        "tool_calls_total": 4,
                        "tool_counts": [
                            {"name": "search_ideal", "call_count": 1, "success_count": 1},
                            {"name": "query_file", "call_count": 1, "success_count": 1},
                            {"name": "submit_answer", "call_count": 1, "success_count": 1},
                        ],
                    }
                ],
            )
            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search_ideal", "result_dataset_ids": ["ds1"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )

            stale_fig_dir = output_root / "figures"
            stale_fig_dir.mkdir(parents=True, exist_ok=True)
            (stale_fig_dir / "obsolete.pdf").write_text("stale")

            run_analysis(
                results_dir=str(results_root),
                base_results_dir=str(base_results_root),
                turn_waste_grouped_dir=str(grouped_turn_waste_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=False,
            )

            expected_figs = {
                "fig01_semantic_buckets_variant.pdf",
                "fig02_log_error_buckets_variant.pdf",
                "fig03_semantic_x_error_variant.pdf",
                "fig04_error_vs_semantic_variant.pdf",
                "fig05_turn_waste_groups_variant.pdf",
                "fig1_semantic_comparison.pdf",
                "fig2a_recall_semantic_combined.pdf",
                "fig2_discovery_metrics.pdf",
                "fig2b_gpt_5_2_xhigh_discovery_metrics.pdf",
                "fig3_failure_breakdown.pdf",
                "fig6_cost_vs_semantic.pdf",
                "fig8_search_tool_precision.pdf",
                "fig9_search_calls.pdf",
                "fig10_search_depth_curve.pdf",
                "fig10b_gpt_5_2_xhigh_search_depth.pdf",
                "fig12_reasoning_density.pdf",
                "fig12b_gpt_5_2_xhigh_reasoning_density.pdf",
                "fig13_tool_error_rates.pdf",
                "fig14_tool_call_counts.pdf",
                "fig15_search_cumulative_retrieval_recall_condition.pdf",
                "fig16_search_cumulative_access_recall_condition.pdf",
                "fig17_search_topk_miss_by_tool.pdf",
                "fig18_search_tool_coverage_waste.pdf",
                "fig19_search_topk_miss_by_condition.pdf",
                "fig20_search_condition_coverage_waste.pdf",
            }
            produced = {path.name for path in stale_fig_dir.glob("*.pdf")}
            self.assertFalse((stale_fig_dir / "obsolete.pdf").exists())
            self.assertEqual(produced, expected_figs)


if __name__ == "__main__":
    unittest.main()
