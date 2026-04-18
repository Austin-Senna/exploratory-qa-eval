#!/usr/bin/env python3
"""Classify eval rows with semantic matching plus log-tail exhaustion rules."""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path


LABEL_EQUIVALENT = "Equivalent"
LABEL_WRONG = "Wrong Answer"
LABEL_ERROR_TURNS = "Error-Turns exhausted"
LABEL_ERROR_CONTEXT = "Error-Context exhausted"
LABEL_INFRA_EVENT_LOOP = "Infra-EventLoopException"
LABEL_INFRA_OTHER = "Infra-Other"
LABEL_UNCLASSIFIED = "Unclassified"

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="results-ec2")
    parser.add_argument("--logs", default="logs-ec2")
    parser.add_argument("--output-dir", default="analysis_results/semantic_outcomes")
    parser.add_argument("--tail-lines", type=int, default=30)
    parser.add_argument("--mode-filter", default="")
    return parser.parse_args()


def as_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def strip_outer_brackets(text: str) -> str:
    value = str(text or "").strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1].strip()
    return value


def normalize_fragment(text: str) -> str:
    value = strip_outer_brackets(text)
    value = unicodedata.normalize("NFKD", value)
    value = value.lower()
    value = re.sub(r"\bu\.?\s*s\.?\b", " united states ", value)
    value = re.sub(r"[^\w\s,/]", " ", value)
    value = " ".join(value.split())
    return value


def split_answer_items(text: str) -> list[str]:
    value = normalize_fragment(text)
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def canonical_item(text: str) -> str:
    tokens = normalize_fragment(text).split()
    while len(tokens) >= 2 and tokens[:2] == ["united", "states"]:
        tokens = tokens[2:]
    if tokens and tokens[-1] == "county":
        tokens = tokens[:-1]
    return " ".join(tokens)


def person_name_match(expected: str, predicted: str) -> bool:
    expected_tokens = canonical_item(expected).split()
    predicted_tokens = canonical_item(predicted).split()
    if not expected_tokens or not predicted_tokens:
        return False
    if expected_tokens[-1] != predicted_tokens[-1]:
        return False
    if len(expected_tokens) != len(predicted_tokens):
        return False

    for left, right in zip(expected_tokens[:-1], predicted_tokens[:-1]):
        if left == right:
            continue
        if len(left) == 1 and right.startswith(left):
            continue
        if len(right) == 1 and left.startswith(right):
            continue
        return False

    return True


def semantic_equivalent(expected: str, predicted: str) -> tuple[bool, str]:
    expected_items = split_answer_items(expected)
    predicted_items = split_answer_items(predicted)

    if not expected_items or not predicted_items:
        return False, ""

    if len(expected_items) == 1 and len(predicted_items) == 1:
        expected_canonical = canonical_item(expected_items[0])
        predicted_canonical = canonical_item(predicted_items[0])
        if expected_canonical == predicted_canonical:
            return True, "canonical_single_match"
        if person_name_match(expected_items[0], predicted_items[0]):
            return True, "person_name_match"
        return False, ""

    expected_canonical = sorted(canonical_item(item) for item in expected_items)
    predicted_canonical = sorted(canonical_item(item) for item in predicted_items)
    if expected_canonical == predicted_canonical:
        return True, "canonical_list_match"
    return False, ""


def semantic_record(expected: str, predicted: str, lexical_exact_match: float) -> tuple[float, str]:
    if lexical_exact_match >= 1.0:
        return 1.0, "lexical_exact_match"

    matched, reason = semantic_equivalent(expected, predicted)
    return (1.0 if matched else 0.0), reason


def relative_task_path(task_id: str) -> Path:
    task_path = Path(str(task_id))
    parts = list(task_path.parts)
    if parts and parts[0].startswith("tasks"):
        parts = parts[1:]
    rel = Path(*parts) if parts else task_path
    return rel.with_suffix(".log")


