"""SprintSteerHandler — tool-enforced sprint reflection and commitment control."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from strands.hooks import AfterToolCallEvent, AgentInitializedEvent
from strands.plugins import hook
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

from sana_evaluation.plugins.source_session import source_from_tool_use
from sana_evaluation.tools.sprint_tool import SprintState, set_sprint_state

logger = logging.getLogger(__name__)


_SPRINT_TOOL = "sprint"

_EXCLUDED_TOOLS = {
    _SPRINT_TOOL,
    "plan",
    "plan_ideal",
    "skills",
}

_FINAL_BUDGET_THRESHOLD = 2
_FINAL_INACTIVE = "inactive"
_FINAL_AWAITING_LOOKUP = "awaiting_lookup"
_FINAL_LOCKED = "locked"


def _cadence_guide_reason() -> str:
    return (
        "Pause tool calls. The k-turn sprint window is up. "
        "Call the sprint tool now with kind='cadence'. Include global_status, "
        "should_submit, potential_answer, answer_confidence, settled_facts, "
        "and short_forward_plan. "
        "Do not call data tools or submit_answer until the sprint tool succeeds."
    )


def _commitment_contract_reason(
    source: str,
    default_budget: int,
    *,
    action: str = "starting work on",
    require_evidence: bool = False,
) -> str:
    evidence_text = (
        " Also include evidence_gained and remaining_gap to justify renewal."
        if require_evidence
        else ""
    )
    return (
        f"Pause tool calls. You are {action} source `{source}`. "
        "This is a source commitment contract. Call the sprint tool now with "
        "kind='commitment_contract'. Include "
        f"current_source='{source}', commitment_goal, max_source_calls "
        f"(default {default_budget}), and plan_step. Keep the contract short. "
        f"{evidence_text} After the sprint tool succeeds, retry the source tool "
        "call you were about to make."
    )


def _pending_reason(previous_reason: Optional[str]) -> str:
    base = previous_reason or "Pause tool calls. A sprint reflection is still pending."
    return (
        f"{base} The sprint is still pending: call the sprint tool before any other tool."
    )


def _final_budget_warning_reason(tool_calls_left: int) -> str:
    return (
        f"Pause tool calls. Final budget: {tool_calls_left} counted tool call(s) left. "
        "If the answer is ready, call submit_answer now. Otherwise choose exactly "
        "one final highest-value lookup; after that lookup, submit_answer is the "
        "only allowed non-administrative action."
    )


def _final_budget_locked_reason() -> str:
    return (
        "Pause tool calls. Final budget is locked after the one final lookup. "
        "Do not call more data/source tools; call submit_answer with the best "
        "answer supported by the current evidence."
    )


class SprintSteerHandler(SteeringHandler):
    """Runtime controller for sprint cadence and source commitment mode."""

    name = "sana-sprint-steer"

    def __init__(
        self,
        *,
        macro_reflection_k: int,
        sprint_mode: str = "cadence",
        commitment_budget_calls: int = 3,
        max_tool_calls: int = 30,
    ) -> None:
        super().__init__()
        self._k = max(int(macro_reflection_k), 1)
        self._mode = sprint_mode
        self._commitment_budget_calls = max(int(commitment_budget_calls), 1)
        self._max_tool_calls = max(int(max_tool_calls), 1)
        self.state = SprintState()
        self._tool_calls_since_reflection = 0
        self._counted_tool_calls = 0
        self._final_budget_state = _FINAL_INACTIVE
        self.dashboard_plugin: Optional[Any] = None
        set_sprint_state(self.state)

    @property
    def source_session(self):
        return self.state.source_session

    @property
    def last_reflection(self):
        return self.state.last_reflection

    def _reset(self) -> None:
        self.state = SprintState()
        self._tool_calls_since_reflection = 0
        self._counted_tool_calls = 0
        self._final_budget_state = _FINAL_INACTIVE
        set_sprint_state(self.state)

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_use = getattr(event, "tool_use", {}) or {}
        tool_name = tool_use.get("name", "")
        if tool_name in _EXCLUDED_TOOLS or tool_name == "submit_answer":
            return
        self._counted_tool_calls += 1
        if self._final_budget_state == _FINAL_AWAITING_LOOKUP:
            self._final_budget_state = _FINAL_LOCKED

        if self._mode == "commitment":
            active_source = self.state.source_session.current_source if self.state.source_session else None
            requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
            if (
                self.state.source_session is not None
                and self.state.source_session.contains_source(requested_source)
            ):
                self.state.source_session.record_call(tool_name)
            return

        self._tool_calls_since_reflection += 1

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        if tool_name == _SPRINT_TOOL:
            return Proceed(reason="sprint tool satisfies pending reflection")
        if tool_name in _EXCLUDED_TOOLS:
            return Proceed(reason="administrative tool")
        if tool_name == "submit_answer" and self._is_in_final_budget():
            return Proceed(reason="submit_answer allowed by final-budget gate")
        if tool_name == "submit_answer" and self.state.pending_kind == "commitment_contract":
            return Proceed(reason="submit_answer bypasses source commitment contract")

        final_action = self._steer_final_budget()
        if final_action is not None:
            return final_action

        if self.state.pending_kind is not None:
            return Guide(reason=_pending_reason(self.state.pending_reason))

        if self._mode == "commitment":
            return self._steer_commitment(tool_use or {})
        return self._steer_cadence()

    def _tool_calls_left(self) -> int:
        return max(self._max_tool_calls - self._counted_tool_calls, 0)

    def _is_in_final_budget(self) -> bool:
        return (
            self._final_budget_state != _FINAL_INACTIVE
            or self._tool_calls_left() <= _FINAL_BUDGET_THRESHOLD
        )

    def _steer_final_budget(self) -> Optional[ToolSteeringAction]:
        if self._final_budget_state == _FINAL_LOCKED:
            return Guide(reason=self._compose_reason(_final_budget_locked_reason()))
        if self._final_budget_state == _FINAL_AWAITING_LOOKUP:
            return Proceed(reason="one final lookup allowed by final-budget gate")
        if self._tool_calls_left() <= _FINAL_BUDGET_THRESHOLD:
            self._final_budget_state = _FINAL_AWAITING_LOOKUP
            return Guide(
                reason=self._compose_reason(
                    _final_budget_warning_reason(self._tool_calls_left())
                )
            )
        return None

    def _steer_cadence(self) -> ToolSteeringAction:
        if self._tool_calls_since_reflection >= self._k:
            self._tool_calls_since_reflection = 0
            reason = self._compose_reason(_cadence_guide_reason())
            self.state.pending_kind = "cadence"
            self.state.pending_reason = reason
            return Guide(reason=reason)
        return Proceed(reason="within sprint window")

    def _steer_commitment(self, tool_use: Dict[str, Any]) -> ToolSteeringAction:
        active_source = self.state.source_session.current_source if self.state.source_session else None
        requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
        if requested_source is None:
            return Proceed(reason="tool has no source-session identity")

        if self.state.source_session is None:
            reason = self._compose_reason(
                _commitment_contract_reason(requested_source, self._commitment_budget_calls)
            )
            self.state.pending_kind = "commitment_contract"
            self.state.pending_reason = reason
            self.state.pending_source = requested_source
            self.state.pending_requires_evidence = False
            return Guide(reason=reason)

        if not self.state.source_session.contains_source(requested_source):
            reason = self._compose_reason(
                _commitment_contract_reason(
                    requested_source,
                    self._commitment_budget_calls,
                    action=(
                        "switching from source "
                        f"`{self.state.source_session.current_source}` to"
                    ),
                )
            )
            self.state.pending_kind = "commitment_contract"
            self.state.pending_reason = reason
            self.state.pending_source = requested_source
            self.state.pending_switch_source = requested_source
            self.state.pending_requires_evidence = False
            return Guide(reason=reason)

        if self.state.source_session.is_budget_exhausted():
            reason = self._compose_reason(
                _commitment_contract_reason(
                    self.state.source_session.current_source,
                    self._commitment_budget_calls,
                    action="renewing work on",
                    require_evidence=True,
                )
            )
            self.state.pending_kind = "commitment_contract"
            self.state.pending_reason = reason
            self.state.pending_source = self.state.source_session.current_source
            self.state.pending_requires_evidence = True
            return Guide(reason=reason)

        return Proceed(reason="within source-session budget")

    def _compose_reason(self, instruction: str) -> str:
        if self.dashboard_plugin is None:
            return instruction
        try:
            return self.dashboard_plugin.render_block() + "\n\n" + instruction
        except Exception as exc:  # pragma: no cover
            logger.warning("Dashboard render_block failed: %s", exc)
            return instruction

    def describe_for_dashboard(self) -> str:
        last = self.state.last_reflection
        lines = []
        if last is not None and last.get("kind") == "cadence":
            plan = last.get("short_forward_plan") or []
            head = plan[0] if plan else "-"
            lines.append(f"sprint_status: {last.get('global_status', '-')} | next: {head}")
            answer = last.get("potential_answer")
            answer_conf = last.get("answer_confidence")
            if answer or answer_conf:
                lines.append(
                    f"candidate_answer: {answer or '-'} "
                    f"| answer_confidence: {answer_conf or '-'}"
                )
        if self.state.source_session is not None:
            lines.append(self.state.source_session.describe())
        return "\n".join(lines)


__all__ = ["SprintSteerHandler"]
