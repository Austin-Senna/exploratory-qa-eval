#!/usr/bin/env python3
"""
Semantic-first mode analysis runner.

Reads semantic-audited eval_results.csv files from:
  results-ec2_semantic/modes/{model}/{variant}/eval_results.csv

Optionally joins discovery metrics from traces:
  results-ec2/traces/modes/{model}/{variant}/{task_dir}/{task}.jsonl

Outputs (default: analysis_results_mode_semantic/):
  semantic_match.json
  discovery.json
  runtime.json
  semantic_buckets.json
  log_error_buckets.json
  search_depth_buckets.json
  reasoning_density_buckets.json
  semantic_error_crosstab.json
  summary.json
  variant_summary.json
  per_task_semantic.csv
  figures/ (unless --no-figures)
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.discovery_metrics import compute_discovery_metrics, load_task_gold_ids, make_task_stem_key
from analysis.reasoning_density import load_task_gold_counts
from analysis.reasoning_density import _BINS as _REASONING_DENSITY_BINS
from analysis.reasoning_density import _assign_bin as _assign_reasoning_density_bin
from analysis.search_depth import _BINS as _SEARCH_DEPTH_BINS
from analysis.search_depth import _assign_bin as _assign_search_depth_bin


SEMANTIC_BUCKETS = [
    "semantic_correct",
    "semantic_incorrect",
    "answer_unknown_blank",
]

SOURCE_LOG_ERROR_BUCKETS = [
    "",
    "error_turns_exhausted",
    "error_tools_limit",
    "error_tokens_reached",
    "error_context_overflow",
    "error_event_loop",
    "error_unknown",
]

DISPLAY_LOG_ERROR_BUCKETS = [
    "no_error",
    "error_turns_exhausted",
    "error_tools_limit",
    "error_tokens_reached",
    "error_context_overflow",
    "error_event_loop",
    "error_unknown",
]

REQUIRED_FIELDS = [
    "exact_match",
    "semantic_match",
    "semantic_reason",
    "semantic_bucket",
    "log_error_bucket",
    "log_error_evidence",
]

SEMANTIC_BUCKET_COLORS = {
    "semantic_correct": "#2E8B57",
    "semantic_incorrect": "#C07A2C",
    "answer_unknown_blank": "#C44E52",
}

LOG_ERROR_BUCKET_COLORS = {
    "no_error": "#2E8B57",
    "error_turns_exhausted": "#C44E52",
    "error_tools_limit": "#E17C05",
    "error_tokens_reached": "#7A3E9D",
    "error_context_overflow": "#9467BD",
    "error_event_loop": "#7F7F7F",
    "error_unknown": "#BCBD22",
}

METRIC_COLORS = {
    "semantic_match": "#2E8B57",
    "D_ret": "#1F77B4",
    "D_acc": "#FF7F0E",
}

METRIC_LABELS = {
    "semantic_match": "Semantic Match",
    "D_ret": "D_ret",
    "D_acc": "D_acc",
}

_LETTER_TO_MODE = {"n": "naive", "d": "standard", "i": "ideal"}
_MODE_PRIORITY = {"ideal": 0, "standard": 1, "naive": 2, None: 3}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results-ec2_semantic/modes")
    parser.add_argument("--traces-dir", default="results-ec2/traces/modes")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results_mode_semantic")
    parser.add_argument(
        "--no-figures",
        action="store_true",
        help="Skip graph generation.",
    )
    parser.add_argument(
        "--model-filter",
        default=None,
        help="Substring filter on model directory name (comma-separated OR).",
    )
    return parser.parse_args()


def as_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _cm_key(model: str, variant: str) -> str:
    return f"{model}/{variant}"


def _split_cm_key(key: str) -> Tuple[str, str]:
    parts = key.split("/", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return "unknown", key


def _parse_variant(variant: str) -> Dict[str, Optional[object]]:
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


def _variant_sort_key(variant: str) -> tuple:
    axes = _parse_variant(variant)
    search_tool = axes.get("search_tool")
    agent_management = axes.get("agent_management")

    if search_tool == "ideal" and agent_management == "ideal":
        ideal_group = 0
    elif search_tool == "ideal":
        ideal_group = 1
    elif agent_management == "ideal":
        ideal_group = 2
    else:
        ideal_group = 3

    return (
        ideal_group,
        _MODE_PRIORITY.get(search_tool, 4),
        _MODE_PRIORITY.get(agent_management, 4),
        _MODE_PRIORITY.get(axes.get("search_results"), 4),
        axes.get("k") if axes.get("k") is not None else 10**9,
        axes.get("sc") if axes.get("sc") is not None else 10**9,
        variant,
    )


def _condition_model_sort_key(key: str) -> tuple:
    model, variant = _split_cm_key(key)
    return (*_variant_sort_key(variant), model)


def _sort_summary_rows(rows: List[dict]) -> List[dict]:
    return sorted(
        rows,
        key=lambda row: (
            *_variant_sort_key(str(row.get("variant", ""))),
            str(row.get("model", "")),
            str(row.get("condition_model", "")),
        ),
    )


def _sort_variant_rows(rows: List[dict]) -> List[dict]:
    return sorted(rows, key=lambda row: _variant_sort_key(str(row.get("variant", ""))))


def _parse_results_csv_path(path: Path, results_root: Path) -> Tuple[str, str]:
    rel = path.relative_to(results_root)
    parts = rel.parts
    if len(parts) >= 3 and parts[-1] == "eval_results.csv":
        return parts[-3], parts[-2]
    raise ValueError(f"Expected <results>/<model>/<variant>/eval_results.csv layout, got {path}")


def _parse_trace_jsonl_path(path: Path, traces_root: Path) -> Tuple[str, str, str]:
    rel = path.relative_to(traces_root)
    parts = rel.parts
    if len(parts) >= 4:
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return parts[-4], parts[-3], task_id
    raise ValueError(f"Expected <traces>/<model>/<variant>/<task_dir>/<task>.jsonl layout, got {path}")


def _validate_required_fields(fieldnames: List[str] | None, path: Path) -> None:
    available = fieldnames or []
    missing = [field for field in REQUIRED_FIELDS if field not in available]
    if missing:
        raise ValueError(f"Missing required semantic columns in {path}: {', '.join(missing)}")


def _normalize_log_error_bucket(value: str) -> str:
    normalized = str(value or "").strip()
    if normalized not in SOURCE_LOG_ERROR_BUCKETS:
        raise ValueError(f"Unexpected log_error_bucket value: {normalized!r}")
    return normalized if normalized else "no_error"


def _extend_field_order(field_order: List[str], new_fields: Iterable[str]) -> None:
    for field in new_fields:
        if field not in field_order:
            field_order.append(field)


def _mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def _round_or_none(value: Optional[float], digits: int = 4) -> Optional[float]:
    if value is None:
        return None
    return round(value, digits)


def _weighted_avg(rows: List[dict], field: str, weight_field: str = "n") -> Optional[float]:
    numerator = 0.0
    denominator = 0.0
    for row in rows:
        value = row.get(field)
        weight = row.get(weight_field)
        if value is None or weight in (None, 0):
            continue
        numerator += float(value) * float(weight)
        denominator += float(weight)
    if denominator == 0:
        return None
    return numerator / denominator


def _normalize_eval_row(row: dict, model: str, variant: str, csv_path: Path) -> dict:
    semantic_bucket = str(row.get("semantic_bucket", "") or "").strip()
    if semantic_bucket not in SEMANTIC_BUCKETS:
        raise ValueError(f"Unexpected semantic_bucket in {csv_path}: {semantic_bucket!r}")

    semantic_match = int(as_float(row.get("semantic_match")))
    if semantic_match not in (0, 1):
        raise ValueError(f"semantic_match must be 0 or 1 in {csv_path}, got {row.get('semantic_match')!r}")
    if semantic_bucket == "semantic_correct" and semantic_match != 1:
        raise ValueError(f"semantic_correct rows must set semantic_match=1 in {csv_path}")
    if semantic_bucket != "semantic_correct" and semantic_match != 0:
        raise ValueError(f"Non-correct semantic buckets must set semantic_match=0 in {csv_path}")

    key = _cm_key(model, variant)
    axes = _parse_variant(variant)
    task_id = str(row.get("task_id", "") or "")

    normalized = dict(row)
    normalized["condition_model"] = key
    normalized["variant"] = variant
    normalized["model_dir"] = model
    normalized["search_tool"] = axes["search_tool"]
    normalized["search_results"] = axes["search_results"]
    normalized["agent_management"] = axes["agent_management"]
    normalized["k"] = axes["k"]
    normalized["sc"] = axes["sc"]
    normalized["task_stem"] = make_task_stem_key(task_id) if task_id else ""
    normalized["log_error_bucket_display"] = _normalize_log_error_bucket(row.get("log_error_bucket", ""))

    normalized["_cm_key"] = key
    normalized["_semantic_match"] = semantic_match
    normalized["_runtime_seconds"] = as_float(row.get("runtime_seconds"))
    normalized["_input_tokens"] = as_float(row.get("input_tokens"))
    normalized["_output_tokens"] = as_float(row.get("output_tokens"))
    normalized["_total_tokens"] = as_float(row.get("total_tokens"))
    normalized["_cost_usd"] = as_float(row.get("cost_usd"))
    normalized["_tool_calls_total"] = as_float(row.get("tool_calls_total"))
    normalized["_api_tool_calls"] = as_float(row.get("api_tool_calls"))
    return normalized


def load_semantic_results_grouped(
    results_dir: str,
    model_filters: Optional[List[str]] = None,
) -> Tuple[Dict[str, List[dict]], List[str]]:
    root = Path(results_dir)
    if not root.exists():
        raise FileNotFoundError(f"Results directory does not exist: {root}")

    def keep_model(model: str) -> bool:
        if not model_filters:
            return True
        lowered = model.lower()
        return any(token in lowered for token in model_filters)

    by_key: Dict[str, List[dict]] = defaultdict(list)
    field_order: List[str] = []
    found = False

    for csv_path in sorted(root.rglob("eval_results.csv")):
        model, variant = _parse_results_csv_path(csv_path, root)
        if not keep_model(model):
            continue
        found = True
        with csv_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            _validate_required_fields(reader.fieldnames, csv_path)
            _extend_field_order(field_order, reader.fieldnames or [])
            for row in reader:
                by_key[_cm_key(model, variant)].append(_normalize_eval_row(row, model, variant, csv_path))

    if not found:
        raise FileNotFoundError(f"No eval_results.csv files found under {root}")

    return dict(by_key), field_order


def load_traces_grouped(
    traces_dir: str,
    model_filters: Optional[List[str]] = None,
) -> Dict[str, dict]:
    root = Path(traces_dir)
    if not root.exists():
        return {}

    def keep_model(model: str) -> bool:
        if not model_filters:
            return True
        lowered = model.lower()
        return any(token in lowered for token in model_filters)

    grouped: Dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for jsonl_path in sorted(root.rglob("*.jsonl")):
        model, variant, task_id = _parse_trace_jsonl_path(jsonl_path, root)
        if not keep_model(model):
            continue
        key = _cm_key(model, variant)
        with jsonl_path.open() as handle:
            for line in handle:
                line = line.strip()
                if line:
                    grouped[key][task_id].append(json.loads(line))
    return {key: dict(value) for key, value in grouped.items()}


def run_discovery(grouped_traces: Dict[str, dict], tasks_dir: str) -> Tuple[dict, Dict[str, Dict[str, dict]]]:
    tasks_root = Path(tasks_dir)
    if not grouped_traces or not tasks_root.exists():
        return {}, {}

    task_gold = load_task_gold_ids(tasks_dir)
    aggregates: dict = {}
    task_metrics_by_key: Dict[str, Dict[str, dict]] = {}

    for key, traces in sorted(grouped_traces.items(), key=lambda item: _condition_model_sort_key(item[0])):
        metrics = compute_discovery_metrics(traces, task_gold)
        aggregate = metrics.get("aggregate", {})
        if aggregate:
            aggregates[key] = aggregate
        task_metrics_by_key[key] = {
            str(task_metric.get("task_id", "")): task_metric for task_metric in metrics.get("task_metrics", [])
        }

    return aggregates, task_metrics_by_key


def build_summary(by_key_records: Dict[str, List[dict]], discovery: dict) -> List[dict]:
    rows: List[dict] = []
    for key in sorted(by_key_records.keys(), key=_condition_model_sort_key):
        records = by_key_records[key]
        model, variant = _split_cm_key(key)
        axes = _parse_variant(variant)
        n = len(records)
        semantic_counts = Counter(str(record.get("semantic_bucket", "")) for record in records)
        error_counts = Counter(str(record.get("log_error_bucket_display", "")) for record in records)

        row = {
            "condition_model": key,
            "model": model,
            "variant": variant,
            "search_tool": axes["search_tool"],
            "search_results": axes["search_results"],
            "agent_management": axes["agent_management"],
            "k": axes["k"],
            "sc": axes["sc"],
            "n": n,
            "semantic_match": _round_or_none(_mean([record["_semantic_match"] for record in records])),
            "avg_runtime_seconds": _round_or_none(_mean([record["_runtime_seconds"] for record in records])),
            "avg_input_tokens": _round_or_none(_mean([record["_input_tokens"] for record in records])),
            "avg_output_tokens": _round_or_none(_mean([record["_output_tokens"] for record in records])),
            "avg_total_tokens": _round_or_none(_mean([record["_total_tokens"] for record in records])),
            "avg_cost_usd": _round_or_none(_mean([record["_cost_usd"] for record in records])),
            "total_cost_usd": round(sum(record["_cost_usd"] for record in records), 4),
            "avg_tool_calls_total": _round_or_none(_mean([record["_tool_calls_total"] for record in records])),
            "avg_api_tool_calls": _round_or_none(_mean([record["_api_tool_calls"] for record in records])),
        }

        discovery_row = discovery.get(key, {})
        if discovery_row:
            row["D_ret"] = _round_or_none(discovery_row.get("D_ret"))
            row["D_ret_precision"] = _round_or_none(discovery_row.get("D_ret_precision"))
            row["D_ret_f1"] = _round_or_none(discovery_row.get("D_ret_f1"))
            row["D_acc"] = _round_or_none(discovery_row.get("D_acc"))
            row["D_acc_precision"] = _round_or_none(discovery_row.get("D_acc_precision"))
            row["D_acc_recall"] = _round_or_none(discovery_row.get("D_acc_recall"))
            row["D_acc_f1"] = _round_or_none(discovery_row.get("D_acc_f1"))
            row["search_avg_precision"] = _round_or_none(discovery_row.get("avg_precision"))
            row["search_avg_recall"] = _round_or_none(discovery_row.get("avg_recall"))
            row["search_avg_f1"] = _round_or_none(discovery_row.get("avg_f1"))
            row["avg_search_calls"] = _round_or_none(discovery_row.get("avg_search_calls"))
            row["avg_read_calls"] = _round_or_none(discovery_row.get("avg_read_calls"))
            avg_search_calls = discovery_row.get("avg_search_calls")
            semantic_match = row.get("semantic_match")
            row["search_efficiency"] = (
                round(float(semantic_match) / float(avg_search_calls), 4)
                if semantic_match is not None and avg_search_calls
                else None
            )
        else:
            row["D_ret"] = None
            row["D_ret_precision"] = None
            row["D_ret_f1"] = None
            row["D_acc"] = None
            row["D_acc_precision"] = None
            row["D_acc_recall"] = None
            row["D_acc_f1"] = None
            row["search_avg_precision"] = None
            row["search_avg_recall"] = None
            row["search_avg_f1"] = None
            row["avg_search_calls"] = None
            row["avg_read_calls"] = None
            row["search_efficiency"] = None

        for bucket in SEMANTIC_BUCKETS:
            count = semantic_counts.get(bucket, 0)
            row[bucket] = count
            row[f"{bucket}_rate"] = round(count / n, 4) if n else 0.0

        for bucket in DISPLAY_LOG_ERROR_BUCKETS:
            count = error_counts.get(bucket, 0)
            row[bucket] = count
            row[f"{bucket}_rate"] = round(count / n, 4) if n else 0.0

        rows.append(row)

    return _sort_summary_rows(rows)


def build_variant_summary(summary_rows: List[dict]) -> List[dict]:
    groups: Dict[str, List[dict]] = defaultdict(list)
    for row in summary_rows:
        groups[str(row.get("variant", "unknown"))].append(row)

    out: List[dict] = []
    for variant, rows in sorted(groups.items(), key=lambda item: _variant_sort_key(item[0])):
        axes = _parse_variant(variant)
        total_n = sum(int(row.get("n", 0) or 0) for row in rows)
        variant_row = {
            "variant": variant,
            "search_tool": axes["search_tool"],
            "search_results": axes["search_results"],
            "agent_management": axes["agent_management"],
            "k": axes["k"],
            "sc": axes["sc"],
            "n_total": total_n,
            "num_model_rows": len(rows),
            "models": sorted({str(row.get("model", "")) for row in rows if row.get("model")}),
            "semantic_match": _round_or_none(_weighted_avg(rows, "semantic_match")),
            "D_ret": _round_or_none(_weighted_avg(rows, "D_ret")),
            "D_ret_precision": _round_or_none(_weighted_avg(rows, "D_ret_precision")),
            "D_ret_f1": _round_or_none(_weighted_avg(rows, "D_ret_f1")),
            "D_acc": _round_or_none(_weighted_avg(rows, "D_acc")),
            "D_acc_precision": _round_or_none(_weighted_avg(rows, "D_acc_precision")),
            "D_acc_recall": _round_or_none(_weighted_avg(rows, "D_acc_recall")),
            "D_acc_f1": _round_or_none(_weighted_avg(rows, "D_acc_f1")),
            "search_avg_precision": _round_or_none(_weighted_avg(rows, "search_avg_precision")),
            "search_avg_recall": _round_or_none(_weighted_avg(rows, "search_avg_recall")),
            "search_avg_f1": _round_or_none(_weighted_avg(rows, "search_avg_f1")),
            "avg_search_calls": _round_or_none(_weighted_avg(rows, "avg_search_calls")),
            "avg_read_calls": _round_or_none(_weighted_avg(rows, "avg_read_calls")),
            "avg_runtime_seconds": _round_or_none(_weighted_avg(rows, "avg_runtime_seconds")),
            "avg_input_tokens": _round_or_none(_weighted_avg(rows, "avg_input_tokens")),
            "avg_output_tokens": _round_or_none(_weighted_avg(rows, "avg_output_tokens")),
            "avg_total_tokens": _round_or_none(_weighted_avg(rows, "avg_total_tokens")),
            "avg_cost_usd": _round_or_none(_weighted_avg(rows, "avg_cost_usd")),
            "total_cost_usd": round(sum(float(row.get("total_cost_usd", 0) or 0) for row in rows), 4),
            "avg_tool_calls_total": _round_or_none(_weighted_avg(rows, "avg_tool_calls_total")),
            "avg_api_tool_calls": _round_or_none(_weighted_avg(rows, "avg_api_tool_calls")),
        }
        avg_search_calls = variant_row.get("avg_search_calls")
        semantic_match = variant_row.get("semantic_match")
        variant_row["search_efficiency"] = (
            round(float(semantic_match) / float(avg_search_calls), 4)
            if semantic_match is not None and avg_search_calls
            else None
        )

        for bucket in SEMANTIC_BUCKETS:
            count = sum(int(row.get(bucket, 0) or 0) for row in rows)
            variant_row[bucket] = count
            variant_row[f"{bucket}_rate"] = round(count / total_n, 4) if total_n else 0.0

        for bucket in DISPLAY_LOG_ERROR_BUCKETS:
            count = sum(int(row.get(bucket, 0) or 0) for row in rows)
            variant_row[bucket] = count
            variant_row[f"{bucket}_rate"] = round(count / total_n, 4) if total_n else 0.0

        out.append(variant_row)

    return _sort_variant_rows(out)


def build_metric_mappings(summary_rows: List[dict]) -> Tuple[dict, dict, dict, dict, dict]:
    semantic_match = {}
    discovery = {}
    runtime = {}
    semantic_buckets = {}
    log_error_buckets = {}

    for row in summary_rows:
        key = str(row["condition_model"])
        semantic_match[key] = {
            "n": row.get("n"),
            "semantic_match": row.get("semantic_match"),
        }
        discovery[key] = {
            "n": row.get("n"),
            "D_ret": row.get("D_ret"),
            "D_ret_precision": row.get("D_ret_precision"),
            "D_ret_f1": row.get("D_ret_f1"),
            "D_acc": row.get("D_acc"),
            "D_acc_precision": row.get("D_acc_precision"),
            "D_acc_recall": row.get("D_acc_recall"),
            "D_acc_f1": row.get("D_acc_f1"),
            "search_avg_precision": row.get("search_avg_precision"),
            "search_avg_recall": row.get("search_avg_recall"),
            "search_avg_f1": row.get("search_avg_f1"),
            "avg_search_calls": row.get("avg_search_calls"),
            "avg_read_calls": row.get("avg_read_calls"),
            "search_efficiency": row.get("search_efficiency"),
        }
        runtime[key] = {
            "n": row.get("n"),
            "avg_runtime_seconds": row.get("avg_runtime_seconds"),
            "avg_input_tokens": row.get("avg_input_tokens"),
            "avg_output_tokens": row.get("avg_output_tokens"),
            "avg_total_tokens": row.get("avg_total_tokens"),
            "avg_cost_usd": row.get("avg_cost_usd"),
            "total_cost_usd": row.get("total_cost_usd"),
            "avg_tool_calls_total": row.get("avg_tool_calls_total"),
            "avg_api_tool_calls": row.get("avg_api_tool_calls"),
        }
        semantic_buckets[key] = {"total": row.get("n")}
        for bucket in SEMANTIC_BUCKETS:
            semantic_buckets[key][bucket] = row.get(bucket, 0)
            semantic_buckets[key][f"{bucket}_rate"] = row.get(f"{bucket}_rate")
        log_error_buckets[key] = {"total": row.get("n")}
        for bucket in DISPLAY_LOG_ERROR_BUCKETS:
            log_error_buckets[key][bucket] = row.get(bucket, 0)
            log_error_buckets[key][f"{bucket}_rate"] = row.get(f"{bucket}_rate")

    return semantic_match, discovery, runtime, semantic_buckets, log_error_buckets


def build_semantic_error_crosstab(
    by_key_records: Dict[str, List[dict]],
    variant_summary: List[dict],
) -> List[dict]:
    rows: List[dict] = []

    def add_rows(level: str, model: Optional[str], variant: str, records: List[dict]) -> None:
        total = len(records)
        counts: Counter = Counter(
            (str(record.get("semantic_bucket", "")), str(record.get("log_error_bucket_display", "")))
            for record in records
        )
        for semantic_bucket in SEMANTIC_BUCKETS:
            for log_error_bucket in DISPLAY_LOG_ERROR_BUCKETS:
                count = counts.get((semantic_bucket, log_error_bucket), 0)
                rows.append(
                    {
                        "level": level,
                        "model": model,
                        "variant": variant,
                        "semantic_bucket": semantic_bucket,
                        "log_error_bucket": log_error_bucket,
                        "n": count,
                        "total": total,
                        "pct_within_group": round(count / total, 4) if total else 0.0,
                    }
                )

    for key in sorted(by_key_records.keys(), key=_condition_model_sort_key):
        model, variant = _split_cm_key(key)
        add_rows("model_variant", model, variant, by_key_records[key])

    grouped_by_variant: Dict[str, List[dict]] = defaultdict(list)
    for records in by_key_records.values():
        for record in records:
            grouped_by_variant[str(record.get("variant", "unknown"))].append(record)

    for row in variant_summary:
        variant = str(row.get("variant", "unknown"))
        add_rows("variant", None, variant, grouped_by_variant.get(variant, []))

    return rows


def _empty_bucket_entry() -> dict:
    entry = {"n": 0}
    for bucket in SEMANTIC_BUCKETS:
        entry[bucket] = 0
        entry[f"{bucket}_rate"] = 0.0
    for bucket in DISPLAY_LOG_ERROR_BUCKETS:
        entry[bucket] = 0
        entry[f"{bucket}_rate"] = 0.0
    return entry


def _finalize_bucket_entry(entry: dict) -> dict:
    total = int(entry.get("n", 0) or 0)
    for bucket in SEMANTIC_BUCKETS:
        count = int(entry.get(bucket, 0) or 0)
        entry[f"{bucket}_rate"] = round(count / total, 4) if total else 0.0
    for bucket in DISPLAY_LOG_ERROR_BUCKETS:
        count = int(entry.get(bucket, 0) or 0)
        entry[f"{bucket}_rate"] = round(count / total, 4) if total else 0.0
    return entry


def _update_bucket_entry(entry: dict, record: dict) -> None:
    entry["n"] = int(entry.get("n", 0) or 0) + 1
    semantic_bucket = str(record.get("semantic_bucket", ""))
    log_error_bucket = str(record.get("log_error_bucket_display", ""))
    if semantic_bucket in SEMANTIC_BUCKETS:
        entry[semantic_bucket] = int(entry.get(semantic_bucket, 0) or 0) + 1
    if log_error_bucket in DISPLAY_LOG_ERROR_BUCKETS:
        entry[log_error_bucket] = int(entry.get(log_error_bucket, 0) or 0) + 1


def _init_binned_outcome_row(model: str, variant: str, bin_labels: List[str]) -> dict:
    axes = _parse_variant(variant)
    return {
        "model": model,
        "variant": variant,
        "search_tool": axes["search_tool"],
        "search_results": axes["search_results"],
        "agent_management": axes["agent_management"],
        "k": axes["k"],
        "sc": axes["sc"],
        "bins": {label: _empty_bucket_entry() for label in bin_labels},
    }


def build_search_depth_buckets(
    by_key_records: Dict[str, List[dict]],
    task_metrics_by_key: Dict[str, Dict[str, dict]],
) -> dict:
    bin_labels = [label for label, _ in _SEARCH_DEPTH_BINS]
    out: dict = {}
    for key in sorted(by_key_records.keys(), key=_condition_model_sort_key):
        model, variant = _split_cm_key(key)
        row = _init_binned_outcome_row(model, variant, bin_labels)
        task_metrics = task_metrics_by_key.get(key, {})
        for record in by_key_records[key]:
            task_metric = task_metrics.get(str(record.get("task_stem", "")))
            if not task_metric:
                continue
            search_calls = int(task_metric.get("num_search_calls", 0) or 0)
            if search_calls <= 0:
                continue
            bin_label = _assign_search_depth_bin(search_calls)
            _update_bucket_entry(row["bins"][bin_label], record)
        for label in bin_labels:
            row["bins"][label] = _finalize_bucket_entry(row["bins"][label])
        out[key] = row
    return out


def build_reasoning_density_buckets(
    by_key_records: Dict[str, List[dict]],
    tasks_dir: str,
) -> dict:
    bin_labels = [label for label, _ in _REASONING_DENSITY_BINS]
    task_gold_counts = load_task_gold_counts(tasks_dir)
    out: dict = {}
    for key in sorted(by_key_records.keys(), key=_condition_model_sort_key):
        model, variant = _split_cm_key(key)
        row = _init_binned_outcome_row(model, variant, bin_labels)
        for record in by_key_records[key]:
            task_stem = str(record.get("task_stem", ""))
            n_docs = task_gold_counts.get(task_stem)
            if n_docs is None:
                continue
            bin_label = _assign_reasoning_density_bin(n_docs)
            _update_bucket_entry(row["bins"][bin_label], record)
        for label in bin_labels:
            row["bins"][label] = _finalize_bucket_entry(row["bins"][label])
        out[key] = row
    return out


def build_per_task_rows(
    by_key_records: Dict[str, List[dict]],
    task_metrics_by_key: Dict[str, Dict[str, dict]],
    source_field_order: List[str],
) -> Tuple[List[dict], List[str]]:
    discovery_fields = [
        "D_ret",
        "D_ret_precision",
        "D_ret_f1",
        "D_acc",
        "D_acc_precision",
        "D_acc_recall",
        "D_acc_f1",
        "search_precision",
        "search_recall",
        "search_f1",
        "num_search_calls",
        "num_read_calls",
        "retrieved_gold_dataset_ids",
    ]
    output_rows: List[dict] = []

    for key in sorted(by_key_records.keys(), key=_condition_model_sort_key):
        model, variant = _split_cm_key(key)
        axes = _parse_variant(variant)
        task_metrics = task_metrics_by_key.get(key, {})
        for record in sorted(by_key_records[key], key=lambda row: str(row.get("task_id", ""))):
            task_metric = task_metrics.get(str(record.get("task_stem", "")), {})
            output_row = {
                "condition_model": key,
                "model_dir": model,
                "variant": variant,
                "search_tool": axes["search_tool"],
                "search_results": axes["search_results"],
                "agent_management": axes["agent_management"],
                "k": axes["k"],
                "sc": axes["sc"],
                "task_stem": record.get("task_stem", ""),
                "log_error_bucket_display": record.get("log_error_bucket_display", ""),
                "D_ret": _round_or_none(task_metric.get("d_ret"), 6),
                "D_ret_precision": _round_or_none(task_metric.get("d_ret_precision"), 6),
                "D_ret_f1": _round_or_none(task_metric.get("d_ret_f1"), 6),
                "D_acc": _round_or_none(task_metric.get("d_acc"), 6),
                "D_acc_precision": _round_or_none(task_metric.get("d_acc_precision"), 6),
                "D_acc_recall": _round_or_none(task_metric.get("d_acc_recall"), 6),
                "D_acc_f1": _round_or_none(task_metric.get("d_acc_f1"), 6),
                "search_precision": _round_or_none(task_metric.get("precision"), 6),
                "search_recall": _round_or_none(task_metric.get("recall"), 6),
                "search_f1": _round_or_none(task_metric.get("f1"), 6),
                "num_search_calls": task_metric.get("num_search_calls"),
                "num_read_calls": task_metric.get("num_read_calls"),
                "retrieved_gold_dataset_ids": ",".join(task_metric.get("retrieved_gold_dataset_ids", [])),
            }
            for field in source_field_order:
                output_row[field] = record.get(field, "")
            output_rows.append(output_row)

    fieldnames = [
        "condition_model",
        "model_dir",
        "variant",
        "search_tool",
        "search_results",
        "agent_management",
        "k",
        "sc",
        "task_stem",
    ] + source_field_order + ["log_error_bucket_display"] + discovery_fields

    deduped_fieldnames: List[str] = []
    for field in fieldnames:
        if field not in deduped_fieldnames:
            deduped_fieldnames.append(field)

    return output_rows, deduped_fieldnames


def write_json(path: Path, data: object) -> None:
    with path.open("w") as handle:
        json.dump(data, handle, indent=2)


def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _import_plot_libs():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except ImportError:
        print("Skipping figures: matplotlib is not installed.")
        return None


def _pretty_model(model_name: str) -> str:
    label = model_name.split("/")[-1]
    label = label.replace("bedrock_", "").replace("openai_", "")
    if label.endswith("-arn"):
        label = label[:-4]
    return label


def _model_variant_label(row: dict) -> str:
    return f"{_pretty_model(str(row.get('model', '')))}\n{row.get('variant', '')}"


def _plot_metric_bars(plt, rows: List[dict], label_fn, title: str, output_path: Path) -> None:
    metric_specs = [
        (field, METRIC_LABELS[field], METRIC_COLORS[field])
        for field in ("semantic_match", "D_ret", "D_acc")
        if any(row.get(field) is not None for row in rows)
    ]
    if not rows or not metric_specs:
        return

    labels = [label_fn(row) for row in rows]
    x_positions = list(range(len(rows)))
    width = 0.8 / len(metric_specs)
    fig_width = max(10, len(rows) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    for idx, (field, label, color) in enumerate(metric_specs):
        values = [(float(row.get(field) or 0.0) * 100.0) for row in rows]
        offset = (idx - len(metric_specs) / 2 + 0.5) * width
        bars = ax.bar(
            [position + offset for position in x_positions],
            values,
            width=width * 0.9,
            label=label,
            color=color,
        )
        for bar, value in zip(bars, values):
            if value < 4.0:
                continue
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 1.0,
                f"{value:.0f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Rate (%)")
    ax.set_title(title)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    fig.tight_layout(rect=(0, 0, 0.84, 1))
    fig.savefig(output_path)
    plt.close(fig)


def _hex_to_rgb(color: str) -> Tuple[float, float, float]:
    value = color.lstrip("#")
    if len(value) != 6:
        return (0.0, 0.0, 0.0)
    return tuple(int(value[idx : idx + 2], 16) / 255.0 for idx in (0, 2, 4))


def _label_text_color(fill_color: str) -> str:
    red, green, blue = _hex_to_rgb(fill_color)
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return "black" if luminance > 0.62 else "white"


def _plot_stacked_buckets_on_ax(
    ax,
    rows: List[dict],
    *,
    buckets: List[str],
    colors: Dict[str, str],
    label_fn,
    total_field: str,
    title: str,
    show_xticklabels: bool = True,
    label_min_pct: float = 6.0,
    show_legend: bool = True,
) -> None:
    if not rows:
        return

    labels = [label_fn(row) for row in rows]
    x_positions = list(range(len(rows)))
    bottoms = [0.0 for _ in rows]

    for bucket in buckets:
        heights = []
        counts = []
        for row in rows:
            total = float(row.get(total_field) or 0.0)
            count = float(row.get(bucket) or 0.0)
            counts.append(int(count))
            heights.append((count / total) * 100.0 if total else 0.0)
        bars = ax.bar(
            x_positions,
            heights,
            bottom=bottoms,
            color=colors[bucket],
            label=bucket,
        )
        label_color = _label_text_color(colors[bucket])
        for bar, height, count, bottom in zip(bars, heights, counts, bottoms):
            if count <= 0 or height < label_min_pct:
                continue
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bottom + height / 2,
                str(count),
                ha="center",
                va="center",
                fontsize=8,
                color=label_color,
            )
        bottoms = [bottom + height for bottom, height in zip(bottoms, heights)]

    ax.set_xticks(x_positions)
    if show_xticklabels:
        ax.set_xticklabels(labels, rotation=30, ha="right")
    else:
        ax.set_xticklabels([])
    ax.set_ylabel("Share of Tasks (%)")
    ax.set_title(title)
    ax.set_ylim(0, 100)
    if show_legend:
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)


def _plot_stacked_buckets(
    plt,
    rows: List[dict],
    *,
    buckets: List[str],
    colors: Dict[str, str],
    label_fn,
    total_field: str,
    title: str,
    output_path: Path,
) -> None:
    if not rows:
        return

    fig_width = max(10, len(rows) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    _plot_stacked_buckets_on_ax(
        ax,
        rows,
        buckets=buckets,
        colors=colors,
        label_fn=label_fn,
        total_field=total_field,
        title=title,
        show_xticklabels=True,
        show_legend=True,
    )
    fig.tight_layout(rect=(0, 0, 0.84, 1))
    fig.savefig(output_path)
    plt.close(fig)


def _plot_combined_model_variant_buckets(
    plt,
    rows: List[dict],
    output_path: Path,
) -> None:
    if not rows:
        return

    fig_width = max(10, len(rows) * 0.8)
    fig, axes = plt.subplots(2, 1, figsize=(fig_width, 11), sharex=True)
    semantic_ax, error_ax = axes

    _plot_stacked_buckets_on_ax(
        semantic_ax,
        rows,
        buckets=SEMANTIC_BUCKETS,
        colors=SEMANTIC_BUCKET_COLORS,
        label_fn=_model_variant_label,
        total_field="n",
        title="Semantic Bucket Distribution by Model x Variant",
        show_xticklabels=False,
        show_legend=True,
    )
    _plot_stacked_buckets_on_ax(
        error_ax,
        rows,
        buckets=DISPLAY_LOG_ERROR_BUCKETS,
        colors=LOG_ERROR_BUCKET_COLORS,
        label_fn=_model_variant_label,
        total_field="n",
        title="Log Error Bucket Distribution by Model x Variant",
        show_xticklabels=True,
        show_legend=True,
    )

    fig.subplots_adjust(top=0.94, bottom=0.18, left=0.06, right=0.82, hspace=0.28)
    fig.savefig(output_path)
    plt.close(fig)


def _plot_binned_bucket_panels(
    plt,
    binned_rows: dict,
    *,
    bin_labels: List[str],
    buckets: List[str],
    colors: Dict[str, str],
    panel_title_fn,
    figure_title: str,
    x_label: str,
    output_path: Path,
) -> None:
    if not binned_rows:
        return

    ordered_keys = sorted(binned_rows.keys(), key=_condition_model_sort_key)
    n_panels = len(ordered_keys)
    ncols = 2 if n_panels > 1 else 1
    nrows = math.ceil(n_panels / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(8 * ncols, 4.6 * nrows), sharey=True)
    axes_list = axes.flatten().tolist() if hasattr(axes, "flatten") else [axes]

    for ax, key in zip(axes_list, ordered_keys):
        row = binned_rows[key]
        plot_rows = []
        for bin_label in bin_labels:
            bin_entry = dict(row["bins"].get(bin_label, _empty_bucket_entry()))
            bin_entry["bin_label"] = bin_label
            plot_rows.append(bin_entry)
        _plot_stacked_buckets_on_ax(
            ax,
            plot_rows,
            buckets=buckets,
            colors=colors,
            label_fn=lambda current_row: str(current_row.get("bin_label", "")),
            total_field="n",
            title=panel_title_fn(row),
            show_xticklabels=True,
            label_min_pct=8.0,
            show_legend=False,
        )
        ax.set_xlabel(x_label)

    for ax in axes_list[n_panels:]:
        ax.axis("off")

    from matplotlib.patches import Patch

    legend_handles = [Patch(color=colors[bucket], label=bucket) for bucket in buckets]
    fig.legend(legend_handles, buckets, loc="upper center", ncol=min(len(buckets), 4), fontsize=9)
    fig.suptitle(figure_title, fontsize=14)
    fig.subplots_adjust(top=0.82, bottom=0.12, left=0.07, right=0.98, hspace=0.42, wspace=0.22)
    fig.savefig(output_path)
    plt.close(fig)


def _plot_variant_crosstab_heatmaps(
    plt,
    crosstab_rows: List[dict],
    variant_rows: List[dict],
    output_path: Path,
) -> None:
    variant_names = [str(row.get("variant", "")) for row in variant_rows]
    if not variant_names:
        return

    ncols = 2 if len(variant_names) > 1 else 1
    nrows = math.ceil(len(variant_names) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(7 * ncols, 4.5 * nrows))
    axes_list = axes.flatten().tolist() if hasattr(axes, "flatten") else [axes]
    max_value = 0.0

    grouped = defaultdict(dict)
    for row in crosstab_rows:
        if row.get("level") != "variant":
            continue
        grouped[str(row.get("variant", ""))][
            (str(row.get("semantic_bucket", "")), str(row.get("log_error_bucket", "")))
        ] = float(row.get("pct_within_group", 0.0) or 0.0) * 100.0
        max_value = max(max_value, grouped[str(row.get("variant", ""))][
            (str(row.get("semantic_bucket", "")), str(row.get("log_error_bucket", "")))
        ])

    image = None
    for ax, variant in zip(axes_list, variant_names):
        matrix = []
        for semantic_bucket in SEMANTIC_BUCKETS:
            matrix.append(
                [
                    grouped.get(variant, {}).get((semantic_bucket, log_error_bucket), 0.0)
                    for log_error_bucket in DISPLAY_LOG_ERROR_BUCKETS
                ]
            )
        image = ax.imshow(matrix, cmap="Blues", vmin=0, vmax=max(max_value, 1.0))
        ax.set_title(variant)
        ax.set_xticks(range(len(DISPLAY_LOG_ERROR_BUCKETS)))
        ax.set_xticklabels(DISPLAY_LOG_ERROR_BUCKETS, rotation=35, ha="right")
        ax.set_yticks(range(len(SEMANTIC_BUCKETS)))
        ax.set_yticklabels(SEMANTIC_BUCKETS)
        for row_idx, matrix_row in enumerate(matrix):
            for col_idx, value in enumerate(matrix_row):
                if value <= 0:
                    continue
                ax.text(col_idx, row_idx, f"{value:.0f}", ha="center", va="center", fontsize=8)

    for ax in axes_list[len(variant_names):]:
        ax.axis("off")

    if image is not None:
        fig.colorbar(image, ax=axes_list, fraction=0.02, pad=0.02, label="Share of Tasks (%)")
    fig.suptitle("Semantic Bucket x Log Error Bucket by Variant", fontsize=14)
    fig.subplots_adjust(top=0.88, wspace=0.35, hspace=0.45)
    fig.savefig(output_path)
    plt.close(fig)


def generate_figures(
    summary_rows: List[dict],
    variant_rows: List[dict],
    crosstab_rows: List[dict],
    search_depth_buckets: dict,
    reasoning_density_buckets: dict,
    output_dir: Path,
) -> None:
    plt = _import_plot_libs()
    if plt is None:
        return

    fig_dir = output_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    _plot_metric_bars(
        plt,
        variant_rows,
        label_fn=lambda row: str(row.get("variant", "")),
        title="Semantic Match, D_ret, and D_acc by Variant",
        output_path=fig_dir / "fig_semantic_discovery_variant.pdf",
    )
    _plot_metric_bars(
        plt,
        summary_rows,
        label_fn=_model_variant_label,
        title="Semantic Match, D_ret, and D_acc by Model x Variant",
        output_path=fig_dir / "fig_semantic_discovery_model_variant.pdf",
    )

    _plot_stacked_buckets(
        plt,
        variant_rows,
        buckets=SEMANTIC_BUCKETS,
        colors=SEMANTIC_BUCKET_COLORS,
        label_fn=lambda row: str(row.get("variant", "")),
        total_field="n_total",
        title="Semantic Bucket Distribution by Variant",
        output_path=fig_dir / "fig_semantic_buckets_variant.pdf",
    )
    _plot_stacked_buckets(
        plt,
        summary_rows,
        buckets=SEMANTIC_BUCKETS,
        colors=SEMANTIC_BUCKET_COLORS,
        label_fn=_model_variant_label,
        total_field="n",
        title="Semantic Bucket Distribution by Model x Variant",
        output_path=fig_dir / "fig_semantic_buckets_model_variant.pdf",
    )
    _plot_combined_model_variant_buckets(
        plt,
        summary_rows,
        output_path=fig_dir / "fig_semantic_log_error_buckets_model_variant.pdf",
    )

    _plot_stacked_buckets(
        plt,
        variant_rows,
        buckets=DISPLAY_LOG_ERROR_BUCKETS,
        colors=LOG_ERROR_BUCKET_COLORS,
        label_fn=lambda row: str(row.get("variant", "")),
        total_field="n_total",
        title="Log Error Bucket Distribution by Variant",
        output_path=fig_dir / "fig_log_error_buckets_variant.pdf",
    )
    _plot_stacked_buckets(
        plt,
        summary_rows,
        buckets=DISPLAY_LOG_ERROR_BUCKETS,
        colors=LOG_ERROR_BUCKET_COLORS,
        label_fn=_model_variant_label,
        total_field="n",
        title="Log Error Bucket Distribution by Model x Variant",
        output_path=fig_dir / "fig_log_error_buckets_model_variant.pdf",
    )

    _plot_variant_crosstab_heatmaps(
        plt,
        crosstab_rows=crosstab_rows,
        variant_rows=variant_rows,
        output_path=fig_dir / "fig_semantic_x_error_variant.pdf",
    )

    _plot_binned_bucket_panels(
        plt,
        search_depth_buckets,
        bin_labels=[label for label, _ in _SEARCH_DEPTH_BINS],
        buckets=SEMANTIC_BUCKETS,
        colors=SEMANTIC_BUCKET_COLORS,
        panel_title_fn=lambda row: _model_variant_label(row).replace("\n", " — "),
        figure_title="Semantic Buckets by Search Depth",
        x_label="Search Calls per Task",
        output_path=fig_dir / "fig_semantic_buckets_search_depth_model_variant.pdf",
    )
    _plot_binned_bucket_panels(
        plt,
        search_depth_buckets,
        bin_labels=[label for label, _ in _SEARCH_DEPTH_BINS],
        buckets=DISPLAY_LOG_ERROR_BUCKETS,
        colors=LOG_ERROR_BUCKET_COLORS,
        panel_title_fn=lambda row: _model_variant_label(row).replace("\n", " — "),
        figure_title="Log Error Buckets by Search Depth",
        x_label="Search Calls per Task",
        output_path=fig_dir / "fig_log_error_buckets_search_depth_model_variant.pdf",
    )
    _plot_binned_bucket_panels(
        plt,
        reasoning_density_buckets,
        bin_labels=[label for label, _ in _REASONING_DENSITY_BINS],
        buckets=SEMANTIC_BUCKETS,
        colors=SEMANTIC_BUCKET_COLORS,
        panel_title_fn=lambda row: _model_variant_label(row).replace("\n", " — "),
        figure_title="Semantic Buckets by Reasoning Density",
        x_label="Number of Gold Documents per Task",
        output_path=fig_dir / "fig_semantic_buckets_reasoning_density_model_variant.pdf",
    )
    _plot_binned_bucket_panels(
        plt,
        reasoning_density_buckets,
        bin_labels=[label for label, _ in _REASONING_DENSITY_BINS],
        buckets=DISPLAY_LOG_ERROR_BUCKETS,
        colors=LOG_ERROR_BUCKET_COLORS,
        panel_title_fn=lambda row: _model_variant_label(row).replace("\n", " — "),
        figure_title="Log Error Buckets by Reasoning Density",
        x_label="Number of Gold Documents per Task",
        output_path=fig_dir / "fig_log_error_buckets_reasoning_density_model_variant.pdf",
    )


def run_analysis(
    *,
    results_dir: str,
    traces_dir: str,
    tasks_dir: str,
    output_dir: str,
    model_filter: Optional[str] = None,
    no_figures: bool = False,
) -> dict:
    model_filters = [token.strip().lower() for token in model_filter.split(",")] if model_filter else None

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading semantic eval results...")
    by_key_records, source_field_order = load_semantic_results_grouped(results_dir, model_filters=model_filters)

    print("Loading traces for discovery metrics...")
    grouped_traces = load_traces_grouped(traces_dir, model_filters=model_filters)

    print("Computing discovery metrics...")
    discovery_aggregates, task_metrics_by_key = run_discovery(grouped_traces, tasks_dir)

    print("Building summary tables...")
    summary_rows = build_summary(by_key_records, discovery_aggregates)
    variant_rows = build_variant_summary(summary_rows)
    search_depth_buckets = build_search_depth_buckets(by_key_records, task_metrics_by_key)
    reasoning_density_buckets = build_reasoning_density_buckets(by_key_records, tasks_dir)
    semantic_match, discovery, runtime, semantic_buckets, log_error_buckets = build_metric_mappings(summary_rows)
    crosstab_rows = build_semantic_error_crosstab(by_key_records, variant_rows)
    per_task_rows, per_task_fieldnames = build_per_task_rows(by_key_records, task_metrics_by_key, source_field_order)

    files = {
        "semantic_match.json": semantic_match,
        "discovery.json": discovery,
        "runtime.json": runtime,
        "semantic_buckets.json": semantic_buckets,
        "log_error_buckets.json": log_error_buckets,
        "search_depth_buckets.json": search_depth_buckets,
        "reasoning_density_buckets.json": reasoning_density_buckets,
        "semantic_error_crosstab.json": crosstab_rows,
        "summary.json": summary_rows,
        "variant_summary.json": variant_rows,
    }

    for filename, data in files.items():
        path = out_dir / filename
        write_json(path, data)
        print(f"  Wrote {path}")

    per_task_path = out_dir / "per_task_semantic.csv"
    write_csv(per_task_path, per_task_rows, per_task_fieldnames)
    print(f"  Wrote {per_task_path} ({len(per_task_rows)} rows)")

    if no_figures:
        print("Skipping figures (--no-figures).")
    else:
        print("Generating figures...")
        generate_figures(
            summary_rows,
            variant_rows,
            crosstab_rows,
            search_depth_buckets,
            reasoning_density_buckets,
            out_dir,
        )
        print(f"  Wrote figures to {out_dir / 'figures'}")

    print(f"\nSummary ({len(summary_rows)} model x variant rows):")
    for row in summary_rows:
        semantic_pct = (
            f"{float(row['semantic_match']) * 100:.1f}%"
            if row.get("semantic_match") is not None
            else "N/A"
        )
        d_ret = f"{row.get('D_ret'):.2f}" if row.get("D_ret") is not None else "N/A"
        d_acc = f"{row.get('D_acc'):.2f}" if row.get("D_acc") is not None else "N/A"
        print(
            f"  {row['condition_model']:<70} "
            f"semantic={semantic_pct:<7} D_ret={d_ret:<5} D_acc={d_acc:<5} n={row.get('n')}"
        )

    return {
        "summary": summary_rows,
        "variant_summary": variant_rows,
        "semantic_match": semantic_match,
        "discovery": discovery,
        "runtime": runtime,
        "semantic_buckets": semantic_buckets,
        "log_error_buckets": log_error_buckets,
        "search_depth_buckets": search_depth_buckets,
        "reasoning_density_buckets": reasoning_density_buckets,
        "semantic_error_crosstab": crosstab_rows,
        "per_task_rows": per_task_rows,
    }


def main() -> None:
    args = parse_args()
    run_analysis(
        results_dir=args.results_dir,
        traces_dir=args.traces_dir,
        tasks_dir=args.tasks_dir,
        output_dir=args.output_dir,
        model_filter=args.model_filter,
        no_figures=args.no_figures,
    )


if __name__ == "__main__":
    main()
