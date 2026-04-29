"""ShortPlanSteerHandler — steering-based k-turn sprint reflection.

Counts non-administrative tool calls. On the k-th call, returns a Guide action
that cancels the tool and instructs the agent to emit a macro-reflection JSON
on its next response. Parses the JSON from the AfterModelCallEvent that
follows. Writes parsed reflection into SanaSharedState.

The Guide pattern (vs. injecting a user-role message) means we don't burn an
extra turn on the reflection — the cancelled tool's slot becomes the
reflection slot.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional

from strands.hooks import AfterModelCallEvent, AfterToolCallEvent, AgentInitializedEvent
from strands.plugins import hook
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

from sana_evaluation.plugins.source_session import SourceSessionState, source_from_tool_use

logger = logging.getLogger(__name__)


_REFLECTION_GUIDE_REASON = (
    "Pause tool calls. The k-turn sprint window is up. "
    "Respond with ONE JSON object only — no tool calls on this response. "
    "Schema: "
    '{"global_status": "ON_TRACK" | "NEEDS_REPLAN" | "ANSWER_READY", '
    '"should_submit": true | false, '
    '"potential_answer": "<best current candidate answer, or null>", '
    '"answer_confidence": "low" | "medium" | "high", '
    '"short_forward_plan": ['
    '"turns 1-2: <actions>", "turns 3-5: <actions>"]}. '
    "Plan entries cover the next k turns total. After the JSON is parsed, you resume tool calls normally."
)

_EXCLUDED_TOOLS = {
    "plan",
    "plan_ideal",
    "skills",
    "summarize_context",
    "submit_answer",
}

_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _source_contract_guide_reason(source: str, default_budget: int) -> str:
    return (
        f"Pause tool calls. You are starting work on source `{source}`. "
        "Respond with ONE JSON object only - no tool calls on this response. "
        "This is a source budget contract. Schema: "
        f'{{"current_source": "{source}", '
        '"commitment_goal": "<what you will learn from this source>", '
        f'"max_source_calls": <positive integer, default {default_budget}>, '
        '"success_condition": "<what evidence means this source commitment is complete>"}. '
        "After the JSON is parsed, retry the source tool call you were about to make."
    )


def _source_reflection_guide_reason(
    *,
    current_source: str,
    next_source: str,
    switch_pending: bool,
) -> str:
    suffix = " Reflect before switching sources." if switch_pending else ""
    return (
        "Pause tool calls. The source-session budget is exhausted or a source switch "
        f"is about to happen. Current source: `{current_source}`. "
        f"Requested next source: `{next_source}`. "
        "Respond with ONE JSON object only - no tool calls on this response. "
        "Schema: "
        f'{{"current_source": "{current_source}", '
        '"calls_used": <integer>, '
        '"commitment_goal": "<current source goal>", '
        '"evidence_gained": "<what this source yielded>", '
        '"remaining_gap": "<what is still missing>", '
        '"next_action": "continue_source" | "switch_source" | "submit", '
        '"revised_budget": <integer additional calls if continuing, else 0>}. '
        "After the JSON is parsed, continue according to next_action."
        f"{suffix}"
    )


def _extract_assistant_text(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    blocks = message.get("content", [])
    if not isinstance(blocks, list):
        return ""
    parts: List[str] = []
    for block in blocks:
        if isinstance(block, dict) and isinstance(block.get("text"), str):
            parts.append(block["text"])
    return "\n".join(parts)


class ShortPlanSteerHandler(SteeringHandler):
    """K-turn sprint reflection via Strands SteeringHandler.Guide pattern."""

    name = "sana-short-plan-steer"

    def __init__(
        self,
        *,
        macro_reflection_k: int,
        short_plan_mode: str = "cadence",
        source_budget_calls: int = 3,
    ) -> None:
        super().__init__()
        self._k = max(int(macro_reflection_k), 1)
        self._mode = short_plan_mode
        self._source_budget_calls = max(int(source_budget_calls), 1)
        self._reset()

        # Peer-plugin reference (set externally by sana_bundle when both are wired).
        # When set, render_block() output is prepended to the reflection Guide reason.
        self.dashboard_plugin: Optional[Any] = None

    def _reset(self) -> None:
        self._tool_calls_since_reflection = 0
        self._awaiting_reflection_response = False
        self._awaiting_contract_response = False
        self._pending_contract_source: Optional[str] = None
        self._pending_switch_source: Optional[str] = None
        self._reflections_done = 0
        self.last_reflection: Optional[Dict[str, Any]] = None
        self.source_session: Optional[SourceSessionState] = None

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    # ------------------------------------------------------------------
    # Counting
    # ------------------------------------------------------------------

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_use = getattr(event, "tool_use", {}) or {}
        tool_name = tool_use.get("name", "")
        if tool_name in _EXCLUDED_TOOLS:
            return
        if self._mode == "source_budget":
            active_source = self.source_session.current_source if self.source_session else None
            requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
            if self.source_session is not None and requested_source == self.source_session.current_source:
                self.source_session.record_call(tool_name)
            return
        self._tool_calls_since_reflection += 1

    # ------------------------------------------------------------------
    # Steering: cancel the k-th tool with a Guide action
    # ------------------------------------------------------------------

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        if tool_name in _EXCLUDED_TOOLS:
            return Proceed(reason="administrative tool — never gated by reflection")
        if self._mode == "source_budget":
            return self._steer_source_budget(tool_use or {})
        return self._steer_cadence(tool_name)

    def _steer_cadence(self, tool_name: str) -> ToolSteeringAction:
        if (
            self._tool_calls_since_reflection >= self._k
            and not self._awaiting_reflection_response
        ):
            self._awaiting_reflection_response = True
            self._tool_calls_since_reflection = 0
            return Guide(reason=self._compose_reason(_REFLECTION_GUIDE_REASON))

        return Proceed(reason="within sprint window")

    def _steer_source_budget(self, tool_use: Dict[str, Any]) -> ToolSteeringAction:
        if self._awaiting_contract_response or self._awaiting_reflection_response:
            return Proceed(reason="awaiting model response to pending source-budget instruction")

        active_source = self.source_session.current_source if self.source_session else None
        requested_source = source_from_tool_use(tool_use, fallback_source=active_source)
        if requested_source is None:
            return Proceed(reason="tool has no source-session identity")

        if self.source_session is None:
            self._awaiting_contract_response = True
            self._pending_contract_source = requested_source
            return Guide(
                reason=self._compose_reason(
                    _source_contract_guide_reason(
                        requested_source,
                        self._source_budget_calls,
                    )
                )
            )

        if requested_source != self.source_session.current_source:
            self._awaiting_reflection_response = True
            self._pending_switch_source = requested_source
            return Guide(
                reason=self._compose_reason(
                    _source_reflection_guide_reason(
                        current_source=self.source_session.current_source,
                        next_source=requested_source,
                        switch_pending=True,
                    )
                )
            )

        if self.source_session.is_budget_exhausted():
            self._awaiting_reflection_response = True
            return Guide(
                reason=self._compose_reason(
                    _source_reflection_guide_reason(
                        current_source=self.source_session.current_source,
                        next_source=self.source_session.current_source,
                        switch_pending=False,
                    )
                )
            )

        return Proceed(reason="within source-session budget")

    def _compose_reason(self, instruction: str) -> str:
        if self.dashboard_plugin is None:
            return instruction
        try:
            return self.dashboard_plugin.render_block() + "\n\n" + instruction
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning("Dashboard render_block failed: %s", exc)
            return instruction

    # ------------------------------------------------------------------
    # Parse reflection JSON from the model's response
    # ------------------------------------------------------------------

    @hook
    def on_after_model(self, event: AfterModelCallEvent) -> None:
        if not self._awaiting_reflection_response and not self._awaiting_contract_response:
            return
        if event.exception is not None:
            self._awaiting_reflection_response = False
            self._awaiting_contract_response = False
            return
        stop_response = event.stop_response
        if stop_response is None:
            self._awaiting_reflection_response = False
            self._awaiting_contract_response = False
            return
        text = _extract_assistant_text(stop_response.message)
        if not text:
            self._awaiting_reflection_response = False
            self._awaiting_contract_response = False
            return
        if self._awaiting_contract_response:
            self._handle_contract_response(text)
            return
        self._handle_reflection_response(text)

    def _handle_contract_response(self, text: str) -> None:
        parsed = self._parse_reflection_json(text)
        self._awaiting_contract_response = False
        if parsed is None:
            logger.warning("Source budget contract did not contain parseable JSON.")
            return
        source = str(parsed.get("current_source") or self._pending_contract_source or "").strip()
        if not source:
            logger.warning("Source budget contract missing current_source.")
            return
        budget = parsed.get("max_source_calls", self._source_budget_calls)
        try:
            budget_int = max(int(budget), 1)
        except (TypeError, ValueError):
            budget_int = self._source_budget_calls
        self.source_session = SourceSessionState(
            current_source=source,
            commitment_goal=str(parsed.get("commitment_goal") or "unspecified"),
            max_source_calls=budget_int,
            success_condition=str(parsed.get("success_condition") or "unspecified"),
        )
        self._pending_contract_source = None

    def _handle_reflection_response(self, text: str) -> None:
        parsed = self._parse_reflection_json(text)
        self.last_reflection = parsed
        self._awaiting_reflection_response = False
        if parsed is None:
            logger.warning("Macro-reflection response did not contain parseable JSON.")
            return
        self._reflections_done += 1
        if self._mode != "source_budget" or self.source_session is None:
            return
        next_action = str(parsed.get("next_action") or "").strip()
        if next_action == "continue_source":
            revised_budget = parsed.get("revised_budget", 0)
            try:
                additional = max(int(revised_budget), 0)
            except (TypeError, ValueError):
                additional = 0
            if additional > 0:
                self.source_session.max_source_calls = self.source_session.calls_used + additional
        elif next_action in {"switch_source", "submit"}:
            self.source_session = None
        self._pending_switch_source = None

    def _parse_reflection_json(self, text: str) -> Optional[Dict[str, Any]]:
        match = _JSON_OBJECT_RE.search(text)
        if not match:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    # ------------------------------------------------------------------
    # Read access for the dashboard
    # ------------------------------------------------------------------

    def describe_for_dashboard(self) -> str:
        last = self.last_reflection
        if last is None:
            return "short_plan: (no reflection yet)"
        plan = last.get("short_forward_plan") or []
        head = plan[0] if plan else "—"
        status = last.get("global_status", "—")
        lines = [
            f"short_plan: step 1/{len(plan) if plan else 0} ({head}) "
            f"| status: {status} | reflections: {self._reflections_done}"
        ]
        answer = last.get("potential_answer")
        answer_conf = last.get("answer_confidence")
        if answer or answer_conf:
            lines.append(
                f"candidate_answer: {answer or '—'} "
                f"| answer_confidence: {answer_conf or '—'}"
            )
        if self.source_session is not None:
            lines.append(self.source_session.describe())
        return "\n".join(lines)


__all__ = ["ShortPlanSteerHandler"]
