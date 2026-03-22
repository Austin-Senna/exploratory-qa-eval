"""
Planning tool for Condition B.

plan — save a research plan to the agent's working context so it persists
       across turns. The agent writes the plan itself; this tool just injects
       it into agent.system_prompt. Call again to update the plan.
"""
from strands import tool
from strands.types.tools import ToolContext

# ---------------------------------------------------------------------------
# Module-level state (reset between tasks)
# ---------------------------------------------------------------------------

_base_prompt: str = ""


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

@tool(context=True)
def plan(plan_text: str, tool_context: ToolContext) -> str:
    """Save your research plan so it persists across turns. Call again to update.

    Args:
        plan_text: Your written plan.
    """
    global _base_prompt
    agent = tool_context.agent
    # On the very first call, capture the base system prompt.
    # Detect this by checking if _base_prompt is empty OR if the current
    # system_prompt no longer contains our injected section (new task).
    current = agent.system_prompt
    if not _base_prompt or "\n\n## CURRENT PLAN\n" not in current:
        _base_prompt = current
    agent.system_prompt = _base_prompt + "\n\n## CURRENT PLAN\n" + plan_text
    return "Plan recorded."


__all__ = ["plan"]
