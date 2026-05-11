"""CoTSteerHandler - enforce structured CoT records around data tools."""

from __future__ import annotations

from typing import Any, Dict

from strands.hooks import AfterToolCallEvent, AgentInitializedEvent
from strands.plugins import hook
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

from sana_evaluation.tools.cot_tool import CoTState, set_cot_state


_COT_TOOL = "cot"
_ADMIN_TOOLS = {
    _COT_TOOL,
    "plan",
    "plan_ideal",
    "skills",
    "sprint",
}


def _is_tracked_tool(tool_name: str) -> bool:
    return bool(tool_name) and tool_name not in _ADMIN_TOOLS and tool_name != "submit_answer"


def _pre_tool_reason(tool_name: str) -> str:
    return (
        f"Pause tool calls. Before calling `{tool_name}`, call the `cot` tool with "
        "kind='pre_tool'. Include intended_tool, current_step, intent, and "
        "confidence. After the cot tool succeeds, retry the same tool call."
    )


def _post_tool_reason(tool_name: str) -> str:
    return (
        f"Pause tool calls. Before another data/search tool or submit_answer, call "
        f"the `cot` tool with kind='post_tool' for completed_tool='{tool_name}'. "
        "Include current_step, tool_result_summary, next_step, "
        "sufficient_to_call_step_complete, and remaining_gap_if_not_complete."
    )


class CoTSteerHandler(SteeringHandler):
    """Runtime controller that requires cot records around tracked tool calls."""

    name = "sana-cot-steer"

    def __init__(self) -> None:
        super().__init__()
        self.state = CoTState()
        set_cot_state(self.state)

    def _reset(self) -> None:
        self.state = CoTState()
        set_cot_state(self.state)

    @hook
    def on_agent_initialized(self, event: AgentInitializedEvent) -> None:
        self._reset()

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_use = getattr(event, "tool_use", {}) or {}
        tool_name = str(tool_use.get("name") or "")
        if not _is_tracked_tool(tool_name):
            return
        self.state.awaiting_tool = None
        self.state.pending_kind = "post_tool"
        self.state.pending_tool = tool_name
        self.state.pending_reason = _post_tool_reason(tool_name)

    async def steer_before_tool(self, *, agent, tool_use: Dict[str, Any], **kwargs) -> ToolSteeringAction:
        tool_name = str((tool_use or {}).get("name") or "")
        if tool_name == _COT_TOOL:
            return Proceed(reason="cot tool satisfies pending CoT record")
        if tool_name in _ADMIN_TOOLS:
            return Proceed(reason="administrative tool")
        if tool_name == "submit_answer":
            if self.state.pending_kind == "post_tool":
                return Guide(reason=self.state.pending_reason or _post_tool_reason(self.state.pending_tool or "tool"))
            return Proceed(reason="submit_answer allowed")
        if not _is_tracked_tool(tool_name):
            return Proceed(reason="untracked tool")

        if self.state.pending_kind == "post_tool":
            return Guide(reason=self.state.pending_reason or _post_tool_reason(self.state.pending_tool or "tool"))

        if self.state.awaiting_tool != tool_name:
            self.state.pending_kind = "pre_tool"
            self.state.pending_tool = tool_name
            self.state.pending_reason = _pre_tool_reason(tool_name)
            return Guide(reason=self.state.pending_reason)

        return Proceed(reason="matching pre-tool CoT record exists")


__all__ = ["CoTSteerHandler"]