def task_log_path(logs_root: Path, model: str, mode: str, task_id: str) -> Path:
    return logs_root / "modes" / model / mode / relative_task_path(task_id)


def read_tail(path: Path, tail_lines: int) -> list[str]:
    if not path.exists():
        return []
    with path.open(errors="ignore") as handle:
        lines = handle.readlines()
    return [line.rstrip("\n") for line in lines[-tail_lines:]]


def latest_marker(text: str, markers: list[str]) -> tuple[int, str]:
    lowered = text.lower()
    latest_pos = -1
    latest_marker_text = ""
    for marker in markers:
        pos = lowered.rfind(marker.lower())
        if pos > latest_pos:
            latest_pos = pos
            latest_marker_text = marker
    return latest_pos, latest_marker_text


def classify_row(
    row: dict,
    model: str,
    mode: str,
    logs_root: Path,
    tail_lines: int,
) -> dict:
    task_id = row.get("task_id", "")
    expected = row.get("expected_answer", "")
    predicted = row.get("predicted_answer", "")
    lexical_exact_match = as_float(row.get("exact_match"))
    semantic_match, semantic_reason = semantic_record(expected, predicted, lexical_exact_match)

    log_path = task_log_path(logs_root, model, mode, task_id)
    tail = read_tail(log_path, tail_lines)
    tail_text = "\n".join(tail)

    submit_pos, submit_marker = latest_marker(tail_text, SUBMIT_MARKERS)
    turns_pos, turns_marker = latest_marker(tail_text, TURNS_MARKERS)
    context_pos, context_marker = latest_marker(tail_text, CONTEXT_MARKERS)

    error_text = str(row.get("error", "") or "")

    if context_pos >= 0:
        label = LABEL_ERROR_CONTEXT
        label_reason = f"log_tail:{context_marker}"
    elif turns_pos >= 0:
        label = LABEL_ERROR_TURNS
        label_reason = f"log_tail:{turns_marker}"
    elif submit_pos >= 0:
        label = LABEL_EQUIVALENT if semantic_match >= 1.0 else LABEL_WRONG
        label_reason = f"log_tail:{submit_marker}"
    elif error_text.startswith("EventLoopException"):
        label = LABEL_INFRA_EVENT_LOOP
        label_reason = "error_field:EventLoopException"
    elif "MaxTokensReachedException" in error_text or "max_tokens limit" in error_text:
        label = LABEL_ERROR_CONTEXT
        label_reason = "error_field:MaxTokensReachedException"
    elif any(marker in error_text for marker in TURNS_MARKERS):
        label = LABEL_ERROR_TURNS
        label_reason = "error_field:turns_exhausted"
    elif error_text:
        label = LABEL_INFRA_OTHER
        label_reason = f"error_field:{error_text.split(':', 1)[0]}"
    elif predicted:
        label = LABEL_EQUIVALENT if semantic_match >= 1.0 else LABEL_WRONG
        label_reason = "fallback:predicted_answer_present"
    else:
        label = LABEL_UNCLASSIFIED
        label_reason = "no_tail_marker_or_error"

    return {
        "model": model,
        "mode": mode,
        "model_mode": f"{model}/{mode}",
        "task_id": task_id,
        "expected_answer": expected,
        "predicted_answer": predicted,
        "lexical_exact_match": lexical_exact_match,
        "semantic_equivalent": semantic_match,
        "semantic_match_reason": semantic_reason,
        "label": label,
        "label_reason": label_reason,
        "tail_has_submit_marker": int(submit_pos >= 0),
        "tail_has_turns_marker": int(turns_pos >= 0),
        "tail_has_context_marker": int(context_pos >= 0),
        "tail_submit_marker": submit_marker,
        "tail_turns_marker": turns_marker,
        "tail_context_marker": context_marker,
        "error": error_text,
        "log_path": str(log_path),
    }


