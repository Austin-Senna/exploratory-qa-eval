"""Planner-facing delegation runtime and public facade."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from strands import Agent

from strands_evaluation.config import AgentConfig, RunConfig
from strands_evaluation.instrumentation.agent_plugins import LoggingPlugin
from strands_evaluation.instrumentation.trace_plugin import write_trace_record
from strands_evaluation.llm.llm_factory import build_model

from sana_evaluation.instrumentation.delegation_subagent_costs import (
    record_subagent_call as record_delegation_subagent_call,
)
from sana_evaluation.tools.delegation_common import (
    _FileReferenceGuard,
    _SUBAGENT_GRACE_TOOL_CALLS,
    _SubagentBudgetSteer,
    _SubagentToolLedger,
    _contract_failure,
    _preloaded_source_sequence,
    _source_hints_from_sequence,
    _subagent_system_prompt,
    _tool_name,
    clear_delegation_runtime,
    current_delegation_runtime,
    set_delegation_runtime,
    tool_names,
)
from sana_evaluation.tools.delegation_inspect import (
    InspectContract,
    _InspectSourceGuard,
    _VALID_INSPECT_STATUS,
    _build_inspect_return_tool,
    _format_inspect_prompt,
    inspect_subagent,
    tools_for_inspect_subagent,
)
from sana_evaluation.tools.delegation_search import (
    SearchContract,
    _VALID_SEARCH_STATUS,
    _build_search_return_tool,
    _format_search_prompt,
    search_subagent,
    tools_for_search_subagent,
)

logger = logging.getLogger(__name__)

_PLANNER_TOOL_NAMES = {
    "plan",
    "plan_ideal",
    "submit_answer",
}


def tools_for_delegation_planner(
    tools: Sequence[Any],
    *,
    include_search_subagent: bool = True,
) -> List[Any]:
    """Return planner tools plus the two delegation entrypoints."""

    out = [tool_obj for tool_obj in tools if _tool_name(tool_obj) in _PLANNER_TOOL_NAMES]
    existing = set(tool_names(out))
    if include_search_subagent and "search_subagent" not in existing:
        out.append(search_subagent)
    if "inspect_subagent" not in existing:
        out.append(inspect_subagent)
    return out


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
            _FileReferenceGuard(),
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
        requested_budget_calls = int(getattr(contract, "requested_budget_calls", max_calls) or max_calls)
        model_name = self.agent_config.model_name or self.agent_config.model_id
        cost_record = record_delegation_subagent_call(
            tool=f"{kind}_subagent",
            subagent_kind=kind,
            model_name=model_name,
            agent_result=agent_result,
            success=payload["status"] in {"success", "partial"},
            contract_id=contract_id,
            status=payload["status"],
            budget_calls=max_calls,
            requested_budget_calls=requested_budget_calls,
            grace_tool_calls=_SUBAGENT_GRACE_TOOL_CALLS,
            hard_budget_calls=max_calls + _SUBAGENT_GRACE_TOOL_CALLS,
            tool_calls=ledger.tool_calls,
            tools_used=list(ledger.tools_used),
        )
        usage = {
            "input_tokens": int(cost_record.get("input_tokens") or 0),
            "cached_input_tokens": int(cost_record.get("cached_input_tokens") or 0),
            "uncached_input_tokens": int(cost_record.get("uncached_input_tokens") or 0),
            "output_tokens": int(cost_record.get("output_tokens") or 0),
            "total_tokens": int(cost_record.get("total_tokens") or 0),
        }
        cost_usd = float(cost_record.get("cost_usd") or 0.0)
        payload["subagent_stats"] = {
            **payload.get("subagent_stats", {}),
            "subagent_kind": kind,
            "model_name": model_name,
            "budget_calls": max_calls,
            "grace_tool_calls": _SUBAGENT_GRACE_TOOL_CALLS,
            "hard_budget_calls": max_calls + _SUBAGENT_GRACE_TOOL_CALLS,
            "requested_budget_calls": requested_budget_calls,
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
