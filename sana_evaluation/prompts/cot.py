"""CoT primitive — lightweight pre-tool intent records."""

from __future__ import annotations


def cot_block(search_tool: str) -> str:
    """Return the CoT primitive prompt block.

    Adds a small pre-tool intent record. The `confidence` field is read by
    `StateOfTaskDashboardPlugin` (when sprint is on) to populate the
    reflection-time state-of-task readout.
    """
    return (
        "\n\n## STRUCTURED TOOL-USE RECORDS\n"
        "- Use this tiny record for data/search tools only.\n"
        "- Do not emit this record before administrative/control tools: skills, plan, plan_ideal, sprint, submit_answer.\n"
        "- Keep it to two short lines. Do not dump reasoning.\n"
        "- Never write the tool request, tool arguments, tool result, or output markers as text.\n"
        "\n"
        "Before each data/search tool call, emit exactly these two fields:\n"
        "intent: <one short sentence>\n"
        "confidence: <low|medium|high>\n"
        "Then make the actual tool call through the tool-calling channel.\n"
    )


__all__ = ["cot_block"]
