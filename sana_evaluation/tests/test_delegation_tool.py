"""Tests for Tabular SANA planner/subagent delegation tools."""

from __future__ import annotations

import asyncio
import importlib
import json
from unittest.mock import MagicMock

from strands.vended_plugins.steering import Guide, Proceed

from strands_evaluation.config import AgentConfig, RunConfig
from strands_evaluation.instrumentation.trace_plugin import set_trace_context

from sana_evaluation.tools.delegation_tool import (
    DelegationRuntime,
    InspectContract,
    SearchContract,
    _FileReferenceGuard,
    _InspectSourceGuard,
    _SubagentBudgetSteer,
    _SubagentToolLedger,
    _build_search_return_tool,
    _build_inspect_return_tool,
    clear_delegation_runtime,
    _format_inspect_prompt,
    _format_search_prompt,
    inspect_subagent,
    _preloaded_source_sequence,
    search_subagent,
    _source_hints_from_sequence,
    _subagent_system_prompt,
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


class _FakeAgent:
    def __init__(self) -> None:
        self.cancelled = False

    def cancel(self) -> None:
        self.cancelled = True


class _FakeToolContext:
    def __init__(self) -> None:
        self.agent = _FakeAgent()


class _FakeMetrics:
    def __init__(self, *, input_tokens: int, output_tokens: int, cached_input_tokens: int = 0) -> None:
        self.accumulated_usage = {
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "totalTokens": input_tokens + output_tokens,
        }
        if cached_input_tokens:
            self.accumulated_usage["cacheReadInputTokens"] = cached_input_tokens


class _FakeAgentResult:
    def __init__(self, *, input_tokens: int, output_tokens: int, cached_input_tokens: int = 0) -> None:
        self.metrics = _FakeMetrics(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens,
        )


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


def test_delegation_facade_reexports_split_subagent_modules() -> None:
    search_module = importlib.import_module("sana_evaluation.tools.delegation_search")
    inspect_module = importlib.import_module("sana_evaluation.tools.delegation_inspect")

    assert search_subagent is search_module.search_subagent
    assert inspect_subagent is inspect_module.inspect_subagent
    assert SearchContract.__module__ == "sana_evaluation.tools.delegation_search"
    assert InspectContract.__module__ == "sana_evaluation.tools.delegation_inspect"


def test_delegation_subagent_cost_recorder_tracks_costs_and_trace(tmp_path) -> None:
    from sana_evaluation.instrumentation import delegation_subagent_costs

    trace_root = tmp_path / "traces"
    set_trace_context("tasks_core_quality/k-1-d-1/task_1.json", [], str(trace_root))
    delegation_subagent_costs.reset_stats()

    record = delegation_subagent_costs.record_subagent_call(
        tool="search_subagent",
        subagent_kind="search",
        model_name="openai/gpt-5.4-nano",
        agent_result=_FakeAgentResult(input_tokens=900, output_tokens=40, cached_input_tokens=300),
        contract_id="s1",
        status="success",
        budget_calls=3,
    )

    expected_cost = ((600 * 0.20) + (300 * 0.02) + (40 * 1.25)) / 1_000_000
    assert record["event"] == "delegation_subagent_cost"
    assert record["tool"] == "search_subagent"
    assert record["subagent_kind"] == "search"
    assert record["input_tokens"] == 900
    assert record["cached_input_tokens"] == 300
    assert record["uncached_input_tokens"] == 600
    assert record["output_tokens"] == 40
    assert record["contract_id"] == "s1"
    assert record["status"] == "success"
    assert record["budget_calls"] == 3
    assert record["success"] is True
    assert record["cost_usd"] == expected_cost

    stats = delegation_subagent_costs.get_stats()
    assert stats["delegation_subagent_calls"] == 1
    assert stats["search_subagent_calls"] == 1
    assert stats["search_subagent_cost_usd"] == expected_cost
    assert stats["delegation_subagent_cost_usd"] == expected_cost

    trace_path = trace_root / "k-1-d-1" / "task_1.jsonl"
    events = [json.loads(line) for line in trace_path.read_text().splitlines()]
    assert [event["event"] for event in events] == ["delegation_subagent_cost"]
    assert events[0]["cost_usd"] == expected_cost


def test_delegation_runtime_records_subagent_cost(monkeypatch) -> None:
    import sana_evaluation.tools.delegation_tool as delegation_tool

    recorded = []

    def fake_record_subagent_call(**kwargs):
        recorded.append(kwargs)
        return {
            "input_tokens": 900,
            "cached_input_tokens": 300,
            "uncached_input_tokens": 600,
            "output_tokens": 40,
            "total_tokens": 940,
            "cost_usd": 0.000176,
        }

    class _CostAgent:
        def __init__(self, *args, **kwargs):
            self.tools = kwargs["tools"]

        def __call__(self, prompt: str):
            _ = prompt
            return_tool = next(t for t in self.tools if getattr(t, "tool_name", "") == "return_search_result")
            return_tool._tool_func(
                status="success",
                search_summary="found source",
                candidates=[],
                tool_context=_FakeToolContext(),
            )
            return _FakeAgentResult(input_tokens=900, output_tokens=40, cached_input_tokens=300)

    monkeypatch.setattr(delegation_tool, "record_delegation_subagent_call", fake_record_subagent_call)
    monkeypatch.setattr(delegation_tool, "Agent", _CostAgent)
    monkeypatch.setattr(delegation_tool, "build_model", lambda agent_config: object())

    runtime = DelegationRuntime(
        agent_config=AgentConfig(model_name="openai/gpt-5.4-nano"),
        run_config=RunConfig(search_tool_mode="standard"),
        task_context={},
        base_tools=[],
    )
    payload = runtime.run_search_contract(
        SearchContract(
            contract_id="s1",
            search_goal="find school data",
            required_source_traits=["schools"],
            budget_calls=3,
        )
    )

    assert payload["status"] == "success"
    assert payload["subagent_stats"]["cost_usd"] == 0.000176
    assert len(recorded) == 1
    assert recorded[0]["tool"] == "search_subagent"
    assert recorded[0]["subagent_kind"] == "search"
    assert recorded[0]["model_name"] == "openai/gpt-5.4-nano"
    assert recorded[0]["contract_id"] == "s1"
    assert recorded[0]["status"] == "success"
    assert recorded[0]["budget_calls"] == 3
    assert recorded[0]["success"] is True


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
        "peek_file",
        "peek_multiple",
    ]


