"""Tests for SANA plugins — exercise their internal state transitions on synthetic events."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

from sana_evaluation.plugins import (
    CoTPostRecordPlugin,
    SprintSteerHandler,
    StateOfTaskDashboardPlugin,
)
from sana_evaluation.tools.sprint_tool import clear_sprint_state, sprint
from strands.vended_plugins.steering import Guide, Proceed


@dataclass
class _StubAgent:
    messages: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class _StubAfterToolEvent:
    tool_use: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    exception: Optional[BaseException] = None


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
    for tool in ("plan", "plan_ideal", "skills", "submit_answer"):
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
# SprintSteerHandler
# ---------------------------------------------------------------------------


def _run_steer(handler, tool_use):
    return asyncio.run(handler.steer_before_tool(agent=None, tool_use=tool_use))


def _sprint_context() -> SimpleNamespace:
    return SimpleNamespace(agent=SimpleNamespace(system_prompt="BASE PROMPT"))


def test_sprint_steer_proceeds_within_sprint_window() -> None:
    h = SprintSteerHandler(macro_reflection_k=3)
    for _ in range(2):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Proceed)


def test_sprint_steer_guides_at_k_boundary() -> None:
    h = SprintSteerHandler(macro_reflection_k=3)
    for _ in range(3):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    assert "sprint" in action.reason
    assert "JSON object only" not in action.reason


def test_sprint_steer_passes_administrative_tools_before_pending() -> None:
    h = SprintSteerHandler(macro_reflection_k=1)
    for tool in ("plan", "submit_answer", "skills"):
        action = _run_steer(h, {"name": tool})
        assert isinstance(action, Proceed)


def test_sprint_steer_skill_calls_dont_count_toward_sprint() -> None:
    """Skill calls must not advance the sprint counter."""
    h = SprintSteerHandler(macro_reflection_k=3)
    for _ in range(10):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "skills"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Proceed)


def test_sprint_tool_call_records_reflection_into_handler() -> None:
    h = SprintSteerHandler(macro_reflection_k=1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    result = sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer="approximately 1.2M orders",
        answer_confidence="medium",
        settled_facts=["peek X returned the order schema"],
        short_forward_plan=["turns 1-2: peek X", "turns 3-5: query Y"],
        tool_context=_sprint_context(),
    )
    assert result == "Sprint recorded."
    assert h.last_reflection is not None
    assert h.last_reflection["global_status"] == "ON_TRACK"
    assert h.last_reflection["potential_answer"] == "approximately 1.2M orders"
    assert h.last_reflection["answer_confidence"] == "medium"
    assert h.last_reflection["settled_facts"] == ["peek X returned the order schema"]
    assert h.last_reflection["short_forward_plan"] == [
        "turns 1-2: peek X",
        "turns 3-5: query Y",
    ]


def test_describe_for_dashboard_includes_candidate_answer_after_reflection() -> None:
    """Once a reflection has produced potential_answer + answer_confidence,
    the dashboard render should surface them on a candidate_answer line."""
    h = SprintSteerHandler(macro_reflection_k=1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    _run_steer(h, {"name": "peek_file"})
    sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer="1.2M",
        answer_confidence="medium",
        settled_facts=["the order count is approximately 1.2M"],
        short_forward_plan=["turns 1-2: x"],
        tool_context=_sprint_context(),
    )
    description = h.describe_for_dashboard()
    assert "candidate_answer: 1.2M" in description
    assert "answer_confidence: medium" in description


def test_sprint_steer_resets_after_tool_call() -> None:
    h = SprintSteerHandler(macro_reflection_k=2)
    for _ in range(2):
        h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action, Guide)
    sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer=None,
        answer_confidence="low",
        settled_facts=[],
        short_forward_plan=[],
        tool_context=_sprint_context(),
    )
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    action2 = _run_steer(h, {"name": "peek_file"})
    assert isinstance(action2, Proceed)


def _send_source_contract(
    handler: SprintSteerHandler,
    source: str,
    budget: int,
    *,
    related_sources: Optional[List[str]] = None,
) -> None:
    sprint(
        kind="commitment_contract",
        current_source=source,
        commitment_goal="find enrollment count",
        max_source_calls=budget,
        plan_step="verify enrollment count",
        related_sources=related_sources,
        tool_context=_sprint_context(),
    )


def test_commitment_requests_contract_on_first_source_tool() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    action = _run_steer(
        h,
        {"name": "peek_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Guide)
    assert "commitment contract" in action.reason.lower()
    assert "schools" in action.reason
    assert "plan_step" in action.reason
    assert "success_condition" not in action.reason


def test_commitment_requests_contract_on_first_relative_uri_tool() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    action = _run_steer(
        h,
        {
            "name": "peek_file",
            "input": {
                "s3_uri": (
                    "datagov/bridge-conditions-nys-department-of-transportation/"
                    "files/rows.txt"
                )
            },
        },
    )
    assert isinstance(action, Guide)
    assert h.state.pending_kind == "commitment_contract"
    assert "bridge-conditions-nys-department-of-transportation" in action.reason


def test_commitment_blocks_non_sprint_tools_while_contract_pending() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    first = _run_steer(
        h,
        {"name": "read_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(first, Guide)

    second = _run_steer(
        h,
        {"name": "read_file", "input": {"dataset_id": "libraries"}},
    )
    assert isinstance(second, Guide)
    assert "still pending" in second.reason.lower()

    submit = _run_steer(
        h,
        {"name": "submit_answer", "input": {"answer": "0"}},
    )
    assert isinstance(submit, Proceed)

    allowed = _run_steer(h, {"name": "sprint", "input": {"kind": "commitment_contract"}})
    assert isinstance(allowed, Proceed)


def test_commitment_tool_contract_allows_retry() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 2)

    action = _run_steer(
        h,
        {"name": "peek_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Proceed)
    assert h.source_session is not None
    assert h.source_session.current_source == "schools"
    assert h.source_session.max_source_calls == 2


def test_commitment_budget_exhaustion_requires_contract_renewal() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=2,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 2)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "query_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(action, Guide)
    assert h.state.pending_kind == "commitment_contract"
    assert "renew" in action.reason.lower()
    assert "commitment_contract" in action.reason
    assert "evidence_gained" in action.reason
    assert "remaining_gap" in action.reason
    assert "commitment_reflection" not in action.reason
    assert "next_action" not in action.reason


def test_commitment_renewal_contract_requires_evidence_and_gap() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=1,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    _run_steer(h, {"name": "query_file", "input": {"dataset_id": "schools"}})

    missing = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=2,
        plan_step="verify enrollment count",
        tool_context=_sprint_context(),
    )
    assert missing.startswith("Sprint not recorded:")
    assert "evidence_gained" in missing
    assert "remaining_gap" in missing

    accepted = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=2,
        plan_step="verify enrollment count",
        evidence_gained="found the schema but not the count",
        remaining_gap="need aggregate enrollment count",
        tool_context=_sprint_context(),
    )
    assert accepted == "Sprint recorded."


def test_commitment_source_switch_requires_new_contract_not_reflection() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 3)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "list_files", "input": {"dataset_ids": ["libraries"]}},
    )
    assert isinstance(action, Guide)
    assert h.state.pending_kind == "commitment_contract"
    assert "commitment_contract" in action.reason
    assert "commitment_reflection" not in action.reason
    assert "libraries" in action.reason
    assert "plan_step" in action.reason

    accepted = sprint(
        kind="commitment_contract",
        current_source="libraries",
        commitment_goal="inspect library rows",
        max_source_calls=2,
        plan_step="switch to library lookup",
        tool_context=_sprint_context(),
    )
    assert accepted == "Sprint recorded."


def test_commitment_related_source_uses_same_package_budget() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 2, related_sources=["school-sites"])
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "school-sites"}},
    )

    assert isinstance(action, Proceed)
    h.on_after_tool(
        _StubAfterToolEvent(
            tool_use={"name": "query_file", "input": {"dataset_id": "school-sites"}}
        )
    )
    assert h.source_session is not None
    assert h.source_session.calls_used == 2
    assert h.source_session.is_budget_exhausted() is True


def test_commitment_outside_related_sources_still_requires_switch_contract() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 3, related_sources=["school-sites"])

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "libraries"}},
    )

    assert isinstance(action, Guide)
    assert h.state.pending_kind == "commitment_contract"
    assert "libraries" in action.reason


def test_commitment_reflection_can_extend_current_source() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=1,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    sprint(
        kind="commitment_reflection",
        current_source="schools",
        calls_used=1,
        commitment_goal="find enrollment count",
        evidence_gained="found schema",
        remaining_gap="need count",
        next_action="continue_source",
        revised_budget=2,
        tool_context=_sprint_context(),
    )
    assert h.source_session is not None
    assert h.source_session.max_source_calls == 3
    assert h.source_session.calls_used == 1


def test_commitment_reflection_is_voluntary_not_runtime_pending() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=1,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "schools"}},
    )

    assert isinstance(action, Guide)
    assert h.state.pending_kind == "commitment_contract"
    assert "commitment_reflection" not in action.reason


def test_final_budget_overrides_cadence_reflection() -> None:
    h = SprintSteerHandler(macro_reflection_k=1, max_tool_calls=3)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))

    action = _run_steer(h, {"name": "query_file"})

    assert isinstance(action, Guide)
    assert "final budget" in action.reason.lower()
    assert h.state.pending_kind is None


def test_final_budget_allows_one_lookup_then_blocks_data_tools() -> None:
    h = SprintSteerHandler(macro_reflection_k=5, max_tool_calls=3)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    first = _run_steer(h, {"name": "query_file", "input": {"dataset_id": "schools"}})
    assert isinstance(first, Guide)
    assert "one final" in first.reason.lower()

    final_lookup = _run_steer(
        h,
        {"name": "grep_file", "input": {"dataset_id": "libraries"}},
    )
    assert isinstance(final_lookup, Proceed)
    h.on_after_tool(
        _StubAfterToolEvent(
            tool_use={"name": "grep_file", "input": {"dataset_id": "libraries"}}
        )
    )

    blocked = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "schools"}},
    )
    assert isinstance(blocked, Guide)
    assert "submit_answer" in blocked.reason

    submit = _run_steer(h, {"name": "submit_answer", "input": {"answer": "42"}})
    assert isinstance(submit, Proceed)


def test_final_budget_overrides_commitment_renewal() -> None:
    h = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=1,
        max_tool_calls=3,
    )
    _run_steer(h, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(h, "schools", 1)
    h.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    action = _run_steer(
        h,
        {"name": "query_file", "input": {"dataset_id": "schools"}},
    )

    assert isinstance(action, Guide)
    assert "final budget" in action.reason.lower()
    assert h.state.pending_kind is None


# ---------------------------------------------------------------------------
# StateOfTaskDashboardPlugin — observe only, render on demand
# ---------------------------------------------------------------------------


def test_dashboard_render_block_includes_observed_state() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10, history_window=3)
    plugin.on_after_tool(
        _StubAfterToolEvent(
            tool_use={
                "name": "plan",
                "input": {
                    "plan_text": (
                        "1) Inspect source schemas.\n"
                        "2) Query qualifying counties.\n"
                        "3) Submit final answer."
                    )
                },
            }
        )
    )
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "query_file"}))
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "sprint"}))  # excluded

    text = plugin.render_block()
    assert "State of Task" in text
    assert "current_plan_step: 1) Inspect source schemas." in text
    assert "tool_calls_left: 8/10" in text
    assert "long_plan" not in text
    assert "confidence" not in text
    assert "reflection" not in text


def test_dashboard_uses_source_session_plan_step_when_available() -> None:
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    handler = SprintSteerHandler(
        macro_reflection_k=5,
        sprint_mode="commitment",
        commitment_budget_calls=3,
    )
    plugin.sprint_plugin = handler
    _run_steer(handler, {"name": "peek_file", "input": {"dataset_id": "schools"}})
    _send_source_contract(handler, "schools", 2)
    handler.source_session.plan_step = "2"
    handler.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))
    plugin.on_after_tool(
        _StubAfterToolEvent(
            tool_use={
                "name": "plan",
                "input": {
                    "plan_text": (
                        "1) Inspect source schemas.\n"
                        "2) Query qualifying counties.\n"
                        "3) Submit final answer."
                    )
                },
            }
        )
    )
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file", "input": {"dataset_id": "schools"}}))

    text = plugin.render_block()

    assert "current_plan_step: 2) Query qualifying counties." in text
    assert "source_session: schools | source_calls: 1/2" in text
    assert "source_goal: find enrollment count" in text
    assert "reflections:" not in text


def test_dashboard_does_not_inject_messages_on_its_own() -> None:
    """Dashboard is render-on-demand — it must not append to agent.messages."""
    plugin = StateOfTaskDashboardPlugin(max_tool_calls=10)
    agent = _StubAgent()
    # The plugin should not register a BeforeModelCallEvent hook anymore;
    # there is no dashboard hook that touches agent.messages.
    plugin.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    assert agent.messages == []


# ---------------------------------------------------------------------------
# SprintSteerHandler + dashboard peer
# ---------------------------------------------------------------------------


def test_sprint_guide_reason_includes_dashboard_when_peer_wired() -> None:
    """At the k-turn boundary, the Guide reason should be dashboard text + sprint instruction."""
    dashboard = StateOfTaskDashboardPlugin(max_tool_calls=10)
    dashboard.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))
    handler = SprintSteerHandler(macro_reflection_k=2)
    handler.dashboard_plugin = dashboard

    for _ in range(2):
        handler.on_after_tool(_StubAfterToolEvent(tool_use={"name": "peek_file"}))

    action = _run_steer(handler, {"name": "peek_file"})
    assert isinstance(action, Guide)
    # Dashboard text appears first, then the sprint-tool instruction.
    state_idx = action.reason.find("State of Task")
    json_idx = action.reason.find("Pause tool calls")
    assert state_idx >= 0
    assert json_idx >= 0
    assert state_idx < json_idx
