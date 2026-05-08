"""delegation primitive — planner-only contract tools for tabular tasks."""

from __future__ import annotations


def delegation_block(search_tool: str) -> str:
    """Return the planner-facing delegation prompt block."""
    search_mode = (search_tool or "").strip().lower()
    if search_mode == "preloaded":
        return (
            "\n\n## PLANNER WITH BOUNDED SUBAGENTS\n"
            "- You are the planner. Do not search, inspect files, write SQL, download data, "
            "or execute code directly.\n"
            "- Source discovery is already complete in preloaded mode. Use the "
            "`## PRELOADED DATASETS` block as the complete source list.\n"
            "- Use `inspect_subagent` to extract required outputs from explicit dataset ids. "
            "Pass the selected `source_family_ids`, required outputs, success criteria, and "
            "a bounded call budget. When you know an exact `s3_uri` or `file_path`, include "
            "it in `known_context`; do not rely on a bare dataset id as a file handle.\n"
            "- For text/wiki-style result sources, tell `inspect_subagent` to use "
            "`grep_file` or `read_file` rather than trying to write SQL.\n"
            "- Treat partial inspection results as evidence: use `answer_fragments`, "
            "`missing_outputs`, and `retry_recommended` to decide whether to inspect another "
            "preloaded family, retry with narrower criteria, or submit.\n"
            "- Keep raw schema details, SQL errors, zero-row filters, and row dumps out of "
            "your reasoning. The subagents summarize those details for you.\n"
            "\n"
            "Use `inspect_subagent` only after you can name explicit dataset ids from the "
            "preloaded source list. Submit only after the compact subagent evidence is "
            "sufficient for the final answer.\n"
        )
    return (
        "\n\n## PLANNER WITH BOUNDED SUBAGENTS\n"
        "- You are the planner. Do not search, inspect files, write SQL, download data, "
        "or execute code directly.\n"
        "- Use `search_subagent` to find useful datasets. It returns compact candidate "
        "records with rationale, confidence, known gaps, and exact `s3_uri` or "
        "`file_path` handles when available.\n"
        "- Use `inspect_subagent` to extract required outputs from explicit dataset ids. "
        "Pass the selected `source_family_ids`, required outputs, success criteria, and "
        "a bounded call budget. When you know an exact `s3_uri` or `file_path`, include "
        "it in `known_context`; do not rely on a bare dataset id as a file handle.\n"
        "- For text/wiki-style result sources, tell `inspect_subagent` to use "
        "`grep_file` or `read_file` rather than trying to write SQL.\n"
        "- Treat partial inspection results as evidence: use `answer_fragments`, "
        "`missing_outputs`, and `retry_recommended` to decide whether to retry, search "
        "again, inspect another family, or submit.\n"
        "- Keep raw schema details, SQL errors, zero-row filters, and row dumps out of "
        "your reasoning. The subagents summarize those details for you.\n"
        "\n"
        "Use `search_subagent` before source discovery is unclear. Use "
        "`inspect_subagent` only after you can name explicit dataset ids. Submit only "
        "after the compact subagent evidence is sufficient for the final answer.\n"
    )


__all__ = ["delegation_block"]
