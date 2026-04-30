"""SANA prompt blocks. Each block is a function (search_tool_mode) -> str."""

from sana_evaluation.prompts.cot import cot_block
from sana_evaluation.prompts.sprint import sprint_block

__all__ = [
    "cot_block",
    "sprint_block",
]
