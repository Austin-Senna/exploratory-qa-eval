#!/usr/bin/env python3
"""Prepare, judge, and summarize iid-vs-iii execution similarity audits."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.trajectory_pair_analysis import (  # noqa: E402
    BENCHMARK_LOG_ROOTS,
    EXECUTING_RE,
    _append_journal_record,
    _extract_runner_model,
    _first_executing_line,
    _mode_log_paths,
    _parse_json_object,
    _strip_log_prefix,
    _truncate,
    call_openai,
    resolve_judge_limit,
)


IDEAL_MODE = "search_i_results_i_plani_computei_k5_skills_off"
PAIR_MODES = {
    "iid_vs_iii": "search_i_results_i_plani_k5_skills_off",
}
LABELS = [
    "executes_correctly",
    "minor_execution_drift",
    "wrong_filter",
    "wrong_operation",
    "wrong_source",
    "wrong_intermediate",
    "wrong_finalization",
    "not_executed",
    "not_comparable",
]
GOOD_LABELS = {"executes_correctly", "minor_execution_drift"}
EXECUTION_TOOLS = {
    "download",
    "execute_code",
    "execute_ideal",
    "grep_file",
    "list_files",
    "parse_xml_records",
    "peek_file",
    "peek_multiple",
    "query_file",
    "query_ideal",
    "read_file",
    "search_prefix",
    "search_schema",
    "search_value",
    "submit_answer",
}
OUTPUT_COLUMNS = [
    "benchmark",
    "pair_label",
    "model_variant",
    "runner_model",
    "task_id",
    "comparison_mode",
    "ideal_mode",
    "comparison_log",
    "ideal_log",
    "comparison_start_line",
    "ideal_start_line",
    "comparison_event_count",
    "ideal_event_count",
    "execution_similarity",
    "execution_error_type",
    "comparison_execution_summary",
    "ideal_execution_summary",
    "aligned_operations",
    "divergent_operations",
    "similarity_reason",
    "evidence",
    "auditor_model",
    "audit_status",
]
AUDIT_UPDATE_COLUMNS = [
    "execution_similarity",
    "execution_error_type",
    "comparison_execution_summary",
    "ideal_execution_summary",
    "aligned_operations",
    "divergent_operations",
    "similarity_reason",
    "evidence",
    "auditor_model",
    "audit_status",
]


def extract_execution_excerpt(
    log_path: Path,
    *,
    start_after_line: int | None = None,
    max_events: int = 80,
    max_chars_per_event: int = 900,
) -> list[str]:
    if not log_path.exists():
        return []
    try:
        lines = log_path.read_text(errors="replace").splitlines()
    except OSError:
        return []

    events: list[str] = []
    last_kept_tool: str | None = None
    start_line = start_after_line or 0
    for line_number, line in enumerate(lines, start=1):
        if line_number <= start_line:
            continue
        if "Executing:" in line:
            match = EXECUTING_RE.search(line)
            tool = match.group(1) if match else ""
            if tool not in EXECUTION_TOOLS:
                last_kept_tool = None
                continue
            last_kept_tool = tool or None
            events.append(f"L{line_number}: {_truncate(_strip_log_prefix(line), max_chars_per_event)}")
        elif "Tool result:" in line and last_kept_tool:
            events.append(f"L{line_number}: {_truncate(_strip_log_prefix(line), max_chars_per_event)}")
            last_kept_tool = None
        elif "ANSWER:" in line:
            events.append(f"L{line_number}: {_truncate(_strip_log_prefix(line), max_chars_per_event)}")
        if len(events) >= max_events:
            break
    return events


def _prefill_not_comparable(row: dict[str, str], error_type: str, reason: str, evidence: str) -> None:
    row.update(
        {
            "execution_similarity": "not_comparable",
            "execution_error_type": error_type,
            "similarity_reason": reason,
            "evidence": evidence,
            "auditor_model": "mechanical",
            "audit_status": "complete",
        }
    )


def build_pair_rows(
    *,
    benchmark: str,
    log_root: Path,
    pair_label: str = "iid_vs_iii",
    model_filter: str | None = None,
    task_filter: str | None = None,
) -> list[dict[str, str]]:
    comparison_mode = PAIR_MODES[pair_label]
    paths_by_model_mode = _mode_log_paths(log_root)
    models = sorted(
        {
            model
            for model, mode in paths_by_model_mode
            if mode in {comparison_mode, IDEAL_MODE}
        }
    )
    rows: list[dict[str, str]] = []
    for model_variant in models:
        if model_filter and model_variant != model_filter:
            continue
        comparison_logs = paths_by_model_mode.get((model_variant, comparison_mode), {})
        ideal_logs = paths_by_model_mode.get((model_variant, IDEAL_MODE), {})
        task_ids = sorted(set(comparison_logs) | set(ideal_logs))
        for task_id in task_ids:
            if task_filter and task_filter not in task_id:
                continue
            comparison_log = comparison_logs.get(task_id)
            ideal_log = ideal_logs.get(task_id)
            comparison_log_str = str(comparison_log.resolve(strict=False)) if comparison_log else ""
            ideal_log_str = str(ideal_log.resolve(strict=False)) if ideal_log else ""
            comparison_plan_line = _first_executing_line(comparison_log, "plan_ideal") if comparison_log else None
            ideal_plan_line = _first_executing_line(ideal_log, "plan_ideal") if ideal_log else None
            comparison_start_line = comparison_plan_line or 0
            ideal_start_line = ideal_plan_line or 0
            comparison_events = (
                extract_execution_excerpt(comparison_log, start_after_line=comparison_start_line)
                if comparison_log
                else []
            )
            ideal_events = (
                extract_execution_excerpt(ideal_log, start_after_line=ideal_start_line)
                if ideal_log
                else []
            )
            comparison_model = _extract_runner_model(comparison_log) if comparison_log else ""
            ideal_model = _extract_runner_model(ideal_log) if ideal_log else ""
            runner_model = comparison_model or ideal_model
            if comparison_model and ideal_model and comparison_model != ideal_model:
                runner_model = f"{comparison_model}|{ideal_model}"

            row = {
                "benchmark": benchmark,
                "pair_label": pair_label,
                "model_variant": model_variant,
                "runner_model": runner_model,
                "task_id": task_id,
                "comparison_mode": comparison_mode,
                "ideal_mode": IDEAL_MODE,
                "comparison_log": comparison_log_str,
                "ideal_log": ideal_log_str,
                "comparison_start_line": str(comparison_start_line),
                "ideal_start_line": str(ideal_start_line),
                "comparison_event_count": str(len(comparison_events)),
                "ideal_event_count": str(len(ideal_events)),
                "execution_similarity": "",
                "execution_error_type": "",
                "comparison_execution_summary": "",
                "ideal_execution_summary": "",
                "aligned_operations": "",
                "divergent_operations": "",
                "similarity_reason": "",
                "evidence": "",
                "auditor_model": "",
                "audit_status": "pending",
            }
            if not comparison_log:
                _prefill_not_comparable(row, "comparison_log_missing", "The iid execution log is missing.", ideal_log_str)
            elif not ideal_log:
                _prefill_not_comparable(row, "ideal_log_missing", "The iii execution log is missing.", comparison_log_str)
            elif comparison_model and ideal_model and comparison_model != ideal_model:
                _prefill_not_comparable(
                    row,
                    "model_mismatch",
                    f"Runner model mismatch: iid log has {comparison_model}, iii log has {ideal_model}.",
                    f"{comparison_log_str}; {ideal_log_str}",
                )
            elif not comparison_plan_line:
                _prefill_not_comparable(
                    row,
                    "comparison_plan_missing",
                    "No explicit plan_ideal() call was found in the iid log.",
                    comparison_log_str,
                )
            elif not ideal_plan_line:
                _prefill_not_comparable(
                    row,
                    "ideal_plan_missing",
                    "No explicit plan_ideal() call was found in the iii log.",
                    ideal_log_str,
                )
            elif not comparison_events or not ideal_events:
                _prefill_not_comparable(
                    row,
                    "execution_missing",
                    "One side has no comparable post-plan execution/evidence-operation events.",
                    f"{comparison_log_str}; {ideal_log_str}",
                )
            rows.append(row)
    return rows


def load_existing_audits(path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="") as handle:
        existing = {}
        for row in csv.DictReader(handle):
            key = (
                row.get("benchmark", ""),
                row.get("pair_label", ""),
                row.get("model_variant", ""),
                row.get("task_id", ""),
            )
            existing[key] = dict(row)
        return existing


def load_tmp_audits(tmp_root: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    existing: dict[tuple[str, str, str, str], dict[str, str]] = {}
    if not tmp_root.exists():
        return existing
    for path in sorted(tmp_root.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        row_key = payload.get("row_key")
        row_update = payload.get("row_update")
        if not isinstance(row_key, dict) or not isinstance(row_update, dict):
            continue
        key = (
            str(row_key.get("benchmark", "")),
            str(row_key.get("pair_label", "")),
            str(row_key.get("model_variant", "")),
            str(row_key.get("task_id", "")),
        )
        if not all(key):
            continue
        existing[key] = {column: str(row_update.get(column, "")) for column in AUDIT_UPDATE_COLUMNS}
    return existing


def merge_existing_audits(rows: list[dict[str, str]], existing: dict[tuple[str, str, str, str], dict[str, str]]) -> None:
    for row in rows:
        key = (row["benchmark"], row["pair_label"], row["model_variant"], row["task_id"])
        old = existing.get(key)
        if old and old.get("audit_status") not in ("", "pending"):
            for column in AUDIT_UPDATE_COLUMNS:
                row[column] = old.get(column, row.get(column, ""))


def _pct(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 1) if denominator else 0.0


def _fraction(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator}" if denominator else "0/0"


def summarize_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["benchmark"], row["model_variant"], row["pair_label"])].append(row)

    summary_rows: list[dict[str, Any]] = []
    breakdown_rows: list[dict[str, Any]] = []
    for (benchmark, model_variant, pair_label), group_rows in sorted(grouped.items()):
        labels = Counter(row.get("execution_similarity", "") or "pending" for row in group_rows)
        statuses = Counter(row.get("audit_status", "") or "pending" for row in group_rows)
        n_total = len(group_rows)
        n_not_comparable = labels.get("not_comparable", 0)
        n_comparable = n_total - n_not_comparable
        n_good = sum(labels.get(label, 0) for label in GOOD_LABELS)
        row = {
            "benchmark": benchmark,
            "model_variant": model_variant,
            "pair_label": pair_label,
            "comparison_mode": PAIR_MODES[pair_label],
            "ideal_mode": IDEAL_MODE,
            "n_total": n_total,
            "n_complete": statuses.get("complete", 0),
            "n_pending": statuses.get("pending", 0),
            "n_comparable": n_comparable,
            "n_not_comparable": n_not_comparable,
            "n_execution_correct": n_good,
            "execution_correct_fraction_all": _fraction(n_good, n_total),
            "execution_correct_pct_all": _pct(n_good, n_total),
            "execution_correct_fraction_comparable": _fraction(n_good, n_comparable),
            "execution_correct_pct_comparable": _pct(n_good, n_comparable),
        }
        for label in LABELS:
            row[f"n_{label}"] = labels.get(label, 0)
            row[f"{label}_fraction_all"] = _fraction(labels.get(label, 0), n_total)
            row[f"{label}_pct_all"] = _pct(labels.get(label, 0), n_total)
        row["n_pending_label"] = labels.get("pending", 0)
        row["pending_fraction_all"] = _fraction(labels.get("pending", 0), n_total)
        summary_rows.append(row)

        for label, count in sorted(labels.items()):
            breakdown_rows.append(
                {
                    "benchmark": benchmark,
                    "model_variant": model_variant,
                    "pair_label": pair_label,
                    "execution_similarity": label,
                    "n": count,
                    "fraction_all": _fraction(count, n_total),
                    "pct_all": _pct(count, n_total),
                    "fraction_comparable": _fraction(count, n_comparable) if label != "not_comparable" else "",
                    "pct_comparable": _pct(count, n_comparable) if label != "not_comparable" else "",
                }
            )
    return summary_rows, breakdown_rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, rows: list[dict[str, str]]) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_path = output_dir / "execution_pair_audit.csv"
    summary_path = output_dir / "execution_pair_summary.csv"
    breakdown_path = output_dir / "execution_pair_label_breakdown.csv"
    json_path = output_dir / "execution_pair_summary.json"
    summary_rows, breakdown_rows = summarize_rows(rows)
    write_csv(audit_path, rows, OUTPUT_COLUMNS)
    write_csv(summary_path, summary_rows)
    write_csv(breakdown_path, breakdown_rows)
    json_path.write_text(
        json.dumps({"summary": summary_rows, "label_breakdown": breakdown_rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    return [audit_path, summary_path, breakdown_path, json_path]


def _row_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["benchmark"], row["pair_label"], row["model_variant"], row["task_id"])


def _row_slug(row: dict[str, str]) -> str:
    benchmark, pair_label, model_variant, task_id = _row_key(row)
    task_stem = Path(task_id).with_suffix("").as_posix()
    raw = "__".join([benchmark, pair_label, model_variant, task_stem])
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("_") or "row"


def _audit_json_path(tmp_root: Path, row: dict[str, str]) -> Path:
    return tmp_root / row["benchmark"] / row["model_variant"] / row["pair_label"] / f"{_row_slug(row)}.json"


def validate_judge_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    label = payload.get("execution_similarity")
    if label not in LABELS:
        errors.append(f"execution_similarity must be one of {LABELS}, got {label!r}")
    if payload.get("audit_status") != "complete":
        errors.append("audit_status must be 'complete'")
    for field in [
        "execution_error_type",
        "comparison_execution_summary",
        "ideal_execution_summary",
        "similarity_reason",
        "evidence",
    ]:
        if not isinstance(payload.get(field), str) or not str(payload.get(field)).strip():
            errors.append(f"{field} must be a non-empty string")
    for field in ["aligned_operations", "divergent_operations"]:
        if not isinstance(payload.get(field), str):
            errors.append(f"{field} must be a string")
    return errors


def build_repair_prompt(original_prompt: str, previous_text: str, errors: list[str]) -> str:
    return (
        original_prompt.rstrip()
        + "\n\nYour previous response failed deterministic validation.\n"
        + "Return JSON only, with exactly the required schema. Fix these errors:\n"
        + "\n".join(f"- {error}" for error in errors)
        + "\n\nPrevious response:\n```text\n"
        + previous_text
        + "\n```"
    )


def build_judge_prompt(row: dict[str, str]) -> str:
    comparison_events = extract_execution_excerpt(
        Path(row["comparison_log"]),
        start_after_line=int(row.get("comparison_start_line") or 0),
    )
    ideal_events = extract_execution_excerpt(
        Path(row["ideal_log"]),
        start_after_line=int(row.get("ideal_start_line") or 0),
    )
    return f"""You are judging execution similarity for the same task.

