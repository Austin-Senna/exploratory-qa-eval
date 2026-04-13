#!/usr/bin/env python3
"""Initialize a mirrored plans_mini scaffold for one tasks_mini file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

_TABLE_DESCRIPTIONS_FILENAME = "table_descriptions.jsonl"
_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"
_KNOWN_URIS_CACHE: dict[Path, set[str]] = {}


def _repo_root(start: Path) -> Path:
    anchor = start if start.is_dir() else start.parent
    for candidate in [anchor, *anchor.parents]:
        if (candidate / "tasks_mini").exists() and (candidate / "plans_mini").exists():
            return candidate
    raise RuntimeError(f"Could not locate repo root from '{start}'.")


def _task_relpath(task_path: Path, repo_root: Path) -> Path:
    tasks_root = (repo_root / "tasks_mini").resolve()
    resolved = task_path.resolve()
    try:
        return resolved.relative_to(tasks_root)
    except ValueError as exc:
        raise ValueError(
            f"Task path '{task_path}' must be inside '{tasks_root}'."
        ) from exc


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


def _validate_dataset_sequence(raw: Any, *, task_path: Path) -> list[str]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(
            f"Task '{task_path}' must contain a non-empty 'datasets_used' list."
        )

    out: list[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, str):
            raise ValueError(
                f"Task '{task_path}' has non-string datasets_used[{index}]."
            )
        dataset_id = item.strip()
        if not dataset_id:
            raise ValueError(
                f"Task '{task_path}' has empty datasets_used[{index}]."
            )
        if "/" in dataset_id or "://" in dataset_id:
            raise ValueError(
                f"Task '{task_path}' datasets_used[{index}] must be a bare dataset ID."
            )
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


def _node_dataset_sequence(payload: Dict[str, Any]) -> list[str]:
    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, dict):
        return []

    def _node_sort_key(item: tuple[str, Any]) -> tuple[int, Any]:
        key = item[0]
        try:
            return (0, int(key))
        except (TypeError, ValueError):
            return (1, str(key))

    out: list[str] = []
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


def _node_items(payload: Dict[str, Any]) -> List[tuple[str, Dict[str, Any]]]:
    raw_nodes = payload.get("nodes")
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


def _resolve_source_entry(
    source: Any,
    *,
    repo_root: Path,
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    if not isinstance(source, str):
        return None, None
    candidates = _source_candidates(source)
    if not candidates:
        return None, None

    known_uris = _known_uris(repo_root)
    for candidate in candidates:
        if _canonical_uri(candidate) in known_uris:
            return candidate, None

    chosen = candidates[0]
    note: Dict[str, Any] = {
        "status": "needs_review",
        "original_source": str(source).strip(),
        "chosen_source": chosen,
        "candidate_sources": candidates,
        "reason": (
            "No indexed source candidate matched the task node. "
            "Check likely data files such as files/data.txt, inspect the dataset file listing, "
            "or launch a subagent to verify the real data file before accepting the plan."
        ),
    }
    return chosen, note


def _node_source_sequence(
    payload: Dict[str, Any],
    *,
    repo_root: Path,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    out: List[str] = []
    review_notes: List[Dict[str, Any]] = []
    for _node_id, node_payload in _node_items(payload):
        resolved, note = _resolve_source_entry(node_payload.get("source"), repo_root=repo_root)
        if resolved:
            out.append(resolved)
        if note:
            note = dict(note)
            note["node_id"] = _node_id
            dataset_id = _dataset_id_from_source(node_payload.get("source"))
            if dataset_id:
                note["dataset_id"] = dataset_id
            review_notes.append(note)
    return out, review_notes


def _placeholder_reasoning_text(dataset_sequence: Iterable[str]) -> List[str]:
    lines: List[str] = []
    for step_number, _dataset_id in enumerate(dataset_sequence, start=1):
        lines.append(
            f"{step_number}. [Describe what to verify or compute from dataset step {step_number}.]"
        )
    return lines if lines else ["1. [Describe the first dataset step.]"]


def build_scaffold(task_path: str | Path) -> Tuple[Path, Dict[str, Any]]:
    resolved_task_path = Path(task_path).resolve()
    repo_root = _repo_root(resolved_task_path)
    payload = _load_json(resolved_task_path)
    relpath = _task_relpath(resolved_task_path, repo_root)
    plan_path = repo_root / "plans_mini" / relpath

    task_datasets = _validate_dataset_sequence(
        payload.get("datasets_used"),
        task_path=resolved_task_path,
    )
    node_datasets = _node_dataset_sequence(payload)
    if node_datasets:
        dataset_sequence = node_datasets
    else:
        dataset_sequence = task_datasets

    node_items = _node_items(payload)
    source_sequence, source_resolution_notes = _node_source_sequence(payload, repo_root=repo_root)
    if node_items and len(source_sequence) != len(node_items):
        raise ValueError(
            f"Could not derive source_sequence for every node in '{resolved_task_path}'."
        )
    if not source_sequence:
        raise ValueError(
            f"Could not derive a non-empty source_sequence from task '{resolved_task_path}'."
        )

    question = str(
        payload.get("question")
        or payload.get("original_question")
        or ""
    ).strip()
    reasoning_chain = payload.get("reasoning_chain")

    scaffold: Dict[str, Any] = {
        "dataset_sequence": dataset_sequence,
        "source_sequence": source_sequence,
        "reasoning_chain_text": _placeholder_reasoning_text(dataset_sequence),
    }
    if source_resolution_notes:
        scaffold["source_resolution_notes"] = source_resolution_notes
    if question:
        scaffold["original_final_question"] = question
    if reasoning_chain is not None:
        scaffold["original_reasoning_chain"] = reasoning_chain

    return plan_path, scaffold


def write_scaffold(task_path: str | Path, *, force: bool = False) -> Tuple[Path, Dict[str, Any]]:
    plan_path, scaffold = build_scaffold(task_path)
    if plan_path.exists() and not force:
        raise FileExistsError(
            f"Plan file already exists at '{plan_path}'. Pass --force to overwrite it."
        )
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(scaffold, indent=2) + "\n")
    return plan_path, scaffold


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a mirrored plans_mini scaffold for one tasks_mini file."
    )
    parser.add_argument("task_json_path", help="Path to tasks_mini/.../task_*.json")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the mirrored plan file if it already exists.",
    )
    args = parser.parse_args(argv)

    try:
        plan_path, scaffold = write_scaffold(args.task_json_path, force=args.force)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"Initialized plan scaffold: {plan_path}")
    print()
    print("Reasoning chain template:")
    print("\n".join(scaffold["reasoning_chain_text"]))
    print()
    print(json.dumps({"plan_path": str(plan_path), "scaffold": scaffold}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
