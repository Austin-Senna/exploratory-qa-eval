"""dashboard primitive — describes the state-of-task block the agent will see each turn."""

from __future__ import annotations


def dashboard_block(search_tool: str, dashboard_active: bool) -> str:
    """Return the dashboard prompt block.

    Tells the agent that every turn (after the first tool call) will be prefixed
    with a state-of-task block summarizing plan progress, confidence trend, and
    evidence collected so far. The agent should consult this block to make
    decisions rather than re-deriving state from the conversation history.
    """
    return (
        "\n\n## STATE-OF-TASK DASHBOARD\n"
        "Each turn after your first tool call will be prefixed with a block like:\n"
        "\n"
        "  [State of Task — Turn N / MAX]\n"
        "  long_plan: 2/4 bullets complete | short_plan: step 1/3 (<active step>)\n"
        "  confidence (last 3): low, low, medium\n"
        "  evidence: 3 sources peeked, 2 queries run\n"
        "  advisory: <if any>\n"
        "\n"
        "Use this block as your authoritative view of task state. Do not re-derive plan "
        "progress or evidence count from the conversation history when this block is "
        "available. The runtime updates the block each turn from your CoT records and "
        "tool-call ledger.\n"
    )


__all__ = ["dashboard_block"]
