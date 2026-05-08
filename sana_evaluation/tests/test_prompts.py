"""Tests for SANA prompt blocks — each is a function (search_tool) -> str."""

from __future__ import annotations

import pytest

from sana_evaluation.prompts import (
    cot_block,
    delegation_block,
    sprint_block,
)


_SEARCH_MODES = ["naive", "preloaded", "standard", "ideal"]


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_cot_block_non_empty(search_tool: str) -> None:
    text = cot_block(search_tool)
    assert "STRUCTURED TOOL-USE RECORDS" in text
    assert "confidence:" in text
    assert "sufficient_to_call_step_complete" not in text
    assert "After each tool result" not in text
    assert "data/search tools only" in text
    assert "intent:" in text
    for tool_name in ("skills", "plan", "plan_ideal", "sprint", "submit_answer"):
        assert tool_name in text
    assert "why_this_tool" not in text
    assert "what_success_looks_like" not in text
    assert "Never write the tool request" in text
    assert "to=functions" not in text
    # Block must not mention "SANA" — that vocabulary leaks framework-internal naming
    # to the agent and was empirically confusing.
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_sprint_block_describes_cadence_reflection(search_tool: str) -> None:
    text = sprint_block(search_tool, sprint_mode="cadence")
    assert "K-TURN SPRINT REFLECTION" in text
    assert "sprint tool" in text
    assert "short_forward_plan" in text
    assert "global_status" in text
    assert "potential_answer" in text
    assert "answer_confidence" in text
    assert "turns 1-2" in text
    assert "State of Task" in text
    assert "current_plan_step" in text
    assert "tool_calls_left" in text
    assert "long_plan" not in text
    assert "confidence (last" not in text
    assert "evidence" not in text
    assert "commitment contract" not in text.lower()
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_sprint_block_describes_commitment_contract(search_tool: str) -> None:
    text = sprint_block(search_tool, sprint_mode="commitment")
    assert "SOURCE COMMITMENT CONTRACT" in text
    assert "sprint tool" in text
    assert "current_source" in text
    assert "commitment_goal" in text
    assert "max_source_calls" in text
    assert "plan_step" in text
    assert "success_condition" not in text
    assert "next_action" in text
    assert "voluntary" in text.lower()
    assert "State of Task" in text
    assert "current_plan_step" in text
    assert "tool_calls_left" in text
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_delegation_block_describes_planner_subagent_tools(search_tool: str) -> None:
    text = delegation_block(search_tool)
    assert "PLANNER WITH BOUNDED SUBAGENTS" in text
    assert "search_subagent" in text
    assert "inspect_subagent" in text
    assert "source_family_ids" in text
    assert "answer_fragments" in text
    assert "missing_outputs" in text
    assert "write SQL" in text
    assert "grep_file" in text
    assert "read_file" in text
    assert "SANA" not in text
