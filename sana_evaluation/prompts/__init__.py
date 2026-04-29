"""SANA prompt blocks. Each block is a function (search_tool_mode, dashboard_active) -> str."""

from sana_evaluation.prompts.cot import cot_block
from sana_evaluation.prompts.dashboard import dashboard_block
from sana_evaluation.prompts.confidence_advisory import confidence_advisory_block
from sana_evaluation.prompts.short_plan import short_plan_block

__all__ = [
    "cot_block",
    "dashboard_block",
    "confidence_advisory_block",
    "short_plan_block",
]