def test_inspect_subagent_tool_scope_excludes_planner_tools() -> None:
    tools = [
        _tool("plan"),
        _tool("search_reranked"),
        _tool("list_files"),
        _tool("peek_file"),
        _tool("peek_multiple"),
        _tool("read_file"),
        _tool("grep_file"),
        _tool("parse_xml_records"),
        _tool("query_file"),
        _tool("download"),
        _tool("execute_code"),
        _tool("get_sandbox_info"),
        _tool("cleanup_sandbox"),
        _tool("submit_answer"),
        _tool("search_subagent"),
        _tool("inspect_subagent"),
    ]

    filtered = tools_for_inspect_subagent(tools)

    assert tool_names(filtered) == [
        "peek_file",
        "peek_multiple",
        "read_file",
        "grep_file",
        "parse_xml_records",
        "query_file",
        "download",
        "execute_code",
        "get_sandbox_info",
        "cleanup_sandbox",
    ]


def test_subagent_budget_steer_allows_one_grace_tool_call() -> None:
    ledger = _SubagentToolLedger("return_inspect_result")
    steer = _SubagentBudgetSteer(
        ledger=ledger,
        max_tool_calls=3,
        return_tool_name="return_inspect_result",
    )

    ledger.tool_calls = 2
    action = asyncio.run(steer.steer_before_tool(agent=None, tool_use={"name": "query_file"}))
    assert isinstance(action, Proceed)

    ledger.tool_calls = 3
    action = asyncio.run(steer.steer_before_tool(agent=None, tool_use={"name": "read_file"}))
    assert isinstance(action, Proceed)
    assert "grace" in action.reason

    ledger.tool_calls = 4
    action = asyncio.run(steer.steer_before_tool(agent=None, tool_use={"name": "read_file"}))
    assert isinstance(action, Guide)
    assert "return_inspect_result" in action.reason

    action = asyncio.run(steer.steer_before_tool(agent=None, tool_use={"name": "return_inspect_result"}))
    assert isinstance(action, Proceed)


def test_subagent_system_prompts_route_text_sources_without_listing() -> None:
    search_prompt = _subagent_system_prompt("search", "return_search_result")
    inspect_prompt = _subagent_system_prompt("inspect", "return_inspect_result")

    assert "list" not in search_prompt.lower()
    assert "grep_file" in inspect_prompt
    assert "read_file" in inspect_prompt
    assert "dataset_id alone" in inspect_prompt


