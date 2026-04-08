#!/usr/bin/env python3
"""
Compute discovery metrics D_ret, D_acc, precision/recall/F1 from trace JSONL files.

D_ret: retrieval gold coverage per task = |retrieved_gold ∩ gold| / |gold|
D_acc: access gold recall per task = |read_gold ∩ gold| / |gold|

Usage:
    python analysis/discovery_metrics.py [--traces-dir results/traces] [--tasks-dir tasks_mini]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

_READ_TOOLS = {"read_file", "grep_file", "query_file"}


def make_task_stem_key(task_id: str) -> str:
    """Return the normalized "{task_dir}/{task_name}" key used across analyses."""
    p = Path(str(task_id))
    return f"{p.parent.name}/{p.stem}"


def make_condition_model_task_key(condition: str, model: str, task_id: str) -> str:
    """Return a stable composite key for multi-run joins."""
    return f"{condition}/{model}/{make_task_stem_key(task_id)}"


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


def load_traces_with_context(traces_dir: str) -> dict[str, list]:
    """Load trace JSONLs keyed by "{condition}/{model}/{task_dir}/{task_name}"."""
    traces: dict = defaultdict(list)
    for jsonl_path in Path(traces_dir).rglob("*.jsonl"):
        parts = jsonl_path.parts
        if len(parts) < 4:
            continue
        condition = parts[-4]
        model = parts[-3]
        task_key = f"{jsonl_path.parent.name}/{jsonl_path.stem}"
        composite_key = f"{condition}/{model}/{task_key}"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    traces[composite_key].append(json.loads(line))
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

        # Separate search traces from read traces and submit_answer record
        search_traces = [t for t in task_traces if t.get("tool") not in _READ_TOOLS and t.get("tool") != "submit_answer"]
        submit_record = next((t for t in task_traces if t.get("tool") == "submit_answer"), None)

        # D_ret coverage: how much of the gold set was retrieved by search results?
        # Also keep hit/precision-style companions:
        # - d_ret_hit: was any gold retrieved at all? (legacy binary)
        # - d_ret_precision: how much of retrieved set is gold? (mentor's "7/70 vs 7/10")
        all_result_ids: set = set()
        all_result_ids_total_count = 0
        for trace in search_traces:
            result_ids = trace.get("result_dataset_ids", [])
            all_result_ids.update(result_ids)
            all_result_ids_total_count += len(result_ids)

        retrieved_gold = all_result_ids & gold_ids
        d_ret = len(retrieved_gold) / len(gold_ids) if gold_ids else 0.0
        d_ret_hit = int(bool(retrieved_gold))
        d_ret_precision = len(retrieved_gold) / len(all_result_ids) if all_result_ids else 0.0
        d_ret_f1 = (
            2 * d_ret_precision * d_ret / (d_ret_precision + d_ret)
            if (d_ret_precision + d_ret) > 0
            else 0.0
        )

        # Precision / Recall: per-call average (standard IR)
        # Compute P/R for each individual search call, then average across calls.
        call_precisions = []
        call_recalls = []
        for trace in search_traces:
            result_ids = trace.get("result_dataset_ids", [])
            if not result_ids:
                continue
            hits = len(set(result_ids) & gold_ids)
            call_precisions.append(hits / len(result_ids))
            call_recalls.append(hits / len(gold_ids))
        precision = sum(call_precisions) / len(call_precisions) if call_precisions else 0.0
        recall = sum(call_recalls) / len(call_recalls) if call_recalls else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        # D_acc read metrics:
        # - d_acc_recall (legacy D_acc): how much of the gold set was accessed
        # - d_acc_precision: how much of accessed set is gold
        # - d_acc_f1: harmonic mean of read precision/recall
        read_records = [t for t in task_traces if t.get("tool") in _READ_TOOLS]
        all_read_ids: set = set()
        for rec in read_records:
            all_read_ids.update(rec.get("read_dataset_ids", []))
        read_gold = all_read_ids & gold_ids
        d_acc = len(read_gold) / len(gold_ids) if gold_ids else 0.0
        d_acc_precision = len(read_gold) / len(all_read_ids) if all_read_ids else 0.0
        d_acc_recall = d_acc
        d_acc_f1 = (
            2 * d_acc_precision * d_acc_recall / (d_acc_precision + d_acc_recall)
            if (d_acc_precision + d_acc_recall) > 0
            else 0.0
        )

        task_metrics.append({
            "task_id": task_id,
            "gold_ids": sorted(gold_ids),
            "retrieved_dataset_ids": sorted(all_result_ids),
            "retrieved_gold_dataset_ids": sorted(retrieved_gold),
            "d_ret": d_ret,
            "d_ret_hit": d_ret_hit,
            "d_ret_precision": d_ret_precision,
            "d_ret_f1": d_ret_f1,
            "d_acc": d_acc,
            "d_acc_precision": d_acc_precision,
            "d_acc_recall": d_acc_recall,
            "d_acc_f1": d_acc_f1,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "num_search_calls": len(search_traces),
            "num_results_total": len(all_result_ids),
            "num_results_total_non_unique": all_result_ids_total_count,
            "num_read_calls": len(read_records),
        })

    n = len(task_metrics)
    if n == 0:
        return {"task_metrics": [], "aggregate": {}}

    agg = {
        "n": n,
        "D_ret": sum(m["d_ret"] for m in task_metrics) / n,
        "D_ret_hit_rate": sum(m["d_ret_hit"] for m in task_metrics) / n,
        "D_ret_precision": sum(m["d_ret_precision"] for m in task_metrics) / n,
        "D_ret_f1": sum(m["d_ret_f1"] for m in task_metrics) / n,
        "D_acc": sum(m["d_acc"] for m in task_metrics) / n,
        "D_acc_precision": sum(m["d_acc_precision"] for m in task_metrics) / n,
        "D_acc_recall": sum(m["d_acc_recall"] for m in task_metrics) / n,
        "D_acc_f1": sum(m["d_acc_f1"] for m in task_metrics) / n,
        "avg_precision": sum(m["precision"] for m in task_metrics) / n,
        "avg_recall": sum(m["recall"] for m in task_metrics) / n,
        "avg_f1": sum(m["f1"] for m in task_metrics) / n,
        "avg_search_calls": sum(m["num_search_calls"] for m in task_metrics) / n,
        "avg_read_calls": sum(m["num_read_calls"] for m in task_metrics) / n,
    }

    return {"task_metrics": task_metrics, "aggregate": agg}


def _resolve_gold(task_id: str, task_gold: dict[str, list]) -> list:
    """Match a trace task_id ("k-2-d-1/task_1") to a gold entry."""
    if task_id.count("/") >= 3:
        task_id = "/".join(task_id.split("/")[-2:])
    # Exact match
    if task_id in task_gold:
        return task_gold[task_id]
    # Match on "{parent.name}/{stem}" from full path keys
    for path_key in task_gold:
        p = Path(path_key)
        if make_task_stem_key(path_key) == task_id:
            return task_gold[path_key]
    return []


def compute_per_folder_discovery(
    traces: dict[str, list],
    task_gold: dict[str, list],
) -> dict:
    """Group traces by task-dir prefix and compute discovery metrics per folder.

    Returns {folder_name: aggregate_dict} where aggregate_dict is the same shape
    as compute_discovery_metrics()['aggregate'] (no task_metrics key).
    """
    from collections import defaultdict

    folder_traces: dict = defaultdict(dict)
    for task_id, recs in traces.items():
        folder = task_id.split("/")[0]
        folder_traces[folder][task_id] = recs

    out = {}
    for folder, subset in sorted(folder_traces.items()):
        result = compute_discovery_metrics(subset, task_gold)
        out[folder] = result["aggregate"]
    return out


def compute_tools_discovery(
    traces: dict[str, list],
    task_gold: dict[str, list],
) -> dict:
    """Per-tool micro-averaged precision/recall/F1 with per_folder > per_task nesting.

    For each task × tool:
    For each task × tool, per-call average (standard IR):
      - precision per call = |gold in call results| / |call results|
      - recall per call    = |gold in call results| / |gold for task|
      - task precision/recall = mean over all calls for that tool in that task
      - f1        = harmonic mean

    per_folder averages the per_task values within that folder.
    Top-level averages all per_task values across all folders.

    Returns {tool_name: {avg_precision, avg_recall, avg_f1, calls, tasks_with_hit,
                         n_tasks, per_folder: {folder: {... per_task: {task_id: {...}}}}}}
    """
    from collections import defaultdict

    # tool -> task_id -> list of per-call (precision, recall) + call count
    tool_task: dict = defaultdict(lambda: defaultdict(lambda: {
        "call_precisions": [],
        "call_recalls": [],
        "calls": 0,
    }))

    for task_id, task_traces in traces.items():
        gold_ids = set(_resolve_gold(task_id, task_gold))
        if not gold_ids:
            continue
        for rec in task_traces:
            tool = rec.get("tool")
            if not tool or tool == "submit_answer" or tool in _READ_TOOLS:
                continue
            result_ids = rec.get("result_dataset_ids", [])
            if not result_ids:
                continue
            hits = len(set(result_ids) & gold_ids)
            s = tool_task[tool][task_id]
            s["call_precisions"].append(hits / len(result_ids))
            s["call_recalls"].append(hits / len(gold_ids))
            s["calls"] += 1

    out = {}
    for tool, task_map in tool_task.items():
        # Build per_task records grouped by folder
        folder_tasks: dict = defaultdict(dict)
        for task_id, s in task_map.items():
            folder = task_id.split("/")[0]
            cp, cr = s["call_precisions"], s["call_recalls"]
            precision = sum(cp) / len(cp) if cp else 0.0
            recall = sum(cr) / len(cr) if cr else 0.0
            f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
            folder_tasks[folder][task_id] = {
                "calls": s["calls"],
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "has_hit": int(recall > 0),
            }

        # Build per_folder aggregates
        per_folder = {}
        all_task_records = []
        for folder, tasks in sorted(folder_tasks.items()):
            task_vals = list(tasks.values())
            all_task_records.extend(task_vals)
            n = len(task_vals)
            folder_calls = sum(t["calls"] for t in task_vals)
            folder_hits = sum(t["has_hit"] for t in task_vals)
            per_folder[folder] = {
                "n_tasks": n,
                "calls": folder_calls,
                "avg_precision": round(sum(t["precision"] for t in task_vals) / n, 4),
                "avg_recall": round(sum(t["recall"] for t in task_vals) / n, 4),
                "avg_f1": round(sum(t["f1"] for t in task_vals) / n, 4),
                "tasks_with_hit": folder_hits,
                "per_task": tasks,
            }

        # Top-level aggregate over all tasks
        n_all = len(all_task_records)
        total_calls = sum(t["calls"] for t in all_task_records)
        tasks_with_hit = sum(t["has_hit"] for t in all_task_records)
        out[tool] = {
            "calls": total_calls,
            "n_tasks": n_all,
            "tasks_with_hit": tasks_with_hit,
            "avg_precision": round(sum(t["precision"] for t in all_task_records) / n_all, 4) if n_all else 0.0,
            "avg_recall": round(sum(t["recall"] for t in all_task_records) / n_all, 4) if n_all else 0.0,
            "avg_f1": round(sum(t["f1"] for t in all_task_records) / n_all, 4) if n_all else 0.0,
            "per_folder": per_folder,
        }

    return out


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
    print(f"  D_ret F1:                   {agg['D_ret_f1']:.3f}")
    print(f"  D_acc (read recall):         {agg['D_acc']:.3f}")
    print(f"  D_acc precision:             {agg['D_acc_precision']:.3f}")
    print(f"  D_acc recall:                {agg['D_acc_recall']:.3f}")
    print(f"  D_acc F1:                    {agg['D_acc_f1']:.3f}")
    print(f"  Search avg precision:        {agg['avg_precision']:.3f}")
    print(f"  Search avg recall:           {agg['avg_recall']:.3f}")
    print(f"  Search avg F1:               {agg['avg_f1']:.3f}")
    print(f"  Avg Search Calls/Task:       {agg['avg_search_calls']:.1f}")
    print(f"  Avg Read Calls/Task:         {agg['avg_read_calls']:.1f}")


if __name__ == "__main__":
    main()
