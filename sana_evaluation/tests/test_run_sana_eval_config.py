from sana_evaluation.flags import SanaFlags
from sana_evaluation.run_sana_eval import _variant_condition_label


def test_variant_label_includes_cadence_short_plan_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(short_plan=True, short_plan_mode="cadence", macro_reflection_k=5),
    )
    assert "sana_spc" in label
    assert "mrk5" in label


def test_variant_label_includes_source_budget_short_plan_mode() -> None:
    label = _variant_condition_label(
        search_tool="preloaded",
        search_results="ideal",
        agent_management="standard",
        k=None,
        search_calls=None,
        sana_flags=SanaFlags(
            short_plan=True,
            short_plan_mode="source_budget",
            source_budget_calls=4,
        ),
    )
    assert "sana_spsb" in label
    assert "sbc4" in label
    assert "mrk" not in label
