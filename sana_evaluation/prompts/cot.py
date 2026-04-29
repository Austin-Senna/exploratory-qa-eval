"""CoT primitive — structured pre/post-tool records (SoK Tool-Augmented Loop)."""

from __future__ import annotations


def cot_block(search_tool: str) -> str:
    """Return the CoT primitive prompt block.

    Adds a structured pre/post-tool record requirement. The pre-record's
    `confidence` field and the post-record's `sufficient_to_call_step_complete`
    field are read by `StateOfTaskDashboardPlugin` (when short_plan is on) to
    populate the reflection-time state-of-task readout.
    """
    return (
        "\n\n## STRUCTURED TOOL-USE RECORDS\n"
        "- Wrap every tool call in a structured record so the runtime can track step progress.\n"
        "- Keep each field concise and action-oriented. Do not dump long reasoning.\n"
        "\n"
        "Before each tool call, emit exactly these four fields (each ≤20 words):\n"
        "goal: <one short sentence>\n"
        "why_this_tool: <one short sentence>\n"
        "what_success_looks_like: <one short sentence>\n"
        "confidence: <low|medium|high>\n"
        "Then call the tool in the same response.\n"
        "\n"
        "After each tool result, before your next tool call (or submit_answer), emit exactly these four fields (each ≤20 words):\n"
        "current_step: <one short sentence>\n"
        "next_step: <one short sentence>\n"
        "sufficient_to_call_step_complete: <true|false>\n"
        "remaining_gap_if_not_complete: <one short sentence, or 'none'>\n"
        "Then continue with your next tool call or submit_answer.\n"
    )


__all__ = ["cot_block"]
