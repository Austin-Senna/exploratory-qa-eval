#!/usr/bin/env python3
"""Build log-level execution inventories and event-level execution audits."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.trajectory_pair_analysis import (  # noqa: E402
    BENCHMARK_LOG_ROOTS,
    EXECUTING_RE,
    _append_journal_record,
    _parse_json_object,
    _strip_log_prefix,
    _truncate,
    call_openai,
    resolve_judge_limit,
)


PLAN_ROOTS = {
    "lakeqa": Path("plans_mini"),
    "kramabench": Path("plans-mini-kramabench"),
}
EXECUTION_TOOLS = {"execute_code", "query_file", "execute_ideal", "query_ideal"}
EVENT_TYPES = {
    "matched_execution",
    "mismatched_execution",
    "wrong_file_execution",
    "schema_metadata_inspection",
    "execution_failure",
    "missing_execution",
    "wasted_schema_inspection",
}
JUDGE_EVENT_TYPES = {"matched_execution", "mismatched_execution", "schema_metadata_inspection", "execution_failure"}
ERROR_TYPES = {
    "none",
    "wrong_file",
    "operation_binding",
    "filter_binding",
    "schema_error",
    "parse_error",
    "schema_metadata_inspection",
    "not_executed",
    "other",
}
EVENT_COLUMNS = [
    "benchmark",
    "model_variant",
    "mode",
    "task_id",
    "log_path",
    "plan_path",
    "event_id",
    "event_origin",
    "event_type",
    "command_index",
    "line_number",
    "tool",
    "bound_sources",
    "matched_ideal_record_keys",
    "ideal_record_key",
    "ideal_node_id",
    "ideal_record_types",
    "error_type",
    "reason",
    "evidence",
    "command_json",
    "ideal_record_json",
    "auditor_model",
    "audit_status",
]
INVENTORY_COLUMNS = [
    "benchmark",
    "model_variant",
    "mode",
    "task_id",
    "log_path",
    "plan_path",
    "n_execution_commands",
    "n_events",
    "n_pending_events",
    "n_matched_execution",
    "n_mismatched_execution",
    "n_wrong_file_execution",
    "n_schema_metadata_inspection",
    "n_execution_failure",
    "n_missing_execution",
    "n_wasted_schema_inspection",
    "source_sequence_json",
    "ideal_records_json",
    "execution_commands_json",
    "event_ids_json",
]
AUDIT_UPDATE_COLUMNS = [
    "event_type",
    "bound_sources",
    "matched_ideal_record_keys",
    "ideal_record_key",
    "ideal_node_id",
    "ideal_record_types",
    "error_type",
    "reason",
    "evidence",
    "auditor_model",
    "audit_status",
]


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _safe_json_loads(value: str) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def normalize_source(source: str) -> str:
    source = source.strip().strip("\"'")
    source = re.sub(r"^s3://[^/]+/", "", source)
    source = re.sub(r"^.*?/(datagov/|wikipedia/)", lambda m: m.group(1), source)
    return source.replace("\\", "/").lstrip("/")


def _mode_log_paths(log_root: Path) -> list[dict[str, str]]:
    modes_root = log_root / "modes"
    rows: list[dict[str, str]] = []
    if not modes_root.is_dir():
        return rows
    for log_path in sorted(modes_root.glob("*/*/**/*.log")):
        rel_parts = log_path.relative_to(modes_root).parts
        if len(rel_parts) < 4:
            continue
        model_variant, mode = rel_parts[0], rel_parts[1]
        task_id = Path(*rel_parts[2:]).with_suffix(".json").as_posix()
        rows.append(
            {
                "model_variant": model_variant,
                "mode": mode,
                "task_id": task_id,
                "log_path": str(log_path.resolve(strict=False)),
            }
        )
    return rows


def plan_path_for_task(repo_root: Path, benchmark: str, task_id: str) -> Path:
    parts = Path(task_id).parts
    if benchmark == "kramabench" and parts and parts[0] == "tasks-mini-kramabench":
        return repo_root / PLAN_ROOTS[benchmark] / Path(*parts[1:])
    if benchmark == "lakeqa" and parts and parts[0] == "tasks_mini":
        return repo_root / PLAN_ROOTS[benchmark] / Path(*parts[1:])
    return repo_root / PLAN_ROOTS[benchmark] / task_id


def load_plan_context(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"source_sequence": [], "ideal_records": [], "plan_error": "plan_missing"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"source_sequence": [], "ideal_records": [], "plan_error": f"plan_load_error:{exc}"}

    source_sequence = [normalize_source(str(source)) for source in data.get("source_sequence", [])]
    records_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for record_type in ["ideal_query", "ideal_code"]:
        records = data.get(record_type, [])
        if not isinstance(records, list):
            continue
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                continue
            node_id = str(record.get("node_id") or index)
            source = normalize_source(str(record.get("source") or ""))
            key = (node_id, source)
            merged = records_by_key.setdefault(
                key,
                {
                    "ideal_record_key": f"{node_id}:{source or 'no_source'}",
                    "node_id": node_id,
                    "source": source,
                    "dataset_id": str(record.get("dataset_id") or ""),
                    "intent": str(record.get("intent") or ""),
                    "answer": record.get("answer"),
                    "record_types": [],
                    "ideal_query": None,
                    "ideal_code": None,
                },
            )
            if record_type not in merged["record_types"]:
                merged["record_types"].append(record_type)
            if record.get("intent") and not merged.get("intent"):
                merged["intent"] = str(record.get("intent"))
            if record_type == "ideal_query":
                merged["ideal_query"] = {
                    "sql": record.get("sql", ""),
                    "intent": record.get("intent", ""),
                    "answer": record.get("answer"),
                }
            else:
                merged["ideal_code"] = {
                    "code": record.get("code", ""),
                    "intent": record.get("intent", ""),
                    "answer": record.get("answer"),
                }
    return {
        "source_sequence": source_sequence,
        "ideal_records": list(records_by_key.values()),
        "plan_error": "",
    }


def _extract_json_arg(stripped_line: str, tool: str) -> dict[str, Any]:
    marker = f"Executing: {tool}("
    start = stripped_line.find(marker)
    if start < 0:
        return {}
    arg_text = stripped_line[start + len(marker) :]
    if arg_text.endswith(")"):
        arg_text = arg_text[:-1]
    try:
        value = json.loads(arg_text)
    except json.JSONDecodeError:
        brace_start = arg_text.find("{")
        brace_end = arg_text.rfind("}")
        if brace_start < 0 or brace_end < brace_start:
            return {}
        try:
            value = json.loads(arg_text[brace_start : brace_end + 1])
        except json.JSONDecodeError:
            return {}
    return value if isinstance(value, dict) else {}


def extract_execution_commands(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    try:
        lines = log_path.read_text(errors="replace").splitlines()
    except OSError:
        return []
    commands: list[dict[str, Any]] = []
    active_result_command: dict[str, Any] | None = None
    for line_number, line in enumerate(lines, start=1):
        if "Executing:" not in line:
            if active_result_command is not None and "Tool result:" in line:
                active_result_command["result_text"] = _truncate(_strip_log_prefix(line), 2500)
                active_result_command = None
            continue
        match = EXECUTING_RE.search(line)
        tool = match.group(1) if match else ""
        if tool not in EXECUTION_TOOLS:
            active_result_command = None
            continue
        stripped = _strip_log_prefix(line)
        args = _extract_json_arg(stripped, tool)
        command = {
            "command_index": len(commands) + 1,
            "line_number": line_number,
            "tool": tool,
            "args": args,
            "text": _truncate(stripped, 2500),
            "result_text": "",
        }
        hash_basis = {key: value for key, value in command.items() if key != "result_text"}
        command["command_hash"] = hashlib.sha1(_json_dumps(hash_basis).encode("utf-8")).hexdigest()[:16]
        commands.append(command)
        active_result_command = command
    return commands


def _direct_source_from_args(args: dict[str, Any]) -> str:
    dataset_id = str(args.get("dataset_id") or "").strip()
    file_path = str(args.get("file_path") or "").strip()
    if dataset_id and file_path:
        return normalize_source(f"datagov/{dataset_id}/{file_path}")
    for key in ["source", "path", "file"]:
        if args.get(key):
            return normalize_source(str(args[key]))
    return ""


def bind_command_sources(command: dict[str, Any], source_sequence: list[str]) -> tuple[list[str], list[str]]:
    args = command.get("args") if isinstance(command.get("args"), dict) else {}
    direct = _direct_source_from_args(args)
    text = _json_dumps(args) + "\n" + str(command.get("text", ""))
    normalized_text = normalize_source(text)
    bound: list[str] = []
    external: list[str] = []
    if direct:
        if direct in source_sequence:
            bound.append(direct)
        else:
            external.append(direct)
    for source in source_sequence:
        basename = Path(source).name
        dataset = source.split("/")[1] if "/" in source else ""
        if source and source in normalized_text:
            bound.append(source)
        elif basename and basename in text and (not dataset or dataset in text or basename != "rows.txt"):
            bound.append(source)
    return sorted(set(bound)), sorted(set(external))


def build_command_event(
    *,
    base: dict[str, str],
    command: dict[str, Any],
    source_sequence: list[str],
    ideal_records: list[dict[str, Any]],
) -> dict[str, str]:
    bound_sources, external_sources = bind_command_sources(command, source_sequence)
    event_id = f"{base['benchmark']}::{base['model_variant']}::{base['mode']}::{base['task_id']}::cmd{command['command_index']}"
    event = {
        **base,
        "event_id": event_id,
        "event_origin": "command",
        "event_type": "",
        "command_index": str(command["command_index"]),
        "line_number": str(command["line_number"]),
        "tool": str(command["tool"]),
        "bound_sources": _json_dumps(bound_sources),
        "matched_ideal_record_keys": "[]",
        "ideal_record_key": "",
        "ideal_node_id": "",
        "ideal_record_types": "",
        "error_type": "",
        "reason": "",
        "evidence": "",
        "command_json": _json_dumps(command),
        "ideal_record_json": "",
        "auditor_model": "",
        "audit_status": "pending",
    }
    if external_sources and not bound_sources:
        event.update(
            {
                "event_type": "wrong_file_execution",
                "bound_sources": _json_dumps(external_sources),
                "error_type": "wrong_file",
                "reason": "The execution command targets a source/file not present in the plan source_sequence.",
                "evidence": str(command.get("text", "")),
                "auditor_model": "mechanical",
                "audit_status": "complete",
            }
        )
    elif not ideal_records:
        event.update(
            {
                "event_type": "mismatched_execution",
                "error_type": "other",
                "reason": "No ideal_code or ideal_query records are available for this task.",
                "evidence": str(command.get("text", "")),
                "auditor_model": "mechanical",
                "audit_status": "complete",
            }
        )
    return event


def derive_missing_and_wasted_events(events: list[dict[str, str]], ideal_records: list[dict[str, Any]]) -> list[dict[str, str]]:
    if not events:
        return []
    base = {key: events[0].get(key, "") for key in ["benchmark", "model_variant", "mode", "task_id", "log_path", "plan_path"]}
    matched_keys: set[str] = set()
    schema_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for event in events:
        if event.get("event_type") == "matched_execution":
            keys = _safe_json_loads(event.get("matched_ideal_record_keys", "")) or []
            matched_keys.update(str(key) for key in keys)
        if event.get("event_type") == "schema_metadata_inspection":
            sources = _safe_json_loads(event.get("bound_sources", "")) or []
            for source in sources or [""]:
                schema_by_source[str(source)].append(event)

    derived: list[dict[str, str]] = []
    all_commands_resolved = all(event.get("audit_status") != "pending" for event in events)
    if all_commands_resolved:
        for record in ideal_records:
            key = str(record.get("ideal_record_key") or "")
            if key and key not in matched_keys:
                derived.append(
                    {
                        **base,
                        "event_id": f"{base['benchmark']}::{base['model_variant']}::{base['mode']}::{base['task_id']}::missing::{key}",
                        "event_origin": "derived",
                        "event_type": "missing_execution",
                        "command_index": "",
                        "line_number": "",
                        "tool": "",
                        "bound_sources": _json_dumps([record.get("source", "")] if record.get("source") else []),
                        "matched_ideal_record_keys": "[]",
                        "ideal_record_key": key,
                        "ideal_node_id": str(record.get("node_id") or ""),
                        "ideal_record_types": ",".join(record.get("record_types", [])),
                        "error_type": "not_executed",
                        "reason": "No judged execution command matched this ideal_code/ideal_query record.",
                        "evidence": "",
                        "command_json": "",
                        "ideal_record_json": _json_dumps(record),
                        "auditor_model": "mechanical",
                        "audit_status": "complete",
                    }
                )
    for source, schema_events in schema_by_source.items():
        for extra_index, source_event in enumerate(schema_events[1:], start=2):
            derived.append(
                {
                    **base,
                    "event_id": f"{source_event['event_id']}::wasted_schema_inspection",
                    "event_origin": "derived",
                    "event_type": "wasted_schema_inspection",
                    "command_index": source_event.get("command_index", ""),
                    "line_number": source_event.get("line_number", ""),
                    "tool": source_event.get("tool", ""),
                    "bound_sources": _json_dumps([source] if source else []),
                    "matched_ideal_record_keys": "[]",
                    "ideal_record_key": "",
                    "ideal_node_id": "",
                    "ideal_record_types": "",
                    "error_type": "schema_metadata_inspection",
                    "reason": f"Schema/metadata inspection #{extra_index} for this source is counted as a wasted execution turn.",
                    "evidence": source_event.get("evidence", ""),
                    "command_json": source_event.get("command_json", ""),
                    "ideal_record_json": "",
                    "auditor_model": "mechanical",
                    "audit_status": "complete",
                }
            )
    return derived


def derive_missing_events_without_commands(context: dict[str, Any]) -> list[dict[str, str]]:
    derived: list[dict[str, str]] = []
    base = {key: str(context.get(key, "")) for key in ["benchmark", "model_variant", "mode", "task_id", "log_path", "plan_path"]}
    for record in context["ideal_records"]:
        key = str(record.get("ideal_record_key") or "")
        if not key:
            continue
        derived.append(
            {
                **base,
                "event_id": f"{base['benchmark']}::{base['model_variant']}::{base['mode']}::{base['task_id']}::missing::{key}",
                "event_origin": "derived",
                "event_type": "missing_execution",
                "command_index": "",
                "line_number": "",
                "tool": "",
                "bound_sources": _json_dumps([record.get("source", "")] if record.get("source") else []),
                "matched_ideal_record_keys": "[]",
                "ideal_record_key": key,
                "ideal_node_id": str(record.get("node_id") or ""),
                "ideal_record_types": ",".join(record.get("record_types", [])),
                "error_type": "not_executed",
                "reason": "The log has no execute_code/query_file/execute_ideal/query_ideal commands for this ideal record.",
                "evidence": "",
                "command_json": "",
                "ideal_record_json": _json_dumps(record),
                "auditor_model": "mechanical",
                "audit_status": "complete",
            }
        )
    return derived


def build_rows(args: argparse.Namespace) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]]]:
    repo_root = Path(args.input_root).resolve()
    benchmarks = list(BENCHMARK_LOG_ROOTS) if args.benchmark == "all" else [args.benchmark]
    events: list[dict[str, str]] = []
    contexts: dict[str, dict[str, Any]] = {}
    for benchmark in benchmarks:
        log_root = repo_root / BENCHMARK_LOG_ROOTS[benchmark]
        for row in _mode_log_paths(log_root):
            if args.model and row["model_variant"] != args.model:
                continue
            if args.mode and row["mode"] != args.mode:
                continue
            if args.task and args.task not in row["task_id"]:
                continue
            plan_path = plan_path_for_task(repo_root, benchmark, row["task_id"])
            plan_context = load_plan_context(plan_path)
            log_path = Path(row["log_path"])
            commands = extract_execution_commands(log_path)
            base = {
                "benchmark": benchmark,
                "model_variant": row["model_variant"],
                "mode": row["mode"],
                "task_id": row["task_id"],
                "log_path": row["log_path"],
                "plan_path": str(plan_path.resolve(strict=False)),
            }
            context_key = _context_key(base)
            contexts[context_key] = {
                **base,
                "source_sequence": plan_context["source_sequence"],
                "ideal_records": plan_context["ideal_records"],
                "plan_error": plan_context["plan_error"],
                "commands": commands,
            }
            for command in commands:
                events.append(
                    build_command_event(
                        base=base,
                        command=command,
                        source_sequence=plan_context["source_sequence"],
                        ideal_records=plan_context["ideal_records"],
                    )
                )
    return events, contexts


def _context_key(row: dict[str, str]) -> str:
    return "\t".join([row["benchmark"], row["model_variant"], row["mode"], row["task_id"]])


def _event_key(event: dict[str, str]) -> tuple[str, str]:
    command_hash = ""
    command = _safe_json_loads(event.get("command_json", "")) or {}
    if isinstance(command, dict):
        command_hash = str(command.get("command_hash") or "")
    return event["event_id"], command_hash


def load_tmp_audits(tmp_root: Path) -> dict[tuple[str, str], dict[str, str]]:
    existing: dict[tuple[str, str], dict[str, str]] = {}
    if not tmp_root.exists():
        return existing
    for path in sorted(tmp_root.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        event_key = payload.get("event_key")
        event_update = payload.get("event_update")
        if not isinstance(event_key, dict) or not isinstance(event_update, dict):
            continue
        key = (str(event_key.get("event_id", "")), str(event_key.get("command_hash", "")))
        if not key[0]:
            continue
        existing[key] = {column: str(event_update.get(column, "")) for column in AUDIT_UPDATE_COLUMNS}
    return existing


def merge_tmp_audits(events: list[dict[str, str]], existing: dict[tuple[str, str], dict[str, str]]) -> None:
    for event in events:
        old = existing.get(_event_key(event))
        if old and old.get("audit_status") not in ("", "pending"):
            for column in AUDIT_UPDATE_COLUMNS:
                event[column] = old.get(column, event.get(column, ""))


def _event_json_path(tmp_root: Path, event: dict[str, str]) -> Path:
    raw = "__".join(
        [
            event["benchmark"],
            event["model_variant"],
            event["mode"],
            Path(event["task_id"]).with_suffix("").as_posix(),
            f"cmd{event['command_index']}",
        ]
    )
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("_")
    return tmp_root / event["benchmark"] / event["model_variant"] / event["mode"] / f"{slug}.json"


def validate_judge_payload(payload: dict[str, Any], ideal_record_keys: set[str]) -> list[str]:
    errors: list[str] = []
    event_type = payload.get("event_type")
    if event_type not in JUDGE_EVENT_TYPES:
        errors.append(f"event_type must be one of {sorted(JUDGE_EVENT_TYPES)}, got {event_type!r}")
    if payload.get("audit_status") != "complete":
        errors.append("audit_status must be 'complete'")
    if payload.get("error_type") not in ERROR_TYPES:
        errors.append(f"error_type must be one of {sorted(ERROR_TYPES)}")
    for field in ["reason", "evidence"]:
        if not isinstance(payload.get(field), str) or not str(payload.get(field)).strip():
            errors.append(f"{field} must be a non-empty string")
    matched = payload.get("matched_ideal_record_keys")
    if not isinstance(matched, list):
        errors.append("matched_ideal_record_keys must be a list")
    else:
        unknown = [str(key) for key in matched if str(key) not in ideal_record_keys]
        if unknown:
            errors.append(f"matched_ideal_record_keys contains unknown keys: {unknown}")
    if event_type == "matched_execution" and not matched:
        errors.append("matched_execution requires at least one matched_ideal_record_key")
    if event_type != "matched_execution" and matched:
        errors.append("only matched_execution may include matched_ideal_record_keys")
    return errors


def build_repair_prompt(original_prompt: str, previous_text: str, errors: list[str]) -> str:
    return (
        original_prompt.rstrip()
        + "\n\nYour previous response failed deterministic validation.\n"
        + "Return JSON only, with exactly the required schema. Fix these errors:\n"
        + "\n".join(f"- {error}" for error in errors)
        + "\n\nPrevious response:\n```text\n"
        + previous_text
        + "\n```"
    )


def call_codex(
    prompt: str,
    *,
    repo_root: Path,
    model: str,
    reasoning_effort: str,
    last_message_path: Path,
    stdout_path: Path,
    timeout: int,
) -> str:
    last_message_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "codex",
        "exec",
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "-C",
        str(repo_root),
        "-s",
        "workspace-write",
        "--output-last-message",
        str(last_message_path),
        "-",
    ]
    proc = subprocess.run(
        cmd,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"codex exec failed with exit code {proc.returncode}; see {stdout_path}")
    if last_message_path.exists():
        return last_message_path.read_text(encoding="utf-8")
    return proc.stdout


def call_judge_model(
    prompt: str,
    *,
    backend: str,
    repo_root: Path,
    model: str,
    reasoning_effort: str,
    last_message_path: Path,
    stdout_path: Path,
    timeout: int,
) -> str:
    if backend == "codex":
        return call_codex(
            prompt,
            repo_root=repo_root,
            model=model,
            reasoning_effort=reasoning_effort,
            last_message_path=last_message_path,
            stdout_path=stdout_path,
            timeout=timeout,
        )
    if backend == "openai":
        text = call_openai(prompt, repo_root=repo_root, model=model, reasoning_effort=reasoning_effort, timeout=timeout)
        last_message_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        last_message_path.write_text(text, encoding="utf-8")
        stdout_path.write_text("", encoding="utf-8")
        return text
    raise ValueError(f"Unsupported judge backend: {backend}")


def build_judge_prompt(event: dict[str, str], context: dict[str, Any]) -> str:
    command = _safe_json_loads(event["command_json"]) or {}
    bound_sources = _safe_json_loads(event.get("bound_sources", "")) or []
    if bound_sources:
        candidates = [record for record in context["ideal_records"] if record.get("source") in bound_sources]
    else:
        candidates = context["ideal_records"]
    return f"""You are auditing one execution command from an agent log.

