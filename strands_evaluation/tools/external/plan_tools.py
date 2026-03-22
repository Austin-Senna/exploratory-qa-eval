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
_plan_injected: bool = False


def reset_plan_state() -> None:
    """Clear plan state. Call before each new task run."""
    global _base_prompt, _plan_injected
    _base_prompt = ""
    _plan_injected = False


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------

@tool
def plan(plan_text: str, tool_context: ToolContext) -> str:
    """Save your research plan so it persists across turns. Call again to update.

    Args:
        plan_text: Your written plan.
    """
    global _base_prompt, _plan_injected
    agent = tool_context.agent
    if not _plan_injected:
        _base_prompt = agent.system_prompt
    agent.system_prompt = _base_prompt + "\n\n## CURRENT PLAN\n" + plan_text
    _plan_injected = True
    return "Plan recorded."


__all__ = ["plan", "reset_plan_state"]
