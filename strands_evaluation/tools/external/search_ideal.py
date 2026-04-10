"""Ideal search tool scaffold.

Design-first placeholder for an ideal search backend. This module preserves the
search tool contract so the ablation framework can be wired end-to-end before
final retrieval behavior is implemented.
"""

from __future__ import annotations

from typing import Any, Dict, List

from strands import tool

_TASK_CONTEXT: Dict[str, Any] = {}


def set_task_context(task_context: Dict[str, Any]) -> None:
    """Optional future hook for task-aware ideal retrieval behavior."""
    global _TASK_CONTEXT
    _TASK_CONTEXT = dict(task_context or {})


def _placeholder_payload(query: str) -> Dict[str, Any]:
    return {
        "results": [],
        "count": 0,
        "query": query,
        "note": (
            "search_ideal is a scaffold in this phase. "
            "Concrete ideal retrieval behavior is not implemented yet."
        ),
    }


@tool
def search_value(query: str, top_k: int = 10) -> dict:
    _ = top_k
    return _placeholder_payload(query)


@tool
def search_schema(query: str, top_k: int = 10) -> dict:
    _ = top_k
    return _placeholder_payload(query)


@tool
def search_prefix(prefixes: List[str], limit: int = 50) -> dict:
    _ = limit
    return {
        "results": [],
        "count": 0,
        "prefixes": prefixes,
        "note": (
            "search_ideal is a scaffold in this phase. "
            "Concrete ideal retrieval behavior is not implemented yet."
        ),
    }

