"""Tests for SanaFlags dataclass and validation."""

from __future__ import annotations

import pytest

from sana_evaluation.flags import SanaFlags


def test_default_all_off() -> None:
    flags = SanaFlags()
    assert not flags.any_active()
    assert flags.active_features() == []


def test_from_feature_names_basic() -> None:
    flags = SanaFlags.from_feature_names(["CoT", "results_apis"])
    assert flags.CoT is True
    assert flags.results_apis is True
    assert flags.short_plan is False
    assert "CoT" in flags.active_features()
    assert "results_apis" in flags.active_features()


def test_from_feature_names_dashboard_no_longer_valid() -> None:
    """The `dashboard` flag was removed; readout is now bundled into short_plan."""
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["dashboard"])


def test_from_feature_names_confidence_advisory_no_longer_valid() -> None:
    """The `confidence_advisory` flag was removed; potential_answer + answer_confidence
    are now part of every k-turn reflection JSON instead."""
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["confidence_advisory"])


def test_from_feature_names_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["bogus_feature"])


def test_short_plan_mode_defaults_to_cadence() -> None:
    flags = SanaFlags(short_plan=True)
    assert flags.short_plan_mode == "cadence"
    assert flags.source_budget_calls == 3


def test_short_plan_accepts_source_budget_mode() -> None:
    flags = SanaFlags.from_feature_names(
        ["short_plan"],
        short_plan_mode="source_budget",
        source_budget_calls=4,
    )
    assert flags.short_plan is True
    assert flags.short_plan_mode == "source_budget"
    assert flags.source_budget_calls == 4
    flags.validate(agent_management="standard")


def test_short_plan_rejects_unknown_mode() -> None:
    flags = SanaFlags(short_plan=True, short_plan_mode="bogus")
    with pytest.raises(ValueError, match="short_plan_mode"):
        flags.validate(agent_management="standard")


def test_source_budget_calls_must_be_positive() -> None:
    flags = SanaFlags(short_plan=True, short_plan_mode="source_budget", source_budget_calls=0)
    with pytest.raises(ValueError, match="source_budget_calls"):
        flags.validate(agent_management="standard")


def test_short_plan_requires_management() -> None:
    flags = SanaFlags(short_plan=True)
    with pytest.raises(ValueError, match="short_plan requires agent_management"):
        flags.validate(agent_management="naive")


def test_short_plan_ok_with_standard() -> None:
    flags = SanaFlags(short_plan=True)
    flags.validate(agent_management="standard")
    flags.validate(agent_management="ideal")


def test_macro_reflection_k_must_be_positive() -> None:
    flags = SanaFlags(macro_reflection_k=0)
    with pytest.raises(ValueError, match="macro_reflection_k"):
        flags.validate(agent_management="naive")
