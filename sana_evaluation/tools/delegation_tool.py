"""Planner-facing delegation tools backed by fresh bounded subagents."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Sequence

from strands import Agent, Plugin, tool
from strands.hooks import AfterToolCallEvent
from strands.plugins import hook
from strands.types.tools import ToolContext
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

from strands_evaluation.config import AgentConfig, RunConfig
from strands_evaluation.instrumentation.agent_plugins import LoggingPlugin
from strands_evaluation.instrumentation.trace_plugin import write_trace_record
from strands_evaluation.llm.llm_factory import build_model

logger = logging.getLogger(__name__)


_SEARCH_TOOL_NAMES = {
    "search_value",
    "search_schema",
    "search_reranked",
    "search_prefix",
    "search_ideal",
    "search",
    "search_keyword",
}

_LIGHT_PEEK_TOOL_NAMES = {
    "peek_file",
    "peek_multiple",
}

_INSPECT_TOOL_NAMES = {
    "peek_file",
    "peek_multiple",
    "read_file",
    "grep_file",
    "parse_xml_records",
    "query_file",
    "query_ideal",
    "download",
    "execute_code",
    "execute_ideal",
    "get_sandbox_info",
    "cleanup_sandbox",
}

_PLANNER_TOOL_NAMES = {
    "plan",
    "plan_ideal",
    "submit_answer",
}

_VALID_SEARCH_STATUS = {"success", "partial", "failed", "budget_exhausted"}
_VALID_INSPECT_STATUS = {"success", "partial", "failed", "budget_exhausted"}
_SUBAGENT_GRACE_TOOL_CALLS = 1
_DATA_LAKE_BUCKET = "lakeqa-yc4103-datalake"
_DATA_LAKE_FOLDERS = {"datagov", "wikipedia"}


def _tool_name(tool_obj: Any) -> str:
    name = getattr(tool_obj, "tool_name", None)
    if name:
        return str(name)
    spec = getattr(tool_obj, "tool_spec", None)
    if isinstance(spec, dict) and spec.get("name"):
        return str(spec["name"])
    return ""


def tool_names(tools: Sequence[Any]) -> List[str]:
    """Return stable tool names for tests and filtering."""

    return [_tool_name(tool_obj) for tool_obj in tools if _tool_name(tool_obj)]


def tools_for_search_subagent(tools: Sequence[Any]) -> List[Any]:
    """Return search-worker tools: retrieval plus light peek/profile only."""

    allowed = _SEARCH_TOOL_NAMES | _LIGHT_PEEK_TOOL_NAMES
    return [tool_obj for tool_obj in tools if _tool_name(tool_obj) in allowed]


def tools_for_inspect_subagent(tools: Sequence[Any]) -> List[Any]:
    """Return inspector tools: data inspection/query/execution, excluding planner tools."""

    return [tool_obj for tool_obj in tools if _tool_name(tool_obj) in _INSPECT_TOOL_NAMES]


def tools_for_delegation_planner(tools: Sequence[Any]) -> List[Any]:
    """Return planner tools plus the two delegation entrypoints."""

    out = [tool_obj for tool_obj in tools if _tool_name(tool_obj) in _PLANNER_TOOL_NAMES]
    existing = set(tool_names(out))
    if "search_subagent" not in existing:
        out.append(search_subagent)
    if "inspect_subagent" not in existing:
        out.append(inspect_subagent)
    return out


def _clean_str(value: Any) -> str:
    return str(value or "").strip()


def _clean_list(values: Optional[Sequence[Any]]) -> List[str]:
    if values is None:
        return []
    if isinstance(values, (str, bytes)):
        return [_clean_str(values)] if _clean_str(values) else []
    return [text for text in (_clean_str(value) for value in values) if text]


def _split_source_reference(value: Any) -> Optional[tuple[str, str]]:
    """Return (dataset_id, file_path) for lake-relative or S3 source refs."""

    if not isinstance(value, str):
        return None
    raw = value.strip()
    if not raw:
        return None
    if raw.startswith("s3://"):
        remainder = raw[len("s3://") :]
        _bucket, sep, raw = remainder.partition("/")
        if not sep:
            return None
    else:
        raw = raw.lstrip("/")
        bucket_prefix = _DATA_LAKE_BUCKET + "/"
        if raw.startswith(bucket_prefix):
            raw = raw[len(bucket_prefix) :]

    parts = raw.split("/", 2)
    if len(parts) < 2 or parts[0] not in _DATA_LAKE_FOLDERS:
        return None
    return parts[1], parts[2] if len(parts) > 2 else ""


def _source_id_from_reference(value: Any) -> str:
    parsed = _split_source_reference(value)
    if parsed is not None:
        return parsed[0]
    return _clean_str(value)


def _canonical_source_s3_uri(value: str) -> str:
    raw = value.strip()
    if raw.startswith("s3://"):
        return raw
    raw = raw.lstrip("/")
    if raw.startswith(_DATA_LAKE_BUCKET + "/"):
        return "s3://" + raw
    return f"s3://{_DATA_LAKE_BUCKET}/{raw}"


def _source_hints_from_sequence(
    source_family_ids: Sequence[Any],
    source_sequence: Sequence[Any],
    *,
    include_all: bool = False,
) -> List[Dict[str, str]]:
    """Return exact file handles from a preloaded plan for requested datasets."""

    requested = {
        source_id
        for source_id in (_source_id_from_reference(value) for value in source_family_ids)
        if source_id
    }
    if not requested and not include_all:
        return []

    hints: List[Dict[str, str]] = []
    seen_uris: set[str] = set()

    def add_hint(source: Any) -> None:
        parsed = _split_source_reference(source)
        if parsed is None:
            return
        dataset_id, file_path = parsed
        if not include_all and dataset_id not in requested:
            return
        if not file_path:
            return
        s3_uri = _canonical_source_s3_uri(str(source))
        if s3_uri in seen_uris:
            return
        seen_uris.add(s3_uri)
        hints.append({"dataset_id": dataset_id, "s3_uri": s3_uri})

    for source in source_sequence:
        add_hint(source)
    for source in source_family_ids:
        add_hint(source)
    return hints


def _preloaded_source_sequence(task_context: Dict[str, Any]) -> List[str]:
    try:
        from strands_evaluation.tools.external.ideal.plan_store import load_plan_for_context
    except Exception:
        return []
    try:
        plan = load_plan_for_context(task_context)
    except Exception:
        return []
    return [str(source) for source in getattr(plan, "source_sequence", []) or [] if str(source).strip()]


def _search_failure_payload(contract_id: str, reason: str, *, status: str = "failed") -> Dict[str, Any]:
    return {
        "status": status,
        "contract_id": contract_id,
        "candidates": [],
        "search_summary": "",
        "missing_or_uncertain_coverage": [reason],
        "failure_reason": reason,
        "retry_recommended": False,
        "subagent_stats": {},
    }


def _inspect_failure_payload(contract_id: str, reason: str, *, status: str = "failed") -> Dict[str, Any]:
    return {
        "status": status,
        "contract_id": contract_id,
        "answer_fragments": [],
        "missing_outputs": [],
        "evidence": [],
        "executor_summary": "",
        "failure_reason": reason,
        "retry_recommended": False,
        "subagent_stats": {},
    }


@dataclass
class SearchContract:
    contract_id: str
    search_goal: str
    required_source_traits: List[str]
    budget_calls: int
    constraints: List[str] = field(default_factory=list)
    known_context: str = ""
    requested_budget_calls: int = 0


@dataclass
class InspectContract:
    contract_id: str
    objective: str
    source_family_ids: List[str]
    required_outputs: List[str]
    success_criteria: str
    budget_calls: int
    constraints: List[str] = field(default_factory=list)
    known_context: str = ""
    retry_of_contract_id: str = ""
    requested_budget_calls: int = 0


class DelegationRuntimeProtocol(Protocol):
    max_search_subagent_calls: int
    max_inspect_subagent_calls: int

    def run_search_contract(self, contract: SearchContract) -> Dict[str, Any]:
        ...

    def run_inspect_contract(self, contract: InspectContract) -> Dict[str, Any]:
        ...


_RUNTIME: Optional[DelegationRuntimeProtocol] = None


def set_delegation_runtime(runtime: DelegationRuntimeProtocol) -> None:
    global _RUNTIME
    _RUNTIME = runtime


def clear_delegation_runtime() -> None:
    global _RUNTIME
    _RUNTIME = None


def current_delegation_runtime() -> Optional[DelegationRuntimeProtocol]:
    return _RUNTIME


def _positive_int(value: Any, *, default: int = 1) -> int:
    try:
        out = int(value)
    except (TypeError, ValueError):
        return default
    return out if out > 0 else default


def _metrics_usage(agent_result: Any) -> Dict[str, int]:
    metrics = getattr(agent_result, "metrics", None)
    usage = getattr(metrics, "accumulated_usage", {}) or {}

    def coerce(key: str) -> int:
        try:
            return int(usage.get(key) or 0)
        except (TypeError, ValueError):
            return 0

    input_tokens = coerce("inputTokens")
    output_tokens = coerce("outputTokens")
    cached_input_tokens = coerce("cacheReadInputTokens")
    total_tokens = coerce("totalTokens") or input_tokens + output_tokens
    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "uncached_input_tokens": max(0, input_tokens - cached_input_tokens),
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def _cost_usd(model_name: str, usage: Dict[str, int]) -> float:
    try:
        from strands_evaluation.instrumentation.ideal_subagent_costs import cost_for_usage
    except Exception:
        return 0.0
    return cost_for_usage(model_name, usage)


class _SubagentToolLedger(Plugin):
    name = "sana-delegation-tool-ledger"

    def __init__(self, return_tool_name: str) -> None:
        super().__init__()
        self.return_tool_name = return_tool_name
        self.tool_calls = 0
        self.tools_used: List[str] = []

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = getattr(event, "tool_use", {}).get("name", "")
        if not tool_name or tool_name == self.return_tool_name:
            return
        self.tool_calls += 1
        self.tools_used.append(tool_name)


class _SubagentBudgetSteer(SteeringHandler):
    name = "sana-delegation-budget-steer"

    def __init__(
        self,
        *,
        ledger: _SubagentToolLedger,
        max_tool_calls: int,
        return_tool_name: str,
        grace_tool_calls: int = _SUBAGENT_GRACE_TOOL_CALLS,
    ) -> None:
        super().__init__()
        self.ledger = ledger
        self.max_tool_calls = max(int(max_tool_calls), 1)
        self.return_tool_name = return_tool_name
        try:
            self.grace_tool_calls = max(int(grace_tool_calls), 0)
        except (TypeError, ValueError):
            self.grace_tool_calls = 0
        self.hard_tool_call_limit = self.max_tool_calls + self.grace_tool_calls

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        if tool_name == self.return_tool_name:
            return Proceed(reason="contract return tool is allowed")
        if self.ledger.tool_calls < self.max_tool_calls:
            return Proceed(reason="within subagent tool budget")
        if self.ledger.tool_calls < self.hard_tool_call_limit:
            return Proceed(reason="within one-call subagent grace window after nominal budget")
        return Guide(
            reason=(
                f"The bounded contract budget of {self.max_tool_calls} tool calls plus "
                f"{self.grace_tool_calls} grace call(s) is exhausted. "
                f"Call `{self.return_tool_name}` now with status='budget_exhausted' and a compact "
                "summary of what was learned. Do not call any other tool."
            )
        )


class _InspectSourceGuard(SteeringHandler):
    name = "sana-delegation-inspect-source-guard"

    def __init__(self, allowed_dataset_ids: Sequence[str]) -> None:
        super().__init__()
        self.allowed = {
            source_id
            for source_id in (_source_id_from_reference(value) for value in _clean_list(allowed_dataset_ids))
            if source_id
        }

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        try:
            from sana_evaluation.plugins.source_session import source_from_tool_use
        except Exception:
            return Proceed(reason="source guard unavailable")

        source = source_from_tool_use(tool_use or {})
        if not source:
            return Proceed(reason="tool has no source identity")
        sources = source.split(":", 1)[1].split(",") if source.startswith("multi:") else [source]
        blocked = [item for item in sources if item not in self.allowed]
        if not blocked:
            return Proceed(reason="source is inside inspection contract")
        return Guide(
            reason=(
                "This inspection contract is limited to explicit dataset ids "
                f"{sorted(self.allowed)}. The attempted tool call referenced {blocked}. "
                "Use only the contracted source family, or call the contract return tool "
                "with a failed/partial status."
            )
        )


@dataclass
class DelegationRuntime:
    """Runtime state used by planner tools to spawn fresh bounded subagents."""

    agent_config: AgentConfig
    run_config: RunConfig
    task_context: Dict[str, Any]
    base_tools: Sequence[Any]
    max_search_subagent_calls: int = 3
    max_inspect_subagent_calls: int = 8

    def run_search_contract(self, contract: SearchContract) -> Dict[str, Any]:
        tools = tools_for_search_subagent(self.base_tools)
        source_hints: List[Dict[str, str]] = []
        search_mode = (self.run_config.search_tool_mode or "").strip().lower()
        if search_mode == "preloaded":
            source_hints = _source_hints_from_sequence(
                [],
                _preloaded_source_sequence(self.task_context),
                include_all=True,
            )
        prompt = _format_search_prompt(contract, source_hints=source_hints)
        return self._run_agent_contract(
            kind="search",
            contract_id=contract.contract_id,
            contract=contract,
            tools=tools,
            return_tool_name="return_search_result",
            build_return_tool=_build_search_return_tool,
            prompt=prompt,
            status_values=_VALID_SEARCH_STATUS,
        )

    def run_inspect_contract(self, contract: InspectContract) -> Dict[str, Any]:
        tools = tools_for_inspect_subagent(self.base_tools)
        source_hints: List[Dict[str, str]] = []
        search_mode = (self.run_config.search_tool_mode or "").strip().lower()
        if search_mode == "preloaded":
            source_hints = _source_hints_from_sequence(
                contract.source_family_ids,
                _preloaded_source_sequence(self.task_context),
            )
        prompt = _format_inspect_prompt(contract, source_hints=source_hints)
        return self._run_agent_contract(
            kind="inspect",
            contract_id=contract.contract_id,
            contract=contract,
            tools=tools,
            return_tool_name="return_inspect_result",
            build_return_tool=_build_inspect_return_tool,
            prompt=prompt,
            status_values=_VALID_INSPECT_STATUS,
            extra_plugins=[_InspectSourceGuard(contract.source_family_ids)],
        )

    def _run_agent_contract(
        self,
        *,
        kind: str,
        contract_id: str,
        contract: Any,
        tools: Sequence[Any],
        return_tool_name: str,
        build_return_tool,
        prompt: str,
        status_values: set[str],
        extra_plugins: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        result_state: Dict[str, Any] = {}
        return_tool = build_return_tool(result_state)
        ledger = _SubagentToolLedger(return_tool_name)
        max_calls = int(getattr(contract, "budget_calls", 1) or 1)
        plugins: List[Any] = [
            _SubagentBudgetSteer(
                ledger=ledger,
                max_tool_calls=max_calls,
                return_tool_name=return_tool_name,
                grace_tool_calls=_SUBAGENT_GRACE_TOOL_CALLS,
            ),
            ledger,
            LoggingPlugin(),
        ]
        if extra_plugins:
            plugins.extend(extra_plugins)

        write_trace_record(
            {
                "event": "delegation_subagent_start",
                "subagent_kind": kind,
                "contract_id": contract_id,
                "budget_calls": max_calls,
                "grace_tool_calls": _SUBAGENT_GRACE_TOOL_CALLS,
                "hard_budget_calls": max_calls + _SUBAGENT_GRACE_TOOL_CALLS,
            }
        )

        agent_result = None
        try:
            agent = Agent(
                model=build_model(self.agent_config),
                system_prompt=_subagent_system_prompt(kind, return_tool_name),
                tools=[*tools, return_tool],
                plugins=plugins,
                callback_handler=None,
            )
            agent_result = agent(prompt)
        except Exception as exc:
            logger.warning("%s subagent failed contract %s: %s", kind, contract_id, exc)
            payload = _contract_failure(
                kind=kind,
                contract_id=contract_id,
                reason=f"{type(exc).__name__}: {exc}",
                ledger=ledger,
                agent_result=agent_result,
            )
        else:
            if result_state.get("payload"):
                payload = dict(result_state["payload"])
            else:
                status = "budget_exhausted" if ledger.tool_calls >= max_calls else "failed"
                payload = _contract_failure(
                    kind=kind,
                    contract_id=contract_id,
                    reason=f"Subagent ended without calling {return_tool_name}.",
                    ledger=ledger,
                    agent_result=agent_result,
                    status=status,
                )

        payload.setdefault("contract_id", contract_id)
        payload["status"] = payload.get("status") if payload.get("status") in status_values else "failed"
        usage = _metrics_usage(agent_result)
        cost_usd = _cost_usd(self.agent_config.model_name, usage)
        payload["subagent_stats"] = {
            **payload.get("subagent_stats", {}),
            "subagent_kind": kind,
            "model_name": self.agent_config.model_name,
            "budget_calls": max_calls,
            "grace_tool_calls": _SUBAGENT_GRACE_TOOL_CALLS,
            "hard_budget_calls": max_calls + _SUBAGENT_GRACE_TOOL_CALLS,
            "requested_budget_calls": int(getattr(contract, "requested_budget_calls", max_calls) or max_calls),
            "tool_calls": ledger.tool_calls,
            "tools_used": list(ledger.tools_used),
            **usage,
            "cost_usd": cost_usd,
        }
        write_trace_record(
            {
                "event": "delegation_subagent_end",
                "subagent_kind": kind,
                "contract_id": contract_id,
                "status": payload.get("status"),
                "budget_calls": max_calls,
                "grace_tool_calls": _SUBAGENT_GRACE_TOOL_CALLS,
                "hard_budget_calls": max_calls + _SUBAGENT_GRACE_TOOL_CALLS,
                "tool_calls": ledger.tool_calls,
                "tools_used": list(ledger.tools_used),
                **usage,
                "cost_usd": cost_usd,
            }
        )
        return payload


def _contract_failure(
    *,
    kind: str,
    contract_id: str,
    reason: str,
    ledger: _SubagentToolLedger,
    agent_result: Any,
    status: str = "failed",
) -> Dict[str, Any]:
    if kind == "search":
        return {
            "status": status,
            "contract_id": contract_id,
            "candidates": [],
            "search_summary": "",
            "missing_or_uncertain_coverage": [reason],
            "retry_recommended": status != "budget_exhausted",
            "failure_reason": reason,
            "subagent_stats": {
                "tool_calls": ledger.tool_calls,
                "tools_used": list(ledger.tools_used),
                **_metrics_usage(agent_result),
            },
        }
    return {
        "status": status,
        "contract_id": contract_id,
        "answer_fragments": [],
        "missing_outputs": [],
        "evidence": [],
        "executor_summary": "",
        "retry_recommended": status != "budget_exhausted",
        "failure_reason": reason,
        "subagent_stats": {
            "tool_calls": ledger.tool_calls,
            "tools_used": list(ledger.tools_used),
            **_metrics_usage(agent_result),
        },
    }


def _subagent_system_prompt(kind: str, return_tool_name: str) -> str:
    if kind == "search":
        role = (
            "You are a bounded dataset-search worker. Find useful datasets for the "
            "contract. You may use search and peek/profile tools only. Do not "
            "perform the final computation."
        )
    else:
        role = (
            "You are a bounded tabular-inspection worker. Inspect only the explicit "
            "dataset ids in the contract, handle schema/query/parsing issues locally, "
            "and return compact extracted evidence. For text-based sources, use "
            "`grep_file` or `read_file` to inspect content."
        )
    return (
        role
        + "\nCall `"
        + return_tool_name
        + "` exactly once before finishing. Return compact summaries only; do not "
        "include raw row dumps, long schemas, or full tracebacks."
    )


def _json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def _format_search_prompt(
    contract: SearchContract,
    *,
    source_hints: Optional[List[Dict[str, str]]] = None,
) -> str:
    source_hint_block = ""
    if source_hints:
        source_hint_block = (
            "Preloaded candidate sources:\n"
            f"{_json_block(source_hints)}\n"
            "If a candidate satisfies the contract, return candidates from this list "
            "with its exact `s3_uri`; do not claim no search tool is available.\n"
        )
    return (
        f"Contract id: {contract.contract_id}\n"
        f"Search goal: {contract.search_goal}\n"
        f"Required source traits:\n{_json_block(contract.required_source_traits)}\n"
        f"{source_hint_block}"
        f"Constraints:\n{_json_block(contract.constraints)}\n"
        f"Known context:\n{contract.known_context or '(none)'}\n"
        f"Budget: {contract.budget_calls} tool calls, plus one grace call if needed, "
        "before returning a result.\n"
    )


def _format_inspect_prompt(
    contract: InspectContract,
    *,
    source_hints: Optional[List[Dict[str, str]]] = None,
) -> str:
    source_hint_block = ""
    if source_hints:
        source_hint_block = (
            "Known source file hints:\n"
            f"{_json_block(source_hints)}\n"
            "When a source hint is present, pass the exact `s3_uri` directly "
            "to file tools. Do not guess file paths.\n"
        )
    return (
        f"Contract id: {contract.contract_id}\n"
        f"Objective: {contract.objective}\n"
        f"Source family dataset ids:\n{_json_block(contract.source_family_ids)}\n"
        f"{source_hint_block}"
        f"Required outputs:\n{_json_block(contract.required_outputs)}\n"
        f"Success criteria: {contract.success_criteria}\n"
        f"Constraints:\n{_json_block(contract.constraints)}\n"
        f"Known context:\n{contract.known_context or '(none)'}\n"
        f"Retry of contract id: {contract.retry_of_contract_id or '(none)'}\n"
        "For text-based result sources, prefer `grep_file` or `read_file` over SQL.\n"
        f"Budget: {contract.budget_calls} tool calls, plus one grace call if needed, "
        "before returning a result.\n"
    )


def _build_search_return_tool(result_state: Dict[str, Any]):
    @tool(context=True)
    def return_search_result(
        status: str,
        search_summary: str,
        tool_context: ToolContext,
        candidates: Optional[List[Dict[str, Any]]] = None,
        missing_or_uncertain_coverage: Optional[List[str]] = None,
        retry_recommended: bool = False,
        failure_reason: str = "",
    ) -> str:
        """Return compact dataset candidates for a search contract. Call exactly once."""

        result_state["payload"] = {
            "status": status,
            "candidates": candidates or [],
            "search_summary": search_summary,
            "missing_or_uncertain_coverage": missing_or_uncertain_coverage or [],
            "retry_recommended": bool(retry_recommended),
            "failure_reason": failure_reason,
        }
        tool_context.agent.cancel()
        return "Search contract result recorded."

    return return_search_result


def _build_inspect_return_tool(result_state: Dict[str, Any]):
    @tool(context=True)
    def return_inspect_result(
        status: str,
        tool_context: ToolContext,
        answer_fragments: Optional[List[Dict[str, Any]]] = None,
        missing_outputs: Optional[List[str]] = None,
        evidence: Optional[List[str]] = None,
        executor_summary: str = "",
        retry_recommended: bool = False,
        failure_reason: str = "",
    ) -> str:
        """Return compact extraction results for an inspection contract. Call exactly once."""

        result_state["payload"] = {
            "status": status,
            "answer_fragments": answer_fragments or [],
            "missing_outputs": missing_outputs or [],
            "evidence": evidence or [],
            "executor_summary": executor_summary,
            "retry_recommended": bool(retry_recommended),
            "failure_reason": failure_reason,
        }
        tool_context.agent.cancel()
        return "Inspection contract result recorded."

    return return_inspect_result


@tool
def search_subagent(
    contract_id: str,
    search_goal: str,
    required_source_traits: List[str],
    budget_calls: int,
    constraints: Optional[List[str]] = None,
    known_context: str = "",
) -> Dict[str, Any]:
    """Ask a bounded search subagent to find useful datasets for the planner."""

    runtime = _RUNTIME
    clean_contract_id = _clean_str(contract_id)
    if runtime is None:
        return _search_failure_payload(clean_contract_id, "Delegation runtime is not initialized.")
    if not clean_contract_id:
        return _search_failure_payload("", "contract_id is required.")
    clean_goal = _clean_str(search_goal)
    if not clean_goal:
        return _search_failure_payload(clean_contract_id, "search_goal is required.")
    traits = _clean_list(required_source_traits)
    if not traits:
        return _search_failure_payload(clean_contract_id, "required_source_traits must be a non-empty list.")
    requested = _positive_int(budget_calls, default=1)
    budget = min(requested, int(runtime.max_search_subagent_calls))
    contract = SearchContract(
        contract_id=clean_contract_id,
        search_goal=clean_goal,
        required_source_traits=traits,
        budget_calls=budget,
        constraints=_clean_list(constraints),
        known_context=_clean_str(known_context),
        requested_budget_calls=requested,
    )
    return runtime.run_search_contract(contract)


@tool
def inspect_subagent(
    contract_id: str,
    objective: str,
    source_family_ids: List[str],
    required_outputs: List[str],
    success_criteria: str,
    budget_calls: int,
    constraints: Optional[List[str]] = None,
    known_context: str = "",
    retry_of_contract_id: str = "",
) -> Dict[str, Any]:
    """Ask a bounded inspector to extract outputs from explicit dataset ids."""

    runtime = _RUNTIME
    clean_contract_id = _clean_str(contract_id)
    if runtime is None:
        return _inspect_failure_payload(clean_contract_id, "Delegation runtime is not initialized.")
    if not clean_contract_id:
        return _inspect_failure_payload("", "contract_id is required.")
    clean_objective = _clean_str(objective)
    if not clean_objective:
        return _inspect_failure_payload(clean_contract_id, "objective is required.")
    source_ids = _clean_list(source_family_ids)
    if not source_ids:
        return _inspect_failure_payload(clean_contract_id, "source_family_ids must be a non-empty list.")
    outputs = _clean_list(required_outputs)
    if not outputs:
        return _inspect_failure_payload(clean_contract_id, "required_outputs must be a non-empty list.")
    clean_success = _clean_str(success_criteria)
    if not clean_success:
        return _inspect_failure_payload(clean_contract_id, "success_criteria is required.")
    requested = _positive_int(budget_calls, default=1)
    budget = min(requested, int(runtime.max_inspect_subagent_calls))
    contract = InspectContract(
        contract_id=clean_contract_id,
        objective=clean_objective,
        source_family_ids=source_ids,
        required_outputs=outputs,
        success_criteria=clean_success,
        budget_calls=budget,
        constraints=_clean_list(constraints),
        known_context=_clean_str(known_context),
        retry_of_contract_id=_clean_str(retry_of_contract_id),
        requested_budget_calls=requested,
    )
    return runtime.run_inspect_contract(contract)


__all__ = [
    "DelegationRuntime",
    "InspectContract",
    "SearchContract",
    "clear_delegation_runtime",
    "current_delegation_runtime",
    "inspect_subagent",
    "search_subagent",
    "set_delegation_runtime",
    "tool_names",
    "tools_for_delegation_planner",
    "tools_for_inspect_subagent",
    "tools_for_search_subagent",
]