The ideal side is iii: ideal search, ideal results, ideal plan, and ideal computation tools.
The comparison side is iid: ideal search, ideal results, ideal plan, but normal execution tools.

Compare only post-plan execution/evidence operations: source/file binding, query/code operation, filters, joins/hops, computation correctness, and final answer binding. Do not penalize harmless tool-name differences such as query_file versus query_ideal if they implement the same operation on the same intended source.

Labels:
- executes_correctly: same intended source, filters, operation/computation, intermediate binding, and final answer.
- minor_execution_drift: same answer-producing execution with harmless retries, equivalent implementation, or small extra inspection.
- wrong_filter: misses or changes a key constraint such as year, county, status, threshold, entity, or row subset.
- wrong_operation: performs the wrong computation/query operation, such as sum vs mean or wrong denominator/formula.
- wrong_source: executes on the wrong dataset/file/source despite the ideal trajectory identifying another source.
- wrong_intermediate: carries the wrong entity/value between hops or joins.
- wrong_finalization: computes or inspects the right thing but submits the wrong value, column, entity, format, or final answer.
- not_executed: does not make a real comparable execution/query/file operation before finalizing or failing.
- not_comparable: insufficient/malformed logs, model/task mismatch, or impossible to compare.

Return JSON only:
{{
  "execution_similarity": "executes_correctly|minor_execution_drift|wrong_filter|wrong_operation|wrong_source|wrong_intermediate|wrong_finalization|not_executed|not_comparable",
  "execution_error_type": "none|source_binding|operation_binding|filter_binding|join_or_hop_binding|computation_correctness|output_binding|not_executed|other",
  "comparison_execution_summary": "one sentence",
  "ideal_execution_summary": "one sentence",
  "aligned_operations": "semicolon-separated aligned execution operations",
  "divergent_operations": "semicolon-separated divergent or missing operations",
  "similarity_reason": "short evidence-grounded reason",
  "evidence": "cite both log paths and relevant line numbers from the excerpts",
  "audit_status": "complete"
}}

