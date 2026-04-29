"""confidence_advisory primitive — describes the soft-advisory the agent will see."""

from __future__ import annotations


def confidence_advisory_block(search_tool: str, dashboard_active: bool) -> str:
    """Return the confidence_advisory prompt block.

    This block tells the agent that its self-reported `confidence` field
    (emitted as part of the CoT pre-tool record) will be parsed by the runtime
    and used to surface soft advisories on subsequent turns. The advisory is
    informational — no hard gates are applied.
    """
    if search_tool == "preloaded":
        action_hints = (
            "  - peek a preloaded URI you have not yet examined\n"
            "  - replan the current bullet\n"
            "  - submit_answer with explicit hedging\n"
        )
    else:
        action_hints = (
            "  - issue a more specific search query for missing evidence\n"
            "  - peek a candidate URI you have not yet examined\n"
            "  - replan the current bullet\n"
            "  - submit_answer with explicit hedging\n"
        )

    surface_note = (
        "It will appear inline on the state-of-task dashboard."
        if dashboard_active else
        "It will appear at the start of the next user turn as a short note."
    )

    return (
        "\n\n## CONFIDENCE ADVISORY\n"
        "Your reported `confidence` field on each CoT record is read by the runtime. "
        "When you report low confidence repeatedly (or report high confidence while plan "
        "bullets remain incomplete), a short advisory will be surfaced to nudge you.\n"
        "\n"
        f"{surface_note}\n"
        "\n"
        "The advisory will suggest options such as:\n"
        f"{action_hints}"
        "\n"
        "Treat the advisory as soft guidance. You retain full control — no tool is blocked.\n"
        "Be honest in your confidence reporting. Reporting high confidence to silence the "
        "advisory while you are not actually ready is a known anti-pattern (closure-chasing).\n"
    )


__all__ = ["confidence_advisory_block"]
