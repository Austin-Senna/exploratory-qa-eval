"""short_plan primitive — k-turn sprint reflection cadence."""

from __future__ import annotations


def short_plan_block(search_tool: str) -> str:
    """Return the short_plan primitive prompt block.

    The runtime works in k-turn sprints: every k non-administrative tool calls,
    the agent's next tool call is cancelled and steering guidance asks for a
    macro-reflection JSON. The reflection prompt also includes a state-of-task
    readout (turn count, plan progress, confidence trend, evidence consumed) so
    the agent can re-plan with a consolidated view. The agent emits the JSON,
    then resumes tool calls.
    """
    return (
        "\n\n## K-TURN SPRINT REFLECTION\n"
        "- The runtime works in k-turn sprints. Every k tool calls, your next tool call "
        "will be cancelled and you will be asked to pause and emit a macro-reflection.\n"
        "- A reflection is a JSON-only response (no tool calls) describing where you are "
        "and what comes next. After you emit the JSON, you resume tool calls normally.\n"
        "\n"
        "When reflection fires, the cancelled-tool synthetic result will contain two parts:\n"
        "1. A state-of-task readout summarizing where you are. Format:\n"
        "\n"
        "   [State of Task — Turn N / MAX]\n"
        "   long_plan: <X step(s) marked complete, Y step(s) flagged incomplete>\n"
        "   short_plan: <step i/N (active step)>  (only after first reflection)\n"
        "   candidate_answer: <prior potential_answer> | answer_confidence: <low|medium|high>\n"
        "      (only after first reflection that produced an answer field)\n"
        "   confidence (last 3): <low|medium|high>, <...>, <...>\n"
        "   evidence: <Z tool call(s) consumed>\n"
        "\n"
        "   Use this readout as your authoritative view of state — do not re-derive plan "
        "   progress or evidence count from the conversation history when this readout is "
        "   present. The runtime updates it from your CoT records and tool-call ledger.\n"
        "\n"
        "2. The reflection instruction itself, asking for a JSON object.\n"
        "\n"
        "Macro-reflection JSON shape:\n"
        "{\n"
        '  "global_status": "ON_TRACK" | "NEEDS_REPLAN" | "ANSWER_READY",\n'
        '  "should_submit": true | false,\n'
        '  "potential_answer": "<your best current answer to the user\'s question, or null if none yet>",\n'
        '  "answer_confidence": "low" | "medium" | "high",\n'
        '  "short_forward_plan": [\n'
        '    "turns 1-2: <action a>, <action b>",\n'
        '    "turns 3-5: <action c>, <action d>"\n'
        "  ]\n"
        "}\n"
        "\n"
        "Field guidance:\n"
        "- `potential_answer` is your best current candidate answer to the user's question. "
        "If you do not yet have enough evidence for any candidate, use null and `answer_confidence: low`.\n"
        "- `answer_confidence` reflects how confident you are in `potential_answer`, not in "
        "the next tool call. (The per-tool-call `confidence` in CoT records is a different field.)\n"
        "- `short_forward_plan` is a turn-budgeted plan for the next sprint of up to k turns. "
        "Each entry should be a free-text string starting with a turn range (e.g. \"turns 1-2:\") "
        "followed by the actions for that range. Aim for 2–3 entries covering the next k turns.\n"
        "\n"
        "When the runtime asks for reflection, respond with ONE JSON object only — "
        "do not call any tool on that response.\n"
        "Be honest about `answer_confidence`. Reporting high confidence in a half-formed answer "
        "to silence the runtime is a known failure mode (closure-chasing).\n"
    )


__all__ = ["short_plan_block"]
