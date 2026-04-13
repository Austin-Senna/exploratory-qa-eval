#!/usr/bin/env python3
"""Validate whether a plans_mini file is clean enough for ideal prompt injection."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

_STEP_RE = re.compile(r"(?m)^\s*(\d+)\.\s+(.*?)\s*$")
_YEAR_RE = re.compile(r"(?:19|20)\d{2}")
_TABLE_DESCRIPTIONS_FILENAME = "table_descriptions.jsonl"
_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"
_KNOWN_URIS_CACHE: Dict[Path, set[str]] = {}

_BANNED_PATTERNS: Sequence[tuple[str, re.Pattern[str], str]] = (
    ("final_answer", re.compile(r"(?i)\bfinal answer\s*:"), "Remove 'Final answer:' text."),
    ("node_label", re.compile(r"(?i)\bnode(?:_\d+)?\b"), "Remove node-style labels and placeholders."),
    ("hop_label", re.compile(r"(?i)\bhop\b"), "Remove HOP-style trace labels."),
    ("dataset_position", re.compile(r"(?i)\bdataset position\b"), "Do not refer to dataset positions in reasoning scaffolding."),
    ("sequence_indexing", re.compile(r"(?i)\bin the sequence after step\b"), "Do not refer to hidden dataset-sequence indexing in reasoning scaffolding."),
    ("verify_matches", re.compile(r"(?i)\bverify (?:that|it)\s+matches\b"), "Remove 'verify it matches' narration and say directly what to determine."),
    ("angle_placeholder", re.compile(r"<[^>\n]+>"), "Remove angle-bracket placeholders."),
    ("raw_source_path", re.compile(r"(?i)(?:datagov|wikipedia)/|://"), "Remove raw dataset or URI paths."),
    ("solution_arrow", re.compile(r"->|→"), "Remove solved-trace arrows."),
    ("set_literal", re.compile(r"[{}]"), "Avoid set-literal notation in reasoning scaffolding."),
)


def _repo_root(start: Path) -> Path:
    anchor = start if start.is_dir() else start.parent
    for candidate in [anchor, *anchor.parents]:
        if (candidate / "tasks_mini").exists() and (candidate / "plans_mini").exists():
            return candidate
    raise RuntimeError(f"Could not locate repo root from '{start}'.")


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at '{path}': {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at '{path}'.")
    return payload


def _known_uris(repo_root: Path) -> set[str]:
    table_path = repo_root / _TABLE_DESCRIPTIONS_FILENAME
    cached = _KNOWN_URIS_CACHE.get(table_path)
    if cached is not None:
        return cached
    if not table_path.exists():
        _KNOWN_URIS_CACHE[table_path] = set()
        return _KNOWN_URIS_CACHE[table_path]

    known: set[str] = set()
    with table_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            uri = str(obj.get("dataset_uri") or obj.get("uri") or "").strip()
            if uri:
                known.add(uri)
    _KNOWN_URIS_CACHE[table_path] = known
    return known


def _canonical_uri(source_path: str) -> str:
    return f"{_S3_PREFIX}{str(source_path).lstrip('/')}"


def _plan_relpath(plan_path: Path, repo_root: Path) -> Path:
    plans_root = (repo_root / "plans_mini").resolve()
    resolved = plan_path.resolve()
    try:
        return resolved.relative_to(plans_root)
    except ValueError as exc:
        raise ValueError(
            f"Plan path '{plan_path}' must be inside '{plans_root}'."
        ) from exc


def _task_path_for_plan(plan_path: Path, repo_root: Path) -> Optional[Path]:
    relpath = _plan_relpath(plan_path, repo_root)
    task_path = repo_root / "tasks_mini" / relpath
    return task_path if task_path.exists() else None


def _add_issue(issues: List[Dict[str, Any]], code: str, message: str, **extra: Any) -> None:
    item: Dict[str, Any] = {"code": code, "message": message}
    item.update(extra)
    issues.append(item)


def _extract_steps(reasoning_chain_text: str) -> List[Dict[str, Any]]:
    return [
        {
            "number": int(match.group(1)),
            "text": match.group(2).strip(),
        }
        for match in _STEP_RE.finditer(reasoning_chain_text)
    ]


def _validate_dataset_sequence(raw: Any, issues: List[Dict[str, Any]]) -> List[str]:
    if not isinstance(raw, list) or not raw:
        _add_issue(
            issues,
            "invalid_dataset_sequence",
            "dataset_sequence must be a non-empty list of bare dataset IDs.",
        )
        return []

    dataset_sequence: List[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, str):
            _add_issue(
                issues,
                "invalid_dataset_id",
                "dataset_sequence entries must be strings.",
                index=index,
            )
            continue
        dataset_id = item.strip()
        if not dataset_id:
            _add_issue(
                issues,
                "invalid_dataset_id",
                "dataset_sequence entries cannot be empty.",
                index=index,
            )
            continue
        if "/" in dataset_id or "://" in dataset_id:
            _add_issue(
                issues,
                "invalid_dataset_id",
                "dataset_sequence entries must be bare dataset IDs, not paths or URIs.",
                index=index,
                value=dataset_id,
            )
            continue
        dataset_sequence.append(dataset_id)
    return dataset_sequence


def _validate_source_sequence(raw: Any, issues: List[Dict[str, Any]]) -> List[str]:
    if not isinstance(raw, list) or not raw:
        _add_issue(
            issues,
            "invalid_source_sequence",
            "source_sequence must be a non-empty list of dataset-relative file paths.",
        )
        return []

    source_sequence: List[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, str):
            _add_issue(
                issues,
                "invalid_source_entry",
                "source_sequence entries must be strings.",
                index=index,
            )
            continue
        source_entry = item.strip()
        if not source_entry:
            _add_issue(
                issues,
                "invalid_source_entry",
                "source_sequence entries cannot be empty.",
                index=index,
            )
            continue
        if "/" not in source_entry:
            _add_issue(
                issues,
                "invalid_source_entry",
                "source_sequence entries must be dataset-relative file paths, not bare dataset IDs.",
                index=index,
                value=source_entry,
            )
            continue
        if "://" in source_entry:
            _add_issue(
                issues,
                "invalid_source_entry",
                "source_sequence entries must be dataset-relative file paths, not full URIs.",
                index=index,
                value=source_entry,
            )
            continue
        source_sequence.append(source_entry)
    return source_sequence


def _task_dataset_ids(raw: Any) -> List[str]:
    if not isinstance(raw, list):
        return []
    out: List[str] = []
    for item in raw:
        if not isinstance(item, str):
            continue
        dataset_id = item.strip()
        if not dataset_id or "/" in dataset_id or "://" in dataset_id:
            continue
        out.append(dataset_id)
    return out


def _dataset_id_from_source(source: Any) -> Optional[str]:
    if not isinstance(source, str):
        return None
    value = source.strip()
    if not value:
        return None
    parts = value.split("/")
    if len(parts) >= 2:
        dataset_id = parts[1].strip()
        return dataset_id or None
    return value


def _node_dataset_sequence(task_payload: Dict[str, Any]) -> List[str]:
    raw_nodes = task_payload.get("nodes")
    if not isinstance(raw_nodes, dict):
        return []

    def _node_sort_key(item: tuple[str, Any]) -> tuple[int, Any]:
        key = item[0]
        try:
            return (0, int(key))
        except (TypeError, ValueError):
            return (1, str(key))

    out: List[str] = []
    seen: set[str] = set()
    for _node_id, node_payload in sorted(raw_nodes.items(), key=_node_sort_key):
        if not isinstance(node_payload, dict):
            continue
        dataset_id = _dataset_id_from_source(node_payload.get("source"))
        if not dataset_id or dataset_id in seen:
            continue
        seen.add(dataset_id)
        out.append(dataset_id)
    return out


def _node_items(task_payload: Dict[str, Any]) -> List[tuple[str, Dict[str, Any]]]:
    raw_nodes = task_payload.get("nodes")
    if not isinstance(raw_nodes, dict):
        return []

    def _node_sort_key(item: tuple[str, Any]) -> tuple[int, Any]:
        key = item[0]
        try:
            return (0, int(key))
        except (TypeError, ValueError):
            return (1, str(key))

    items: List[tuple[str, Dict[str, Any]]] = []
    for node_id, node_payload in sorted(raw_nodes.items(), key=_node_sort_key):
        if isinstance(node_payload, dict):
            items.append((node_id, node_payload))
    return items


def _source_candidates(source: str) -> List[str]:
    value = str(source or "").strip()
    if not value:
        return []

    stem, dot, _ext = value.rpartition(".")
    txt_candidate = f"{stem}.txt" if dot else value
    json_candidate = f"{stem}.json" if dot else f"{value}.json"

    ordered: List[str] = []
    seen: set[str] = set()
    for candidate in (txt_candidate, value, json_candidate):
        for option in (candidate, candidate.replace("/v1/files/", "/files/")):
            normalized = option.strip().lstrip("/")
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
    return ordered


def _resolve_source_entry(source: Any, *, repo_root: Path) -> Optional[str]:
    if not isinstance(source, str):
        return None
    candidates = _source_candidates(source)
    if not candidates:
        return None

    known_uris = _known_uris(repo_root)
    for candidate in candidates:
        if _canonical_uri(candidate) in known_uris:
            return candidate
    return candidates[0]


def _node_source_sequence(task_payload: Dict[str, Any], *, repo_root: Path) -> List[str]:
    out: List[str] = []
    for _node_id, node_payload in _node_items(task_payload):
        resolved = _resolve_source_entry(node_payload.get("source"), repo_root=repo_root)
        if resolved:
            out.append(resolved)
    return out


def _normalize_reasoning_text_value(value: str) -> str:
    text = value.strip()
    if "\n" not in text and "\\n" in text:
        text = text.replace("\\n", "\n")
    return text


def _validate_source_resolution_notes(raw: Any, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        _add_issue(
            issues,
            "invalid_source_resolution_notes",
            "source_resolution_notes must be a list when present.",
        )
        return []
    notes: List[Dict[str, Any]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            _add_issue(
                issues,
                "invalid_source_resolution_note",
                "source_resolution_notes entries must be objects.",
                index=index,
            )
            continue
        notes.append(item)
    return notes


def _validate_reasoning_text(raw: Any, issues: List[Dict[str, Any]]) -> str:
    if isinstance(raw, str):
        text = _normalize_reasoning_text_value(raw)
        if not text:
            _add_issue(
                issues,
                "invalid_reasoning_chain_text",
                "reasoning_chain_text cannot be empty.",
            )
        return text

    if isinstance(raw, list):
        if not raw:
            _add_issue(
                issues,
                "invalid_reasoning_chain_text",
                "reasoning_chain_text cannot be an empty list.",
            )
            return ""

        lines: List[str] = []
        for index, item in enumerate(raw):
            if not isinstance(item, str):
                _add_issue(
                    issues,
                    "invalid_reasoning_chain_text_item",
                    "reasoning_chain_text list entries must be strings.",
                    index=index,
                )
                continue
            text = _normalize_reasoning_text_value(item)
            if not text:
                _add_issue(
                    issues,
                    "invalid_reasoning_chain_text_item",
                    "reasoning_chain_text list entries cannot be empty.",
                    index=index,
                )
                continue
            lines.append(text)
        return "\n".join(lines)

    _add_issue(
        issues,
        "invalid_reasoning_chain_text",
        "reasoning_chain_text must be a string or a list of strings.",
    )
    return ""


def _dataset_group_key(dataset_id: str) -> str:
    base = _YEAR_RE.sub("", dataset_id.lower())
    base = re.sub(r"[-_]+", "-", base).strip("-")
    return base


def _dataset_years(dataset_sequence: Sequence[str]) -> set[str]:
    years: set[str] = set()
    for dataset_id in dataset_sequence:
        years.update(_YEAR_RE.findall(dataset_id))
    return years


def _task_question(task_payload: Dict[str, Any]) -> str:
    return str(
        task_payload.get("question")
        or task_payload.get("original_question")
        or ""
    ).strip()


def _flatten_candidate_answers(raw: Any) -> Iterable[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, (int, float)):
        return [str(raw)]
    if isinstance(raw, list):
        values: List[str] = []
        for item in raw:
            values.extend(_flatten_candidate_answers(item))
        return values
    return []


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _contains_candidate(text: str, candidate: str) -> bool:
    candidate = candidate.strip()
    if not candidate:
        return False

    if candidate.isdigit():
        return re.search(rf"(?<!\d){re.escape(candidate)}(?!\d)", text) is not None

    return _normalized(candidate) in _normalized(text)


def _collect_leak_candidates(task_payload: Dict[str, Any]) -> List[str]:
    question_text = _task_question(task_payload)
    question_norm = _normalized(question_text)

    raw_candidates: List[str] = []
    raw_candidates.extend(_flatten_candidate_answers(task_payload.get("answer")))

    nodes = task_payload.get("nodes")
    if isinstance(nodes, dict):
        for node_payload in nodes.values():
            if isinstance(node_payload, dict):
                raw_candidates.extend(_flatten_candidate_answers(node_payload.get("answer")))

    cleaned: List[str] = []
    seen = set()
    for candidate in raw_candidates:
        text = str(candidate).strip()
        if not text:
            continue
        if len(text) < 3 and not text.isdigit():
            continue
        normalized = _normalized(text)
        if normalized in question_norm:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        cleaned.append(text)
    return cleaned


def evaluate_plan(plan_path: str | Path) -> Dict[str, Any]:
    resolved_plan_path = Path(plan_path).resolve()
    repo_root = _repo_root(resolved_plan_path)
    issues: List[Dict[str, Any]] = []

    payload = _load_json(resolved_plan_path)
    dataset_sequence = _validate_dataset_sequence(payload.get("dataset_sequence"), issues)
    source_sequence = _validate_source_sequence(payload.get("source_sequence"), issues)
    source_resolution_notes = _validate_source_resolution_notes(
        payload.get("source_resolution_notes"),
        issues,
    )
    reasoning_chain_text = _validate_reasoning_text(payload.get("reasoning_chain_text"), issues)
    steps = _extract_steps(reasoning_chain_text)

    non_empty_lines = [line.strip() for line in reasoning_chain_text.splitlines() if line.strip()]
    if reasoning_chain_text and len(non_empty_lines) != len(steps):
        _add_issue(
            issues,
            "unnumbered_text",
            "reasoning_chain_text must contain only numbered step lines.",
        )

    expected_numbers = list(range(1, len(steps) + 1))
    actual_numbers = [step["number"] for step in steps]
    if steps and actual_numbers != expected_numbers:
        _add_issue(
            issues,
            "step_numbering",
            "Step numbers must be contiguous and start at 1.",
            actual=actual_numbers,
            expected=expected_numbers,
        )

    if dataset_sequence and steps and len(steps) > len(dataset_sequence):
        _add_issue(
            issues,
            "step_count_exceeds_datasets",
            "The number of reasoning steps should not exceed dataset_sequence length.",
            dataset_count=len(dataset_sequence),
            step_count=len(steps),
        )
    if source_sequence and steps and len(steps) > len(source_sequence):
        _add_issue(
            issues,
            "step_count_exceeds_sources",
            "The number of reasoning steps should not exceed source_sequence length.",
            source_count=len(source_sequence),
            step_count=len(steps),
        )

    if source_resolution_notes:
        _add_issue(
            issues,
            "source_resolution_review_required",
            "source_resolution_notes is still populated. Resolve the file choice before accepting the plan.",
            note_count=len(source_resolution_notes),
        )

    oversplit_hits = [
        phrase
        for phrase in (
            "for one of the",
            "for a second",
            "for the remaining",
        )
        if phrase in reasoning_chain_text.lower()
    ]
    if len(oversplit_hits) >= 2:
        _add_issue(
            issues,
            "oversplit_parallel_lookup",
            "Collapse repetitive parallel lookups into a grouped step when they are part of the same subtask.",
            matches=oversplit_hits,
        )

    duplicate_steps: Dict[str, int] = {}
    for step in steps:
        text_key = re.sub(r"\s+", " ", step["text"].strip().lower())
        if text_key in duplicate_steps:
            _add_issue(
                issues,
                "duplicate_step",
                f"Step {step['number']} duplicates step {duplicate_steps[text_key]}.",
                step=step["number"],
            )
        else:
            duplicate_steps[text_key] = step["number"]

        for match in re.finditer(r"(?i)\bstep\s+(\d+)\b", step["text"]):
            referenced_step = int(match.group(1))
            if referenced_step > step["number"]:
                _add_issue(
                    issues,
                    "forward_reference",
                    f"Step {step['number']} references future step {referenced_step}.",
                    step=step["number"],
                    referenced_step=referenced_step,
                )

    for code, pattern, message in _BANNED_PATTERNS:
        match = pattern.search(reasoning_chain_text)
        if match:
            _add_issue(
                issues,
                code,
                message,
                match=match.group(0),
            )

    group_counts = Counter(
        _dataset_group_key(dataset_id)
        for dataset_id in dataset_sequence
        if _YEAR_RE.search(dataset_id)
    )
    step_years = [set(_YEAR_RE.findall(step["text"])) for step in steps]
    for dataset_id in dataset_sequence:
        years_in_dataset = set(_YEAR_RE.findall(dataset_id))
        group_key = _dataset_group_key(dataset_id)
        if years_in_dataset and group_counts[group_key] > 1:
            if not any(years_in_step.intersection(years_in_dataset) for years_in_step in step_years):
                _add_issue(
                    issues,
                    "missing_year_context",
                    f"The reasoning chain should mention the year or period for dataset '{dataset_id}'.",
                    dataset_id=dataset_id,
                )

    task_path = _task_path_for_plan(resolved_plan_path, repo_root)
    if task_path is not None:
        task_payload = _load_json(task_path)
        task_datasets = _task_dataset_ids(task_payload.get("datasets_used"))
        node_datasets = _node_dataset_sequence(task_payload)
        expected_sequence = node_datasets or task_datasets
        node_items = _node_items(task_payload)
        known_uris = _known_uris(repo_root)

        if node_datasets and task_datasets and set(node_datasets) != set(task_datasets):
            _add_issue(
                issues,
                "task_source_dataset_mismatch",
                "The mirrored task's datasets_used list does not match the unique dataset IDs referenced by nodes.",
                task_datasets=task_datasets,
                node_datasets=node_datasets,
            )

        if expected_sequence:
            if set(dataset_sequence) != set(expected_sequence):
                _add_issue(
                    issues,
                    "dataset_coverage_mismatch",
                    "dataset_sequence must cover the same unique dataset IDs used by the mirrored task.",
                    expected_sequence=expected_sequence,
                    actual_sequence=dataset_sequence,
                )
            elif dataset_sequence != expected_sequence:
                _add_issue(
                    issues,
                    "dataset_order_mismatch",
                    "dataset_sequence must follow first-appearance node order from the mirrored task.",
                    expected_sequence=expected_sequence,
                    actual_sequence=dataset_sequence,
                )

        if node_items:
            if len(source_sequence) != len(node_items):
                _add_issue(
                    issues,
                    "source_sequence_length_mismatch",
                    "source_sequence must contain one file-backed entry per node in node order.",
                    expected_count=len(node_items),
                    actual_count=len(source_sequence),
                )
            else:
                for index, ((node_id, node_payload), source_entry) in enumerate(zip(node_items, source_sequence)):
                    expected_dataset_id = _dataset_id_from_source(node_payload.get("source"))
                    actual_dataset_id = _dataset_id_from_source(source_entry)
                    if expected_dataset_id and actual_dataset_id != expected_dataset_id:
                        _add_issue(
                            issues,
                            "source_dataset_mismatch",
                            "source_sequence must stay aligned to the dataset used by each node.",
                            index=index,
                            node_id=node_id,
                            expected_dataset_id=expected_dataset_id,
                            actual_dataset_id=actual_dataset_id,
                            actual_source=source_entry,
                        )

        for index, source_entry in enumerate(source_sequence):
            if _canonical_uri(source_entry) not in known_uris:
                _add_issue(
                    issues,
                    "source_not_indexed",
                    "source_sequence entries must point to indexed file-backed sources, or remain explicitly marked for review.",
                    index=index,
                    source_entry=source_entry,
                )

        dataset_year_values = _dataset_years(dataset_sequence)
        step_text_for_leaks = "\n".join(step["text"] for step in steps)
        leaked_values = [
            candidate
            for candidate in _collect_leak_candidates(task_payload)
            if not (candidate.isdigit() and candidate in dataset_year_values)
            if _contains_candidate(step_text_for_leaks, candidate)
        ]
        if leaked_values:
            _add_issue(
                issues,
                "answer_leak",
                "reasoning_chain_text leaks discovered answers or intermediate entities not present in the question.",
                leaked_values=leaked_values[:10],
            )

    result = {
        "status": "clean" if not issues else "needs_revision",
        "plan_path": str(resolved_plan_path),
        "task_path": str(task_path) if task_path is not None else None,
        "dataset_count": len(dataset_sequence),
        "step_count": len(steps),
        "issues": issues,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a plans_mini reasoning chain is clean enough for ideal-mode prompt injection."
    )
    parser.add_argument("plan_json_path", help="Path to plans_mini/.../task_*.json")
    args = parser.parse_args(argv)

    try:
        result = evaluate_plan(args.plan_json_path)
    except Exception as exc:
        print(json.dumps({
            "status": "needs_revision",
            "issues": [{"code": "runtime_error", "message": str(exc)}],
        }, indent=2))
        return 1

    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "clean" else 1


if __name__ == "__main__":
    raise SystemExit(main())
