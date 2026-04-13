"""Ideal planning helpers and tool surface.

In ideal management mode, plans are loaded from plans_mini and treated as the
canonical source of reasoning and dataset order. The reasoning chain is
planning context: the agent may reuse/copy it when accurate, but should prefer
to produce a clearer, execution-ready plan.
"""

from __future__ import annotations

from typing import Any, Iterable

from strands import tool
from strands.types.tools import ToolContext

from strands_evaluation.tools.external.ideal.plan_store import load_plan_for_context

_BASE_PROMPT: str = ""


def format_reasoning_chain(reasoning_chain: Any) -> str:
    """Render task reasoning_chain into stable prompt text."""
    if reasoning_chain is None:
        return ""
    if isinstance(reasoning_chain, str):
        text = reasoning_chain.strip()
        return text
    if isinstance(reasoning_chain, Iterable):
        lines = [str(item).strip() for item in reasoning_chain if str(item).strip()]
        return "\n".join(lines)
    return str(reasoning_chain).strip()


def inject_reasoning_chain_prompt(
    system_prompt: str,
    reasoning_chain: Any,
    *,
    task_id: str = "",
) -> str:
    """Append the gold reasoning chain as planning context for ideal mode."""
    chain_text = format_reasoning_chain(reasoning_chain)
    if not chain_text:
        return system_prompt

    task_suffix = f" ({task_id})" if task_id else ""
    section = (
        f"\n\n## GOLD REASONING CHAIN{task_suffix}\n"
        "Treat this as planning context for the task. "
        "You may copy it when accurate, but prefer a clearer execution plan.\n"
        f"{chain_text}"
    )
    return system_prompt.rstrip() + section


@tool(context=True)
def plan_ideal(plan_text: str, tool_context: ToolContext) -> str:
    """Load file-backed reasoning context and ask agent to generate an ideal plan."""
    _ = plan_text  # File-backed only: manual plan text is ignored by design.
    global _BASE_PROMPT

    plan = load_plan_for_context()
    plan_block = (
        "Target reasoning chain (planning context):\n"
        f"{plan.reasoning_chain_text}\n\n"
        "STEP-BY-STEP PLANNING DIRECTIVE:\n"
        "Before additional retrieval/execution, write a numbered execution plan based on this reasoning chain.\n"
        "You may copy chain steps when they are already correct.\n"
        "Prefer improving the plan with clearer execution actions, validations, and expected intermediate outputs.\n"
        "Requirements for that plan:\n"
        "1. Keep steps faithful to the order implied by the reasoning chain.\n"
        "2. For each step, state what must be verified/computed.\n"
        "3. Produce an execution-ready plan in your own words where possible; copy only when it improves clarity."
    )

    agent = tool_context.agent
    current = agent.system_prompt
    if not _BASE_PROMPT or "\n\n## IDEAL PLAN\n" not in current:
        _BASE_PROMPT = current
    agent.system_prompt = _BASE_PROMPT + "\n\n## IDEAL PLAN\n" + plan_block
    return (
        "Ideal plan context loaded. "
        "Now produce a numbered execution plan from the reasoning chain; "
        "copying is allowed, but a clearer execution-ready plan is preferred."
    )


__all__ = [
    "plan_ideal",
    "format_reasoning_chain",
    "inject_reasoning_chain_prompt",
]
