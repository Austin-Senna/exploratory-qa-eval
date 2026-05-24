#!/usr/bin/env python3
"""Run answer-failure audits through external model calls and temp JSON files."""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.answer_failure_validation import (
    EVENT_COLUMNS,
    MODEL_VALIDATION_NOTES_FIELD,
    MODEL_VALIDATION_STATUS_FIELD,
    ROW_OUTPUT_COLUMNS,
    VALIDATION_NOTES_FIELD,
    VALIDATION_STATUS_FIELD,
    is_non_correct_row,
    row_log_path,
    validate_answer_failure_root,
)
from analysis.build_answer_failure_report import build_answer_failure_report


SOURCE_ROOTS = {
    "results_semantic": ("results_semantic_answer_failures", Path("logs/modes")),
    "results-ec2_semantic": ("results-ec2_semantic_answer_failures", Path("logs-ec2/modes")),
    "sana-results_semantic": ("sana-results_semantic_answer_failures", Path("sana-results/logs/modes")),
    "results-kramabench_semantic": ("results-kramabench_semantic_answer_failures", Path("log-kramabench/modes")),
}

PLAN_ROOTS = {
    "tasks_mini": "plans_mini",
    "tasks_mini_core": "plans_mini_core",
    "tasks-mini-kramabench": "plans-mini-kramabench",
    "tasks-hotpotqa-mini": "plans-hotpotqa-mini",
    "tasks_core_quality": "plans_core_quality",
}

DEFAULT_ROW_MODEL = "gpt-5.4-mini"
DEFAULT_ROW_REASONING = "medium"
DEFAULT_AUDITOR_MODEL = "gpt-5.4"
DEFAULT_AUDITOR_REASONING = "medium"

ANSWER_FAILURE_TYPE_ALIASES = {
    "computation": "computation_or_aggregation_error",
    "computation_error": "computation_or_aggregation_error",
    "computation_failure": "computation_or_aggregation_error",
    "reasoning": "computation_or_aggregation_error",
    "reasoning_error": "computation_or_aggregation_error",
    "data_access": "tool_or_data_blocker",
    "data_access_error": "tool_or_data_blocker",
    "data_access_failure": "tool_or_data_blocker",
    "system_failure": "tool_or_data_blocker",
    "tool_failure": "tool_or_data_blocker",
    "tool_misuse": "tool_or_data_blocker",
    "tool_limit": "incomplete_evidence_not_enough_turns",
    "tool_exhaustion": "incomplete_evidence_not_enough_turns",
    "evidence_gap": "incomplete_evidence_early_answer",
    "missing_evidence": "incomplete_evidence_early_answer",
    "source_selection": "wrong_source_or_scope",
    "source_selection_error": "wrong_source_or_scope",
    "source_selection_failure": "wrong_source_or_scope",
    "source_mistake": "wrong_source_or_scope",
    "source_mismatch": "wrong_source_or_scope",
    "wrong_source": "wrong_source_or_scope",
    "evidence_gathering_error": "incomplete_evidence_early_answer",
    "task_understanding": "question_or_constraint_misread",
    "entity_confusion": "question_or_constraint_misread",
    "extraction": "extraction_or_parsing_error",
    "extraction_error": "extraction_or_parsing_error",
    "submission": "evidence_available_answer_error",
    "submission_error": "evidence_available_answer_error",
    "submission_failure": "evidence_available_answer_error",
    "finalization": "evidence_available_answer_error",
    "finalization_error": "evidence_available_answer_error",
    "formatting": "evidence_available_answer_error",
    "hallucination": "evidence_available_answer_error",
    "hallucinated_answer": "evidence_available_answer_error",
    "unsupported_estimate": "evidence_available_answer_error",
    "wrong_answer": "evidence_available_answer_error",
    "retrieval": "incomplete_evidence_early_answer",
    "evidence_gathering": "incomplete_evidence_early_answer",
}


@dataclass(frozen=True)
class AuditLayout:
    repo_root: Path
    source_root: Path
    output_root: Path
    logs_root: Path
    eval_path: Path
    mirrored_eval_path: Path
    mirrored_events_path: Path
    mirrored_report_path: Path
    model_variant: str
    mode_variant: str


@dataclass(frozen=True)
class PendingEvalStats:
    eval_path: Path
    eligible_rows: int
    pending_rows: int
    invalid_rows: int
    has_all_artifacts: bool
    pending_task_ids: tuple[str, ...]
    invalid_task_ids: tuple[str, ...]


def infer_layout(eval_path: str | Path) -> AuditLayout:
    eval_path = Path(eval_path).resolve()
    source_root: Optional[Path] = None
    output_root_name = ""
    logs_rel = Path()

    for parent in [eval_path.parent, *eval_path.parents]:
        if parent.name in SOURCE_ROOTS:
            source_root = parent
            output_root_name, logs_rel = SOURCE_ROOTS[parent.name]
            break
    if source_root is None:
        known = ", ".join(sorted(SOURCE_ROOTS))
        raise ValueError(f"Could not infer source root for {eval_path}; expected one of: {known}")

    rel_path = eval_path.relative_to(source_root)
    parts = rel_path.parts
    if "modes" not in parts:
        raise ValueError(f"Expected eval path under a modes/ tree: {eval_path}")
    modes_index = parts.index("modes")
    after_modes = parts[modes_index + 1 :]
    if len(after_modes) < 3 or after_modes[-1] != "eval_results.csv":
        raise ValueError(f"Expected .../modes/{{model_variant}}/{{mode_variant}}/eval_results.csv: {eval_path}")

    repo_root = source_root.parent
    output_root = repo_root / output_root_name
    mirrored_eval_path = output_root / rel_path
    model_variant = after_modes[0]
    mode_variant = after_modes[1]
    return AuditLayout(
        repo_root=repo_root,
        source_root=source_root,
        output_root=output_root,
        logs_root=repo_root / logs_rel,
        eval_path=eval_path,
        mirrored_eval_path=mirrored_eval_path,
        mirrored_events_path=mirrored_eval_path.parent / "answer_failure_events.csv",
        mirrored_report_path=mirrored_eval_path.parent / "answer_failure_report.md",
        model_variant=model_variant,
        mode_variant=mode_variant,
    )


