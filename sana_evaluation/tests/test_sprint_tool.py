"""Tests for the SANA sprint tool and prompt-section persistence."""

from __future__ import annotations

from types import SimpleNamespace

from sana_evaluation.tools.sprint_tool import (
    SprintState,
    clear_sprint_state,
    set_sprint_state,
    sprint,
)
from sana_evaluation.plugins.source_session import SourceSessionState
from strands_evaluation.tools.external.plan_tools import plan


def _tool_context(prompt: str = "BASE PROMPT"):
    agent = SimpleNamespace(system_prompt=prompt)
    return SimpleNamespace(agent=agent)


def test_sprint_tool_records_current_sprint_after_current_plan() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT\n\n## CURRENT PLAN\nUse source A.")

    result = sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer="2369",
        answer_confidence="medium",
        settled_facts=["Source A contains the relevant count."],
        short_forward_plan=["turns 1-2: verify count", "turns 3-5: submit"],
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert "## CURRENT PLAN\nUse source A." in ctx.agent.system_prompt
    assert "## CURRENT SPRINT" in ctx.agent.system_prompt
    assert ctx.agent.system_prompt.index("## CURRENT PLAN") < ctx.agent.system_prompt.index(
        "## CURRENT SPRINT"
    )
    assert "potential_answer: 2369" in ctx.agent.system_prompt
    assert "settled_facts: Source A contains the relevant count." in ctx.agent.system_prompt
    clear_sprint_state()


def test_sprint_tool_requires_cadence_settled_facts() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer=None,
        answer_confidence="low",
        short_forward_plan=["turns 1-2: inspect"],
        tool_context=ctx,
    )

    assert result.startswith("Sprint not recorded:")
    assert "settled_facts" in result
    assert "## CURRENT SPRINT" not in ctx.agent.system_prompt
    clear_sprint_state()


def test_sprint_tool_accepts_empty_cadence_settled_facts() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer=None,
        answer_confidence="low",
        settled_facts=[],
        short_forward_plan=["turns 1-2: inspect"],
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert "settled_facts: none" in ctx.agent.system_prompt
    clear_sprint_state()


def test_plan_tool_preserves_existing_current_sprint() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")
    sprint(
        kind="cadence",
        global_status="ON_TRACK",
        should_submit=False,
        potential_answer=None,
        answer_confidence="low",
        settled_facts=[],
        short_forward_plan=["turns 1-2: inspect"],
        tool_context=ctx,
    )

    result = plan(plan_text="Use the listed source sequence.", tool_context=ctx)

    assert result == "Plan recorded."
    assert "## CURRENT PLAN\nUse the listed source sequence." in ctx.agent.system_prompt
    assert "## CURRENT SPRINT" in ctx.agent.system_prompt
    assert ctx.agent.system_prompt.index("## CURRENT PLAN") < ctx.agent.system_prompt.index(
        "## CURRENT SPRINT"
    )
    clear_sprint_state()


def test_sprint_tool_rejects_missing_required_fields_without_prompt_update() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(kind="cadence", tool_context=ctx)

    assert result.startswith("Sprint not recorded:")
    assert "global_status" in result
    assert "## CURRENT SPRINT" not in ctx.agent.system_prompt
    clear_sprint_state()


def test_commitment_contract_creates_source_session() -> None:
    state = SprintState(pending_kind="commitment_contract")
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=4,
        plan_step="verify enrollment count",
        related_sources=["school-sites", "school-results"],
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert state.pending_kind is None
    assert state.source_session is not None
    assert state.source_session.current_source == "schools"
    assert state.source_session.max_source_calls == 4
    assert state.source_session.plan_step == "verify enrollment count"
    assert state.source_session.related_sources == ["school-sites", "school-results"]
    assert "kind: commitment_contract" in ctx.agent.system_prompt
    assert "plan_step: verify enrollment count" in ctx.agent.system_prompt
    assert "related_sources: school-sites; school-results" in ctx.agent.system_prompt
    clear_sprint_state()


