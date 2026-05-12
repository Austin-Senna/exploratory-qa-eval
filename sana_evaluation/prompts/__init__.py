"""SANA prompt blocks. Each block is a function (search_tool_mode) -> str."""

from sana_evaluation.prompts.cot import cot_block
from sana_evaluation.prompts.delegation import delegation_block, delegation_planner_prompt
from sana_evaluation.prompts.sprint import sprint_block

__all__ = [
    "cot_block",
    "delegation_block",
    "delegation_planner_prompt",
    "sprint_block",
]
