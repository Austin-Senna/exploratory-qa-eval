import csv
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.build_turn_waste_global_report import build_turn_waste_global_report


class TestBuildTurnWasteGlobalReport(unittest.TestCase):
    def _write_csv(self, path: Path, fieldnames: list[str], rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_log(self, path: Path, lines: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n")

    def test_report_uses_evidence_and_optional_log_snippets_only(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            grouped_root = root / "results-ec2_semantic_turn_waste_grouped"
            logs_root = root / "logs-ec2" / "modes"
            task_path = root / "tasks_mini" / "k-4-d-4" / "task_8.json"
            plan_path = root / "plans_mini" / "k-4-d-4" / "task_8.json"

            task_path.parent.mkdir(parents=True, exist_ok=True)
            plan_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text('{"question": "dummy"}\n')
            plan_path.write_text('{"dataset_sequence": []}\n')

            model_dir = "openai_gpt-5.2-xhigh"
            variant = "search_i_results_i_plani_k5"
            file_dir = grouped_root / "modes" / model_dir / variant

            self._write_csv(
                file_dir / "eval_results.csv",
                ["task_id"],
                [{"task_id": "tasks_mini/k-4-d-4/task_8.json"}],
            )
            self._write_csv(
                file_dir / "turn_waste_global_failures.csv",
                [
                    "task_id",
                    "log_error_bucket",
                    "estimated_wasted_turns",
                    "turn_waste_global_group",
                    "turn_waste_global_subtype",
                    "turn_waste_summary",
                    "turn_repeated_behavior",
                    "turn_progress_stop_point",
                    "wasted_turn_ranges",
                    "productive_turn_ranges",
                    "turn_budget_failure_reason",
                    "turn_waste_evidence",
                    "turn_waste_global_group_reason",
                    "turn_waste_global_subtype_reason",
                    "turn_waste_local_group",
                    "turn_waste_local_group_reason",
                ],
                [
                    {
                        "task_id": "tasks_mini/k-4-d-4/task_8.json",
                        "log_error_bucket": "error_tools_limit",
                        "estimated_wasted_turns": "6",
                        "turn_waste_global_group": "Answer-Ready Overshoot",
                        "turn_waste_global_subtype": "late verification tail",
                        "turn_waste_summary": "Worked through Missouri expenditures and Route 66 city comparison, then wrapped up with the Chicago-vs-Santa Monica reasoning.",
                        "turn_repeated_behavior": "Kept revisiting the city-health and terminus-city comparison rather than moving directly to the last submission step.",
                        "turn_progress_stop_point": "Turn 25 computes 2007 agency totals; turns 26-31 are duplicate count checks and the final tool-limit warning.",
                        "wasted_turn_ranges": "26-31",
                        "productive_turn_ranges": "1-25",
                        "turn_budget_failure_reason": "It had the ranking path, but instead of closing out it kept rechecking agency counts on the same datasets until the tool cap stopped it.",
                        "turn_waste_evidence": "Turn 26 starts repeated count-distinct checks; Turn 31 triggers the 30/30 tool-limit warning.",
                        "turn_waste_global_group_reason": "The answer path was essentially complete.",
                        "turn_waste_global_subtype_reason": "The main spending answer was basically done.",
                        "turn_waste_local_group": "Duplicate query loops",
                        "turn_waste_local_group_reason": "It repeated identical count-distinct checks.",
                    }
                ],
            )

            self._write_log(
                logs_root / model_dir / variant / "tasks_mini" / "k-4-d-4" / "task_8.log",
                [
                    "--- Turn 26 (elapsed: 177.8s) ---",
                    'Executing: query_file({"dataset_id": "2008-state-expenditures", "file_path": "files/rows.txt", "sql": "SELECT COUNT(DISTINCT \\"Agency Name\\") AS n_agencies FROM t;"})',
                    "--- Turn 31 (elapsed: 212.3s) ---",
                    'Tool result: Tool call cancelled. Tool limit reached (30/30 calls used). You must stop using other tools and immediately call submit_answer with your best current answer and reasoning.',
                ],
            )

            outputs = build_turn_waste_global_report(
                source_root=grouped_root,
                logs_dir=logs_root,
                representative_limit=3,
            )

            report_text = outputs["report_path"].read_text()
            self.assertIn("Answer-Ready Overshoot", report_text)
            self.assertIn("late verification tail (1)", report_text)
            self.assertIn("The answer path is already mostly established", report_text)
            self.assertIn("late verification after the decisive clue is already visible", report_text)
            self.assertIn("[task](../tasks_mini/k-4-d-4/task_8.json)", report_text)
            self.assertIn("[plan](../plans_mini/k-4-d-4/task_8.json)", report_text)
            self.assertIn("[log](../logs-ec2/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/tasks_mini/k-4-d-4/task_8.log)", report_text)
            self.assertIn("Turn 26 starts repeated count-distinct checks", report_text)
            self.assertIn('Turn 26: Executing: query_file({"dataset_id": "2008-state-expenditures"', report_text)
            self.assertIn("Turn 31: Tool result: Tool call cancelled. Tool limit reached (30/30 calls used).", report_text)

            # Unsupported row-summary prose should not be copied into the global report.
            self.assertNotIn("Route 66 city comparison", report_text)
            self.assertNotIn("Chicago-vs-Santa Monica reasoning", report_text)

    def test_report_suppresses_rows_that_fail_model_validation(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            grouped_root = root / "results-ec2_semantic_turn_waste_grouped"
            task_path = root / "tasks_mini" / "k-1-d-1" / "task_1.json"
            plan_path = root / "plans_mini" / "k-1-d-1" / "task_1.json"

            task_path.parent.mkdir(parents=True, exist_ok=True)
            plan_path.parent.mkdir(parents=True, exist_ok=True)
            task_path.write_text('{"question": "dummy"}\n')
            plan_path.write_text('{"dataset_sequence": []}\n')

            model_dir = "openai_gpt-5.2-xhigh"
            variant = "search_i_results_i_plani_k5"
            file_dir = grouped_root / "modes" / model_dir / variant

            self._write_csv(
                file_dir / "eval_results.csv",
                ["task_id"],
                [{"task_id": "tasks_mini/k-1-d-1/task_1.json"}],
            )
            self._write_csv(
                file_dir / "turn_waste_global_failures.csv",
                [
                    "task_id",
                    "log_error_bucket",
                    "estimated_wasted_turns",
                    "turn_waste_global_group",
                    "turn_waste_global_subtype",
                    "turn_waste_evidence",
                    "turn_waste_model_validation_status",
                    "turn_waste_model_validation_notes",
                ],
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "log_error_bucket": "error_tokens_reached",
                        "estimated_wasted_turns": "4",
                        "turn_waste_global_group": "mixed or unclear",
                        "turn_waste_global_subtype": "",
                        "turn_waste_evidence": "Turn 9 | Executing: search_ideal({\"query\": \"ACT Iowa City\"})",
                        "turn_waste_model_validation_status": "invalid_untrusted",
                        "turn_waste_model_validation_notes": "Narrative mentioned ACT Iowa City but the task/log belonged to a Texas prison-release run.",
                    }
                ],
            )

            outputs = build_turn_waste_global_report(
                source_root=grouped_root,
                representative_limit=3,
            )

            report_text = outputs["report_path"].read_text()
            self.assertIn("Evidence: omitted due to failed model validation", report_text)
            self.assertNotIn('Turn 9 | Executing: search_ideal({"query": "ACT Iowa City"})', report_text)


if __name__ == "__main__":
    unittest.main()
