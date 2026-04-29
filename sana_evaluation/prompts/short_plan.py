"""short_plan primitive — short-horizon reflection modes."""

from __future__ import annotations


def short_plan_block(search_tool: str, short_plan_mode: str = "cadence") -> str:
    """Return the short_plan primitive prompt block.

    `cadence` preserves the k-turn sprint checkpoint. `source_budget` changes
    the reflection unit to source-session budget contracts for multi-turn data
    access commitments.
    """
    if short_plan_mode == "source_budget":
        return _source_budget_block()
    return _cadence_block()


def _cadence_block() -> str:
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


def _source_budget_block() -> str:
    return (
        "\n\n## SOURCE BUDGET CONTRACT REFLECTION\n"
        "- Dataset access is a multi-turn commitment. When you begin using a source, "
        "the runtime may pause the attempted tool call and ask for a source budget contract.\n"
        "- The contract declares what you are trying to learn from that source, how many "
        "source calls you intend to spend, and what evidence closes the commitment.\n"
        "\n"
        "When reflection fires, the cancelled-tool synthetic result will contain two parts:\n"
        "1. A state-of-task readout summarizing where you are. Format:\n"
        "\n"
        "   [State of Task — Turn N / MAX]\n"
        "   long_plan: <X step(s) marked complete, Y step(s) flagged incomplete>\n"
        "   short_plan: <step i/N (active step)>  (only after first reflection)\n"
        "   candidate_answer: <prior potential_answer> | answer_confidence: <low|medium|high>\n"
        "      (only after first reflection that produced an answer field)\n"
        "   source_session: <source> | calls: <used>/<budget> | goal: <goal> | success: <condition>\n"
        "   confidence (last 3): <low|medium|high>, <...>, <...>\n"
        "   evidence: <Z tool call(s) consumed>\n"
        "\n"
        "2. A JSON-only instruction, either a source budget contract or a source-session reflection.\n"
        "\n"
        "Source budget contract JSON shape:\n"
        "{\n"
        '  "current_source": "<dataset_id or source id>",\n'
        '  "commitment_goal": "<what this source should answer>",\n'
        '  "max_source_calls": 3,\n'
        '  "success_condition": "<evidence that means this source is complete>"\n'
        "}\n"
        "\n"
        "When the source budget is exhausted, or before switching sources, the runtime "
        "will ask for a source-session reflection.\n"
        "\n"
        "Source-session reflection JSON shape:\n"
        "{\n"
        '  "current_source": "<dataset_id or source id>",\n'
        '  "calls_used": 3,\n'
        '  "commitment_goal": "<current source goal>",\n'
        '  "evidence_gained": "<what this source yielded>",\n'
        '  "remaining_gap": "<what is still missing>",\n'
        '  "next_action": "continue_source" | "switch_source" | "submit",\n'
        '  "revised_budget": 0\n'
        "}\n"
        "\n"
        "If `next_action` is `continue_source`, use `revised_budget` for the additional "
        "source calls you need. If it is `switch_source`, move on. If it is `submit`, "
        "submit the answer on the next turn.\n"
        "\n"
        "Use the state-of-task readout as the runtime view of plan progress, confidence "
        "trend, source commitment, and evidence count.\n"
        "When the runtime asks for a contract or reflection, respond with ONE JSON object only — "
        "do not call any tool on that response.\n"
    )


__all__ = ["short_plan_block"]
