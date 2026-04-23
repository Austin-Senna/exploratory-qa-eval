import csv
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.build_turn_waste_global_report import build_turn_waste_global_report
from analysis.turn_waste_validation import (
    VALIDATION_MAX_TURN_FIELD,
    VALIDATION_NOTES_FIELD,
    VALIDATION_STATUS_FIELD,
    validate_audit_row,
    validate_turn_waste_root,
)


class TestTurnWasteValidation(unittest.TestCase):
    def _write_csv(self, path: Path, fieldnames: list[str], rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _write_log(self, path: Path, lines: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n")

    def test_validate_audit_row_rejects_impossible_turns(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            log_path = root / "task.log"
            self._write_log(
                log_path,
                [
                    "--- Turn 1 (elapsed: 0.0s) ---",
                    'Executing: search_ideal({"query": "texas releases"})',
                    "--- Turn 16 (elapsed: 231.4s) ---",
                    "MaxTokensReachedException: Agent has reached an unrecoverable state due to max_tokens limit.",
                ],
            )

            row = {
                "turn_waste_summary": "Found ACT and school-district-office sources.",
                "turn_progress_stop_point": "After ACT and the school-district-office source were found.",
                "productive_turn_ranges": "1-16",
                "wasted_turn_ranges": "17-33",
                "estimated_wasted_turns": "17",
                "turn_waste_evidence": "Turns 17-20 repeat discover-data and search_ideal around the same public-school source family; Turns 24-33 keep reopening files.",
            }
            result = validate_audit_row(row, log_path)

            self.assertEqual(result["status"], "invalid")
            self.assertEqual(result["log_max_turn"], 16)
            self.assertIn("wasted_turn_ranges exceeds log max turn 16", result["notes"])
            self.assertIn("turn_waste_evidence references turns beyond log max turn 16", result["notes"])

    def test_validate_root_rewrites_status_columns_and_report_builder_suppresses_invalid_evidence(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_root = root / "results-ec2_semantic_turn_waste"
            grouped_root = root / "results-ec2_semantic_turn_waste_grouped"
            logs_root = root / "logs-ec2" / "modes"
            model_dir = "openai_gpt-5.2-xhigh"
            variant = "search_i_results_i_plani_k5"
            task_id = "tasks_mini/k-6-d-4/task_1.json"

            eval_rows = [
                {
                    "task_id": task_id,
                    "log_error_bucket": "error_tokens_reached",
                    "turn_waste_summary": "Found ACT and school-district-office sources, then looped.",
                    "turn_repeated_behavior": "Repeated discover-data/search/list/peek cycles.",
                    "turn_progress_stop_point": "After ACT and the school-district-office source were found, it kept reopening the same related school files.",
                    "productive_turn_ranges": "1-16",
                    "wasted_turn_ranges": "17-33",
                    "estimated_wasted_turns": "17",
                    "turn_budget_failure_reason": "Repeated rediscovery ate the tail.",
                    "turn_waste_evidence": "Turns 17-20 repeat discover-data and search_ideal around the same public-school source family; Turns 24-33 keep reopening public/private/postsecondary files and end with a repeated Iowa City grep",
                    "turn_waste_local_group": "NCES school-location spiral",
                    "turn_waste_local_group_reason": "It kept rediscovering and reopening the same school-location datasets instead of finishing the county aggregation.",
                }
            ]
            fieldnames = list(eval_rows[0].keys())

            self._write_csv(
                source_root / "modes" / model_dir / variant / "eval_results.csv",
                fieldnames,
                eval_rows,
            )
            self._write_csv(
                source_root / "modes" / model_dir / variant / "turn_waste_failures.csv",
                fieldnames,
                eval_rows,
            )

            grouped_rows = [
                {
                    **eval_rows[0],
                    "turn_waste_global_group": "source inspection or schema thrash",
                    "turn_waste_global_group_reason": "The run got trapped in file inspection.",
                    "turn_waste_global_subtype": "nces school-location spiral",
                    "turn_waste_global_subtype_reason": "Repeated rediscovery and peeking across NCES-style school-location files.",
                }
            ]
            grouped_fieldnames = list(grouped_rows[0].keys())
            self._write_csv(
                grouped_root / "modes" / model_dir / variant / "turn_waste_global_failures.csv",
                grouped_fieldnames,
                grouped_rows,
            )

            self._write_log(
                logs_root / model_dir / variant / "k-6-d-4" / "task_1.log",
                [
                    "--- Turn 1 (elapsed: 0.0s) ---",
                    'Executing: search_ideal({"query": "Texas prison releases"})',
                    "--- Turn 16 (elapsed: 231.4s) ---",
                    "MaxTokensReachedException: Agent has reached an unrecoverable state due to max_tokens limit.",
                ],
            )

            outputs = validate_turn_waste_root(
                source_root=source_root,
                logs_dir=logs_root,
                rewrite=True,
            )
            self.assertEqual(len(outputs["invalid_rows"]), 1)

            with (source_root / "modes" / model_dir / variant / "eval_results.csv").open() as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row[VALIDATION_STATUS_FIELD], "invalid")
            self.assertEqual(row[VALIDATION_MAX_TURN_FIELD], "16")
            self.assertIn("turn_waste_evidence references turns beyond log max turn 16", row[VALIDATION_NOTES_FIELD])

            report_outputs = build_turn_waste_global_report(
                source_root=grouped_root,
                logs_dir=logs_root,
                representative_limit=3,
            )
            report_text = report_outputs["report_path"].read_text()
            self.assertIn("Evidence: omitted due to failed row validation", report_text)
            self.assertNotIn("Turns 17-20 repeat discover-data", report_text)


if __name__ == "__main__":
    unittest.main()