def _escape_quotes_in_backtick_spans_inside_json_strings(text: str) -> str:
    out: list[str] = []
    in_string = False
    in_backtick_span = False
    escaped = False
    for char in text:
        if escaped:
            out.append(char)
            escaped = False
            continue
        if in_string and char == "\\":
            out.append(char)
            escaped = True
            continue
        if in_string and char == "`":
            out.append(char)
            in_backtick_span = not in_backtick_span
            continue
        if in_string and in_backtick_span and char == '"':
            out.append('\\"')
            continue
        if char == '"':
            out.append(char)
            in_string = not in_string
            if not in_string:
                in_backtick_span = False
            continue
        out.append(char)
    return "".join(out)


def parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if fence:
        text = fence.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= start:
            text = text[start : end + 1]
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        repaired = _escape_quotes_in_backtick_spans_inside_json_strings(text)
        if repaired == text:
            raise
        try:
            parsed = json.loads(repaired)
        except json.JSONDecodeError:
            raise exc
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object")
    return parsed


def _read_source_rows(eval_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with eval_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(errors="replace")


def _resolve_plan_path(repo_root: Path, task_id: str) -> Optional[Path]:
    task_path = Path(task_id)
    if not task_path.parts:
        return None
    plan_root = PLAN_ROOTS.get(task_path.parts[0])
    if plan_root is None:
        return None
    plan_path = repo_root / plan_root / Path(*task_path.parts[1:])
    return plan_path if plan_path.exists() else None


def _load_prompt_artifacts(
    *,
    layout: AuditLayout,
    source_row: dict[str, str],
    task_id: str,
    log_path: Path,
) -> dict[str, Any]:
    task_path = layout.repo_root / task_id
    plan_path = _resolve_plan_path(layout.repo_root, task_id)
    return {
        "source_row_text": json.dumps(source_row, ensure_ascii=False, indent=2),
        "task_path": task_path,
        "task_text": _read_text_if_exists(task_path),
        "plan_path": plan_path,
        "plan_text": _read_text_if_exists(plan_path) if plan_path is not None else "",
        "log_path": log_path,
        "log_text": _read_text_if_exists(log_path),
    }


def _mirrored_output_complete(layout: AuditLayout) -> bool:
    required = [layout.mirrored_eval_path, layout.mirrored_events_path, layout.mirrored_report_path]
    if any(not path.exists() for path in required):
        return False

    try:
        with layout.mirrored_eval_path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                if is_non_correct_row(row) and row.get(VALIDATION_STATUS_FIELD) in {"invalid", "missing_log"}:
                    return False
    except OSError:
        return False
    return True


def _default_tmp_root_for_layout(layout: AuditLayout) -> Path:
    return layout.repo_root / ".tmp_answer_failure_audits"


def _cached_audit_task_ids(
    layout: AuditLayout,
    *,
    tmp_root: Optional[str | Path] = None,
    journal_path: Optional[str | Path] = None,
    task_ids: Optional[list[str]] = None,
) -> set[str]:
    candidates = set(task_ids or [])
    cached: set[str] = set()
    resolved_tmp_root = Path(tmp_root) if tmp_root is not None else _default_tmp_root_for_layout(layout)
    if not resolved_tmp_root.is_absolute():
        resolved_tmp_root = layout.repo_root / resolved_tmp_root
    for task_id in candidates:
        path = _audit_json_path(resolved_tmp_root, layout, task_id)
        if not path.exists():
            continue
        try:
            parsed = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(parsed, dict):
            cached.add(task_id)

    resolved_journal_path = Path(journal_path) if journal_path is not None else _default_journal_path(layout)
    cached.update(task_id for task_id in _load_journal_audits(resolved_journal_path, layout) if not candidates or task_id in candidates)
    return cached


def eval_pending_stats(
    eval_path: str | Path,
    *,
    tmp_root: Optional[str | Path] = None,
    journal_path: Optional[str | Path] = None,
) -> PendingEvalStats:
    layout = infer_layout(eval_path)
    source_rows, _ = _read_source_rows(layout.eval_path)
    eligible_task_ids = [str(row.get("task_id", "")) for row in source_rows if is_non_correct_row(row)]
    cached_task_ids = _cached_audit_task_ids(
        layout,
        tmp_root=tmp_root,
        journal_path=journal_path,
        task_ids=eligible_task_ids,
    )
    required = [layout.mirrored_eval_path, layout.mirrored_events_path, layout.mirrored_report_path]
    has_all_artifacts = all(path.exists() for path in required)
    if not has_all_artifacts or not layout.mirrored_eval_path.exists():
        pending_task_ids = [task_id for task_id in eligible_task_ids if task_id not in cached_task_ids]
        return PendingEvalStats(
            eval_path=layout.eval_path,
            eligible_rows=len(eligible_task_ids),
            pending_rows=len(pending_task_ids),
            invalid_rows=0,
            has_all_artifacts=has_all_artifacts,
            pending_task_ids=tuple(pending_task_ids),
            invalid_task_ids=(),
        )

    pending_task_ids: list[str] = []
    invalid_task_ids: list[str] = []
    try:
        with layout.mirrored_eval_path.open(newline="") as handle:
            mirrored_by_task = {str(row.get("task_id", "")): row for row in csv.DictReader(handle)}
    except OSError:
        mirrored_by_task = {}
    for task_id in eligible_task_ids:
        mirrored = mirrored_by_task.get(task_id)
        status = str((mirrored or {}).get(VALIDATION_STATUS_FIELD, ""))
        if task_id in cached_task_ids:
            continue
        if mirrored is None or not status:
            pending_task_ids.append(task_id)
        elif status in {"invalid", "missing_log"}:
            invalid_task_ids.append(task_id)

    return PendingEvalStats(
        eval_path=layout.eval_path,
        eligible_rows=len(eligible_task_ids),
        pending_rows=len(pending_task_ids),
        invalid_rows=len(invalid_task_ids),
        has_all_artifacts=has_all_artifacts,
        pending_task_ids=tuple(pending_task_ids),
        invalid_task_ids=tuple(invalid_task_ids),
    )


def find_pending_eval_stats(
    repo_root: str | Path,
    *,
    source_root_name: str = "results_semantic",
    tmp_root: Optional[str | Path] = None,
    journal_path: Optional[str | Path] = None,
) -> list[PendingEvalStats]:
    repo_root = Path(repo_root).resolve()
    source_root = repo_root / source_root_name
    if source_root_name not in SOURCE_ROOTS:
        known = ", ".join(sorted(SOURCE_ROOTS))
        raise ValueError(f"Unknown source root {source_root_name}; expected one of: {known}")
    if not source_root.exists():
        return []
    pending: list[PendingEvalStats] = []
    for eval_path in sorted((source_root / "modes").rglob("eval_results.csv")):
        stats = eval_pending_stats(eval_path, tmp_root=tmp_root, journal_path=journal_path)
        if not stats.has_all_artifacts or stats.pending_rows or stats.invalid_rows:
            pending.append(stats)
    return pending


def find_pending_eval_paths(
    repo_root: str | Path,
    *,
    source_root_name: str = "results_semantic",
    tmp_root: Optional[str | Path] = None,
    journal_path: Optional[str | Path] = None,
) -> list[Path]:
    return [
        stats.eval_path
        for stats in find_pending_eval_stats(
            repo_root,
            source_root_name=source_root_name,
            tmp_root=tmp_root,
            journal_path=journal_path,
        )
    ]


def _load_audits_from_mirrored_outputs(layout: AuditLayout) -> dict[str, dict[str, Any]]:
    if not layout.mirrored_eval_path.exists() or not layout.mirrored_events_path.exists():
        return {}
    with layout.mirrored_eval_path.open(newline="") as handle:
        eval_by_task = {str(row.get("task_id", "")): row for row in csv.DictReader(handle)}
    events_by_task: dict[str, list[dict[str, Any]]] = {}
    with layout.mirrored_events_path.open(newline="") as handle:
        for event in csv.DictReader(handle):
            task_id = str(event.get("task_id", ""))
            events_by_task.setdefault(task_id, []).append(
                {
                    "event_index": event.get("event_index", ""),
                    "answer_failure_type": event.get("answer_failure_type", ""),
                    "answer_failure_subtype": event.get("answer_failure_subtype", ""),
                    "failure_stage": event.get("failure_stage", ""),
                    "failure_summary": event.get("failure_summary", ""),
                    "failure_evidence": event.get("failure_evidence", ""),
                    "confidence": event.get("confidence", ""),
                }
            )
    audits: dict[str, dict[str, Any]] = {}
    for task_id, events in events_by_task.items():
        row = eval_by_task.get(task_id, {})
        audits[task_id] = {
            "task_id": task_id,
            "answer_failure_summary": row.get("answer_failure_summary", ""),
            "events": events,
        }
    return audits


def _task_slug(task_id: str) -> str:
    return task_id.replace("/", "__").replace("\\", "__").replace(".json", "")


def _temp_dir_for_layout(tmp_root: Path, layout: AuditLayout) -> Path:
    return tmp_root / layout.source_root.name / f"{layout.model_variant}__{layout.mode_variant}"


def _audit_json_path(tmp_root: Path, layout: AuditLayout, task_id: str) -> Path:
    return _temp_dir_for_layout(tmp_root, layout) / f"{_task_slug(task_id)}.json"


def _slug_for_journal(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def _compact_slug_for_journal(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "", value)


def _short_mode_variant(mode_variant: str) -> str:
    tokens = mode_variant.split("_")
    kept: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "results":
            index += 2
            continue
        if re.fullmatch(r"k\d+", token) or token in {"skills", "off", "on"}:
            index += 1
            continue
        kept.append(token)
        index += 1
    return "_".join(kept)


def _default_journal_path(layout: AuditLayout) -> Path:
    source_slug = _slug_for_journal(layout.source_root.name)
    model_slug = _compact_slug_for_journal(layout.model_variant)
    mode_slug = _short_mode_variant(layout.mode_variant)
    return Path("/tmp") / f"answer_failure_audits_{source_slug}_{model_slug}_{mode_slug}.jsonl"


def _append_journal_record(
    journal_path: Path,
    *,
    layout: AuditLayout,
    task_id: str,
    status: str,
    audit: Optional[dict[str, Any]] = None,
    error: str = "",
) -> None:
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    record: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_variant": layout.model_variant,
        "mode_variant": layout.mode_variant,
        "source_eval": str(layout.eval_path),
        "task_id": task_id,
        "status": status,
    }
    if audit is not None:
        record["audit"] = audit
    if error:
        record["error"] = error
    with journal_path.open("a") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load_journal_audits(journal_path: Path, layout: AuditLayout) -> dict[str, dict[str, Any]]:
    if not journal_path.exists():
        return {}
    audits: dict[str, dict[str, Any]] = {}
    with journal_path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"warning: ignoring malformed journal line {line_number} in {journal_path}", file=sys.stderr)
                continue
            if record.get("model_variant") != layout.model_variant or record.get("mode_variant") != layout.mode_variant:
                continue
            if record.get("source_eval") != str(layout.eval_path):
                continue
            if record.get("status") != "ok" or not isinstance(record.get("audit"), dict):
                continue
            task_id = str(record.get("task_id", ""))
            if task_id:
                audits[task_id] = record["audit"]
    return audits


