#!/usr/bin/env python3
"""
Compute discovery metrics D_ret, D_acc, precision/recall/F1 from sidecar traces.

D_ret: fraction of tasks where at least one gold dataset appeared in any search result
D_acc: fraction of tasks where the agent used (cited) a gold dataset in its answer sources

Usage:
    python analysis/discovery_metrics.py [--sidecar-dir results/sidecar] [--results-dir results]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_sidecar_traces(sidecar_dir: str) -> dict[str, list]:
    """Load all sidecar JSONL files. Returns {task_id: [trace_records]}."""
    traces: dict = defaultdict(list)
    for jsonl_path in Path(sidecar_dir).rglob("*.jsonl"):
        task_id = jsonl_path.stem
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    traces[task_id].append(json.loads(line))
    return dict(traces)


def load_agent_results(results_dir: str) -> dict[str, dict]:
    """Load agent_results.jsonl. Returns {task_id: result_record}."""
    results: dict = {}
    for jsonl_path in Path(results_dir).rglob("agent_results.jsonl"):
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                task_id = str(r.get("task_id", ""))
                if task_id:
                    results[task_id] = r
    return results


def compute_discovery_metrics(
    traces: dict[str, list],
    agent_results: dict[str, dict],
    task_gold: dict[str, list],
) -> dict:
    """Compute per-task and aggregate discovery metrics."""
    task_metrics: list = []

    all_task_ids = set(traces) | set(agent_results)
    for task_id in all_task_ids:
        gold_ids = set(task_gold.get(task_id, []))
        if not gold_ids:
            continue

        # D_ret: did any search result contain a gold dataset?
        task_traces = traces.get(task_id, [])
        all_result_ids: set = set()
        for trace in task_traces:
            all_result_ids.update(trace.get("result_dataset_ids", []))

        retrieved_gold = all_result_ids & gold_ids
        d_ret = int(bool(retrieved_gold))

        # Precision / Recall over all search results
        precision = len(retrieved_gold) / len(all_result_ids) if all_result_ids else 0.0
        recall = len(retrieved_gold) / len(gold_ids) if gold_ids else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        # D_acc: did the agent cite a gold dataset in its answer?
        agent_result = agent_results.get(task_id, {})
        sources_used = agent_result.get("sources_used", [])
        cited_ids = set()
        for s in sources_used:
            # Normalize: strip prefix, take first component
            s = str(s)
            if "lakeqa-yc4103-datalake/" in s:
                s = s.split("lakeqa-yc4103-datalake/")[-1]
            cited_ids.add(s.split("/")[0])
        d_acc = int(bool(cited_ids & gold_ids))

        task_metrics.append({
            "task_id": task_id,
            "gold_ids": list(gold_ids),
            "d_ret": d_ret,
            "d_acc": d_acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "num_search_calls": len(task_traces),
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


def load_task_gold_ids(tasks_dir: str) -> dict[str, list]:
    """Load gold dataset IDs from task files. Returns {task_id: [dataset_id]}."""
    import glob as glob_mod
    gold: dict = {}
    for path in glob_mod.glob(str(Path(tasks_dir) / "**" / "*.json"), recursive=True):
        with open(path) as f:
            task = json.load(f)
        task_id = path  # matches agent.py task["id"] = path
        gold[task_id] = task.get("datasets_used", [])
    return gold


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sidecar-dir", default="results/sidecar")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    args = parser.parse_args()

    traces = load_sidecar_traces(args.sidecar_dir)
    agent_results = load_agent_results(args.results_dir)
    task_gold = load_task_gold_ids(args.tasks_dir)

    print(f"Loaded {len(traces)} sidecar traces, {len(agent_results)} agent results")

    metrics = compute_discovery_metrics(traces, agent_results, task_gold)
    agg = metrics["aggregate"]

    if not agg:
        print("No metrics computed (check task gold IDs and sidecar traces).")
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
