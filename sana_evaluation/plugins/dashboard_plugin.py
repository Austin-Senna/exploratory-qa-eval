"""StateOfTaskDashboardPlugin — observes runtime state, renders on demand.

The plugin tracks turn count, confidence trend, tool-call ledger, and plan-step
completion via Strands hooks. It does NOT inject any messages on its own.
`render_block()` returns the formatted readout for a peer plugin (currently
`SprintSteerHandler`) to surface at reflection time.

State sources:
  - confidence history: parsed from assistant CoT records on AfterModelCallEvent
  - tool-call ledger: incremented on AfterToolCallEvent
  - long_plan progress: parsed from `sufficient_to_call_step_complete` flags
  - sprint progress: read from a peer SprintSteerHandler if available
    (its describe_for_dashboard() returns the active step + last reflection's
    candidate_answer + answer_confidence)
"""

from __future__ import annotations

import logging
import re
from collections import deque
from typing import Any, Deque, List, Optional

from strands import Plugin
from strands.hooks import (
    AfterModelCallEvent,
    AfterToolCallEvent,
    AgentInitializedEvent,
)
from strands.plugins import hook

logger = logging.getLogger(__name__)


_CONFIDENCE_RE = re.compile(r"^\s*confidence\s*:\s*(low|medium|high)\s*$", re.IGNORECASE | re.MULTILINE)
_STEP_COMPLETE_RE = re.compile(
    r"^\s*sufficient_to_call_step_complete\s*:\s*(true|false)\s*$",
    re.IGNORECASE | re.MULTILINE,
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


class StateOfTaskDashboardPlugin(Plugin):
    """Observe runtime state; render a state-of-task block on demand."""

    name = "sana-dashboard"

    def __init__(self, *, max_tool_calls: int, history_window: int = 3) -> None:
        super().__init__()
        self._max_tool_calls = max(int(max_tool_calls), 1)
        self._history_window = max(int(history_window), 1)
        self._reset()

        # Peer-plugin reference (set externally by sana_bundle when both are wired).
        self.sprint_plugin: Optional[Any] = None

    # ------------------------------------------------------------------
    # Lifecycle / state
    # ------------------------------------------------------------------

    def _reset(self) -> None:
        self._tool_call_count = 0
        self._step_completes = 0
        self._step_incompletes = 0
        self._confidence_history: Deque[str] = deque(maxlen=self._history_window)

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    # ------------------------------------------------------------------
    # State update hooks
    # ------------------------------------------------------------------

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = (getattr(event, "tool_use", {}) or {}).get("name", "")
        if tool_name and tool_name not in {"plan", "plan_ideal", "skills", "summarize_context"}:
            self._tool_call_count += 1

    @hook
    def on_after_model(self, event: AfterModelCallEvent) -> None:
        if event.exception is not None:
            return
        stop_response = event.stop_response
        if stop_response is None:
            return
        text = _extract_assistant_text(stop_response.message)
        if not text:
            return
        for match in _CONFIDENCE_RE.finditer(text):
            self._confidence_history.append(match.group(1).lower())
        for match in _STEP_COMPLETE_RE.finditer(text):
            if match.group(1).lower() == "true":
                self._step_completes += 1
            else:
                self._step_incompletes += 1

    # ------------------------------------------------------------------
    # Rendering (called by peer plugin at reflection time)
    # ------------------------------------------------------------------

    def render_block(self) -> str:
        """Compose and return the state-of-task readout as a string.

        Caller is responsible for surfacing it (typically prepended to the
            SprintSteerHandler reflection Guide reason).
        """
        turn_label = f"{self._tool_call_count} / {self._max_tool_calls}"
        history = list(self._confidence_history) or ["—"]
        confidence_str = ", ".join(history)

        long_plan_line = (
            f"long_plan: {self._step_completes} step(s) marked complete, "
            f"{self._step_incompletes} step(s) flagged incomplete"
        )
        sprint_line: Optional[str] = None
        if self.sprint_plugin is not None:
            sprint_line = self.sprint_plugin.describe_for_dashboard()

        evidence_line = f"evidence: {self._tool_call_count} tool call(s) consumed"

        lines = [
            f"[State of Task — Turn {turn_label}]",
            long_plan_line,
        ]
        if sprint_line:
            lines.append(sprint_line)
        lines.append(f"confidence (last {self._history_window}): {confidence_str}")
        lines.append(evidence_line)
        return "\n".join(lines)


__all__ = ["StateOfTaskDashboardPlugin"]