def _row_summary_from_events(events: list[dict[str, Any]]) -> dict[str, str]:
    types: list[str] = []
    subtypes: list[str] = []
    evidence: list[str] = []
    summaries: list[str] = []
    for event in sorted(events, key=lambda row: int(str(row.get("event_index") or 0))):
        failure_type = " ".join(str(event.get("answer_failure_type", "")).split())
        subtype = " ".join(str(event.get("answer_failure_subtype", "")).split())
        if failure_type and failure_type not in types:
            types.append(failure_type)
        if subtype and subtype not in subtypes:
            subtypes.append(subtype)
        if str(event.get("failure_evidence", "")).strip():
            evidence.append(" ".join(str(event.get("failure_evidence", "")).split()))
        if str(event.get("failure_summary", "")).strip():
            summaries.append(" ".join(str(event.get("failure_summary", "")).split()))
    return {
        "answer_failure_types": "; ".join(types),
        "answer_failure_subtypes": "; ".join(subtypes),
        "answer_failure_event_count": str(len(events)),
        "answer_failure_evidence": "; ".join(evidence[:4]),
        "answer_failure_summary": "; ".join(summaries[:3]),
    }


def _normalized_events(audit: dict[str, Any]) -> list[dict[str, str]]:
    events = audit.get("events") or []
    if not isinstance(events, list):
        raise ValueError(f"Audit for {audit.get('task_id')} has non-list events")
    normalized: list[dict[str, str]] = []
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict):
            raise ValueError(f"Audit for {audit.get('task_id')} has non-object event {index}")
        event_index = event.get("event_index") or index
        failure_type = str(event.get("answer_failure_type", ""))
        normalized_type = ANSWER_FAILURE_TYPE_ALIASES.get(failure_type, failure_type)
        subtype = str(event.get("answer_failure_subtype", ""))
        if normalized_type == "tool_or_data_blocker" and not subtype:
            subtype = "data_source_missing_or_unavailable"
        if failure_type in {"tool_limit", "tool_exhaustion"} and not subtype:
            subtype = "tool_budget_exhausted"
        normalized.append(
            {
                "event_index": str(event_index),
                "answer_failure_type": normalized_type,
                "answer_failure_subtype": subtype,
                "failure_stage": str(event.get("failure_stage", "")),
                "failure_summary": str(event.get("failure_summary", "")),
                "failure_evidence": str(event.get("failure_evidence", "")),
                "confidence": str(event.get("confidence", "")),
            }
        )
    return normalized