def test_source_hints_from_preloaded_sequence_include_s3_uris() -> None:
    hints = _source_hints_from_sequence(
        ["public-school-locations-current-23297", "Khan_Lab_School"],
        [
            "datagov/public-school-locations-current-23297/files/data.csv",
            "datagov/private-school-locations-current-f7d96/files/data.csv",
            "wikipedia/Khan_Lab_School/content.txt",
        ],
    )

    assert hints == [
        {
            "dataset_id": "public-school-locations-current-23297",
            "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/public-school-locations-current-23297/files/data.csv",
        },
        {
            "dataset_id": "Khan_Lab_School",
            "s3_uri": "s3://lakeqa-yc4103-datalake/wikipedia/Khan_Lab_School/content.txt",
        },
    ]


def test_preloaded_source_sequence_loads_task_plan_sources() -> None:
    sources = _preloaded_source_sequence(
        {
            "task_id": "tasks_core_quality/k-5-d-4/task_13.json",
            "datasets_used": [],
            "reasoning_chain": [],
        }
    )

    assert "datagov/public-school-locations-current-23297/files/data.txt" in sources


def test_inspect_prompt_includes_source_hints_and_s3_uri_instruction() -> None:
    contract = InspectContract(
        contract_id="i1",
        objective="count schools",
        source_family_ids=["public-school-locations-current-23297"],
        required_outputs=["top_counties"],
        success_criteria="Return top counties.",
        budget_calls=3,
    )

    prompt = _format_inspect_prompt(
        contract,
        source_hints=[
            {
                "dataset_id": "public-school-locations-current-23297",
                "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/public-school-locations-current-23297/files/data.csv",
            }
        ],
    )

    assert "Known source file hints" in prompt
    assert "s3_uri" in prompt
    assert "files/data.csv" in prompt
    assert "Do not guess file paths" in prompt
    assert "Never call file tools with only a dataset_id" in prompt


def test_search_prompt_includes_preloaded_candidate_sources() -> None:
    contract = SearchContract(
        contract_id="s1",
        search_goal="find Khan Lab School page",
        required_source_traits=["Khan Lab School location"],
        budget_calls=2,
    )

    prompt = _format_search_prompt(
        contract,
        source_hints=[
            {
                "dataset_id": "Khan_Lab_School",
                "s3_uri": "s3://lakeqa-yc4103-datalake/wikipedia/Khan_Lab_School/content.txt",
            }
        ],
    )

    assert "Preloaded candidate sources" in prompt
    assert "Khan_Lab_School" in prompt
    assert "return candidates from this list" in prompt
    assert "s3_uri" in prompt


def test_inspect_source_guard_normalizes_contract_s3_uris() -> None:
    guard = _InspectSourceGuard(
        ["s3://lakeqa-yc4103-datalake/datagov/public-school-locations-current-23297/files/data.csv"]
    )

    action = asyncio.run(
        guard.steer_before_tool(
            agent=None,
            tool_use={
                "name": "query_file",
                "input": {
                    "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/public-school-locations-current-23297/files/data.csv",
                    "sql": "SELECT 1",
                },
            },
        )
    )

    assert isinstance(action, Proceed)


def test_file_reference_guard_blocks_bare_dataset_id_file_tools() -> None:
    guard = _FileReferenceGuard()

    action = asyncio.run(
        guard.steer_before_tool(
            agent=None,
            tool_use={
                "name": "peek_file",
                "input": {"dataset_id": "public-school-locations-current-23297", "max_rows": 20},
            },
        )
    )

    assert isinstance(action, Guide)
    assert "s3_uri" in action.reason
    assert "file_path" in action.reason


def test_file_reference_guard_allows_exact_references() -> None:
    guard = _FileReferenceGuard()

    with_s3_uri = asyncio.run(
        guard.steer_before_tool(
            agent=None,
            tool_use={
                "name": "grep_file",
                "input": {
                    "s3_uri": "s3://lakeqa-yc4103-datalake/wikipedia/Khan_Lab_School/content.txt",
                    "regex_pattern": "California",
                },
            },
        )
    )
    with_file_path = asyncio.run(
        guard.steer_before_tool(
            agent=None,
            tool_use={
                "name": "query_file",
                "input": {
                    "dataset_id": "bridge-conditions-nys-department-of-transportation",
                    "file_path": "files/rows.txt",
                    "sql": "SELECT 1",
                },
            },
        )
    )

    assert isinstance(with_s3_uri, Proceed)
    assert isinstance(with_file_path, Proceed)


