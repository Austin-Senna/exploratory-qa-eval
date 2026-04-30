"""StateOfTaskDashboardPlugin — observes runtime state, renders on demand.

The plugin tracks the current plan text and non-admin tool-call ledger via
Strands hooks. It does NOT inject any messages on its own. `render_block()`
returns the formatted readout for a peer plugin (currently
`SprintSteerHandler`) to surface at reflection time.

State sources:
  - current plan: parsed from plan/plan_ideal tool calls
  - tool budget: incremented on counted AfterToolCallEvent events
  - sprint/source progress: read from a peer SprintSteerHandler if available
"""

from __future__ import annotations

import re
from typing import Any, List, Optional

from strands import Plugin
from strands.hooks import (
    AfterToolCallEvent,
    AgentInitializedEvent,
)
from strands.plugins import hook

_PLAN_MARKER_RE = re.compile(r"\d+[\).]\s+")

_ADMIN_TOOLS = {
    "plan",
    "plan_ideal",
    "skills",
    "sprint",
    "submit_answer",
}


class StateOfTaskDashboardPlugin(Plugin):
    """Observe runtime state; render a state-of-task block on demand."""

    name = "sana-dashboard"

    def __init__(self, *, max_tool_calls: int, history_window: int = 3) -> None:
        super().__init__()
        self._max_tool_calls = max(int(max_tool_calls), 1)
        self._reset()

        # Peer-plugin reference (set externally by sana_bundle when both are wired).
        self.sprint_plugin: Optional[Any] = None

    # ------------------------------------------------------------------
    # Lifecycle / state
    # ------------------------------------------------------------------

    def _reset(self) -> None:
        self._tool_call_count = 0
        self._plan_steps: List[str] = []

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    # ------------------------------------------------------------------
    # State update hooks
    # ------------------------------------------------------------------

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        if event.exception is not None:
            return
        tool_use = getattr(event, "tool_use", {}) or {}
        tool_name = tool_use.get("name", "")
        tool_input = tool_use.get("input", {}) or {}
        if tool_name in {"plan", "plan_ideal"}:
            self._record_plan(tool_input.get("plan_text") or tool_input.get("plan"))
            return
        if tool_name and tool_name not in _ADMIN_TOOLS:
            self._tool_call_count += 1

    def _record_plan(self, plan_text: Any) -> None:
        if not isinstance(plan_text, str):
            return
        steps = _parse_plan_steps(plan_text)
        if steps:
            self._plan_steps = steps

    def _current_plan_step(self) -> str:
        plan_step = _source_session_plan_step(self.sprint_plugin)
        if plan_step:
            if plan_step.isdigit():
                index = int(plan_step) - 1
                if 0 <= index < len(self._plan_steps):
                    return self._plan_steps[index]
            return plan_step
        if self._plan_steps:
            return self._plan_steps[0]
        return "-"

    # ------------------------------------------------------------------
    # Rendering (called by peer plugin at reflection time)
    # ------------------------------------------------------------------

    def render_block(self) -> str:
        """Compose and return the state-of-task readout as a string.

        Caller is responsible for surfacing it (typically prepended to the
            SprintSteerHandler reflection Guide reason).
        """
        sprint_line: Optional[str] = None
        if self.sprint_plugin is not None:
            sprint_line = self.sprint_plugin.describe_for_dashboard()

        calls_left = max(self._max_tool_calls - self._tool_call_count, 0)

        lines = [
            "[State of Task]",
            f"current_plan_step: {self._current_plan_step()}",
            f"tool_calls_left: {calls_left}/{self._max_tool_calls}",
        ]
        if sprint_line:
            lines.append(sprint_line)
        return "\n".join(lines)


def _parse_plan_steps(plan_text: str) -> List[str]:
    matches = list(_PLAN_MARKER_RE.finditer(plan_text))
    if not matches:
        stripped = " ".join(plan_text.split())
        return [stripped] if stripped else []

    steps: List[str] = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(plan_text)
        step = " ".join(plan_text[match.start():end].split())
        if step:
            steps.append(step)
    return steps


def _source_session_plan_step(sprint_plugin: Optional[Any]) -> Optional[str]:
    session = getattr(sprint_plugin, "source_session", None)
    plan_step = getattr(session, "plan_step", None)
    if not isinstance(plan_step, str):
        return None
    plan_step = plan_step.strip()
    return plan_step or None


__all__ = ["StateOfTaskDashboardPlugin"]
