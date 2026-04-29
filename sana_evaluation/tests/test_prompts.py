"""Tests for SANA prompt blocks — each is a function (search_tool, dashboard_active) -> str."""

from __future__ import annotations

import pytest

from sana_evaluation.prompts import (
    confidence_advisory_block,
    cot_block,
    dashboard_block,
    short_plan_block,
)


_SEARCH_MODES = ["naive", "preloaded", "standard", "ideal"]


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
@pytest.mark.parametrize("dashboard_active", [True, False])
def test_cot_block_non_empty(search_tool: str, dashboard_active: bool) -> None:
    text = cot_block(search_tool, dashboard_active)
    assert "STRUCTURED TOOL-USE RECORDS" in text
    assert "confidence:" in text
    assert "sufficient_to_call_step_complete" in text
    # Block must not mention "SANA" — that vocabulary leaks framework-internal naming
    # to the agent and was empirically confusing.
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
@pytest.mark.parametrize("dashboard_active", [True, False])
def test_short_plan_block_non_empty(search_tool: str, dashboard_active: bool) -> None:
    text = short_plan_block(search_tool, dashboard_active)
    assert "K-TURN SPRINT REFLECTION" in text
    assert "short_forward_plan" in text
    assert "global_status" in text
    assert "SANA" not in text


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
@pytest.mark.parametrize("dashboard_active", [True, False])
def test_confidence_advisory_block(search_tool: str, dashboard_active: bool) -> None:
    text = confidence_advisory_block(search_tool, dashboard_active)
    assert "CONFIDENCE ADVISORY" in text
    assert "confidence" in text.lower()
    assert "SANA" not in text
    if dashboard_active:
        assert "dashboard" in text.lower()
    if search_tool == "preloaded":
        assert "search query" not in text.lower()
    else:
        assert "search query" in text.lower()


@pytest.mark.parametrize("search_tool", _SEARCH_MODES)
@pytest.mark.parametrize("dashboard_active", [True, False])
def test_dashboard_block(search_tool: str, dashboard_active: bool) -> None:
    text = dashboard_block(search_tool, dashboard_active)
    assert "STATE-OF-TASK DASHBOARD" in text
    assert "long_plan" in text
    assert "confidence" in text.lower()
    assert "SANA" not in text


def test_dashboard_suppression_changes_cot_block() -> None:
    """When dashboard is active, the inline per-turn note should be omitted."""
    with_dashboard = cot_block("preloaded", dashboard_active=True)
    without_dashboard = cot_block("preloaded", dashboard_active=False)
    # The without-dashboard variant carries an extra line about inline context.
    assert "Per-turn state context will appear inline" in without_dashboard
    assert "Per-turn state context will appear inline" not in with_dashboard
