"""StateOfTaskDashboardPlugin — composes per-turn state-of-task block.

Inject point: BeforeModelCallEvent. The plugin appends a user-role message to
`event.agent.messages` containing the rendered dashboard block. The first model
call (which carries the user's actual question) is skipped.

State sources:
  - turn counter: incremented on each model call
  - confidence history: parsed from assistant CoT records on AfterModelCallEvent
  - tool-call ledger: incremented on AfterToolCallEvent
  - long_plan progress: parsed from `sufficient_to_call_step_complete` flags
  - short_plan progress: read from a peer ShortPlanPlugin if available
  - advisory text: read from a peer ConfidenceAdvisoryPlugin if available
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
    BeforeModelCallEvent,
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
    """Compose and inject a per-turn state-of-task block."""

    name = "sana-dashboard"

    def __init__(self, *, max_tool_calls: int, history_window: int = 3) -> None:
        super().__init__()
        self._max_tool_calls = max(int(max_tool_calls), 1)
        self._history_window = max(int(history_window), 1)
        self._reset()

        # Peer-plugin references (set externally by sana_bundle when both are wired).
        self.short_plan_plugin: Optional[Any] = None
        self.confidence_advisory_plugin: Optional[Any] = None

    # ------------------------------------------------------------------
    # Lifecycle / state
    # ------------------------------------------------------------------

    def _reset(self) -> None:
        self._model_call_count = 0
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
    # Injection
    # ------------------------------------------------------------------

    @hook
    def on_before_model(self, event: BeforeModelCallEvent) -> None:
        self._model_call_count += 1
        if self._model_call_count <= 1:
            return  # First model call carries the user's actual question; no dashboard.

        block = self._render_block()
        try:
            event.agent.messages.append(
                {"role": "user", "content": [{"text": block}]}
            )
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning("Dashboard injection failed: %s", exc)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render_block(self) -> str:
        turn_label = f"{self._model_call_count} / {self._max_tool_calls}"
        history = list(self._confidence_history) or ["—"]
        confidence_str = ", ".join(history)

        long_plan_line = (
            f"long_plan: {self._step_completes} step(s) marked complete, "
            f"{self._step_incompletes} step(s) flagged incomplete"
        )
        short_plan_line: Optional[str] = None
        if self.short_plan_plugin is not None:
            short_plan_line = self.short_plan_plugin.describe_for_dashboard()

        evidence_line = f"evidence: {self._tool_call_count} tool call(s) consumed"

        advisory_line: Optional[str] = None
        if self.confidence_advisory_plugin is not None:
            advisory_text = self.confidence_advisory_plugin.consume_pending_advisory()
            if advisory_text:
                advisory_line = f"advisory: {advisory_text}"

        lines = [
            f"[State of Task — Turn {turn_label}]",
            long_plan_line,
        ]
        if short_plan_line:
            lines.append(short_plan_line)
        lines.append(f"confidence (last {self._history_window}): {confidence_str}")
        lines.append(evidence_line)
        if advisory_line:
            lines.append(advisory_line)
        return "\n".join(lines)


__all__ = ["StateOfTaskDashboardPlugin"]
