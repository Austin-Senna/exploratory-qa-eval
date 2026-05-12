"""delegation primitive — planner-only contract tools for tabular tasks."""

from __future__ import annotations


_ATOMIC_CONTRACT_GUIDANCE = (
    "\n## ATOMIC CONTRACT GUIDANCE\n"
    "- Each `inspect_subagent` contract MUST target ONE atomic output. Prefer:\n"
    "  - One entry in `required_outputs` (one fact, number, or short list).\n"
    "  - One dataset id in `source_family_ids` whenever the question maps to a "
    "single dataset. Use multiple ids only when the answer literally needs a "
    "join across files (same row joined across two datasets).\n"
    "- Decompose multi-step questions into a chain of atomic contracts; thread "
    "prior evidence into `known_context` of the next contract instead of "
    "bundling the whole pipeline into one call.\n"
    "- Worked example. For \"smallest postsecondary count among the intersection "
    "of top-3 CA counties for public schools, private schools, and district "
    "offices\", do NOT issue one contract with 4 datasets and 4 required_outputs. "
    "Split into:\n"
    "    c1: required_outputs=[\"top-3 CA counties by public school count\"], "
    "source_family_ids=[\"public-school-locations-current-23297\"]\n"
    "    c2: required_outputs=[\"top-3 CA counties by private school count\"], "
    "source_family_ids=[\"private-school-locations-current-f7d96\"]\n"
    "    c3: required_outputs=[\"top-3 CA counties by district office count\"], "
    "source_family_ids=[\"school-district-office-locations-current-d848f\"]\n"
    "    c4: required_outputs=[\"postsecondary count per county in {intersection}\"], "
    "source_family_ids=[\"postsecondary-school-locations-2022-23\"], "
    "known_context=\"intersection={Los Angeles County, San Diego County}\"\n"
    "- If a contract returns status=failed or budget_exhausted, the fix is "
    "almost never to retry with a larger budget. Split the contract into "
    "smaller atoms.\n"
    "- Pass exact `s3_uri` or (`dataset_id` + `file_path`) handles in "
    "`known_context` whenever you already know them. Never invent a dataset_id "
    "— use only ids that appeared in prior tool outputs or in the preloaded "
    "source list.\n"
)


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
            + _ATOMIC_CONTRACT_GUIDANCE
            + "\n"
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
        + _ATOMIC_CONTRACT_GUIDANCE
        + "\n"
        "Use `search_subagent` before source discovery is unclear. Use "
        "`inspect_subagent` only after you can name explicit dataset ids. Submit only "
        "after the compact subagent evidence is sufficient for the final answer.\n"
    )


def delegation_planner_prompt(search_tool: str, *, management_tool: str = "plan") -> str:
    """Return the full lean parent prompt for delegation mode."""
    search_mode = (search_tool or "").strip().lower()
    include_search = search_mode != "preloaded"
    tools = [
        f"- `{management_tool}(plan_text)`: save a brief numbered plan.",
    ]
    if include_search:
        tools.append(
            "- `search_subagent(contract_id, search_goal, required_source_traits, "
            "budget_calls, constraints, known_context)`: delegate dataset discovery."
        )
    tools.extend(
        [
            "- `inspect_subagent(contract_id, objective, source_family_ids, "
            "required_outputs, success_criteria, budget_calls, constraints, "
            "known_context, retry_of_contract_id)`: delegate extraction from explicit "
            "dataset ids.",
            "- `submit_answer(answer, reasoning)`: submit the final answer and stop.",
        ]
    )
    source_rule = (
        "- Source discovery is already complete. Use the `## PRELOADED DATASETS` "
        "block as the complete source list.\n"
        if not include_search
        else "- Use `search_subagent` when useful dataset ids are not yet known.\n"
    )
    result_fields = (
        "`answer_fragments`, `missing_outputs`, `candidates`, and `retry_recommended`"
        if include_search
        else "`answer_fragments`, `missing_outputs`, and `retry_recommended`"
    )
    return (
        "## DELEGATION PLANNER\n"
        "You are a planner for a bounded delegation workflow.\n\n"
        "## HOW THIS WORKS\n"
        "- Make one tool call at a time. The system executes it and returns the real result.\n"
        "- Do not simulate tool results, make up data, or continue without a tool call.\n"
        "- You do not have direct data-access or execution tools. Delegate source discovery "
        "and extraction through the subagent tools, then synthesize their compact returns.\n\n"
        "## AVAILABLE DELEGATION TOOLS\n"
        + "\n".join(tools)
        + "\n\n## PLANNER CONTRACT\n"
        "- Call the planning tool early with a short execution plan.\n"
        + source_rule
        + "- Use `inspect_subagent` only with explicit dataset ids from a prior result or "
        "the preloaded source list.\n"
        f"- Treat partial subagent returns as evidence. Use {result_fields} to decide "
        "the next contract or final submission.\n"
        "- Keep your own text short and operational. Submit as soon as the compact "
        "subagent evidence is sufficient.\n"
        + _ATOMIC_CONTRACT_GUIDANCE
    )


__all__ = ["delegation_block", "delegation_planner_prompt"]
