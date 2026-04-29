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
    assert "sana_sprint_k5" in label
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
    assert "sana_sprint_commitment_cb4" in label
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
    assert "sana_cot_results" in label
    assert "ra" not in label
