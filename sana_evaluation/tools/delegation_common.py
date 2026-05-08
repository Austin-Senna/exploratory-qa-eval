"""Shared helpers for Tabular SANA delegation subagents."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Protocol, Sequence

from strands import Plugin
from strands.hooks import AfterToolCallEvent
from strands.plugins import hook
from strands.vended_plugins.steering import Guide, Proceed, SteeringHandler, ToolSteeringAction


_SUBAGENT_GRACE_TOOL_CALLS = 1
_DATA_LAKE_BUCKET = "lakeqa-yc4103-datalake"
_DATA_LAKE_FOLDERS = {"datagov", "wikipedia"}
_SINGLE_FILE_REFERENCE_TOOLS = {
    "peek_file",
    "read_file",
    "grep_file",
    "parse_xml_records",
    "query_file",
}
_BATCH_FILE_REFERENCE_TOOLS = {
    "peek_multiple",
    "download",
}


class DelegationRuntimeProtocol(Protocol):
    max_search_subagent_calls: int
    max_inspect_subagent_calls: int

    def run_search_contract(self, contract: Any) -> Dict[str, Any]:
        ...

    def run_inspect_contract(self, contract: Any) -> Dict[str, Any]:
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


def _clean_str(value: Any) -> str:
    return str(value or "").strip()


def _clean_list(values: Optional[Sequence[Any]]) -> List[str]:
    if values is None:
        return []
    if isinstance(values, (str, bytes)):
        return [_clean_str(values)] if _clean_str(values) else []
    return [text for text in (_clean_str(value) for value in values) if text]


def _positive_int(value: Any, *, default: int = 1) -> int:
    try:
        out = int(value)
    except (TypeError, ValueError):
        return default
    return out if out > 0 else default


def _json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


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


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has_single_file_reference(tool_input: Dict[str, Any]) -> bool:
    if _has_text(tool_input.get("s3_uri") or tool_input.get("uri")):
        return True
    return _has_text(tool_input.get("dataset_id")) and _has_text(
        tool_input.get("file_path") or tool_input.get("path")
    )


def _batch_file_reference_error(tool_input: Dict[str, Any]) -> Optional[str]:
    files = tool_input.get("files")
    if files is None:
        files = tool_input.get("entries")
    if isinstance(files, str):
        return None if _has_text(files) else "empty string entry"
    if isinstance(files, dict):
        files = [files]
    if not isinstance(files, list) or not files:
        return "missing non-empty `files` list"
    for index, entry in enumerate(files, start=1):
        if isinstance(entry, str):
            if _has_text(entry):
                continue
            return f"entry {index} is empty"
        if not isinstance(entry, dict):
            return f"entry {index} is not a file reference object"
        if _has_single_file_reference(entry):
            continue
        return f"entry {index} is missing `s3_uri` or `dataset_id` + `file_path`"
    return None


class _FileReferenceGuard(SteeringHandler):
    name = "sana-delegation-file-reference-guard"

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        tool_name = (tool_use or {}).get("name", "")
        tool_input = (tool_use or {}).get("input", {}) or {}
        if tool_name in _SINGLE_FILE_REFERENCE_TOOLS:
            if _has_single_file_reference(tool_input):
                return Proceed(reason="file tool has exact file reference")
            return Guide(
                reason=(
                    f"`{tool_name}` must include an exact file reference: either `s3_uri`, "
                    "or both `dataset_id` and `file_path`. Do not call file tools with "
                    "a dataset_id alone. Use the source hints from the contract, or return "
                    "partial/failed if no exact file path is available."
                )
            )
        if tool_name in _BATCH_FILE_REFERENCE_TOOLS:
            error = _batch_file_reference_error(tool_input)
            if error is None:
                return Proceed(reason="batch file tool has exact file references")
            return Guide(
                reason=(
                    f"`{tool_name}` requires exact file references in `files`: each entry "
                    "must include `s3_uri`, or both `dataset_id` and `file_path`; "
                    f"{error}. Do not use dataset_id-only entries."
                )
            )
        return Proceed(reason="tool does not require file reference")


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
        + "\nFor every file tool call, pass an exact `s3_uri`, or pass both "
        "`dataset_id` and `file_path`; never call file tools with dataset_id alone."
        + "\nCall `"
        + return_tool_name
        + "` exactly once before finishing. Return compact summaries only; do not "
        "include raw row dumps, long schemas, or full tracebacks."
    )


__all__ = [
    "DelegationRuntimeProtocol",
    "_FileReferenceGuard",
    "_SubagentBudgetSteer",
    "_SubagentToolLedger",
    "_SUBAGENT_GRACE_TOOL_CALLS",
    "_clean_list",
    "_clean_str",
    "_contract_failure",
    "_cost_usd",
    "_json_block",
    "_metrics_usage",
    "_positive_int",
    "_preloaded_source_sequence",
    "_source_hints_from_sequence",
    "_source_id_from_reference",
    "_subagent_system_prompt",
    "_tool_name",
    "clear_delegation_runtime",
    "current_delegation_runtime",
    "set_delegation_runtime",
    "tool_names",
]
