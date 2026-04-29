"""short_plan primitive — k-turn sprint reflection cadence."""

from __future__ import annotations


def short_plan_block(search_tool: str, dashboard_active: bool) -> str:
    """Return the short_plan primitive prompt block.

    The runtime works in k-turn sprints: every k non-administrative tool calls,
    the agent's next tool call is cancelled and steering guidance asks for a
    macro-reflection JSON. The agent emits the JSON, then resumes.
    """
    return (
        "\n\n## K-TURN SPRINT REFLECTION\n"
        "- The runtime works in k-turn sprints. Every k tool calls, your next tool call "
        "will be cancelled and you will be asked to pause and emit a macro-reflection.\n"
        "- A reflection is a JSON-only response (no tool calls) describing where you are "
        "and what comes next. After you emit the JSON, you resume tool calls normally.\n"
        "\n"
        "Macro-reflection JSON shape:\n"
        "{\n"
        '  "global_status": "ON_TRACK" | "NEEDS_REPLAN" | "ANSWER_READY",\n'
        '  "should_submit": true | false,\n'
        '  "short_forward_plan": ["<step 1>", "<step 2>", "<step 3>"]\n'
        "}\n"
        "\n"
        "`short_forward_plan` is a 2–4 step tactical plan for the next sprint.\n"
        "When the runtime asks for reflection, respond with ONE JSON object only — "
        "do not call any tool on that response.\n"
    )


__all__ = ["short_plan_block"]