The task plan context includes source_sequence and ideal_code/ideal_query records. The command has already been mechanically bound to source_sequence when possible. Judge whether this single command is a real execution that matches one or more ideal records, is a mismatched execution, or is only schema/metadata inspection.

Return JSON only:
{{
  "event_type": "matched_execution|mismatched_execution|schema_metadata_inspection|execution_failure",
  "matched_ideal_record_keys": ["one or more ideal_record_key values when event_type is matched_execution, otherwise []"],
  "error_type": "none|operation_binding|filter_binding|schema_error|parse_error|schema_metadata_inspection|not_executed|other",
  "reason": "short evidence-grounded reason",
  "evidence": "cite the command line and ideal record keys/intents used",
  "audit_status": "complete"
}}

Return matched_ideal_record_keys as [] for every event_type except matched_execution.
Use schema_metadata_inspection when the command primarily inspects columns, headers, shape, sample rows, table names, file metadata, or parse structure rather than performing the intended computation.
Use execution_failure when the command attempts a substantive execution but the tool result shows a runtime, parse, schema, timeout, path, file, or data-access failure before producing a usable result.
Use mismatched_execution when it is a substantive execution on a needed source but does not match the intended ideal operation/filter/computation.
Use matched_execution when it performs the same intended operation as one or more ideal records, even if the implementation differs.