def write_mirrored_outputs(
    layout: AuditLayout,
    audits_by_task: dict[str, dict[str, Any]],
    *,
    model_validation_by_task: Optional[dict[str, dict[str, str]]] = None,
) -> dict[str, Any]:
    rows, fieldnames = _read_source_rows(layout.eval_path)
    fieldnames = list(fieldnames)
    for column in ROW_OUTPUT_COLUMNS:
        if column not in fieldnames:
            fieldnames.append(column)

    model_validation_by_task = model_validation_by_task or {}
    event_rows: list[dict[str, str]] = []
    output_rows: list[dict[str, str]] = []

    for row in rows:
        output_row = dict(row)
        task_id = str(row.get("task_id", ""))
        if is_non_correct_row(row):
            audit = audits_by_task.get(task_id)
            if audit is None:
                raise ValueError(f"Missing audit JSON for eligible task_id: {task_id}")
            events = _normalized_events(audit)
            summary = _row_summary_from_events(events)
            if str(audit.get("answer_failure_summary", "")).strip():
                summary["answer_failure_summary"] = str(audit.get("answer_failure_summary", "")).strip()
            output_row.update(summary)
            output_row[VALIDATION_STATUS_FIELD] = ""
            output_row[VALIDATION_NOTES_FIELD] = ""
            validation = model_validation_by_task.get(task_id, {})
            output_row[MODEL_VALIDATION_STATUS_FIELD] = validation.get("status", "")
            output_row[MODEL_VALIDATION_NOTES_FIELD] = validation.get("notes", "")
            for event in events:
                event_rows.append(
                    {
                        "task_id": task_id,
                        "model_variant": layout.model_variant,
                        "mode_variant": layout.mode_variant,
                        **event,
                    }
                )
        else:
            for column in ROW_OUTPUT_COLUMNS:
                output_row[column] = ""
        output_rows.append(output_row)

    layout.mirrored_eval_path.parent.mkdir(parents=True, exist_ok=True)
    with layout.mirrored_eval_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    event_rows.sort(key=lambda row: (row["task_id"], int(row["event_index"] or 0)))
    with layout.mirrored_events_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EVENT_COLUMNS)
        writer.writeheader()
        writer.writerows(event_rows)

    return {
        "eval_path": layout.mirrored_eval_path,
        "events_path": layout.mirrored_events_path,
        "row_count": len(output_rows),
        "event_count": len(event_rows),
    }


def _missing_log_audit(task_id: str) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "answer_failure_summary": "The raw log is missing, so no grounded diagnosis is possible.",
        "events": [
            {
                "event_index": 1,
                "answer_failure_type": "ungroundable",
                "answer_failure_subtype": "missing_or_malformed_log",
                "failure_stage": "validation",
                "failure_summary": "The raw log is missing, so no grounded diagnosis is possible.",
                "failure_evidence": "matching raw log missing from logs root",
                "confidence": "high",
            }
        ],
    }


