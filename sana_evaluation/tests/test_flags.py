"""Tests for SanaFlags dataclass and validation."""

from __future__ import annotations

import pytest

from sana_evaluation.flags import SanaFlags


def test_default_all_off() -> None:
    flags = SanaFlags()
    assert not flags.any_active()
    assert flags.active_features() == []


def test_from_feature_names_basic() -> None:
    flags = SanaFlags.from_feature_names(["cot", "results"])
    assert flags.cot is True
    assert flags.results is True
    assert flags.sprint is False
    assert "cot" in flags.active_features()
    assert "results" in flags.active_features()


def test_from_feature_names_dashboard_no_longer_valid() -> None:
    """The `dashboard` flag was removed; readout is now bundled into sprint."""
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["dashboard"])


def test_from_feature_names_confidence_advisory_no_longer_valid() -> None:
    """The `confidence_advisory` flag was removed; potential_answer + answer_confidence
    are now part of every k-turn reflection JSON instead."""
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["confidence_advisory"])


def test_old_public_feature_names_are_rejected() -> None:
    for old_name in ("short_plan", "CoT", "results_apis"):
        with pytest.raises(ValueError, match="Unknown SANA feature"):
            SanaFlags.from_feature_names([old_name])


def test_from_feature_names_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown SANA feature"):
        SanaFlags.from_feature_names(["bogus_feature"])


def test_sprint_mode_defaults_to_cadence() -> None:
    flags = SanaFlags(sprint=True)
    assert flags.sprint_mode == "cadence"
    assert flags.commitment_budget_calls == 3


def test_sprint_accepts_commitment_mode() -> None:
    flags = SanaFlags.from_feature_names(
        ["sprint"],
        sprint_mode="commitment",
        commitment_budget_calls=4,
    )
    assert flags.sprint is True
    assert flags.sprint_mode == "commitment"
    assert flags.commitment_budget_calls == 4
    flags.validate(agent_management="standard")


def test_sprint_rejects_unknown_mode() -> None:
    flags = SanaFlags(sprint=True, sprint_mode="bogus")
    with pytest.raises(ValueError, match="sprint_mode"):
        flags.validate(agent_management="standard")


def test_commitment_budget_calls_must_be_positive() -> None:
    flags = SanaFlags(sprint=True, sprint_mode="commitment", commitment_budget_calls=0)
    with pytest.raises(ValueError, match="commitment_budget_calls"):
        flags.validate(agent_management="standard")


def test_sprint_requires_management() -> None:
    flags = SanaFlags(sprint=True)
    with pytest.raises(ValueError, match="sprint requires agent_management"):
        flags.validate(agent_management="naive")


def test_sprint_ok_with_standard() -> None:
    flags = SanaFlags(sprint=True)
    flags.validate(agent_management="standard")
    flags.validate(agent_management="ideal")


def test_macro_reflection_k_must_be_positive() -> None:
    flags = SanaFlags(macro_reflection_k=0)
    with pytest.raises(ValueError, match="macro_reflection_k"):
        flags.validate(agent_management="naive")
