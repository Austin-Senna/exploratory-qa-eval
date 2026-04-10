#!/usr/bin/env python3
"""
Compute Exact Match (EM) and F1 per condition × model from agent_results.jsonl files.

Usage:
    python analysis/compute_em.py [--results-dir results]
"""
import argparse
import json
import os
from collections import defaultdict
from pathlib import Path


def load_results(results_dir: str) -> list[dict]:
    """Load all agent_results.jsonl files from results/{condition}/{model}/"""
    records = []
    for jsonl_path in Path(results_dir).rglob("agent_results.jsonl"):
        parts = jsonl_path.parts
        # Expect: results/{condition}/{model}/agent_results.jsonl
        condition = parts[-3] if len(parts) >= 3 else "unknown"
        model = parts[-2] if len(parts) >= 2 else "unknown"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                r.setdefault("condition", condition)
                r.setdefault("model_label", model)
                records.append(r)
    return records


_SEARCH_TOOL_NAMES = {
    "search_value", "search_schema", "search_reranked",
    "search_prefix", "search_ideal", "search", "search_keyword",
}


def _count_search_calls(record: dict) -> int:
    """Sum call_count for search tools from the tool_counts list in a record."""
    return sum(
        t.get("call_count", 0)
        for t in record.get("tool_counts", [])
        if t.get("name") in _SEARCH_TOOL_NAMES
    )


def _count_tool_calls(record: dict, tool_name: str) -> int:
    """Sum call_count for a specific tool from the tool_counts list in a record."""
    return sum(
        t.get("call_count", 0)
        for t in record.get("tool_counts", [])
        if t.get("name") == tool_name
    )


def compute_stats(records: list[dict]) -> dict:
    """Group by (condition, model) and compute EM, F1, cost, tool_calls, search_calls."""
    groups: dict = defaultdict(list)
    for r in records:
        key = (r.get("condition", "?"), r.get("model_label", r.get("model", "?")))
        groups[key].append(r)

    table = {}
    for (cond, model), rows in sorted(groups.items()):
        n = len(rows)
        em_vals = [r.get("exact_match", 0) for r in rows if "exact_match" in r]
        f1_vals = [r.get("f1_score", 0.0) for r in rows if "f1_score" in r]
        cost_vals = [r.get("cost_usd", 0.0) for r in rows]
        tool_vals = [r.get("tool_calls_total", 0) for r in rows]
        time_vals = [r.get("time", 0.0) for r in rows]
        search_vals = [_count_search_calls(r) for r in rows]
        query_file_vals = [_count_tool_calls(r, "query_file") for r in rows]
        execute_code_vals = [_count_tool_calls(r, "execute_code") for r in rows]

        table[(cond, model)] = {
            "condition": cond,
            "model": model,
            "n": n,
            "em": sum(em_vals) / len(em_vals) if em_vals else None,
            "em_count": sum(em_vals),
            "f1": sum(f1_vals) / len(f1_vals) if f1_vals else None,
            "avg_cost_usd": sum(cost_vals) / n if n else 0.0,
            "total_cost_usd": sum(cost_vals),
            "avg_tool_calls": sum(tool_vals) / n if n else 0.0,
            "avg_search_calls": sum(search_vals) / n if n else 0.0,
            "avg_query_file_calls": sum(query_file_vals) / n if n else 0.0,
            "avg_execute_code_calls": sum(execute_code_vals) / n if n else 0.0,
            "avg_time_s": sum(time_vals) / n if n else 0.0,
        }
    return table


def print_table(table: dict) -> None:
    header = f"{'Condition':<12} {'Model':<45} {'n':>4} {'EM%':>7} {'F1':>7} {'AvgCost':>9} {'AvgTools':>9}"
    print(header)
    print("-" * len(header))
    for (cond, model), s in table.items():
        em_pct = f"{s['em']*100:.1f}%" if s["em"] is not None else "N/A"
        f1_str = f"{s['f1']:.3f}" if s["f1"] is not None else "N/A"
        print(
            f"{cond:<12} {model:<45} {s['n']:>4} {em_pct:>7} {f1_str:>7} "
            f"${s['avg_cost_usd']:>8.4f} {s['avg_tool_calls']:>9.1f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--output", default=None, help="Save CSV to path")
    args = parser.parse_args()

    records = load_results(args.results_dir)
    if not records:
        print(f"No agent_results.jsonl files found under {args.results_dir}")
        return

    print(f"Loaded {len(records)} task results\n")
    table = compute_stats(records)
    print_table(table)

    if args.output:
        import csv
        fields = ["condition", "model", "n", "em", "em_count", "f1",
                  "avg_cost_usd", "total_cost_usd", "avg_tool_calls", "avg_time_s"]
        with open(args.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for s in table.values():
                writer.writerow(s)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
