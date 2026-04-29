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
