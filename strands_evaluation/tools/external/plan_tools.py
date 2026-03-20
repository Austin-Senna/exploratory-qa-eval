"""
Planning tools for Condition B (planning-rich agent).

generate_plan             — decompose the question into sub-tasks with search strategies
generate_reflective_plan  — revise the current plan based on discoveries so far

Each tool spawns a short-lived Strands Agent subagent that returns its response
as a plain string, then parses sub-tasks from the result.

The planning model is configurable via set_plan_model().
"""
from typing import Dict, List

from strands import Agent, tool

# ---------------------------------------------------------------------------
# Module-level state
# ---------------------------------------------------------------------------

_plan_model_id: str = "claude-haiku-4-5-20251001"
_plan_provider: str = "anthropic"
_current_plan: str = ""


def set_plan_model(model_id: str, provider: str = "anthropic") -> None:
    """Set the model used by planning subagents. Called at agent init."""
    global _plan_model_id, _plan_provider
    _plan_model_id = model_id
    _plan_provider = provider


def get_current_plan() -> str:
    """Return the most recently generated plan text."""
    return _current_plan


# ---------------------------------------------------------------------------
# Subagent runner
# ---------------------------------------------------------------------------

def _run_planning_subagent(system_prompt: str, user_message: str) -> str:
    """Spin up a single-turn Strands Agent subagent and return its response."""
    from strands_evaluation.llm.llm_factory import build_model
    from strands_evaluation.config import AgentConfig

    config = AgentConfig(provider=_plan_provider, model_id=_plan_model_id)
    model = build_model(config)

    subagent = Agent(
        model=model,
        system_prompt=system_prompt,
        # No tools — pure reasoning/text generation
        tools=[],
        # Single turn, no conversation history needed
        load_tools_from_directory=False,
    )
    response = subagent(user_message)
    return str(response)


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

_PLAN_SYSTEM = """You are a planning assistant for a data lake research agent.
Given a natural-language question about public government datasets, decompose it
into concrete sub-tasks. For each sub-task, specify:
1. What information is needed
2. A suggested search strategy (what keywords or topics to query)
3. Which dataset types are likely relevant (e.g., census, health, economic)

Format your response as:
PLAN:
<overall strategy in 1-2 sentences>

SUB-TASKS:
1. [Sub-task description] | Search: [suggested query] | Dataset type: [type]
2. ...

Keep the plan concise (3-5 sub-tasks). Do not hallucinate dataset names."""

_REPLAN_SYSTEM = """You are a planning assistant reviewing the progress of a data lake research agent.
Given the original plan and a summary of what has been discovered so far,
revise the plan to reflect current knowledge. Focus on what still needs to be found.

Format your response as:
REVISED PLAN:
<updated strategy in 1-2 sentences>

REMAINING SUB-TASKS:
1. [Sub-task description] | Search: [suggested query] | Dataset type: [type]
2. ...

Keep the revised plan concise (2-4 remaining sub-tasks)."""


def _parse_sub_tasks(text: str) -> List[str]:
    sub_tasks: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line and line[0].isdigit() and "." in line[:3]:
            sub_tasks.append(line)
    return sub_tasks


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def generate_plan(question: str) -> Dict:
    """Decompose the question into sub-tasks with explicit search strategies.

    Call this at the start of a task to build a structured research plan.
    The plan breaks the question into steps, each with a suggested search query.

    Args:
        question: The original research question to plan for.
    """
    global _current_plan
    try:
        plan_text = _run_planning_subagent(
            _PLAN_SYSTEM,
            f"Question: {question}\n\nGenerate a research plan.",
        )
        _current_plan = plan_text
        return {"plan": plan_text, "sub_tasks": _parse_sub_tasks(plan_text)}
    except Exception as e:
        return {"error": str(e), "plan": "", "sub_tasks": []}


@tool
def generate_reflective_plan(discoveries_so_far: str = "") -> Dict:
    """Revise the current plan based on discoveries so far.

    Call this when stuck or when the current plan needs updating.
    Replaces the previous plan with a revised version that focuses
    on what still needs to be found.

    Args:
        discoveries_so_far: Brief summary of what you have found so far
                            (dataset names, relevant fields, partial answers).
    """
    global _current_plan
    try:
        prior_plan = _current_plan or "(no prior plan)"
        user_message = (
            f"Prior plan:\n{prior_plan}\n\n"
            f"Discoveries so far:\n{discoveries_so_far or '(none specified)'}\n\n"
            "Revise the plan based on current progress."
        )
        revised_text = _run_planning_subagent(_REPLAN_SYSTEM, user_message)
        _current_plan = revised_text
        return {"plan": revised_text, "sub_tasks": _parse_sub_tasks(revised_text), "revised": True}
    except Exception as e:
        return {"error": str(e), "plan": _current_plan, "sub_tasks": [], "revised": False}


__all__ = ["generate_plan", "generate_reflective_plan", "set_plan_model", "get_current_plan"]