def _build_row_prompt(
    *,
    layout: AuditLayout,
    source_row: dict[str, str],
    task_id: str,
    log_path: Path,
    backend: str,
    repair_notes: str = "",
) -> str:
    skill_path = layout.repo_root / ".agents" / "skills" / "answer-failure-auditor" / "SKILL.md"
    raw_log_root = layout.logs_root / layout.model_variant / layout.mode_variant
    artifacts = _load_prompt_artifacts(
        layout=layout,
        source_row=source_row,
        task_id=task_id,
        log_path=log_path,
    )
    base = f"""You are the row-audit subagent for Answer Failure Auditor at {skill_path}.
Use that skill only as taxonomy/reference context.
Do not spawn agents. Do not run the file-level workflow. Do not process any other row.

Audit why this one non-correct answer failed.
Source eval: {layout.eval_path}
Task id: {task_id}
Raw log root: {raw_log_root}/ (.json -> .log)

Read the task JSON and matching raw log directly.
Do not estimate turn waste. Do not choose one dominant error if multiple material failures are visible.

Resolved matching raw log: {log_path}

Return JSON only with keys: task_id, answer_failure_summary, events.
Each event must include event_index, answer_failure_type, answer_failure_subtype, failure_stage, failure_summary, failure_evidence, confidence.
Evidence must be raw-log anchored and start with Turn N |  when citing a turn.
If the log is missing/unusable, return one ungroundable event with subtype missing_or_malformed_log.

{{
  "task_id": "{task_id}",
  "answer_failure_summary": "short row-level summary",
  "events": [
    {{
      "event_index": 1,
      "answer_failure_type": "one allowed type",
      "answer_failure_subtype": "short subtype or empty string",
      "failure_stage": "task_understanding | source_selection | data_access | evidence_gathering | computation | extraction | finalization | submission | validation",
      "failure_summary": "short string",
      "failure_evidence": "Turn N | exact or tightly grounded log fragment",
      "confidence": "high | medium | low"
    }}
  ]
}}
"""
    plan_path = artifacts["plan_path"] or "(no matching plan file found)"
    repair_block = ""
    if repair_notes:
        repair_block = (
            "\nPrevious deterministic validation failed for this row:\n"
            + repair_notes
            + "\n\nRepair requirements:\n"
            + "- Use only allowed answer_failure_type taxonomy labels from the skill.\n"
            + "- If citing an exact tool call/result/exception prefix like `Executing:` or `Tool result:`, copy the raw-log text exactly.\n"
            + "- If you cannot copy the exact raw-log text, keep the `Turn N | ` anchor but paraphrase without starting the evidence snippet with `Executing:`, `Tool result:`, `WARNING`, `ERROR`, `Traceback`, or `Exception`.\n"
            + "- Return at least one event for this non-correct row unless the log is missing/unusable.\n"
        )
    return (
        base
        + repair_block
        + "\nAssigned artifacts are embedded below. Use these embedded artifacts as the audit source of truth.\n\n"
        + "CSV row JSON:\n```json\n"
        + artifacts["source_row_text"]
        + "\n```\n\nTask JSON path: "
        + str(artifacts["task_path"])
        + "\nTask JSON:\n```json\n"
        + artifacts["task_text"]
        + "\n```\n\nPlan JSON path: "
        + str(plan_path)
        + "\nPlan JSON:\n```json\n"
        + artifacts["plan_text"]
        + "\n```\n\nRaw log path: "
        + str(artifacts["log_path"])
        + "\nRaw log:\n```text\n"
        + artifacts["log_text"]
        + "\n```"
    )


