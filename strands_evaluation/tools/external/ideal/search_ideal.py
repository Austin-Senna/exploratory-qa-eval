"""Ideal search tool for source-ordered retrieval.

In ideal mode this is the *only* search tool. Each call consumes up to
``top_k`` planned source targets from ``source_sequence`` and returns the next
concrete file-backed results in plan order.

Use this until exhaustion. You will most likely need all the planned sources.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from strands import tool

from strands_evaluation.tools.external.ideal.plan_store import (
    IdealTaskPlan,
    load_plan_for_context,
    set_plans_root as _set_plans_root_shared,
    set_task_context as _set_task_context_shared,
)

logger = logging.getLogger(__name__)

_TASK_CONTEXT: Dict[str, Any] = {}
_CURRENT_PLAN: Optional[IdealTaskPlan] = None
_PLAN_CURSOR: int = 0

_TABLE_DESCRIPTIONS_PATH = Path("table_descriptions.jsonl")
_TABLE_CACHE_LOADED = False
_TABLE_ENTRY_BY_URI: Dict[str, Dict[str, str]] = {}

_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"
_TRUNCATED_CONTENT_WORDS = 200


def set_db_path(path: str) -> None:
    """Retained for compatibility; ideal source-driven retrieval ignores db_path."""
    _ = path


def set_plans_root(path: str | Path) -> None:
    """Override plans root (mainly for tests)."""
    _set_plans_root_shared(path)
    global _CURRENT_PLAN, _PLAN_CURSOR
    _CURRENT_PLAN = None
    _PLAN_CURSOR = 0


def set_task_context(task_context: Dict[str, Any]) -> None:
    """Load and validate the active task plan; resets iterator cursor."""
    global _TASK_CONTEXT, _CURRENT_PLAN, _PLAN_CURSOR
    _TASK_CONTEXT = dict(task_context or {})
    _set_task_context_shared(_TASK_CONTEXT)
    _CURRENT_PLAN = load_plan_for_context(_TASK_CONTEXT)
    _PLAN_CURSOR = 0


def reset_state() -> None:
    """Reset in-process plan/iterator state and cached table descriptions."""
    global _TASK_CONTEXT, _CURRENT_PLAN, _PLAN_CURSOR
    global _TABLE_CACHE_LOADED, _TABLE_ENTRY_BY_URI
    _TASK_CONTEXT = {}
    _CURRENT_PLAN = None
    _PLAN_CURSOR = 0
    _TABLE_CACHE_LOADED = False
    _TABLE_ENTRY_BY_URI = {}
    _set_task_context_shared({})


def _require_plan() -> IdealTaskPlan:
    global _CURRENT_PLAN
    if _CURRENT_PLAN is None:
        _CURRENT_PLAN = load_plan_for_context(_TASK_CONTEXT)
    return _CURRENT_PLAN


def _load_table_cache() -> None:
    global _TABLE_CACHE_LOADED, _TABLE_ENTRY_BY_URI
    if _TABLE_CACHE_LOADED:
        return

    if not _TABLE_DESCRIPTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Required dependency '{_TABLE_DESCRIPTIONS_PATH}' not found. "
            "search_tool=ideal requires table_descriptions.jsonl at the repo root "
            "for description/content enrichment."
        )

    _TABLE_CACHE_LOADED = True
    uri_map: Dict[str, Dict[str, str]] = {}
    with _TABLE_DESCRIPTIONS_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            uri = str(obj.get("dataset_uri") or obj.get("uri") or "").strip()
            if not uri:
                continue

            description = str(obj.get("description") or "").strip()
            content = str(obj.get("content") or "").strip()
            uri_map[uri] = {
                "description": description,
                "content": content,
            }

    _TABLE_ENTRY_BY_URI = uri_map


def _truncate_words(text: str, max_words: int = _TRUNCATED_CONTENT_WORDS) -> str:
    words = (text or "").split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words])


def _dataset_id_from_source(source: str) -> str:
    value = str(source or "").strip()
    if "/" not in value:
        return value
    parts = value.split("/")
    if len(parts) >= 2 and parts[1].strip():
        return parts[1].strip()
    return value


def _canonical_uri(source_path: str) -> str:
    return f"{_S3_PREFIX}{str(source_path).lstrip('/')}"


def _metadata_for_uri(uri: str) -> Dict[str, str]:
    _load_table_cache()
    return _TABLE_ENTRY_BY_URI.get(uri, {})


def _build_file_result(source_path: str) -> Dict[str, Any]:
    uri = _canonical_uri(source_path)
    dataset_id = _dataset_id_from_source(source_path)
    metadata = _metadata_for_uri(uri)
    out: Dict[str, Any] = {
        "source_kind": "file",
        "dataset_id": dataset_id,
        "uri": uri,
    }
    description = metadata.get("description", "")
    content = _truncate_words(metadata.get("content", ""))
    if description:
        out["description"] = description
    if content:
        out["content"] = content
    return out


def _normalize_top_k(top_k: Any) -> int:
    try:
        value = int(top_k)
    except (TypeError, ValueError):
        return 10
    return max(value, 1)


@tool
def search_ideal(query: str, top_k: int = 10) -> dict:
    """Ideal-mode retrieval: consume the next planned source target.

    ``query`` is retained only for interface compatibility with the other
    search tools. Source-driven ideal retrieval does not use query text to
    choose results; it walks the pre-authored ``source_sequence`` in order.
    ``top_k`` controls how many sequential planned sources are returned in one
    call.
    """
    global _PLAN_CURSOR
    plan = _require_plan()

    total_steps = len(plan.source_sequence)
    if _PLAN_CURSOR >= total_steps:
        return {
            "results": [],
            "count": 0,
            "query": query,
            "task_id": plan.task_id,
            "plan_path": str(plan.plan_path),
            "plan_step_index": _PLAN_CURSOR,
            "plan_steps_total": total_steps,
            "plan_exhausted": True,
            "note": "ideal search exhausted; no further planned sources remain for this task.",
        }

    limit = _normalize_top_k(top_k)
    start_index = _PLAN_CURSOR
    end_index = min(total_steps, start_index + limit)
    result_rows: List[Dict[str, Any]] = []
    dataset_ids: List[str] = []
    step_indices: List[int] = []
    step_numbers: List[int] = []

    for step_index in range(start_index, end_index):
        source_entry = plan.source_sequence[step_index]
        result_row = _build_file_result(source_entry)
        result_rows.append(result_row)
        dataset_ids.append(result_row.get("dataset_id") or _dataset_id_from_source(source_entry))
        step_indices.append(step_index)
        step_numbers.append(step_index + 1)

    _PLAN_CURSOR = end_index

    payload: Dict[str, Any] = {
        "results": result_rows,
        "count": len(result_rows),
        "query": query,
        "task_id": plan.task_id,
        "plan_path": str(plan.plan_path),
        "dataset_ids": dataset_ids,
        "plan_step_indices": step_indices,
        "plan_step_numbers": step_numbers,
        "plan_steps_total": total_steps,
        "plan_exhausted": _PLAN_CURSOR >= total_steps,
        "ideal_source_driven": True,
    }
    if dataset_ids:
        payload["dataset_id"] = dataset_ids[0]
    if step_indices:
        payload["plan_step_index"] = step_indices[0]
    if step_numbers:
        payload["plan_step_number"] = step_numbers[0]
    return payload
