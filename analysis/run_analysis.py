#!/usr/bin/env python3
"""
Unified analysis runner. Collects all metrics and writes to analysis_results/.

Output files:
  analysis_results/em_f1.json          — EM/F1 per condition × model
  analysis_results/discovery.json      — D_ret, D_acc, precision/recall per condition × model
  analysis_results/failure.json        — failure attribution per condition × model
  analysis_results/efficiency.json     — cost/runtime/tool-call distributions
  analysis_results/provenance.json     — Condition A backend first-hit attribution
  analysis_results/summary.json        — flat table of key metrics for all conditions

Usage:
    python analysis/run_analysis.py [--results-dir results] [--traces-dir results/traces] [--tasks-dir tasks_mini]
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.compute_em import load_results, compute_stats
from analysis.discovery_metrics import (
    load_traces,
    load_task_gold_ids,
    compute_discovery_metrics,
    compute_per_folder_discovery,
    compute_tools_discovery,
)
from analysis.failure_attribution import classify_failure
from analysis.provenance import compute_provenance


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _condition_model_from_path(jsonl_path: Path) -> tuple[str, str]:
    parts = jsonl_path.parts
    condition = parts[-3] if len(parts) >= 3 else "unknown"
    model = parts[-2] if len(parts) >= 2 else "unknown"
    return condition, model


def _percentile(vals: list, p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    return s[min(int(len(s) * p / 100), len(s) - 1)]


def _dist(vals: list) -> dict:
    if not vals:
        return {}
    n = len(vals)
    return {
        "mean": sum(vals) / n,
        "p50": _percentile(vals, 50),
        "p90": _percentile(vals, 90),
        "n": n,
    }


# ---------------------------------------------------------------------------
# EM / F1
# ---------------------------------------------------------------------------

def run_em(results_dir: str) -> dict:
    records = load_results(results_dir)
    table = compute_stats(records)
    return {f"{cond}/{model}": v for (cond, model), v in table.items()}


# ---------------------------------------------------------------------------
# Discovery metrics — per condition × model
# ---------------------------------------------------------------------------

def run_discovery(traces_dir: str, tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    traces_root = Path(traces_dir)

    # Iterate condition/model subdirs
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        for model_dir in sorted(condition_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            traces = load_traces(str(model_dir))
            if not traces:
                continue
            metrics = compute_discovery_metrics(traces, task_gold)
            key = f"{condition_dir.name}/{model_dir.name}"
            out[key] = metrics["aggregate"]
            out[key]["task_metrics"] = metrics["task_metrics"]
            out[key]["per_folder"] = compute_per_folder_discovery(traces, task_gold)
    return out


# ---------------------------------------------------------------------------
# Failure attribution — per condition × model
# ---------------------------------------------------------------------------

def run_failure(results_dir: str, traces_dir: str, tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    traces_root = Path(traces_dir)

    # Build agent_results lookup: "{condition}/{model}" -> {k-x-d-x/task_x -> result}
    agent_results_by_cm: dict = defaultdict(dict)
    for jsonl_path in Path(results_dir).rglob("agent_results.jsonl"):
        condition, model = _condition_model_from_path(jsonl_path)
        key = f"{condition}/{model}"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                task_id = str(r.get("task_id", ""))
                if task_id:
                    p = Path(task_id)
                    agent_results_by_cm[key][f"{p.parent.name}/{p.stem}"] = r

    out = {}
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        for model_dir in sorted(condition_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            key = f"{condition_dir.name}/{model_dir.name}"
            traces = load_traces(str(model_dir))
            if not traces:
                continue
            metrics = compute_discovery_metrics(traces, task_gold)
            ar = agent_results_by_cm.get(key, {})
            counts: Counter = Counter()
            for m in metrics["task_metrics"]:
                result = ar.get(m["task_id"], {})
                label = classify_failure(result, m["d_ret"], m["d_acc"])
                counts[label] += 1
            total = sum(counts.values())
            out[key] = {
                label: {"n": counts.get(label, 0), "pct": round(100 * counts.get(label, 0) / total, 1) if total else 0}
                for label in ["correct", "search", "discovery-reason", "execution", "hallucination"]
            }
            out[key]["total"] = total
    return out


# ---------------------------------------------------------------------------
# Efficiency
# ---------------------------------------------------------------------------

def run_efficiency(results_dir: str) -> dict:
    by_cm: dict = defaultdict(list)
    for jsonl_path in Path(results_dir).rglob("agent_results.jsonl"):
        condition, model = _condition_model_from_path(jsonl_path)
        key = f"{condition}/{model}"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                by_cm[key].append(json.loads(line))

    out = {}
    for key, rows in sorted(by_cm.items()):
        out[key] = {
            "cost_usd": _dist([r.get("cost_usd", 0.0) for r in rows]),
            "time_s": _dist([r.get("time", 0.0) for r in rows]),
            "tool_calls": _dist([r.get("tool_calls_total", 0) for r in rows]),
            "total_cost_usd": sum(r.get("cost_usd", 0.0) for r in rows),
            "n": len(rows),
        }
    return out


# ---------------------------------------------------------------------------
# Provenance (Condition A)
# ---------------------------------------------------------------------------

def run_provenance(traces_dir: str, tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    traces_root = Path(traces_dir)
    out = {}
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir() or condition_dir.name != "a":
            continue
        for model_dir in sorted(condition_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            traces = load_traces(str(model_dir))
            if not traces:
                continue
            key = f"{condition_dir.name}/{model_dir.name}"
            out[key] = compute_provenance(traces, task_gold)
    return out


# ---------------------------------------------------------------------------
# Tools discovery
# ---------------------------------------------------------------------------

def run_tools_discovery(traces_dir: str, tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    traces_root = Path(traces_dir)
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        for model_dir in sorted(condition_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            traces = load_traces(str(model_dir))
            if not traces:
                continue
            key = f"{condition_dir.name}/{model_dir.name}"
            out[key] = compute_tools_discovery(traces, task_gold)
    return out


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def build_summary(em: dict, discovery: dict, failure: dict, efficiency: dict) -> list[dict]:
    keys = sorted(set(list(em.keys()) + list(discovery.keys()) + list(failure.keys())))
    rows = []
    for key in keys:
        parts = key.split("/", 1) if "/" in key else [key, ""]
        row = {"condition_model": key, "condition": parts[0], "model": parts[1]}
        if key in em:
            e = em[key]
            row["n"] = e.get("n")
            row["em"] = round(e.get("em", 0) or 0, 3)
            row["f1"] = round(e.get("f1", 0) or 0, 3)
            row["avg_cost_usd"] = round(e.get("avg_cost_usd", 0), 4)
            row["avg_tool_calls"] = round(e.get("avg_tool_calls", 0), 1)
        if key in discovery:
            d = discovery[key]
            row["D_ret"] = round(d.get("D_ret", 0), 3)
            row["D_acc"] = round(d.get("D_acc", 0), 3)
            row["avg_recall"] = round(d.get("avg_recall", 0), 3)
            row["avg_precision"] = round(d.get("avg_precision", 0), 3)
        if key in failure:
            f = failure[key]
            row["pct_correct"] = f.get("correct", {}).get("pct")
            row["pct_search_fail"] = f.get("search", {}).get("pct")
            row["pct_discovery_reason"] = f.get("discovery-reason", {}).get("pct")
            row["pct_execution"] = f.get("execution", {}).get("pct")
            row["pct_hallucination"] = f.get("hallucination", {}).get("pct")
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    print("Running EM/F1...")
    em = run_em(args.results_dir)

    print("Running discovery metrics...")
    discovery = run_discovery(args.traces_dir, args.tasks_dir)

    print("Running failure attribution...")
    failure = run_failure(args.results_dir, args.traces_dir, args.tasks_dir)

    print("Running efficiency...")
    efficiency = run_efficiency(args.results_dir)

    print("Running provenance (Condition A)...")
    provenance = run_provenance(args.traces_dir, args.tasks_dir)

    print("Running tools discovery...")
    tools_discovery = run_tools_discovery(args.traces_dir, args.tasks_dir)

    print("Building summary...")
    summary = build_summary(em, discovery, failure, efficiency)

    files = {
        "em_f1.json": em,
        "discovery.json": {k: {kk: vv for kk, vv in v.items() if kk != "task_metrics"} for k, v in discovery.items()},
        "tools_discovery.json": tools_discovery,
        "failure.json": failure,
        "efficiency.json": efficiency,
        "provenance.json": provenance,
        "summary.json": summary,
    }

    for fname, data in files.items():
        path = out_dir / fname
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Wrote {path}")

    print(f"\nSummary ({len(summary)} condition×model rows):")
    for row in summary:
        em_pct = f"{row.get('em', 0)*100:.1f}%" if row.get('em') is not None else "N/A"
        d_ret = f"{row.get('D_ret', 0):.2f}" if row.get('D_ret') is not None else "N/A"
        print(f"  {row['condition_model']:<55} EM={em_pct}  D_ret={d_ret}  correct={row.get('pct_correct')}%")


if __name__ == "__main__":
    main()
