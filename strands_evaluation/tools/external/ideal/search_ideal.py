"""Ideal search tool for file-backed, step-ordered dataset traversal.

In ideal mode this is the *only* search tool. Each call consumes one dataset
from ``plans_mini/.../task_*.json`` -> ``dataset_sequence`` and searches only
within that dataset.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import sys

from strands import tool

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent.parent.parent.parent / "external-tools" / "hybrid_search"),
)

import api as _api  # noqa: E402

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


def set_db_path(path: str) -> None:
    """Override LanceDB search index path for this process."""
    _api.cfg.path = str(path)
    _api._db = None


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
    """Reset in-process plan/iterator state (mainly for tests)."""
    global _TASK_CONTEXT, _CURRENT_PLAN, _PLAN_CURSOR
    _TASK_CONTEXT = {}
    _CURRENT_PLAN = None
    _PLAN_CURSOR = 0
    _set_task_context_shared({})


def _require_plan() -> IdealTaskPlan:
    global _CURRENT_PLAN
    if _CURRENT_PLAN is None:
        _CURRENT_PLAN = load_plan_for_context(_TASK_CONTEXT)
    return _CURRENT_PLAN


def _safe_top_k(value: Any) -> int:
    try:
        n = int(value)
    except Exception:
        return 10
    return n if n > 0 else 10


def _search_dataset(query: str, dataset_id: str, top_k: int) -> List[Dict[str, Any]]:
    table = _api.get_table()
    marker = f"/{dataset_id}/"
    scan_limit = max(top_k * 12, 60)

    rows: List[Dict[str, Any]]
    try:
        escaped = dataset_id.replace("'", "''")
        rows = (
            table.search(query, query_type="fts", fts_columns="text")
            .where(f"uri LIKE '%/{escaped}/%'")
            .limit(scan_limit)
            .select(["uri", "text", "_score"])
            .to_list()
        )
    except Exception as exc:
        logger.warning(
            "Dataset-scoped where() query failed for dataset '%s'; using fallback filter (%s)",
            dataset_id,
            exc,
        )
        rows = (
            table.search(query, query_type="fts", fts_columns="text")
            .limit(scan_limit * 3)
            .select(["uri", "text", "_score"])
            .to_list()
        )
        rows = [r for r in rows if marker in str(r.get("uri", ""))]

    out: List[Dict[str, Any]] = []
    for row in rows:
        uri = str(row.get("uri") or "").strip()
        if not uri or marker not in uri:
            continue
        doc = str(row.get("text") or "")
        score_raw = row.get("_score", 0.0)
        try:
            score_text = f"{float(score_raw):.3f}"
        except Exception:
            score_text = str(score_raw)
        out.append(
            {
                "uri": uri,
                "dataset_id": dataset_id,
                "document": doc,
                "score": score_text,
            }
        )
        if len(out) >= top_k:
            break

    return out


@tool
def search_ideal(query: str, top_k: int = 10) -> dict:
    """Ideal-mode search: consume next dataset in sequence and search only within it."""
    global _PLAN_CURSOR
    plan = _require_plan()

    requested_top_k = _safe_top_k(top_k)
    total_steps = len(plan.dataset_sequence)
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
            "note": "dataset_sequence exhausted; no further ideal search datasets remain.",
        }

    step_index = _PLAN_CURSOR
    dataset_id = plan.dataset_sequence[step_index]
    _PLAN_CURSOR += 1  # strict iterator: every search_ideal call consumes exactly one step.

    try:
        results = _search_dataset(query, dataset_id, requested_top_k)
        payload: Dict[str, Any] = {
            "results": results,
            "count": len(results),
            "query": query,
            "task_id": plan.task_id,
            "plan_path": str(plan.plan_path),
            "dataset_id": dataset_id,
            "plan_step_index": step_index,
            "plan_step_number": step_index + 1,
            "plan_steps_total": total_steps,
            "plan_exhausted": _PLAN_CURSOR >= total_steps,
        }
        return payload
    except Exception as exc:
        return {
            "error": str(exc),
            "results": [],
            "count": 0,
            "query": query,
            "task_id": plan.task_id,
            "plan_path": str(plan.plan_path),
            "dataset_id": dataset_id,
            "plan_step_index": step_index,
            "plan_step_number": step_index + 1,
            "plan_steps_total": total_steps,
            "plan_exhausted": _PLAN_CURSOR >= total_steps,
        }
