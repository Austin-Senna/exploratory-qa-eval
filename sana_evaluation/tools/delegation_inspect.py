"""Inspection-side delegation contract and planner tool."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from strands import tool
from strands.types.tools import ToolContext
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction

from sana_evaluation.tools.delegation_common import (
    _clean_list,
    _clean_str,
    _json_block,
    _positive_int,
    _source_id_from_reference,
    _tool_name,
    current_delegation_runtime,
)


_PARTIAL_OR_SUCCESS_STATUS = {"success", "partial"}


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
}

_VALID_INSPECT_STATUS = {"success", "partial", "failed", "budget_exhausted"}


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


def tools_for_inspect_subagent(tools: Sequence[Any]) -> List[Any]:
    """Return inspector tools: data inspection/query/execution, excluding planner tools."""

    return [tool_obj for tool_obj in tools if _tool_name(tool_obj) in _INSPECT_TOOL_NAMES]


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
            "to file tools. Do not guess file paths. Never call file tools with only a dataset_id.\n"
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
        "Every file tool call must include `s3_uri`, or both `dataset_id` and `file_path`.\n"
        f"Budget: {contract.budget_calls} tool calls, plus one grace call if needed, "
        "before returning a result.\n"
        "When you call `return_inspect_result` with status=success or status=partial, "
        "you MUST fill `answer_fragments` with the derived value(s) for "
        "`required_outputs` and list short pointers to the files/queries you used in "
        "`evidence`, e.g. "
        '`answer_fragments=[{"output": "<required output>", "value": <value>, '
        '"source_s3_uri": "s3://..."}]` and `evidence=["peek_file(s3://...)"]`. '
        "Empty results with a success status will be treated as a contract failure.\n"
    )


def _build_inspect_return_tool(
    result_state: Dict[str, Any],
    captured_evidence_getter: Optional[Any] = None,
):
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
        """Return compact extraction results for an inspection contract. Call EXACTLY once.

        When status is "success" or "partial":
          - `answer_fragments` MUST list the derived values for the contract's
            `required_outputs`, e.g.
              [{"output": "2020 deaths", "value": 91799,
                "source_s3_uri": "s3://..."}]
          - `evidence` MUST list short pointers to the files/queries you used,
            e.g. ["peek_file(s3://...rows.txt)"].
        Use status="failed" only if no required output could be derived.
        """

        resolved_evidence = list(evidence or [])
        if (
            not resolved_evidence
            and status in _PARTIAL_OR_SUCCESS_STATUS
            and callable(captured_evidence_getter)
        ):
            resolved_evidence = list(captured_evidence_getter() or [])
        result_state["payload"] = {
            "status": status,
            "answer_fragments": answer_fragments or [],
            "missing_outputs": missing_outputs or [],
            "evidence": resolved_evidence,
            "executor_summary": executor_summary,
            "retry_recommended": bool(retry_recommended),
            "failure_reason": failure_reason,
        }
        tool_context.agent.cancel()
        return "Inspection contract result recorded."

    return return_inspect_result


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

    runtime = current_delegation_runtime()
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
    "InspectContract",
    "_InspectSourceGuard",
    "_VALID_INSPECT_STATUS",
    "_build_inspect_return_tool",
    "_format_inspect_prompt",
    "inspect_subagent",
    "tools_for_inspect_subagent",
]