def _call_codex(
    prompt: str,
    *,
    cwd: Path,
    model: str,
    reasoning_effort: str,
    last_message_path: Path,
    stdout_path: Path,
    timeout: int,
) -> str:
    last_message_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "codex",
        "exec",
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "-C",
        str(cwd),
        "-s",
        "workspace-write",
        "--output-last-message",
        str(last_message_path),
        "-",
    ]
    proc = subprocess.run(
        cmd,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    stdout_path.write_text(proc.stdout)
    if proc.returncode != 0:
        raise RuntimeError(f"codex exec failed with exit code {proc.returncode}; see {stdout_path}")
    if last_message_path.exists():
        return last_message_path.read_text()
    return proc.stdout


def _extract_response_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    pieces: list[str] = []
    for item in payload.get("output", []) or []:
        for content in item.get("content", []) or []:
            text = content.get("text")
            if isinstance(text, str):
                pieces.append(text)
    return "\n".join(pieces)


def _openai_api_key(repo_root: Path) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    env_path = repo_root / ".env"
    if env_path.exists():
        with env_path.open() as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                if key == "OPENAI_API_KEY":
                    return value.strip().strip('"').strip("'")
    return ""


def _call_openai(prompt: str, *, cwd: Path, model: str, reasoning_effort: str, timeout: int) -> str:
    api_key = _openai_api_key(cwd)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for --backend openai")
    body = {
        "model": model,
        "input": prompt,
        "reasoning": {"effort": reasoning_effort},
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    text = _extract_response_text(payload)
    if not text:
        raise RuntimeError("OpenAI response did not contain output text")
    return text


def _call_model(
    prompt: str,
    *,
    backend: str,
    cwd: Path,
    model: str,
    reasoning_effort: str,
    last_message_path: Path,
    stdout_path: Path,
    timeout: int,
) -> str:
    if backend == "codex":
        return _call_codex(
            prompt,
            cwd=cwd,
            model=model,
            reasoning_effort=reasoning_effort,
            last_message_path=last_message_path,
            stdout_path=stdout_path,
            timeout=timeout,
        )
    if backend == "openai":
        text = _call_openai(prompt, cwd=cwd, model=model, reasoning_effort=reasoning_effort, timeout=timeout)
        last_message_path.parent.mkdir(parents=True, exist_ok=True)
        last_message_path.write_text(text)
        stdout_path.write_text("")
        return text
    raise ValueError(f"Unsupported backend: {backend}")


def run_row_audit(
    *,
    layout: AuditLayout,
    source_row: dict[str, str],
    tmp_root: Path,
    backend: str,
    model: str,
    reasoning_effort: str,
    timeout: int,
    force: bool,
    repair_notes: str = "",
) -> tuple[str, dict[str, Any]]:
    task_id = str(source_row.get("task_id", ""))
    out_path = _audit_json_path(tmp_root, layout, task_id)
    if out_path.exists() and not force:
        print(f"row audit cache hit: task={task_id}", flush=True)
        return task_id, json.loads(out_path.read_text())

    log_path = row_log_path(layout.logs_root, layout.model_variant, layout.mode_variant, task_id)
    if not log_path.exists():
        print(f"row audit missing log: task={task_id} log={log_path}", flush=True)
        audit = _missing_log_audit(task_id)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(audit, indent=2) + "\n")
        return task_id, audit

    print(
        f"row audit start: task={task_id} model={layout.model_variant} "
        f"mode={layout.mode_variant} backend={backend}",
        flush=True,
    )
    if backend == "codex":
        print(f"  spawning codex row-audit subagent for task={task_id}", flush=True)
    else:
        print(f"  calling {backend} row-audit judge for task={task_id}", flush=True)
    prompt = _build_row_prompt(
        layout=layout,
        source_row=source_row,
        task_id=task_id,
        log_path=log_path,
        backend=backend,
        repair_notes=repair_notes,
    )
    stem = out_path.with_suffix("")
    text = _call_model(
        prompt,
        backend=backend,
        cwd=layout.repo_root,
        model=model,
        reasoning_effort=reasoning_effort,
        last_message_path=stem.with_suffix(".last_message.txt"),
        stdout_path=stem.with_suffix(f".{backend}_stdout.log"),
        timeout=timeout,
    )
    audit = parse_json_object(text)
    audit["task_id"] = task_id
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    return task_id, audit


def _load_audits_for_rows(layout: AuditLayout, tmp_root: Path, rows: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    audits: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not is_non_correct_row(row):
            continue
        task_id = str(row.get("task_id", ""))
        path = _audit_json_path(tmp_root, layout, task_id)
        if path.exists():
            audits[task_id] = json.loads(path.read_text())
    return audits


def _deterministic_status_by_task(layout: AuditLayout) -> dict[str, dict[str, str]]:
    if not layout.mirrored_eval_path.exists():
        return {}
    with layout.mirrored_eval_path.open(newline="") as handle:
        return {
            str(row.get("task_id", "")): {
                "status": str(row.get(VALIDATION_STATUS_FIELD, "")),
                "notes": str(row.get(VALIDATION_NOTES_FIELD, "")),
            }
            for row in csv.DictReader(handle)
        }


def _task_ids_for_deterministic_repair(validation_outputs: dict[str, Any]) -> list[str]:
    task_ids: list[str] = []
    for row in validation_outputs.get("invalid_rows", []):
        if row.get(VALIDATION_STATUS_FIELD) != "invalid":
            continue
        task_id = str(row.get("task_id", ""))
        if task_id and task_id not in task_ids:
            task_ids.append(task_id)
    return task_ids


def _build_batch_auditor_prompt(
    *,
    layout: AuditLayout,
    tmp_root: Path,
    audits_by_task: dict[str, dict[str, Any]],
    deterministic_by_task: dict[str, dict[str, str]],
    backend: str,
) -> str:
    rows = [
        {
            "task_id": task_id,
            "deterministic_validation": deterministic_by_task.get(task_id, {}),
            "audit": audit,
        }
        for task_id, audit in sorted(audits_by_task.items())
        if deterministic_by_task.get(task_id, {}).get("status") in {"valid", "valid_with_warnings"}
    ]
    base = f"""You are the final batch auditor for $answer-failure-auditor.
Do not spawn agents. Audit the row-level JSON outputs as a batch.

Source eval: {layout.eval_path}
Mirrored eval: {layout.mirrored_eval_path}
Mirrored events: {layout.mirrored_events_path}
Temporary JSON directory: {_temp_dir_for_layout(tmp_root, layout)}
Logs root: {layout.logs_root}

For each row, return pass if the JSON is grounded enough to keep, needs_repair if it should be replaced by a smaller grounded version, or invalid_untrusted if it should not be summarized.
Prefer deleting weak events over inventing stronger narratives.
Return JSON only:
{{
  "rows": [
    {{
      "task_id": "tasks_mini/.../task_1.json",
      "verdict": "pass | needs_repair | invalid_untrusted",
      "problems": ["short string"],
      "supported_facts": ["short string"],
      "repaired_row": {{
        "task_id": "tasks_mini/.../task_1.json",
        "answer_failure_summary": "short string",
        "events": []
      }}
    }}
  ]
}}
"""
    if backend == "codex":
        return (
            base
            + "\nRead the temporary JSON files directly. Inspect raw logs only when needed to resolve grounding doubts. "
            + "Apply a verdict to every valid or valid_with_warnings row."
        )
    return base + "\nEmbedded row audit payload:\n```json\n" + json.dumps(rows, indent=2) + "\n```"


def _validated_batch_repair(original: dict[str, Any], repaired: dict[str, Any]) -> tuple[dict[str, Any], str]:
    events = repaired.get("events")
    if not isinstance(events, list) or not events:
        return original, "empty repaired_row rejected; kept original row audit"
    return repaired, ""


def run_batch_auditor(
    *,
    layout: AuditLayout,
    tmp_root: Path,
    audits_by_task: dict[str, dict[str, Any]],
    deterministic_by_task: dict[str, dict[str, str]],
    backend: str,
    model: str,
    reasoning_effort: str,
    timeout: int,
    allow_downgrade: bool,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, Any]]]:
    prompt = _build_batch_auditor_prompt(
        layout=layout,
        tmp_root=tmp_root,
        audits_by_task=audits_by_task,
        deterministic_by_task=deterministic_by_task,
        backend=backend,
    )
    batch_dir = _temp_dir_for_layout(tmp_root, layout)
    print(
        f"batch auditor start: model={layout.model_variant} mode={layout.mode_variant} "
        f"backend={backend} rows={len(audits_by_task)}",
        flush=True,
    )
    if backend == "codex":
        print(
            f"  spawning codex batch-auditor subagent for model={layout.model_variant} "
            f"mode={layout.mode_variant}",
            flush=True,
        )
    else:
        print(f"  calling {backend} batch auditor for model={layout.model_variant}", flush=True)
    text = _call_model(
        prompt,
        backend=backend,
        cwd=layout.repo_root,
        model=model,
        reasoning_effort=reasoning_effort,
        last_message_path=batch_dir / "batch_auditor.last_message.txt",
        stdout_path=batch_dir / f"batch_auditor.{backend}_stdout.log",
        timeout=timeout,
    )
    payload = parse_json_object(text)
    rows = payload.get("rows") or []
    if not isinstance(rows, list):
        raise ValueError("Batch auditor JSON must contain a rows list")

    validation_by_task: dict[str, dict[str, str]] = {}
    repaired_audits = dict(audits_by_task)
    for item in rows:
        if not isinstance(item, dict):
            continue
        task_id = str(item.get("task_id", ""))
        verdict = str(item.get("verdict", "invalid_untrusted"))
        problems = item.get("problems") or []
        notes = "; ".join(str(problem) for problem in problems if str(problem).strip())
        if verdict == "pass":
            validation_by_task[task_id] = {"status": "pass", "notes": notes}
        elif verdict == "needs_repair" and isinstance(item.get("repaired_row"), dict):
            repaired = item["repaired_row"]
            repaired["task_id"] = task_id
            accepted, repair_note = _validated_batch_repair(audits_by_task.get(task_id, {}), repaired)
            repaired_audits[task_id] = accepted
            if repair_note:
                validation_by_task[task_id] = {
                    "status": "invalid_untrusted" if allow_downgrade else "pass",
                    "notes": "; ".join(part for part in [notes, repair_note] if part),
                }
            else:
                validation_by_task[task_id] = {"status": "repaired_pass", "notes": notes or "batch auditor repaired row"}
        else:
            validation_by_task[task_id] = {
                "status": "invalid_untrusted" if allow_downgrade else "pass",
                "notes": notes,
            }

    for task_id, status in deterministic_by_task.items():
        if status.get("status") in {"invalid", "missing_log"}:
            validation_by_task[task_id] = {
                "status": "invalid_untrusted",
                "notes": status.get("notes", ""),
            }
        elif status.get("status") in {"valid", "valid_with_warnings"} and task_id not in validation_by_task:
            validation_by_task[task_id] = {
                "status": "invalid_untrusted" if allow_downgrade else "pass",
                "notes": "batch auditor did not return a verdict for this row",
            }

    return validation_by_task, repaired_audits


