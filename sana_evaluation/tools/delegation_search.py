"""Search-side delegation contract and planner tool."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from strands import tool
from strands.types.tools import ToolContext

from sana_evaluation.tools.delegation_common import (
    _clean_list,
    _clean_str,
    _json_block,
    _positive_int,
    _tool_name,
    current_delegation_runtime,
)


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

_VALID_SEARCH_STATUS = {"success", "partial", "failed", "budget_exhausted"}


@dataclass
class SearchContract:
    contract_id: str
    search_goal: str
    required_source_traits: List[str]
    budget_calls: int
    constraints: List[str] = field(default_factory=list)
    known_context: str = ""
    requested_budget_calls: int = 0


def tools_for_search_subagent(tools: Sequence[Any]) -> List[Any]:
    """Return search-worker tools: retrieval plus light peek/profile only."""

    allowed = _SEARCH_TOOL_NAMES | _LIGHT_PEEK_TOOL_NAMES
    return [tool_obj for tool_obj in tools if _tool_name(tool_obj) in allowed]


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
            "with its exact `s3_uri`; do not claim no search tool is available. If "
            "you inspect a candidate, pass its exact `s3_uri` to file tools.\n"
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

    runtime = current_delegation_runtime()
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


__all__ = [
    "SearchContract",
    "_VALID_SEARCH_STATUS",
    "_build_search_return_tool",
    "_format_search_prompt",
    "search_subagent",
    "tools_for_search_subagent",
]
