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
from analysis.failure_attribution import classify_failure, _LABEL_ORDER
from analysis.provenance import compute_provenance
from analysis.search_depth import compute_search_depth_curve
from analysis.planning_overhead import compute_planning_overhead
from analysis.reasoning_density import compute_reasoning_density_curve, load_task_gold_counts
from analysis.tool_error_analysis import compute_tool_error_rates
from analysis.generate_figures import main as generate_figs


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


def _as_float(value) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _total_cost_with_ideal_subagents(record: dict) -> float:
    explicit = record.get("total_cost_with_ideal_subagents_usd")
    if explicit not in (None, ""):
        return _as_float(explicit)
    return _as_float(record.get("cost_usd")) + _as_float(record.get("ideal_subagent_cost_usd"))


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
                label = classify_failure(
                    result,
                    m["d_ret"],
                    m["d_acc"],
                    num_read_calls=m.get("num_read_calls", 0),
                )
                counts[label] += 1
            total = sum(counts.values())
            out[key] = {
                label: {"n": counts.get(label, 0), "pct": round(100 * counts.get(label, 0) / total, 1) if total else 0}
                for label in _LABEL_ORDER
            }
            out[key]["total"] = total
    return out


# ---------------------------------------------------------------------------
# Search depth curve
# ---------------------------------------------------------------------------

def run_search_depth(results_dir: str) -> dict:
    records = load_results(results_dir)
    return compute_search_depth_curve(records)


# ---------------------------------------------------------------------------
# Planning overhead (Condition B)
# ---------------------------------------------------------------------------

