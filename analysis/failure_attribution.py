#!/usr/bin/env python3
"""
Classify each task into EM × D_acc threshold bins.

Threshold bins:
  - d_acc < 0.2
  - 0.2 <= d_acc < 0.5
  - 0.5 <= d_acc < 0.8
  - 0.8 <= d_acc <= 1.0

Each bin is crossed with EM in {0, 1}.

Usage:
    python analysis/failure_attribution.py [--traces-dir results/traces] [--results-dir results]
"""
import argparse
import json
from collections import Counter
from pathlib import Path


# Display order for the summary table
_LABEL_ORDER = [
    "em1_dacc_ge_0_8",
    "em1_dacc_0_5_to_0_8",
    "em1_dacc_0_2_to_0_5",
    "em1_dacc_lt_0_2",
    "em0_dacc_ge_0_8",
    "em0_dacc_0_5_to_0_8",
    "em0_dacc_0_2_to_0_5",
    "em0_dacc_lt_0_2",
]

_DACC_EPS = 1e-9


def _condition_model_from_path(jsonl_path: Path) -> tuple[str, str]:
    parts = jsonl_path.parts
    condition = parts[-3] if len(parts) >= 3 else "unknown"
    model = parts[-2] if len(parts) >= 2 else "unknown"
    return condition, model


def classify_failure(
    task_result: dict,
    d_ret: int,
    d_acc: float,
    max_tool_calls: int = 30,
    num_read_calls: int | None = None,
) -> str:
    """Return the EM × D_acc threshold-bin label for a single task result.

    Args:
        task_result: row from agent_results.jsonl
        d_ret: unused in this taxonomy; kept for API compatibility
        d_acc: fraction of gold datasets accessed via a read tool (0.0-1.0)
        max_tool_calls: unused in this taxonomy; kept for API compatibility
        num_read_calls: unused in this taxonomy; kept for API compatibility
    """
    _ = d_ret, max_tool_calls, num_read_calls
    em = int(bool(task_result.get("exact_match", 0)))
    d_acc_val = 0.0 if d_acc is None else float(d_acc)
    d_acc = max(0.0, min(1.0, d_acc_val))

    if d_acc >= 0.8 - _DACC_EPS:
        d_acc_bin = "dacc_ge_0_8"
    elif d_acc >= 0.5 - _DACC_EPS:
        d_acc_bin = "dacc_0_5_to_0_8"
    elif d_acc >= 0.2 - _DACC_EPS:
        d_acc_bin = "dacc_0_2_to_0_5"
    else:
        d_acc_bin = "dacc_lt_0_2"

    return f"em{em}_{d_acc_bin}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    args = parser.parse_args()

    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analysis.discovery_metrics import (
        load_traces_with_context,
        load_task_gold_ids,
        compute_discovery_metrics,
        make_condition_model_task_key,
    )

    task_gold = load_task_gold_ids(args.tasks_dir)
    traces = load_traces_with_context(args.traces_dir)
    metrics = compute_discovery_metrics(traces, task_gold)

    # Load agent results for EM scores and sources_used
    agent_results: dict = {}
    for jsonl_path in Path(args.results_dir).rglob("agent_results.jsonl"):
        condition, model = _condition_model_from_path(jsonl_path)
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                task_id = str(r.get("task_id", ""))
                if task_id:
                    agent_results[make_condition_model_task_key(condition, model, task_id)] = r

    counts: Counter = Counter()
    for m in metrics["task_metrics"]:
        task_id = m["task_id"]
        ar = agent_results.get(task_id, {})
        label = classify_failure(ar, m["d_ret"], m["d_acc"], num_read_calls=m.get("num_read_calls", 0))
        counts[label] += 1
        m["failure_type"] = label

    total = sum(counts.values())
    print(f"\nEM × D_acc Threshold Attribution (n={total}):")
    print(f"  {'Label':<30} {'N':>4}  {'%':>6}")
    print(f"  {'-'*42}")
    for label in _LABEL_ORDER:
        n = counts.get(label, 0)
        pct = 100 * n / total if total else 0
        print(f"  {label:<30} {n:>4}  ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
