import csv
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from analysis.paper_figure_generator import (
    _benchmark_defaults,
    _load_search_figure_data,
    _search_variant_label,
    _selected_existing_figures,
    _turn_waste_scope_complete,
    export_paper_figures,
)


class TestPaperFigureGenerator(unittest.TestCase):
    def test_benchmark_defaults_choose_expected_roots(self):
        lakeqa = _benchmark_defaults("lakeqa")
        kramabench = _benchmark_defaults("kramabench")

        self.assertEqual(lakeqa.results_dir, Path("results_semantic/modes"))
        self.assertEqual(lakeqa.base_results_dir, Path("results/modes"))
        self.assertEqual(lakeqa.traces_dir, Path("results/traces/modes"))
        self.assertEqual(lakeqa.tasks_dir, Path("tasks_mini"))
        self.assertEqual(lakeqa.analysis_dir, Path("analysis_results_mode_semantic"))

        self.assertEqual(kramabench.results_dir, Path("results-kramabench_semantic/modes"))
        self.assertEqual(kramabench.base_results_dir, Path("results-kramabench/modes"))
        self.assertEqual(kramabench.traces_dir, Path("results-kramabench/traces/modes"))
        self.assertEqual(kramabench.tasks_dir, Path("tasks-mini-kramabench"))
        self.assertEqual(kramabench.analysis_dir, Path("analysis_results_mode_kramabench_semantic"))

    def test_selected_existing_figures_include_benchmark_specific_fig21b(self):
        self.assertIn(
            "fig21b_lakeqa_semantic_delta_ablation.pdf",
            _selected_existing_figures("lakeqa"),
        )
        self.assertIn(
            "fig21b_krama_semantic_delta_ablation.pdf",
            _selected_existing_figures("kramabench"),
        )

    def test_search_variant_label_maps_canonical_trio(self):
        self.assertEqual(
            _search_variant_label("search_n_results_i_plani_computei_k5_skills_off"),
            "NII",
        )
        self.assertEqual(
            _search_variant_label("search_d_results_i_plani_computei_k5_skills_off"),
            "DII",
        )
        self.assertEqual(
            _search_variant_label("search_i_results_i_plani_computei_k5_skills_off"),
            "III",
        )
        self.assertIsNone(_search_variant_label("search_p_results_i_plani_computei_k5_skills_off"))

    def test_load_search_figure_data_filters_canonical_trio(self):
        with TemporaryDirectory() as tmpdir:
            analysis_dir = Path(tmpdir)
            summary_rows = [
                {
                    "model": "openai_gpt-5-mini",
                    "variant": "search_n_results_i_plani_computei_k5_skills_off",
                    "avg_search_calls": 3,
                    "D_ret": 0.5,
                    "D_acc": 0.25,
                },
                {
                    "model": "openai_gpt-5-mini",
                    "variant": "search_d_results_i_plani_computei_k5_skills_off",
                    "avg_search_calls": 4,
                    "D_ret": 0.6,
                    "D_acc": 0.4,
                },
                {
                    "model": "openai_gpt-5-mini",
                    "variant": "search_i_results_i_plani_computei_k5_skills_off",
                    "avg_search_calls": 1,
                    "D_ret": 1.0,
                    "D_acc": 1.0,
                },
                {
                    "model": "openai_gpt-5-mini",
                    "variant": "search_p_results_i_plani_computei_k5_skills_off",
                    "avg_search_calls": 0,
                    "D_ret": 1.0,
                    "D_acc": 1.0,
                },
            ]
            (analysis_dir / "summary.json").write_text(json.dumps(summary_rows))
            with (analysis_dir / "search_call_cumulative_retrieval.csv").open("w", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "model",
                        "variant",
                        "task_id",
                        "search_call_index",
                        "cumulative_search_gold_recall",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "model": "openai_gpt-5-mini",
                        "variant": "search_n_results_i_plani_computei_k5_skills_off",
                        "task_id": "k-1/task_1",
                        "search_call_index": "1",
                        "cumulative_search_gold_recall": "0.5",
                    }
                )

            data = _load_search_figure_data(analysis_dir)

            self.assertEqual(list(data["summary_by_model"].keys()), ["openai_gpt-5-mini"])
            self.assertEqual(
                [row["label"] for row in data["summary_by_model"]["openai_gpt-5-mini"]],
                ["NII", "DII", "III"],
            )
            self.assertEqual(data["curves"][("openai_gpt-5-mini", "NII")][1], 0.5)

    def test_export_paper_figures_copies_existing_and_new_outputs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            analysis_dir = root / "analysis"
            figures_dir = analysis_dir / "figures"
            figures_dir.mkdir(parents=True)
            for name in [
                "fig05_turn_waste_groups_by_model.pdf",
                "fig05b_turn_waste_groups_by_condition.pdf",
                "fig21b_semantic_delta_ablation_compact.pdf",
            ]:
                (figures_dir / name).write_bytes(b"%PDF-1.4\n")
            new_figure = analysis_dir / "search_efficiency_cumulative_retrieval_lakeqa.pdf"
            new_figure.write_bytes(b"%PDF-1.4\n")

            copied = export_paper_figures(
                benchmark="lakeqa",
                analysis_dir=analysis_dir,
                search_figure_path=new_figure,
                destinations=[root / "paper", root / "mirror"],
            )

            self.assertIn(root / "paper" / new_figure.name, copied)
            self.assertTrue((root / "mirror" / "fig05_turn_waste_groups_by_model.pdf").exists())
            self.assertTrue((root / "paper" / "fig21b_lakeqa_semantic_delta_ablation.pdf").exists())

    def test_turn_waste_scope_complete_detects_partial_grouped_outputs(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            results_dir = root / "results_semantic" / "modes"
            grouped_dir = root / "results_semantic_turn_waste_grouped"
            for variant in ["variant_a", "variant_b"]:
                path = results_dir / "model_a" / variant / "eval_results.csv"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("task_id,semantic_match\n")
            grouped_path = grouped_dir / "model_a" / "variant_a" / "eval_results.csv"
            grouped_path.parent.mkdir(parents=True, exist_ok=True)
            grouped_path.write_text("task_id,turn_waste_global_group,turn_waste_global_group_reason\n")

            self.assertFalse(_turn_waste_scope_complete(results_dir, grouped_dir, None))

            grouped_path = grouped_dir / "model_a" / "variant_b" / "eval_results.csv"
            grouped_path.parent.mkdir(parents=True, exist_ok=True)
            grouped_path.write_text("task_id,turn_waste_global_group,turn_waste_global_group_reason\n")

            self.assertTrue(_turn_waste_scope_complete(results_dir, grouped_dir, None))

    def test_export_paper_figures_uses_fallback_dir_for_optional_figures(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            analysis_dir = root / "analysis"
            (analysis_dir / "figures").mkdir(parents=True)
            fallback_dir = root / "existing_paper"
            fallback_dir.mkdir()
            for name in [
                "fig05_turn_waste_groups_by_model.pdf",
                "fig05b_turn_waste_groups_by_condition.pdf",
                "fig21b_lakeqa_semantic_delta_ablation.pdf",
            ]:
                (fallback_dir / name).write_bytes(b"%PDF-1.4\n")
            new_figure = analysis_dir / "search_efficiency_cumulative_retrieval_lakeqa.pdf"
            new_figure.write_bytes(b"%PDF-1.4\n")

            export_paper_figures(
                benchmark="lakeqa",
                analysis_dir=analysis_dir,
                search_figure_path=new_figure,
                destinations=[fallback_dir, root / "mirror"],
                fallback_dirs=[fallback_dir],
            )

            self.assertTrue((root / "mirror" / "fig05_turn_waste_groups_by_model.pdf").exists())


if __name__ == "__main__":
    unittest.main()
