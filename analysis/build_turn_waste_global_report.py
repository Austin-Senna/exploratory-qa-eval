#!/usr/bin/env python3
"""
Build an evidence-bounded turn-waste global report from grouped CSV outputs.

The report intentionally avoids free-form narrative synthesis. It only emits:
  - file and group counts from grouped CSVs
  - subtype breakdown counts from grouped CSVs
  - representative row evidence from `turn_waste_evidence`
  - optional raw-log turn snippets when `--logs-dir` is provided

Default scope matches the grouped outputs used in this repo:
    python analysis/build_turn_waste_global_report.py

Model-scoped report:
    python analysis/build_turn_waste_global_report.py --source-root results_semantic_turn_waste_grouped --model openai_gpt-5-mini
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.turn_waste_validation import (
    VALIDATION_MAX_TURN_FIELD,
    VALIDATION_NOTES_FIELD,
    VALIDATION_STATUS_FIELD,
    row_log_path,
    validate_audit_row,
)
from analysis.combine_turn_waste_grouped_models import reconcile_global_group


TURN_HEADER_RE = re.compile(r"--- Turn (\d+)")
TURN_REF_RE = re.compile(r"\bTurns?\s+(\d+)(?:-(\d+))?")

_SIGNAL_MARKERS = (
    "Executing:",
    "Tool result: Tool call cancelled",
    "Tool limit reached",
    "Timeout reached",
    "MaxTokensReachedException",
)

MODEL_VALIDATION_STATUS_FIELD = "turn_waste_model_validation_status"
MODEL_VALIDATION_NOTES_FIELD = "turn_waste_model_validation_notes"
TRUSTED_MODEL_VALIDATION_STATUSES = {"pass", "repaired_pass"}
GROUP_METADATA = {
    "Answer-Ready Overshoot": {
        "meaning": (
            "The answer path is already mostly established, but the run spends its tail on extra checks, "
            "nearby-source validation, or one more low-yield action instead of submitting."
        ),
        "characteristics": [
            "late verification after the decisive clue is already visible",
            "adjacent-source checking that does not materially change the answer",
            "extra turns after a stop warning, timeout warning, or obvious answer-ready point",
        ],
    },
    "Discovery Drift": {
        "meaning": (
            "The run stays broad and exploratory instead of converging, reopening discovery, replanning, or "
            "rediscovering already-located sources."
        ),
        "characteristics": [
            "repeated source-finding or dataset-orientation work",
            "late replanning, guidance reloads, or problem reframing",
            "broad search churn that never settles into a concrete extraction step",
        ],
    },
    "Constraint and Format Recovery Thrash": {
        "meaning": (
            "File size, schema uncertainty, parsing trouble, or query/tool constraints dominate the wasted tail, "
            "pulling the run into recovery work instead of task logic."
        ),
        "characteristics": [
            "large-file inspection loops or repeated schema peeks",
            "parser or format recovery retries after errors",
            "constraint workarounds that never transition into a clean extraction path",
        ],
    },
    "Duplicate Query Churn": {
        "meaning": (
            "The run stays grounded in the same source or query family, but keeps recomputing near-identical "
            "lookups with little new information."
        ),
        "characteristics": [
            "repeat counts, rankings, or filters on the same source family",
            "minor wording or parameter tweaks without substantive new evidence",
            "recomputation that delays synthesis rather than advancing it",
        ],
    },
    "Mostly On-Path Exhaustion": {
        "meaning": (
            "The run remains largely productive and hits the token, time, or tool budget before a distinct "
            "wasted-tail pattern clearly emerges."
        ),
        "characteristics": [
            "the tail is still doing necessary extraction or synthesis work",
            "estimated wasted turns are zero or small relative to the whole run",
            "no single low-yield loop clearly dominates the ending",
        ],
    },
    "unassigned": {
        "meaning": (
            "The row is preserved in the grouped outputs, but it was not assigned to one of the canonical umbrella "
            "groups in this pass."
        ),
        "characteristics": [
            "missing trusted assignment data for this grouping pass",
            "row kept for comparison in failures tables and file-level outputs",
            "useful as a follow-up bucket for cleanup or reruns",
        ],
    },
    "mixed or unclear": {
        "meaning": "The available evidence supports multiple umbrellas, or no single umbrella clearly dominates.",
        "characteristics": [
            "signals overlap across multiple behavior patterns",
            "the tail contains competing failure modes",
            "useful as a temporary bucket until a stronger taxonomy signal appears",
        ],
    },
}


def _safe_int(value: str | int | float | None) -> Optional[int]:
    if value in ("", None):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _normalize_text(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def _truncate(value: str, limit: int = 220) -> str:
    text = _normalize_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _relative_link(from_dir: Path, target: Path) -> str:
    return os.path.relpath(target, start=from_dir)


def _markdown_link(label: str, from_dir: Path, target: Optional[Path]) -> str:
    if target is None:
        return label
    return f"[{label}]({_relative_link(from_dir, target)})"


def _resolve_task_path(repo_root: Path, task_id: str) -> Optional[Path]:
    task_path = repo_root / Path(task_id)
    if task_path.exists():
        return task_path
    return None


def _resolve_plan_path(repo_root: Path, task_id: str) -> Optional[Path]:
    task_path = Path(task_id)
    if not task_path.parts:
        return None

    plan_roots = {
        "tasks_mini": "plans_mini",
        "tasks_mini_core": "plans_mini_core",
    }
    plan_root = plan_roots.get(task_path.parts[0])
    if plan_root is None:
        return None

    plan_path = repo_root / plan_root / Path(*task_path.parts[1:])
    if plan_path.exists():
        return plan_path
    return None


def _parse_turn_refs(evidence_text: str) -> list[int]:
    turns: list[int] = []
    for match in TURN_REF_RE.finditer(evidence_text or ""):
        start = int(match.group(1))
        end = int(match.group(2) or start)
        if end < start:
            start, end = end, start
        for turn in range(start, min(end, start + 2) + 1):
            if turn not in turns:
                turns.append(turn)
    return turns


def _extract_turn_highlights(log_path: Path) -> dict[int, list[str]]:
    highlights: dict[int, list[str]] = defaultdict(list)
    current_turn: Optional[int] = None
    with log_path.open() as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            turn_match = TURN_HEADER_RE.search(line)
            if turn_match:
                current_turn = int(turn_match.group(1))
                continue
            if current_turn is None:
                continue
            if not any(marker in line for marker in _SIGNAL_MARKERS):
                continue
            # Strip timestamp/log prefix if present.
            parts = line.split(" | ", 4)
            message = parts[-1] if len(parts) >= 5 else line.strip()
            highlights[current_turn].append(_normalize_text(message))
    return highlights


def _validated_log_snippets(log_path: Path, evidence_text: str, max_turns: int = 2) -> list[str]:
    if not log_path.exists():
        return []
    turn_refs = _parse_turn_refs(evidence_text)
    if not turn_refs:
        return []
    highlights = _extract_turn_highlights(log_path)
    snippets: list[str] = []
    for turn in turn_refs[:max_turns]:
        messages = highlights.get(turn, [])
        if not messages:
            continue
        snippets.append(f"Turn {turn}: {_truncate(messages[0], 180)}")
    return snippets


def _repo_root_from_source_root(source_root: Path) -> Path:
    for candidate in [source_root, *source_root.parents]:
        if (candidate / ".git").exists() or (candidate / "tasks_mini").exists():
            return candidate
    return source_root.parent


def _variants_from_grouped_path(source_root: Path, failures_path: Path) -> tuple[str, str] | None:
    rel_path = failures_path.relative_to(source_root)
    parts = rel_path.parts
    if "modes" in parts:
        modes_index = parts.index("modes")
        after_modes = parts[modes_index + 1 :]
        if len(after_modes) >= 3:
            return after_modes[0], after_modes[1]
        if len(after_modes) >= 2 and modes_index >= 1:
            return parts[modes_index - 1], after_modes[0]
    if len(parts) >= 4:
        return parts[-3], parts[-2]
    return None


def _parse_grouped_failures(source_root: Path, *, model_filter: str | None = None) -> tuple[list[dict], list[dict]]:
    file_summaries: list[dict] = []
    rows: list[dict] = []
    for failures_path in sorted(source_root.rglob("turn_waste_global_failures.csv")):
        variants = _variants_from_grouped_path(source_root, failures_path)
        if variants is None:
            continue
        model_variant, mode_variant = variants
        if model_filter and model_variant != model_filter:
            continue
        eval_path = failures_path.parent / "eval_results.csv"

        with failures_path.open() as handle:
            file_rows = list(csv.DictReader(handle))

        file_summaries.append(
            {
                "model_variant": model_variant,
                "mode_variant": mode_variant,
                "eval_path": eval_path,
                "failures_path": failures_path,
                "row_count": len(file_rows),
            }
        )

        for row in file_rows:
            enriched = dict(row)
            enriched["model_variant"] = model_variant
            enriched["mode_variant"] = mode_variant
            enriched["eval_path"] = eval_path
            enriched["failures_path"] = failures_path
            enriched["estimated_wasted_turns_int"] = _safe_int(row.get("estimated_wasted_turns"))
            rows.append(enriched)
    return file_summaries, rows


def _group_sort_key(item: tuple[str, list[dict]]) -> tuple[int, str]:
    group_name, rows = item
    return (-len(rows), group_name)


def _representative_rows(rows: Iterable[dict], limit: int = 5) -> list[dict]:
    return sorted(
        rows,
        key=lambda row: (
            -(row.get("estimated_wasted_turns_int") or -1),
            str(row.get("task_id", "")),
            str(row.get("mode_variant", "")),
        ),
    )[:limit]


def _group_explanation_lines(group_name: str) -> list[str]:
    metadata = GROUP_METADATA.get(group_name)
    if metadata is None:
        return []
    characteristics = "; ".join(metadata["characteristics"])
    return [
        f"- Meaning: {metadata['meaning']}",
        f"- Characteristics: {characteristics}",
    ]


def _model_counts_text(counter: Counter[str]) -> str:
    return "; ".join(f"{model}: {count}" for model, count in sorted(counter.items()))


def _add_table(lines: list[str], headers: list[str], table_rows: list[list[str]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in table_rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    lines.append("")


def _count_by_key(rows: list[dict], key_fn) -> list[tuple[tuple[str, ...], int, Counter[str]]]:
    counts: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for row in rows:
        counts[key_fn(row)][str(row.get("model_variant", ""))] += 1
    return sorted(
        ((key, sum(model_counts.values()), model_counts) for key, model_counts in counts.items()),
        key=lambda item: (-item[1], item[0]),
    )


def _representative_link_cell(
    row: dict,
    *,
    report_dir: Path,
    repo_root: Path,
    logs_root: Optional[Path],
) -> str:
    task_id = str(row.get("task_id", ""))
    task_path = _resolve_task_path(repo_root, task_id)
    plan_path = _resolve_plan_path(repo_root, task_id)
    log_path = None
    if logs_root is not None:
        candidate = row_log_path(logs_root, str(row.get("model_variant", "")), str(row.get("mode_variant", "")), task_id)
        log_path = candidate if candidate.exists() else None

    return " / ".join(
        [
            _markdown_link("task", report_dir, task_path),
            _markdown_link("plan", report_dir, plan_path),
            _markdown_link("log", report_dir, log_path),
        ]
    )


def _representative_by_key(rows: list[dict], key_fn) -> dict[tuple[str, ...], dict]:
    grouped: dict[tuple[str, ...], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[key_fn(row)].append(row)
    return {key: _representative_rows(key_rows, limit=1)[0] for key, key_rows in grouped.items()}


def _add_summary_tables(
    lines: list[str],
    rows: list[dict],
    *,
    report_dir: Path,
    repo_root: Path,
    logs_root: Optional[Path],
) -> None:
    lines.extend(["## Counts by Reconciled Global Group", ""])
    group_rows = _count_by_key(
        rows,
        lambda row: (reconcile_global_group(str(row.get("turn_waste_global_group", ""))),),
    )
    _add_table(
        lines,
        ["Reconciled Global Group", "Errors", "Errors by Model"],
        [[key[0], str(total), _model_counts_text(model_counts)] for key, total, model_counts in group_rows],
    )

    lines.extend(["## Counts by Reconciled Global Group and Subtype", ""])
    reconciled_subtype_key = lambda row: (
        reconcile_global_group(str(row.get("turn_waste_global_group", ""))),
        _normalize_text(str(row.get("turn_waste_global_subtype", ""))) or "(none)",
    )
    subtype_rows = _count_by_key(
        rows,
        reconciled_subtype_key,
    )
    subtype_representatives = _representative_by_key(rows, reconciled_subtype_key)
    _add_table(
        lines,
        ["Global Group", "Subtype", "Errors", "Errors by Model", "Representative"],
        [
            [
                key[0],
                key[1],
                str(total),
                _model_counts_text(model_counts),
                _representative_link_cell(
                    subtype_representatives[key],
                    report_dir=report_dir,
                    repo_root=repo_root,
                    logs_root=logs_root,
                ),
            ]
            for key, total, model_counts in subtype_rows
        ],
    )

    lines.extend(["## Counts by Original Global Group and Subtype", ""])
    original_subtype_key = lambda row: (
        _normalize_text(str(row.get("turn_waste_global_group", ""))) or "unassigned",
        _normalize_text(str(row.get("turn_waste_global_subtype", ""))) or "(none)",
    )
    original_subtype_rows = _count_by_key(
        rows,
        original_subtype_key,
    )
    original_subtype_representatives = _representative_by_key(rows, original_subtype_key)
    _add_table(
        lines,
        ["Original Global Group", "Subtype", "Errors", "Errors by Model", "Representative"],
        [
            [
                key[0],
                key[1],
                str(total),
                _model_counts_text(model_counts),
                _representative_link_cell(
                    original_subtype_representatives[key],
                    report_dir=report_dir,
                    repo_root=repo_root,
                    logs_root=logs_root,
                ),
            ]
            for key, total, model_counts in original_subtype_rows
        ],
    )


def build_turn_waste_global_report(
    source_root: str | Path = "results-ec2_semantic_turn_waste_grouped",
    *,
    output_path: str | Path | None = None,
    logs_dir: str | Path | None = None,
    model: str | None = None,
    representative_limit: int = 5,
) -> dict:
    source_root = Path(source_root)
    if output_path:
        report_path = Path(output_path)
    elif model and source_root.name != model:
        report_path = source_root / model / "turn_waste_global_report.md"
    else:
        report_path = source_root / "turn_waste_global_report.md"
    logs_root = Path(logs_dir) if logs_dir else None
    repo_root = _repo_root_from_source_root(source_root)

    file_summaries, rows = _parse_grouped_failures(source_root, model_filter=model)
    grouped_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        group_name = _normalize_text(str(row.get("turn_waste_global_group", ""))) or "unassigned"
        grouped_rows[group_name].append(row)

    lines = [
        "# Turn Waste Global Report",
        "",
        "## Scope",
        "",
        f"- Source root: `{source_root}`",
        f"- Output root: `{source_root}`",
        f"- Model filter: `{model}`" if model else "- Model filter: all models",
        f"- Processed files: {len(file_summaries)}",
        f"- Total grouped runtime-failure rows: {len(rows)}",
        (
            f"- Evidence mode: row `turn_waste_evidence` plus raw-log turn validation from `{logs_root}`"
            if logs_root
            else "- Evidence mode: row `turn_waste_evidence` only"
        ),
        "",
        "## File Counts",
        "",
    ]

    for summary in file_summaries:
        eval_link = _markdown_link(str(summary["eval_path"].relative_to(source_root)), report_path.parent, summary["eval_path"])
        failures_link = _markdown_link(
            summary["failures_path"].name,
            report_path.parent,
            summary["failures_path"],
        )
        lines.append(
            f"- {eval_link}: {summary['row_count']} grouped runtime-failure rows; failures table: {failures_link}"
        )

    lines.append("")
    _add_summary_tables(lines, rows, report_dir=report_path.parent, repo_root=repo_root, logs_root=logs_root)

    lines.extend(
        [
            "## Canonical Groups",
            "",
            "_Narrative claims below are limited to grouped counts, direct `turn_waste_evidence`, and optional validated log snippets._",
            "",
        ]
    )

    for group_name, group_rows in sorted(grouped_rows.items(), key=_group_sort_key):
        lines.append(f"### {group_name}")
        lines.append("")
        lines.extend(_group_explanation_lines(group_name))
        lines.append(f"- Count: {len(group_rows)}")
        subtype_counts = Counter(
            _normalize_text(str(row.get("turn_waste_global_subtype", "")))
            for row in group_rows
            if _normalize_text(str(row.get("turn_waste_global_subtype", "")))
        )
        if subtype_counts:
            subtype_text = "; ".join(
                f"{name} ({count})" for name, count in sorted(subtype_counts.items(), key=lambda item: (-item[1], item[0]))
            )
            lines.append(f"- Subtypes: {subtype_text}")
        else:
            lines.append("- Subtypes: none")
        lines.append("- Representative evidence-backed rows:")

        for row in _representative_rows(group_rows, limit=representative_limit):
            task_id = str(row.get("task_id", ""))
            task_path = _resolve_task_path(repo_root, task_id)
            plan_path = _resolve_plan_path(repo_root, task_id)
            log_path = None
            validation_result = None
            if logs_root is not None:
                log_path = row_log_path(logs_root, row["model_variant"], row["mode_variant"], task_id)
                if not log_path.exists():
                    log_path = None
                validation_result = validate_audit_row(row, log_path)

            row_links: list[str] = []
            if task_path is not None:
                row_links.append(_markdown_link("task", report_path.parent, task_path))
            if plan_path is not None:
                row_links.append(_markdown_link("plan", report_path.parent, plan_path))
            if log_path is not None:
                row_links.append(_markdown_link("log", report_path.parent, log_path))

            row_prefix = f"{' | '.join(row_links)} | " if row_links else ""
            wasted = row.get("estimated_wasted_turns_int")
            wasted_text = f" (estimated wasted turns: {wasted})" if wasted is not None else ""
            lines.append(f"  - {row_prefix}`{task_id}` @ `{row['mode_variant']}`{wasted_text}")

            recorded_status = _normalize_text(str(row.get(VALIDATION_STATUS_FIELD, "")))
            recorded_notes = _normalize_text(str(row.get(VALIDATION_NOTES_FIELD, "")))
            recorded_max_turn = _normalize_text(str(row.get(VALIDATION_MAX_TURN_FIELD, "")))
            effective_status = recorded_status or (validation_result or {}).get("status", "")
            effective_notes = recorded_notes or _normalize_text((validation_result or {}).get("notes", ""))
            effective_max_turn = recorded_max_turn or str((validation_result or {}).get("log_max_turn", "") or "")

            model_status = _normalize_text(str(row.get(MODEL_VALIDATION_STATUS_FIELD, ""))).lower()
            model_notes = _normalize_text(str(row.get(MODEL_VALIDATION_NOTES_FIELD, "")))

            if model_status and model_status not in TRUSTED_MODEL_VALIDATION_STATUSES:
                lines.append(
                    f"    Evidence: omitted due to failed model validation: {_truncate(model_notes or model_status, 240)}"
                )
            elif effective_status == "invalid":
                suffix = f" (log max turn {effective_max_turn})" if effective_max_turn else ""
                lines.append(
                    f"    Evidence: omitted due to failed row validation{suffix}: {_truncate(effective_notes or 'invalid evidence', 240)}"
                )
            elif effective_status == "missing_log":
                lines.append("    Evidence: omitted because the matching raw log is missing")
            else:
                evidence_text = _truncate(str(row.get("turn_waste_evidence", "")) or "No `turn_waste_evidence` provided.", 240)
                lines.append(f"    Evidence: {evidence_text}")
                if effective_status == "valid_with_warnings" and effective_notes:
                    lines.append(f"    Validation: {_truncate(effective_notes, 240)}")

            if log_path is not None:
                snippets = _validated_log_snippets(log_path, str(row.get("turn_waste_evidence", "")))
                if snippets:
                    lines.append(f"    Log check: {'; '.join(snippets)}")
        lines.append("")

    mixed_rows = grouped_rows.get("mixed or unclear", []) + grouped_rows.get("unassigned", [])
    lines.extend(
        [
            "## Notes",
            "",
            "- This report does not restate `turn_waste_summary`, `turn_repeated_behavior`, or group reasons as fact.",
            "- Stronger row-level claims should come from `turn_waste_evidence` or from rerunning with `--logs-dir` for validated turn snippets.",
            "- When present, model-validation statuses other than `pass` or `repaired_pass` suppress row evidence in this report.",
            f"- Mixed or unresolved rows visible here: {len(mixed_rows)}",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n")
    return {
        "report_path": report_path,
        "row_count": len(rows),
        "file_count": len(file_summaries),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", default="results-ec2_semantic_turn_waste_grouped")
    parser.add_argument("--output-path", default=None)
    parser.add_argument("--logs-dir", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--representative-limit", type=int, default=5)
    args = parser.parse_args()

    outputs = build_turn_waste_global_report(
        source_root=args.source_root,
        output_path=args.output_path,
        logs_dir=args.logs_dir,
        model=args.model,
        representative_limit=args.representative_limit,
    )
    print(f"Wrote {outputs['report_path']}")


if __name__ == "__main__":
    main()
