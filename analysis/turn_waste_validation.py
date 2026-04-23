#!/usr/bin/env python3
"""
Validation helpers for row-level turn-waste audits.

These checks are intentionally conservative. They do not try to prove that a
summary is correct; they only reject rows that are clearly inconsistent with
the raw log structure.
"""
from __future__ import annotations

import csv
import os
import re
from pathlib import Path
from typing import Optional


TURN_HEADER_RE = re.compile(r"--- Turn (\d+)")
TURN_REF_RE = re.compile(r"\bTurns?\s+(\d+)(?:-(\d+))?")
EXACT_EVIDENCE_RE = re.compile(r"\bTurn\s+(\d+)\s*[:|]\s*(.+)")

AUDITED_FIELDS = (
    "turn_waste_summary",
    "turn_repeated_behavior",
    "turn_progress_stop_point",
    "turn_waste_evidence",
    "productive_turn_ranges",
    "wasted_turn_ranges",
    "estimated_wasted_turns",
)

VALIDATION_STATUS_FIELD = "turn_waste_validation_status"
VALIDATION_NOTES_FIELD = "turn_waste_validation_notes"
VALIDATION_MAX_TURN_FIELD = "turn_waste_log_max_turn"

_EXACT_SNIPPET_PREFIXES = (
    "Executing:",
    "Tool result:",
    "WARNING",
    "ERROR",
    "[Stagnation]",
)


