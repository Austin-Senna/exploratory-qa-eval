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
        if getattr(event, "cancel_message", None):
            return
        self.tool_calls += 1
        self.tools_used.append(tool_name)


_SEARCH_RESULT_TOOL_NAMES = {
    "search_value",
    "search_schema",
    "search_reranked",
    "search_prefix",
    "search_ideal",
    "search",
    "search_keyword",
}


_COMPUTE_TOOLS = {"execute_code", "execute_ideal", "query_ideal"}


_COMPUTE_SUMMARY_MAX_CHARS = 60


def _result_payloads(result: Any) -> List[Any]:
    """Parse JSON payloads from a strands ToolResult content list."""

    if not isinstance(result, dict):
        return []
    payloads: List[Any] = []
    content = result.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if "json" in block and block["json"] is not None:
                payloads.append(block["json"])
                continue
            text = block.get("text")
            if isinstance(text, str) and text:
                try:
                    payloads.append(json.loads(text))
                except (json.JSONDecodeError, TypeError):
                    continue
    return payloads


def _result_is_error(result: Any) -> bool:
    """Return True when a strands ToolResult signals an error or logical failure."""

    if not isinstance(result, dict):
        return False
    raw_status = result.get("status")
    if isinstance(raw_status, str) and raw_status.strip().lower() == "error":
        return True
    for payload in _result_payloads(result):
        if isinstance(payload, dict) and (
            "error" in payload or payload.get("success") is False
        ):
            return True
    return False


def _candidate_records_from_payload(payload: Any) -> List[Dict[str, str]]:
    """Return [{'dataset_id': ..., 's3_uri': ...}] entries inside a search payload."""

    records: List[Dict[str, str]] = []
    if not isinstance(payload, dict):
        return records
    results = payload.get("results")
    if not isinstance(results, list):
        return records
    for entry in results:
        if not isinstance(entry, dict):
            continue
        s3_uri = _clean_str(entry.get("s3_uri") or entry.get("uri"))
        dataset_id = _clean_str(entry.get("dataset_id"))
        if not s3_uri and not dataset_id:
            continue
        record: Dict[str, str] = {}
        if dataset_id:
            record["dataset_id"] = dataset_id
        if s3_uri:
            record["s3_uri"] = s3_uri
        summary = _clean_str(entry.get("llm_desc") or entry.get("description") or entry.get("summary"))
        if summary:
            record["summary"] = summary
        records.append(record)
    return records


def _file_reference_from_tool_use(tool_use: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Return a short reference describing a single-file tool call's target."""

    tool_input = (tool_use or {}).get("input") or {}
    if not isinstance(tool_input, dict):
        return None
    s3_uri = _clean_str(tool_input.get("s3_uri") or tool_input.get("uri"))
    dataset_id = _clean_str(tool_input.get("dataset_id"))
    file_path = _clean_str(tool_input.get("file_path") or tool_input.get("path"))
    if not s3_uri and not (dataset_id and file_path):
        return None
    ref: Dict[str, str] = {}
    if dataset_id:
        ref["dataset_id"] = dataset_id
    if file_path:
        ref["file_path"] = file_path
    if s3_uri:
        ref["s3_uri"] = s3_uri
    return ref


def _file_references_from_batch_tool_use(tool_use: Dict[str, Any]) -> List[Dict[str, str]]:
    """Return file references for batch tool calls (peek_multiple/download)."""

    tool_input = (tool_use or {}).get("input") or {}
    if not isinstance(tool_input, dict):
        return []
    entries = tool_input.get("files")
    if entries is None:
        entries = tool_input.get("entries")
    if isinstance(entries, dict):
        entries = [entries]
    if not isinstance(entries, list):
        return []
    refs: List[Dict[str, str]] = []
    for entry in entries:
        if isinstance(entry, str):
            s3_uri = _clean_str(entry)
            if s3_uri:
                refs.append({"s3_uri": s3_uri})
            continue
        if not isinstance(entry, dict):
            continue
        ref = _file_reference_from_tool_use({"input": entry})
        if ref:
            refs.append(ref)
    return refs


def _summary_from_compute_tool_use(tool_use: Dict[str, Any]) -> str:
    """Return a short label for a compute tool invocation (execute_code / query_ideal)."""

    tool_input = (tool_use or {}).get("input") or {}
    if not isinstance(tool_input, dict):
        return ""
    raw = tool_input.get("code") or tool_input.get("sql") or tool_input.get("intent") or ""
    if not isinstance(raw, str):
        return ""
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:_COMPUTE_SUMMARY_MAX_CHARS]
    return raw.strip()[:_COMPUTE_SUMMARY_MAX_CHARS]


