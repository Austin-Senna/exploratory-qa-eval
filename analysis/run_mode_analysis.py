#!/usr/bin/env python3
"""
Mode-variant analysis runner.

Reads the multi-axis ablation output layout produced by run_mode_eval:

  results/modes/{model}/{variant}/agent_results.jsonl
  results/traces/modes/{model}/{variant}/{task_dir}/{task}.jsonl

Where {variant} encodes the three axes:
  search_{s}_results_{r}_plan{p}  (each letter in {n, d, i} = naive/standard/ideal)
  optional _k{N} and _sc{N} suffixes.

Output files (default: analysis_results_mode/):
  em_f1.json
  discovery.json
  tools_discovery.json
  failure.json
  semantic_outcomes.json
  efficiency.json
  search_depth.json
  reasoning_density.json
  tool_errors.json
  summary.json
  variant_summary.json
  per_task_retrieval.csv
  figures/ (unless --no-figures)

Not emitted (don't apply to mode runs without a base_condition layer):
  provenance.json
  planning_overhead.json
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
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.compute_em import compute_stats
from analysis.build_semantic_results import semantic_record
from analysis.discovery_metrics import (
    load_task_gold_ids,
    compute_discovery_metrics,
    compute_per_folder_discovery,
    compute_tools_discovery,
)
from analysis.failure_attribution import classify_failure, _LABEL_ORDER
from analysis.search_depth import compute_search_depth_curve
from analysis.reasoning_density import compute_reasoning_density_curve, load_task_gold_counts


_LETTER_TO_MODE = {"n": "naive", "d": "standard", "i": "ideal"}

BUCKET_SEMANTIC = "semantic_equivalents"
BUCKET_SEMANTIC_EXHAUSTED = "semantic_equivalents_but_exhausted"
BUCKET_WRONG = "wrong_answers"
BUCKET_WRONG_EXHAUSTED = "wrong_answers_but_exhausted"
BUCKET_UNSUB_TURNS = "unsubmitted_turns_exhausted"
BUCKET_UNSUB_CONTEXT = "unsubmitted_context_exhausted"
BUCKET_INFRA_EVENT_LOOP = "infra_event_loop_exception"

SUBMIT_MARKERS = [
    "Executing: submit_answer(",
    "Tool result: Answer submitted:",
    "Answer submitted! Triggering native agent cancellation.",
    "ANSWER:",
]

TURNS_MARKERS = [
    "Tool limit reached",
    "Timeout reached",
    "Search call budget exhausted",
    "Call submit_answer NOW",
]

CONTEXT_MARKERS = [
    "MaxTokensReachedException",
    "max_tokens limit",
    "Context window overflow",
    "ValidationException",
]


def _cm_key(model: str, variant: str) -> str:
    return f"{model}/{variant}"


def _split_cm_key(key: str) -> Tuple[str, str]:
    parts = key.split("/", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return "unknown", key


def _parse_variant(variant: str) -> Dict[str, Optional[object]]:
    """search_i_results_i_plani_k5_sc20 -> structured axes."""
    out: Dict[str, Optional[object]] = {
        "variant": variant,
        "search_tool": None,
        "search_results": None,
        "agent_management": None,
        "k": None,
        "sc": None,
    }
    parts = variant.split("_")
    for idx, token in enumerate(parts):
        if token == "search" and idx + 1 < len(parts):
            out["search_tool"] = _LETTER_TO_MODE.get(parts[idx + 1])
        elif token == "results" and idx + 1 < len(parts):
            out["search_results"] = _LETTER_TO_MODE.get(parts[idx + 1])
        elif token.startswith("plan") and len(token) > 4:
            out["agent_management"] = _LETTER_TO_MODE.get(token[4:])
        elif token.startswith("k") and token[1:].isdigit():
            out["k"] = int(token[1:])
        elif token.startswith("sc") and token[2:].isdigit():
            out["sc"] = int(token[2:])
    return out


def _task_stem(task_id: str) -> str:
    p = Path(str(task_id))
    return f"{p.parent.name}/{p.stem}"


def relative_task_path(task_id: str) -> Path:
    task_path = Path(str(task_id))
    parts = list(task_path.parts)
    if parts and parts[0].startswith("tasks"):
        parts = parts[1:]
    relative = Path(*parts) if parts else task_path
    return relative.with_suffix(".log")


def latest_marker(text: str, markers: List[str]) -> Tuple[int, str]:
    lowered = text.lower()
    latest_pos = -1
    latest_text = ""
    for marker in markers:
        pos = lowered.rfind(marker.lower())
        if pos > latest_pos:
            latest_pos = pos
            latest_text = marker
    return latest_pos, latest_text


def _parse_results_jsonl_path(path: Path, results_root: Path) -> Tuple[str, str]:
    # {results_root}/{model}/{variant}/agent_results.jsonl -> (model, variant)
    rel = path.relative_to(results_root)
    parts = rel.parts
    if len(parts) >= 3:
        return parts[-3], parts[-2]
    return "unknown", "unknown"


def _parse_trace_jsonl_path(path: Path, traces_root: Path) -> Tuple[str, str, str]:
    # {traces_root}/{model}/{variant}/{task_dir}/{task}.jsonl -> (model, variant, task_id)
    rel = path.relative_to(traces_root)
    parts = rel.parts
    if len(parts) >= 4:
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return parts[-4], parts[-3], task_id
    return "unknown", "unknown", "unknown/unknown"


def load_results_grouped(results_dir: str) -> Tuple[List[dict], Dict[str, List[dict]], Dict[str, dict]]:
    root = Path(results_dir)
    records: List[dict] = []
    by_key: Dict[str, List[dict]] = defaultdict(list)
    meta_by_key: Dict[str, dict] = {}

    for jsonl_path in root.rglob("agent_results.jsonl"):
        model, variant = _parse_results_jsonl_path(jsonl_path, root)
        key = _cm_key(model, variant)
        meta_by_key[key] = {"model": model, "variant": variant}
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                r["variant"] = variant
                r["model_label"] = model
                r["_cm_key"] = key
                # Option A: key condition-scoped metrics per-cell.
                r["condition"] = key
                records.append(r)
                by_key[key].append(r)

    return records, by_key, meta_by_key


def load_traces_grouped(traces_dir: str) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    root = Path(traces_dir)
    grouped: Dict[str, dict] = defaultdict(lambda: defaultdict(list))
    meta_by_key: Dict[str, dict] = {}

    for jsonl_path in root.rglob("*.jsonl"):
        model, variant, task_id = _parse_trace_jsonl_path(jsonl_path, root)
        key = _cm_key(model, variant)
        meta_by_key[key] = {"model": model, "variant": variant}
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
        # cond_label was set to _cm_key = "{model}/{variant}"
        key = cond_label if "/" in cond_label else _cm_key(model, cond_label)
        row = dict(vals)
        _, variant = _split_cm_key(key)
        row["variant"] = variant
        row["model"] = model
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


def _read_log_tail(path: Path, tail_lines: int = 30) -> str:
    if not path.exists():
        return ""
    with path.open(errors="ignore") as handle:
        lines = handle.readlines()
    return "".join(lines[-tail_lines:])


def run_semantic_outcomes(by_key_records: Dict[str, List[dict]], logs_dir: str, tail_lines: int = 30) -> dict:
    logs_root = Path(logs_dir)
    out: dict = {}

    for key, rows in sorted(by_key_records.items()):
        model, variant = _split_cm_key(key)
        counts: Counter = Counter()

        for r in rows:
            task_id = str(r.get("task_id", ""))
            expected = r.get("ground_truth", r.get("expected_answer", ""))
            predicted = r.get("predicted_answer", "")
            lexical_exact_match = float(r.get("exact_match", 0) or 0)
            semantic_match, _ = semantic_record(expected, predicted, lexical_exact_match)

            log_path = logs_root / "modes" / model / variant / relative_task_path(task_id)
            tail_text = _read_log_tail(log_path, tail_lines=tail_lines)

            submitted = latest_marker(tail_text, SUBMIT_MARKERS)[0] >= 0
            turns_exhausted = latest_marker(tail_text, TURNS_MARKERS)[0] >= 0
            context_exhausted = latest_marker(tail_text, CONTEXT_MARKERS)[0] >= 0
            error_text = str(r.get("error", "") or "")

            if context_exhausted:
                if submitted:
                    bucket = BUCKET_SEMANTIC_EXHAUSTED if semantic_match >= 1.0 else BUCKET_WRONG_EXHAUSTED
                else:
                    bucket = BUCKET_UNSUB_CONTEXT
            elif turns_exhausted:
                if submitted:
                    bucket = BUCKET_SEMANTIC_EXHAUSTED if semantic_match >= 1.0 else BUCKET_WRONG_EXHAUSTED
                else:
                    bucket = BUCKET_UNSUB_TURNS
            elif submitted:
                bucket = BUCKET_SEMANTIC if semantic_match >= 1.0 else BUCKET_WRONG
            elif error_text.startswith("EventLoopException"):
                bucket = BUCKET_INFRA_EVENT_LOOP
            elif "MaxTokensReachedException" in error_text or "max_tokens limit" in error_text:
                bucket = BUCKET_UNSUB_CONTEXT
            elif any(marker in error_text for marker in TURNS_MARKERS):
                bucket = BUCKET_UNSUB_TURNS
            elif predicted:
                bucket = BUCKET_SEMANTIC if semantic_match >= 1.0 else BUCKET_WRONG
            else:
                # Keep the mode-analysis view constrained to the agreed buckets.
                bucket = BUCKET_INFRA_EVENT_LOOP

            counts[bucket] += 1

        out[key] = {
            BUCKET_SEMANTIC: counts.get(BUCKET_SEMANTIC, 0),
            BUCKET_SEMANTIC_EXHAUSTED: counts.get(BUCKET_SEMANTIC_EXHAUSTED, 0),
            BUCKET_WRONG: counts.get(BUCKET_WRONG, 0),
            BUCKET_WRONG_EXHAUSTED: counts.get(BUCKET_WRONG_EXHAUSTED, 0),
            BUCKET_UNSUB_TURNS: counts.get(BUCKET_UNSUB_TURNS, 0),
            BUCKET_UNSUB_CONTEXT: counts.get(BUCKET_UNSUB_CONTEXT, 0),
            BUCKET_INFRA_EVENT_LOOP: counts.get(BUCKET_INFRA_EVENT_LOOP, 0),
            "total": sum(counts.values()),
        }

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

    out = {}
    for key, rows in sorted(by_key_records.items()):
        out[key] = {
            "cost_usd": dist([r.get("cost_usd", 0.0) for r in rows]),
            "time_s": dist([r.get("time", 0.0) for r in rows]),
            "tool_calls": dist([r.get("tool_calls_total", 0) for r in rows]),
            "total_cost_usd": sum(r.get("cost_usd", 0.0) for r in rows),
            "n": len(rows),
        }
    return out


def run_tools_discovery(grouped_traces: Dict[str, dict], tasks_dir: str) -> dict:
    task_gold = load_task_gold_ids(tasks_dir)
    out = {}
    for key, traces in sorted(grouped_traces.items()):
        out[key] = compute_tools_discovery(traces, task_gold)
    return out


def run_search_depth(records: List[dict]) -> dict:
    return compute_search_depth_curve(records)


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
    semantic_outcomes: dict | None = None,
    search_depth: dict | None = None,
    reasoning_density: dict | None = None,
    tool_errors: dict | None = None,
) -> List[dict]:
    keys = sorted(set(list(em.keys()) + list(discovery.keys()) + list(failure.keys())))
    rows: List[dict] = []
    for key in keys:
        model, variant = _split_cm_key(key)
        axes = _parse_variant(variant)
        row: dict = {
            "condition_model": key,
            "model": model,
            "variant": variant,
            "search_tool": axes["search_tool"],
            "search_results": axes["search_results"],
            "agent_management": axes["agent_management"],
            "k": axes["k"],
            "sc": axes["sc"],
        }
        if key in em:
            e = em[key]
            row["n"] = e.get("n")
            row["em"] = round(e.get("em", 0) or 0, 3)
            row["f1"] = round(e.get("f1", 0) or 0, 3)
            row["avg_cost_usd"] = round(e.get("avg_cost_usd", 0), 4)
            row["total_cost_usd"] = round(e.get("total_cost_usd", 0), 4)
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
            row["dacc_precision"] = round(d.get("D_acc_precision", 0), 3)
            row["dacc_recall"] = round(d.get("D_acc_recall", d.get("D_acc", 0)), 3)
            row["dacc_f1"] = round(d.get("D_acc_f1", 0), 3)
            row["search_avg_precision"] = round(d.get("avg_precision", 0), 3)
            row["search_avg_recall"] = round(d.get("avg_recall", 0), 3)
            row["search_avg_f1"] = round(d.get("avg_f1", 0), 3)
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
        if semantic_outcomes is not None and key in semantic_outcomes:
            so = semantic_outcomes[key]
            row[BUCKET_SEMANTIC] = so.get(BUCKET_SEMANTIC, 0)
            row[BUCKET_SEMANTIC_EXHAUSTED] = so.get(BUCKET_SEMANTIC_EXHAUSTED, 0)
            row[BUCKET_WRONG] = so.get(BUCKET_WRONG, 0)
            row[BUCKET_WRONG_EXHAUSTED] = so.get(BUCKET_WRONG_EXHAUSTED, 0)
            row[BUCKET_UNSUB_TURNS] = so.get(BUCKET_UNSUB_TURNS, 0)
            row[BUCKET_UNSUB_CONTEXT] = so.get(BUCKET_UNSUB_CONTEXT, 0)
            row[BUCKET_INFRA_EVENT_LOOP] = so.get(BUCKET_INFRA_EVENT_LOOP, 0)
        if tool_errors is not None and key in tool_errors:
            te = tool_errors[key]
            for tool_name in ("query_file", "execute_code", "peek_file"):
                row[f"{tool_name}_error_rate"] = te.get(tool_name, {}).get("error_rate")
        if search_depth is not None:
            depth = search_depth.get(key, {})
            for bin_label in ("1", "2-3", "4-6", "7-10", "11-30"):
                safe = bin_label.replace("-", "_")
                entry = depth.get(bin_label, {})
                row[f"depth_{safe}_em"] = entry.get("mean_em")
                row[f"depth_{safe}_n"] = entry.get("n")
        if reasoning_density is not None:
            rdensity = reasoning_density.get(key, {})
            for bin_label in ("<=2", "3-4", "5-7", "8-10", ">10"):
                safe = bin_label.replace("<", "lte").replace(">", "gt").replace("-", "_")
                entry = rdensity.get(bin_label, {})
                row[f"rdensity_{safe}_em"] = entry.get("mean_em")
                row[f"rdensity_{safe}_n"] = entry.get("n")
        rows.append(row)
    return rows


def build_variant_summary(summary_rows: List[dict]) -> List[dict]:
    groups: Dict[str, List[dict]] = defaultdict(list)
    for row in summary_rows:
        groups[row.get("variant", "unknown")].append(row)

    def weighted_avg(rows: List[dict], field: str) -> Optional[float]:
        num = 0.0
        den = 0.0
        for r in rows:
            v = r.get(field)
            n = r.get("n")
            if v is None or n in (None, 0):
                continue
            num += float(v) * float(n)
            den += float(n)
        if den == 0:
            return None
        return round(num / den, 4)

    out: List[dict] = []
    for variant, rows in sorted(groups.items()):
        axes = _parse_variant(variant)
        total_n = sum(int(r.get("n", 0) or 0) for r in rows)
        total_cost = round(sum(float(r.get("total_cost_usd", 0) or 0) for r in rows), 4)
        avg_search_calls = weighted_avg(rows, "avg_search_calls")
        em = weighted_avg(rows, "em")
        out.append(
            {
                "variant": variant,
                "search_tool": axes["search_tool"],
                "search_results": axes["search_results"],
                "agent_management": axes["agent_management"],
                "k": axes["k"],
                "sc": axes["sc"],
                "n_total": total_n,
                "num_model_rows": len(rows),
                "models": sorted({r.get("model", "") for r in rows if r.get("model")}),
                "total_cost_usd": total_cost,
                "em": em,
                "f1": weighted_avg(rows, "f1"),
                "D_ret": weighted_avg(rows, "D_ret"),
                "D_acc": weighted_avg(rows, "D_acc"),
                "D_acc_precision": weighted_avg(rows, "dacc_precision"),
                "D_acc_recall": weighted_avg(rows, "dacc_recall"),
                "D_acc_f1": weighted_avg(rows, "dacc_f1"),
                "avg_cost_usd": weighted_avg(rows, "avg_cost_usd"),
                "avg_tool_calls": weighted_avg(rows, "avg_tool_calls"),
                "avg_search_calls": avg_search_calls,
                BUCKET_SEMANTIC: sum(int(r.get(BUCKET_SEMANTIC, 0) or 0) for r in rows),
                BUCKET_SEMANTIC_EXHAUSTED: sum(int(r.get(BUCKET_SEMANTIC_EXHAUSTED, 0) or 0) for r in rows),
                BUCKET_WRONG: sum(int(r.get(BUCKET_WRONG, 0) or 0) for r in rows),
                BUCKET_WRONG_EXHAUSTED: sum(int(r.get(BUCKET_WRONG_EXHAUSTED, 0) or 0) for r in rows),
                BUCKET_UNSUB_TURNS: sum(int(r.get(BUCKET_UNSUB_TURNS, 0) or 0) for r in rows),
                BUCKET_UNSUB_CONTEXT: sum(int(r.get(BUCKET_UNSUB_CONTEXT, 0) or 0) for r in rows),
                BUCKET_INFRA_EVENT_LOOP: sum(int(r.get(BUCKET_INFRA_EVENT_LOOP, 0) or 0) for r in rows),
                "search_efficiency": round(em / avg_search_calls, 4)
                if (em is not None and avg_search_calls)
                else None,
            }
        )
    return out


def write_per_task_retrieval_csv(discovery: dict, output_csv: Path) -> int:
    fieldnames = [
        "condition_model",
        "model",
        "variant",
        "search_tool",
        "search_results",
        "agent_management",
        "k",
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
        model, variant = _split_cm_key(key)
        axes = _parse_variant(variant)
        task_metrics = sorted(d.get("task_metrics", []), key=lambda m: str(m.get("task_id", "")))
        for m in task_metrics:
            gold_ids_count = len(m.get("gold_ids", []))
            retrieved_unique_count = len(m.get("retrieved_dataset_ids", []))
            retrieved_ids_count = int(m.get("num_results_total_non_unique", retrieved_unique_count) or 0)
            retrieved_gold_ids_count = len(m.get("retrieved_gold_dataset_ids", []))
            rows.append(
                {
                    "condition_model": key,
                    "model": model,
                    "variant": variant,
                    "search_tool": axes["search_tool"],
                    "search_results": axes["search_results"],
                    "agent_management": axes["agent_management"],
                    "k": axes["k"],
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


def _safe_symlink(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    os.symlink(src, dst)


def _collect_results_runs(results_root: Path) -> List[Tuple[str, str, Path]]:
    runs: List[Tuple[str, str, Path]] = []
    for jsonl_path in results_root.rglob("agent_results.jsonl"):
        model, variant = _parse_results_jsonl_path(jsonl_path, results_root)
        runs.append((model, variant, jsonl_path))
    return runs


def _collect_trace_runs(traces_root: Path) -> Dict[Tuple[str, str], Path]:
    model_dirs: Dict[Tuple[str, str], Path] = {}
    for jsonl_path in traces_root.rglob("*.jsonl"):
        model, variant, _ = _parse_trace_jsonl_path(jsonl_path, traces_root)
        run_key = (model, variant)
        if run_key not in model_dirs:
            parts = jsonl_path.relative_to(traces_root).parts
            if len(parts) >= 4:
                model_dirs[run_key] = traces_root / parts[0] / parts[1]
    return model_dirs


def generate_mode_figures(
    results_dir: str,
    traces_dir: str,
    tasks_dir: str,
    output_dir: Path,
    model_filter: Optional[str] = None,
) -> None:
    results_root = Path(results_dir)
    traces_root = Path(traces_dir)

    runs = _collect_results_runs(results_root)
    if not runs:
        print("Skipping figure generation: no agent_results.jsonl files found.")
        return

    trace_runs = _collect_trace_runs(traces_root) if traces_root.exists() else {}
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="mode_analysis_figs_") as tmpdir:
        tmp_root = Path(tmpdir)
        flat_results = tmp_root / "results"
        flat_traces = tmp_root / "traces"

        for model, variant, src_jsonl in runs:
            dst_jsonl = flat_results / variant / model / "agent_results.jsonl"
            _safe_symlink(src_jsonl.resolve(), dst_jsonl)

        for (model, variant), src_model_dir in trace_runs.items():
            dst_model_dir = flat_traces / variant / model
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results/modes")
    parser.add_argument("--traces-dir", default="results/traces/modes")
    parser.add_argument("--logs-dir", default="logs")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results_mode")
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

    model_filters = (
        [s.strip().lower() for s in args.model_filter.split(",")] if args.model_filter else None
    )

    def _keep_model(name: str) -> bool:
        if not model_filters:
            return True
        n = (name or "").lower()
        return any(f in n for f in model_filters)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading grouped results...")
    records, by_key_records, _ = load_results_grouped(args.results_dir)
    if not records:
        print(f"No agent_results.jsonl files found under {args.results_dir}")
        return

    print("Loading grouped traces...")
    grouped_traces, _ = load_traces_grouped(args.traces_dir)

    if model_filters:
        records = [r for r in records if _keep_model(_split_cm_key(r.get("_cm_key", ""))[0])]
        by_key_records = {k: v for k, v in by_key_records.items() if _keep_model(_split_cm_key(k)[0])}
        grouped_traces = {k: v for k, v in grouped_traces.items() if _keep_model(_split_cm_key(k)[0])}

    print("Running EM/F1...")
    em = run_em(records)

    print("Running discovery metrics...")
    discovery = run_discovery(grouped_traces, args.tasks_dir)

    print("Running failure attribution...")
    failure = run_failure(by_key_records, grouped_traces, args.tasks_dir)

    print("Running semantic outcome buckets...")
    semantic_outcomes = run_semantic_outcomes(by_key_records, args.logs_dir)

    print("Running efficiency...")
    efficiency = run_efficiency(by_key_records)

    print("Running tools discovery...")
    tools_discovery = run_tools_discovery(grouped_traces, args.tasks_dir)

    print("Running search depth curve...")
    search_depth = run_search_depth(records)

    print("Running reasoning density curve...")
    reasoning_density = run_reasoning_density(records, args.tasks_dir)

    print("Running tool error rates...")
    tool_errors = run_tool_errors(by_key_records)

    print("Building summaries...")
    summary = build_summary(
        em,
        discovery,
        failure,
        efficiency,
        semantic_outcomes,
        search_depth,
        reasoning_density,
        tool_errors,
    )
    variant_summary = build_variant_summary(summary)

    files = {
        "em_f1.json": em,
        "discovery.json": {
            k: {kk: vv for kk, vv in v.items() if kk != "task_metrics"}
            for k, v in discovery.items()
        },
        "tools_discovery.json": tools_discovery,
        "failure.json": failure,
        "semantic_outcomes.json": semantic_outcomes,
        "efficiency.json": efficiency,
        "search_depth.json": search_depth,
        "reasoning_density.json": reasoning_density,
        "tool_errors.json": tool_errors,
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

    print(f"\nSummary ({len(summary)} model\u00d7variant rows):")
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
            f"  {row['variant']:<40} "
            f"EM={em_pct:<7} D_ret={row.get('D_ret')} "
            f"D_acc={row.get('D_acc')} n={row.get('n_total')}"
        )

    if args.no_figures:
        print("\nSkipping figures (--no-figures).")
    else:
        print("\nGenerating figures...")
        try:
            generate_mode_figures(
                args.results_dir, args.traces_dir, args.tasks_dir, out_dir, args.model_filter
            )
            print(f"Figures written to {out_dir / 'figures'}")
        except subprocess.CalledProcessError as exc:
            print(f"Figure generation failed with exit code {exc.returncode}.")


if __name__ == "__main__":
    main()
