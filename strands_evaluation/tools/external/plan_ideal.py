"""Ideal planning helpers and tool surface.

In ideal management mode, the runner can inject a gold reasoning chain directly
into the system prompt. `plan_ideal` is a companion tool for explicit updates.
"""

from __future__ import annotations

from typing import Any, Iterable

from strands import tool
from strands.types.tools import ToolContext

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
    """Persist an ideal plan section into the active system prompt."""
    global _BASE_PROMPT
    agent = tool_context.agent
    current = agent.system_prompt
    if not _BASE_PROMPT or "\n\n## IDEAL PLAN\n" not in current:
        _BASE_PROMPT = current
    agent.system_prompt = _BASE_PROMPT + "\n\n## IDEAL PLAN\n" + str(plan_text or "").strip()
    return "Ideal plan recorded."


__all__ = [
    "plan_ideal",
    "format_reasoning_chain",
    "inject_reasoning_chain_prompt",
]