def _evidence_string_from_ref(tool_name: str, ref: Dict[str, str]) -> str:
    """Return a compact evidence string for a file-tool reference."""

    s3_uri = ref.get("s3_uri")
    if s3_uri:
        return f"{tool_name}({s3_uri})"
    dataset_id = ref.get("dataset_id")
    file_path = ref.get("file_path")
    if dataset_id and file_path:
        return f"{tool_name}({dataset_id}/{file_path})"
    if dataset_id:
        return f"{tool_name}({dataset_id})"
    return f"{tool_name}()"


class _SubagentResultCapture(Plugin):
    """Accumulates fallback contract-return values from tool outputs."""

    name = "sana-delegation-result-capture"

    def __init__(self, kind: str, return_tool_name: str) -> None:
        super().__init__()
        self.kind = kind
        self.return_tool_name = return_tool_name
        self._candidates: List[Dict[str, str]] = []
        self._seen_uris: set[str] = set()
        self._evidence: List[str] = []
        self._seen_evidence: set[str] = set()

    def captured_candidates(self) -> List[Dict[str, str]]:
        return [dict(record) for record in self._candidates]

    def captured_evidence(self) -> List[str]:
        return list(self._evidence)

    def _record_candidate(self, record: Dict[str, str]) -> None:
        key = record.get("s3_uri") or record.get("dataset_id") or ""
        if not key or key in self._seen_uris:
            return
        self._seen_uris.add(key)
        self._candidates.append(record)

    def _record_evidence(self, tool_name: str, ref: Dict[str, str]) -> None:
        entry = _evidence_string_from_ref(tool_name, ref)
        if not entry or entry in self._seen_evidence:
            return
        self._seen_evidence.add(entry)
        self._evidence.append(entry)

    def _record_compute_evidence(self, tool_name: str, summary: str) -> None:
        entry = f"{tool_name}({summary})" if summary else f"{tool_name}()"
        if entry in self._seen_evidence:
            return
        self._seen_evidence.add(entry)
        self._evidence.append(entry)

    @hook
    def on_after_tool(self, event: AfterToolCallEvent) -> None:
        tool_use = getattr(event, "tool_use", {}) or {}
        tool_name = tool_use.get("name", "")
        if not tool_name or tool_name == self.return_tool_name:
            return
        if getattr(event, "cancel_message", None):
            return
        result = getattr(event, "result", None)
        if _result_is_error(result):
            return

        if self.kind == "search" and tool_name in _SEARCH_RESULT_TOOL_NAMES:
            for payload in _result_payloads(result):
                for record in _candidate_records_from_payload(payload):
                    self._record_candidate(record)

        if self.kind == "inspect":
            if tool_name in _SINGLE_FILE_REFERENCE_TOOLS:
                ref = _file_reference_from_tool_use(tool_use)
                if ref:
                    self._record_evidence(tool_name, ref)
            elif tool_name in _BATCH_FILE_REFERENCE_TOOLS:
                for ref in _file_references_from_batch_tool_use(tool_use):
                    self._record_evidence(tool_name, ref)
            elif tool_name in _COMPUTE_TOOLS:
                summary = _summary_from_compute_tool_use(tool_use)
                self._record_compute_evidence(tool_name, summary)


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


_SEARCH_TOOL_CATALOG = """
TOOL PICKER (pick ONE primary search call per contract, then verify):
- search_ideal(query, top_k=100): preferred when search_results=ideal. Returns
  `results=[{dataset_id, s3_uri, ...}]`; the inner judge has already filtered.
  One focused query is usually enough.
- search_value(query, top_k=10): hybrid semantic+keyword over dataset content.
  Use when looking for a topic or phrase (e.g. "annual overdose deaths").
- search_schema(query, top_k=10): hybrid search over column names / schemas.
  Use when you need a dataset by column name (e.g. "Violent Count column").
- search_reranked(query, top_k=10): cross-encoder reranking on top of hybrid.
  Slower but more accurate; use when search_value is ambiguous.
- search_prefix(prefixes=[...]): S3 native prefix search across wikipedia/ and
  datagov/. Use for known entity name fragments (e.g. ["Erie_County"]).
- search_keyword(keywords=[...]): tag-style keyword filter. Use short tags
  (e.g. ["police", "crime"]), not sentences.

VERIFY: after a candidate is returned, call `peek_file(s3_uri=...)` (or
`peek_multiple(files=[...])` for several) to confirm columns / record_tag /
file family before you forward it. Do NOT call query_file, read_file,
grep_file, or execute_code — those belong to the inspect worker.
""".strip()


