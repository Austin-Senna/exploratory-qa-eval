"""SANA-flavored conversation-manager builder.

Reuses Strands' SummarizingConversationManager but supplies a SANA-aware
summarization prompt that explicitly preserves CoT post-tool records and the
most recent macro-reflection JSON. No custom subclass — just a tuned prompt.
"""

from __future__ import annotations

from strands.agent.conversation_manager import SummarizingConversationManager

from strands_evaluation.config import RunConfig


SANA_SUMMARIZATION_PROMPT = """
You are summarizing a tool-using data-analysis conversation produced by an agent
that emits a numbered plan, structured CoT records, and periodic macro-reflection
JSON.

PRESERVE EXACTLY (verbatim, do not paraphrase or omit):
- The original user question.
- The plan emitted by `plan_ideal` or `plan_agent` — preserve every numbered
  bullet exactly as the tool produced it.
- The most recent macro-reflection JSON object — keep its `global_status`,
  `should_submit`, and `short_forward_plan` fields exactly as emitted.

RENDER PROGRESS:
- The agent emits `current_step:` lines as it works through the plan.
- Render the preserved plan as a checklist:
  - Mark every plan step that comes BEFORE the most recent `current_step:`
    value as ✓ done. (Linear-progress inference: previous steps are complete.)
  - Mark the most recent `current_step:` value as ▸ in progress.
  - Leave remaining plan steps unchecked (☐ pending).
- Cross-check with `sufficient_to_call_step_complete: true` — if the agent
  explicitly claimed a step done, mark it ✓ even if its position would
  otherwise leave it unchecked.

ALSO SUMMARIZE concisely:
- Datasets/files inspected, key SQL queries, important findings.
- Failed approaches and constraints learned.
- Best current answer candidate and remaining uncertainty.

Format:
1. "Plan progress:" — the preserved plan rendered as a ✓ / ▸ / ☐ checklist.
2. "Last macro-reflection:" — verbatim JSON fields.
3. "Findings & state:" — technical bullets.

Use precise technical language. Omit conversational filler.
""".strip()


def build_sana_conversation_manager(run_config: RunConfig) -> SummarizingConversationManager:
    """Return a SummarizingConversationManager tuned for SANA-style runs."""
    return SummarizingConversationManager(
        summary_ratio=run_config.summary_ratio,
        preserve_recent_messages=run_config.preserve_recent_messages,
        summarization_system_prompt=SANA_SUMMARIZATION_PROMPT,
    )


__all__ = ["SANA_SUMMARIZATION_PROMPT", "build_sana_conversation_manager"]
