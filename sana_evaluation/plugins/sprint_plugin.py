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


def _cadence_guide_reason() -> str:
    return (
        "Pause tool calls. The k-turn sprint window is up. "
        "Call the sprint tool now with kind='cadence'. Include global_status, "
        "should_submit, potential_answer, answer_confidence, and short_forward_plan. "
        "Do not call data tools or submit_answer until the sprint tool succeeds."
    )


def _commitment_contract_reason(
    source: str,
    default_budget: int,
    *,
    action: str = "starting work on",
) -> str:
    return (
        f"Pause tool calls. You are {action} source `{source}`. "
        "This is a source commitment contract. Call the sprint tool now with "
        "kind='commitment_contract'. Include "
        f"current_source='{source}', commitment_goal, max_source_calls "
        f"(default {default_budget}), and plan_step. Keep the contract short. "
        "After the sprint tool succeeds, retry the source tool call you were about to make."
    )


def _pending_reason(previous_reason: Optional[str]) -> str:
    base = previous_reason or "Pause tool calls. A sprint reflection is still pending."
    return (
        f"{base} The sprint is still pending: call the sprint tool before any other tool."
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
    ) -> None:
        super().__init__()
        self._k = max(int(macro_reflection_k), 1)
        self._mode = sprint_mode
        self._commitment_budget_calls = max(int(commitment_budget_calls), 1)
        self.state = SprintState()
        self._tool_calls_since_reflection = 0
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

        if self._mode == "commitment":
            active_source = self.state.source_session.current_source if self.state.source_session else None
            requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
            if self.state.source_session is not None and requested_source == self.state.source_session.current_source:
                self.state.source_session.record_call(tool_name)
            return

        self._tool_calls_since_reflection += 1

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        if tool_name == _SPRINT_TOOL:
            return Proceed(reason="sprint tool satisfies pending reflection")
        if tool_name == "submit_answer" and self.state.pending_kind == "commitment_contract":
            return Proceed(reason="submit_answer bypasses source commitment contract")

        if self.state.pending_kind is not None:
            return Guide(reason=_pending_reason(self.state.pending_reason))

        if tool_name in _EXCLUDED_TOOLS:
            return Proceed(reason="administrative tool")

        if self._mode == "commitment":
            return self._steer_commitment(tool_use or {})
        return self._steer_cadence()

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
            return Guide(reason=reason)

        if requested_source != self.state.source_session.current_source:
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
            return Guide(reason=reason)

        if self.state.source_session.is_budget_exhausted():
            reason = self._compose_reason(
                _commitment_contract_reason(
                    self.state.source_session.current_source,
                    self._commitment_budget_calls,
                    action="renewing work on",
                )
            )
            self.state.pending_kind = "commitment_contract"
            self.state.pending_reason = reason
            self.state.pending_source = self.state.source_session.current_source
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
