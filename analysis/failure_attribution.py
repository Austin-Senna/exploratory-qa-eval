#!/usr/bin/env python3
"""
Classify each task into a success mode or failure mode using the expanded taxonomy.

Success modes (EM == 1):
  grounded_success              — EM=1, D_acc=1          (right answer, all gold sources cited)
  partial_parametric_success    — EM=1, 0 < D_acc <= 0.5 (right answer, only some gold sources cited)
  parametric_hallucination      — EM=1, D_acc=0          (right answer, no gold sources cited — lucky guess)

Failure modes (EM == 0):
  execution_failed              — EM=0, D_ret=1, D_acc=1 (found + cited gold, but wrong final answer)
  discovery_reasoning_failed    — EM=0, D_ret=1, D_acc=0 (gold was retrieved but not recognised/cited)
  hallucination                 — EM=0, D_ret=0, sources=[] (nothing found, nothing cited, wrong)
  search_failed                 — EM=0, D_ret=0, sources!=[] (cited something, but gold never retrieved)

Usage:
    python analysis/failure_attribution.py [--traces-dir results/traces] [--results-dir results]
"""
import argparse
import json
from collections import Counter
from pathlib import Path


# Display order for the summary table
_LABEL_ORDER = [
    # Success modes
    "grounded_success",
    "partial_parametric_success",
    "parametric_hallucination",
    # Failure modes
    "execution_failed",
    "read_not_cited",
    "search_not_read",
    "hallucination",
    "search_failed",
]


def classify_failure(task_result: dict, d_ret: int, d_read: int, d_acc: float) -> str:
    """Return the taxonomy label for a single task result.

    Args:
        task_result: row from agent_results.jsonl
        d_ret:  1 if any gold dataset appeared in search results, else 0
        d_read: 1 if agent opened a gold dataset via a read tool, else 0
        d_acc:  fraction of gold datasets cited in the final answer (0.0–1.0)
    """
    em = int(bool(task_result.get("exact_match", 0)))
    sources = task_result.get("sources_used", [])

    # --- Success modes ---
    if em:
        if d_acc == 1:
            return "grounded_success"
        if d_acc >= 0.5:
            return "partial_parametric_success"
        return "parametric_hallucination"

    # --- Failure modes ---
    if d_ret == 1:
        if d_acc == 1:
            return "execution_failed"
        if d_read == 1:
            return "read_not_cited"   # opened gold, failed to cite/reason
        return "search_not_read"      # found in search, never opened

    # d_ret == 0
    if not sources:
        return "hallucination"
    return "search_failed"


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
        label = classify_failure(ar, m["d_ret"], m.get("d_read", 0), m["d_acc"])
        counts[label] += 1
        m["failure_type"] = label

    total = sum(counts.values())
    print(f"\nFailure / Success Attribution (n={total}):")
    print(f"  {'Label':<30} {'N':>4}  {'%':>6}")
    print(f"  {'-'*42}")
    for label in _LABEL_ORDER:
        n = counts.get(label, 0)
        pct = 100 * n / total if total else 0
        print(f"  {label:<30} {n:>4}  ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