def _run_row_jobs(
    *,
    rows_to_run: list[dict[str, str]],
    layout: AuditLayout,
    tmp_root: Path,
    journal_path: Path,
    backend: str,
    model: str,
    reasoning_effort: str,
    timeout: int,
    concurrency: int,
    force: bool,
    repair_notes_by_task: Optional[dict[str, str]] = None,
) -> dict[str, dict[str, Any]]:
    repair_notes_by_task = repair_notes_by_task or {}
    audits_by_task: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {
            pool.submit(
                run_row_audit,
                layout=layout,
                source_row=row,
                tmp_root=tmp_root,
                backend=backend,
                model=model,
                reasoning_effort=reasoning_effort,
                timeout=timeout,
                force=force,
                repair_notes=repair_notes_by_task.get(str(row.get("task_id", "")), ""),
            ): str(row.get("task_id", ""))
            for row in rows_to_run
        }
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                task_id, audit = future.result()
            except Exception as exc:
                _append_journal_record(journal_path, layout=layout, task_id=task_id, status="error", error=str(exc))
                raise
            audits_by_task[task_id] = audit
            _append_journal_record(journal_path, layout=layout, task_id=task_id, status="ok", audit=audit)
            print(f"row audit complete: {task_id}")
    return audits_by_task


def run_audit_file(args: argparse.Namespace) -> dict[str, Any]:
    eval_path = args.eval_path
    selected_stats: PendingEvalStats | None = None
    tmp_root = Path(args.tmp_root).resolve()
    explicit_journal_path = Path(args.journal_path).resolve() if args.journal_path else None
    if eval_path is None:
        eval_path = choose_pending_eval_path(
            repo_root=Path(args.repo_root).resolve(),
            source_root_name=args.source_root,
            tmp_root=tmp_root,
            journal_path=explicit_journal_path,
        )
        selected_stats = eval_pending_stats(eval_path, tmp_root=tmp_root, journal_path=explicit_journal_path)
    layout = infer_layout(eval_path)
    if selected_stats is None:
        selected_stats = eval_pending_stats(layout.eval_path, tmp_root=tmp_root, journal_path=explicit_journal_path)
    journal_path = explicit_journal_path or _default_journal_path(layout)
    rows, _ = _read_source_rows(layout.eval_path)
    eligible_rows = [row for row in rows if is_non_correct_row(row)]
    limited_smoke = args.limit is not None
    if args.limit is not None:
        eligible_rows = eligible_rows[: args.limit]

    print(f"Source eval: {layout.eval_path}")
    print(f"Eligible rows: {len(eligible_rows)}")
    print(f"Temp JSON dir: {_temp_dir_for_layout(tmp_root, layout)}")
    print(f"JSONL journal: {journal_path}")

    audits_by_task: dict[str, dict[str, Any]] = _load_journal_audits(journal_path, layout)
    audits_by_task.update(_load_audits_for_rows(layout, tmp_root, eligible_rows))
    audits_by_task.update(_load_audits_from_mirrored_outputs(layout))
    for task_id, audit in sorted(audits_by_task.items()):
        out_path = _audit_json_path(tmp_root, layout, task_id)
        if not out_path.exists():
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    if audits_by_task:
        print(f"Resumed {len(audits_by_task)} completed row audits from cache")

    selected_pending_ids = set(selected_stats.pending_task_ids)
    rows_to_run = [
        row
        for row in eligible_rows
        if args.force
        or str(row.get("task_id", "")) not in audits_by_task
        or str(row.get("task_id", "")) in selected_pending_ids
    ]
    if args.force:
        audits_by_task = {}

    audits_by_task.update(
        _run_row_jobs(
            rows_to_run=rows_to_run,
            layout=layout,
            tmp_root=tmp_root,
            journal_path=journal_path,
            backend=args.backend,
            model=args.row_model,
            reasoning_effort=args.row_reasoning_effort,
            timeout=args.timeout,
            concurrency=args.concurrency,
            force=args.force,
        )
    )

    if args.limit is None:
        audits_by_task.update(_load_audits_for_rows(layout, tmp_root, rows))

    if limited_smoke:
        return {
            "layout": layout,
            "eligible_rows": len(eligible_rows),
            "initial_invalid_rows": 0,
            "final_invalid_rows": 0,
            "event_count": sum(len(audit.get("events") or []) for audit in audits_by_task.values()),
            "eval_path": layout.mirrored_eval_path,
            "events_path": layout.mirrored_events_path,
            "report_path": layout.mirrored_report_path,
            "smoke_only": True,
            "journal_path": journal_path,
        }

    write_mirrored_outputs(layout, audits_by_task)
    validation_outputs = validate_answer_failure_root(
        source_root=layout.output_root,
        logs_dir=layout.logs_root,
        rewrite=True,
    )
    row_by_task = {str(row.get("task_id", "")): row for row in eligible_rows}
    if selected_stats.invalid_rows:
        print(f"Selected file has invalid_rows={selected_stats.invalid_rows}; repair mode will target those rows.")
    for repair_round in range(1, args.repair_invalid_rounds + 1):
        repair_ids = _task_ids_for_deterministic_repair(validation_outputs)
        if not repair_ids:
            break
        repair_rows = [row_by_task[task_id] for task_id in repair_ids if task_id in row_by_task]
        repair_notes_by_task = {
            str(row.get("task_id", "")): str(row.get(VALIDATION_NOTES_FIELD, ""))
            for row in validation_outputs.get("invalid_rows", [])
        }
        print(f"Repair round {repair_round}: rerunning {len(repair_rows)} deterministic-invalid rows")
        repaired = _run_row_jobs(
            rows_to_run=repair_rows,
            layout=layout,
            tmp_root=tmp_root,
            journal_path=journal_path,
            backend=args.backend,
            model=args.row_model,
            reasoning_effort=args.row_reasoning_effort,
            timeout=args.timeout,
            concurrency=args.concurrency,
            force=True,
            repair_notes_by_task=repair_notes_by_task,
        )
        audits_by_task.update(repaired)
        write_mirrored_outputs(layout, audits_by_task)
        validation_outputs = validate_answer_failure_root(
            source_root=layout.output_root,
            logs_dir=layout.logs_root,
            rewrite=True,
        )
    deterministic_by_task = _deterministic_status_by_task(layout)

    if args.no_batch_auditor:
        model_validation_by_task = {
            task_id: {
                "status": "pass" if status.get("status") in {"valid", "valid_with_warnings"} else "invalid_untrusted",
                "notes": "batch auditor skipped by --no-batch-auditor",
            }
            for task_id, status in deterministic_by_task.items()
            if task_id in audits_by_task
        }
        final_audits = audits_by_task
    else:
        model_validation_by_task, final_audits = run_batch_auditor(
            layout=layout,
            tmp_root=tmp_root,
            audits_by_task=audits_by_task,
            deterministic_by_task=deterministic_by_task,
            backend=args.auditor_backend or args.backend,
            model=args.auditor_model,
            reasoning_effort=args.auditor_reasoning_effort,
            timeout=args.timeout,
            allow_downgrade=args.strict_batch_auditor,
        )

    write_mirrored_outputs(
        layout,
        final_audits,
        model_validation_by_task=model_validation_by_task,
    )
    final_validation_outputs = validate_answer_failure_root(
        source_root=layout.output_root,
        logs_dir=layout.logs_root,
        rewrite=True,
    )
    report_outputs = build_answer_failure_report(
        source_root=layout.output_root,
        events_path=layout.mirrored_events_path,
        logs_dir=layout.logs_root,
    )
    return {
        "layout": layout,
        "eligible_rows": len(eligible_rows),
        "initial_invalid_rows": len(validation_outputs["invalid_rows"]),
        "final_invalid_rows": len(final_validation_outputs["invalid_rows"]),
        "event_count": report_outputs["event_count"],
        "eval_path": layout.mirrored_eval_path,
        "events_path": layout.mirrored_events_path,
        "report_path": layout.mirrored_report_path,
        "journal_path": journal_path,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-path", help="Source semantic eval_results.csv to audit")
    parser.add_argument("--repo-root", default=".", help="Repo root to scan when --eval-path is omitted")
    parser.add_argument(
        "--source-root",
        choices=sorted(SOURCE_ROOTS),
        default="results_semantic",
        help="Semantic results root to scan when --eval-path is omitted",
    )
    parser.add_argument("--backend", choices=["codex", "openai"], default="codex")
    parser.add_argument("--auditor-backend", choices=["codex", "openai"], default=None)
    parser.add_argument("--row-model", default=DEFAULT_ROW_MODEL)
    parser.add_argument("--row-reasoning-effort", default=DEFAULT_ROW_REASONING)
    parser.add_argument("--auditor-model", default=DEFAULT_AUDITOR_MODEL)
    parser.add_argument("--auditor-reasoning-effort", default=DEFAULT_AUDITOR_REASONING)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--tmp-root", default=".tmp_answer_failure_audits")
    parser.add_argument("--journal-path", help="Append/resume row audit JSONL journal; defaults to /tmp/answer_failure_audits_{source_root}_{model}_{mode}.jsonl")
    parser.add_argument("--force", action="store_true", help="Rerun row audits even when temp JSON exists")
    parser.add_argument("--no-batch-auditor", action="store_true", help="Skip final model audit and trust deterministic validation")
    parser.add_argument("--strict-batch-auditor", action="store_true", help="Allow the batch auditor to downgrade deterministic-valid rows to invalid_untrusted")
    parser.add_argument("--repair-invalid-rounds", type=int, default=1, help="Rerun deterministic-invalid rows this many times before model validation")
    parser.add_argument("--limit", type=int, help="Audit only the first N eligible rows and stop before mirrored output writes")
    return parser


def choose_pending_eval_path(
    *,
    repo_root: Path,
    source_root_name: str,
    tmp_root: Optional[str | Path] = None,
    journal_path: Optional[str | Path] = None,
) -> Path:
    pending = find_pending_eval_stats(
        repo_root,
        source_root_name=source_root_name,
        tmp_root=tmp_root,
        journal_path=journal_path,
    )
    if not pending:
        raise SystemExit(f"No pending eval_results.csv files found under {repo_root / source_root_name}/modes")

    print(f"Pending answer-failure files under {repo_root / source_root_name}:")
    for index, stats in enumerate(pending, 1):
        artifact_note = "" if stats.has_all_artifacts else " missing_artifacts=yes"
        print(
            f"{index}. {stats.eval_path.relative_to(repo_root)} "
            f"pending_rows={stats.pending_rows} invalid_rows={stats.invalid_rows}{artifact_note}"
        )

    while True:
        choice = input("Pick a file number: ").strip()
        try:
            selected = int(choice)
        except ValueError:
            print("Enter a number from the list.")
            continue
        if 1 <= selected <= len(pending):
            return pending[selected - 1].eval_path
        print(f"Enter a number between 1 and {len(pending)}.")


def main() -> None:
    args = build_arg_parser().parse_args()
    outputs = run_audit_file(args)
    if outputs.get("smoke_only"):
        print("Smoke run only: skipped mirrored CSV/report writes")
    else:
        print(f"Wrote {outputs['eval_path']}")
        print(f"Wrote {outputs['events_path']}")
        print(f"Wrote {outputs['report_path']}")
    print(f"Eligible rows: {outputs['eligible_rows']}")
    print(f"Event rows: {outputs['event_count']}")
    print(f"Final invalid rows: {outputs['final_invalid_rows']}")
    print(f"JSONL journal: {outputs['journal_path']}")


if __name__ == "__main__":
    main()
