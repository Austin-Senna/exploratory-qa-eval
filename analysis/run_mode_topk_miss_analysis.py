#!/usr/bin/env python3
"""
Analyze how often gold datasets are missing from the top-k search results in mode traces.

Inputs:
  results-ec2/traces/modes/{model}/{variant}/{task_dir}/{task}.jsonl

Outputs (default: analysis_results_mode_topk_miss/):
  summary.json
  summary.csv
  variant_summary.json
  variant_summary.csv
  first_hit_rounds_variant.json
  first_hit_rounds_variant.csv
  per_call.csv
  figures/ (unless --no-figures)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.discovery_metrics import load_task_gold_ids, make_task_stem_key


_LETTER_TO_MODE = {"n": "naive", "d": "standard", "i": "ideal", "p": "preloaded"}
_FIRST_HIT_CUTOFFS = (1, 3, 5)
_TOOL_ORDER = ["search_ideal", "search_reranked", "search_value", "search_prefix", "search_schema"]
_TOOL_COLORS = {
    "search_ideal": "#2E8B57",
    "search_reranked": "#1F77B4",
    "search_value": "#C07A2C",
    "search_prefix": "#C44E52",
    "search_schema": "#7F7F7F",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces-dir", default="results-ec2/traces/modes")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results_mode_topk_miss")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--model-filter",
        default=None,
        help="Substring filter on model directory name (comma-separated OR).",
    )
    parser.add_argument(
        "--no-figures",
        action="store_true",
        help="Skip graph generation.",
    )
    return parser.parse_args()


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
        "plan": None,
        "skills": None,
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
            out["plan"] = _LETTER_TO_MODE.get(token[4:])
        elif token == "skills" and idx + 1 < len(parts):
            out["skills"] = parts[idx + 1]
        elif token.startswith("k") and token[1:].isdigit():
            out["k"] = int(token[1:])
        elif token.startswith("sc") and token[2:].isdigit():
            out["sc"] = int(token[2:])
    return out


def _variant_sort_key(variant: str) -> tuple:
    axes = _parse_variant(variant)
    mode_priority = {"ideal": 0, "standard": 1, "naive": 2, None: 3}
    return (
        mode_priority.get(axes.get("search_tool"), 4),
        mode_priority.get(axes.get("plan"), 4),
        mode_priority.get(axes.get("search_results"), 4),
        axes.get("k") if axes.get("k") is not None else 10**9,
        axes.get("sc") if axes.get("sc") is not None else 10**9,
        variant,
    )


def _condition_model_sort_key(key: str) -> tuple:
    model, variant = _split_cm_key(key)
    return (*_variant_sort_key(variant), model)


def _tool_sort_key(tool: str) -> tuple:
    if tool in _TOOL_ORDER:
        return (_TOOL_ORDER.index(tool), tool)
    return (len(_TOOL_ORDER), tool)


def _model_variant_label(row: dict) -> str:
    return f"{row.get('model', '')}\n{row.get('variant', '')}"


def _parse_turn(value) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _order_search_events(events: List[dict]) -> List[dict]:
    if events and all(event.get("parsed_turn") is not None for event in events):
        return sorted(events, key=lambda event: (int(event["parsed_turn"]), int(event["line_index"])))
    return list(events)


def _parse_trace_jsonl_path(path: Path, traces_root: Path) -> Tuple[str, str, str]:
    rel = path.relative_to(traces_root)
    parts = rel.parts
    if len(parts) >= 4:
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return parts[-4], parts[-3], task_id
    raise ValueError(f"Expected <traces>/<model>/<variant>/<task_dir>/<task>.jsonl layout, got {path}")


def _task_stem_from_trace_record(record: dict, fallback_task_stem: str) -> str:
    task_id = str(record.get("task_id", "") or "")
    if not task_id:
        return fallback_task_stem
    return make_task_stem_key(task_id)


def _load_task_gold_by_stem(tasks_dir: str) -> Dict[str, set[str]]:
    gold_by_stem: Dict[str, set[str]] = {}
    for path_key, dataset_ids in load_task_gold_ids(tasks_dir).items():
        gold_by_stem[make_task_stem_key(path_key)] = set(dataset_ids)
    return gold_by_stem


def _first_gold_rank(result_ids: List[str], gold_ids: set[str]) -> Optional[int]:
    for idx, dataset_id in enumerate(result_ids, start=1):
        if dataset_id in gold_ids:
            return idx
    return None


def _as_bool_int(value: bool) -> int:
    return 1 if value else 0


def _import_plot_libs():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except Exception:
        print("Skipping figures: matplotlib is not installed.")
        return None


def _cleanup_figure_dir(fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    for existing_pdf in fig_dir.glob("*.pdf"):
        existing_pdf.unlink()


def _plot_grouped_tool_bars(
    plt,
    rows: List[dict],
    *,
    label_fn,
    value_field: str,
    title: str,
    y_label: str,
    output_path: Path,
    is_rate: bool,
) -> None:
    if not rows:
        return

    ordered_rows = list(rows)
    labels = [label_fn(row) for row in ordered_rows]
    tools = sorted({str(row.get("search_call_tool", "")) for row in ordered_rows}, key=_tool_sort_key)
    if not tools:
        return

    by_label_tool = {(label_fn(row), str(row.get("search_call_tool", ""))): row for row in ordered_rows}
    x_positions = list(range(len(labels)))
    width = min(0.82 / len(tools), 0.28)
    fig_width = max(10, len(labels) * 1.0)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    max_value = max(float(row.get(value_field) or 0.0) for row in ordered_rows)
    if is_rate:
        max_value *= 100.0
    count_label_min = max(2.0, max_value * 0.08)

    for idx, tool in enumerate(tools):
        offsets = [x + (idx - (len(tools) - 1) / 2) * width for x in x_positions]
        values = [float(by_label_tool.get((label, tool), {}).get(value_field, 0.0) or 0.0) for label in labels]
        if is_rate:
            values = [value * 100.0 for value in values]
        bars = ax.bar(
            offsets,
            values,
            width=width * 0.92,
            label=tool,
            color=_TOOL_COLORS.get(tool, "#4C72B0"),
        )
        for bar, value in zip(bars, values):
            if is_rate:
                label_min = 3.0
                if value < label_min:
                    continue
                label = f"{value:.0f}%"
                y_offset = 1.2
            else:
                if value < count_label_min:
                    continue
                label = f"{int(round(value))}"
                y_offset = max(0.8, max_value * 0.015)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + y_offset,
                label,
                ha="center",
                va="bottom",
                fontsize=8,
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    if is_rate:
        ax.set_ylim(0, 100)
    else:
        ax.set_ylim(0, max_value * 1.16 if max_value > 0 else 1.0)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
    fig.tight_layout(rect=(0, 0, 0.84, 1))
    fig.savefig(output_path)
    plt.close(fig)


def _plot_first_hit_rounds_variant(plt, first_hit_rows: List[dict], output_path: Path) -> None:
    if not first_hit_rows:
        return

    ordered_variants = sorted({str(row.get("variant", "")) for row in first_hit_rows}, key=_variant_sort_key)
    cutoff_rows = {
        cutoff: {
            str(row.get("variant", "")): row
            for row in first_hit_rows
            if int(row.get("cutoff", 0) or 0) == cutoff
        }
        for cutoff in _FIRST_HIT_CUTOFFS
    }
    max_round = max(int(row.get("max_round", 0) or 0) for row in first_hit_rows)
    if max_round <= 0:
        return

    fig, axes = plt.subplots(len(_FIRST_HIT_CUTOFFS), 1, figsize=(12, 11), sharex=True, sharey=True)
    axes_list = axes.flatten().tolist() if hasattr(axes, "flatten") else [axes]
    color_map = {variant: f"C{idx % 10}" for idx, variant in enumerate(ordered_variants)}

    for ax, cutoff in zip(axes_list, _FIRST_HIT_CUTOFFS):
        rows_by_variant = cutoff_rows[cutoff]
        x_values = list(range(1, max_round + 1))
        for variant in ordered_variants:
            row = rows_by_variant.get(variant)
            if not row:
                continue
            cumulative_rates = row.get("cumulative_found_rates", {}) or {}
            final_rate = 0.0
            y_values = []
            for round_number in x_values:
                rate = cumulative_rates.get(str(round_number))
                if rate is None:
                    rate = final_rate
                else:
                    final_rate = float(rate)
                y_values.append(final_rate * 100.0)
            color = color_map[variant]
            ax.step(x_values, y_values, where="post", linewidth=2, color=color, label=variant)
            ax.text(
                max_round + 0.15,
                y_values[-1],
                f"{float(row.get('not_found_rate', 0.0) or 0.0) * 100:.0f}% NF",
                color=color,
                fontsize=8,
                va="center",
            )

        ax.set_title(f"First Gold Hit by Search Round (Top-{cutoff})")
        ax.set_ylabel("Tasks Found (%)")
        ax.set_ylim(0, 100)
        ax.set_xlim(1, max_round + 0.8)
        ax.grid(True, axis="y", alpha=0.25)
        if max_round <= 12:
            ax.set_xticks(x_values)

    axes_list[-1].set_xlabel("Search Round")
    handles = [plt.Line2D([0], [0], color=color_map[variant], lw=2) for variant in ordered_variants]
    fig.legend(handles, ordered_variants, loc="center right", bbox_to_anchor=(0.995, 0.5), fontsize=8)
    fig.tight_layout(rect=(0, 0, 0.86, 1))
    fig.savefig(output_path)
    plt.close(fig)


def generate_figures(
    variant_summary_rows: List[dict],
    first_hit_rows: List[dict],
    output_dir: Path,
) -> None:
    plt = _import_plot_libs()
    if plt is None:
        return

    fig_dir = output_dir / "figures"
    _cleanup_figure_dir(fig_dir)

    _plot_grouped_tool_bars(
        plt,
        variant_summary_rows,
        label_fn=lambda row: str(row.get("variant", "")),
        value_field="top_k_miss_rate",
        title="Top-k Gold Miss Rate by Variant and Search Tool",
        y_label="Miss Rate (%)",
        output_path=fig_dir / "fig_topk_miss_rate_variant.pdf",
        is_rate=True,
    )
    _plot_grouped_tool_bars(
        plt,
        variant_summary_rows,
        label_fn=lambda row: str(row.get("variant", "")),
        value_field="top_k_misses",
        title="Top-k Gold Miss Count by Variant and Search Tool",
        y_label="Missed Calls",
        output_path=fig_dir / "fig_topk_miss_count_variant.pdf",
        is_rate=False,
    )
    _plot_first_hit_rounds_variant(
        plt,
        first_hit_rows,
        output_path=fig_dir / "fig_first_hit_rounds_variant.pdf",
    )


def _build_first_hit_variant_rows(task_first_hit_rows: List[dict]) -> List[dict]:
    groups: Dict[Tuple[str, int], List[dict]] = defaultdict(list)
    for row in task_first_hit_rows:
        variant = str(row.get("variant", ""))
        for cutoff in _FIRST_HIT_CUTOFFS:
            groups[(variant, cutoff)].append(row)

    out: List[dict] = []
    for (variant, cutoff), rows in sorted(groups.items(), key=lambda item: (_variant_sort_key(item[0][0]), item[0][1])):
        n_tasks = len(rows)
        found_rounds = []
        max_round = 0
        round_counts: Dict[int, int] = defaultdict(int)
        for row in rows:
            max_round = max(max_round, int(row.get("num_search_rounds", 0) or 0))
            round_value = row.get(f"first_hit_round_top_{cutoff}", "")
            if round_value in ("", None):
                continue
            round_number = int(round_value)
            found_rounds.append(round_number)
            round_counts[round_number] += 1

        found_tasks = len(found_rounds)
        not_found_tasks = n_tasks - found_tasks
        cumulative_found_counts = {}
        cumulative_found_rates = {}
        running_found = 0
        for round_number in range(1, max_round + 1):
            running_found += round_counts.get(round_number, 0)
            cumulative_found_counts[str(round_number)] = running_found
            cumulative_found_rates[str(round_number)] = round(running_found / n_tasks, 4) if n_tasks else 0.0

        out.append(
            {
                "variant": variant,
                "cutoff": cutoff,
                "n_tasks": n_tasks,
                "found_tasks": found_tasks,
                "not_found_tasks": not_found_tasks,
                "not_found_rate": round(not_found_tasks / n_tasks, 4) if n_tasks else 0.0,
                "max_round": max_round,
                "models": sorted({str(row.get("model", "")) for row in rows if row.get("model")}),
                "num_model_rows": len({str(row.get("condition_model", "")) for row in rows if row.get("condition_model")}),
                "round_counts": {str(round_number): count for round_number, count in sorted(round_counts.items())},
                "cumulative_found_counts": cumulative_found_counts,
                "cumulative_found_rates": cumulative_found_rates,
            }
        )

    return out


def run_analysis(
    *,
    traces_dir: str,
    tasks_dir: str,
    output_dir: str,
    top_k: int = 5,
    model_filter: Optional[str] = None,
    no_figures: bool = False,
) -> dict:
    traces_root = Path(traces_dir)
    if not traces_root.exists():
        raise FileNotFoundError(f"Traces directory does not exist: {traces_root}")

    gold_by_stem = _load_task_gold_by_stem(tasks_dir)
    if not gold_by_stem:
        raise FileNotFoundError(f"No task gold datasets found under {tasks_dir}")

    model_filters = [token.strip().lower() for token in model_filter.split(",")] if model_filter else None

    def keep_model(model: str) -> bool:
        if not model_filters:
            return True
        lowered = model.lower()
        return any(token in lowered for token in model_filters)

    per_call_rows: List[dict] = []
    task_first_hit_rows: List[dict] = []
    grouped: Dict[Tuple[str, str], dict] = defaultdict(
        lambda: {
            "search_calls": 0,
            "top_k_hits": 0,
            "top_k_misses": 0,
            "returned_anywhere_hits": 0,
            "returned_anywhere_misses": 0,
            "tasks_with_calls": set(),
            "tasks_with_any_top_k_miss": set(),
            "tasks_with_all_top_k_miss": defaultdict(lambda: {"calls": 0, "misses": 0}),
        }
    )

    for jsonl_path in sorted(traces_root.rglob("*.jsonl")):
        model, variant, fallback_task_stem = _parse_trace_jsonl_path(jsonl_path, traces_root)
        if not keep_model(model):
            continue

        search_events: List[dict] = []
        with jsonl_path.open() as handle:
            for line_index, line in enumerate(handle):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                tool = str(record.get("tool", "") or "")
                result_ids = record.get("result_dataset_ids")
                if not tool or result_ids is None:
                    continue

                task_stem = _task_stem_from_trace_record(record, fallback_task_stem)
                gold_ids = gold_by_stem.get(task_stem)
                if not gold_ids:
                    continue

                result_ids = list(result_ids)
                gold_rank = _first_gold_rank(result_ids, gold_ids)
                top_result_ids = result_ids[:top_k]
                gold_in_top_k = bool(set(top_result_ids) & gold_ids)
                gold_returned_anywhere = gold_rank is not None
                cutoff_hits = {
                    cutoff: bool(set(result_ids[:cutoff]) & gold_ids)
                    for cutoff in _FIRST_HIT_CUTOFFS
                }

                key = (_cm_key(model, variant), tool)
                bucket = grouped[key]
                bucket["search_calls"] += 1
                bucket["top_k_hits"] += _as_bool_int(gold_in_top_k)
                bucket["top_k_misses"] += _as_bool_int(not gold_in_top_k)
                bucket["returned_anywhere_hits"] += _as_bool_int(gold_returned_anywhere)
                bucket["returned_anywhere_misses"] += _as_bool_int(not gold_returned_anywhere)
                bucket["tasks_with_calls"].add(task_stem)
                if not gold_in_top_k:
                    bucket["tasks_with_any_top_k_miss"].add(task_stem)
                task_rollup = bucket["tasks_with_all_top_k_miss"][task_stem]
                task_rollup["calls"] += 1
                task_rollup["misses"] += _as_bool_int(not gold_in_top_k)

                per_call_row = {
                    "condition_model": _cm_key(model, variant),
                    "model": model,
                    "variant": variant,
                    "task_id": str(record.get("task_id", "") or task_stem),
                    "task_stem": task_stem,
                    "search_call_tool": tool,
                    "turn": record.get("turn"),
                    "search_round": "",
                    "query": record.get("query", ""),
                    "top_k": top_k,
                    "results_returned": len(result_ids),
                    "gold_rank": gold_rank if gold_rank is not None else "",
                    "gold_in_top_k": _as_bool_int(gold_in_top_k),
                    "gold_in_top_1": _as_bool_int(cutoff_hits[1]),
                    "gold_in_top_3": _as_bool_int(cutoff_hits[3]),
                    "gold_in_top_5": _as_bool_int(cutoff_hits[5]),
                    "gold_returned_anywhere": _as_bool_int(gold_returned_anywhere),
                    "top_result_dataset_ids": ",".join(top_result_ids),
                    "gold_dataset_ids": ",".join(sorted(gold_ids)),
                }
                per_call_rows.append(per_call_row)
                search_events.append(
                    {
                        "line_index": line_index,
                        "parsed_turn": _parse_turn(record.get("turn")),
                        "task_id": str(record.get("task_id", "") or task_stem),
                        "task_stem": task_stem,
                        "cutoff_hits": cutoff_hits,
                        "row": per_call_row,
                    }
                )

        if search_events:
            ordered_events = _order_search_events(search_events)
            task_first_hit_row = {
                "condition_model": _cm_key(model, variant),
                "model": model,
                "variant": variant,
                "task_id": str(ordered_events[0].get("task_id", "")),
                "task_stem": str(ordered_events[0].get("task_stem", "")),
                "num_search_rounds": len(ordered_events),
            }
            for round_number, event in enumerate(ordered_events, start=1):
                event["row"]["search_round"] = round_number
            for cutoff in _FIRST_HIT_CUTOFFS:
                first_hit_round = next(
                    (
                        round_number
                        for round_number, event in enumerate(ordered_events, start=1)
                        if bool(event.get("cutoff_hits", {}).get(cutoff))
                    ),
                    None,
                )
                task_first_hit_row[f"first_hit_round_top_{cutoff}"] = (
                    first_hit_round if first_hit_round is not None else ""
                )
            task_first_hit_rows.append(task_first_hit_row)

    summary_rows: List[dict] = []
    for (condition_model, search_call_tool), stats in sorted(grouped.items(), key=lambda item: (_condition_model_sort_key(item[0][0]), item[0][1])):
        model, variant = _split_cm_key(condition_model)
        axes = _parse_variant(variant)
        search_calls = int(stats["search_calls"])
        tasks_with_all_top_k_miss = sum(
            1
            for task_stats in stats["tasks_with_all_top_k_miss"].values()
            if task_stats["calls"] > 0 and task_stats["calls"] == task_stats["misses"]
        )
        row = {
            "condition_model": condition_model,
            "model": model,
            "variant": variant,
            "search_tool": axes["search_tool"],
            "search_results": axes["search_results"],
            "plan": axes["plan"],
            "skills": axes["skills"],
            "k": axes["k"],
            "sc": axes["sc"],
            "search_call_tool": search_call_tool,
            "top_k": top_k,
            "search_calls": search_calls,
            "top_k_hits": int(stats["top_k_hits"]),
            "top_k_misses": int(stats["top_k_misses"]),
            "top_k_miss_rate": round(int(stats["top_k_misses"]) / search_calls, 4) if search_calls else 0.0,
            "returned_anywhere_hits": int(stats["returned_anywhere_hits"]),
            "returned_anywhere_misses": int(stats["returned_anywhere_misses"]),
            "returned_anywhere_miss_rate": round(int(stats["returned_anywhere_misses"]) / search_calls, 4)
            if search_calls
            else 0.0,
            "tasks_with_calls": len(stats["tasks_with_calls"]),
            "tasks_with_any_top_k_miss": len(stats["tasks_with_any_top_k_miss"]),
            "tasks_with_all_top_k_miss": tasks_with_all_top_k_miss,
        }
        summary_rows.append(row)

    variant_groups: Dict[Tuple[str, str], List[dict]] = defaultdict(list)
    for row in summary_rows:
        variant_groups[(str(row["variant"]), str(row["search_call_tool"]))].append(row)

    variant_summary_rows: List[dict] = []
    for (variant, search_call_tool), rows in sorted(variant_groups.items(), key=lambda item: (_variant_sort_key(item[0][0]), item[0][1])):
        axes = _parse_variant(variant)
        search_calls = sum(int(row["search_calls"]) for row in rows)
        top_k_misses = sum(int(row["top_k_misses"]) for row in rows)
        returned_anywhere_misses = sum(int(row["returned_anywhere_misses"]) for row in rows)
        variant_summary_rows.append(
            {
                "variant": variant,
                "search_tool": axes["search_tool"],
                "search_results": axes["search_results"],
                "plan": axes["plan"],
                "skills": axes["skills"],
                "k": axes["k"],
                "sc": axes["sc"],
                "search_call_tool": search_call_tool,
                "top_k": top_k,
                "num_model_rows": len(rows),
                "models": sorted({str(row["model"]) for row in rows}),
                "search_calls": search_calls,
                "top_k_hits": sum(int(row["top_k_hits"]) for row in rows),
                "top_k_misses": top_k_misses,
                "top_k_miss_rate": round(top_k_misses / search_calls, 4) if search_calls else 0.0,
                "returned_anywhere_hits": sum(int(row["returned_anywhere_hits"]) for row in rows),
                "returned_anywhere_misses": returned_anywhere_misses,
                "returned_anywhere_miss_rate": round(returned_anywhere_misses / search_calls, 4)
                if search_calls
                else 0.0,
                "tasks_with_calls": sum(int(row["tasks_with_calls"]) for row in rows),
                "tasks_with_any_top_k_miss": sum(int(row["tasks_with_any_top_k_miss"]) for row in rows),
                "tasks_with_all_top_k_miss": sum(int(row["tasks_with_all_top_k_miss"]) for row in rows),
            }
        )

    first_hit_variant_rows = _build_first_hit_variant_rows(task_first_hit_rows)

    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    files = {
        "summary.json": summary_rows,
        "variant_summary.json": variant_summary_rows,
        "first_hit_rounds_variant.json": first_hit_variant_rows,
    }
    for filename, data in files.items():
        with (output_root / filename).open("w") as handle:
            json.dump(data, handle, indent=2)

    summary_fieldnames = [
        "condition_model",
        "model",
        "variant",
        "search_tool",
        "search_results",
        "plan",
        "skills",
        "k",
        "sc",
        "search_call_tool",
        "top_k",
        "search_calls",
        "top_k_hits",
        "top_k_misses",
        "top_k_miss_rate",
        "returned_anywhere_hits",
        "returned_anywhere_misses",
        "returned_anywhere_miss_rate",
        "tasks_with_calls",
        "tasks_with_any_top_k_miss",
        "tasks_with_all_top_k_miss",
    ]
    with (output_root / "summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    variant_summary_fieldnames = [
        "variant",
        "search_tool",
        "search_results",
        "plan",
        "skills",
        "k",
        "sc",
        "search_call_tool",
        "top_k",
        "num_model_rows",
        "models",
        "search_calls",
        "top_k_hits",
        "top_k_misses",
        "top_k_miss_rate",
        "returned_anywhere_hits",
        "returned_anywhere_misses",
        "returned_anywhere_miss_rate",
        "tasks_with_calls",
        "tasks_with_any_top_k_miss",
        "tasks_with_all_top_k_miss",
    ]
    with (output_root / "variant_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=variant_summary_fieldnames)
        writer.writeheader()
        for row in variant_summary_rows:
            normalized = dict(row)
            normalized["models"] = ",".join(row["models"])
            writer.writerow(normalized)

    first_hit_fieldnames = [
        "variant",
        "cutoff",
        "n_tasks",
        "found_tasks",
        "not_found_tasks",
        "not_found_rate",
        "max_round",
        "num_model_rows",
        "models",
        "round_counts",
        "cumulative_found_counts",
        "cumulative_found_rates",
    ]
    with (output_root / "first_hit_rounds_variant.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=first_hit_fieldnames)
        writer.writeheader()
        for row in first_hit_variant_rows:
            normalized = dict(row)
            normalized["models"] = ",".join(row["models"])
            normalized["round_counts"] = json.dumps(row["round_counts"], sort_keys=True)
            normalized["cumulative_found_counts"] = json.dumps(row["cumulative_found_counts"], sort_keys=True)
            normalized["cumulative_found_rates"] = json.dumps(row["cumulative_found_rates"], sort_keys=True)
            writer.writerow(normalized)

    per_call_fieldnames = [
        "condition_model",
        "model",
        "variant",
        "task_id",
        "task_stem",
        "search_call_tool",
        "turn",
        "search_round",
        "query",
        "top_k",
        "results_returned",
        "gold_rank",
        "gold_in_top_k",
        "gold_in_top_1",
        "gold_in_top_3",
        "gold_in_top_5",
        "gold_returned_anywhere",
        "top_result_dataset_ids",
        "gold_dataset_ids",
    ]
    with (output_root / "per_call.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=per_call_fieldnames)
        writer.writeheader()
        writer.writerows(per_call_rows)

    print(f"Wrote {output_root / 'summary.json'}")
    print(f"Wrote {output_root / 'variant_summary.json'}")
    print(f"Wrote {output_root / 'first_hit_rounds_variant.json'}")
    print(f"Wrote {output_root / 'summary.csv'}")
    print(f"Wrote {output_root / 'variant_summary.csv'}")
    print(f"Wrote {output_root / 'first_hit_rounds_variant.csv'}")
    print(f"Wrote {output_root / 'per_call.csv'} ({len(per_call_rows)} rows)")

    if not no_figures:
        generate_figures(variant_summary_rows, first_hit_variant_rows, output_root)
        print(f"Wrote figures to {output_root / 'figures'}")

    print("\nTop-k miss summary:")
    for row in summary_rows:
        print(
            f"  {row['condition_model']:<70} {row['search_call_tool']:<18} "
            f"misses={row['top_k_misses']:<4} calls={row['search_calls']:<4} "
            f"miss_rate={row['top_k_miss_rate']:.1%}"
        )

    return {
        "summary": summary_rows,
        "variant_summary": variant_summary_rows,
        "first_hit_rounds_variant": first_hit_variant_rows,
        "task_first_hit_rows": task_first_hit_rows,
        "per_call": per_call_rows,
    }


def main() -> None:
    args = parse_args()
    run_analysis(
        traces_dir=args.traces_dir,
        tasks_dir=args.tasks_dir,
        output_dir=args.output_dir,
        top_k=args.top_k,
        model_filter=args.model_filter,
        no_figures=args.no_figures,
    )


if __name__ == "__main__":
    main()
