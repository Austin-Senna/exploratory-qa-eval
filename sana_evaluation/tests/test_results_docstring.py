"""Test that profile-aware peek docs advertise the shared `profile` field."""

from __future__ import annotations

from sana_evaluation.tools.peek_file_with_profile import peek_file, peek_multiple


def _doc(tool) -> str:
    if hasattr(tool, "tool_spec") and isinstance(tool.tool_spec, dict):
        return tool.tool_spec.get("description", "") or ""
    return tool.__doc__ or ""


def test_sana_peek_file_docstring_documents_profile_field() -> None:
    doc = _doc(peek_file)
    assert "profile" in doc
    assert "columns" in doc
    assert "name/type" in doc
    assert "llm_description" in doc


def test_sana_peek_file_docstring_prefers_s3_uri() -> None:
    doc = _doc(peek_file)
    assert "Prefer `s3_uri`" in doc
    assert "files/rows.txt" in doc


def test_sana_peek_file_docstring_does_not_mention_sana() -> None:
    doc = _doc(peek_file)
    assert "SANA" not in doc


def test_sana_peek_multiple_docstring_documents_profile_field() -> None:
    doc = _doc(peek_multiple)
    assert "profile" in doc
    assert "columns" in doc
    assert "name/type" in doc
    assert "llm_description" in doc


def test_sana_peek_multiple_docstring_prefers_s3_uri() -> None:
    doc = _doc(peek_multiple)
    assert "Prefer per-entry `s3_uri`" in doc
    assert "files" in doc


def test_baseline_peek_file_docstring_documents_profile_field() -> None:
    from strands_evaluation.tools.agent_tools_v2 import peek_file as baseline_peek
    doc = _doc(baseline_peek)
    assert "profile" in doc
    assert "llm_description" in doc


def test_baseline_peek_multiple_docstring_documents_profile_field() -> None:
    from strands_evaluation.tools.agent_tools_v2 import peek_multiple as baseline_peek_multiple
    doc = _doc(baseline_peek_multiple)
    assert "profile" in doc
    assert "llm_description" in doc
