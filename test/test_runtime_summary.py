import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.runtime_summary import compute_runtime_summary


class RuntimeSummaryTests(unittest.TestCase):
    def test_sums_runtime_by_mode_and_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lakeqa_modes = root / "results" / "modes"
            kramabench_modes = root / "results-kramabench" / "modes"

            self._write_eval_csv(
                lakeqa_modes / "openai_gpt-5-mini" / "mode-x" / "eval_results.csv",
                [
                    ("lake/task_1.json", 1.25, 100, 10, 0.10),
                    ("lake/task_2.json", 2.75, 200, 20, 0.20),
                ],
            )
            self._write_eval_csv(
                lakeqa_modes / "openai_gpt-5.4-nano" / "mode-x" / "eval_results.csv",
                [("lake/task_3.json", 3.0, 300, 30, 0.30)],
            )
            self._write_eval_csv(
                kramabench_modes / "openai_gpt-5-mini" / "mode-y" / "eval_results.csv",
                [("krama/task_1.json", 4.0, 400, 40, 0.40)],
            )

            summary = compute_runtime_summary(
                {
                    "lakeqa": lakeqa_modes,
                    "kramabench": kramabench_modes,
                }
            )

            expected_lakeqa_uncached_cost = (
                (0.25 * 300 / 1_000_000) + (2.00 * 30 / 1_000_000)
                + (0.20 * 300 / 1_000_000) + (1.25 * 30 / 1_000_000)
            )
            expected_kramabench_uncached_cost = (
                (0.25 * 400 / 1_000_000) + (2.00 * 40 / 1_000_000)
            )
            expected_overall_uncached_cost = expected_lakeqa_uncached_cost + expected_kramabench_uncached_cost

            self.assertEqual(summary.overall["tasks"], 4)
            self.assertAlmostEqual(summary.overall["total_seconds"], 11.0)
            self.assertAlmostEqual(summary.overall["total_cost_usd"], expected_overall_uncached_cost)
            self.assertAlmostEqual(summary.overall["logged_total_cost_usd"], 1.0)

            lakeqa = summary.by_benchmark["lakeqa"]
            self.assertEqual(lakeqa["tasks"], 3)
            self.assertAlmostEqual(lakeqa["total_seconds"], 7.0)
            self.assertAlmostEqual(lakeqa["total_cost_usd"], expected_lakeqa_uncached_cost)
            self.assertAlmostEqual(lakeqa["logged_total_cost_usd"], 0.60)

            kramabench = summary.by_benchmark["kramabench"]
            self.assertEqual(kramabench["tasks"], 1)
            self.assertAlmostEqual(kramabench["total_seconds"], 4.0)
            self.assertAlmostEqual(kramabench["total_cost_usd"], expected_kramabench_uncached_cost)
            self.assertAlmostEqual(kramabench["logged_total_cost_usd"], 0.40)

            lakeqa_mode = summary.by_mode[("lakeqa", "mode-x")]
            self.assertEqual(lakeqa_mode["tasks"], 3)
            self.assertAlmostEqual(lakeqa_mode["total_seconds"], 7.0)
            self.assertAlmostEqual(lakeqa_mode["total_cost_usd"], expected_lakeqa_uncached_cost)

            model_mode = summary.by_model_mode[("lakeqa", "openai_gpt-5-mini", "mode-x")]
            self.assertEqual(model_mode["tasks"], 2)
            self.assertAlmostEqual(model_mode["total_seconds"], 4.0)
            self.assertAlmostEqual(
                model_mode["total_cost_usd"],
                (0.25 * 300 / 1_000_000) + (2.00 * 30 / 1_000_000),
            )
            self.assertAlmostEqual(model_mode["logged_total_cost_usd"], 0.30)

    def _write_eval_csv(self, path: Path, rows: list[tuple[str, float, int, int, float]]) -> None:
        path.parent.mkdir(parents=True)
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "task_id",
                    "runtime_seconds",
                    "input_tokens",
                    "output_tokens",
                    "ideal_subagent_input_tokens",
                    "ideal_subagent_output_tokens",
                    "delegation_subagent_input_tokens",
                    "delegation_subagent_output_tokens",
                    "total_cost_with_all_subagents_usd",
                ],
            )
            writer.writeheader()
            for task_id, runtime_seconds, input_tokens, output_tokens, total_cost_usd in rows:
                writer.writerow(
                    {
                        "task_id": task_id,
                        "runtime_seconds": runtime_seconds,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "ideal_subagent_input_tokens": 0,
                        "ideal_subagent_output_tokens": 0,
                        "delegation_subagent_input_tokens": 0,
                        "delegation_subagent_output_tokens": 0,
                        "total_cost_with_all_subagents_usd": total_cost_usd,
                    }
                )


if __name__ == "__main__":
    unittest.main()
