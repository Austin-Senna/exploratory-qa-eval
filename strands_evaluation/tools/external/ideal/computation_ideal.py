"""Ideal computation tools backed by authored plan records."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from strands import Agent, tool

from strands_evaluation.config import AgentConfig
from strands_evaluation.llm.llm_factory import build_model
from strands_evaluation.tools.agent_tools import _get_sandbox_dir, execute_code as _execute_code_tool
from strands_evaluation.tools.agent_tools_v2 import peek_file as _peek_file_tool
from strands_evaluation.tools.agent_tools_v2 import query_file as _query_file_tool
from strands_evaluation.tools.external.ideal.plan_store import (
    IdealComputationRecord,
    IdealTaskPlan,
    load_plan_for_context,
    set_task_context as _set_task_context_shared,
)

logger = logging.getLogger(__name__)

_S3_PREFIX = "s3://lakeqa-yc4103-datalake/"
_MAX_REPAIR_ATTEMPTS = 2
_TASK_CONTEXT: Dict[str, Any] = {}
_ACTIVE_PLAN: Optional[IdealTaskPlan] = None
_STATS: Dict[str, int] = {
    "execute_ideal_agent_repair_calls": 0,
    "query_ideal_agent_repair_calls": 0,
}

_base_query_file = getattr(_query_file_tool, "_tool_func", _query_file_tool)
_base_execute_code = getattr(_execute_code_tool, "_tool_func", _execute_code_tool)
_base_peek_file = getattr(_peek_file_tool, "_tool_func", _peek_file_tool)


def set_task_context(task_context: Dict[str, Any]) -> None:
    """Load the active task's ideal computation records."""
    global _TASK_CONTEXT, _ACTIVE_PLAN
    _TASK_CONTEXT = dict(task_context or {})
    _set_task_context_shared(_TASK_CONTEXT)
    _ACTIVE_PLAN = load_plan_for_context(_TASK_CONTEXT)
    reset_stats()


def reset_state() -> None:
    """Reset in-process ideal computation state."""
    global _TASK_CONTEXT, _ACTIVE_PLAN
    _TASK_CONTEXT = {}
    _ACTIVE_PLAN = None
    _set_task_context_shared({})
    reset_stats()


def reset_stats() -> None:
    """Reset per-task ideal computation instrumentation counters."""
    for key in _STATS:
        _STATS[key] = 0


def get_stats() -> Dict[str, int]:
    """Return per-task ideal computation instrumentation counters."""
    return dict(_STATS)


def _record_repair_event(tool_name: str, event: str, **fields: Any) -> None:
    try:
        from strands_evaluation.instrumentation.trace_plugin import write_trace_record
    except Exception:
        return
    write_trace_record({"tool": tool_name, "event": event, **fields})


def _active_plan() -> IdealTaskPlan:
    if _ACTIVE_PLAN is not None:
        return _ACTIVE_PLAN
    return load_plan_for_context(_TASK_CONTEXT)


def _dataset_id_from_source(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.startswith(_S3_PREFIX):
        text = text[len(_S3_PREFIX) :]
    elif text.startswith("s3://"):
        text = text.split("/", 3)[-1]
    text = text.lstrip("/")
    parts = text.split("/")
    if len(parts) >= 2 and parts[0] in {"datagov", "wikipedia"}:
        return parts[1]
    return parts[0]


def _canonical_uri(source: str) -> str:
    source = str(source or "").strip()
    if source.startswith("s3://"):
        return source
    return _S3_PREFIX + source.lstrip("/")


def _tokens(text: Any) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(text or "").lower()))