def test_commitment_contract_requires_plan_step_not_success_condition() -> None:
    state = SprintState(pending_kind="commitment_contract")
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    missing_plan = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=4,
        tool_context=ctx,
    )
    assert missing_plan.startswith("Sprint not recorded:")
    assert "plan_step" in missing_plan
    assert "success_condition" not in missing_plan

    accepted = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=4,
        plan_step="verify enrollment count",
        tool_context=ctx,
    )
    assert accepted == "Sprint recorded."
    clear_sprint_state()


def test_commitment_contract_requires_pending_contract_gate() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_contract",
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=4,
        plan_step="verify enrollment count",
        tool_context=ctx,
    )

    assert result.startswith("Sprint not recorded:")
    assert "pending commitment_contract" in result
    assert state.source_session is None
    clear_sprint_state()


def test_commitment_contract_rejects_wrong_pending_source() -> None:
    state = SprintState(pending_kind="commitment_contract", pending_source="schools")
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_contract",
        current_source="libraries",
        commitment_goal="inspect library rows",
        max_source_calls=2,
        plan_step="switch to libraries",
        tool_context=ctx,
    )

    assert result.startswith("Sprint not recorded:")
    assert "pending source" in result
    assert "## CURRENT SPRINT" not in ctx.agent.system_prompt
    assert state.source_session is None
    clear_sprint_state()


def test_commitment_contract_accepts_package_covering_pending_multi_source() -> None:
    state = SprintState(
        pending_kind="commitment_contract",
        pending_source="multi:libraries,schools",
    )
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_contract",
        current_source="schools",
        related_sources=["libraries"],
        commitment_goal="compare school and library records",
        max_source_calls=3,
        plan_step="compare related sources",
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert state.source_session is not None
    assert state.source_session.current_source == "schools"
    assert state.source_session.related_sources == ["libraries"]
    clear_sprint_state()


def test_commitment_reflection_requires_active_source_session() -> None:
    state = SprintState()
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_reflection",
        current_source="schools",
        calls_used=1,
        commitment_goal="find enrollment count",
        evidence_gained="found schema",
        remaining_gap="need count",
        next_action="submit",
        revised_budget=0,
        tool_context=ctx,
    )

    assert result.startswith("Sprint not recorded:")
    assert "active source session" in result
    assert "## CURRENT SPRINT" not in ctx.agent.system_prompt
    clear_sprint_state()


def test_commitment_reflection_rejects_source_outside_active_package() -> None:
    state = SprintState(
        source_session=SourceSessionState(
            current_source="schools",
            commitment_goal="find enrollment count",
            max_source_calls=2,
            related_sources=["school-sites"],
        )
    )
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_reflection",
        current_source="libraries",
        calls_used=1,
        commitment_goal="inspect library rows",
        evidence_gained="found schema",
        remaining_gap="need count",
        next_action="submit",
        revised_budget=0,
        tool_context=ctx,
    )

    assert result.startswith("Sprint not recorded:")
    assert "active source package" in result
    assert state.source_session is not None
    assert state.source_session.current_source == "schools"
    clear_sprint_state()


def test_commitment_reflection_records_without_mutating_source_session() -> None:
    session = SourceSessionState(
        current_source="schools",
        commitment_goal="find enrollment count",
        max_source_calls=2,
        related_sources=["school-sites"],
        calls_used=1,
    )
    state = SprintState(source_session=session)
    set_sprint_state(state)
    ctx = _tool_context("BASE PROMPT")

    result = sprint(
        kind="commitment_reflection",
        current_source="schools",
        calls_used=99,
        commitment_goal="find enrollment count",
        evidence_gained="found schema",
        remaining_gap="need final answer",
        next_action="submit",
        revised_budget=5,
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert state.source_session is session
    assert state.source_session.calls_used == 1
    assert state.source_session.max_source_calls == 2
    assert state.source_session.related_sources == ["school-sites"]
    assert "kind: commitment_reflection" in ctx.agent.system_prompt
    clear_sprint_state()
