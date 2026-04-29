"""Tests for SANA prompt blocks — each is a function (search_tool) -> str."""

from __future__ import annotations

import pytest

from sana_evaluation.prompts import (
    cot_block,
    short_plan_block,
)


_SEARCH_MODES = ["naive", "preloaded", "standard", "ideal"]


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_cot_block_non_empty(search_tool: str) -> None:
    text = cot_block(search_tool)
    assert "STRUCTURED TOOL-USE RECORDS" in text
    assert "confidence:" in text
    assert "sufficient_to_call_step_complete" in text
    # Block must not mention "SANA" — that vocabulary leaks framework-internal naming
    # to the agent and was empirically confusing.
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_short_plan_block_describes_cadence_reflection(search_tool: str) -> None:
    text = short_plan_block(search_tool, short_plan_mode="cadence")
    assert "K-TURN SPRINT REFLECTION" in text
    assert "short_forward_plan" in text
    assert "global_status" in text
    assert "potential_answer" in text
    assert "answer_confidence" in text
    assert "turns 1-2" in text
    assert "State of Task" in text
    assert "long_plan" in text
    assert "confidence" in text
    assert "evidence" in text
    assert "source budget contract" not in text.lower()
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
def test_short_plan_block_describes_source_budget_contract(search_tool: str) -> None:
    text = short_plan_block(search_tool, short_plan_mode="source_budget")
    assert "SOURCE BUDGET CONTRACT" in text
    assert "current_source" in text
    assert "commitment_goal" in text
    assert "max_source_calls" in text
    assert "success_condition" in text
    assert "next_action" in text
    assert "continue_source" in text
    assert "switch_source" in text
    assert "State of Task" in text
    assert "SANA" not in text
