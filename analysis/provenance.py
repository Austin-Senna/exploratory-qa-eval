#!/usr/bin/env python3
"""
Condition A: per-backend first-hit attribution for each gold dataset.

For each gold dataset, determines which search backend (sparse/hybrid/graph)
first retrieved it (lowest turn number), or "none" if never retrieved.

Usage:
    python analysis/provenance.py [--traces-dir results/traces/a]
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def _resolve_gold(task_id: str, task_gold: dict) -> list:
    """Match trace task_id ('k-2-d-1/task_1') to gold entry (mirrors discovery_metrics)."""
    if task_id in task_gold:
        return task_gold[task_id]
    for path_key in task_gold:
        p = Path(path_key)
        if f"{p.parent.name}/{p.stem}" == task_id:
            return task_gold[path_key]
    return []


def compute_provenance(traces: dict[str, list], task_gold: dict[str, list]) -> dict:
    """For each gold dataset, find the first backend that retrieved it."""
    backend_hits: Counter = Counter()
    total_gold: int = 0
    never_retrieved: int = 0
    task_provenance: list = []

    for task_id, task_traces in traces.items():
        gold_ids = set(_resolve_gold(task_id, task_gold))
        if not gold_ids:
            continue

        # Sort traces by turn number
        sorted_traces = sorted(task_traces, key=lambda t: t.get("turn", 0))

        first_hit: dict = {}  # gold_id -> (turn, backend)
        for trace in sorted_traces:
            backend = trace.get("tool", "unknown")
            result_ids = trace.get("result_dataset_ids", [])
            turn = trace.get("turn", 0)
            for rid in result_ids:
                if rid in gold_ids and rid not in first_hit:
                    first_hit[rid] = (turn, backend)

        total_gold += len(gold_ids)
        for gold_id in gold_ids:
            if gold_id in first_hit:
                _, backend = first_hit[gold_id]
                backend_hits[backend] += 1
            else:
                never_retrieved += 1

        task_provenance.append({
            "task_id": task_id,
            "gold_ids": list(gold_ids),
            "first_hits": {gid: {"turn": t, "backend": b} for gid, (t, b) in first_hit.items()},
        })

    return {
        "backend_hits": dict(backend_hits),
        "total_gold": total_gold,
        "never_retrieved": never_retrieved,
        "task_provenance": task_provenance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results/traces/a")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    args = parser.parse_args()

    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analysis.discovery_metrics import load_traces, load_task_gold_ids

    traces = load_traces(args.traces_dir)
    task_gold = load_task_gold_ids(args.tasks_dir)

    results = compute_provenance(traces, task_gold)
    hits = results["backend_hits"]
    total = results["total_gold"]
    never = results["never_retrieved"]

    print(f"\nCondition A Backend Provenance (total gold datasets: {total})")
    for backend in ["search_sparse", "search_hybrid", "search_graph"]:
        n = hits.get(backend, 0)
        pct = 100 * n / total if total else 0
        print(f"  {backend:<20} first-hit {n:>4} ({pct:.1f}%)")
    print(f"  {'never retrieved':<20} {never:>4} ({100*never/total:.1f}%)" if total else "")


if __name__ == "__main__":
    main()
