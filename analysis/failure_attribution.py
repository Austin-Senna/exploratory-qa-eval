#!/usr/bin/env python3
"""
Classify failures into: search / discovery-reasoning / execution / hallucination.

Failure taxonomy:
  search            — gold dataset never appeared in any search result (D_ret=0)
  discovery-reason  — gold dataset retrieved but not cited in answer (D_ret=1, D_acc=0)
  execution         — gold dataset cited but answer is wrong (D_acc=1, EM=0)
  hallucination     — no sources cited, answer wrong, gold never retrieved
  correct           — EM=1

Usage:
    python analysis/failure_attribution.py [--traces-dir results/traces] [--results-dir results]
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def classify_failure(task_result: dict, d_ret: int, d_acc: int) -> str:
    em = task_result.get("exact_match", 0)
    if em:
        return "correct"
    if d_ret == 0:
        sources = task_result.get("sources_used", [])
        if not sources:
            return "hallucination"
        return "search"
    if d_acc == 0:
        return "discovery-reason"
    return "execution"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    args = parser.parse_args()

    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analysis.discovery_metrics import (
        load_traces,
        load_task_gold_ids,
        compute_discovery_metrics,
    )

    traces = load_traces(args.traces_dir)
    task_gold = load_task_gold_ids(args.tasks_dir)
    metrics = compute_discovery_metrics(traces, task_gold)

    # Load agent results for EM scores and sources_used
    agent_results: dict = {}
    for jsonl_path in Path(args.results_dir).rglob("agent_results.jsonl"):
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                task_id = str(r.get("task_id", ""))
                if task_id:
                    p = Path(task_id)
                    agent_results[f"{p.parent.name}/{p.stem}"] = r

    counts: Counter = Counter()
    for m in metrics["task_metrics"]:
        task_id = m["task_id"]
        ar = agent_results.get(task_id, {})
        label = classify_failure(ar, m["d_ret"], m["d_acc"])
        counts[label] += 1
        m["failure_type"] = label

    total = sum(counts.values())
    print(f"\nFailure Attribution (n={total}):")
    for label in ["correct", "search", "discovery-reason", "execution", "hallucination"]:
        n = counts.get(label, 0)
        pct = 100 * n / total if total else 0
        print(f"  {label:<22} {n:>4} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
