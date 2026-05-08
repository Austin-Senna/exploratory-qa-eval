#!/usr/bin/env python3
"""
Search-variant analysis runner.

This mirrors analysis/run_analysis.py but preserves the search-variant directory
layer used by run_search_eval:

  results/{variant}/{base_condition}/{model}/agent_results.jsonl
  results/traces/{variant}/{base_condition}/{model}/...

It also supports legacy layout:

  results/{condition}/{model}/agent_results.jsonl
  results/traces/{condition}/{model}/...

Output files (default: analysis_results_search/):
  em_f1.json
  discovery.json
  tools_discovery.json
  failure.json
  efficiency.json
  provenance.json
  search_depth.json
  planning_overhead.json
  reasoning_density.json
  tool_errors.json
  search_first_hit_condition.json
  search_first_hit_tool.json
  search_topk_miss_tool.json
  search_tool_efficiency.json
  summary.json
  variant_summary.json
  per_task_retrieval.csv
  per_task_search_bottleneck.csv
  per_task_search_tool_bottleneck.csv
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.compute_em import compute_stats
from analysis.discovery_metrics import (
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
from analysis.search_bottleneck import (
    SEARCH_BOTTLENECK_CUTOFFS,
    SEARCH_TOOL_COLORS,
    SEARCH_TOOL_ORDER,
    compute_search_bottleneck,
    generate_search_bottleneck_figures as _shared_generate_search_bottleneck_figures,
    write_search_bottleneck_csv as _shared_write_search_bottleneck_csv,
)


def _condition_label(variant: str, base_condition: str) -> str:
    return f"{variant}/{base_condition}"


def _cm_key(variant: str, base_condition: str, model: str) -> str:
    return f"{variant}/{base_condition}/{model}"


def _is_base_condition_b(base_condition: str) -> bool:
    return base_condition == "b" or base_condition.startswith("b_plan_")


def _split_cm_key(key: str) -> Tuple[str, str, str]:
    parts = key.split("/", 2)
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], parts[0], parts[1]
    if len(parts) == 1:
        return parts[0], parts[0], ""
    return "unknown", "unknown", key


def _task_stem(task_id: str) -> str:
    p = Path(str(task_id))
    return f"{p.parent.name}/{p.stem}"


def _parse_results_jsonl_path(path: Path, results_root: Path) -> Tuple[str, str, str]:
    rel = path.relative_to(results_root)
    parts = rel.parts
    # Search-ablation layout: {variant}/{base_condition}/{model}/agent_results.jsonl
    if len(parts) >= 4:
        return parts[-4], parts[-3], parts[-2]
    # Legacy layout: {condition}/{model}/agent_results.jsonl
    if len(parts) >= 3:
        return parts[-3], parts[-3], parts[-2]
    return "unknown", "unknown", "unknown"


def _parse_trace_jsonl_path(path: Path, traces_root: Path) -> Tuple[str, str, str, str]:
    rel = path.relative_to(traces_root)
    parts = rel.parts
    # Search-ablation layout: {variant}/{base_condition}/{model}/{task_dir}/{task}.jsonl
    if len(parts) >= 5:
        variant, base_condition, model = parts[-5], parts[-4], parts[-3]
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return variant, base_condition, model, task_id
    # Legacy layout: {condition}/{model}/{task_dir}/{task}.jsonl
    if len(parts) >= 4:
        variant, base_condition, model = parts[-4], parts[-4], parts[-3]
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return variant, base_condition, model, task_id
    return "unknown", "unknown", "unknown", "unknown/unknown"


def load_results_grouped(results_dir: str) -> Tuple[List[dict], Dict[str, List[dict]], Dict[str, dict]]:
    root = Path(results_dir)
    records: List[dict] = []
    by_key: Dict[str, List[dict]] = defaultdict(list)
    meta_by_key: Dict[str, dict] = {}

    for jsonl_path in root.rglob("agent_results.jsonl"):
        variant, base_condition, model = _parse_results_jsonl_path(jsonl_path, root)
        cond_label = _condition_label(variant, base_condition)
        key = _cm_key(variant, base_condition, model)
        meta_by_key[key] = {
            "variant": variant,
            "base_condition": base_condition,
            "condition_label": cond_label,
            "model": model,
        }
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                r["variant"] = variant
                r["base_condition"] = base_condition
                r["condition"] = cond_label
                r["model_label"] = model
                r["_cm_key"] = key
                records.append(r)
                by_key[key].append(r)

    return records, by_key, meta_by_key


def load_traces_grouped(traces_dir: str) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    root = Path(traces_dir)
    grouped: Dict[str, dict] = defaultdict(lambda: defaultdict(list))
    meta_by_key: Dict[str, dict] = {}

    for jsonl_path in root.rglob("*.jsonl"):
        variant, base_condition, model, task_id = _parse_trace_jsonl_path(jsonl_path, root)
        key = _cm_key(variant, base_condition, model)
        meta_by_key[key] = {
            "variant": variant,
            "base_condition": base_condition,
            "condition_label": _condition_label(variant, base_condition),
            "model": model,
        }
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    grouped[key][task_id].append(json.loads(line))

    return {k: dict(v) for k, v in grouped.items()}, meta_by_key


def run_em(records: List[dict]) -> dict:
    table = compute_stats(records)
    out = {}
    for (cond_label, model), vals in table.items():
        parts = cond_label.split("/", 1)
        variant = parts[0]
        base_condition = parts[1] if len(parts) == 2 else parts[0]
        key = _cm_key(variant, base_condition, model)
        row = dict(vals)
        row["variant"] = variant
        row["base_condition"] = base_condition
        row["condition_label"] = cond_label
        out[key] = row
    return out


def run_discovery(grouped_traces: Dict[str, dict], tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    for key, traces in sorted(grouped_traces.items()):
        metrics = compute_discovery_metrics(traces, task_gold)
        out[key] = metrics["aggregate"]
        out[key]["task_metrics"] = metrics["task_metrics"]
        out[key]["per_folder"] = compute_per_folder_discovery(traces, task_gold)
    return out


def run_failure(by_key_records: Dict[str, List[dict]], grouped_traces: Dict[str, dict], tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}

    agent_results_by_cm: Dict[str, dict] = defaultdict(dict)
    for key, rows in by_key_records.items():
        for r in rows:
            task_id = str(r.get("task_id", ""))
            if task_id:
                agent_results_by_cm[key][_task_stem(task_id)] = r

    for key, traces in sorted(grouped_traces.items()):
        metrics = compute_discovery_metrics(traces, task_gold)
        counts: Counter = Counter()
        ar = agent_results_by_cm.get(key, {})
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
            label: {
                "n": counts.get(label, 0),
                "pct": round(100 * counts.get(label, 0) / total, 1) if total else 0,
            }
            for label in _LABEL_ORDER
        }
        out[key]["total"] = total
    return out


def run_efficiency(by_key_records: Dict[str, List[dict]]) -> dict:
    def percentile(vals: list, p: float) -> float:
        if not vals:
            return 0.0
        s = sorted(vals)
        return s[min(int(len(s) * p / 100), len(s) - 1)]

    def dist(vals: list) -> dict:
        if not vals:
            return {}
        n = len(vals)
        return {
            "mean": sum(vals) / n,
            "p50": percentile(vals, 50),
            "p90": percentile(vals, 90),
            "n": n,
        }

    def as_float(value) -> float:
        try:
            return float(value or 0.0)
        except (TypeError, ValueError):
            return 0.0

    def total_with_ideal(row: dict) -> float:
        explicit = row.get("total_cost_with_ideal_subagents_usd")
        if explicit not in (None, ""):
            return as_float(explicit)
        return as_float(row.get("cost_usd")) + as_float(row.get("ideal_subagent_cost_usd"))

    out = {}
    for key, rows in sorted(by_key_records.items()):
        out[key] = {
            "cost_usd": dist([as_float(r.get("cost_usd")) for r in rows]),
            "ideal_subagent_cost_usd": dist([as_float(r.get("ideal_subagent_cost_usd")) for r in rows]),
            "total_cost_with_ideal_subagents_usd": dist([total_with_ideal(r) for r in rows]),
            "time_s": dist([r.get("time", 0.0) for r in rows]),
            "tool_calls": dist([r.get("tool_calls_total", 0) for r in rows]),
            "total_cost_usd": sum(as_float(r.get("cost_usd")) for r in rows),
            "total_ideal_subagent_cost_usd": sum(as_float(r.get("ideal_subagent_cost_usd")) for r in rows),
            "total_cost_with_ideal_subagents_sum_usd": sum(total_with_ideal(r) for r in rows),
            "n": len(rows),
        }
    return out


def run_provenance(grouped_traces: Dict[str, dict], tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    for key, traces in sorted(grouped_traces.items()):
        _, base_condition, _ = _split_cm_key(key)
        if base_condition != "a":
            continue
        out[key] = compute_provenance(traces, task_gold)
    return out


def run_tools_discovery(grouped_traces: Dict[str, dict], tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    for key, traces in sorted(grouped_traces.items()):
        out[key] = compute_tools_discovery(traces, task_gold)
    return out


def run_search_depth(records: List[dict]) -> dict:
    return compute_search_depth_curve(records)


def run_planning_overhead(records: List[dict]) -> dict:
    by_condition: Dict[str, List[dict]] = defaultdict(list)
    for r in records:
        by_condition[r.get("condition", "")].append(r)

    out = {}
    for cond_label, rows in sorted(by_condition.items()):
        parts = cond_label.split("/", 1)
        base_condition = parts[1] if len(parts) == 2 else cond_label
        if not _is_base_condition_b(base_condition):
            continue
        patched = [dict(r, condition="b") for r in rows]
        out[cond_label] = compute_planning_overhead(patched)
    return out


def run_reasoning_density(records: List[dict], tasks_dir: str) -> dict:
    task_gold_counts = load_task_gold_counts(tasks_dir)
    return compute_reasoning_density_curve(records, task_gold_counts)


def run_tool_errors(by_key_records: Dict[str, List[dict]]) -> dict:
    acc: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for key, rows in by_key_records.items():
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


def build_summary(
    em: dict,
    discovery: dict,
    failure: dict,
    efficiency: dict,
    search_depth: dict | None = None,
    reasoning_density: dict | None = None,
    tool_errors: dict | None = None,
    search_bottleneck: dict | None = None,
) -> list[dict]:
    keys = sorted(set(list(em.keys()) + list(discovery.keys()) + list(failure.keys())))
    rows = []
    for key in keys:
        variant, base_condition, model = _split_cm_key(key)
        condition_label = _condition_label(variant, base_condition)
        row = {
            "condition_model": key,
            "variant": variant,
            "base_condition": base_condition,
            "condition": condition_label,
            "model": model,
        }
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
                row[f"{tool_name}_error_rate"] = te.get(tool_name, {}).get("error_rate")
        if search_depth is not None:
            depth = search_depth.get(condition_label, {})
            for bin_label in ("1", "2-3", "4-6", "7-10", "11-30"):
                safe = bin_label.replace("-", "_")
                entry = depth.get(bin_label, {})
                row[f"depth_{safe}_em"] = entry.get("mean_em")
                row[f"depth_{safe}_n"] = entry.get("n")
        if reasoning_density is not None:
            rdensity = reasoning_density.get(condition_label, {})
            for bin_label in ("<=2", "3-4", "5-7", "8-10", ">10"):
                safe = bin_label.replace("<", "lte").replace(">", "gt").replace("-", "_")
                entry = rdensity.get(bin_label, {})
                row[f"rdensity_{safe}_em"] = entry.get("mean_em")
                row[f"rdensity_{safe}_n"] = entry.get("n")
        if search_bottleneck is not None:
            sb = search_bottleneck.get(key, {})
            row["n_tasks_with_search"] = sb.get("n_tasks_with_search")
            row["n_tasks_without_search"] = sb.get("n_tasks_without_search")
            for cutoff in SEARCH_BOTTLENECK_CUTOFFS:
                found_tasks = sb.get(f"found_tasks_top_{cutoff}")
                not_found_tasks = sb.get(f"not_found_tasks_top_{cutoff}")
                avg_first_hit = sb.get(f"avg_first_hit_round_top_{cutoff}")
                avg_wasted = sb.get(f"avg_wasted_rounds_top_{cutoff}")
                row[f"found_tasks_top_{cutoff}"] = found_tasks
                row[f"found_tasks_top{cutoff}"] = found_tasks
                row[f"not_found_tasks_top_{cutoff}"] = not_found_tasks
                row[f"not_found_tasks_top{cutoff}"] = not_found_tasks
                row[f"top{cutoff}_not_found_rate"] = sb.get(f"top{cutoff}_not_found_rate")
                row[f"avg_first_hit_round_top_{cutoff}"] = avg_first_hit
                row[f"avg_first_hit_round_top{cutoff}"] = avg_first_hit
                row[f"avg_wasted_rounds_top_{cutoff}"] = avg_wasted
                row[f"avg_wasted_rounds_top{cutoff}"] = avg_wasted
        rows.append(row)
    return rows


def build_variant_summary(summary_rows: List[dict]) -> List[dict]:
    groups: Dict[str, List[dict]] = defaultdict(list)
    for row in summary_rows:
        groups[row.get("variant", "unknown")].append(row)

    def weighted_avg(rows: List[dict], field: str, weight_field: str = "n") -> float | None:
        num = 0.0
        den = 0.0
        for r in rows:
            v = r.get(field)
            n = r.get(weight_field)
            if v is None or n in (None, 0):
                continue
            num += float(v) * float(n)
            den += float(n)
        if den == 0:
            return None
        return round(num / den, 4)

    out = []
    for variant, rows in sorted(groups.items()):
        total_n = sum(int(r.get("n", 0) or 0) for r in rows)
        total_cost = round(sum(float(r.get("total_cost_usd", 0) or 0) for r in rows), 4)
        total_ideal_subagent_cost = round(
            sum(float(r.get("total_ideal_subagent_cost_usd", 0) or 0) for r in rows), 4
        )
        total_cost_with_ideal = round(
            sum(float(r.get("total_cost_with_ideal_subagents_usd", 0) or 0) for r in rows), 4
        )
        avg_search_calls = weighted_avg(rows, "avg_search_calls")
        em = weighted_avg(rows, "em")
        row = {
            "variant": variant,
            "n_total": total_n,
            "num_condition_model_rows": len(rows),
            "conditions": sorted({r.get("base_condition", "") for r in rows if r.get("base_condition")}),
            "models": sorted({r.get("model", "") for r in rows if r.get("model")}),
            "total_cost_usd": total_cost,
            "total_ideal_subagent_cost_usd": total_ideal_subagent_cost,
            "total_cost_with_ideal_subagents_usd": total_cost_with_ideal,
            "em": em,
            "f1": weighted_avg(rows, "f1"),
            "D_ret": weighted_avg(rows, "D_ret"),
            "D_acc": weighted_avg(rows, "D_acc"),
            "D_acc_precision": weighted_avg(rows, "dacc_precision"),
            "D_acc_recall": weighted_avg(rows, "dacc_recall"),
            "D_acc_f1": weighted_avg(rows, "dacc_f1"),
            "avg_cost_usd": weighted_avg(rows, "avg_cost_usd"),
            "avg_ideal_subagent_cost_usd": weighted_avg(rows, "avg_ideal_subagent_cost_usd"),
            "avg_total_cost_with_ideal_subagents_usd": weighted_avg(
                rows, "avg_total_cost_with_ideal_subagents_usd"
            ),
            "avg_tool_calls": weighted_avg(rows, "avg_tool_calls"),
            "avg_search_calls": avg_search_calls,
            "search_efficiency": round(em / avg_search_calls, 4) if (em is not None and avg_search_calls) else None,
        }
        row["n_tasks_with_search"] = sum(int(r.get("n_tasks_with_search", 0) or 0) for r in rows)
        row["n_tasks_without_search"] = sum(int(r.get("n_tasks_without_search", 0) or 0) for r in rows)
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS:
            found_tasks = sum(int(r.get(f"found_tasks_top_{cutoff}", 0) or 0) for r in rows)
            not_found_tasks = sum(int(r.get(f"not_found_tasks_top_{cutoff}", 0) or 0) for r in rows)
            avg_first_hit = weighted_avg(
                rows,
                f"avg_first_hit_round_top_{cutoff}",
                weight_field=f"found_tasks_top_{cutoff}",
            )
            avg_wasted = weighted_avg(
                rows,
                f"avg_wasted_rounds_top_{cutoff}",
                weight_field="n_tasks_with_search",
            )
            row[f"found_tasks_top_{cutoff}"] = found_tasks
            row[f"found_tasks_top{cutoff}"] = found_tasks
            row[f"not_found_tasks_top_{cutoff}"] = not_found_tasks
            row[f"not_found_tasks_top{cutoff}"] = not_found_tasks
            row[f"top{cutoff}_not_found_rate"] = weighted_avg(
                rows,
                f"top{cutoff}_not_found_rate",
                weight_field="n_tasks_with_search",
            )
            row[f"avg_first_hit_round_top_{cutoff}"] = avg_first_hit
            row[f"avg_first_hit_round_top{cutoff}"] = avg_first_hit
            row[f"avg_wasted_rounds_top_{cutoff}"] = avg_wasted
            row[f"avg_wasted_rounds_top{cutoff}"] = avg_wasted
        out.append(row)
    return out


def write_per_task_retrieval_csv(discovery: dict, output_csv: Path) -> int:
    """Write task-level retrieval details used for D_ret precision/recall analysis."""
    fieldnames = [
        "condition_model",
        "task_id",
        "search_calls_count",
        "gold_datasets_needed_count",
        "datasets_retrieved_count",
        "datasets_retrieved_unique_count",
        "gold_datasets_retrieved_count",
        "retrieval_recall",
        "retrieval_precision",
        "retrieval_f1",
    ]
    rows: List[dict] = []
    for key, d in sorted(discovery.items()):
        task_metrics = sorted(d.get("task_metrics", []), key=lambda m: str(m.get("task_id", "")))
        for m in task_metrics:
            gold_ids_count = len(m.get("gold_ids", []))
            retrieved_unique_count = len(m.get("retrieved_dataset_ids", []))
            retrieved_ids_count = int(m.get("num_results_total_non_unique", retrieved_unique_count) or 0)
            retrieved_gold_ids_count = len(m.get("retrieved_gold_dataset_ids", []))
            rows.append(
                {
                    "condition_model": key,
                    "task_id": m.get("task_id", ""),
                    "search_calls_count": int(m.get("num_search_calls", 0) or 0),
                    "gold_datasets_needed_count": gold_ids_count,
                    "datasets_retrieved_count": retrieved_ids_count,
                    "datasets_retrieved_unique_count": retrieved_unique_count,
                    "gold_datasets_retrieved_count": retrieved_gold_ids_count,
                    "retrieval_recall": round(float(m.get("d_ret", 0) or 0), 6),
                    "retrieval_precision": round(float(m.get("d_ret_precision", 0) or 0), 6),
                    "retrieval_f1": round(float(m.get("d_ret_f1", 0) or 0), 6),
                }
            )

    with output_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_search_bottleneck_csv(rows: List[dict], output_csv: Path, fieldnames: List[str]) -> int:
    return _shared_write_search_bottleneck_csv(rows, output_csv, fieldnames)


def _tool_sort_key(tool_name: str) -> tuple:
    if tool_name in SEARCH_TOOL_ORDER:
        return (SEARCH_TOOL_ORDER.index(tool_name), tool_name)
    return (len(SEARCH_TOOL_ORDER), tool_name)


def _condition_sort_key(condition_label: str) -> tuple:
    if "/" in condition_label:
        variant, base_condition = condition_label.split("/", 1)
        return (variant, base_condition)
    return (condition_label, "")


def _import_plot_libs():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except Exception:
        print("Skipping bottleneck figures: matplotlib is not installed.")
        return None


def _annotate_bar_values(ax, bars, *, pct: bool = False, min_value: float = 0.0) -> None:
    for bar in bars:
        value = float(bar.get_height())
        if value < min_value:
            continue
        label = f"{value:.0f}%" if pct else f"{value:.1f}".rstrip("0").rstrip(".")
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + (1.0 if pct else max(0.05, value * 0.03)),
            label,
            ha="center",
            va="bottom",
            fontsize=8,
        )


def _plot_first_hit_rounds_condition(plt, rows: List[dict], output_path: Path) -> None:
    if not rows:
        return
    ordered_conditions = sorted({str(row.get("condition", "")) for row in rows}, key=_condition_sort_key)
    max_round = max(int(row.get("max_round", 0) or 0) for row in rows)
    if max_round <= 0:
        return

    fig, axes = plt.subplots(1, len(SEARCH_BOTTLENECK_CUTOFFS), figsize=(18, 5), sharey=True)
    for ax, cutoff in zip(axes, SEARCH_BOTTLENECK_CUTOFFS):
        cutoff_rows = {str(row["condition"]): row for row in rows if int(row.get("cutoff", 0) or 0) == cutoff}
        for condition in ordered_conditions:
            row = cutoff_rows.get(condition)
            if row is None:
                continue
            xs = list(range(1, max_round + 1))
            cumulative = row.get("cumulative_found_rates", {})
            ys = [100.0 * float(cumulative.get(str(round_number), 0.0) or 0.0) for round_number in xs]
            not_found_pct = 100.0 * float(row.get("not_found_rate", 0.0) or 0.0)
            ax.plot(xs, ys, marker="o", linewidth=2, label=f"{condition} (nf {not_found_pct:.0f}%)")
        ax.set_title(f"Top-{cutoff}")
        ax.set_xlabel("Search Round")
        ax.set_ylim(0, 100)
        ax.grid(alpha=0.25, linestyle="--", linewidth=0.7)
        if ax is axes[0]:
            ax.set_ylabel("Tasks Found by Round (%)")
    handles, labels = axes[-1].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8)
    fig.suptitle("First Gold Hit by Search Round and Condition")
    fig.tight_layout(rect=(0, 0, 0.83, 0.95))
    fig.savefig(output_path)
    plt.close(fig)


def _plot_first_hit_rounds_tool(plt, rows: List[dict], output_path: Path) -> None:
    if not rows:
        return
    ordered_tools = sorted({str(row.get("search_tool", "")) for row in rows}, key=_tool_sort_key)
    max_round = max(int(row.get("max_round", 0) or 0) for row in rows)
    if max_round <= 0:
        return

    fig, axes = plt.subplots(1, len(SEARCH_BOTTLENECK_CUTOFFS), figsize=(18, 5), sharey=True)
    for ax, cutoff in zip(axes, SEARCH_BOTTLENECK_CUTOFFS):
        cutoff_rows = {str(row["search_tool"]): row for row in rows if int(row.get("cutoff", 0) or 0) == cutoff}
        for tool_name in ordered_tools:
            row = cutoff_rows.get(tool_name)
            if row is None:
                continue
            xs = list(range(1, max_round + 1))
            cumulative = row.get("cumulative_found_rates", {})
            ys = [100.0 * float(cumulative.get(str(round_number), 0.0) or 0.0) for round_number in xs]
            not_found_pct = 100.0 * float(row.get("not_found_rate", 0.0) or 0.0)
            ax.plot(
                xs,
                ys,
                marker="o",
                linewidth=2,
                label=f"{tool_name} (nf {not_found_pct:.0f}%)",
                color=SEARCH_TOOL_COLORS.get(tool_name),
            )
        ax.set_title(f"Top-{cutoff}")
        ax.set_xlabel("Tool-Local Search Round")
        ax.set_ylim(0, 100)
        ax.grid(alpha=0.25, linestyle="--", linewidth=0.7)
        if ax is axes[0]:
            ax.set_ylabel("Tasks Found by Round (%)")
    handles, labels = axes[-1].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8)
    fig.suptitle("First Gold Hit by Search Tool and Tool-Local Round")
    fig.tight_layout(rect=(0, 0, 0.83, 0.95))
    fig.savefig(output_path)
    plt.close(fig)


def _plot_topk_miss_by_tool(plt, rows: List[dict], output_path: Path) -> None:
    if not rows:
        return
    ordered_tools = sorted({str(row.get("search_tool", "")) for row in rows}, key=_tool_sort_key)
    cutoff_to_rows = {
        cutoff: {str(row["search_tool"]): row for row in rows if int(row.get("cutoff", 0) or 0) == cutoff}
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS
    }
    fig, ax = plt.subplots(figsize=(max(9, len(ordered_tools) * 1.4), 6))
    x_positions = list(range(len(ordered_tools)))
    width = 0.22
    for idx, cutoff in enumerate(SEARCH_BOTTLENECK_CUTOFFS):
        offsets = [x + (idx - 1) * width for x in x_positions]
        values = [
            100.0 * float(cutoff_to_rows[cutoff].get(tool_name, {}).get("miss_rate", 0.0) or 0.0)
            for tool_name in ordered_tools
        ]
        bars = ax.bar(offsets, values, width=width * 0.92, label=f"Top-{cutoff}")
        _annotate_bar_values(ax, bars, pct=True, min_value=4.0)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(ordered_tools, rotation=20, ha="right")
    ax.set_ylabel("Miss Rate (%)")
    ax.set_title("Gold Miss Rate by Search Tool")
    ax.legend()
    ax.grid(axis="y", alpha=0.25, linestyle="--", linewidth=0.7)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def _plot_search_tool_coverage_waste(plt, rows: List[dict], output_path: Path) -> None:
    if not rows:
        return
    ordered_tools = sorted({str(row.get("search_tool", "")) for row in rows}, key=_tool_sort_key)
    cutoff_to_rows = {
        cutoff: {str(row["search_tool"]): row for row in rows if int(row.get("cutoff", 0) or 0) == cutoff}
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS
    }
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    x_positions = list(range(len(ordered_tools)))
    width = 0.22

    for idx, cutoff in enumerate(SEARCH_BOTTLENECK_CUTOFFS):
        offsets = [x + (idx - 1) * width for x in x_positions]
        coverage = [
            100.0 * float(cutoff_to_rows[cutoff].get(tool_name, {}).get("ever_found_rate", 0.0) or 0.0)
            for tool_name in ordered_tools
        ]
        wasted = [
            float(cutoff_to_rows[cutoff].get(tool_name, {}).get("avg_wasted_rounds", 0.0) or 0.0)
            for tool_name in ordered_tools
        ]
        bars_cov = axes[0].bar(offsets, coverage, width=width * 0.92, label=f"Top-{cutoff}")
        bars_waste = axes[1].bar(offsets, wasted, width=width * 0.92, label=f"Top-{cutoff}")
        _annotate_bar_values(axes[0], bars_cov, pct=True, min_value=4.0)
        _annotate_bar_values(axes[1], bars_waste, pct=False, min_value=0.15)

    axes[0].set_title("Ever Found Rate by Search Tool")
    axes[0].set_ylabel("Tasks Ever Found (%)")
    axes[1].set_title("Average Wasted Rounds Before First Hit")
    axes[1].set_ylabel("Wasted Rounds")
    for ax in axes:
        ax.set_xticks(x_positions)
        ax.set_xticklabels(ordered_tools, rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25, linestyle="--", linewidth=0.7)
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def generate_search_bottleneck_figures(search_bottleneck: dict, output_dir: Path) -> None:
    _shared_generate_search_bottleneck_figures(search_bottleneck, output_dir)


def _collect_results_runs(results_root: Path) -> List[Tuple[str, str, str, Path]]:
    runs: List[Tuple[str, str, str, Path]] = []
    for jsonl_path in results_root.rglob("agent_results.jsonl"):
        variant, base_condition, model = _parse_results_jsonl_path(jsonl_path, results_root)
        runs.append((variant, base_condition, model, jsonl_path))
    return runs


def _collect_trace_runs(traces_root: Path) -> Dict[Tuple[str, str, str], Path]:
    model_dirs: Dict[Tuple[str, str, str], Path] = {}
    for jsonl_path in traces_root.rglob("*.jsonl"):
        variant, base_condition, model, _ = _parse_trace_jsonl_path(jsonl_path, traces_root)
        run_key = (variant, base_condition, model)
        if run_key not in model_dirs:
            parts = jsonl_path.relative_to(traces_root).parts
            # Search-ablation: variant/base/model/task/task.jsonl
            if len(parts) >= 5:
                model_dirs[run_key] = traces_root / parts[0] / parts[1] / parts[2]
            # Legacy: condition/model/task/task.jsonl
            elif len(parts) >= 4:
                model_dirs[run_key] = traces_root / parts[0] / parts[1]
    return model_dirs


def _safe_symlink(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    os.symlink(src, dst)


def _figure_condition_label(variant: str, base_condition: str) -> str:
    if variant == base_condition:
        return base_condition
    return f"{variant}__{base_condition}"


def generate_search_figures(
    results_dir: str,
    traces_dir: str,
    tasks_dir: str,
    output_dir: Path,
    model_filter: str | None = None,
    search_bottleneck: dict | None = None,
) -> None:
    """Generate standard analysis figures while preserving search variants."""
    results_root = Path(results_dir)
    traces_root = Path(traces_dir)

    runs = _collect_results_runs(results_root)
    if not runs:
        print("Skipping figure generation: no agent_results.jsonl files found.")
        return

    trace_runs = _collect_trace_runs(traces_root)
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="search_analysis_figs_") as tmpdir:
        tmp_root = Path(tmpdir)
        flat_results = tmp_root / "results"
        flat_traces = tmp_root / "traces"

        for variant, base_condition, model, src_jsonl in runs:
            condition_label = _figure_condition_label(variant, base_condition)
            dst_jsonl = flat_results / condition_label / model / "agent_results.jsonl"
            _safe_symlink(src_jsonl.resolve(), dst_jsonl)

        for (variant, base_condition, model), src_model_dir in trace_runs.items():
            condition_label = _figure_condition_label(variant, base_condition)
            dst_model_dir = flat_traces / condition_label / model
            _safe_symlink(src_model_dir.resolve(), dst_model_dir)

        cmd = [
            sys.executable,
            str(Path(__file__).with_name("generate_figures.py")),
            "--results-dir",
            str(flat_results),
            "--traces-dir",
            str(flat_traces),
            "--tasks-dir",
            str(tasks_dir),
            "--output-dir",
            str(fig_dir),
        ]
        if model_filter:
            cmd += ["--model-filter", model_filter]
        subprocess.run(cmd, check=True)
    if search_bottleneck is not None:
        generate_search_bottleneck_figures(search_bottleneck, output_dir)


def run_analysis(
    *,
    results_dir: str,
    traces_dir: str,
    tasks_dir: str,
    output_dir: str,
    no_figures: bool = False,
    model_filter: str | None = None,
) -> dict:
    model_filters = [s.strip().lower() for s in model_filter.split(",")] if model_filter else None

    def _keep_model(name: str) -> bool:
        if not model_filters:
            return True
        n = (name or "").lower()
        return any(f in n for f in model_filters)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading grouped results...")
    records, by_key_records, _ = load_results_grouped(results_dir)
    if not records:
        print(f"No agent_results.jsonl files found under {results_dir}")
        return {}

    print("Loading grouped traces...")
    grouped_traces, trace_meta = load_traces_grouped(traces_dir)

    if model_filters:
        records = [r for r in records if _keep_model(_split_cm_key(r.get("_cm_key", ""))[2])]
        by_key_records = {k: v for k, v in by_key_records.items() if _keep_model(_split_cm_key(k)[2])}
        grouped_traces = {k: v for k, v in grouped_traces.items() if _keep_model(_split_cm_key(k)[2])}
        trace_meta = {k: v for k, v in trace_meta.items() if _keep_model(_split_cm_key(k)[2])}

    print("Running EM/F1...")
    em = run_em(records)

    print("Running discovery metrics...")
    discovery = run_discovery(grouped_traces, tasks_dir)

    print("Running failure attribution...")
    failure = run_failure(by_key_records, grouped_traces, tasks_dir)

    print("Running efficiency...")
    efficiency = run_efficiency(by_key_records)

    print("Running provenance (Condition A variants)...")
    provenance = run_provenance(grouped_traces, tasks_dir)

    print("Running tools discovery...")
    tools_discovery = run_tools_discovery(grouped_traces, tasks_dir)

    print("Running search depth curve...")
    search_depth = run_search_depth(records)

    print("Running planning overhead (Condition B variants)...")
    planning_overhead = run_planning_overhead(records)

    print("Running reasoning density curve...")
    reasoning_density = run_reasoning_density(records, tasks_dir)

    print("Running tool error rates...")
    tool_errors = run_tool_errors(by_key_records)

    print("Running search bottleneck analysis...")
    task_gold = load_task_gold_ids(tasks_dir)
    search_bottleneck = compute_search_bottleneck(grouped_traces, trace_meta, task_gold)

    print("Building summaries...")
    summary = build_summary(
        em,
        discovery,
        failure,
        efficiency,
        search_depth,
        reasoning_density,
        tool_errors,
        search_bottleneck.get("condition_model_summary"),
    )
    variant_summary = build_variant_summary(summary)

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
        "search_first_hit_condition.json": search_bottleneck.get("condition_summary_rows", []),
        "search_first_hit_tool.json": search_bottleneck.get("tool_first_hit_rows", []),
        "search_topk_miss_tool.json": search_bottleneck.get("tool_miss_rows", []),
        "search_tool_efficiency.json": search_bottleneck.get("tool_efficiency_rows", []),
        "summary.json": summary,
        "variant_summary.json": variant_summary,
    }

    for fname, data in files.items():
        path = out_dir / fname
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Wrote {path}")

    per_task_csv = out_dir / "per_task_retrieval.csv"
    num_rows = write_per_task_retrieval_csv(discovery, per_task_csv)
    print(f"  Wrote {per_task_csv} ({num_rows} rows)")

    per_task_search_csv = out_dir / "per_task_search_bottleneck.csv"
    per_task_search_rows = search_bottleneck.get("per_task_rows", [])
    per_task_search_fields = [
        "condition_model",
        "condition",
        "variant",
        "base_condition",
        "model",
        "task_id",
        "num_search_calls",
    ] + [
        field
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS
        for field in (
            f"found_top_{cutoff}",
            f"first_hit_round_top_{cutoff}",
            f"wasted_rounds_top_{cutoff}",
        )
    ]
    num_task_search_rows = write_search_bottleneck_csv(
        per_task_search_rows,
        per_task_search_csv,
        per_task_search_fields,
    )
    print(f"  Wrote {per_task_search_csv} ({num_task_search_rows} rows)")

    per_task_tool_csv = out_dir / "per_task_search_tool_bottleneck.csv"
    per_task_tool_rows = search_bottleneck.get("per_task_tool_rows", [])
    per_task_tool_fields = [
        "condition_model",
        "condition",
        "variant",
        "base_condition",
        "model",
        "task_id",
        "search_tool",
        "num_tool_calls",
    ] + [
        field
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS
        for field in (
            f"found_top_{cutoff}",
            f"first_hit_round_top_{cutoff}",
            f"wasted_rounds_top_{cutoff}",
        )
    ]
    num_task_tool_rows = write_search_bottleneck_csv(
        per_task_tool_rows,
        per_task_tool_csv,
        per_task_tool_fields,
    )
    print(f"  Wrote {per_task_tool_csv} ({num_task_tool_rows} rows)")

    search_first_hit_condition_csv = out_dir / "search_first_hit_condition.csv"
    write_search_bottleneck_csv(
        search_bottleneck.get("condition_summary_rows", []),
        search_first_hit_condition_csv,
        [
            "condition",
            "variant",
            "base_condition",
            "cutoff",
            "n_tasks_with_search",
            "n_tasks_without_search",
            "found_tasks",
            "not_found_tasks",
            "not_found_rate",
            "ever_found_rate",
            "avg_first_hit_round_found_only",
            "median_first_hit_round_found_only",
            "avg_wasted_rounds",
            "max_round",
            "models",
            "num_condition_model_rows",
            "round_counts",
            "cumulative_found_counts",
            "cumulative_found_rates",
        ],
    )
    print(f"  Wrote {search_first_hit_condition_csv}")

    search_first_hit_tool_csv = out_dir / "search_first_hit_tool.csv"
    write_search_bottleneck_csv(
        search_bottleneck.get("tool_first_hit_rows", []),
        search_first_hit_tool_csv,
        [
            "search_tool",
            "cutoff",
            "tasks_with_tool",
            "found_tasks",
            "not_found_tasks",
            "not_found_rate",
            "ever_found_rate",
            "avg_first_hit_round_found_only",
            "median_first_hit_round_found_only",
            "avg_wasted_rounds",
            "max_round",
            "conditions",
            "models",
            "num_condition_model_rows",
            "round_counts",
            "cumulative_found_counts",
            "cumulative_found_rates",
        ],
    )
    print(f"  Wrote {search_first_hit_tool_csv}")

    search_topk_miss_tool_csv = out_dir / "search_topk_miss_tool.csv"
    write_search_bottleneck_csv(
        search_bottleneck.get("tool_miss_rows", []),
        search_topk_miss_tool_csv,
        [
            "search_tool",
            "cutoff",
            "n_calls",
            "hit_calls",
            "miss_calls",
            "miss_rate",
            "conditions",
            "models",
            "num_condition_model_rows",
        ],
    )
    print(f"  Wrote {search_topk_miss_tool_csv}")

    search_tool_efficiency_csv = out_dir / "search_tool_efficiency.csv"
    write_search_bottleneck_csv(
        search_bottleneck.get("tool_efficiency_rows", []),
        search_tool_efficiency_csv,
        [
            "search_tool",
            "cutoff",
            "tasks_with_tool",
            "ever_found_rate",
            "avg_first_hit_round_found_only",
            "avg_wasted_rounds",
            "conditions",
            "models",
            "num_condition_model_rows",
        ],
    )
    print(f"  Wrote {search_tool_efficiency_csv}")

    print(f"\nSummary ({len(summary)} variant×condition×model rows):")
    for row in summary:
        em_pct = f"{row.get('em', 0)*100:.1f}%" if row.get("em") is not None else "N/A"
        d_ret = f"{row.get('D_ret', 0):.2f}" if row.get("D_ret") is not None else "N/A"
        print(
            f"  {row['condition_model']:<70} "
            f"EM={em_pct}  D_ret={d_ret}  n={row.get('n')}"
        )

    print("\nVariant summary:")
    for row in variant_summary:
        em_pct = f"{row.get('em', 0)*100:.1f}%" if row.get("em") is not None else "N/A"
        print(
            f"  {row['variant']:<24} "
            f"EM={em_pct:<7} D_ret={row.get('D_ret')} "
            f"D_acc={row.get('D_acc')} n={row.get('n_total')}"
        )

    if no_figures:
        print("\nSkipping figures (--no-figures).")
    else:
        print("\nGenerating figures...")
        try:
            generate_search_figures(
                results_dir,
                traces_dir,
                tasks_dir,
                out_dir,
                model_filter,
                search_bottleneck,
            )
            print(f"Figures written to {out_dir / 'figures'}")
        except subprocess.CalledProcessError as exc:
            print(f"Figure generation failed with exit code {exc.returncode}.")

    return {
        "summary": summary,
        "variant_summary": variant_summary,
        "search_bottleneck": search_bottleneck,
        "discovery": discovery,
        "tools_discovery": tools_discovery,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results_search")
    parser.add_argument(
        "--no-figures",
        action="store_true",
        help="Skip diagram generation (JSON outputs only).",
    )
    parser.add_argument(
        "--model-filter",
        default=None,
        help="Substring filter on model name (comma-separated OR). e.g. 'haiku,sonnet'.",
    )
    args = parser.parse_args()
    run_analysis(
        results_dir=args.results_dir,
        traces_dir=args.traces_dir,
        tasks_dir=args.tasks_dir,
        output_dir=args.output_dir,
        no_figures=args.no_figures,
        model_filter=args.model_filter,
    )


if __name__ == "__main__":
    main()
