import csv
import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT_PATH = Path(__file__).resolve().parent.parent / "analysis" / "combine_turn_waste_grouped_models.py"


def load_combiner():
    spec = importlib.util.spec_from_file_location("combine_turn_waste_grouped_models", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestTurnWasteModelCombinerSkill(unittest.TestCase):
    def _write_failures(self, path: Path, rows: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "task_id",
            "log_error_bucket",
            "estimated_wasted_turns",
            "turn_waste_global_group",
            "turn_waste_global_subtype",
            "turn_waste_evidence",
        ]
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def test_combines_grouped_failures_and_reports_model_counts(self):
        combiner = load_combiner()

        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            grouped_root = root / "results_semantic_turn_waste_grouped"
            output_root = root / "results_semantic_turn_waste_grouped_combined"

            self._write_failures(
                grouped_root
                / "openai_gpt-5-mini"
                / "modes"
                / "openai_gpt-5-mini"
                / "search_a"
                / "turn_waste_global_failures.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "log_error_bucket": "error_tools_limit",
                        "estimated_wasted_turns": "6",
                        "turn_waste_global_group": "Redundant Revalidation",
                        "turn_waste_global_subtype": "candidate rechecks",
                        "turn_waste_evidence": "Turn 20 repeats the same candidate query.",
                    }
                ],
            )
            self._write_failures(
                grouped_root
                / "openai_gpt-5.4-nano"
                / "modes"
                / "openai_gpt-5.4-nano"
                / "search_a"
                / "turn_waste_global_failures.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "log_error_bucket": "error_tools_limit",
                        "estimated_wasted_turns": "4",
                        "turn_waste_global_group": "Redundant Revalidation",
                        "turn_waste_global_subtype": "schema rechecks",
                        "turn_waste_evidence": "Turn 18 repeats schema inspection.",
                    },
                    {
                        "task_id": "tasks_mini/k-2-d-1/task_1.json",
                        "log_error_bucket": "error_unknown",
                        "estimated_wasted_turns": "2",
                        "turn_waste_global_group": "Source and Query-Shape Churn",
                        "turn_waste_global_subtype": "",
                        "turn_waste_evidence": "Turn 12 probes the wrong file.",
                    },
                ],
            )

            outputs = combiner.combine_grouped_models(grouped_root=grouped_root, output_root=output_root)

            with outputs["csv_path"].open() as handle:
                combined_rows = list(csv.DictReader(handle))
            self.assertEqual(len(combined_rows), 3)
            self.assertEqual(
                [row["model_variant"] for row in combined_rows],
                ["openai_gpt-5-mini", "openai_gpt-5.4-nano", "openai_gpt-5.4-nano"],
            )
            self.assertEqual(
                combined_rows[0]["source_file"],
                "openai_gpt-5-mini/modes/openai_gpt-5-mini/search_a/turn_waste_global_failures.csv",
            )

            report_text = outputs["report_path"].read_text()
            self.assertIn("| Redundant Revalidation | 2 | openai_gpt-5-mini: 1; openai_gpt-5.4-nano: 1 |", report_text)
            self.assertIn("| Source and Query-Shape Churn | 1 | openai_gpt-5.4-nano: 1 |", report_text)
            self.assertIn("| openai_gpt-5.4-nano | 2 |", report_text)
            self.assertIn("| openai_gpt-5-mini | 1 |", report_text)
            self.assertIn("[task](../tasks_mini/k-1-d-1/task_1.json)", report_text)
            self.assertIn("[plan](../plans_mini/k-1-d-1/task_1.json)", report_text)
            self.assertIn(
                "[log](../logs/modes/openai_gpt-5-mini/search_a/tasks_mini/k-1-d-1/task_1.log)",
                report_text,
            )

    def test_reconciles_equivalent_group_names_across_models(self):
        combiner = load_combiner()

        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            grouped_root = root / "results_semantic_turn_waste_grouped"
            output_root = root / "results_semantic_turn_waste_grouped_combined"

            self._write_failures(
                grouped_root
                / "openai_gpt-5-mini"
                / "modes"
                / "openai_gpt-5-mini"
                / "search_a"
                / "turn_waste_global_failures.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "log_error_bucket": "error_tools_limit",
                        "estimated_wasted_turns": "6",
                        "turn_waste_global_group": "Redundant Reconfirmation After Evidence",
                        "turn_waste_global_subtype": "candidate rechecks",
                        "turn_waste_evidence": "Turn 20 repeats the same candidate query.",
                    }
                ],
            )
            self._write_failures(
                grouped_root
                / "openai_gpt-5.4-nano"
                / "modes"
                / "openai_gpt-5.4-nano"
                / "search_a"
                / "turn_waste_global_failures.csv",
                [
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_2.json",
                        "log_error_bucket": "error_tools_limit",
                        "estimated_wasted_turns": "4",
                        "turn_waste_global_group": "Same-hop recomputation churn",
                        "turn_waste_global_subtype": "schema rechecks",
                        "turn_waste_evidence": "Turn 18 repeats schema inspection.",
                    }
                ],
            )

            outputs = combiner.combine_grouped_models(grouped_root=grouped_root, output_root=output_root)

            with outputs["csv_path"].open() as handle:
                combined_rows = list(csv.DictReader(handle))
            self.assertEqual(
                {row["reconciled_turn_waste_global_group"] for row in combined_rows},
                {"Redundant same-hop work after evidence"},
            )

            report_text = outputs["report_path"].read_text()
            self.assertIn(
                "| Redundant same-hop work after evidence | 2 | openai_gpt-5-mini: 1; openai_gpt-5.4-nano: 1 |",
                report_text,
            )

    def test_condition_figure_counts_named_conditions_and_excludes_runtime_fallback(self):
        combiner = load_combiner()

        rows = [
            {
                "mode_variant": "search_i_results_i_plann_computei_k5_skills_off",
                "model_variant": "openai_gpt-5.4-nano",
                "reconciled_turn_waste_global_group": "Data/source access and repair loops",
            },
            {
                "mode_variant": "search_i_results_i_plann_computei_k5_skills_off",
                "model_variant": "openai_gpt-5-mini",
                "reconciled_turn_waste_global_group": "Redundant same-hop work after evidence",
            },
            {
                "mode_variant": "search_i_results_i_plann_computei_k5_skills_off",
                "model_variant": "openai_gpt-5-mini",
                "reconciled_turn_waste_global_group": "Runtime/blocker fallback",
            },
            {
                "mode_variant": "search_n_results_i_plani_computei_k5_skills_off",
                "model_variant": "openai_gpt-5.4-nano",
                "reconciled_turn_waste_global_group": "Wrong-source and lookup fixation",
            },
            {
                "mode_variant": "search_n_results_i_plann_k5_skills_off",
                "model_variant": "openai_gpt-5.4-nano",
                "reconciled_turn_waste_global_group": "Redundant same-hop work after evidence",
            },
        ]

        active_conditions, ordered_groups, counts = combiner.condition_group_counts(rows)
        condition_models = combiner.ordered_condition_models(active_conditions, counts)

        self.assertEqual([label for label, _ in active_conditions], ["No Plan", "BM25"])
        self.assertEqual(
            ordered_groups,
            [
                "Data/source access and repair loops",
                "Redundant same-hop work after evidence",
                "Wrong-source and lookup fixation",
            ],
        )
        self.assertEqual(
            condition_models[:2],
            [
                ("No Plan", "search_i_results_i_plann_computei_k5_skills_off", "openai_gpt-5.4-nano"),
                ("No Plan", "search_i_results_i_plann_computei_k5_skills_off", "openai_gpt-5-mini"),
            ],
        )
        self.assertEqual(counts[("search_i_results_i_plann_computei_k5_skills_off", "openai_gpt-5.4-nano")]["Data/source access and repair loops"], 1)
        self.assertEqual(counts[("search_n_results_i_plani_computei_k5_skills_off", "openai_gpt-5.4-nano")]["Wrong-source and lookup fixation"], 1)
        self.assertNotIn("Runtime/blocker fallback", ordered_groups)


if __name__ == "__main__":
    unittest.main()
