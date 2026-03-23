#!/usr/bin/env python3
"""
Compute discovery metrics D_ret, D_acc, precision/recall/F1 from trace JSONL files.

D_ret: fraction of tasks where at least one gold dataset appeared in any search result
D_acc: fraction of tasks where the agent cited a gold dataset in its submit_answer sources

Usage:
    python analysis/discovery_metrics.py [--traces-dir results/traces] [--tasks-dir tasks_mini]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_traces(traces_dir: str) -> dict[str, list]:
    """Load all trace JSONL files. Returns {task_id: [trace_records]}.

    task_id key is "{parent_dir}/{stem}", e.g. "k-2-d-1/task_1".
    """
    traces: dict = defaultdict(list)
    for jsonl_path in Path(traces_dir).rglob("*.jsonl"):
        task_id = f"{jsonl_path.parent.name}/{jsonl_path.stem}"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    traces[task_id].append(json.loads(line))
    return dict(traces)


def compute_discovery_metrics(
    traces: dict[str, list],
    task_gold: dict[str, list],
) -> dict:
    """Compute per-task and aggregate discovery metrics."""
    task_metrics: list = []

    for task_id, task_traces in traces.items():
        # Resolve task_id stem back to a full path key for gold lookup
        gold_ids = set(_resolve_gold(task_id, task_gold))
        if not gold_ids:
            continue

        # Separate search traces from submit_answer record
        search_traces = [t for t in task_traces if t.get("tool") != "submit_answer"]
        submit_record = next((t for t in task_traces if t.get("tool") == "submit_answer"), None)

        # D_ret: did any search result contain a gold dataset?
        all_result_ids: set = set()
        for trace in search_traces:
            all_result_ids.update(trace.get("result_dataset_ids", []))

        retrieved_gold = all_result_ids & gold_ids
        d_ret = int(bool(retrieved_gold))

        # Precision / Recall over all search results
        precision = len(retrieved_gold) / len(all_result_ids) if all_result_ids else 0.0
        recall = len(retrieved_gold) / len(gold_ids) if gold_ids else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        # D_acc: did the agent cite a gold dataset in submit_answer?
        cited_ids: set = set()
        if submit_record:
            for s in submit_record.get("sources_cited", []):
                cited_ids.add(str(s))
        d_acc = int(bool(cited_ids & gold_ids))

        task_metrics.append({
            "task_id": task_id,
            "gold_ids": list(gold_ids),
            "d_ret": d_ret,
            "d_acc": d_acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "num_search_calls": len(search_traces),
            "num_results_total": len(all_result_ids),
        })

    n = len(task_metrics)
    if n == 0:
        return {"task_metrics": [], "aggregate": {}}

    agg = {
        "n": n,
        "D_ret": sum(m["d_ret"] for m in task_metrics) / n,
        "D_acc": sum(m["d_acc"] for m in task_metrics) / n,
        "avg_precision": sum(m["precision"] for m in task_metrics) / n,
        "avg_recall": sum(m["recall"] for m in task_metrics) / n,
        "avg_f1": sum(m["f1"] for m in task_metrics) / n,
        "avg_search_calls": sum(m["num_search_calls"] for m in task_metrics) / n,
    }

    return {"task_metrics": task_metrics, "aggregate": agg}


def _resolve_gold(task_id: str, task_gold: dict[str, list]) -> list:
    """Match a trace task_id ("k-2-d-1/task_1") to a gold entry."""
    # Exact match
    if task_id in task_gold:
        return task_gold[task_id]
    # Match on "{parent.name}/{stem}" from full path keys
    for path_key in task_gold:
        p = Path(path_key)
        if f"{p.parent.name}/{p.stem}" == task_id:
            return task_gold[path_key]
    return []


def load_task_gold_ids(tasks_dir: str) -> dict[str, list]:
    """Load gold dataset IDs from task files. Returns {task_path: [dataset_id]}."""
    import glob as glob_mod
    gold: dict = {}
    for path in glob_mod.glob(str(Path(tasks_dir) / "**" / "*.json"), recursive=True):
        with open(path) as f:
            task = json.load(f)
        gold[path] = task.get("datasets_used", [])
    return gold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    args = parser.parse_args()

    traces = load_traces(args.traces_dir)
    task_gold = load_task_gold_ids(args.tasks_dir)

    print(f"Loaded traces for {len(traces)} tasks from {args.traces_dir}")

    metrics = compute_discovery_metrics(traces, task_gold)
    agg = metrics["aggregate"]

    if not agg:
        print("No metrics computed (check task gold IDs and trace files).")
        return

    print(f"\nAggregate Discovery Metrics (n={agg['n']}):")
    print(f"  D_ret (retrieval coverage): {agg['D_ret']:.3f}")
    print(f"  D_acc (answer attribution):  {agg['D_acc']:.3f}")
    print(f"  Avg Precision:               {agg['avg_precision']:.3f}")
    print(f"  Avg Recall:                  {agg['avg_recall']:.3f}")
    print(f"  Avg F1:                      {agg['avg_f1']:.3f}")
    print(f"  Avg Search Calls/Task:       {agg['avg_search_calls']:.1f}")


if __name__ == "__main__":
    main()
