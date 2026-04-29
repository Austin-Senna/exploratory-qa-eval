"""Tests for SANA plugins — exercise their internal state transitions on synthetic events."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from sana_evaluation.plugins import (
    CoTPostRecordPlugin,
    ShortPlanSteerHandler,
    StateOfTaskDashboardPlugin,
)
from strands.vended_plugins.steering import Guide, Proceed


@dataclass
class _StubAgent:
    messages: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class _StubStopResponse:
    message: Dict[str, Any]


@dataclass
class _StubAfterModelEvent:
    stop_response: Optional[_StubStopResponse]
    exception: Optional[BaseException] = None


@dataclass
class _StubAfterToolEvent:
    tool_use: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    exception: Optional[BaseException] = None


def _assistant_message(text: str) -> Dict[str, Any]:
    return {"role": "assistant", "content": [{"text": text}]}


# ---------------------------------------------------------------------------
# CoTPostRecordPlugin
# ---------------------------------------------------------------------------


def test_cot_post_record_appends_to_data_tool_result() -> None:
    plugin = CoTPostRecordPlugin()
    result = {"toolUseId": "x", "status": "success", "content": [{"text": "rows..."}]}
    event = _StubAfterToolEvent(tool_use={"name": "peek_file"}, result=result)
    plugin.on_after_tool(event)
    appended = event.result["content"][-1]["text"]
    assert "current_step" in appended
    assert "sufficient_to_call_step_complete" in appended


def test_cot_post_record_skips_administrative_tools() -> None:
    plugin = CoTPostRecordPlugin()
    for tool in ("plan", "plan_ideal", "skills", "submit_answer", "summarize_context"):
        result = {"toolUseId": "x", "status": "success", "content": [{"text": "ok"}]}
        event = _StubAfterToolEvent(tool_use={"name": tool}, result=result)
        plugin.on_after_tool(event)
        assert len(event.result["content"]) == 1, f"{tool} should not get a reminder"


def test_cot_post_record_skips_on_exception() -> None:
    plugin = CoTPostRecordPlugin()
    result = {"toolUseId": "x", "status": "error", "content": [{"text": "boom"}]}
    event = _StubAfterToolEvent(
        tool_use={"name": "peek_file"},
        result=result,
        exception=RuntimeError("kaboom"),
    )
    plugin.on_after_tool(event)
    assert len(event.result["content"]) == 1


# ---------------------------------------------------------------------------
# ShortPlanSteerHandler
# ---------------------------------------------------------------------------


def _run_steer(handler, tool_use):
    return asyncio.run(handler.steer_before_tool(agent=None, tool_use=tool_use))


def test_short_plan_steer_proceeds_within_sprint_window() -> None:
    h = ShortPlanSteerHandler(macro_reflection_k=3)
    for _ in range(2):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Proceed)


def test_short_plan_steer_guides_at_k_boundary() -> None:
    h = ShortPlanSteerHandler(macro_reflection_k=3)
    for _ in range(3):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    assert "JSON" in action.reason


def test_short_plan_steer_passes_administrative_tools() -> None:
    h = ShortPlanSteerHandler(macro_reflection_k=1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    for tool in ("plan", "submit_answer", "skills", "summarize_context"):
        action = _run_steer(h, {"name": tool})
        assert isinstance(action, Proceed)


def test_short_plan_steer_skill_calls_dont_count_toward_sprint() -> None:
    """Skill calls must not advance the sprint counter."""
    h = ShortPlanSteerHandler(macro_reflection_k=3)
    for _ in range(10):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "skills"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Proceed)


def test_short_plan_steer_parses_reflection_json_into_handler() -> None:
    h = ShortPlanSteerHandler(macro_reflection_k=1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    response_text = (
        '{"global_status": "ON_TRACK", "should_submit": false, '
        '"potential_answer": "approximately 1.2M orders", '
        '"answer_confidence": "medium", '
        '"short_forward_plan": ["turns 1-2: peek X", "turns 3-5: query Y"]}'
    )
    h.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message(response_text)))
    )
    assert h.last_reflection is not None
    assert h.last_reflection["global_status"] == "ON_TRACK"
    assert h.last_reflection["potential_answer"] == "approximately 1.2M orders"
    assert h.last_reflection["answer_confidence"] == "medium"
    assert h.last_reflection["short_forward_plan"] == [
        "turns 1-2: peek X",
        "turns 3-5: query Y",
    ]


def test_describe_for_dashboard_includes_candidate_answer_after_reflection() -> None:
    """Once a reflection has produced potential_answer + answer_confidence,
    the dashboard render should surface them on a candidate_answer line."""
    h = ShortPlanSteerHandler(macro_reflection_k=1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    _run_steer(h, {"name": "peek_file"})
    response_text = (
        '{"global_status": "ON_TRACK", "should_submit": false, '
        '"potential_answer": "1.2M", "answer_confidence": "medium", '
        '"short_forward_plan": ["turns 1-2: x"]}'
    )
    h.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message(response_text)))
    )
    description = h.describe_for_dashboard()
    assert "candidate_answer: 1.2M" in description
    assert "answer_confidence: medium" in description


def test_short_plan_steer_resets_after_reflection() -> None:
    h = ShortPlanSteerHandler(macro_reflection_k=2)
    for _ in range(2):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    h.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message('{"global_status": "ON_TRACK", "should_submit": false, "short_forward_plan": []}')
            )
        )
    )
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action2 = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action2, Proceed)


# ---------------------------------------------------------------------------
# StateOfTaskDashboardPlugin — observe only, render on demand
# ---------------------------------------------------------------------------


def test_dashboard_render_block_includes_observed_state() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10, history_window=3)
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "query_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "plan"}))  # excluded
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
    )
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: medium")))
    )
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: high")))
    )

    text = plugin.render_block()
    assert "State of Task" in text
    assert "long_plan" in text
    assert "2 tool call(s)" in text  # plan excluded
    assert "low" in text and "medium" in text and "high" in text


def test_dashboard_does_not_inject_messages_on_its_own() -> None:
    """Dashboard is render-on-demand — it must not append to agent.messages."""
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    agent = _StubAgent()
    # The plugin should not register a BeforeModelCallEvent hook anymore;
    # there is no dashboard hook that touches agent.messages.
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
    )
    assert agent.messages == []


# ---------------------------------------------------------------------------
# ShortPlanSteerHandler + dashboard peer
# ---------------------------------------------------------------------------


def test_short_plan_guide_reason_includes_dashboard_when_peer_wired() -> None:
    """At the k-turn boundary, the Guide reason should be dashboard text + JSON instruction."""
    dashboard = StateOfTaskDashboardPlugin(max_tool_calls=10)
    dashboard.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    dashboard.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: medium")))
    )
    handler = ShortPlanSteerHandler(macro_reflection_k=2)
    handler.dashboard_plugin = dashboard

    for _ in range(2):
        handler.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))

    action = _run_steer(handler, {"name": "peek_file"})
    assert isinstance(action, Guide)
    # Dashboard text appears first, then the JSON instruction.
    state_idx = action.reason.find("State of Task")
    json_idx = action.reason.find("Pause tool calls")
    assert state_idx >= 0
    assert json_idx >= 0
    assert state_idx < json_idx
