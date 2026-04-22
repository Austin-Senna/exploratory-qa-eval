#!/usr/bin/env python3
"""
Categorize wasted-turn patterns for failed semantic-mode runs.

This script aligns semantic eval CSV rows with raw execution logs and emits:
  - a per-run CSV with tool/turn metrics and a primary waste category
  - a markdown report summarizing the dominant waste patterns

Default scope matches the EC2 semantic outputs used in this repo:
    python analysis/turn_waste_analysis.py
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter
from pathlib import Path
import re


TARGET_LOG_ERROR_BUCKETS = {"error_tokens_reached", "error_tools_limit"}

SETUP_TOOLS = {"skills", "plan_ideal"}
SEARCH_TOOLS = {"search_ideal", "search_value", "search_schema", "search_prefix"}
INSPECT_TOOLS = {"peek_file", "peek_multiple", "list_files", "read_file", "grep_file"}

TURN_RE = re.compile(r"--- Turn (\d+)")
EXEC_RE = re.compile(r"Executing: ([A-Za-z_]+)\((.*)\)$")


def _normalize_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def _normalize_sql(value: str) -> str:
    return _normalize_text(value).lower()


def _safe_int(value: str | int | float | None) -> int | None:
    if value in ("", None):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _safe_float(value: str | int | float | None) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _median(values: list[int | float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _format_median(value: float | None) -> str:
    if value is None:
        return "n/a"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


def _share_text(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0 (0.0%)"
    return f"{numerator}/{denominator} ({100 * numerator / denominator:.1f}%)"


def is_probe_query(sql: str) -> bool:
    normalized = _normalize_sql(sql)
    if not normalized:
        return False
    probe_patterns = (
        "select * from t limit 1",
        "select * from t limit 5",
        "typeof(",
        "meta.view.columns[",
        "list_count(data)",
        "select data[1]",
    )
    return any(pattern in normalized for pattern in probe_patterns)


def _parse_log(log_path: Path) -> dict:
    turns = 0
    calls: list[dict] = []
    stagnation_warnings = 0
    timeout_submit_warning = False
    tool_limit_submit_warning = False
    stop_warning_seen = False
    post_warning_non_submit_calls = 0

    with log_path.open() as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            turn_match = TURN_RE.search(line)
            if turn_match:
                turns = max(turns, int(turn_match.group(1)))

            if "[Stagnation]" in line:
                stagnation_warnings += 1
            if "Timeout reached" in line and "submit_answer" in line:
                timeout_submit_warning = True
                stop_warning_seen = True
            if "Tool limit reached" in line and "submit_answer" in line:
                tool_limit_submit_warning = True
                stop_warning_seen = True

            exec_match = EXEC_RE.search(line.strip())
            if not exec_match:
                continue

            tool_name = exec_match.group(1)
            args_text = exec_match.group(2)
            try:
                args = json.loads(args_text)
            except json.JSONDecodeError:
                args = {}
            if stop_warning_seen and tool_name != "submit_answer":
                post_warning_non_submit_calls += 1
            calls.append({"tool": tool_name, "args": args})

    tool_counts = Counter(call["tool"] for call in calls)
    search_query_counts: Counter[str] = Counter()
    query_signature_counts: Counter[tuple[str | None, str | None, str]] = Counter()
    query_target_counts: Counter[tuple[str | None, str | None]] = Counter()
    inspect_target_counts: Counter[tuple[str, str | None, str | None]] = Counter()

    search_calls = 0
    inspect_calls = 0
    query_file_calls = 0
    probe_query_calls = 0
    analytic_query_calls = 0
    download_calls = 0
    execute_code_calls = 0
    answer_calls = 0
    first_analytic_call_index: int | None = None

    for idx, call in enumerate(calls, start=1):
        tool = call["tool"]
        args = call["args"]
        if tool in SEARCH_TOOLS:
            search_calls += 1
            normalized_query = _normalize_text(str(args.get("query", "")))
            if normalized_query:
                search_query_counts[normalized_query] += 1
        elif tool in INSPECT_TOOLS:
            inspect_calls += 1
            inspect_target_counts[(tool, args.get("dataset_id"), args.get("file_path"))] += 1
        elif tool == "query_file":
            query_file_calls += 1
            normalized_sql = _normalize_sql(str(args.get("sql", "")))
            query_signature_counts[
                (args.get("dataset_id"), args.get("file_path"), normalized_sql)
            ] += 1
            query_target_counts[(args.get("dataset_id"), args.get("file_path"))] += 1
            if is_probe_query(str(args.get("sql", ""))):
                probe_query_calls += 1
            else:
                analytic_query_calls += 1
                if first_analytic_call_index is None:
                    first_analytic_call_index = idx
        elif tool == "download":
            download_calls += 1
            if first_analytic_call_index is None:
                first_analytic_call_index = idx
        elif tool == "execute_code":
            execute_code_calls += 1
            if first_analytic_call_index is None:
                first_analytic_call_index = idx
        elif tool == "submit_answer":
            answer_calls += 1

    compute_calls = analytic_query_calls + download_calls + execute_code_calls
    repeated_search_queries = sum(count - 1 for count in search_query_counts.values() if count > 1)
    repeated_query_signatures = sum(count - 1 for count in query_signature_counts.values() if count > 1)
    repeated_query_targets = sum(count - 1 for count in query_target_counts.values() if count > 1)
    repeated_inspect_targets = sum(count - 1 for count in inspect_target_counts.values() if count > 1)

    logged_exec_calls = len(calls)
    if first_analytic_call_index is None:
        calls_before_first_analytic = logged_exec_calls
        no_analytic_step = True
    else:
        calls_before_first_analytic = first_analytic_call_index - 1
        no_analytic_step = False

    submit_called = answer_calls > 0
    ignored_stop_signal = (timeout_submit_warning or tool_limit_submit_warning) and (
        not submit_called or post_warning_non_submit_calls > 0
    )
    submit_after_hard_stop_only = submit_called and (timeout_submit_warning or tool_limit_submit_warning)

    metrics = {
        "turn_count": turns,
        "logged_exec_calls": logged_exec_calls,
        "setup_calls": sum(tool_counts[name] for name in SETUP_TOOLS),
        "search_calls": search_calls,
        "inspect_calls": inspect_calls,
        "query_file_calls": query_file_calls,
        "probe_query_calls": probe_query_calls,
        "analytic_query_calls": analytic_query_calls,
        "compute_calls": compute_calls,
        "download_calls": download_calls,
        "execute_code_calls": execute_code_calls,
        "answer_calls": answer_calls,
        "list_files_calls": tool_counts["list_files"],
        "peek_calls": tool_counts["peek_file"] + tool_counts["peek_multiple"],
        "read_calls": tool_counts["read_file"],
        "grep_calls": tool_counts["grep_file"],
        "repeated_plan_calls": max(tool_counts["plan_ideal"] - 1, 0),
        "repeated_skill_calls": max(tool_counts["skills"] - 2, 0),
        "repeated_search_queries": repeated_search_queries,
        "repeated_query_signatures": repeated_query_signatures,
        "repeated_query_targets": repeated_query_targets,
        "repeated_inspect_targets": repeated_inspect_targets,
        "stagnation_warnings": stagnation_warnings,
        "timeout_submit_warning": int(timeout_submit_warning),
        "tool_limit_submit_warning": int(tool_limit_submit_warning),
        "ignored_stop_signal": int(ignored_stop_signal),
        "submit_called": int(submit_called),
        "submit_after_hard_stop_only": int(submit_after_hard_stop_only),
        "post_warning_non_submit_calls": post_warning_non_submit_calls,
        "no_analytic_step": int(no_analytic_step),
        "first_analytic_call_index": first_analytic_call_index,
        "calls_before_first_analytic": calls_before_first_analytic,
    }
    return metrics


def _score_categories(metrics: dict) -> dict[str, int]:
    inspection_active = (
        metrics["inspect_calls"] >= 8
        or metrics["repeated_inspect_targets"] >= 2
        or (metrics["no_analytic_step"] and metrics["inspect_calls"] >= 4)
    )
    query_active = (
        metrics["analytic_query_calls"] >= 6
        or metrics["probe_query_calls"] >= 2
        or metrics["repeated_query_targets"] >= 3
        or metrics["repeated_query_signatures"] >= 2
    )
    search_active = (
        metrics["search_calls"] >= 5
        or metrics["repeated_search_queries"] >= 1
        or (metrics["no_analytic_step"] and metrics["search_calls"] >= 3)
    )
    download_active = metrics["download_calls"] >= 1 and metrics["execute_code_calls"] >= 1
    setup_active = (
        metrics["setup_calls"] >= 8
        or metrics["repeated_plan_calls"] >= 1
        or metrics["repeated_skill_calls"] >= 2
        or (metrics["no_analytic_step"] and metrics["setup_calls"] >= 6)
    )

    scores: dict[str, int] = {}
    if inspection_active:
        scores["schema_file_inspection_loop"] = (
            metrics["inspect_calls"] + 2 * metrics["repeated_inspect_targets"] + metrics["stagnation_warnings"]
        )
    if query_active:
        scores["query_reformulation_loop"] = (
            metrics["query_file_calls"]
            + 2 * metrics["probe_query_calls"]
            + metrics["repeated_query_targets"]
            + 2 * metrics["repeated_query_signatures"]
        )
    if search_active:
        scores["search_thrash"] = metrics["search_calls"] + 2 * metrics["repeated_search_queries"]
    if download_active:
        scores["download_execute_detour"] = 2 * (
            metrics["download_calls"] + metrics["execute_code_calls"]
        ) + metrics["calls_before_first_analytic"] // 4
    if setup_active:
        scores["setup_replanning_churn"] = (
            metrics["setup_calls"]
            + 3 * metrics["repeated_plan_calls"]
            + 2 * metrics["repeated_skill_calls"]
        )
    return scores


def classify_waste(metrics: dict) -> tuple[str, str, str]:
    scores = _score_categories(metrics)
    if scores:
        primary_category = max(scores.items(), key=lambda item: (item[1], item[0]))[0]
        active_categories = ";".join(
            name for name, _ in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        )
    elif metrics["no_analytic_step"]:
        primary_category = "never_left_overhead"
        active_categories = primary_category
    elif metrics["ignored_stop_signal"]:
        primary_category = "failed_to_stop_and_answer"
        active_categories = primary_category
    else:
        primary_category = "mixed_overhead"
        active_categories = primary_category

    if primary_category == "schema_file_inspection_loop":
        rationale = (
            f"{metrics['inspect_calls']} inspect calls, "
            f"{metrics['repeated_inspect_targets']} repeated inspect targets"
        )
    elif primary_category == "query_reformulation_loop":
        rationale = (
            f"{metrics['query_file_calls']} query_file calls, "
            f"{metrics['probe_query_calls']} probe queries, "
            f"{metrics['repeated_query_targets']} repeated query targets"
        )
    elif primary_category == "search_thrash":
        rationale = (
            f"{metrics['search_calls']} search calls, "
            f"{metrics['repeated_search_queries']} repeated search queries"
        )
    elif primary_category == "download_execute_detour":
        rationale = (
            f"{metrics['download_calls']} downloads, "
            f"{metrics['execute_code_calls']} execute_code calls"
        )
    elif primary_category == "setup_replanning_churn":
        rationale = (
            f"{metrics['setup_calls']} setup calls, "
            f"{metrics['repeated_plan_calls']} repeated plans, "
            f"{metrics['repeated_skill_calls']} repeated skill refreshes"
        )
    elif primary_category == "never_left_overhead":
        rationale = f"{metrics['calls_before_first_analytic']} calls before any analytic step"
    elif primary_category == "failed_to_stop_and_answer":
        rationale = "received a stop-and-submit warning but did not cleanly cut over"
    else:
        rationale = "no single waste pattern dominated the run"

    return primary_category, active_categories, rationale


def _load_failed_rows(results_dir: Path, logs_dir: Path) -> list[dict]:
    detailed_rows: list[dict] = []
    for eval_path in sorted(results_dir.rglob("eval_results.csv")):
        variant = eval_path.parent.name
        model_variant = eval_path.parent.parent.name if eval_path.parent.parent else "unknown"
        with eval_path.open() as handle:
            for row in csv.DictReader(handle):
                bucket = row.get("log_error_bucket", "")
                if bucket not in TARGET_LOG_ERROR_BUCKETS:
                    continue
                task_path = Path(str(row["task_id"]))
                log_path = logs_dir / model_variant / variant / task_path.parent.name / f"{task_path.stem}.log"
                if not log_path.exists():
                    continue

                metrics = _parse_log(log_path)
                primary_category, active_categories, rationale = classify_waste(metrics)

                detailed_row = {
                    "model_variant": model_variant,
                    "mode_variant": variant,
                    "condition_model": f"{model_variant}/{variant}",
                    "task_id": row["task_id"],
                    "log_path": str(log_path),
                    "model": row.get("model", ""),
                    "log_error_bucket": bucket,
                    "runtime_seconds": _safe_float(row.get("runtime_seconds")),
                    "cycle_count": _safe_int(row.get("cycle_count")),
                    "tool_calls_total": _safe_int(row.get("tool_calls_total")),
                    "api_tool_calls": _safe_int(row.get("api_tool_calls")),
                    "input_tokens": _safe_int(row.get("input_tokens")),
                    "output_tokens": _safe_int(row.get("output_tokens")),
                    "total_tokens": _safe_int(row.get("total_tokens")),
                    "sources_used_count": _safe_int(row.get("sources_used_count")),
                    "required_dataset_count": _safe_int(row.get("required_dataset_count")),
                    "primary_waste_category": primary_category,
                    "active_waste_categories": active_categories,
                    "waste_rationale": rationale,
                }
                detailed_row.update(metrics)
                detailed_rows.append(detailed_row)

    return sorted(detailed_rows, key=lambda item: (item["condition_model"], item["task_id"]))


def _summarize_rows(rows: list[dict]) -> list[dict]:
    categories = Counter(row["primary_waste_category"] for row in rows)
    summary_rows = []
    for category, count in sorted(categories.items(), key=lambda item: (-item[1], item[0])):
        group = [row for row in rows if row["primary_waste_category"] == category]
        summary_rows.append(
            {
                "primary_waste_category": category,
                "runs": count,
                "share": count / len(rows) if rows else 0.0,
                "median_turns": _median([row["turn_count"] for row in group]),
                "median_logged_exec_calls": _median([row["logged_exec_calls"] for row in group]),
                "median_setup_calls": _median([row["setup_calls"] for row in group]),
                "median_search_calls": _median([row["search_calls"] for row in group]),
                "median_inspect_calls": _median([row["inspect_calls"] for row in group]),
                "median_query_file_calls": _median([row["query_file_calls"] for row in group]),
                "no_analytic_runs": sum(row["no_analytic_step"] for row in group),
                "ignored_stop_signal_runs": sum(row["ignored_stop_signal"] for row in group),
                "tool_limit_runs": sum(row["log_error_bucket"] == "error_tools_limit" for row in group),
                "token_limit_runs": sum(row["log_error_bucket"] == "error_tokens_reached" for row in group),
            }
        )
    return summary_rows


def _write_detailed_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _top_examples(rows: list[dict], category: str, limit: int = 2) -> list[dict]:
    category_rows = [row for row in rows if row["primary_waste_category"] == category]
    if not category_rows:
        return []

    def score(row: dict) -> tuple[int, int, int]:
        return (
            row["logged_exec_calls"],
            row["turn_count"],
            row["calls_before_first_analytic"],
        )

    return sorted(category_rows, key=score, reverse=True)[:limit]


def _build_markdown_report(rows: list[dict], summary_rows: list[dict], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    ideal_rows = [row for row in rows if row["mode_variant"] == "search_i_results_i_plani_k5"]
    ideal_summary = _summarize_rows(ideal_rows) if ideal_rows else []

    lines = [
        "# Turn Waste Analysis",
        "",
        "Scope: failed runs with `error_tokens_reached` or `error_tools_limit` aligned from",
        "`results-ec2_semantic/modes/.../eval_results.csv` to `logs-ec2/modes/.../*.log`.",
        "",
        f"- Failed runs analyzed: **{len(rows)}**",
        f"- Token-limit failures: **{sum(row['log_error_bucket'] == 'error_tokens_reached' for row in rows)}**",
        f"- Tool-limit failures: **{sum(row['log_error_bucket'] == 'error_tools_limit' for row in rows)}**",
        f"- Runs with no analytic step before failure: **{sum(row['no_analytic_step'] for row in rows)}**",
        f"- Runs that ignored a stop-and-submit warning: **{sum(row['ignored_stop_signal'] for row in rows)}**",
        "",
        "## Category Summary",
        "",
        "| Category | Runs | Share | Median Turns | Median Logged Calls | No Analytic | Ignored Stop Signal |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in summary_rows:
        lines.append(
            "| "
            f"{row['primary_waste_category']} | "
            f"{row['runs']} | "
            f"{row['share'] * 100:.1f}% | "
            f"{_format_median(row['median_turns'])} | "
            f"{_format_median(row['median_logged_exec_calls'])} | "
            f"{row['no_analytic_runs']} | "
            f"{row['ignored_stop_signal_runs']} |"
        )

    if ideal_rows:
        lines.extend(
            [
                "",
                "## Ideal-Context Subset",
                "",
                "Subset: `search_i_results_i_plani_k5`, where the whole planned context was already available.",
                "",
                f"- Failed runs: **{len(ideal_rows)}**",
                f"- Token-limit failures: **{sum(row['log_error_bucket'] == 'error_tokens_reached' for row in ideal_rows)}**",
                f"- Tool-limit failures: **{sum(row['log_error_bucket'] == 'error_tools_limit' for row in ideal_rows)}**",
                f"- Median turns: **{_format_median(_median([row['turn_count'] for row in ideal_rows]))}**",
                f"- Median calls before first analytic step: **{_format_median(_median([row['calls_before_first_analytic'] for row in ideal_rows]))}**",
                "",
                "| Category | Runs | Share | Median Turns | Median Logged Calls |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in ideal_summary:
            lines.append(
                "| "
                f"{row['primary_waste_category']} | "
                f"{row['runs']} | "
                f"{row['share'] * 100:.1f}% | "
                f"{_format_median(row['median_turns'])} | "
                f"{_format_median(row['median_logged_exec_calls'])} |"
            )

    lines.extend(
        [
            "",
            "## Category Definitions",
            "",
            "- `schema_file_inspection_loop`: budget spent on `list_files`/`peek_file`/`read_file`/`grep_file`, often on the same target repeatedly.",
            "- `query_reformulation_loop`: many `query_file` retries, probe queries, or repeated querying on the same dataset/file pair.",
            "- `search_thrash`: too many search calls or repeated search queries after the needed sources were already in scope.",
            "- `download_execute_detour`: switched into `download` + `execute_code` and burned budget in heavier local processing.",
            "- `setup_replanning_churn`: repeated `skills(...)` or `plan_ideal(...)` refreshes consumed budget without moving the task forward.",
            "- `never_left_overhead`: failure happened before any analytic step was reached and no single waste source dominated enough to beat the catch-all.",
            "- `failed_to_stop_and_answer`: received a stop-and-submit warning and still did not cleanly cut over to an answer.",
            "- `mixed_overhead`: overhead was real, but no single bucket dominated strongly enough to label it more specifically.",
            "",
            "## Example Runs",
            "",
        ]
    )

    for summary in summary_rows:
        category = summary["primary_waste_category"]
        examples = _top_examples(rows, category)
        if not examples:
            continue
        lines.append(f"### {category}")
        lines.append("")
        for example in examples:
            lines.append(
                "- "
                f"`{example['task_id']}` in `{example['condition_model']}`: "
                f"{example['waste_rationale']}; "
                f"{example['turn_count']} turns, {example['logged_exec_calls']} logged calls, "
                f"log bucket `{example['log_error_bucket']}`."
            )
        lines.append("")

    report_path.write_text("\n".join(lines))


def run_analysis(
    results_dir: str = "results-ec2_semantic/modes",
    logs_dir: str = "logs-ec2/modes",
    output_dir: str = "analysis_results_mode_semantic",
) -> dict:
    results_root = Path(results_dir)
    logs_root = Path(logs_dir)
    output_root = Path(output_dir)

    rows = _load_failed_rows(results_root, logs_root)
    summary_rows = _summarize_rows(rows)

    csv_path = output_root / "turn_waste_failed_runs.csv"
    markdown_path = output_root / "turn_waste_report.md"

    _write_detailed_csv(csv_path, rows)
    _build_markdown_report(rows, summary_rows, markdown_path)

    return {
        "rows": rows,
        "summary": summary_rows,
        "csv_path": csv_path,
        "markdown_path": markdown_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results-ec2_semantic/modes")
    parser.add_argument("--logs-dir", default="logs-ec2/modes")
    parser.add_argument("--output-dir", default="analysis_results_mode_semantic")
    args = parser.parse_args()

    outputs = run_analysis(
        results_dir=args.results_dir,
        logs_dir=args.logs_dir,
        output_dir=args.output_dir,
    )
    print(f"Wrote {outputs['csv_path']}")
    print(f"Wrote {outputs['markdown_path']}")


if __name__ == "__main__":
    main()