Metadata:
- benchmark: {event['benchmark']}
- model_variant: {event['model_variant']}
- mode: {event['mode']}
- task_id: {event['task_id']}
- log_path: {event['log_path']}
- line_number: {event['line_number']}
- tool: {event['tool']}
- bound_sources: {event['bound_sources']}

COMMAND:
{json.dumps(command, indent=2, ensure_ascii=False)}

SOURCE_SEQUENCE:
{json.dumps(context['source_sequence'], indent=2, ensure_ascii=False)}

CANDIDATE IDEAL RECORDS:
{json.dumps(candidates, indent=2, ensure_ascii=False)}
"""


def judge_pending_events(
    events: list[dict[str, str]],
    contexts: dict[str, dict[str, Any]],
    *,
    backend: str,
    output_dir: Path,
    repo_root: Path,
    model: str,
    reasoning_effort: str,
    limit: int,
    timeout: int,
    tmp_root: Path,
    journal_path: Path,
    max_retries: int,
) -> int:
    judged = 0
    for event in events:
        if event.get("event_origin") != "command" or event.get("audit_status") != "pending":
            continue
        if limit and judged >= limit:
            break
        print(
            "Judging execution event "
            f"#{judged + 1}: benchmark={event['benchmark']} model={event['model_variant']} "
            f"mode={event['mode']} task={event['task_id']} "
            f"command={event['command_index']} tool={event['tool']} line={event['line_number']}",
            flush=True,
        )
        context = contexts[_context_key(event)]
        ideal_keys = {str(record.get("ideal_record_key")) for record in context["ideal_records"]}
        prompt = build_judge_prompt(event, context)
        out_path = _event_json_path(tmp_root, event)
        stem = out_path.with_suffix("")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path = stem.with_suffix(".prompt.txt")
        last_message_path = stem.with_suffix(".last_message.txt")
        stdout_path = stem.with_suffix(f".{backend}_stdout.log")
        attempt_prompt = prompt
        parsed: dict[str, Any] | None = None
        text = ""
        validation_errors: list[str] = []
        for attempt in range(1, max_retries + 2):
            prompt_path.write_text(attempt_prompt, encoding="utf-8")
            stem.with_suffix(f".attempt{attempt}.prompt.txt").write_text(attempt_prompt, encoding="utf-8")
            print(
                f"  attempt {attempt}: spawning {backend} judge for task={event['task_id']} "
                f"command={event['command_index']} tool={event['tool']}",
                flush=True,
            )
            try:
                text = call_judge_model(
                    attempt_prompt,
                    backend=backend,
                    repo_root=repo_root,
                    model=model,
                    reasoning_effort=reasoning_effort,
                    last_message_path=last_message_path,
                    stdout_path=stdout_path,
                    timeout=timeout,
                )
            except Exception as exc:
                _append_journal_record(
                    journal_path,
                    {
                        "status": "error",
                        "error": str(exc),
                        "attempt": attempt,
                        "event_id": event["event_id"],
                        "prompt_path": str(prompt_path),
                        "stdout_path": str(stdout_path),
                    },
                )
                raise
            stem.with_suffix(f".attempt{attempt}.last_message.txt").write_text(text, encoding="utf-8")
            try:
                parsed = _parse_json_object(text)
            except (json.JSONDecodeError, ValueError) as exc:
                validation_errors = [f"response must be a JSON object: {exc}"]
            else:
                validation_errors = validate_judge_payload(parsed, ideal_keys)
            if not validation_errors:
                break
            _append_journal_record(
                journal_path,
                {
                    "status": "retry",
                    "attempt": attempt,
                    "errors": validation_errors,
                    "event_id": event["event_id"],
                    "prompt_path": str(prompt_path),
                    "last_message_path": str(last_message_path),
                    "stdout_path": str(stdout_path),
                },
            )
            if attempt > max_retries:
                raise RuntimeError("Execution event judge failed validation after retries: " + "; ".join(validation_errors))
            attempt_prompt = build_repair_prompt(prompt, text, validation_errors)

        assert parsed is not None
        matched_keys = [str(key) for key in parsed.get("matched_ideal_record_keys", [])]
        first_record = next((record for record in context["ideal_records"] if record.get("ideal_record_key") in matched_keys), None)
        event.update(
            {
                "event_type": str(parsed.get("event_type")),
                "matched_ideal_record_keys": _json_dumps(matched_keys),
                "ideal_record_key": str(first_record.get("ideal_record_key") if first_record else ""),
                "ideal_node_id": str(first_record.get("node_id") if first_record else ""),
                "ideal_record_types": ",".join(first_record.get("record_types", [])) if first_record else "",
                "error_type": str(parsed.get("error_type")),
                "reason": str(parsed.get("reason", "")),
                "evidence": str(parsed.get("evidence", "")),
                "ideal_record_json": _json_dumps(first_record) if first_record else "",
                "auditor_model": model,
                "audit_status": "complete",
            }
        )
        command = _safe_json_loads(event.get("command_json", "")) or {}
        audit_payload = {
            "event_key": {"event_id": event["event_id"], "command_hash": str(command.get("command_hash", ""))},
            "backend": backend,
            "judge_model": model,
            "reasoning_effort": reasoning_effort,
            "prompt_path": str(prompt_path),
            "last_message_path": str(last_message_path),
            "stdout_path": str(stdout_path),
            "parsed": parsed,
            "event_update": {column: event[column] for column in AUDIT_UPDATE_COLUMNS},
        }
        out_path.write_text(json.dumps(audit_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        _append_journal_record(
            journal_path,
            {
                "status": "ok",
                "event_id": event["event_id"],
                "label": event["event_type"],
                "audit_json_path": str(out_path),
                "prompt_path": str(prompt_path),
                "last_message_path": str(last_message_path),
                "stdout_path": str(stdout_path),
            },
        )
        judged += 1
        time.sleep(0.1)
        inventory_rows, all_events = assemble_outputs(events, contexts)
        write_outputs(output_dir, inventory_rows, all_events)
    return judged


def assemble_outputs(
    command_events: list[dict[str, str]],
    contexts: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    events_by_context: dict[str, list[dict[str, str]]] = defaultdict(list)
    for event in command_events:
        events_by_context[_context_key(event)].append(event)

    all_events: list[dict[str, str]] = []
    inventory_rows: list[dict[str, str]] = []
    for key, context in sorted(contexts.items()):
        base_events = sorted(events_by_context.get(key, []), key=lambda event: int(event.get("command_index") or 0))
        if base_events:
            derived_events = derive_missing_and_wasted_events(base_events, context["ideal_records"])
        else:
            derived_events = derive_missing_events_without_commands(context)
        combined = base_events + derived_events
        counts = Counter(event.get("event_type") or "pending" for event in combined)
        pending = sum(1 for event in combined if event.get("audit_status") == "pending")
        inventory_rows.append(
            {
                "benchmark": context["benchmark"],
                "model_variant": context["model_variant"],
                "mode": context["mode"],
                "task_id": context["task_id"],
                "log_path": context["log_path"],
                "plan_path": context["plan_path"],
                "n_execution_commands": str(len(context["commands"])),
                "n_events": str(len(combined)),
                "n_pending_events": str(pending),
                "n_matched_execution": str(counts.get("matched_execution", 0)),
                "n_mismatched_execution": str(counts.get("mismatched_execution", 0)),
                "n_wrong_file_execution": str(counts.get("wrong_file_execution", 0)),
                "n_schema_metadata_inspection": str(counts.get("schema_metadata_inspection", 0)),
                "n_execution_failure": str(counts.get("execution_failure", 0)),
                "n_missing_execution": str(counts.get("missing_execution", 0)),
                "n_wasted_schema_inspection": str(counts.get("wasted_schema_inspection", 0)),
                "source_sequence_json": _json_dumps(context["source_sequence"]),
                "ideal_records_json": _json_dumps(context["ideal_records"]),
                "execution_commands_json": _json_dumps(context["commands"]),
                "event_ids_json": _json_dumps([event["event_id"] for event in combined]),
            }
        )
        all_events.extend(combined)
    return inventory_rows, all_events


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, inventory_rows: list[dict[str, str]], event_rows: list[dict[str, str]]) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory_path = output_dir / "execution_inventory.csv"
    events_path = output_dir / "execution_events.csv"
    write_csv(inventory_path, inventory_rows, INVENTORY_COLUMNS)
    write_csv(events_path, event_rows, EVENT_COLUMNS)
    return [inventory_path, events_path]


def print_summary(inventory_rows: list[dict[str, str]]) -> None:
    grouped: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    for row in inventory_rows:
        key = (row["benchmark"], row["model_variant"], row["mode"])
        for field in [
            "n_execution_commands",
            "n_events",
            "n_pending_events",
            "n_matched_execution",
            "n_mismatched_execution",
            "n_wrong_file_execution",
            "n_schema_metadata_inspection",
            "n_execution_failure",
            "n_missing_execution",
            "n_wasted_schema_inspection",
        ]:
            grouped[key][field] += int(row.get(field) or 0)
        grouped[key]["n_logs"] += 1
    print("Execution inventory summary:")
    for (benchmark, model_variant, mode), counts in sorted(grouped.items()):
        print(
            f"  {benchmark:<11} {model_variant:<18} {mode:<48} "
            f"logs={counts['n_logs']} commands={counts['n_execution_commands']} "
            f"matched={counts['n_matched_execution']} mismatched={counts['n_mismatched_execution']} "
            f"wrong_file={counts['n_wrong_file_execution']} schema={counts['n_schema_metadata_inspection']} "
            f"failure={counts['n_execution_failure']} "
            f"missing={counts['n_missing_execution']} wasted_schema={counts['n_wasted_schema_inspection']} "
            f"pending={counts['n_pending_events']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", default=".", help="Repository/input root containing logs and plans.")
    parser.add_argument("--output-dir", default="agent_analysis/execution_inventory_analysis")
    parser.add_argument("--benchmark", choices=["all", *BENCHMARK_LOG_ROOTS.keys()], default="all")
    parser.add_argument("--model", default="", help="Optional model folder, e.g. openai_gpt-5-mini.")
    parser.add_argument("--mode", default="", help="Optional mode folder, e.g. search_i_results_i_plani_k5_skills_off.")
    parser.add_argument("--task", default="", help="Optional task-id substring filter.")
    parser.add_argument("--judge", action="store_true", help="Judge pending execution commands.")
    parser.add_argument("--backend", choices=["codex", "openai"], default="codex", help="Judge backend; defaults to codex exec.")
    parser.add_argument("--judge-model", default="gpt-5.4-mini")
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max pending command events to judge. Omit for an interactive prompt; 0 means all.",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument(
        "--tmp-root",
        default="agent_analysis/execution_inventory_analysis/tmp",
        help="Directory for per-command prompt, raw response, and parsed judge JSON files.",
    )
    parser.add_argument(
        "--journal-path",
        default="",
        help="Optional JSONL journal path. Defaults to <output-dir>/execution_inventory_journal.jsonl.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    tmp_root = Path(args.tmp_root).resolve()
    command_events, contexts = build_rows(args)
    merge_tmp_audits(command_events, load_tmp_audits(tmp_root))
    inventory_rows, event_rows = assemble_outputs(command_events, contexts)
    written = write_outputs(output_dir, inventory_rows, event_rows)
    if args.judge:
        journal_path = Path(args.journal_path).resolve() if args.journal_path else output_dir / "execution_inventory_journal.jsonl"
        print(f"Temp judge dir: {tmp_root}")
        print(f"JSONL journal: {journal_path}")
        print(f"Judge backend: {args.backend}")
        pending_count = sum(1 for event in command_events if event.get("audit_status") == "pending")
        judge_limit = resolve_judge_limit(
            requested_limit=args.limit,
            pending_count=pending_count,
            is_interactive=sys.stdin.isatty(),
        )
        if judge_limit is None:
            print("Aborted without judging events.")
            print_summary(inventory_rows)
            for path in written:
                print(f"Wrote {path}")
            return 0
        judged = judge_pending_events(
            command_events,
            contexts,
            backend=args.backend,
            output_dir=output_dir,
            repo_root=Path(args.input_root).resolve(),
            model=args.judge_model,
            reasoning_effort=args.reasoning_effort,
            limit=judge_limit,
            timeout=args.timeout,
            tmp_root=tmp_root,
            journal_path=journal_path,
            max_retries=args.max_retries,
        )
        print(f"Judged {judged} pending event(s).")
        command_events, contexts = build_rows(args)
        merge_tmp_audits(command_events, load_tmp_audits(tmp_root))
        inventory_rows, event_rows = assemble_outputs(command_events, contexts)
        written = write_outputs(output_dir, inventory_rows, event_rows)
    print_summary(inventory_rows)
    for path in written:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