Metadata:
- benchmark: {row['benchmark']}
- task_id: {row['task_id']}
- model_variant: {row['model_variant']}
- runner_model: {row['runner_model']}
- pair_label: {row['pair_label']}
- comparison_mode: {row['comparison_mode']}
- ideal_mode: {row['ideal_mode']}
- comparison_log: {row['comparison_log']}
- ideal_log: {row['ideal_log']}

IID EXECUTION:
{chr(10).join(comparison_events)}

III EXECUTION:
{chr(10).join(ideal_events)}
"""


def judge_pending_rows(
    rows: list[dict[str, str]],
    *,
    output_dir: Path,
    repo_root: Path,
    model: str,
    reasoning_effort: str,
    limit: int,
    timeout: int,
    tmp_root: Path,
    journal_path: Path,
    max_retries: int,
) -> int:
    judged = 0
    for row in rows:
        if row.get("audit_status") != "pending":
            continue
        if limit and judged >= limit:
            break
        prompt = build_judge_prompt(row)
        out_path = _audit_json_path(tmp_root, row)
        stem = out_path.with_suffix("")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path = stem.with_suffix(".prompt.txt")
        last_message_path = stem.with_suffix(".last_message.txt")
        attempt_prompt = prompt
        parsed: dict[str, Any] | None = None
        text = ""
        validation_errors: list[str] = []
        for attempt in range(1, max_retries + 2):
            prompt_path.write_text(attempt_prompt, encoding="utf-8")
            stem.with_suffix(f".attempt{attempt}.prompt.txt").write_text(attempt_prompt, encoding="utf-8")
            try:
                text = call_openai(
                    attempt_prompt,
                    repo_root=repo_root,
                    model=model,
                    reasoning_effort=reasoning_effort,
                    timeout=timeout,
                )
            except Exception as exc:
                _append_journal_record(
                    journal_path,
                    {
                        "status": "error",
                        "error": str(exc),
                        "attempt": attempt,
                        "benchmark": row["benchmark"],
                        "pair_label": row["pair_label"],
                        "model_variant": row["model_variant"],
                        "task_id": row["task_id"],
                        "prompt_path": str(prompt_path),
                    },
                )
                raise
            last_message_path.write_text(text, encoding="utf-8")
            stem.with_suffix(f".attempt{attempt}.last_message.txt").write_text(text, encoding="utf-8")
            try:
                parsed = _parse_json_object(text)
            except (json.JSONDecodeError, ValueError) as exc:
                validation_errors = [f"response must be a JSON object: {exc}"]
            else:
                validation_errors = validate_judge_payload(parsed)
            if not validation_errors:
                break
            _append_journal_record(
                journal_path,
                {
                    "status": "retry",
                    "attempt": attempt,
                    "errors": validation_errors,
                    "benchmark": row["benchmark"],
                    "pair_label": row["pair_label"],
                    "model_variant": row["model_variant"],
                    "task_id": row["task_id"],
                    "prompt_path": str(prompt_path),
                    "last_message_path": str(last_message_path),
                },
            )
            if attempt > max_retries:
                raise RuntimeError(
                    "Execution judge response failed validation after retries: "
                    + "; ".join(validation_errors)
                )
            attempt_prompt = build_repair_prompt(prompt, text, validation_errors)
        stem.with_suffix(".openai_stdout.log").write_text("", encoding="utf-8")
        assert parsed is not None
        label = str(parsed.get("execution_similarity", "not_comparable"))
        row.update(
            {
                "execution_similarity": label,
                "execution_error_type": str(parsed.get("execution_error_type", "other")),
                "comparison_execution_summary": str(parsed.get("comparison_execution_summary", "")),
                "ideal_execution_summary": str(parsed.get("ideal_execution_summary", "")),
                "aligned_operations": str(parsed.get("aligned_operations", "")),
                "divergent_operations": str(parsed.get("divergent_operations", "")),
                "similarity_reason": str(parsed.get("similarity_reason", "")),
                "evidence": str(parsed.get("evidence", "")),
                "auditor_model": model,
                "audit_status": str(parsed.get("audit_status", "complete") or "complete"),
            }
        )
        audit_payload = {
            "row_key": {
                "benchmark": row["benchmark"],
                "pair_label": row["pair_label"],
                "model_variant": row["model_variant"],
                "task_id": row["task_id"],
            },
            "judge_model": model,
            "reasoning_effort": reasoning_effort,
            "prompt_path": str(prompt_path),
            "last_message_path": str(last_message_path),
            "parsed": parsed,
            "row_update": {key: row[key] for key in AUDIT_UPDATE_COLUMNS},
        }
        out_path.write_text(json.dumps(audit_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _append_journal_record(
            journal_path,
            {
                "status": "ok",
                "benchmark": row["benchmark"],
                "pair_label": row["pair_label"],
                "model_variant": row["model_variant"],
                "task_id": row["task_id"],
                "label": label,
                "audit_json_path": str(out_path),
                "prompt_path": str(prompt_path),
                "last_message_path": str(last_message_path),
            },
        )
        judged += 1
        write_outputs(output_dir, rows)
        time.sleep(0.1)
    return judged


def build_all_rows(args: argparse.Namespace) -> list[dict[str, str]]:
    benchmarks = list(BENCHMARK_LOG_ROOTS) if args.benchmark == "all" else [args.benchmark]
    rows: list[dict[str, str]] = []
    for benchmark in benchmarks:
        root = Path(args.input_root) / BENCHMARK_LOG_ROOTS[benchmark]
        rows.extend(
            build_pair_rows(
                benchmark=benchmark,
                log_root=root,
                pair_label=args.pair,
                model_filter=args.model or None,
                task_filter=args.task or None,
            )
        )
    return rows


def row_matches_filters(row: dict[str, str], args: argparse.Namespace) -> bool:
    if args.benchmark != "all" and row["benchmark"] != args.benchmark:
        return False
    if args.model and row["model_variant"] != args.model:
        return False
    if args.task and args.task not in row["task_id"]:
        return False
    return True


def full_build_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(**{**vars(args), "benchmark": "all", "model": "", "task": ""})


def print_summary(rows: list[dict[str, str]]) -> None:
    summary_rows, _ = summarize_rows(rows)
    print("Execution-pair summary:")
    for row in summary_rows:
        print(
            f"  {row['benchmark']:<11} {row['model_variant']:<18} {row['pair_label']:<10} "
            f"correct={row['execution_correct_pct_all']:>5.1f}% "
            f"({row['execution_correct_fraction_all']}), "
            f"pending={row['n_pending_label']} n/c={row['n_not_comparable']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", default=".", help="Repository/input root containing logs and log-kramabench.")
    parser.add_argument("--output-dir", default="agent_analysis/execution_pair_analysis")
    parser.add_argument("--benchmark", choices=["all", *BENCHMARK_LOG_ROOTS.keys()], default="all")
    parser.add_argument("--pair", choices=list(PAIR_MODES), default="iid_vs_iii")
    parser.add_argument("--model", default="", help="Optional model folder, e.g. openai_gpt-5-mini.")
    parser.add_argument("--task", default="", help="Optional task-id substring filter.")
    parser.add_argument("--judge", action="store_true", help="Judge pending pairs with the OpenAI Responses API.")
    parser.add_argument("--judge-model", default="gpt-5.4-mini")
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max pending rows to judge. Omit for an interactive prompt; 0 means all.",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-retries", type=int, default=2, help="Retry invalid judge JSON this many times.")
    parser.add_argument(
        "--tmp-root",
        default="agent_analysis/execution_pair_analysis/tmp",
        help="Directory for per-row prompt, raw response, and parsed judge JSON files.",
    )
    parser.add_argument(
        "--journal-path",
        default="",
        help="Optional JSONL journal path. Defaults to <output-dir>/execution_pair_journal.jsonl.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    audit_path = output_dir / "execution_pair_audit.csv"
    tmp_root = Path(args.tmp_root).resolve()
    rows = build_all_rows(full_build_args(args))
    merge_existing_audits(rows, load_existing_audits(audit_path))
    merge_existing_audits(rows, load_tmp_audits(tmp_root))
    written = write_outputs(output_dir, rows)
    if args.judge:
        journal_path = Path(args.journal_path).resolve() if args.journal_path else output_dir / "execution_pair_journal.jsonl"
        print(f"Temp judge dir: {tmp_root}")
        print(f"JSONL journal: {journal_path}")
        rows_to_judge = [row for row in rows if row_matches_filters(row, args)]
        pending_count = sum(1 for row in rows_to_judge if row.get("audit_status") == "pending")
        judge_limit = resolve_judge_limit(
            requested_limit=args.limit,
            pending_count=pending_count,
            is_interactive=sys.stdin.isatty(),
        )
        if judge_limit is None:
            print("Aborted without judging rows.")
            print_summary(rows)
            for path in written:
                print(f"Wrote {path}")
            return 0
        judged = judge_pending_rows(
            rows_to_judge,
            output_dir=output_dir,
            repo_root=Path(args.input_root).resolve(),
            model=args.judge_model,
            reasoning_effort=args.reasoning_effort,
            limit=judge_limit,
            timeout=args.timeout,
            tmp_root=tmp_root,
            journal_path=journal_path,
            max_retries=args.max_retries,
        )
        print(f"Judged {judged} pending row(s).")
        rows = build_all_rows(full_build_args(args))
        merge_existing_audits(rows, load_existing_audits(audit_path))
        merge_existing_audits(rows, load_tmp_audits(tmp_root))
        written = write_outputs(output_dir, rows)
    print_summary(rows)
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
