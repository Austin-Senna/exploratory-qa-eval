"""Ideal search tool for query-driven retrieval over the authored source pool."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from strands import Agent, tool

from strands_evaluation.config import AgentConfig
from strands_evaluation.llm.llm_factory import build_model
from strands_evaluation.tools.external.ideal.plan_store import (
    load_plan_for_context,
    set_plans_root as _set_plans_root_shared,
    set_task_context as _set_task_context_shared,
)

logger = logging.getLogger(__name__)

_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"
_JUDGE_SYSTEM_PROMPT = (
    "You are a dataset selector. The user gives you a search query and a list of\n"
    "candidate datasets (each with s3_uri and dataset_id). Call the `pick` tool\n"
    "exactly once with the s3_uris most relevant to the query. Return nothing if nothing is too semantically similar to the dataset.\n"
    If\n"
    'the query is clearly aggregate (year ranges, "all of", multiple regions),\n'
    "pick the matching group. Never pick an s3_uri not in the list."
)

# The eval runner uses one task at a time per process; parallel runs fork subprocesses.
_CANDIDATES: list[tuple[str, str]] = []
_USED_S3_URIS: set[str] = set()


def set_db_path(path: str) -> None:
    """Retained for compatibility; ideal retrieval ignores db_path."""
    _ = path


def set_plans_root(path: str | Path) -> None:
    """Override plans root (mainly for tests)."""
    _set_plans_root_shared(path)
    _CANDIDATES.clear()
    _USED_S3_URIS.clear()


def set_task_context(task_context: Dict[str, Any]) -> None:
    """Load the active task plan and materialize the candidate pool."""
    task_context = dict(task_context or {})
    _set_task_context_shared(task_context)
    plan = load_plan_for_context(task_context)
    _CANDIDATES.clear()
    _CANDIDATES.extend(
        (_canonical_uri(source_path), _dataset_id_from_source(source_path))
        for source_path in plan.source_sequence
    )
    _USED_S3_URIS.clear()


def reset_state() -> None:
    """Reset in-process candidate/judge state."""
    _CANDIDATES.clear()
    _USED_S3_URIS.clear()
    _set_task_context_shared({})


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


def _format_judge_prompt(query: str, remaining: list[tuple[str, str]]) -> str:
    lines = [f"Query: {query}", "", "Candidates:"]
    for index, (s3_uri, dataset_id) in enumerate(remaining, start=1):
        lines.append(f"{index}. s3_uri={s3_uri}  dataset_id={dataset_id}")
    return "\n".join(lines)


def _judge_model():
    return build_model(AgentConfig(model_name="openai/gpt-5.4-nano"))


def _build_judge(remaining: list[tuple[str, str]]) -> tuple[Agent, Dict[str, Any]]:
    valid_uris = {uri for uri, _ in remaining}
    state: Dict[str, Any] = {"picked": None, "reason": None}

    @tool
    def pick(s3_uris: list[str], reason: str) -> str:
        """Record the s3_uris most relevant to the query. Call EXACTLY once."""
        if not isinstance(s3_uris, list) or not s3_uris:
            raise ValueError("s3_uris must be a non-empty list of strings")
        bad = [uri for uri in s3_uris if uri not in valid_uris]
        if bad:
            raise ValueError(
                f"Picked s3_uri(s) not in candidate list: {bad}. "
                "You must pick from the provided list only."
            )
        state["picked"] = list(dict.fromkeys(s3_uris))
        state["reason"] = reason
        return f"Recorded {len(state['picked'])} pick(s)."

    judge = Agent(
        model=_judge_model(),
        system_prompt=_JUDGE_SYSTEM_PROMPT,
        tools=[pick],
        callback_handler=None,
    )
    return judge, state


def _fallback_pick(remaining: list[tuple[str, str]]) -> list[str]:
    fallback = [remaining[0][0]]
    logger.warning("search_ideal judge failed to record a pick; falling back to first remaining uri=%s", fallback[0])
    return fallback


@tool
def search_ideal(query: str, top_k: int = 100) -> dict:
    """Return the planned sources most relevant to ``query``."""
    _ = top_k

    if not _CANDIDATES:
        return {"error": "search_ideal called before set_task_context; no plan loaded."}

    remaining = [(uri, dsid) for uri, dsid in _CANDIDATES if uri not in _USED_S3_URIS]
    if not remaining:
        return {
            "results": [],
            "count": 0,
            "query": query,
            "plan_exhausted": True,
        }

    judge, state = _build_judge(remaining)
    judge(_format_judge_prompt(query, remaining))

    picked = state["picked"] or _fallback_pick(remaining)
    _USED_S3_URIS.update(picked)
    logger.info(
        "search_ideal judge picked %d uri(s) reason=%r",
        len(picked),
        state["reason"],
    )

    dsid_by_uri = dict(remaining)
    results = [{"s3_uri": uri, "dataset_id": dsid_by_uri[uri]} for uri in picked]
    return {
        "results": results,
        "count": len(results),
        "query": query,
        "plan_exhausted": len(_USED_S3_URIS) >= len(_CANDIDATES),
    }