def _overlap_score(a: Any, b: Any) -> float:
    left = _tokens(a)
    right = _tokens(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _source_filter(records: Iterable[IdealComputationRecord], dataset_id: str, source: str) -> List[IdealComputationRecord]:
    dataset_id = _dataset_id_from_source(dataset_id)
    source_dataset = _dataset_id_from_source(source)
    wanted = dataset_id or source_dataset
    records = list(records)
    if not wanted:
        return records
    return [record for record in records if record.dataset_id == wanted]


def _best_record(
    records: Iterable[IdealComputationRecord],
    *,
    payload: str,
    intent: str,
    dataset_id: str = "",
    source: str = "",
) -> Optional[IdealComputationRecord]:
    candidates = _source_filter(records, dataset_id, source)
    if not candidates:
        return None

    scored: List[tuple[float, IdealComputationRecord]] = []
    normalized_payload = " ".join(str(payload or "").split()).lower()
    for record in candidates:
        score = 0.0
        payload_exact = False
        if normalized_payload and normalized_payload == " ".join(record.payload.split()).lower():
            payload_exact = True
            score += 3.0
        intent_score = _overlap_score(intent, record.intent)
        payload_score = _overlap_score(payload, record.payload)
        if not payload_exact and intent_score < 0.34 and payload_score < 0.65:
            continue
        score += intent_score * 2.0
        score += payload_score
        scored.append((score, record))

    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        return None
    best_score, best = scored[0]
    return best if best_score >= 0.9 else None


def _s3_uri_for_record(record: IdealComputationRecord) -> str:
    return _canonical_uri(record.source)


def _file_path_for_record(record: IdealComputationRecord) -> str:
    marker = f"/{record.dataset_id}/"
    if marker in record.source:
        return record.source.split(marker, 1)[1]
    parts = record.source.split("/")
    if len(parts) >= 3 and parts[1] == record.dataset_id:
        return "/".join(parts[2:])
    return record.source


def _query_answer_payload(record: IdealComputationRecord) -> Dict[str, Any]:
    return {
        "success": True,
        "dataset_id": record.dataset_id,
        "file_path": _file_path_for_record(record),
        "s3_uri": _s3_uri_for_record(record),
        "columns": ["answer"],
        "rows": [[record.answer]],
        "row_count": 1,
        "truncated": False,
    }


def _execute_answer_payload(record: IdealComputationRecord) -> Dict[str, Any]:
    return {
        "output": str(record.answer),
        "success": True,
    }


def _is_success(result: Any) -> bool:
    if not isinstance(result, dict):
        return False
    if result.get("success") is False:
        return False
    return "error" not in result


def _decorate_repair_result(result: Dict[str, Any], *, attempts: int, repairs: List[Dict[str, str]]) -> Dict[str, Any]:
    _ = attempts, repairs
    return dict(result)


def _plan_records_for_prompt(plan: IdealTaskPlan, records: Iterable[IdealComputationRecord]) -> str:
    rows = []
    for record in records:
        rows.append(
            {
                "node_id": record.node_id,
                "dataset_id": record.dataset_id,
                "source": record.source,
                "intent": record.intent,
                "payload": record.payload,
                "answer": record.answer,
            }
        )
    return json.dumps(
        {
            "task_id": plan.task_id,
            "plan_path": str(plan.plan_path),
            "records": rows,
        },
        ensure_ascii=False,
        indent=2,
    )


def _profile_context(source: str) -> str:
    if not source:
        return ""
    try:
        from strands_evaluation.helper.peek_profile import load_dataset_profile
    except Exception:
        return ""
    try:
        profile = load_dataset_profile(_canonical_uri(source))
    except Exception:
        profile = None
    if profile is None:
        return ""
    return json.dumps(profile, ensure_ascii=False)[:6000]


def _enhanced_peek_context(source: str) -> str:
    if not source:
        return ""
    s3_uri = _canonical_uri(source)
    payload: Dict[str, Any] = {"s3_uri": s3_uri}
    try:
        peek = _base_peek_file(s3_uri=s3_uri, max_rows=5)
    except Exception as exc:
        peek = {"error": f"enhanced peek failed: {type(exc).__name__}: {exc}"}
    payload["enhanced_peek_file"] = peek

    try:
        from strands_evaluation.helper.peek_profile import load_dataset_profile
        profile = load_dataset_profile(s3_uri)
    except Exception:
        profile = None
    if profile:
        payload["dataset_profile"] = profile
        description = profile.get("llm_description") or profile.get("description")
        if description:
            payload["dataset_description"] = str(description)

    return json.dumps(payload, ensure_ascii=False)[:10000]


def _target_sources_for_code(plan: IdealTaskPlan, code: str, intent: str) -> List[str]:
    scored: List[tuple[float, str]] = []
    code_text = str(code or "").lower()
    for record in plan.ideal_code:
        score = _overlap_score(intent, record.intent)
        if record.source and record.source.lower() in code_text:
            score += 3.0
        if record.dataset_id and record.dataset_id.lower() in code_text:
            score += 2.0
        scored.append((score, record.source))
    scored.sort(key=lambda item: item[0], reverse=True)
    out: List[str] = []
    for score, source in scored:
        if source and source not in out and (score > 0 or not out):
            out.append(source)
        if len(out) >= 3:
            break
    return out


def _target_dataset_context_for_code(plan: IdealTaskPlan, code: str, intent: str) -> str:
    contexts = []
    for source in _target_sources_for_code(plan, code, intent):
        context = _enhanced_peek_context(source)
        if context:
            contexts.append({"source": source, "context": json.loads(context)})
    if not contexts:
        return ""
    return json.dumps(contexts, ensure_ascii=False)[:12000]


def _sandbox_context() -> str:
    try:
        sandbox = _get_sandbox_dir()
    except Exception:
        return ""
    files: List[str] = []
    if Path(sandbox).exists():
        for path in Path(sandbox).rglob("*"):
            if path.is_file():
                try:
                    files.append(str(path.relative_to(sandbox)))
                except ValueError:
                    files.append(str(path))
    return json.dumps({"sandbox_dir": str(sandbox), "files": sorted(files)[:200]}, indent=2)


def _repair_model():
    return build_model(
        AgentConfig(
            model_name="openai/gpt-5.4",
            max_tokens=4096,
        )
    )


def _repair_query(
    *,
    plan: IdealTaskPlan,
    dataset_id: str,
    file_path: str,
    s3_uri: str,
    sql: str,
    intent: str,
    previous_error: str = "",
) -> Dict[str, str]:
    state: Dict[str, str] = {}

    @tool
    def submit_repaired_sql(sql: str, reason: str) -> str:
        """Submit the repaired SQL. Call exactly once."""
        state["sql"] = sql
        state["reason"] = reason
        return "repaired SQL recorded"

    source = s3_uri or ""
    if not source and dataset_id and file_path:
        source = f"datagov/{dataset_id}/{file_path.lstrip('/')}"
    records = _source_filter(plan.ideal_query, dataset_id, source)
    prompt = (
        "Rewrite the SQL so it accomplishes the user's intent against table alias t.\n"
        "Call submit_repaired_sql exactly once. Return only executable DuckDB SQL via the tool.\n\n"
        f"Intent:\n{intent}\n\nOriginal SQL:\n{sql}\n\nPrevious error:\n{previous_error}\n\n"
        f"Plan records:\n{_plan_records_for_prompt(plan, records)}\n\n"
        f"Profile context:\n{_profile_context(source)}\n\n"
        f"Target dataset context:\n{_enhanced_peek_context(source)}"
    )
    from strands_evaluation.instrumentation.agent_plugins import LoggingPlugin

    Agent(
        model=_repair_model(),
        system_prompt="You repair DuckDB SQL for a benchmark tool call.",
        tools=[submit_repaired_sql],
        plugins=[LoggingPlugin()],
        callback_handler=None,
    )(prompt)
    return state


def _repair_code(
    *,
    plan: IdealTaskPlan,
    code: str,
    intent: str,
    previous_error: str = "",
) -> Dict[str, str]:
    state: Dict[str, str] = {}

    @tool
    def submit_repaired_code(code: str, reason: str) -> str:
        """Submit the repaired Python code. Call exactly once."""
        state["code"] = code
        state["reason"] = reason
        return "repaired code recorded"

    prompt = (
        "Rewrite the Python code so it accomplishes the user's intent in the sandbox.\n"
        "The code must print the result. Call submit_repaired_code exactly once.\n\n"
        f"Intent:\n{intent}\n\nOriginal code:\n{code}\n\nPrevious error:\n{previous_error}\n\n"
        f"Plan records:\n{_plan_records_for_prompt(plan, plan.ideal_code)}\n\n"
        f"Target dataset context:\n{_target_dataset_context_for_code(plan, code, intent)}\n\n"
        f"Sandbox context:\n{_sandbox_context()}"
    )
    from strands_evaluation.instrumentation.agent_plugins import LoggingPlugin

    Agent(
        model=_repair_model(),
        system_prompt="You repair Python data-analysis code for a benchmark tool call.",
        tools=[submit_repaired_code],
        plugins=[LoggingPlugin()],
        callback_handler=None,
    )(prompt)
    return state


@tool
def query_ideal(
    dataset_id: str | None = None,
    file_path: str | None = None,
    sql: str = "",
    s3_uri: str | None = None,
    intent: str = "",
) -> Dict[str, Any]:
    """
    Ideal SQL tool for tabular or JSON-like sources only.
    Do not use query_ideal for non-tabular/non-JSON sources such as
    Wikipedia/content.txt, prose/plain text, XML/KML, HTML, PDFs, or binary files.
    For XML/KML structured records, use parse_xml_records instead.
    """
    plan = _active_plan()
    dataset_id = dataset_id or ""
    file_path = file_path or ""
    s3_uri = s3_uri or ""
    record = _best_record(
        plan.ideal_query,
        payload=sql,
        intent=intent,
        dataset_id=dataset_id,
        source=s3_uri,
    )
    if record is not None:
        return _query_answer_payload(record)

    repairs: List[Dict[str, str]] = []
    previous_error = ""
    last_result: Dict[str, Any] = {
        "success": False,
        "error": "query_ideal did not execute; no repair attempted.",
    }
    for attempt in range(1, _MAX_REPAIR_ATTEMPTS + 1):
        logger.info("query_ideal repair agent invoked attempt=%s", attempt)
        _STATS["query_ideal_agent_repair_calls"] += 1
        _record_repair_event(
            "query_ideal",
            "repair_agent_invoked",
            attempt=attempt,
            previous_error=previous_error,
        )
        try:
            repaired = _repair_query(
                plan=plan,
                dataset_id=dataset_id,
                file_path=file_path,
                s3_uri=s3_uri,
                sql=sql,
                intent=intent,
                previous_error=previous_error,
            )
        except Exception as exc:
            error = f"SQL repair failed: {type(exc).__name__}: {exc}"
            _record_repair_event(
                "query_ideal",
                "repair_agent_failed",
                attempt=attempt,
                error=error,
            )
            repairs.append({"sql": "", "reason": "", "error": error})
            last_result = {"success": False, "error": error}
            previous_error = error
            continue
        repaired_sql = str(repaired.get("sql") or "").strip()
        _record_repair_event(
            "query_ideal",
            "repair_agent_completed",
            attempt=attempt,
            repair_reason=str(repaired.get("reason") or ""),
            submitted_sql=repaired_sql,
        )
        repairs.append({"sql": repaired_sql, "reason": str(repaired.get("reason") or "")})
        if not repaired_sql:
            last_result = {"success": False, "error": "SQL repair returned empty SQL."}
            previous_error = last_result["error"]
            continue
        last_result = _base_query_file(
            dataset_id=dataset_id,
            file_path=file_path,
            sql=repaired_sql,
            s3_uri=s3_uri,
        )
        if _is_success(last_result):
            return _decorate_repair_result(last_result, attempts=attempt, repairs=repairs)
        previous_error = str(last_result.get("error") or last_result)

    return _decorate_repair_result(last_result, attempts=len(repairs), repairs=repairs)


@tool
def execute_ideal(code: str, intent: str) -> Dict[str, Any]:
    """
    Ideal Python tool for tabular or JSON-like sources only.
    Do not use execute_ideal for non-tabular/non-JSON sources such as
    Wikipedia/content.txt, prose/plain text, XML/KML, HTML, PDFs, or binary files.
    For XML/KML structured records, use parse_xml_records instead.
    """
    plan = _active_plan()
    record = _best_record(plan.ideal_code, payload=code, intent=intent)
    if record is not None:
        return _execute_answer_payload(record)

    repairs: List[Dict[str, str]] = []
    previous_error = ""
    last_result: Dict[str, Any] = {
        "success": False,
        "error": "execute_ideal did not execute; no repair attempted.",
    }
    for attempt in range(1, _MAX_REPAIR_ATTEMPTS + 1):
        logger.info("execute_ideal repair agent invoked attempt=%s", attempt)
        _STATS["execute_ideal_agent_repair_calls"] += 1
        _record_repair_event(
            "execute_ideal",
            "repair_agent_invoked",
            attempt=attempt,
            previous_error=previous_error,
        )
        try:
            repaired = _repair_code(
                plan=plan,
                code=code,
                intent=intent,
                previous_error=previous_error,
            )
        except Exception as exc:
            error = f"Code repair failed: {type(exc).__name__}: {exc}"
            _record_repair_event(
                "execute_ideal",
                "repair_agent_failed",
                attempt=attempt,
                error=error,
            )
            repairs.append({"code": "", "reason": "", "error": error})
            last_result = {"success": False, "error": error}
            previous_error = error
            continue
        repaired_code = str(repaired.get("code") or "").strip()
        _record_repair_event(
            "execute_ideal",
            "repair_agent_completed",
            attempt=attempt,
            repair_reason=str(repaired.get("reason") or ""),
            submitted_code=repaired_code,
        )
        repairs.append({"code": repaired_code, "reason": str(repaired.get("reason") or "")})
        if not repaired_code:
            last_result = {"success": False, "error": "Code repair returned empty code."}
            previous_error = last_result["error"]
            continue
        last_result = _base_execute_code(repaired_code)
        if _is_success(last_result):
            return _decorate_repair_result(last_result, attempts=attempt, repairs=repairs)
        previous_error = str(last_result.get("error") or last_result)

    return _decorate_repair_result(last_result, attempts=len(repairs), repairs=repairs)


__all__ = [
    "execute_ideal",
    "query_ideal",
    "reset_state",
    "get_stats",
    "set_task_context",
]
