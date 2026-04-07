#!/usr/bin/env python3
"""
Classify each task into EM × D_acc decile bins (0.1 width).

D_acc bins:
  [0.0, 0.1), [0.1, 0.2), ..., [0.8, 0.9), [0.9, 1.0]

The last bin includes 1.0 exactly.

Usage:
    python analysis/failure_attribution_deciles.py [--traces-dir results/traces] [--results-dir results]
"""
import argparse
import json
from collections import Counter
from pathlib import Path

_DACC_EPS = 1e-9


def _fmt_edge(x: float) -> str:
    return f"{x:.1f}".replace(".", "_")


def _make_label(em: int, low: float, high: float) -> str:
    return f"em{em}_dacc_{_fmt_edge(low)}_to_{_fmt_edge(high)}"


_LABEL_ORDER = [
    _make_label(em, i / 10, (i + 1) / 10)
    for em in (1, 0)
    for i in range(10)
]


def _condition_model_from_path(jsonl_path: Path) -> tuple[str, str]:
    parts = jsonl_path.parts
    condition = parts[-3] if len(parts) >= 3 else "unknown"
    model = parts[-2] if len(parts) >= 2 else "unknown"
    return condition, model


def classify_failure_decile(task_result: dict, d_acc: float) -> str:
    em = int(bool(task_result.get("exact_match", 0)))
    d_acc_val = 0.0 if d_acc is None else float(d_acc)
    d_acc = max(0.0, min(1.0, d_acc_val))
    idx = 9 if d_acc >= 1.0 - _DACC_EPS else int(d_acc * 10)
    low = idx / 10
    high = (idx + 1) / 10
    return _make_label(em, low, high)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-json", default=None, help="Optional path to save counts as JSON")
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
                    key = make_condition_model_task_key(condition, model, task_id)
                    agent_results[key] = r

    counts: Counter = Counter()
    for m in metrics["task_metrics"]:
        task_id = m["task_id"]
        ar = agent_results.get(task_id, {})
        label = classify_failure_decile(ar, m["d_acc"])
        counts[label] += 1

    total = sum(counts.values())
    print(f"\nEM × D_acc Decile Attribution (n={total}):")
    print(f"  {'Label':<30} {'N':>4}  {'%':>6}")
    print(f"  {'-'*42}")
    for label in _LABEL_ORDER:
        n = counts.get(label, 0)
        pct = 100 * n / total if total else 0
        print(f"  {label:<30} {n:>4}  ({pct:5.1f}%)")

    if args.output_json:
        out = {
            "total": total,
            "labels": {
                label: {
                    "n": counts.get(label, 0),
                    "pct": round(100 * counts.get(label, 0) / total, 1) if total else 0.0,
                }
                for label in _LABEL_ORDER
            },
        }
        out_path = Path(args.output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
