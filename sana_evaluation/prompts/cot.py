"""CoT primitive — runtime-enforced structured tool-use records."""

from __future__ import annotations


def cot_block(search_tool: str) -> str:
    """Return the CoT primitive prompt block.

    Describes the cot control tool. Runtime plugins enforce the actual record
    cadence; the prompt is a compact guide, not the source of truth.
    """
    return (
        "\n\n## STRUCTURED TOOL-USE GATE\n"
        "- The runtime may pause data/search/source tool calls and require the `cot` tool.\n"
        "- When asked for `pre_tool`, call `cot` with `kind`, `intended_tool`, "
        "`current_step`, `intent`, and `confidence`.\n"
        "- When asked for `post_tool`, call `cot` with `kind`, `completed_tool`, "
        "`current_step`, `tool_result_summary`, `next_step`, "
        "`sufficient_to_call_step_complete`, and `remaining_gap_if_not_complete`.\n"
        "- Do not write free-text CoT records. Use the `cot` tool only.\n"
        "- Do not call `cot` before administrative/control tools: skills, plan, "
        "plan_ideal, or sprint. If the runtime asks for `post_tool` before "
        "submit_answer, call `cot` first.\n"
    )


__all__ = ["cot_block"]
