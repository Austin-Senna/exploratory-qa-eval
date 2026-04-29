"""ConfidenceAdvisoryPlugin — parses self-reported confidence and emits soft advisories.

Soft only: no tool calls are blocked. The advisory either becomes part of the
state-of-task dashboard (when StateOfTaskDashboardPlugin is also active) or is
appended as its own user-role message.
"""

from __future__ import annotations

import logging
import re
from collections import deque
from typing import Any, Deque, List, Optional

from strands import Plugin
from strands.hooks import (
    AfterModelCallEvent,
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


class ConfidenceAdvisoryPlugin(Plugin):
    """Watch agent confidence and emit soft advisories."""

    name = "sana-confidence-advisory"

    def __init__(
        self,
        *,
        search_tool: str,
        history_window: int = 3,
        low_streak_threshold: int = 3,
        dashboard_active: bool = False,
    ) -> None:
        super().__init__()
        self._search_tool = search_tool
        self._history_window = max(int(history_window), 1)
        self._low_streak_threshold = max(int(low_streak_threshold), 1)
        self._dashboard_active = bool(dashboard_active)
        self._reset()

    def _reset(self) -> None:
        self._confidence_history: Deque[str] = deque(maxlen=self._history_window)
        self._step_complete_history: Deque[bool] = deque(maxlen=self._history_window)
        self._pending_advisory: Optional[str] = None
        self._last_emitted_signature: Optional[str] = None

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    # ------------------------------------------------------------------
    # Read CoT records from assistant text
    # ------------------------------------------------------------------

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

        last_confidence: Optional[str] = None
        for match in _CONFIDENCE_RE.finditer(text):
            last_confidence = match.group(1).lower()
        if last_confidence is not None:
            self._confidence_history.append(last_confidence)

        last_complete: Optional[bool] = None
        for match in _STEP_COMPLETE_RE.finditer(text):
            last_complete = (match.group(1).lower() == "true")
        if last_complete is not None:
            self._step_complete_history.append(last_complete)

        self._maybe_compose_advisory()

    # ------------------------------------------------------------------
    # Advisory composition
    # ------------------------------------------------------------------

    def _low_streak(self) -> int:
        streak = 0
        for value in reversed(self._confidence_history):
            if value == "low":
                streak += 1
            else:
                break
        return streak

    def _high_but_incomplete(self) -> bool:
        if not self._confidence_history or not self._step_complete_history:
            return False
        if self._confidence_history[-1] != "high":
            return False
        if not self._step_complete_history:
            return False
        return self._step_complete_history[-1] is False

    def _maybe_compose_advisory(self) -> None:
        signature: Optional[str] = None
        text: Optional[str] = None

        low_streak = self._low_streak()
        if low_streak >= self._low_streak_threshold:
            signature = f"low-streak:{low_streak}"
            if self._search_tool == "preloaded":
                action_hint = (
                    "peek a preloaded URI you have not examined, replan the bullet, "
                    "or submit_answer with hedging"
                )
            else:
                action_hint = (
                    "issue a more specific search query, peek a candidate URI, "
                    "replan the bullet, or submit_answer with hedging"
                )
            text = (
                f"Low confidence on the last {low_streak} CoT record(s). "
                f"Consider: {action_hint}. You decide."
            )
        elif self._high_but_incomplete():
            signature = "high-incomplete"
            text = (
                "Confidence reported high but the last CoT marked the step incomplete. "
                "Verify the gap is closed before submitting."
            )

        if signature is None or text is None:
            return
        if signature == self._last_emitted_signature:
            return  # Don't re-emit the same advisory back-to-back.
        self._last_emitted_signature = signature
        self._pending_advisory = text

    # ------------------------------------------------------------------
    # Surfacing
    # ------------------------------------------------------------------

    def consume_pending_advisory(self) -> Optional[str]:
        """Return and clear the current pending advisory.

        Used by StateOfTaskDashboardPlugin to absorb advisory output when both
        plugins are active.
        """
        text = self._pending_advisory
        self._pending_advisory = None
        return text

    @hook
    def on_before_model(self, event: BeforeModelCallEvent) -> None:
        if self._dashboard_active:
            return  # Dashboard absorbs the advisory.
        text = self._pending_advisory
        if not text:
            return
        self._pending_advisory = None
        try:
            event.agent.messages.append(
                {"role": "user", "content": [{"text": f"[Advisory] {text}"}]}
            )
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning("Advisory injection failed: %s", exc)


__all__ = ["ConfidenceAdvisoryPlugin"]
