import csv
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.turn_waste_analysis import run_analysis


class TestTurnWasteAnalysis(unittest.TestCase):
    def _write_eval_results(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "task_id",
            "model",
            "log_error_bucket",
            "runtime_seconds",
            "cycle_count",
            "tool_calls_total",
            "api_tool_calls",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "sources_used_count",
            "required_dataset_count",
        ]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_log(self, path: Path, lines: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n")

    def test_run_analysis_writes_csv_and_markdown(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_root = root / "results-ec2_semantic" / "modes"
            logs_root = root / "logs-ec2" / "modes"
            output_root = root / "analysis_results_mode_semantic"

            model_dir = "openai_gpt-5.2-xhigh"
            inspection_variant = "search_i_results_i_plani_k5"
            search_variant = "search_n_results_i_plani_k5"

            self._write_eval_results(
                results_root / model_dir / inspection_variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "model": "gpt-5.2",
                        "log_error_bucket": "error_tokens_reached",
                        "runtime_seconds": "120",
                        "cycle_count": "12",
                        "tool_calls_total": "15",
                        "api_tool_calls": "10",
                        "input_tokens": "1000",
                        "output_tokens": "100",
                        "total_tokens": "1100",
                        "sources_used_count": "1",
                        "required_dataset_count": "2",
                    }
                ],
            )
            self._write_eval_results(
                results_root / model_dir / search_variant / "eval_results.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "model": "gpt-5.2",
                        "log_error_bucket": "error_tools_limit",
                        "runtime_seconds": "180",
                        "cycle_count": "18",
                        "tool_calls_total": "20",
                        "api_tool_calls": "12",
                        "input_tokens": "1500",
                        "output_tokens": "120",
                        "total_tokens": "1620",
                        "sources_used_count": "2",
                        "required_dataset_count": "2",
                    }
                ],
            )

            self._write_log(
                logs_root / model_dir / inspection_variant / "tasks_mini" / "k-1-d-1" / "task_1.log",
                [
                    "--- Turn 1 (elapsed: 0.0s) ---",
                    'Executing: skills({"skill_name": "plan-ideal"})',
                    "--- Turn 2 (elapsed: 1.0s) ---",
                    'Executing: plan_ideal({"plan_text": "x"})',
                    "--- Turn 3 (elapsed: 2.0s) ---",
                    'Executing: skills({"skill_name": "discover-data"})',
                    "--- Turn 4 (elapsed: 3.0s) ---",
                    'Executing: list_files({"dataset_ids": ["ds1"], "limit": 50})',
                    "--- Turn 5 (elapsed: 4.0s) ---",
                    'Executing: peek_file({"dataset_id": "ds1", "file_path": "files/rows.txt", "max_rows": 5})',
                    "--- Turn 6 (elapsed: 5.0s) ---",
                    'Executing: peek_file({"dataset_id": "ds1", "file_path": "files/rows.txt", "max_rows": 5})',
                    "--- Turn 7 (elapsed: 6.0s) ---",
                    'Executing: read_file({"dataset_id": "ds1", "file_path": "files/rows.txt", "start_line": 0, "max_lines": 50})',
                    "--- Turn 8 (elapsed: 7.0s) ---",
                    'Executing: grep_file({"dataset_id": "ds1", "file_path": "files/rows.txt", "regex_pattern": "Ward", "context_lines": 2})',
                ],
            )
            self._write_log(
                logs_root / model_dir / search_variant / "tasks_mini" / "k-1-d-1" / "task_2.log",
                [
                    "--- Turn 1 (elapsed: 0.0s) ---",
                    'Executing: skills({"skill_name": "plan-ideal"})',
                    "--- Turn 2 (elapsed: 1.0s) ---",
                    'Executing: plan_ideal({"plan_text": "x"})',
                    "--- Turn 3 (elapsed: 2.0s) ---",
                    'Executing: skills({"skill_name": "discover-data"})',
                    "--- Turn 4 (elapsed: 3.0s) ---",
                    'Executing: search_value({"query": "dc permits"})',
                    "--- Turn 5 (elapsed: 4.0s) ---",
                    'Executing: search_value({"query": "dc permits"})',
                    "--- Turn 6 (elapsed: 5.0s) ---",
                    'Executing: search_value({"query": "dc crime"})',
                    "--- Turn 7 (elapsed: 6.0s) ---",
                    'Executing: search_schema({"query": "ward offense"})',
                    "--- Turn 8 (elapsed: 7.0s) ---",
                    'Executing: search_schema({"query": "ward offense"})',
                    'Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning. Do not call any other tool before submit_answer. You MUST follow this guidance immediately.',
                    "--- Turn 9 (elapsed: 8.0s) ---",
                    'Executing: submit_answer({"answer": "[Ward 1]", "reasoning": "best effort"})',
                ],
            )

            outputs = run_analysis(
                results_dir=str(results_root),
                logs_dir=str(logs_root),
                output_dir=str(output_root),
            )

            self.assertEqual(len(outputs["rows"]), 2)
            categories = {row["task_id"]: row["primary_waste_category"] for row in outputs["rows"]}
            self.assertEqual(categories["tasks_mini/k-1-d-1/task_1.json"], "schema_file_inspection_loop")
            self.assertEqual(categories["tasks_mini/k-1-d-1/task_2.json"], "search_thrash")

            self.assertTrue(outputs["csv_path"].exists())
            self.assertTrue(outputs["markdown_path"].exists())
            report_text = outputs["markdown_path"].read_text()
            self.assertIn("schema_file_inspection_loop", report_text)
            self.assertIn("search_thrash", report_text)


if __name__ == "__main__":
    unittest.main()
