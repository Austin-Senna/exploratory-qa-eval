"""Ideal planning helpers and tool surface.

In ideal management mode, plans are loaded from plans_mini and treated as the
canonical source of reasoning and dataset order.
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
    """Append the gold reasoning chain to prompt context for ideal mode."""
    chain_text = format_reasoning_chain(reasoning_chain)
    if not chain_text:
        return system_prompt

    task_suffix = f" ({task_id})" if task_id else ""
    section = (
        f"\n\n## GOLD REASONING CHAIN{task_suffix}\n"
        "Treat this as the canonical reasoning plan for this task. "
        "Use tools to verify and execute it efficiently.\n"
        f"{chain_text}"
    )
    return system_prompt.rstrip() + section


@tool(context=True)
def plan_ideal(plan_text: str, tool_context: ToolContext) -> str:
    """Load ideal target chain and require a step-by-step execution plan."""
    _ = plan_text  # File-backed only: manual plan text is ignored by design.
    global _BASE_PROMPT

    plan = load_plan_for_context()
    plan_block = (
        "Target reasoning chain:\n"
        f"{plan.reasoning_chain_text}\n\n"
        "STEP-BY-STEP PLANNING DIRECTIVE:\n"
        "Before additional retrieval/execution, write a numbered execution plan that explains how you will reach the target reasoning chain.\n"
        "Requirements for that plan:\n"
        "1. Keep steps in dataset_sequence order.\n"
        "2. For each step, name what must be verified/computed.\n"
        "3. Do not just copy the target reasoning chain; explain concrete execution actions."
    )

    agent = tool_context.agent
    current = agent.system_prompt
    if not _BASE_PROMPT or "\n\n## IDEAL PLAN\n" not in current:
        _BASE_PROMPT = current
    agent.system_prompt = _BASE_PROMPT + "\n\n## IDEAL PLAN\n" + plan_block
    return "Ideal plan target loaded. Now produce a numbered step-by-step execution plan to reach the target reasoning chain, then continue."


__all__ = [
    "plan_ideal",
    "format_reasoning_chain",
    "inject_reasoning_chain_prompt",
]