def run_planning_overhead(results_dir: str) -> dict:
    records = load_results(results_dir)
    return compute_planning_overhead(records)


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
        main_costs = [_as_float(r.get("cost_usd")) for r in rows]
        ideal_subagent_costs = [_as_float(r.get("ideal_subagent_cost_usd")) for r in rows]
        combined_costs = [_total_cost_with_ideal_subagents(r) for r in rows]
        out[key] = {
            "cost_usd": _dist(main_costs),
            "ideal_subagent_cost_usd": _dist(ideal_subagent_costs),
            "total_cost_with_ideal_subagents_usd": _dist(combined_costs),
            "time_s": _dist([r.get("time", 0.0) for r in rows]),
            "tool_calls": _dist([r.get("tool_calls_total", 0) for r in rows]),
            "total_cost_usd": sum(main_costs),
            "total_ideal_subagent_cost_usd": sum(ideal_subagent_costs),
            "total_cost_with_ideal_subagents_sum_usd": sum(combined_costs),
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
# Tool error rates
# ---------------------------------------------------------------------------

def run_tool_errors(results_dir: str) -> dict:
    """Compute tool error rates keyed by path-derived condition/model (same as summary keys)."""
    by_cm: dict = defaultdict(list)
    for jsonl_path in Path(results_dir).rglob("agent_results.jsonl"):
        condition, model = _condition_model_from_path(jsonl_path)
        key = f"{condition}/{model}"
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                r["_cm_key"] = key  # inject path-derived key
                by_cm[key].append(r)

    # Patch records so compute_tool_error_rates can group by _cm_key
    from analysis.tool_error_analysis import _DATA_TOOLS
    from collections import defaultdict as _dd
    acc: dict = _dd(lambda: _dd(lambda: [0, 0]))
    for key, rows in by_cm.items():
        for r in rows:
            for tc in r.get("tool_counts", []):
                name = tc.get("name", "")
                calls = tc.get("call_count", 0)
                successes = tc.get("success_count", 0)
                if calls == 0:
                    continue
                errors = max(calls - successes, 0)
                acc[key][name][0] += calls
                acc[key][name][1] += errors

    out = {}
    for key, tools in sorted(acc.items()):
        out[key] = {}
        for tool_name, (total_calls, total_errors) in sorted(tools.items()):
            out[key][tool_name] = {
                "total_calls": total_calls,
                "total_errors": total_errors,
                "error_rate": round(total_errors / total_calls, 4) if total_calls else 0.0,
            }
    return out


# ---------------------------------------------------------------------------
# Reasoning density curve (EM by gold-doc count — reproduces LakeQA Fig 4)
# ---------------------------------------------------------------------------

def run_reasoning_density(results_dir: str, tasks_dir: str) -> dict:
    records = load_results(results_dir)
    task_gold_counts = load_task_gold_counts(tasks_dir)
    return compute_reasoning_density_curve(records, task_gold_counts)


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def build_summary(em: dict, discovery: dict, failure: dict, efficiency: dict, search_depth: dict | None = None, reasoning_density: dict | None = None, tool_errors: dict | None = None) -> list[dict]:
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
            row["total_cost_usd"] = round(e.get("total_cost_usd", 0), 4)
            row["avg_ideal_subagent_cost_usd"] = round(e.get("avg_ideal_subagent_cost_usd", 0), 4)
            row["total_ideal_subagent_cost_usd"] = round(e.get("total_ideal_subagent_cost_usd", 0), 4)
            row["avg_total_cost_with_ideal_subagents_usd"] = round(
                e.get("avg_total_cost_with_ideal_subagents_usd", 0), 4
            )
            row["total_cost_with_ideal_subagents_usd"] = round(
                e.get("total_cost_with_ideal_subagents_usd", 0), 4
            )
            row["avg_tool_calls"] = round(e.get("avg_tool_calls", 0), 1)
            row["avg_search_calls"] = round(e.get("avg_search_calls", 0), 1)
            row["avg_query_file_calls"] = round(e.get("avg_query_file_calls", 0), 1)
            row["avg_execute_code_calls"] = round(e.get("avg_execute_code_calls", 0), 1)
            avg_sc = e.get("avg_search_calls") or 0
            em_val = e.get("em") or 0
            row["search_efficiency"] = round(em_val / avg_sc, 4) if avg_sc else None
        if key in discovery:
            d = discovery[key]
            row["D_ret"] = round(d.get("D_ret", 0), 3)
            row["D_acc"] = round(d.get("D_acc", 0), 3)
            row["exploration_gap"] = round(d.get("D_ret", 0) - d.get("D_acc", 0), 3)
            # Read/access quality (D_acc family)
            row["dacc_precision"] = round(d.get("D_acc_precision", 0), 3)
            row["dacc_recall"] = round(d.get("D_acc_recall", d.get("D_acc", 0)), 3)
            row["dacc_f1"] = round(d.get("D_acc_f1", 0), 3)
            # Search-call quality (legacy metrics, renamed for clarity)
            row["search_avg_precision"] = round(d.get("avg_precision", 0), 3)
            row["search_avg_recall"] = round(d.get("avg_recall", 0), 3)
            row["search_avg_f1"] = round(d.get("avg_f1", 0), 3)
            # Back-compat aliases used by older notebooks/scripts.
            row["dacc_avg_precision"] = row["dacc_precision"]
            row["dacc_avg_recall"] = row["dacc_recall"]
        if key in failure:
            f = failure[key]
            row["pct_em1_dacc_ge_0_8"] = f.get("em1_dacc_ge_0_8", {}).get("pct")
            row["pct_em1_dacc_0_5_to_0_8"] = f.get("em1_dacc_0_5_to_0_8", {}).get("pct")
            row["pct_em1_dacc_0_2_to_0_5"] = f.get("em1_dacc_0_2_to_0_5", {}).get("pct")
            row["pct_em1_dacc_lt_0_2"] = f.get("em1_dacc_lt_0_2", {}).get("pct")
            row["pct_em0_dacc_ge_0_8"] = f.get("em0_dacc_ge_0_8", {}).get("pct")
            row["pct_em0_dacc_0_5_to_0_8"] = f.get("em0_dacc_0_5_to_0_8", {}).get("pct")
            row["pct_em0_dacc_0_2_to_0_5"] = f.get("em0_dacc_0_2_to_0_5", {}).get("pct")
            row["pct_em0_dacc_lt_0_2"] = f.get("em0_dacc_lt_0_2", {}).get("pct")
        if tool_errors is not None and key in tool_errors:
            te = tool_errors[key]
            for tool_name in ("query_file", "execute_code", "peek_file"):
                col = f"{tool_name}_error_rate"
                row[col] = te.get(tool_name, {}).get("error_rate")
        if search_depth is not None:
            cond = parts[0]
            depth = search_depth.get(cond, {})
            for bin_label in ("1", "2-3", "4-6", "7-10", "11-30"):
                safe = bin_label.replace("-", "_")
                entry = depth.get(bin_label, {})
                row[f"depth_{safe}_em"] = entry.get("mean_em")
                row[f"depth_{safe}_n"] = entry.get("n")
        if reasoning_density is not None:
            cond = parts[0]
            rdensity = reasoning_density.get(cond, {})
            for bin_label in ("<=2", "3-4", "5-7", "8-10", ">10"):
                safe = bin_label.replace("<", "lte").replace(">", "gt").replace("-", "_")
                entry = rdensity.get(bin_label, {})
                row[f"rdensity_{safe}_em"] = entry.get("mean_em")
                row[f"rdensity_{safe}_n"] = entry.get("n")
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
    parser.add_argument(
        "--model-filter",
        default=None,
        help="Substring filter on model name (comma-separated OR). e.g. 'haiku,sonnet'.",
    )
    args = parser.parse_args()

    model_filters = [s.strip().lower() for s in args.model_filter.split(",")] if args.model_filter else None

    def _keep_model(name: str) -> bool:
        if not model_filters:
            return True
        n = (name or "").lower()
        return any(f in n for f in model_filters)


    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    def _filter_cm_dict(d: dict) -> dict:
        if not model_filters:
            return d
        return {k: v for k, v in d.items() if _keep_model(k.split("/", 1)[-1])}

    print("Running EM/F1...")
    em = _filter_cm_dict(run_em(args.results_dir))

    print("Running discovery metrics...")
    discovery = _filter_cm_dict(run_discovery(args.traces_dir, args.tasks_dir))

    print("Running failure attribution...")
    failure = _filter_cm_dict(run_failure(args.results_dir, args.traces_dir, args.tasks_dir))

    print("Running efficiency...")
    efficiency = _filter_cm_dict(run_efficiency(args.results_dir))

    print("Running provenance (Condition A)...")
    provenance = _filter_cm_dict(run_provenance(args.traces_dir, args.tasks_dir))

    print("Running tools discovery...")
    tools_discovery = _filter_cm_dict(run_tools_discovery(args.traces_dir, args.tasks_dir))

    print("Running search depth curve...")
    search_depth = run_search_depth(args.results_dir)  # keyed by condition only

    print("Running planning overhead (Condition B)...")
    planning_overhead = run_planning_overhead(args.results_dir)

    print("Running reasoning density curve (LakeQA Fig 4)...")
    reasoning_density = run_reasoning_density(args.results_dir, args.tasks_dir)

    print("Running tool error rates...")
    tool_errors = _filter_cm_dict(run_tool_errors(args.results_dir))

    print("Building summary...")
    summary = build_summary(em, discovery, failure, efficiency, search_depth, reasoning_density, tool_errors)

    files = {
        "em_f1.json": em,
        "discovery.json": {k: {kk: vv for kk, vv in v.items() if kk != "task_metrics"} for k, v in discovery.items()},
        "tools_discovery.json": tools_discovery,
        "failure.json": failure,
        "efficiency.json": efficiency,
        "provenance.json": provenance,
        "search_depth.json": search_depth,
        "planning_overhead.json": planning_overhead,
        "reasoning_density.json": reasoning_density,
        "tool_errors.json": tool_errors,
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
        em1_hi = row.get("pct_em1_dacc_ge_0_8")
        print(f"  {row['condition_model']:<55} EM={em_pct}  D_ret={d_ret}  em1_dacc_ge_0_8={em1_hi}%")

    print("Generating figures...")
    if model_filters:
        old_argv = sys.argv
        sys.argv = [old_argv[0], "--model-filter", args.model_filter]
        try:
            generate_figs()
        finally:
            sys.argv = old_argv
    else:
        generate_figs()


if __name__ == "__main__":
    main()
