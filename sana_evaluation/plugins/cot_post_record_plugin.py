"""CoTPostRecordPlugin — append a post-tool-record reminder to each tool result.

System-prompt-only directives are unreliable for smaller models — they often
skip emitting the post-tool record after a tool result and immediately call the
next tool. This plugin uses the strands SDK's `AfterToolCallEvent` (whose
`result` field is mutable) to append a short reminder text block onto each tool
result. The model sees the reminder as part of the tool response it just
received, which is a much more attention-grabbing channel than a static system
prompt rule.

Excluded tools: plan-style and submit_answer don't get a reminder appended
since the post-record loop applies to data-discovery and inspection tools.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from strands import Plugin
from strands.hooks import AfterToolCallEvent
from strands.plugins import hook

logger = logging.getLogger(__name__)


_POST_RECORD_REMINDER = (
    "\n\n---\n"
    "[Post-tool record required]\n"
    "Before your next action, emit (each field ≤20 words):\n"
    "current_step: <one short sentence>\n"
    "next_step: <one short sentence>\n"
    "sufficient_to_call_step_complete: <true|false>\n"
    "remaining_gap_if_not_complete: <one short sentence, or 'none'>\n"
    "Then continue with your next tool call or submit_answer."
)

_EXCLUDED_TOOLS = {
    "plan",
    "plan_ideal",
    "skills",
    "summarize_context",
    "submit_answer",
}


class CoTPostRecordPlugin(Plugin):
    """Append a post-tool-record reminder to every non-administrative tool result."""

    name = "sana-cot-post-record"

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        if event.exception is not None:
            return
        tool_name = (event.tool_use or {}).get("name", "")
        if tool_name in _EXCLUDED_TOOLS:
            return

        result = event.result
        if not isinstance(result, dict):
            return

        content = list(result.get("content", []))
        content.append({"text": _POST_RECORD_REMINDER})

        new_result: Dict[str, Any] = dict(result)
        new_result["content"] = content

        try:
            event.result = new_result
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning("CoT post-record reminder injection failed: %s", exc)


__all__ = ["CoTPostRecordPlugin"]
