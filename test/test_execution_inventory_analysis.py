import json
from argparse import Namespace
from pathlib import Path

from analysis.execution_inventory_analysis import (
    assemble_outputs,
    bind_command_sources,
    build_command_event,
    build_judge_prompt,
    build_rows,
    derive_missing_and_wasted_events,
    derive_missing_events_without_commands,
    extract_execution_commands,
    judge_pending_events,
    load_plan_context,
    load_tmp_audits,
    merge_tmp_audits,
    validate_judge_payload,
)


def _write_plan(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "source_sequence": [
                    "datagov/ds/files/rows.txt",
                    "datagov/other/files/rows.txt",
                ],
                "ideal_query": [
                    {
                        "node_id": "1",
                        "dataset_id": "ds",
                        "source": "datagov/ds/files/rows.txt",
                        "intent": "Compute average x for 2020.",
                        "sql": "select avg(x) from t where year=2020",
                        "answer": "4",
                    }
                ],
                "ideal_code": [
                    {
                        "node_id": "1",
                        "dataset_id": "ds",
                        "source": "datagov/ds/files/rows.txt",
                        "intent": "Compute average x for 2020.",
                        "code": "print(4)",
                        "answer": "4",
                    },
                    {
                        "node_id": "2",
                        "dataset_id": "other",
                        "source": "datagov/other/files/rows.txt",
                        "intent": "Compute count y.",
                        "code": "print(7)",
                        "answer": "7",
                    },
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )


def _write_log(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                '2026 | INFO | x | Executing: query_file({"dataset_id": "ds", "file_path": "files/rows.txt", "sql": "select avg(x) from t where year=2020"})',
                '2026 | INFO | x | Executing: query_file({"dataset_id": "ds", "file_path": "files/rows.txt", "sql": "select * from t limit 5"})',
                '2026 | INFO | x | Executing: execute_code({"code": "path=SANDBOX_DIR + \\"/other/files/rows.txt\\"\\nprint(open(path).readline())"})',
                '2026 | INFO | x | Executing: query_file({"dataset_id": "wrong", "file_path": "files/rows.txt", "sql": "select count(*) from t"})',
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_load_plan_context_merges_code_and_query_by_node_source(tmp_path: Path) -> None:
    plan = tmp_path / "plan.json"
    _write_plan(plan)

    context = load_plan_context(plan)

    assert context["source_sequence"] == ["datagov/ds/files/rows.txt", "datagov/other/files/rows.txt"]
    assert len(context["ideal_records"]) == 2
    first = next(record for record in context["ideal_records"] if record["node_id"] == "1")
    assert set(first["record_types"]) == {"ideal_query", "ideal_code"}
    assert first["ideal_query"]["sql"].startswith("select avg")
    assert first["ideal_code"]["code"] == "print(4)"


def test_extract_execution_commands_keeps_execution_tools(tmp_path: Path) -> None:
    log = tmp_path / "task.log"
    _write_log(log)

    commands = extract_execution_commands(log)

    assert [command["tool"] for command in commands] == [
        "query_file",
        "query_file",
        "execute_code",
        "query_file",
    ]
    assert commands[0]["args"]["dataset_id"] == "ds"
    assert commands[0]["command_hash"]


def test_extract_execution_commands_attaches_following_tool_result(tmp_path: Path) -> None:
    log = tmp_path / "task.log"
    log.write_text(
        "\n".join(
            [
                '2026 | INFO | x | Executing: execute_code({"code": "raise FileNotFoundError(\\"missing.csv\\")"})',
                "2026 | INFO | x | Tool result: Traceback (most recent call last): FileNotFoundError: missing.csv",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    commands = extract_execution_commands(log)

    assert len(commands) == 1
    assert "FileNotFoundError" in commands[0]["result_text"]


def test_bind_command_sources_direct_and_text_matching(tmp_path: Path) -> None:
    log = tmp_path / "task.log"
    _write_log(log)
    commands = extract_execution_commands(log)
    sources = ["datagov/ds/files/rows.txt", "datagov/other/files/rows.txt"]

    assert bind_command_sources(commands[0], sources) == (["datagov/ds/files/rows.txt"], [])
    assert bind_command_sources(commands[2], sources) == (["datagov/other/files/rows.txt"], [])
    assert bind_command_sources(commands[3], sources) == ([], ["datagov/wrong/files/rows.txt"])


def test_build_command_event_marks_wrong_file_mechanically(tmp_path: Path) -> None:
    log = tmp_path / "task.log"
    _write_log(log)
    command = extract_execution_commands(log)[3]
    base = {
        "benchmark": "lakeqa",
        "model_variant": "openai_gpt-test",
        "mode": "search_i_results_i_plani_k5_skills_off",
        "task_id": "tasks_mini/k/task.json",
        "log_path": str(log),
        "plan_path": str(tmp_path / "plan.json"),
    }

    event = build_command_event(
        base=base,
        command=command,
        source_sequence=["datagov/ds/files/rows.txt"],
        ideal_records=[{"ideal_record_key": "1:datagov/ds/files/rows.txt"}],
    )

    assert event["event_type"] == "wrong_file_execution"
    assert event["audit_status"] == "complete"
    assert "datagov/wrong/files/rows.txt" in event["bound_sources"]


def test_derive_missing_and_wasted_events() -> None:
    base = {
        "benchmark": "lakeqa",
        "model_variant": "openai_gpt-test",
        "mode": "mode",
        "task_id": "task.json",
        "log_path": "task.log",
        "plan_path": "plan.json",
    }
    ideal_records = [
        {"ideal_record_key": "1:datagov/ds/files/rows.txt", "node_id": "1", "source": "datagov/ds/files/rows.txt", "record_types": ["ideal_query"]},
        {"ideal_record_key": "2:datagov/ds/files/rows.txt", "node_id": "2", "source": "datagov/ds/files/rows.txt", "record_types": ["ideal_code"]},
    ]
    events = [
        {
            **base,
            "event_id": "e1",
            "event_type": "matched_execution",
            "audit_status": "complete",
            "matched_ideal_record_keys": '["1:datagov/ds/files/rows.txt"]',
            "bound_sources": '["datagov/ds/files/rows.txt"]',
            "command_index": "1",
            "line_number": "1",
            "tool": "query_file",
            "evidence": "e1",
            "command_json": "{}",
        },
        {
            **base,
            "event_id": "e2",
            "event_type": "schema_metadata_inspection",
            "audit_status": "complete",
            "matched_ideal_record_keys": "[]",
            "bound_sources": '["datagov/ds/files/rows.txt"]',
            "command_index": "2",
            "line_number": "2",
            "tool": "query_file",
            "evidence": "e2",
            "command_json": "{}",
        },
        {
            **base,
            "event_id": "e3",
            "event_type": "schema_metadata_inspection",
            "audit_status": "complete",
            "matched_ideal_record_keys": "[]",
            "bound_sources": '["datagov/ds/files/rows.txt"]',
            "command_index": "3",
            "line_number": "3",
            "tool": "query_file",
            "evidence": "e3",
            "command_json": "{}",
        },
    ]

    derived = derive_missing_and_wasted_events(events, ideal_records)

    assert [event["event_type"] for event in derived] == [
        "missing_execution",
        "wasted_schema_inspection",
    ]
    assert derived[0]["ideal_record_key"] == "2:datagov/ds/files/rows.txt"
    assert derived[1]["command_index"] == "3"


def test_derive_missing_events_without_commands() -> None:
    context = {
        "benchmark": "lakeqa",
        "model_variant": "openai_gpt-test",
        "mode": "mode",
        "task_id": "task.json",
        "log_path": "task.log",
        "plan_path": "plan.json",
        "ideal_records": [
            {
                "ideal_record_key": "1:datagov/ds/files/rows.txt",
                "node_id": "1",
                "source": "datagov/ds/files/rows.txt",
                "record_types": ["ideal_query"],
            }
        ],
    }

    derived = derive_missing_events_without_commands(context)

    assert len(derived) == 1
    assert derived[0]["event_type"] == "missing_execution"
    assert derived[0]["reason"].startswith("The log has no execute_code")


def test_build_rows_and_assemble_outputs(tmp_path: Path) -> None:
    repo = tmp_path
    log = repo / "logs/modes/openai_gpt-test/search_i_results_i_plani_k5_skills_off/tasks_mini/k/task.log"
    plan = repo / "plans_mini/k/task.json"
    _write_log(log)
    _write_plan(plan)
    args = Namespace(input_root=str(repo), benchmark="lakeqa", model="", mode="", task="")

    command_events, contexts = build_rows(args)
    inventory, events = assemble_outputs(command_events, contexts)

    assert len(inventory) == 1
    assert inventory[0]["n_execution_commands"] == "4"
    assert inventory[0]["n_wrong_file_execution"] == "1"
    assert inventory[0]["n_pending_events"] == "3"
    assert not any(event["event_type"] == "missing_execution" for event in events)


def test_tmp_audits_merge_by_event_and_command_hash(tmp_path: Path) -> None:
    event = {
        "event_id": "e1",
        "command_json": '{"command_hash": "abc"}',
        "event_type": "",
        "bound_sources": "[]",
        "matched_ideal_record_keys": "[]",
        "ideal_record_key": "",
        "ideal_node_id": "",
        "ideal_record_types": "",
        "error_type": "",
        "reason": "",
        "evidence": "",
        "auditor_model": "",
        "audit_status": "pending",
    }
    path = tmp_path / "tmp/audit.json"
    path.parent.mkdir()
    path.write_text(
        json.dumps(
            {
                "event_key": {"event_id": "e1", "command_hash": "abc"},
                "event_update": {
                    "event_type": "matched_execution",
                    "bound_sources": "[]",
                    "matched_ideal_record_keys": '["k"]',
                    "ideal_record_key": "k",
                    "ideal_node_id": "1",
                    "ideal_record_types": "ideal_query",
                    "error_type": "none",
                    "reason": "r",
                    "evidence": "e",
                    "auditor_model": "judge",
                    "audit_status": "complete",
                },
            }
        ),
        encoding="utf-8",
    )

    merge_tmp_audits([event], load_tmp_audits(tmp_path / "tmp"))

    assert event["event_type"] == "matched_execution"
    assert event["audit_status"] == "complete"


def test_validate_judge_payload() -> None:
    errors = validate_judge_payload(
        {
            "event_type": "matched_execution",
            "matched_ideal_record_keys": ["k"],
            "error_type": "none",
            "reason": "same",
            "evidence": "lines",
            "audit_status": "complete",
        },
        {"k"},
    )
    assert errors == []
    bad = validate_judge_payload(
        {
            "event_type": "matched_execution",
            "matched_ideal_record_keys": [],
            "error_type": "weird",
            "audit_status": "done",
        },
        {"k"},
    )
    assert any("matched_execution requires" in error for error in bad)
    assert any("audit_status" in error for error in bad)


def test_validate_judge_payload_accepts_execution_failure() -> None:
    errors = validate_judge_payload(
        {
            "event_type": "execution_failure",
            "matched_ideal_record_keys": [],
            "error_type": "schema_error",
            "reason": "The query failed before producing a result.",
            "evidence": "Tool result: Binder Error",
            "audit_status": "complete",
        },
        {"k"},
    )

    assert errors == []


def test_validate_judge_payload_rejects_matched_keys_for_non_matches() -> None:
    errors = validate_judge_payload(
        {
            "event_type": "execution_failure",
            "matched_ideal_record_keys": ["k"],
            "error_type": "schema_error",
            "reason": "The query failed before producing a result.",
            "evidence": "Tool result: Binder Error",
            "audit_status": "complete",
        },
        {"k"},
    )

    assert any("only matched_execution may include matched_ideal_record_keys" in error for error in errors)


def test_build_judge_prompt_includes_execution_failure_guidance_and_result() -> None:
    event = {
        "benchmark": "lakeqa",
        "model_variant": "openai_gpt-test",
        "mode": "mode",
        "task_id": "task.json",
        "log_path": "task.log",
        "line_number": "10",
        "tool": "execute_code",
        "bound_sources": "[]",
        "command_json": json.dumps(
            {
                "command_hash": "abc",
                "tool": "execute_code",
                "args": {"code": "raise FileNotFoundError('missing.csv')"},
                "result_text": "Tool result: FileNotFoundError: missing.csv",
            }
        ),
    }
    context = {
        "source_sequence": ["datagov/ds/files/rows.txt"],
        "ideal_records": [
            {
                "ideal_record_key": "1:datagov/ds/files/rows.txt",
                "source": "datagov/ds/files/rows.txt",
                "intent": "Compute average x.",
            }
        ],
    }

    prompt = build_judge_prompt(event, context)

    assert "execution_failure" in prompt
    assert "FileNotFoundError" in prompt


def test_judge_pending_events_retries_invalid_until_valid(tmp_path: Path, monkeypatch) -> None:
    event = {
        "benchmark": "lakeqa",
        "model_variant": "openai_gpt-test",
        "mode": "mode",
        "task_id": "task.json",
        "log_path": "task.log",
        "plan_path": "plan.json",
        "event_id": "lakeqa::openai_gpt-test::mode::task.json::cmd1",
        "event_origin": "command",
        "event_type": "",
        "command_index": "1",
        "line_number": "10",
        "tool": "query_file",
        "bound_sources": '["datagov/ds/files/rows.txt"]',
        "matched_ideal_record_keys": "[]",
        "ideal_record_key": "",
        "ideal_node_id": "",
        "ideal_record_types": "",
        "error_type": "",
        "reason": "",
        "evidence": "",
        "command_json": '{"command_hash": "abc", "tool": "query_file"}',
        "ideal_record_json": "",
        "auditor_model": "",
        "audit_status": "pending",
    }
    contexts = {
        "lakeqa\topenai_gpt-test\tmode\ttask.json": {
            "benchmark": "lakeqa",
            "model_variant": "openai_gpt-test",
            "mode": "mode",
            "task_id": "task.json",
            "log_path": "task.log",
            "plan_path": "plan.json",
            "source_sequence": ["datagov/ds/files/rows.txt"],
            "ideal_records": [
                {
                    "ideal_record_key": "1:datagov/ds/files/rows.txt",
                    "node_id": "1",
                    "source": "datagov/ds/files/rows.txt",
                    "record_types": ["ideal_query"],
                    "intent": "Compute average x.",
                }
            ],
            "commands": [{"command_hash": "abc"}],
        }
    }
    responses = iter(
        [
            '{"event_type": "matched_execution", "matched_ideal_record_keys": [], "error_type": "none", "audit_status": "complete"}',
            """{
              "event_type": "matched_execution",
              "matched_ideal_record_keys": ["1:datagov/ds/files/rows.txt"],
              "error_type": "none",
              "reason": "same computation",
              "evidence": "line 10",
              "audit_status": "complete"
            }""",
        ]
    )
    monkeypatch.setattr("analysis.execution_inventory_analysis.call_judge_model", lambda *_args, **_kwargs: next(responses))

    judged = judge_pending_events(
        [event],
        contexts,
        backend="codex",
        output_dir=tmp_path / "out",
        repo_root=tmp_path,
        model="gpt-5.4-mini",
        reasoning_effort="low",
        limit=0,
        timeout=10,
        tmp_root=tmp_path / "tmp",
        journal_path=tmp_path / "journal.jsonl",
        max_retries=2,
    )

    assert judged == 1
    assert event["event_type"] == "matched_execution"
    assert event["ideal_record_key"] == "1:datagov/ds/files/rows.txt"
    assert '"status": "retry"' in (tmp_path / "journal.jsonl").read_text()
