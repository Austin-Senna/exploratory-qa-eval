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
    assert "STRUCTURED TOOL-USE GATE" in text
    assert "cot" in text
    assert "pre_tool" in text
    assert "post_tool" in text
    assert "intended_tool" in text
    assert "completed_tool" in text
    assert "sufficient_to_call_step_complete" in text
    assert "Do not write free-text CoT records" in text
    for tool_name in ("skills", "plan", "plan_ideal", "sprint", "submit_answer"):
        assert tool_name in text
    assert "intent:" not in text
    assert "confidence:" not in text
    assert "current_step:" not in text
    assert "why_this_tool" not in text
    assert "what_success_looks_like" not in text
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
    assert "settled_facts" in text
    assert "should not be rechecked" in text
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
    assert "related_sources" in text
    assert "commitment_goal" in text
    assert "max_source_calls" in text
    assert "plan_step" in text
    assert "renewal" in text
    assert "evidence_gained" in text
    assert "remaining_gap" in text
    assert "success_condition" not in text
    assert "next_action" in text
    assert "voluntary" in text.lower()
    assert "observation-only" in text.lower()
    assert "State of Task" in text
    assert "current_plan_step" in text
    assert "tool_calls_left" in text
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", ["naive", "standard", "ideal"])
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
    assert "s3_uri" in text
    assert "file_path" in text
    assert "SANA" not in text
    # Atomic contract guidance must anchor the planner toward decomposition.
    assert "ATOMIC CONTRACT GUIDANCE" in text
    assert "required_outputs" in text
    assert "known_context" in text
    assert "Split the contract" in text
    assert "Never invent a dataset_id" in text


def test_delegation_block_preloaded_is_inspect_only() -> None:
    text = delegation_block("preloaded")
    assert "PLANNER WITH BOUNDED SUBAGENTS" in text
    assert "search_subagent" not in text
    assert "inspect_subagent" in text
    assert "PRELOADED DATASETS" in text
    assert "source_family_ids" in text
    assert "s3_uri" in text
    assert "file_path" in text
    assert "SANA" not in text
    # Atomic guidance is symmetric on the preloaded branch.
    assert "ATOMIC CONTRACT GUIDANCE" in text
    assert "required_outputs" in text
    assert "known_context" in text
    assert "Split the contract" in text
