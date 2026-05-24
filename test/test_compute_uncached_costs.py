import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.compute_uncached_costs import compute_uncached_costs


class ComputeUncachedCostsTests(unittest.TestCase):
    def test_uses_trace_events_to_reprice_ideal_subagents_without_cache_discount(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results_dir = root / "results_semantic" / "modes"
            traces_dir = root / "results" / "traces" / "modes"
            model = "openai_gpt-5.4-nano"
            variant = "search_i_results_i_plani_computei_k5_skills_off"
            eval_dir = results_dir / model / variant
            trace_dir = traces_dir / model / variant / "k-1-d-1"
            eval_dir.mkdir(parents=True)
            trace_dir.mkdir(parents=True)

            with (eval_dir / "eval_results.csv").open("w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "task_id",
                        "input_tokens",
                        "cached_input_tokens",
                        "uncached_input_tokens",
                        "output_tokens",
                        "cost_usd",
                        "ideal_subagent_cost_usd",
                        "total_cost_with_all_subagents_usd",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "task_id": "tasks_mini/k-1-d-1/task_1.json",
                        "input_tokens": "10000",
                        "cached_input_tokens": "8000",
                        "uncached_input_tokens": "2000",
                        "output_tokens": "500",
                        "cost_usd": "0.001185",
                        "ideal_subagent_cost_usd": "0.008195",
                        "total_cost_with_all_subagents_usd": "0.00938",
                    }
                )

            trace_events = [
                {
                    "event": "ideal_subagent_cost",
                    "model_name": "openai/gpt-5.4-nano",
                    "input_tokens": 1000,
                    "cached_input_tokens": 800,
                    "uncached_input_tokens": 200,
                    "output_tokens": 100,
                    "cost_usd": 0.000181,
                },
                {
                    "event": "ideal_subagent_cost",
                    "model_name": "openai/gpt-5.4",
                    "input_tokens": 2000,
                    "cached_input_tokens": 1000,
                    "uncached_input_tokens": 1000,
                    "output_tokens": 200,
                    "cost_usd": 0.008014,
                },
            ]
            with (trace_dir / "task_1.jsonl").open("w") as f:
                for event in trace_events:
                    f.write(json.dumps(event) + "\n")

            result = compute_uncached_costs(results_dir, traces_dir)

            self.assertEqual(len(result.rows), 1)
            row = result.rows[0]
            self.assertAlmostEqual(row.logged_main_cost_usd, 0.001185)
            self.assertAlmostEqual(row.uncached_main_cost_usd, 0.002625)
            self.assertAlmostEqual(row.logged_ideal_cost_usd, 0.008195)
            self.assertAlmostEqual(row.uncached_ideal_cost_usd, 0.008325)
            self.assertAlmostEqual(row.logged_total_cost_usd, 0.00938)
            self.assertAlmostEqual(row.uncached_total_cost_usd, 0.01095)

            summary = result.variant_summaries[(model, variant)]
            self.assertAlmostEqual(summary["delta_total_cost_usd"], 0.00157)
            self.assertAlmostEqual(summary["uncached_total_cost_usd"], 0.01095)
            self.assertAlmostEqual(summary["avg_uncached_total_cost_usd"], 0.01095)
            self.assertAlmostEqual(summary["avg_uncached_main_cost_usd"], 0.002625)
            self.assertAlmostEqual(summary["avg_uncached_ideal_cost_usd"], 0.008325)


if __name__ == "__main__":
    unittest.main()
