"""SANA CoT tool - record runtime-enforced tool-use progress records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from strands import tool
from strands.types.tools import ToolContext


_VALID_KINDS = {"pre_tool", "post_tool"}
_VALID_CONFIDENCE = {"low", "medium", "high"}


@dataclass
class CoTState:
    """Shared state between CoTSteerHandler and the cot tool."""

    pending_kind: Optional[str] = None
    pending_tool: Optional[str] = None
    pending_reason: Optional[str] = None
    awaiting_tool: Optional[str] = None
    last_pre_record: Optional[Dict[str, Any]] = None
    last_post_record: Optional[Dict[str, Any]] = None
    records_done: int = 0


_STATE: Optional[CoTState] = None


def set_cot_state(state: CoTState) -> None:
    global _STATE
    _STATE = state


def clear_cot_state() -> None:
    global _STATE
    _STATE = None


def current_cot_state() -> Optional[CoTState]:
    return _STATE


def _missing(record: Dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for field in fields:
        value = record.get(field)
        if value is None or value == "":
            missing.append(field)
    return missing


def _validate_record(state: CoTState, record: Dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = str(record.get("kind") or "").strip()
    if kind not in _VALID_KINDS:
        return [f"kind must be one of {sorted(_VALID_KINDS)}"]
    if state.pending_kind is not None and kind != state.pending_kind:
        errors.append(f"pending CoT kind is {state.pending_kind}; got {kind}")

    if kind == "pre_tool":
        missing = _missing(record, ("intended_tool", "current_step", "intent", "confidence"))
        if missing:
            errors.append("missing required field(s): " + ", ".join(missing))
        intended_tool = str(record.get("intended_tool") or "").strip()
        if state.pending_tool is not None and intended_tool != state.pending_tool:
            errors.append(f"pending intended tool is {state.pending_tool}; got {intended_tool}")
        if record.get("confidence") not in _VALID_CONFIDENCE:
            errors.append(f"confidence must be one of {sorted(_VALID_CONFIDENCE)}")
    else:
        missing = _missing(
            record,
            (
                "completed_tool",
                "current_step",
                "tool_result_summary",
                "next_step",
                "sufficient_to_call_step_complete",
                "remaining_gap_if_not_complete",
            ),
        )
        if missing:
            errors.append("missing required field(s): " + ", ".join(missing))
        completed_tool = str(record.get("completed_tool") or "").strip()
        if state.pending_tool is None:
            errors.append("post_tool requires a pending completed tool")
        elif completed_tool != state.pending_tool:
            errors.append(f"pending completed tool is {state.pending_tool}; got {completed_tool}")
        if not isinstance(record.get("sufficient_to_call_step_complete"), bool):
            errors.append("sufficient_to_call_step_complete must be a boolean")
    return errors


def _apply_record(state: CoTState, record: Dict[str, Any]) -> None:
    kind = record["kind"]
    state.records_done += 1
    state.pending_kind = None
    state.pending_reason = None

    if kind == "pre_tool":
        state.last_pre_record = record
        state.awaiting_tool = str(record.get("intended_tool") or "")
        state.pending_tool = None
        return

    state.last_post_record = record
    state.awaiting_tool = None
    state.pending_tool = None


@tool(context=True)
def cot(
    kind: str,
    tool_context: ToolContext,
    intended_tool: Optional[str] = None,
    current_step: Optional[str] = None,
    intent: Optional[str] = None,
    confidence: Optional[str] = None,
    completed_tool: Optional[str] = None,
    tool_result_summary: Optional[str] = None,
    next_step: Optional[str] = None,
    sufficient_to_call_step_complete: Optional[bool] = None,
    remaining_gap_if_not_complete: Optional[str] = None,
) -> str:
    """Record a structured pre-tool or post-tool progress note."""

    state = _STATE
    if state is None:
        return "CoT not recorded: CoT runtime state is not initialized."

    record: Dict[str, Any] = {
        "kind": kind,
        "intended_tool": intended_tool,
        "current_step": current_step,
        "intent": intent,
        "confidence": confidence,
        "completed_tool": completed_tool,
        "tool_result_summary": tool_result_summary,
        "next_step": next_step,
        "sufficient_to_call_step_complete": sufficient_to_call_step_complete,
        "remaining_gap_if_not_complete": remaining_gap_if_not_complete,
    }
    record = {key: value for key, value in record.items() if value is not None}

    errors = _validate_record(state, record)
    if errors:
        return "CoT not recorded: " + "; ".join(errors)

    _apply_record(state, record)
    return "CoT recorded."


__all__ = [
    "CoTState",
    "clear_cot_state",
    "cot",
    "current_cot_state",
    "set_cot_state",
]
