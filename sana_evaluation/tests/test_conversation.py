"""Tests for the SANA conversation-manager builder."""

from __future__ import annotations

from strands.agent.conversation_manager import SummarizingConversationManager

from sana_evaluation.helper.conversation import (
    SANA_SUMMARIZATION_PROMPT,
    build_sana_conversation_manager,
)
from sana_evaluation.sana_config import SanaRunConfig


def test_builder_returns_summarizing_conversation_manager() -> None:
    rc = SanaRunConfig(preserve_recent_messages=8, summary_ratio=0.5)
    cm = build_sana_conversation_manager(rc)
    assert isinstance(cm, SummarizingConversationManager)


def test_summarization_prompt_preserves_plan_and_records() -> None:
    """The prompt must explicitly preserve the plan and current sprint."""
    assert "plan_ideal" in SANA_SUMMARIZATION_PROMPT
    assert "plan_agent" in SANA_SUMMARIZATION_PROMPT
    assert "current_step" in SANA_SUMMARIZATION_PROMPT
    assert "sufficient_to_call_step_complete: true" in SANA_SUMMARIZATION_PROMPT
    assert "CURRENT SPRINT" in SANA_SUMMARIZATION_PROMPT
    assert "Current sprint" in SANA_SUMMARIZATION_PROMPT


def test_summarization_prompt_describes_progress_checklist() -> None:
    """The prompt must instruct the LLM to render a ✓/▸/☐ progress checklist."""
    assert "✓" in SANA_SUMMARIZATION_PROMPT
    assert "▸" in SANA_SUMMARIZATION_PROMPT
    assert "☐" in SANA_SUMMARIZATION_PROMPT
    assert "Linear-progress" in SANA_SUMMARIZATION_PROMPT
    assert "checklist" in SANA_SUMMARIZATION_PROMPT.lower()