def test_file_reference_guard_blocks_incomplete_batch_entries() -> None:
    guard = _FileReferenceGuard()

    action = asyncio.run(
        guard.steer_before_tool(
            agent=None,
            tool_use={
                "name": "peek_multiple",
                "input": {
                    "files": [
                        {"dataset_id": "public-school-locations-current-23297"},
                        {
                            "dataset_id": "Khan_Lab_School",
                            "file_path": "content.txt",
                        },
                    ],
                },
            },
        )
    )

    assert isinstance(action, Guide)
    assert "entry 1" in action.reason


def test_inspect_return_tool_defaults_missing_answer_fragments() -> None:
    result_state = {}
    tool = _build_inspect_return_tool(result_state)
    context = _FakeToolContext()

    result = tool._tool_func(
        status="failed",
        missing_outputs=["top3_public_counties"],
        evidence=["404 on source file"],
        executor_summary="Could not read the file.",
        tool_context=context,
    )

    assert result == "Inspection contract result recorded."
    assert result_state["payload"]["answer_fragments"] == []
    assert context.agent.cancelled is True


def test_search_return_tool_defaults_missing_candidates() -> None:
    result_state = {}
    tool = _build_search_return_tool(result_state)
    context = _FakeToolContext()

    result = tool._tool_func(
        status="failed",
        search_summary="No match.",
        tool_context=context,
    )

    assert result == "Search contract result recorded."
    assert result_state["payload"]["candidates"] == []
    assert context.agent.cancelled is True


def test_search_return_tool_autofills_candidates_on_success() -> None:
    captured = [
        {
            "dataset_id": "vsrr-provisional-drug-overdose-death-counts",
            "s3_uri": "s3://bucket/datagov/vsrr/files/rows.txt",
        }
    ]
    result_state = {}
    tool = _build_search_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="success",
        search_summary="Found via search_ideal.",
        tool_context=context,
    )

    assert result_state["payload"]["candidates"] == captured
    # ensure the captured list is copied, not aliased
    assert result_state["payload"]["candidates"] is not captured


def test_search_return_tool_preserves_explicit_candidates() -> None:
    captured = [{"dataset_id": "fallback", "s3_uri": "s3://bucket/fallback"}]
    explicit = [{"dataset_id": "chosen", "s3_uri": "s3://bucket/chosen"}]
    result_state = {}
    tool = _build_search_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="success",
        search_summary="Worker explicitly picked.",
        candidates=explicit,
        tool_context=context,
    )

    assert result_state["payload"]["candidates"] == explicit


def test_search_return_tool_does_not_autofill_on_failure() -> None:
    captured = [{"dataset_id": "ignored", "s3_uri": "s3://bucket/ignored"}]
    result_state = {}
    tool = _build_search_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="failed",
        search_summary="No match.",
        tool_context=context,
    )

    assert result_state["payload"]["candidates"] == []


def test_inspect_return_tool_autofills_evidence_on_partial() -> None:
    captured = [
        {"tool": "peek_file", "s3_uri": "s3://bucket/datagov/vsrr/files/rows.txt"}
    ]
    result_state = {}
    tool = _build_inspect_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="partial",
        answer_fragments=[{"output": "2020 deaths", "value": 91799}],
        missing_outputs=["2021 deaths"],
        executor_summary="2020 was present; 2021 not in file.",
        tool_context=context,
    )

    assert result_state["payload"]["evidence"] == captured


def test_inspect_return_tool_preserves_explicit_evidence() -> None:
    captured = [{"tool": "peek_file", "s3_uri": "s3://bucket/fallback"}]
    explicit = ["query_file(s3://bucket/chosen)"]
    result_state = {}
    tool = _build_inspect_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="success",
        answer_fragments=[{"output": "x", "value": 1}],
        evidence=explicit,
        tool_context=context,
    )

    assert result_state["payload"]["evidence"] == explicit


def test_inspect_return_tool_does_not_autofill_on_failure() -> None:
    captured = [{"tool": "peek_file", "s3_uri": "s3://bucket/x"}]
    result_state = {}
    tool = _build_inspect_return_tool(result_state, lambda: captured)
    context = _FakeToolContext()

    tool._tool_func(
        status="failed",
        failure_reason="Could not read.",
        tool_context=context,
    )

    assert result_state["payload"]["evidence"] == []


