"""Tests for SANA plugins — exercise their internal state transitions on synthetic events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pytest

import asyncio

from sana_evaluation.plugins import (
    ConfidenceAdvisoryPlugin,
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
class _StubBeforeModelEvent:
    agent: _StubAgent


@dataclass
class _StubAfterToolEvent:
    tool_use: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    exception: Optional[BaseException] = None


def _assistant_message(text: str) -> Dict[str, Any]:
    return {"role": "assistant", "content": [{"text": text}]}


# ---------------------------------------------------------------------------
# ConfidenceAdvisoryPlugin
# ---------------------------------------------------------------------------


def test_advisory_low_streak_triggers_advisory() -> None:
    plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", history_window=5, dashboard_active=True)
    for _ in range(3):
        plugin.on_after_model(
            _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
        )
    advisory = plugin.consume_pending_advisory()
    assert advisory is not None
    assert "Low confidence" in advisory
    # Should be cleared after consume.
    assert plugin.consume_pending_advisory() is None


def test_advisory_high_but_incomplete_triggers() -> None:
    plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", dashboard_active=True)
    plugin.on_after_model(
        _StubAfterModelEvent(
            stop_response=_StubStopResponse(
                _assistant_message(
                    "confidence: high\nsufficient_to_call_step_complete: false"
                )
            )
        )
    )
    advisory = plugin.consume_pending_advisory()
    assert advisory is not None
    assert "high" in advisory.lower()
    assert "incomplete" in advisory.lower() or "step incomplete" in advisory.lower()


def test_advisory_doesnt_repeat_same_signature() -> None:
    plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", dashboard_active=True)
    for _ in range(3):
        plugin.on_after_model(
            _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
        )
    first = plugin.consume_pending_advisory()
    assert first is not None
    # Same low streak → should not re-emit.
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
    )
    second = plugin.consume_pending_advisory()
    assert second is None


def test_advisory_search_modes_have_different_action_hints() -> None:
    preloaded_plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", dashboard_active=True)
    ideal_plugin = ConfidenceAdvisoryPlugin(search_tool="ideal", dashboard_active=True)
    for plugin in (preloaded_plugin, ideal_plugin):
        for _ in range(3):
            plugin.on_after_model(
                _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
            )
    pre = preloaded_plugin.consume_pending_advisory() or ""
    ide = ideal_plugin.consume_pending_advisory() or ""
    assert "search query" not in pre.lower()
    assert "search query" in ide.lower()


def test_advisory_injects_when_dashboard_inactive() -> None:
    plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", dashboard_active=False)
    for _ in range(3):
        plugin.on_after_model(
            _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
        )
    agent = _StubAgent()
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    assert len(agent.messages) == 1
    assert agent.messages[0]["role"] == "user"
    assert "[Advisory]" in agent.messages[0]["content"][0]["text"]
    assert "SANA" not in agent.messages[0]["content"][0]["text"]


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
        '"short_forward_plan": ["step 1", "step 2", "step 3"]}'
    )
    h.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message(response_text)))
    )
    assert h.last_reflection is not None
    assert h.last_reflection["global_status"] == "ON_TRACK"
    assert h.last_reflection["short_forward_plan"] == ["step 1", "step 2", "step 3"]


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
# StateOfTaskDashboardPlugin
# ---------------------------------------------------------------------------


def test_dashboard_skips_first_model_call() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    agent = _StubAgent()
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    assert len(agent.messages) == 0


def test_dashboard_injects_after_first_call() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    agent = _StubAgent()
    # First call (skipped)
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    # Second call (injected)
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    assert len(agent.messages) == 1
    text = agent.messages[0]["content"][0]["text"]
    assert "State of Task" in text
    assert "long_plan" in text


def test_dashboard_picks_up_confidence_history() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10, history_window=3)
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
    )
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: medium")))
    )
    plugin.on_after_model(
        _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: high")))
    )
    agent = _StubAgent()
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    text = agent.messages[0]["content"][0]["text"]
    assert "low" in text and "medium" in text and "high" in text


def test_dashboard_absorbs_advisory_from_peer_plugin() -> None:
    advisory_plugin = ConfidenceAdvisoryPlugin(search_tool="preloaded", dashboard_active=True)
    for _ in range(3):
        advisory_plugin.on_after_model(
            _StubAfterModelEvent(stop_response=_StubStopResponse(_assistant_message("confidence: low")))
        )
    dash_plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    dash_plugin.confidence_advisory_plugin = advisory_plugin
    agent = _StubAgent()
    dash_plugin.on_before_model(_StubBeforeModelEvent(agent=agent))  # first, skipped
    dash_plugin.on_before_model(_StubBeforeModelEvent(agent=agent))  # second, injects
    text = agent.messages[0]["content"][0]["text"]
    assert "advisory" in text.lower()


def test_dashboard_counts_tool_calls() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "query_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "plan"}))  # excluded
    agent = _StubAgent()
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    plugin.on_before_model(_StubBeforeModelEvent(agent=agent))
    text = agent.messages[0]["content"][0]["text"]
    assert "2 tool call(s)" in text
