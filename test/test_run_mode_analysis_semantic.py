import csv
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.run_mode_analysis_semantic import run_analysis


class TestRunModeAnalysisSemantic(unittest.TestCase):
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
            "tool_calls_total",
            "api_tool_calls",
            "error",
        ]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_trace(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for record in records:
                handle.write(json.dumps(record))
                handle.write("\n")

    def _write_task(self, path: Path, datasets_used: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"datasets_used": datasets_used}))

    def test_run_analysis_writes_semantic_outputs_and_rollups(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
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
                        "tool_calls_total": "6",
                        "api_tool_calls": "3",
                        "error": "MaxTokensReachedException",
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

            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_task(tasks_root / "k-1-d-1" / "task_2.json", ["ds2"])

            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_a / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search", "result_dataset_ids": ["ds1", "other"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_a / "k-1-d-1" / "task_2.jsonl",
                [
                    {"tool": "search", "result_dataset_ids": ["other"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.4-mini" / variant_a / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search", "result_dataset_ids": ["ds1"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant_b / "k-1-d-1" / "task_1.jsonl",
                [
                    {"tool": "search", "result_dataset_ids": ["ds1"]},
                    {"tool": "query_file", "read_dataset_ids": ["ds1"]},
                    {"tool": "submit_answer"},
                ],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                no_figures=True,
            )

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

            variant_summary = outputs["variant_summary"]
            variant_row = next(item for item in variant_summary if item["variant"] == variant_a)
            self.assertEqual(variant_row["n_total"], 3)
            self.assertEqual(variant_row["semantic_correct"], 1)
            self.assertEqual(variant_row["semantic_incorrect"], 1)
            self.assertEqual(variant_row["answer_unknown_blank"], 1)
            self.assertEqual(variant_row["error_turns_exhausted"], 1)
            self.assertEqual(variant_row["error_tokens_reached"], 1)

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

            search_depth = outputs["search_depth_buckets"]
            depth_row = search_depth[f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertEqual(depth_row["bins"]["1"]["n"], 2)
            self.assertEqual(depth_row["bins"]["1"]["semantic_correct"], 1)
            self.assertEqual(depth_row["bins"]["1"]["answer_unknown_blank"], 1)

            reasoning_density = outputs["reasoning_density_buckets"]
            density_row = reasoning_density[f"openai_gpt-5.2-xhigh/{variant_a}"]
            self.assertEqual(density_row["bins"]["<=2"]["n"], 2)
            self.assertEqual(density_row["bins"]["<=2"]["error_tokens_reached"], 1)

            per_task_path = output_root / "per_task_semantic.csv"
            self.assertTrue(per_task_path.exists())
            with per_task_path.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 4)
            joined_row = next(row for row in rows if row["task_id"] == "tasks_mini/k-1-d-1/task_2.json")
            self.assertEqual(joined_row["log_error_bucket_display"], "error_tokens_reached")
            self.assertEqual(joined_row["D_ret"], "0.0")
            self.assertEqual(joined_row["D_acc"], "0.0")

            self.assertTrue((output_root / "summary.json").exists())
            self.assertTrue((output_root / "variant_summary.json").exists())
            self.assertTrue((output_root / "semantic_error_crosstab.json").exists())
            self.assertTrue((output_root / "search_depth_buckets.json").exists())
            self.assertTrue((output_root / "reasoning_density_buckets.json").exists())

    def test_model_filter_limits_outputs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
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
            self._write_eval_results(
                results_root / "anthropic_claude-3.5-sonnet" / variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "claude-3.5-sonnet",
                        "expected_answer": "2020",
                        "predicted_answer": "unknown",
                        "exact_match": "0.0",
                        "semantic_match": "0",
                        "semantic_reason": "blank answer",
                        "semantic_bucket": "answer_unknown_blank",
                        "log_error_bucket": "error_unknown",
                        "log_error_evidence": "missing answer",
                        "runtime_seconds": "12",
                        "input_tokens": "110",
                        "output_tokens": "21",
                        "total_tokens": "131",
                        "cost_usd": "0.11",
                        "tool_calls_total": "5",
                        "api_tool_calls": "2",
                        "error": "unknown",
                    }
                ],
            )
            self._write_task(tasks_root / "k-1-d-1" / "task_1.json", ["ds1"])
            self._write_trace(
                traces_root / "openai_gpt-5.2-xhigh" / variant / "k-1-d-1" / "task_1.jsonl",
                [{"tool": "search", "result_dataset_ids": ["ds1"]}],
            )
            self._write_trace(
                traces_root / "anthropic_claude-3.5-sonnet" / variant / "k-1-d-1" / "task_1.jsonl",
                [{"tool": "search", "result_dataset_ids": ["ds1"]}],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                traces_dir=str(traces_root),
                tasks_dir=str(tasks_root),
                output_dir=str(output_root),
                model_filter="gpt-5.2",
                no_figures=True,
            )

            self.assertEqual(len(outputs["summary"]), 1)
            self.assertEqual(outputs["summary"][0]["model"], "openai_gpt-5.2-xhigh")


if __name__ == "__main__":
    unittest.main()