def write_task_rows(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "model",
        "mode",
        "model_mode",
        "task_id",
        "expected_answer",
        "predicted_answer",
        "lexical_exact_match",
        "semantic_equivalent",
        "semantic_match_reason",
        "label",
        "label_reason",
        "tail_has_submit_marker",
        "tail_has_turns_marker",
        "tail_has_context_marker",
        "tail_submit_marker",
        "tail_turns_marker",
        "tail_context_marker",
        "error",
        "log_path",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_summary(path: Path, rows: list[dict]) -> None:
    summary_rows: list[dict] = []
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["model_mode"], []).append(row)

    for model_mode in sorted(grouped):
        mode_rows = grouped[model_mode]
        counts = Counter(row["label"] for row in mode_rows)
        summary_rows.append(
            {
                "model": mode_rows[0]["model"],
                "mode": mode_rows[0]["mode"],
                "model_mode": model_mode,
                "task_count": len(mode_rows),
                "lexical_exact_matches": int(sum(row["lexical_exact_match"] for row in mode_rows)),
                "semantic_equivalents": int(sum(row["semantic_equivalent"] for row in mode_rows)),
                LABEL_EQUIVALENT: counts.get(LABEL_EQUIVALENT, 0),
                LABEL_WRONG: counts.get(LABEL_WRONG, 0),
                LABEL_ERROR_TURNS: counts.get(LABEL_ERROR_TURNS, 0),
                LABEL_ERROR_CONTEXT: counts.get(LABEL_ERROR_CONTEXT, 0),
                LABEL_INFRA_EVENT_LOOP: counts.get(LABEL_INFRA_EVENT_LOOP, 0),
                LABEL_INFRA_OTHER: counts.get(LABEL_INFRA_OTHER, 0),
                LABEL_UNCLASSIFIED: counts.get(LABEL_UNCLASSIFIED, 0),
            }
        )

    fieldnames = [
        "model",
        "mode",
        "model_mode",
        "task_count",
        "lexical_exact_matches",
        "semantic_equivalents",
        LABEL_EQUIVALENT,
        LABEL_WRONG,
        LABEL_ERROR_TURNS,
        LABEL_ERROR_CONTEXT,
        LABEL_INFRA_EVENT_LOOP,
        LABEL_INFRA_OTHER,
        LABEL_UNCLASSIFIED,
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)


def collect_rows(
    source_root: Path,
    logs_root: Path,
    tail_lines: int,
    mode_filter: str,
) -> list[dict]:
    rows: list[dict] = []
    for eval_path in sorted(source_root.glob("modes/*/*/eval_results.csv")):
        model = eval_path.parent.parent.name
        mode = eval_path.parent.name
        if mode_filter and mode_filter not in mode:
            continue
        with eval_path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                rows.append(classify_row(row, model, mode, logs_root, tail_lines))
    return rows


def main() -> None:
    args = parse_args()
    source_root = Path(args.source)
    logs_root = Path(args.logs)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = collect_rows(
        source_root=source_root,
        logs_root=logs_root,
        tail_lines=args.tail_lines,
        mode_filter=args.mode_filter,
    )

    write_task_rows(output_dir / "task_labels.csv", rows)
    write_summary(output_dir / "summary.csv", rows)

    counts = Counter(row["label"] for row in rows)
    print(f"Wrote {len(rows)} task labels to {output_dir / 'task_labels.csv'}")
    print(f"Wrote summary to {output_dir / 'summary.csv'}")
    for label in [
        LABEL_EQUIVALENT,
        LABEL_WRONG,
        LABEL_ERROR_TURNS,
        LABEL_ERROR_CONTEXT,
        LABEL_INFRA_EVENT_LOOP,
        LABEL_INFRA_OTHER,
        LABEL_UNCLASSIFIED,
    ]:
        print(f"{label}: {counts.get(label, 0)}")


if __name__ == "__main__":
    main()
