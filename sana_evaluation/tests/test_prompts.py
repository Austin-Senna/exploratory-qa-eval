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
def test_short_plan_block_describes_reflection_and_dashboard(search_tool: str) -> None:
    """short_plan owns the full reflection-moment description, including the
    state-of-task readout, candidate-answer fields, and turn-budgeted forward plan."""
    text = short_plan_block(search_tool)
    assert "K-TURN SPRINT REFLECTION" in text
    # Reflection JSON shape (now includes potential_answer + answer_confidence)
    assert "short_forward_plan" in text
    assert "global_status" in text
    assert "potential_answer" in text
    assert "answer_confidence" in text
    # Plan format must show turn-range examples
    assert "turns 1-2" in text
    # State-of-task readout fields (folded in from former dashboard_block)
    assert "State of Task" in text
    assert "long_plan" in text
    assert "confidence" in text
    assert "evidence" in text
    assert "SANA" not in text
