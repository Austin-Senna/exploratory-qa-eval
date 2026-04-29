"""Test that SANA's peek_file wrapper documents the `profile` field.

Baseline strands_evaluation peek_file is profile-unaware; SANA's wrapper owns
the profile concept and must document it in its docstring (since the agent
reads tool docstrings to learn what the tool returns).
"""

from __future__ import annotations

from sana_evaluation.tools.peek_file_with_profile import peek_file


def _doc() -> str:
    if hasattr(peek_file, "tool_spec") and isinstance(peek_file.tool_spec, dict):
        return peek_file.tool_spec.get("description", "") or ""
    return peek_file.__doc__ or ""


def test_sana_peek_file_docstring_documents_profile_field() -> None:
    doc = _doc()
    assert "profile" in doc
    assert "schema_columns" in doc
    assert "llm_description" in doc


def test_sana_peek_file_docstring_does_not_mention_sana() -> None:
    doc = _doc()
    assert "SANA" not in doc


def test_baseline_peek_file_docstring_does_not_mention_profile() -> None:
    """Baseline tool must stay profile-unaware."""
    from strands_evaluation.tools.agent_tools_v2 import peek_file as baseline_peek
    if hasattr(baseline_peek, "tool_spec") and isinstance(baseline_peek.tool_spec, dict):
        doc = baseline_peek.tool_spec.get("description", "") or ""
    else:
        doc = baseline_peek.__doc__ or ""
    assert "profile" not in doc
