"""sprint primitive — short-horizon reflection modes submitted as a tool call."""

from __future__ import annotations


def sprint_block(search_tool: str, sprint_mode: str = "cadence") -> str:
    """Return the sprint primitive prompt block."""
    if sprint_mode == "commitment":
        return _commitment_block()
    return _cadence_block()


def _readout_text() -> str:
    return (
        "   [State of Task - Turn N / MAX]\n"
        "   long_plan: <X step(s) marked complete, Y step(s) flagged incomplete>\n"
        "   sprint: <last sprint status and next action, when available>\n"
        "   candidate_answer: <prior potential_answer> | answer_confidence: <low|medium|high>\n"
        "   source_session: <source> | calls: <used>/<budget> | goal: <goal> | success: <condition>\n"
        "   confidence (last 3): <low|medium|high>, <...>, <...>\n"
        "   evidence: <Z tool call(s) consumed>\n"
    )


def _cadence_block() -> str:
    return (
        "\n\n## K-TURN SPRINT REFLECTION\n"
        "- The runtime works in k-turn sprints. Every k counted tool calls, your next "
        "non-administrative tool call may be cancelled and you will be asked to call "
        "the `sprint` tool.\n"
        "- The sprint tool records your reflection and writes a persistent "
        "`## CURRENT SPRINT` section into the system prompt. Treat that section as "
        "the current short-horizon operating state.\n"
        "- While a sprint is pending, data tools and `submit_answer` are blocked until "
        "the `sprint` tool succeeds.\n"
        "\n"
        "When sprint reflection fires, the cancelled-tool synthetic result contains a "
        "state-of-task readout followed by the instruction to call the sprint tool. "
        "Read the state first, then call the sprint tool.\n"
        "\n"
        + _readout_text()
        + "\n"
        "Call the sprint tool with:\n"
        "- `kind`: `cadence`\n"
        "- `global_status`: `ON_TRACK`, `NEEDS_REPLAN`, or `ANSWER_READY`\n"
        "- `should_submit`: true only when the answer is ready to submit on the next turn\n"
        "- `potential_answer`: your best current answer, or null if none yet\n"
        "- `answer_confidence`: `low`, `medium`, or `high`\n"
        "- `short_forward_plan`: 2-3 strings covering the next sprint, each prefixed "
        "with a turn range such as `turns 1-2:`\n"
        "\n"
        "Be honest about answer confidence. Reporting high confidence in a half-formed "
        "answer to silence the runtime is a known failure mode.\n"
    )


def _commitment_block() -> str:
    return (
        "\n\n## SOURCE COMMITMENT CONTRACT REFLECTION\n"
        "- Dataset access is a multi-turn commitment. Before starting a source, the "
        "runtime may cancel the attempted source tool call and ask you to call the "
        "`sprint` tool with a source commitment contract.\n"
        "- The contract declares what you are trying to learn, how many source calls "
        "you intend to spend, and what evidence closes that commitment.\n"
        "- When the source budget is exhausted, or before switching sources, the "
        "runtime asks for another `sprint` tool call reflecting on the source session.\n"
        "- While a sprint is pending, data tools and `submit_answer` are blocked until "
        "the `sprint` tool succeeds.\n"
        "\n"
        "When a source commitment prompt fires, the cancelled-tool synthetic result "
        "contains a state-of-task readout followed by the instruction to call the "
        "sprint tool. Read the state first, then call the sprint tool.\n"
        "\n"
        + _readout_text()
        + "\n"
        "For a new source, call the sprint tool with:\n"
        "- `kind`: `commitment_contract`\n"
        "- `current_source`: dataset/source id\n"
        "- `commitment_goal`: what this source should answer\n"
        "- `max_source_calls`: positive integer budget\n"
        "- `success_condition`: evidence that means this source is complete\n"
        "\n"
        "For an exhausted source or source switch, call the sprint tool with:\n"
        "- `kind`: `commitment_reflection`\n"
        "- `current_source`, `calls_used`, `commitment_goal`, `evidence_gained`, "
        "`remaining_gap`\n"
        "- `next_action`: `continue_source`, `switch_source`, or `submit`\n"
        "- `revised_budget`: additional calls if continuing, otherwise 0\n"
    )


__all__ = ["sprint_block"]
