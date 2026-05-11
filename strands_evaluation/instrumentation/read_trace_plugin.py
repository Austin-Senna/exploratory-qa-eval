"""
ReadTracePlugin — Strands Plugin that writes per-read-call JSONL traces.

Records which datasets were opened via read tools so D_read can be computed
in analysis/discovery_metrics.py. Shares the same per-task JSONL file as
TracePlugin (tool field distinguishes record types).

Call set_trace_context(...) once per task before agent.run() — same call used
by TracePlugin; no separate setup needed.
"""

import json
import time
from typing import Any, List

from strands import Plugin
from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent
from strands.plugins import hook

import strands_evaluation.instrumentation.trace_plugin as _tp
from strands_evaluation.instrumentation.trace_plugin import _normalize_dataset_id, _write_record

_READ_TOOLS = {
    "read_file",
    "peek_file",
    "peek_multiple",
    "grep_file",
    "parse_xml_records",
    "query_file",
    "query_ideal",
    "execute_ideal",
}


def _dataset_id_from_file_spec(file_spec) -> str:
    """Return a normalized dataset id from a file-tool input fragment."""
    if isinstance(file_spec, str):
        raw = file_spec
    elif isinstance(file_spec, dict):
        raw = (
            file_spec.get("dataset_id")
            or file_spec.get("s3_uri")
            or file_spec.get("uri")
            or ""
        )
    else:
        raw = ""
    return _normalize_dataset_id(raw) if raw else ""


def _extract_read_dataset_ids(tool_name: str, tool_input: dict) -> List[str]:
    """Return normalized dataset_id(s) from a read tool's input."""
    if tool_name == "peek_multiple":
        files = tool_input.get("files", [])
        if not isinstance(files, list):
            return []
        return [
            dataset_id
            for dataset_id in (_dataset_id_from_file_spec(file_spec) for file_spec in files)
            if dataset_id
        ]
    dataset_id = _dataset_id_from_file_spec(tool_input)
    if dataset_id:
        return [dataset_id]
    return []


def _result_status(result: dict) -> str:
    """Return success/error for metric purposes from a Strands tool result."""
    if not isinstance(result, dict):
        return "success"

    raw_status = result.get("status")
    if raw_status is not None:
        status = str(raw_status).strip().lower()
        if status and status != "success":
            return status

    content = result.get("content", [])
    if not isinstance(content, list):
        return "success"

    for block in content:
        if not isinstance(block, dict) or "text" not in block:
            continue
        try:
            parsed = json.loads(block["text"])
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(parsed, dict) and ("error" in parsed or parsed.get("success") is False):
            return "error"
    return "success"


def _tool_use_key(tool_use: dict[str, Any]) -> str:
    """Return a stable key for pairing before/after tool hook state."""
    return str(tool_use.get("toolUseId") or "__legacy_single_tool__")


class ReadTracePlugin(Plugin):
    """Writes per-call JSONL traces for read tools (D_read metric)."""

    name = "read-trace"

    def __init__(self) -> None:
        super().__init__()
        self._t0: float = 0.0
        self._pending_tool: str = ""
        self._started_at_by_tool_use: dict[str, float] = {}
        self.gold_datasets_read: set = set()


    @hook
    def on_before_tool(self, event: BeforeToolCallEvent) -> None:
        tool_name = event.tool_use.get("name", "")
        if tool_name not in _READ_TOOLS:
            return
        started_at = time.time()
        self._t0 = started_at
        self._pending_tool = tool_name
        self._started_at_by_tool_use[_tool_use_key(event.tool_use)] = started_at

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = event.tool_use.get("name", "")
        if tool_name not in _READ_TOOLS:
            return

        started_at = self._started_at_by_tool_use.pop(
            _tool_use_key(event.tool_use),
            self._t0,
        )
        latency_ms = int((time.time() - started_at) * 1000)
        tool_input = event.tool_use.get("input", {})
        attempted_read_ids = _extract_read_dataset_ids(tool_name, tool_input)
        status = _result_status(event.result)
        read_ids = attempted_read_ids if status == "success" else []
        gold_set = set(_tp._current_gold_ids)
        gold_read = [rid for rid in read_ids if rid in gold_set]

        self.gold_datasets_read.update(gold_read)

        _write_record({
            "task_id": _tp._current_task_id,
            "tool": tool_name,
            "status": status,
            "attempted_read_dataset_ids": attempted_read_ids,
            "read_dataset_ids": read_ids,
            "gold_dataset_ids_read": gold_read,
            "latency_ms": latency_ms,
            "timestamp_ms": int(time.time() * 1000),
        })