def _fake_after_tool_event(name: str, tool_input: dict, result_json: object) -> object:
    """Build a minimal stand-in for AfterToolCallEvent for capture-plugin tests."""

    event = MagicMock()
    event.tool_use = {"name": name, "input": tool_input}
    event.result = {
        "status": "success",
        "content": [{"text": json.dumps(result_json)}],
        "toolUseId": "call_test",
    }
    return event


def test_result_capture_search_aggregates_search_ideal_picks() -> None:
    from sana_evaluation.tools.delegation_common import _SubagentResultCapture

    capture = _SubagentResultCapture(kind="search", return_tool_name="return_search_result")
    capture.on_after_tool(
        _fake_after_tool_event(
            "search_ideal",
            {"query": "overdose deaths by state"},
            {
                "results": [
                    {
                        "dataset_id": "vsrr-provisional-drug-overdose-death-counts",
                        "s3_uri": "s3://bucket/datagov/vsrr/files/rows.txt",
                        "llm_desc": "annual state-level overdose deaths",
                    }
                ],
                "count": 1,
            },
        )
    )
    capture.on_after_tool(
        _fake_after_tool_event(
            "search_ideal",
            {"query": "another"},
            {
                "results": [
                    {
                        "dataset_id": "vsrr-provisional-drug-overdose-death-counts",
                        "s3_uri": "s3://bucket/datagov/vsrr/files/rows.txt",
                    }
                ],
                "count": 1,
            },
        )
    )

    candidates = capture.captured_candidates()
    assert len(candidates) == 1, "duplicates should be deduped by s3_uri"
    assert candidates[0]["dataset_id"] == "vsrr-provisional-drug-overdose-death-counts"
    assert candidates[0]["s3_uri"] == "s3://bucket/datagov/vsrr/files/rows.txt"
    assert candidates[0]["summary"] == "annual state-level overdose deaths"


def test_result_capture_search_ignores_non_search_tools_and_errors() -> None:
    from sana_evaluation.tools.delegation_common import _SubagentResultCapture

    capture = _SubagentResultCapture(kind="search", return_tool_name="return_search_result")
    capture.on_after_tool(
        _fake_after_tool_event(
            "peek_file",
            {"s3_uri": "s3://bucket/x"},
            {"preview_text": "..."},
        )
    )
    # Errored search result should not contribute
    error_event = _fake_after_tool_event(
        "search_ideal",
        {"query": "x"},
        {"error": "Dataset not found"},
    )
    capture.on_after_tool(error_event)
    # Empty results list should also not contribute
    capture.on_after_tool(
        _fake_after_tool_event(
            "search_ideal",
            {"query": "y"},
            {"results": [], "count": 0},
        )
    )

    assert capture.captured_candidates() == []


def test_result_capture_inspect_aggregates_file_refs() -> None:
    from sana_evaluation.tools.delegation_common import _SubagentResultCapture

    capture = _SubagentResultCapture(kind="inspect", return_tool_name="return_inspect_result")
    capture.on_after_tool(
        _fake_after_tool_event(
            "peek_file",
            {"s3_uri": "s3://bucket/datagov/vsrr/files/rows.txt"},
            {"preview_text": "State,Year,..."},
        )
    )
    capture.on_after_tool(
        _fake_after_tool_event(
            "query_file",
            {"dataset_id": "vsrr", "file_path": "files/rows.txt", "sql": "select 1"},
            {"rows": [{"x": 1}]},
        )
    )

    evidence = capture.captured_evidence()
    assert len(evidence) == 2
    assert evidence[0]["tool"] == "peek_file"
    assert evidence[0]["s3_uri"] == "s3://bucket/datagov/vsrr/files/rows.txt"
    assert evidence[1]["tool"] == "query_file"
    assert evidence[1]["dataset_id"] == "vsrr"
    assert evidence[1]["file_path"] == "files/rows.txt"


def test_result_capture_inspect_handles_batch_tools() -> None:
    from sana_evaluation.tools.delegation_common import _SubagentResultCapture

    capture = _SubagentResultCapture(kind="inspect", return_tool_name="return_inspect_result")
    capture.on_after_tool(
        _fake_after_tool_event(
            "peek_multiple",
            {
                "files": [
                    {"s3_uri": "s3://bucket/a"},
                    {"dataset_id": "b", "file_path": "files/b.csv"},
                ]
            },
            {"results": ["...", "..."]},
        )
    )

    evidence = capture.captured_evidence()
    assert len(evidence) == 2
    assert evidence[0]["s3_uri"] == "s3://bucket/a"
    assert evidence[1]["dataset_id"] == "b"
    assert evidence[1]["file_path"] == "files/b.csv"
