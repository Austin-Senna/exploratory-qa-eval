"""SANA sprint tool — persist runtime reflection into the system prompt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from strands import tool
from strands.types.tools import ToolContext

from strands_evaluation.helper.prompt_sections import upsert_prompt_section


_VALID_KINDS = {"cadence", "commitment_contract", "commitment_reflection"}
_VALID_STATUS = {"ON_TRACK", "NEEDS_REPLAN", "ANSWER_READY"}
_VALID_CONFIDENCE = {"low", "medium", "high"}
_VALID_NEXT_ACTION = {"continue_source", "switch_source", "submit"}


@dataclass
class SprintState:
    """Shared state between SprintSteerHandler and the sprint tool."""

    pending_kind: Optional[str] = None
    pending_reason: Optional[str] = None
    pending_source: Optional[str] = None
    pending_switch_source: Optional[str] = None
    pending_requires_evidence: bool = False
    last_reflection: Optional[Dict[str, Any]] = None
    reflections_done: int = 0
    source_session: Optional[Any] = None


_STATE: Optional[SprintState] = None


def set_sprint_state(state: SprintState) -> None:
    global _STATE
    _STATE = state


def clear_sprint_state() -> None:
    global _STATE
    _STATE = None


def current_sprint_state() -> Optional[SprintState]:
    return _STATE


def _missing(record: Dict[str, Any], fields: List[str]) -> List[str]:
    out: List[str] = []
    for field in fields:
        value = record.get(field)
        if value is None or value == "":
            out.append(field)
    return out


def _coerce_positive_int(value: Any, *, default: Optional[int] = None) -> Optional[int]:
    try:
        out = int(value)
    except (TypeError, ValueError):
        return default
    if out <= 0:
        return default
    return out


def _source_parts(source: Any) -> set[str]:
    if not isinstance(source, str):
        return set()
    value = source.strip()
    if not value:
        return set()
    if value.startswith("multi:"):
        return {part.strip() for part in value[len("multi:") :].split(",") if part.strip()}
    return {value}


def _record_source_package(record: Dict[str, Any]) -> set[str]:
    package = _source_parts(record.get("current_source"))
    related = record.get("related_sources") or []
    if isinstance(related, list):
        for source in related:
            package.update(_source_parts(str(source).strip()))
    return package


def _record_covers_pending_source(state: SprintState, record: Dict[str, Any]) -> bool:
    pending_parts = _source_parts(state.pending_source)
    if not pending_parts:
        return True
    return pending_parts.issubset(_record_source_package(record))


def _record_matches_active_source_session(state: SprintState, record: Dict[str, Any]) -> bool:
    session = state.source_session
    if session is None:
        return False
    source = str(record.get("current_source") or "").strip()
    if not source:
        return False
    try:
        return bool(session.contains_source(source))
    except Exception:
        return False


def _validate_record(state: SprintState, record: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    kind = str(record.get("kind") or "").strip()
    if kind not in _VALID_KINDS:
        return [f"kind must be one of {sorted(_VALID_KINDS)}"]
    if state.pending_kind is not None and kind != state.pending_kind:
        errors.append(f"pending sprint kind is {state.pending_kind}; got {kind}")

    if kind == "cadence":
        missing = _missing(
            record,
            [
                "global_status",
                "should_submit",
                "answer_confidence",
                "settled_facts",
                "short_forward_plan",
            ],
        )
        if missing:
            errors.append("missing required field(s): " + ", ".join(missing))
        if record.get("global_status") not in _VALID_STATUS:
            errors.append(f"global_status must be one of {sorted(_VALID_STATUS)}")
        if record.get("answer_confidence") not in _VALID_CONFIDENCE:
            errors.append(f"answer_confidence must be one of {sorted(_VALID_CONFIDENCE)}")
        if not isinstance(record.get("settled_facts"), list):
            errors.append("settled_facts must be a list")
        if not isinstance(record.get("short_forward_plan"), list):
            errors.append("short_forward_plan must be a list")
    elif kind == "commitment_contract":
        if state.pending_kind != "commitment_contract":
            errors.append("commitment_contract requires a pending commitment_contract")
        missing = _missing(
            record,
            ["current_source", "commitment_goal", "max_source_calls", "plan_step"],
        )
        if missing:
            errors.append("missing required field(s): " + ", ".join(missing))
        if _coerce_positive_int(record.get("max_source_calls")) is None:
            errors.append("max_source_calls must be a positive integer")
        if "related_sources" in record and not isinstance(record.get("related_sources"), list):
            errors.append("related_sources must be a list")
        if not _record_covers_pending_source(state, record):
            errors.append(
                "commitment_contract does not cover pending source "
                f"{state.pending_source}"
            )
        if state.pending_requires_evidence:
            evidence_missing = _missing(record, ["evidence_gained", "remaining_gap"])
            if evidence_missing:
                errors.append(
                    "missing required renewal field(s): "
                    + ", ".join(evidence_missing)
                )
    else:
        if state.source_session is None:
            errors.append("commitment_reflection requires an active source session")
        missing = _missing(
            record,
            [
                "current_source",
                "calls_used",
                "commitment_goal",
                "evidence_gained",
                "remaining_gap",
                "next_action",
                "revised_budget",
            ],
        )
        if missing:
            errors.append("missing required field(s): " + ", ".join(missing))
        if record.get("next_action") not in _VALID_NEXT_ACTION:
            errors.append(f"next_action must be one of {sorted(_VALID_NEXT_ACTION)}")
        if _coerce_nonnegative_int(record.get("calls_used")) is None:
            errors.append("calls_used must be a non-negative integer")
        if _coerce_nonnegative_int(record.get("revised_budget")) is None:
            errors.append("revised_budget must be a non-negative integer")
        if state.source_session is not None and not _record_matches_active_source_session(state, record):
            errors.append("commitment_reflection current_source must be in the active source package")
    return errors


def _coerce_nonnegative_int(value: Any, *, default: Optional[int] = None) -> Optional[int]:
    try:
        out = int(value)
    except (TypeError, ValueError):
        return default
    if out < 0:
        return default
    return out


def _apply_record(state: SprintState, record: Dict[str, Any]) -> None:
    kind = record["kind"]
    state.last_reflection = record
    state.reflections_done += 1
    state.pending_kind = None
    state.pending_reason = None
    state.pending_requires_evidence = False

    if kind == "commitment_contract":
        from sana_evaluation.plugins.source_session import SourceSessionState

        budget = _coerce_positive_int(record.get("max_source_calls"), default=1) or 1
        state.source_session = SourceSessionState(
            current_source=str(record.get("current_source") or ""),
            commitment_goal=str(record.get("commitment_goal") or "unspecified"),
            max_source_calls=budget,
            plan_step=str(record.get("plan_step") or ""),
            success_condition=str(record.get("success_condition") or ""),
            related_sources=[
                str(source).strip()
                for source in (record.get("related_sources") or [])
                if str(source).strip()
            ],
        )
        state.pending_source = None
        state.pending_switch_source = None
        return

    if kind == "commitment_reflection":
        return


def _format_sprint_section(record: Dict[str, Any]) -> str:
    kind = str(record.get("kind") or "")
    lines = [f"kind: {kind}"]

    if kind == "cadence":
        plan = record.get("short_forward_plan") or []
        plan_text = "; ".join(str(item) for item in plan) if isinstance(plan, list) else str(plan)
        settled = record.get("settled_facts") or []
        settled_text = (
            "; ".join(str(item) for item in settled)
            if isinstance(settled, list) and settled
            else "none"
        )
        lines.extend(
            [
                f"global_status: {record.get('global_status')}",
                f"should_submit: {record.get('should_submit')}",
                f"potential_answer: {record.get('potential_answer') or 'null'}",
                f"answer_confidence: {record.get('answer_confidence')}",
                f"settled_facts: {settled_text}",
                f"short_forward_plan: {plan_text}",
            ]
        )
    elif kind == "commitment_contract":
        lines.extend(
            [
                f"current_source: {record.get('current_source')}",
                f"commitment_goal: {record.get('commitment_goal')}",
                f"max_source_calls: {record.get('max_source_calls')}",
                f"plan_step: {record.get('plan_step')}",
            ]
        )
        related = record.get("related_sources") or []
        if related:
            lines.append("related_sources: " + "; ".join(str(item) for item in related))
        if record.get("success_condition"):
            lines.append(f"success_condition: {record.get('success_condition')}")
        if record.get("evidence_gained"):
            lines.append(f"evidence_gained: {record.get('evidence_gained')}")
        if record.get("remaining_gap"):
            lines.append(f"remaining_gap: {record.get('remaining_gap')}")
    else:
        lines.extend(
            [
                f"current_source: {record.get('current_source')}",
                f"calls_used: {record.get('calls_used')}",
                f"commitment_goal: {record.get('commitment_goal')}",
                f"evidence_gained: {record.get('evidence_gained')}",
                f"remaining_gap: {record.get('remaining_gap')}",
                f"next_action: {record.get('next_action')}",
                f"revised_budget: {record.get('revised_budget')}",
            ]
        )
    return "\n".join(lines)


@tool(context=True)
def sprint(
    kind: str,
    tool_context: ToolContext,
    global_status: Optional[str] = None,
    should_submit: Optional[bool] = None,
    potential_answer: Optional[str] = None,
    answer_confidence: Optional[str] = None,
    settled_facts: Optional[List[str]] = None,
    short_forward_plan: Optional[List[str]] = None,
    current_source: Optional[str] = None,
    related_sources: Optional[List[str]] = None,
    commitment_goal: Optional[str] = None,
    max_source_calls: Optional[int] = None,
    plan_step: Optional[str] = None,
    success_condition: Optional[str] = None,
    calls_used: Optional[int] = None,
    evidence_gained: Optional[str] = None,
    remaining_gap: Optional[str] = None,
    next_action: Optional[str] = None,
    revised_budget: Optional[int] = None,
) -> str:
    """Record the current sprint reflection or source commitment.

    Use `kind="cadence"` for ordinary k-turn sprint reflection,
    `kind="commitment_contract"` before starting or renewing a dataset/source
    session, and `kind="commitment_reflection"` as an optional source-session
    note.
    """

    state = _STATE
    if state is None:
        return "Sprint not recorded: sprint runtime state is not initialized."

    record: Dict[str, Any] = {
        "kind": kind,
        "global_status": global_status,
        "should_submit": should_submit,
        "potential_answer": potential_answer,
        "answer_confidence": answer_confidence,
        "settled_facts": settled_facts,
        "short_forward_plan": short_forward_plan,
        "current_source": current_source,
        "related_sources": related_sources,
        "commitment_goal": commitment_goal,
        "max_source_calls": max_source_calls,
        "plan_step": plan_step,
        "success_condition": success_condition,
        "calls_used": calls_used,
        "evidence_gained": evidence_gained,
        "remaining_gap": remaining_gap,
        "next_action": next_action,
        "revised_budget": revised_budget,
    }
    record = {key: value for key, value in record.items() if value is not None}

    errors = _validate_record(state, record)
    if errors:
        return "Sprint not recorded: " + "; ".join(errors)

    _apply_record(state, record)
    agent = tool_context.agent
    agent.system_prompt = upsert_prompt_section(
        agent.system_prompt,
        "CURRENT SPRINT",
        _format_sprint_section(record),
    )
    return "Sprint recorded."


__all__ = [
    "SprintState",
    "clear_sprint_state",
    "current_sprint_state",
    "set_sprint_state",
    "sprint",
]