_INSPECT_TOOL_CATALOG = """
TOOL PICKER (know the schema before SQL; dispatch on `family`):
- Unknown family yet → `peek_file(s3_uri=...)` for one file, or
  `peek_multiple(files=[{s3_uri: ...}, ...])` for several. Read `family`,
  `header_columns`, `xml_record_tag_candidates`, and `size_bytes` from the
  response before choosing the next tool.

- NEVER call `query_file` on a file you do not know the schema of.

- family=csv → `query_file(s3_uri=..., sql="...")` with DuckDB. Table alias
  is `t`. Quote any column name with spaces or special chars:
  `WHERE "Poor Status" = 'Y'`. Use GROUP BY/HAVING for counts and thresholds.
  Results capped at 200 rows.

- family=json AND the file is a flat tabular array (one row per record) →
  `query_file` works the same as CSV.

- family=json AND the file is a nested FeatureCollection / large (>5MB) /
  GeoJSON / arbitrary nested → DO NOT call `query_file` (DuckDB sees one row
  at the top level). Instead:
    1. `download(files=[{"s3_uri": "..."}])`  (single call; ≤5 files).
    2. `execute_code(code='''
         import ijson
         from collections import Counter
         counts = Counter()
         path = SANDBOX_DIR + "/<dataset_id>/<file_path>"
         for feat in ijson.items(open(path, "rb"), "features.item"):
             props = feat.get("properties", {})
             if props.get("STATE") == "CA":
                 counts[props.get("NMCNTY")] += 1
         print(counts.most_common(3))
       ''')`
  `ijson` is pre-imported. `SANDBOX_DIR` is a pre-set variable.

- family=xml OR family=kml → `parse_xml_records(s3_uri=..., record_tag=...,
  fields=[...], filters={...}, group_by=[...], limit=200)`. `record_tag`
  comes from peek_file's `xml_record_tag_candidates` (e.g. "Placemark").
  NEVER call `query_file` or `execute_code` on XML/KML.

- family=text (wikipedia content.txt, prose, HTML) → `grep_file(s3_uri=...,
  regex_pattern="...", context_lines=2)` first to locate the relevant line,
  then `read_file(s3_uri=..., start_line=..., max_lines=120)` for context.
  NEVER call `query_file` or `execute_code` on prose. When asked for a
  specific fact (year, name, date), grep the authoritative article
  (e.g. `wikipedia/Holland_Land_Company/content.txt`), not a tangentially
  related one.

""".strip()


def _subagent_system_prompt(kind: str, return_tool_name: str) -> str:
    if kind == "search":
        role = (
            "You are a bounded dataset-search worker. Find dataset candidates for "
            "the contract. Do not perform the final computation; do not parse data."
        )
        tool_catalog = _SEARCH_TOOL_CATALOG
        return_requirement = (
            "When status is `success` or `partial`, you MUST populate `candidates` "
            "with every dataset you intend to forward. Each entry needs `dataset_id` "
            "and `s3_uri`; copy them verbatim from your search tool results. Use "
            "status `failed` only if no dataset matched."
        )
    else:
        role = (
            "You are a bounded tabular-inspection worker. Extract compact evidence "
            "from the contracted dataset ids. Do not search; do not pick the dataset."
        )
        tool_catalog = _INSPECT_TOOL_CATALOG
        return_requirement = (
            "When status is `success` or `partial`, you MUST populate "
            "`answer_fragments` with the derived values for `required_outputs` and "
            "list the files/queries you used in `evidence`. Use status `failed` only "
            "if no required output could be derived."
        )
    return (
        role
        + "\n\n"
        + tool_catalog
        + "\n\nEXACT FILE REFERENCES: every file tool call must pass an exact "
        "`s3_uri`, or pass both `dataset_id` and `file_path`; never call file "
        "tools with a bare `dataset_id`."
        + "\n\nRETURN: call `"
        + return_tool_name
        + "` EXACTLY once before finishing. Return compact summaries only; do not "
        "include raw row dumps, long schemas, or full tracebacks."
        + "\n" + return_requirement
    )


__all__ = [
    "DelegationRuntimeProtocol",
    "_FileReferenceGuard",
    "_SubagentBudgetSteer",
    "_SubagentResultCapture",
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
