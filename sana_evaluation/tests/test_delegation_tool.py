"""Tests for Tabular SANA planner/subagent delegation tools."""

from __future__ import annotations

from unittest.mock import MagicMock

from sana_evaluation.tools.delegation_tool import (
    clear_delegation_runtime,
    inspect_subagent,
    search_subagent,
    set_delegation_runtime,
    tool_names,
    tools_for_inspect_subagent,
    tools_for_search_subagent,
)


class _FakeRuntime:
    max_search_subagent_calls = 4
    max_inspect_subagent_calls = 9

    def __init__(self) -> None:
        self.search_contract = None
        self.inspect_contract = None

    def run_search_contract(self, contract):
        self.search_contract = contract
        return {
            "status": "success",
            "candidates": [
                {
                    "dataset_id": "school-safety-2019",
                    "s3_uri": "s3://bucket/datagov/school-safety-2019/files/rows.txt",
                    "why_relevant": "Matches school safety and year.",
                    "confidence": "high",
                    "known_gaps": [],
                }
            ],
            "search_summary": "Found a matching dataset.",
            "missing_or_uncertain_coverage": [],
            "retry_recommended": False,
            "subagent_stats": {"budget_calls": contract.budget_calls},
        }

    def run_inspect_contract(self, contract):
        self.inspect_contract = contract
        return {
            "status": "partial",
            "answer_fragments": [{"label": "2019", "value": "12"}],
            "missing_outputs": ["2020"],
            "evidence": ["school-safety-2019 rows.txt"],
            "executor_summary": "2019 was present; 2020 was not in the family.",
            "retry_recommended": False,
            "failure_reason": "",
            "subagent_stats": {"budget_calls": contract.budget_calls},
        }


def _tool(name: str):
    tool = MagicMock()
    tool.tool_name = name
    return tool


def test_search_subagent_validates_required_fields() -> None:
    set_delegation_runtime(_FakeRuntime())
    try:
        result = search_subagent(
            contract_id="c1",
            search_goal="find school safety data",
            required_source_traits=[],
            budget_calls=2,
        )
    finally:
        clear_delegation_runtime()

    assert result["status"] == "failed"
    assert "required_source_traits" in result["failure_reason"]


def test_search_subagent_clamps_budget_and_returns_candidates() -> None:
    runtime = _FakeRuntime()
    set_delegation_runtime(runtime)
    try:
        result = search_subagent(
            contract_id="c1",
            search_goal="find school safety data",
            required_source_traits=["NYC", "2019"],
            budget_calls=99,
        )
    finally:
        clear_delegation_runtime()

    assert runtime.search_contract is not None
    assert runtime.search_contract.budget_calls == 4
    assert result["status"] == "success"
    assert result["candidates"][0]["dataset_id"] == "school-safety-2019"


def test_inspect_subagent_requires_explicit_source_family_ids() -> None:
    set_delegation_runtime(_FakeRuntime())
    try:
        result = inspect_subagent(
            contract_id="i1",
            objective="extract yearly counts",
            source_family_ids=[],
            required_outputs=["2019", "2020"],
            success_criteria="Return both yearly counts.",
            budget_calls=3,
        )
    finally:
        clear_delegation_runtime()

    assert result["status"] == "failed"
    assert "source_family_ids" in result["failure_reason"]


def test_inspect_subagent_clamps_budget_and_allows_partial_results() -> None:
    runtime = _FakeRuntime()
    set_delegation_runtime(runtime)
    try:
        result = inspect_subagent(
            contract_id="i1",
            objective="extract yearly counts",
            source_family_ids=["school-safety-2019", "school-safety-2020"],
            required_outputs=["2019", "2020"],
            success_criteria="Return both yearly counts.",
            budget_calls=99,
        )
    finally:
        clear_delegation_runtime()

    assert runtime.inspect_contract is not None
    assert runtime.inspect_contract.budget_calls == 9
    assert result["status"] == "partial"
    assert result["missing_outputs"] == ["2020"]


def test_search_subagent_tool_scope_is_light_peek_only() -> None:
    tools = [
        _tool("search_reranked"),
        _tool("search_schema"),
        _tool("list_files"),
        _tool("peek_file"),
        _tool("peek_multiple"),
        _tool("read_file"),
        _tool("grep_file"),
        _tool("query_file"),
        _tool("execute_code"),
        _tool("submit_answer"),
    ]

    filtered = tools_for_search_subagent(tools)

    assert tool_names(filtered) == [
        "search_reranked",
        "search_schema",
        "list_files",
        "peek_file",
        "peek_multiple",
    ]


def test_inspect_subagent_tool_scope_excludes_planner_tools() -> None:
    tools = [
        _tool("plan"),
        _tool("search_reranked"),
        _tool("list_files"),
        _tool("peek_file"),
        _tool("read_file"),
        _tool("query_file"),
        _tool("execute_code"),
        _tool("submit_answer"),
        _tool("search_subagent"),
        _tool("inspect_subagent"),
    ]

    filtered = tools_for_inspect_subagent(tools)

    assert tool_names(filtered) == [
        "list_files",
        "peek_file",
        "read_file",
        "query_file",
        "execute_code",
    ]
