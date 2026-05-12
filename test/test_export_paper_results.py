import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.export_paper_results import (
    build_main_result_rows,
    render_results_table,
)


class ExportPaperResultsTests(unittest.TestCase):
    def test_main_result_rows_include_planned_cells_and_current_values(self):
        summary_rows = [
            {
                "model": "openai_gpt-5.4-nano",
                "variant": "search_i_results_i_plani_computei_k5_skills_off",
                "search_tool": "ideal",
                "search_results": "ideal",
                "agent_management": "ideal",
                "computation_tool": "ideal",
                "n": 87,
                "semantic_match": 0.4023,
                "avg_total_cost_with_ideal_subagents_usd": 0.083,
                "avg_tool_calls_total": 17.8161,
                "D_acc_recall": None,
                "D_acc": None,
                "D_ret": None,
            },
            {
                "model": "openai_gpt-5.4-nano",
                "variant": "search_i_results_i_plani_k5_skills_off",
                "search_tool": "ideal",
                "search_results": "ideal",
                "agent_management": "ideal",
                "computation_tool": "standard",
                "n": 87,
                "semantic_match": 0.3333,
                "avg_total_cost_with_ideal_subagents_usd": 0.0152,
                "avg_tool_calls_total": 19.908,
                "D_acc_recall": None,
                "D_acc": None,
                "D_ret": None,
            },
        ]

        rows = build_main_result_rows(summary_rows)

        self.assertEqual(len(rows), 20)
        full_ideal = next(
            row for row in rows
            if row["model"] == "gpt-5.4-nano"
            and row["plan"] == "Ideal"
            and row["search"] == "Ideal"
            and row["compute"] == "Ideal"
            and row["results"] == "Ideal"
        )
        standard_compute = next(
            row for row in rows
            if row["model"] == "gpt-5.4-nano"
            and row["plan"] == "Ideal"
            and row["search"] == "Ideal"
            and row["compute"] == "Standard"
            and row["results"] == "Ideal"
        )
        preloaded_search = next(
            row for row in rows
            if row["model"] == "gpt-5.4-nano"
            and row["plan"] == "Ideal"
            and row["search"] == "Preloaded"
            and row["compute"] == "Ideal"
            and row["results"] == "Ideal"
        )
        pending_mini = next(row for row in rows if row["model"] == "gpt-5-mini")

        self.assertEqual(full_ideal["semantic_match"], "40.2")
        self.assertEqual(full_ideal["avg_cost"], "0.083")
        self.assertEqual(full_ideal["avg_calls"], "17.8")
        self.assertEqual(full_ideal["status"], "observed")
        self.assertEqual(standard_compute["semantic_match"], "33.3")
        self.assertEqual(standard_compute["compute"], "Standard")
        self.assertEqual(preloaded_search["condition"], "I-P-I-I")
        self.assertEqual(preloaded_search["status"], "pending")
        self.assertEqual(pending_mini["semantic_match"], "Pending")
        self.assertEqual(pending_mini["status"], "pending")

    def test_render_results_table_uses_standard_compute_and_pending_placeholders(self):
        rows = [
            {
                "model": "gpt-5.4-nano",
                "condition": "I-I-I-I",
                "plan": "Ideal",
                "search": "Ideal",
                "compute": "Standard",
                "results": "Ideal",
                "n": "87",
                "semantic_match": "33.3",
                "avg_cost": "0.015",
                "avg_calls": "19.9",
                "D_acc": "N/A",
                "D_ret": "N/A",
                "status": "observed",
            },
            {
                "model": "gpt-5-mini",
                "condition": "N-I-I-I",
                "plan": "Naive",
                "search": "Ideal",
                "compute": "Ideal",
                "results": "Ideal",
                "n": "Pending",
                "semantic_match": "Pending",
                "avg_cost": "Pending",
                "avg_calls": "Pending",
                "D_acc": "Pending",
                "D_ret": "Pending",
                "status": "pending",
            },
        ]

        latex = render_results_table(rows)

        self.assertIn("Standard", latex)
        self.assertIn("Pending", latex)
        self.assertIn("33.3", latex)
        self.assertNotIn("Compute naive", latex)


if __name__ == "__main__":
    unittest.main()
