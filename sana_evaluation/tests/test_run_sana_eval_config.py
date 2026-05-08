from sana_evaluation.flags import SanaFlags
from sana_evaluation.run_sana_eval import _variant_condition_label


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
