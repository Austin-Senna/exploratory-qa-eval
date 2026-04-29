"""SANA prompt blocks. Each block is a function (search_tool_mode) -> str."""

from sana_evaluation.prompts.cot import cot_block
from sana_evaluation.prompts.short_plan import short_plan_block

__all__ = [
    "cot_block",
    "short_plan_block",
]
