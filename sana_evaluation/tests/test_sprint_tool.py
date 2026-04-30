"""Tests for the SANA sprint tool and prompt-section persistence."""

from __future__ import annotations

from types import SimpleNamespace

from sana_evaluation.tools.sprint_tool import (
    SprintState,
    clear_sprint_state,
    set_sprint_state,
    sprint,
)
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
        tool_context=ctx,
    )

    assert result == "Sprint recorded."
    assert state.pending_kind is None
    assert state.source_session is not None
    assert state.source_session.current_source == "schools"
    assert state.source_session.max_source_calls == 4
    assert state.source_session.plan_step == "verify enrollment count"
    assert "kind: commitment_contract" in ctx.agent.system_prompt
    assert "plan_step: verify enrollment count" in ctx.agent.system_prompt
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
