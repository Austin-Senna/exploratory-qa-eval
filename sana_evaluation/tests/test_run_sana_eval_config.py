from sana_evaluation.flags import SanaFlags
from sana_evaluation.run_sana_eval import (
    _effective_plan_skills_enabled,
    _validate_axis_combination,
    _variant_condition_label,
)


def test_variant_label_includes_cadence_sprint_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(sprint=True, sprint_mode="cadence", macro_reflection_k=5),
    )
    assert label == "sana_sprint_k5_sp_ri_pd"
    assert "mrk" not in label


def test_variant_label_includes_commitment_sprint_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(
            sprint=True,
            sprint_mode="commitment",
            commitment_budget_calls=4,
        ),
    )
    assert label == "sana_sprint_commitment_cb4_sp_ri_pd"
    assert "mrk" not in label


def test_variant_label_uses_readable_feature_names() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(cot=True, results=True),
    )
    assert label == "sana_cot_results_sp_ri_pd"
    assert "ra" not in label


def test_variant_label_keeps_axis_suffix_for_non_sana_runs() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(),
    )
    assert label == "sp_ri_pd"


def test_variant_label_appends_ideal_computation_axis() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        computation_tool="ideal",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(),
    )
    assert label == "sp_ri_pd_ci"


def test_variant_label_appends_plan_skills_when_enabled() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        plan_skills_enabled=True,
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(),
    )
    assert label == "sp_ri_pd_skills_on"


def test_variant_label_appends_search_free_and_lessguide_when_enabled() -> None:
    label = _variant_condition_label(
        search_tool="ideal",
        search_results="ideal",
        agent_management="standard",
        search_free=True,
        search_lessguide=True,
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(),
    )
    assert label == "si_ri_pd_free_lessguide"


def test_skills_on_rejects_naive_plans_axis() -> None:
    try:
        _validate_axis_combination(agent_management="naive", skills="on")
    except ValueError as exc:
        assert "--skills on requires --plans standard or --plans ideal" in str(exc)
    else:
        raise AssertionError("Expected ValueError for --skills on with naive plans")


def test_delegation_makes_plan_skills_nonfactor() -> None:
    assert (
        _effective_plan_skills_enabled(
            requested="on",
            sana_flags=SanaFlags(delegation=True),
        )
        is False
    )


def test_non_delegation_keeps_requested_plan_skills() -> None:
    assert (
        _effective_plan_skills_enabled(
            requested="on",
            sana_flags=SanaFlags(delegation=False),
        )
        is True
    )
