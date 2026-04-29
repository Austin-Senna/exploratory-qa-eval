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
    ) -> None:
        super().__init__()
        self._k = max(int(macro_reflection_k), 1)
        self._reset()

        # Peer-plugin reference (set externally by sana_bundle when both are wired).
        # When set, render_block() output is prepended to the reflection Guide reason.
        self.dashboard_plugin: Optional[Any] = None

    def _reset(self) -> None:
        self._tool_calls_since_reflection = 0
        self._awaiting_reflection_response = False
        self._reflections_done = 0
        self.last_reflection: Optional[Dict[str, Any]] = None

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    # ------------------------------------------------------------------
    # Counting
    # ------------------------------------------------------------------

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = (getattr(event, "tool_use", {}) or {}).get("name", "")
        if tool_name in _EXCLUDED_TOOLS:
            return
        self._tool_calls_since_reflection += 1

    # ------------------------------------------------------------------
    # Steering: cancel the k-th tool with a Guide action
    # ------------------------------------------------------------------

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        if tool_name in _EXCLUDED_TOOLS:
            return Proceed(reason="administrative tool — never gated by reflection")

        if (
            self._tool_calls_since_reflection >= self._k
            and not self._awaiting_reflection_response
        ):
            self._awaiting_reflection_response = True
            self._tool_calls_since_reflection = 0
            reason = _REFLECTION_GUIDE_REASON
            if self.dashboard_plugin is not None:
                try:
                    reason = self.dashboard_plugin.render_block() + "\n\n" + reason
                except Exception as exc:  # pragma: no cover — defensive
                    logger.warning("Dashboard render_block failed: %s", exc)
            return Guide(reason=reason)

        return Proceed(reason="within sprint window")

    # ------------------------------------------------------------------
    # Parse reflection JSON from the model's response
    # ------------------------------------------------------------------

    @hook
    def on_after_model(self, event: AfterModelCallEvent) -> None:
        if not self._awaiting_reflection_response:
            return
        if event.exception is not None:
            self._awaiting_reflection_response = False
            return
        stop_response = event.stop_response
        if stop_response is None:
            self._awaiting_reflection_response = False
            return
        text = _extract_assistant_text(stop_response.message)
        if not text:
            self._awaiting_reflection_response = False
            return
        parsed = self._parse_reflection_json(text)
        if parsed is None:
            logger.warning("Macro-reflection response did not contain parseable JSON.")
            self._awaiting_reflection_response = False
            return
        self.last_reflection = parsed
        self._awaiting_reflection_response = False
        self._reflections_done += 1

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
        return "\n".join(lines)


__all__ = ["ShortPlanSteerHandler"]
