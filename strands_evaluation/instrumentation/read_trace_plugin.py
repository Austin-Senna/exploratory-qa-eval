"""
ReadTracePlugin — Strands Plugin that writes per-read-call JSONL traces.

Records which datasets were opened via read tools so D_read can be computed
in analysis/discovery_metrics.py. Shares the same per-task JSONL file as
TracePlugin (tool field distinguishes record types).

Call set_trace_context(...) once per task before agent.run() — same call used
by TracePlugin; no separate setup needed.
"""

import time
from typing import List

from strands import Plugin
from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent
from strands.plugins import hook

from strands_evaluation.instrumentation.trace_plugin import (
    _current_gold_ids,
    _current_task_id,
    _normalize_dataset_id,
    _write_record,
)

_READ_TOOLS = {"read_file", "peek_file", "peek_files", "grep_file", "query_file"}


def _extract_read_dataset_ids(tool_name: str, tool_input: dict) -> List[str]:
    """Return normalized dataset_id(s) from a read tool's input."""
    if tool_name == "peek_files":
        files = tool_input.get("files", [])
        return [_normalize_dataset_id(f["dataset_id"]) for f in files if f.get("dataset_id")]
    raw = tool_input.get("dataset_id", "")
    if raw:
        return [_normalize_dataset_id(raw)]
    return []


class ReadTracePlugin(Plugin):
    """Writes per-call JSONL traces for read tools (D_read metric)."""

    name = "read-trace"

    def __init__(self) -> None:
        super().__init__()
        self._t0: float = 0.0
        self._pending_tool: str = ""

    @hook
    def on_before_tool(self, event: BeforeToolCallEvent) -> None:
        tool_name = event.tool_use.get("name", "")
        if tool_name not in _READ_TOOLS:
            return
        self._t0 = time.time()
        self._pending_tool = tool_name

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_name = event.tool_use.get("name", "")
        if tool_name not in _READ_TOOLS:
            return

        latency_ms = int((time.time() - self._t0) * 1000)
        tool_input = event.tool_use.get("input", {})
        read_ids = _extract_read_dataset_ids(tool_name, tool_input)
        gold_set = set(_current_gold_ids)
        gold_read = [rid for rid in read_ids if rid in gold_set]

        _write_record({
            "task_id": _current_task_id,
            "tool": tool_name,
            "read_dataset_ids": read_ids,
            "gold_dataset_ids_read": gold_read,
            "latency_ms": latency_ms,
            "timestamp_ms": int(time.time() * 1000),
        })
