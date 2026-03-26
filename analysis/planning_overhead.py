#!/usr/bin/env python3
"""
Planning overhead analysis for Condition B.

Since the `plan` tool is excluded from tool_calls_total and not logged separately,
cycle_count (LLM invocation count) is used as a proxy for planning depth —
more planning calls drive more cycles.

Computes:
  - Mean EM and mean output_tokens per cycle_count bin (Condition B)
  - Pearson correlation between cycle_count and exact_match (Condition B)

Usage:
    python analysis/planning_overhead.py [--results-dir results]
"""
import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.compute_em import load_results

_CYCLE_BINS = [
    ("1-3", lambda n: 1 <= n <= 3),
    ("4-6", lambda n: 4 <= n <= 6),
    ("7-10", lambda n: 7 <= n <= 10),
    ("11+", lambda n: n >= 11),
]


def _assign_cycle_bin(cycles: int) -> str:
    for label, pred in _CYCLE_BINS:
        if pred(cycles):
            return label
    return "11+"


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx * sy == 0:
        return None
    return round(cov / (sx * sy), 4)


def compute_planning_overhead(records: list[dict]) -> dict:
    """Analyse cycle_count vs EM and output_tokens for Condition B.

    Returns:
        {
          "by_bin": {bin_label: {"mean_em": float, "mean_output_tokens": float, "n": int}},
          "pearson_cycle_em": float | None,
          "n_cond_b": int,
        }
    """
    b_records = [r for r in records if r.get("condition") == "b"]
    if not b_records:
        return {"by_bin": {}, "pearson_cycle_em": None, "n_cond_b": 0}

    bins: dict = defaultdict(lambda: {"em": [], "tokens": []})
    cycle_list: list[float] = []
    em_list: list[float] = []

    for r in b_records:
        em = r.get("exact_match")
        cycles = r.get("cycle_count")
        tokens = r.get("output_tokens")
        if em is None or cycles is None:
            continue
        label = _assign_cycle_bin(int(cycles))
        bins[label]["em"].append(float(em))
        if tokens is not None:
            bins[label]["tokens"].append(float(tokens))
        cycle_list.append(float(cycles))
        em_list.append(float(em))

    by_bin = {}
    for label, _ in _CYCLE_BINS:
        entry = bins.get(label, {"em": [], "tokens": []})
        em_vals = entry["em"]
        tok_vals = entry["tokens"]
        by_bin[label] = {
            "mean_em": round(sum(em_vals) / len(em_vals), 4) if em_vals else None,
            "mean_output_tokens": round(sum(tok_vals) / len(tok_vals), 1) if tok_vals else None,
            "n": len(em_vals),
        }

    return {
        "by_bin": by_bin,
        "pearson_cycle_em": _pearson(cycle_list, em_list),
        "n_cond_b": len(b_records),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()

    records = load_results(args.results_dir)
    if not records:
        print(f"No agent_results.jsonl files found under {args.results_dir}")
        return

    result = compute_planning_overhead(records)
    if result["n_cond_b"] == 0:
        print("No Condition B records found.")
        return

    print(f"\nPlanning Overhead — Condition B (n={result['n_cond_b']})")
    print(f"  Pearson r(cycle_count, exact_match) = {result['pearson_cycle_em']}")
    print(f"\n  {'Cycles':<8} {'EM%':>7} {'AvgOutTokens':>14} {'n':>5}")
    print(f"  {'-'*36}")
    for label, _ in _CYCLE_BINS:
        entry = result["by_bin"].get(label, {})
        em = entry.get("mean_em")
        tok = entry.get("mean_output_tokens")
        n = entry.get("n", 0)
        em_str = f"{em*100:.1f}%" if em is not None else "  N/A"
        tok_str = f"{tok:.0f}" if tok is not None else "N/A"
        print(f"  {label:<8} {em_str:>7} {tok_str:>14} {n:>5}")


if __name__ == "__main__":
    main()