def _normalize_text(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def _safe_int(value: str | int | float | None) -> Optional[int]:
    if value in ("", None):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def is_audited_row(row: dict) -> bool:
    return any(_normalize_text(str(row.get(field, ""))) for field in AUDITED_FIELDS)


def parse_turn_refs(text: str | None) -> list[int]:
    turns: list[int] = []
    for match in TURN_REF_RE.finditer(text or ""):
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if end < start:
            start, end = end, start
        for turn in range(start, end + 1):
            if turn not in turns:
                turns.append(turn)
    return turns


def expand_turn_ranges(ranges_text: str | None) -> tuple[set[int], list[str]]:
    turns: set[int] = set()
    issues: list[str] = []
    normalized = _normalize_text(ranges_text)
    if not normalized:
        return turns, issues

    for token in [part.strip() for part in normalized.split(";") if part.strip()]:
        if "-" in token:
            left, right = token.split("-", 1)
            try:
                start = int(left)
                end = int(right)
            except ValueError:
                issues.append(f"invalid range token `{token}`")
                continue
            if start <= 0 or end <= 0:
                issues.append(f"non-positive range `{token}`")
                continue
            if end < start:
                start, end = end, start
            turns.update(range(start, end + 1))
        else:
            try:
                turn = int(token)
            except ValueError:
                issues.append(f"invalid turn token `{token}`")
                continue
            if turn <= 0:
                issues.append(f"non-positive turn `{token}`")
                continue
            turns.add(turn)
    return turns, issues


def parse_log_turn_blocks(log_path: Path) -> tuple[int, dict[int, str]]:
    max_turn = 0
    blocks: dict[int, list[str]] = {}
    current_turn: Optional[int] = None

    with log_path.open() as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            turn_match = TURN_HEADER_RE.search(line)
            if turn_match:
                current_turn = int(turn_match.group(1))
                max_turn = max(max_turn, current_turn)
                blocks.setdefault(current_turn, [])
                continue
            if current_turn is None:
                continue
            parts = line.split(" | ", 4)
            message = parts[-1] if len(parts) >= 5 else line.strip()
            if message:
                blocks[current_turn].append(_normalize_text(message))

    return max_turn, {turn: " ".join(lines) for turn, lines in blocks.items()}


def validate_audit_row(row: dict, log_path: Path | None) -> dict:
    if not is_audited_row(row):
        return {
            "status": "not_audited",
            "notes": "",
            "log_max_turn": "",
            "issues": [],
            "warnings": [],
        }

    if log_path is None or not log_path.exists():
        return {
            "status": "missing_log",
            "notes": "matching raw log is missing",
            "log_max_turn": "",
            "issues": ["matching raw log is missing"],
            "warnings": [],
        }

    log_max_turn, turn_blocks = parse_log_turn_blocks(log_path)
    issues: list[str] = []
    warnings: list[str] = []

    productive_turns, productive_issues = expand_turn_ranges(row.get("productive_turn_ranges"))
    wasted_turns, wasted_issues = expand_turn_ranges(row.get("wasted_turn_ranges"))
    issues.extend(productive_issues)
    issues.extend(wasted_issues)

    if productive_turns and max(productive_turns) > log_max_turn:
        issues.append(
            f"productive_turn_ranges exceeds log max turn {log_max_turn}"
        )
    if wasted_turns and max(wasted_turns) > log_max_turn:
        issues.append(
            f"wasted_turn_ranges exceeds log max turn {log_max_turn}"
        )
    if productive_turns & wasted_turns:
        overlap = sorted(productive_turns & wasted_turns)
        issues.append(
            f"productive and wasted ranges overlap at turns {','.join(str(turn) for turn in overlap[:5])}"
        )

    for field in ("turn_waste_evidence", "turn_progress_stop_point"):
        refs = parse_turn_refs(str(row.get(field, "")))
        if refs and max(refs) > log_max_turn:
            issues.append(f"{field} references turns beyond log max turn {log_max_turn}")

    estimated_wasted_turns = _safe_int(row.get("estimated_wasted_turns"))
    if estimated_wasted_turns is not None and wasted_turns and estimated_wasted_turns != len(wasted_turns):
        warnings.append(
            f"estimated_wasted_turns={estimated_wasted_turns} but wasted_turn_ranges covers {len(wasted_turns)} turns"
        )

    for entry in str(row.get("turn_waste_evidence", "")).split(";"):
        match = EXACT_EVIDENCE_RE.search(entry.strip())
        if not match:
            continue
        snippet = _normalize_text(match.group(2))
        if not snippet.startswith(_EXACT_SNIPPET_PREFIXES):
            continue
        turn = int(match.group(1))
        if turn > log_max_turn:
            continue
        block_text = turn_blocks.get(turn, "")
        if snippet and snippet not in block_text:
            issues.append(f"exact evidence snippet for turn {turn} does not match the raw log")

    status = "valid"
    if issues:
        status = "invalid"
    elif warnings:
        status = "valid_with_warnings"

    notes = "; ".join(issues + warnings)
    return {
        "status": status,
        "notes": notes,
        "log_max_turn": log_max_turn,
        "issues": issues,
        "warnings": warnings,
    }


def row_log_path(logs_root: Path, model_variant: str, mode_variant: str, task_id: str) -> Path:
    task_path = Path(task_id)
    return logs_root / model_variant / mode_variant / task_path.parent.name / f"{task_path.stem}.log"


def validate_turn_waste_root(
    source_root: str | Path = "results-ec2_semantic_turn_waste",
    *,
    logs_dir: str | Path = "logs-ec2/modes",
    rewrite: bool = False,
) -> dict:
    source_root = Path(source_root)
    logs_root = Path(logs_dir)
    audited_rows = 0
    invalid_rows: list[dict] = []
    file_rows: list[tuple[Path, list[dict], list[str]]] = []

    for eval_path in sorted(source_root.rglob("eval_results.csv")):
        rel_path = eval_path.relative_to(source_root)
        if len(rel_path.parts) < 4:
            continue
        model_variant = rel_path.parts[-3]
        mode_variant = rel_path.parts[-2]

        with eval_path.open() as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = list(reader.fieldnames or [])

        for required in (VALIDATION_STATUS_FIELD, VALIDATION_NOTES_FIELD, VALIDATION_MAX_TURN_FIELD):
            if required not in fieldnames:
                fieldnames.append(required)

        for row in rows:
            if not is_audited_row(row):
                row[VALIDATION_STATUS_FIELD] = "not_audited"
                row[VALIDATION_NOTES_FIELD] = ""
                row[VALIDATION_MAX_TURN_FIELD] = ""
                continue

            audited_rows += 1
            log_path = row_log_path(logs_root, model_variant, mode_variant, str(row.get("task_id", "")))
            result = validate_audit_row(row, log_path)
            row[VALIDATION_STATUS_FIELD] = result["status"]
            row[VALIDATION_NOTES_FIELD] = result["notes"]
            row[VALIDATION_MAX_TURN_FIELD] = result["log_max_turn"]
            if result["status"] in {"invalid", "missing_log"}:
                invalid_rows.append(
                    {
                        "model_variant": model_variant,
                        "mode_variant": mode_variant,
                        "task_id": row.get("task_id", ""),
                        VALIDATION_STATUS_FIELD: result["status"],
                        VALIDATION_NOTES_FIELD: result["notes"],
                        VALIDATION_MAX_TURN_FIELD: result["log_max_turn"],
                        "turn_waste_summary": row.get("turn_waste_summary", ""),
                        "turn_waste_evidence": row.get("turn_waste_evidence", ""),
                        "productive_turn_ranges": row.get("productive_turn_ranges", ""),
                        "wasted_turn_ranges": row.get("wasted_turn_ranges", ""),
                    }
                )

        file_rows.append((eval_path, rows, fieldnames))

    if rewrite:
        for eval_path, rows, fieldnames in file_rows:
            with eval_path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            failures_path = eval_path.parent / "turn_waste_failures.csv"
            if not failures_path.exists():
                continue
            with failures_path.open() as handle:
                reader = csv.DictReader(handle)
                failure_rows = list(reader)
                failure_fieldnames = list(reader.fieldnames or [])
            for required in (VALIDATION_STATUS_FIELD, VALIDATION_NOTES_FIELD, VALIDATION_MAX_TURN_FIELD):
                if required not in failure_fieldnames:
                    failure_fieldnames.append(required)
            failure_index = {str(row.get("task_id", "")): row for row in rows}
            for failure_row in failure_rows:
                source_row = failure_index.get(str(failure_row.get("task_id", "")))
                if source_row is None:
                    continue
                for required in (VALIDATION_STATUS_FIELD, VALIDATION_NOTES_FIELD, VALIDATION_MAX_TURN_FIELD):
                    failure_row[required] = source_row.get(required, "")
            with failures_path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=failure_fieldnames)
                writer.writeheader()
                writer.writerows(failure_rows)

    failures_path = source_root / "turn_waste_validation_failures.csv"
    report_path = source_root / "turn_waste_validation_report.md"

    fieldnames = [
        "model_variant",
        "mode_variant",
        "task_id",
        VALIDATION_STATUS_FIELD,
        VALIDATION_NOTES_FIELD,
        VALIDATION_MAX_TURN_FIELD,
        "turn_waste_summary",
        "turn_waste_evidence",
        "productive_turn_ranges",
        "wasted_turn_ranges",
    ]
    with failures_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(invalid_rows)

    status_counts: dict[str, int] = {}
    for _, rows, _ in file_rows:
        for row in rows:
            status = str(row.get(VALIDATION_STATUS_FIELD, "") or "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

    lines = [
        "# Turn Waste Validation Report",
        "",
        f"- Source root: `{source_root}`",
        f"- Logs root: `{logs_root}`",
        f"- Audited rows checked: {audited_rows}",
        f"- Invalid or missing-log rows: {len(invalid_rows)}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")

    if invalid_rows:
        lines.extend(["", "## Invalid Rows", ""])
        for row in invalid_rows[:20]:
            lines.append(
                f"- `{row['task_id']}` in `{row['model_variant']}/{row['mode_variant']}`: "
                f"{row[VALIDATION_STATUS_FIELD]} - {row[VALIDATION_NOTES_FIELD]}"
            )

    report_path.write_text("\n".join(lines) + "\n")
    return {
        "audited_rows": audited_rows,
        "invalid_rows": invalid_rows,
        "failures_path": failures_path,
        "report_path": report_path,
    }
