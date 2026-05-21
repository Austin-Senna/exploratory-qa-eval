import csv
import json
from pathlib import Path

from analysis.answer_failure_audit_runner import (
    _build_row_prompt,
    _append_journal_record,
    _audit_json_path,
    _default_journal_path,
    _load_journal_audits,
    _load_prompt_artifacts,
    _normalized_events,
    _openai_api_key,
    _temp_dir_for_layout,
    eval_pending_stats,
    _task_ids_for_deterministic_repair,
    _validated_batch_repair,
    choose_pending_eval_path,
    find_pending_eval_stats,
    find_pending_eval_paths,
    infer_layout,
    parse_json_object,
    write_mirrored_outputs,
)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_infer_layout_maps_semantic_eval_to_answer_failure_outputs(tmp_path):
    eval_path = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_pland_k5_skills_off"
        / "eval_results.csv"
    )
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")

    layout = infer_layout(eval_path)

    assert layout.source_root == tmp_path / "results_semantic"
    assert layout.output_root == tmp_path / "results_semantic_answer_failures"
    assert layout.logs_root == tmp_path / "logs" / "modes"
    assert layout.model_variant == "openai_gpt-5-mini"
    assert layout.mode_variant == "search_d_results_i_pland_k5_skills_off"
    assert layout.mirrored_eval_path == (
        tmp_path
        / "results_semantic_answer_failures"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_pland_k5_skills_off"
        / "eval_results.csv"
    )


def test_parse_json_object_accepts_fenced_model_output():
    payload = {
        "task_id": "tasks_mini/k-1-d-1/task_1.json",
        "answer_failure_summary": "Used the wrong source.",
        "events": [],
    }
    text = "Here is the audit:\n```json\n" + json.dumps(payload) + "\n```\n"

    assert parse_json_object(text) == payload


def test_parse_json_object_repairs_unescaped_quotes_inside_backticks():
    text = (
        '{"task_id":"tasks_mini/k-6-d-3/task_3.json",'
        '"answer_failure_summary":"Wrong final entity.",'
        '"events":[{"event_index":1,'
        '"answer_failure_type":"evidence_available_answer_error",'
        '"answer_failure_subtype":"wrong_final_entity_selection",'
        '"failure_stage":"finalization",'
        '"failure_summary":"The final entity was wrong.",'
        '"failure_evidence":"Turn 33 | it submitted `"[44116]"` with the wrong reasoning.",'
        '"confidence":"high"}]}'
    )

    parsed = parse_json_object(text)

    assert parsed["events"][0]["failure_evidence"] == (
        'Turn 33 | it submitted `"[44116]"` with the wrong reasoning.'
    )


def test_row_prompt_matches_answer_failure_worker_contract(tmp_path):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")
    layout = infer_layout(eval_path)
    task_id = "tasks_mini/k-4-d-1/task_3.json"

    prompt = _build_row_prompt(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        task_id=task_id,
        log_path=layout.logs_root / "model" / "mode" / "tasks_mini" / "k-4-d-1" / "task_3.log",
        backend="codex",
    )

    assert "You are the row-audit subagent for Answer Failure Auditor" in prompt
    assert "Use that skill only as taxonomy/reference context." in prompt
    assert "Do not run the file-level workflow. Do not process any other row." in prompt
    assert f"Task id: {task_id}" in prompt
    assert f"Raw log root: {layout.logs_root / 'model' / 'mode'}/ (.json -> .log)" in prompt
    assert "Return JSON only with keys: task_id, answer_failure_summary, events." in prompt


def test_load_prompt_artifacts_reads_task_plan_and_log_text(tmp_path):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")
    layout = infer_layout(eval_path)
    task_id = "tasks_mini/k-4-d-1/task_3.json"
    task_path = tmp_path / task_id
    plan_path = tmp_path / "plans_mini" / "k-4-d-1" / "task_3.json"
    log_path = layout.logs_root / "model" / "mode" / "tasks_mini" / "k-4-d-1" / "task_3.log"
    task_path.parent.mkdir(parents=True)
    plan_path.parent.mkdir(parents=True)
    log_path.parent.mkdir(parents=True)
    task_path.write_text('{"question": "Which value?"}\n')
    plan_path.write_text('{"reasoning_chain_text": "Find the source, then compute."}\n')
    log_path.write_text("--- Turn 1 ---\nExecuting: search_ideal({})\n")

    artifacts = _load_prompt_artifacts(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        task_id=task_id,
        log_path=log_path,
    )

    assert artifacts["task_path"] == task_path
    assert artifacts["plan_path"] == plan_path
    assert '"question": "Which value?"' in artifacts["task_text"]
    assert "Find the source, then compute." in artifacts["plan_text"]
    assert "Executing: search_ideal" in artifacts["log_text"]


def test_row_prompt_embeds_task_plan_log_for_codex_and_openai(tmp_path):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")
    layout = infer_layout(eval_path)
    task_id = "tasks_mini/k-4-d-1/task_3.json"
    (tmp_path / "tasks_mini" / "k-4-d-1").mkdir(parents=True)
    (tmp_path / "plans_mini" / "k-4-d-1").mkdir(parents=True)
    log_path = layout.logs_root / "model" / "mode" / "tasks_mini" / "k-4-d-1" / "task_3.log"
    log_path.parent.mkdir(parents=True)
    (tmp_path / task_id).write_text('{"question": "embedded task"}\n')
    (tmp_path / "plans_mini" / "k-4-d-1" / "task_3.json").write_text('{"plan": "embedded plan"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: embedded log\n")

    prompts = [
        _build_row_prompt(
            layout=layout,
            source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            task_id=task_id,
            log_path=log_path,
            backend=backend,
        )
        for backend in ("codex", "openai")
    ]

    for prompt in prompts:
        assert "Task JSON:" in prompt
        assert "Plan JSON:" in prompt
        assert "Raw log:" in prompt
        assert "embedded task" in prompt
        assert "embedded plan" in prompt
        assert "embedded log" in prompt


def test_find_pending_eval_paths_lists_missing_or_invalid_outputs(tmp_path):
    source_eval = tmp_path / "results_semantic" / "modes" / "model" / "missing_output" / "eval_results.csv"
    invalid_eval = tmp_path / "results_semantic" / "modes" / "model" / "invalid_output" / "eval_results.csv"
    complete_eval = tmp_path / "results_semantic" / "modes" / "model" / "complete_output" / "eval_results.csv"
    for path in (source_eval, invalid_eval, complete_eval):
        _write_csv(
            path,
            ["task_id", "semantic_bucket", "semantic_match"],
            [{"task_id": "tasks_mini/k-1-d-1/task_1.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0"}],
        )

    invalid_layout = infer_layout(invalid_eval)
    complete_layout = infer_layout(complete_eval)
    for layout, validation_status in ((invalid_layout, "invalid"), (complete_layout, "valid")):
        _write_csv(
            layout.mirrored_eval_path,
            ["task_id", "semantic_bucket", "semantic_match", "answer_failure_validation_status"],
            [
                {
                    "task_id": "tasks_mini/k-1-d-1/task_1.json",
                    "semantic_bucket": "semantic_incorrect",
                    "semantic_match": "0",
                    "answer_failure_validation_status": validation_status,
                }
            ],
        )
        layout.mirrored_events_path.parent.mkdir(parents=True, exist_ok=True)
        layout.mirrored_events_path.write_text("task_id,model_variant,mode_variant,event_index,answer_failure_type,answer_failure_subtype,failure_stage,failure_summary,failure_evidence,confidence\n")
        layout.mirrored_report_path.write_text("# report\n")

    pending = find_pending_eval_paths(tmp_path, source_root_name="results_semantic")

    assert pending == [invalid_eval.resolve(), source_eval.resolve()]


def test_eval_pending_stats_counts_pending_and_invalid_rows(tmp_path):
    source_eval = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    _write_csv(
        source_eval,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": "tasks_mini/k-1-d-1/task_1.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": "tasks_mini/k-1-d-1/task_2.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": "tasks_mini/k-1-d-1/task_3.json", "semantic_bucket": "semantic_correct", "semantic_match": "1"},
        ],
    )
    layout = infer_layout(source_eval)
    _write_csv(
        layout.mirrored_eval_path,
        ["task_id", "semantic_bucket", "semantic_match", "answer_failure_validation_status"],
        [
            {"task_id": "tasks_mini/k-1-d-1/task_1.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0", "answer_failure_validation_status": "invalid"},
            {"task_id": "tasks_mini/k-1-d-1/task_2.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0", "answer_failure_validation_status": ""},
            {"task_id": "tasks_mini/k-1-d-1/task_3.json", "semantic_bucket": "semantic_correct", "semantic_match": "1", "answer_failure_validation_status": ""},
        ],
    )
    layout.mirrored_events_path.parent.mkdir(parents=True, exist_ok=True)
    layout.mirrored_events_path.write_text("task_id,model_variant,mode_variant,event_index,answer_failure_type,answer_failure_subtype,failure_stage,failure_summary,failure_evidence,confidence\n")
    layout.mirrored_report_path.write_text("# report\n")

    stats = eval_pending_stats(source_eval)

    assert stats.eligible_rows == 2
    assert stats.pending_rows == 1
    assert stats.invalid_rows == 1
    assert stats.has_all_artifacts


def test_eval_pending_stats_excludes_existing_temp_json_audits(tmp_path):
    source_eval = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    cached_task = "tasks_mini/k-1-d-1/task_1.json"
    missing_task = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        source_eval,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": cached_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": missing_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        ],
    )
    layout = infer_layout(source_eval)
    tmp_root = tmp_path / ".tmp_answer_failure_audits"
    out_path = _audit_json_path(tmp_root, layout, cached_task)
    out_path.parent.mkdir(parents=True)
    out_path.write_text(json.dumps({"task_id": cached_task, "answer_failure_summary": "cached", "events": []}))

    stats = eval_pending_stats(source_eval, tmp_root=tmp_root)

    assert stats.pending_rows == 1
    assert stats.pending_task_ids == (missing_task,)
    assert not stats.has_all_artifacts


def test_eval_pending_stats_excludes_existing_journal_audits(tmp_path):
    source_eval = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    cached_task = "tasks_mini/k-1-d-1/task_1.json"
    missing_task = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        source_eval,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": cached_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": missing_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        ],
    )
    layout = infer_layout(source_eval)
    journal_path = tmp_path / "answer_failure_audits.jsonl"
    audit = {"task_id": cached_task, "answer_failure_summary": "cached", "events": []}
    _append_journal_record(journal_path, layout=layout, task_id=cached_task, status="ok", audit=audit)

    stats = eval_pending_stats(source_eval, journal_path=journal_path)

    assert stats.pending_rows == 1
    assert stats.pending_task_ids == (missing_task,)


def test_eval_pending_stats_excludes_invalid_rows_with_existing_temp_json_audits(tmp_path):
    source_eval = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    cached_invalid = "tasks_mini/k-1-d-1/task_1.json"
    still_invalid = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        source_eval,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": cached_invalid, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": still_invalid, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        ],
    )
    layout = infer_layout(source_eval)
    _write_csv(
        layout.mirrored_eval_path,
        ["task_id", "semantic_bucket", "semantic_match", "answer_failure_validation_status"],
        [
            {"task_id": cached_invalid, "semantic_bucket": "semantic_incorrect", "semantic_match": "0", "answer_failure_validation_status": "invalid"},
            {"task_id": still_invalid, "semantic_bucket": "semantic_incorrect", "semantic_match": "0", "answer_failure_validation_status": "invalid"},
        ],
    )
    layout.mirrored_events_path.parent.mkdir(parents=True, exist_ok=True)
    layout.mirrored_events_path.write_text(
        "task_id,model_variant,mode_variant,event_index,answer_failure_type,answer_failure_subtype,failure_stage,failure_summary,failure_evidence,confidence\n"
    )
    layout.mirrored_report_path.write_text("# report\n")
    tmp_root = tmp_path / ".tmp_answer_failure_audits"
    out_path = _audit_json_path(tmp_root, layout, cached_invalid)
    out_path.parent.mkdir(parents=True)
    out_path.write_text(json.dumps({"task_id": cached_invalid, "answer_failure_summary": "cached", "events": []}))

    stats = eval_pending_stats(source_eval, tmp_root=tmp_root)

    assert stats.pending_rows == 0
    assert stats.invalid_rows == 1
    assert stats.invalid_task_ids == (still_invalid,)
    assert stats.has_all_artifacts


def test_find_pending_eval_stats_excludes_complete_outputs(tmp_path):
    missing_eval = tmp_path / "results_semantic" / "modes" / "model" / "missing" / "eval_results.csv"
    complete_eval = tmp_path / "results_semantic" / "modes" / "model" / "complete" / "eval_results.csv"
    for path in (missing_eval, complete_eval):
        _write_csv(path, ["task_id", "semantic_bucket", "semantic_match"], [
            {"task_id": "tasks_mini/k-1-d-1/task_1.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0"}
        ])
    complete_layout = infer_layout(complete_eval)
    _write_csv(
        complete_layout.mirrored_eval_path,
        ["task_id", "semantic_bucket", "semantic_match", "answer_failure_validation_status"],
        [{"task_id": "tasks_mini/k-1-d-1/task_1.json", "semantic_bucket": "semantic_incorrect", "semantic_match": "0", "answer_failure_validation_status": "valid"}],
    )
    complete_layout.mirrored_events_path.parent.mkdir(parents=True, exist_ok=True)
    complete_layout.mirrored_events_path.write_text("task_id,model_variant,mode_variant,event_index,answer_failure_type,answer_failure_subtype,failure_stage,failure_summary,failure_evidence,confidence\n")
    complete_layout.mirrored_report_path.write_text("# report\n")

    stats = find_pending_eval_stats(tmp_path, source_root_name="results_semantic")

    assert [item.eval_path for item in stats] == [missing_eval.resolve()]
    assert stats[0].pending_rows == 1
    assert stats[0].invalid_rows == 0


def test_choose_pending_eval_path_returns_numbered_selection(tmp_path, monkeypatch, capsys):
    first = tmp_path / "results_semantic" / "modes" / "model" / "a" / "eval_results.csv"
    second = tmp_path / "results_semantic" / "modes" / "model" / "b" / "eval_results.csv"
    for path in (first, second):
        _write_csv(path, ["task_id", "semantic_bucket", "semantic_match"], [])

    monkeypatch.setattr("builtins.input", lambda _: "2")

    selected = choose_pending_eval_path(repo_root=tmp_path, source_root_name="results_semantic")

    assert selected == second.resolve()
    output = capsys.readouterr().out
    assert "1. results_semantic/modes/model/a/eval_results.csv pending_rows=0 invalid_rows=0" in output
    assert "2. results_semantic/modes/model/b/eval_results.csv pending_rows=0 invalid_rows=0" in output


def test_journal_roundtrip_loads_latest_successful_audit(tmp_path):
    eval_path = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_plani_computei_k5_skills_off"
        / "eval_results.csv"
    )
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")
    layout = infer_layout(eval_path)
    journal_path = tmp_path / "audit.jsonl"
    task_id = "tasks_mini/k-1-d-1/task_1.json"
    first_audit = {"task_id": task_id, "answer_failure_summary": "old", "events": []}
    latest_audit = {"task_id": task_id, "answer_failure_summary": "new", "events": []}

    _append_journal_record(journal_path, layout=layout, task_id=task_id, status="ok", audit=first_audit)
    _append_journal_record(journal_path, layout=layout, task_id=task_id, status="error", error="transient")
    _append_journal_record(journal_path, layout=layout, task_id=task_id, status="ok", audit=latest_audit)

    assert _load_journal_audits(journal_path, layout) == {task_id: latest_audit}


def test_default_journal_path_is_readable_for_target_variant(tmp_path):
    eval_path = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_plani_computei_k5_skills_off"
        / "eval_results.csv"
    )
    eval_path.parent.mkdir(parents=True)
    eval_path.write_text("task_id,semantic_bucket,semantic_match\n")
    layout = infer_layout(eval_path)

    assert _default_journal_path(layout) == Path(
        "/tmp/answer_failure_audits_results_semantic_openai_gpt5mini_search_d_plani_computei.jsonl"
    )


def test_temp_and_journal_paths_are_source_root_isolated(tmp_path):
    lakeqa_eval = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_plani_computei_k5_skills_off"
        / "eval_results.csv"
    )
    kramabench_eval = (
        tmp_path
        / "results-kramabench_semantic"
        / "modes"
        / "openai_gpt-5-mini"
        / "search_d_results_i_plani_computei_k5_skills_off"
        / "eval_results.csv"
    )
    lakeqa_eval.parent.mkdir(parents=True)
    kramabench_eval.parent.mkdir(parents=True)
    lakeqa_eval.write_text("task_id,semantic_bucket,semantic_match\n")
    kramabench_eval.write_text("task_id,semantic_bucket,semantic_match\n")
    lakeqa_layout = infer_layout(lakeqa_eval)
    kramabench_layout = infer_layout(kramabench_eval)

    assert _temp_dir_for_layout(tmp_path / ".tmp", lakeqa_layout) == (
        tmp_path
        / ".tmp"
        / "results_semantic"
        / "openai_gpt-5-mini__search_d_results_i_plani_computei_k5_skills_off"
    )
    assert _temp_dir_for_layout(tmp_path / ".tmp", kramabench_layout) == (
        tmp_path
        / ".tmp"
        / "results-kramabench_semantic"
        / "openai_gpt-5-mini__search_d_results_i_plani_computei_k5_skills_off"
    )
    assert _default_journal_path(lakeqa_layout) != _default_journal_path(kramabench_layout)
    assert _default_journal_path(kramabench_layout).name.startswith(
        "answer_failure_audits_results_kramabench_semantic_"
    )


def test_openai_api_key_falls_back_to_dotenv(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    (tmp_path / ".env").write_text("OTHER=value\nOPENAI_API_KEY=test-key\n")

    assert _openai_api_key(tmp_path) == "test-key"


def test_normalized_events_maps_common_model_shortlabels_to_taxonomy():
    events = _normalized_events(
        {
            "task_id": "task",
            "events": [
                {
                    "event_index": 1,
                    "answer_failure_type": "computation",
                    "answer_failure_subtype": "wrong_total",
                    "failure_stage": "computation",
                    "failure_summary": "Used the wrong total.",
                    "failure_evidence": "Turn 3 | computed wrong total",
                    "confidence": "high",
                },
                {
                    "event_index": 2,
                    "answer_failure_type": "data_access",
                    "answer_failure_subtype": "",
                    "failure_stage": "data_access",
                    "failure_summary": "The file was too large.",
                    "failure_evidence": "Turn 4 | file too large",
                    "confidence": "high",
                },
                {
                    "event_index": 3,
                    "answer_failure_type": "source_selection_error",
                    "answer_failure_subtype": "",
                    "failure_stage": "source_selection",
                    "failure_summary": "Used the wrong county.",
                    "failure_evidence": "Turn 5 | wrong county",
                    "confidence": "medium",
                },
            ],
        }
    )

    assert events[0]["answer_failure_type"] == "computation_or_aggregation_error"
    assert events[1]["answer_failure_type"] == "tool_or_data_blocker"
    assert events[1]["answer_failure_subtype"] == "data_source_missing_or_unavailable"
    assert events[2]["answer_failure_type"] == "wrong_source_or_scope"


def test_task_ids_for_deterministic_repair_uses_invalid_rows_only():
    outputs = {
        "invalid_rows": [
            {"task_id": "tasks_mini/k-1-d-1/task_1.json", "answer_failure_validation_status": "invalid"},
            {"task_id": "tasks_mini/k-1-d-1/task_2.json", "answer_failure_validation_status": "missing_log"},
            {"task_id": "tasks_mini/k-1-d-1/task_3.json", "answer_failure_validation_status": "invalid"},
        ]
    }

    assert _task_ids_for_deterministic_repair(outputs) == [
        "tasks_mini/k-1-d-1/task_1.json",
        "tasks_mini/k-1-d-1/task_3.json",
    ]


def test_validated_batch_repair_rejects_empty_repaired_rows():
    original = {"task_id": "task", "answer_failure_summary": "old", "events": [{"event_index": 1}]}
    repaired = {"task_id": "task", "answer_failure_summary": "empty", "events": []}

    accepted, notes = _validated_batch_repair(original, repaired)

    assert accepted == original
    assert "empty repaired_row" in notes


def test_write_mirrored_outputs_preserves_source_rows_and_writes_events(tmp_path):
    eval_path = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "model"
        / "mode"
        / "eval_results.csv"
    )
    task_id = "tasks_mini/k-1-d-1/task_1.json"
    correct_task_id = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        eval_path,
        ["task_id", "semantic_bucket", "semantic_match", "exact_match"],
        [
            {
                "task_id": task_id,
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "exact_match": "0",
            },
            {
                "task_id": correct_task_id,
                "semantic_bucket": "semantic_correct",
                "semantic_match": "1",
                "exact_match": "1",
            },
        ],
    )
    layout = infer_layout(eval_path)

    outputs = write_mirrored_outputs(
        layout,
        {
            task_id: {
                "task_id": task_id,
                "answer_failure_summary": "The run queried the wrong source.",
                "events": [
                    {
                        "event_index": 1,
                        "answer_failure_type": "wrong_source_or_scope",
                        "answer_failure_subtype": "wrong_dataset",
                        "failure_stage": "source_selection",
                        "failure_summary": "The run queried the wrong source.",
                        "failure_evidence": 'Turn 2 | Executing: query_file({"dataset_id": "wrong"})',
                        "confidence": "high",
                    }
                ],
            }
        },
        model_validation_by_task={
            task_id: {
                "status": "pass",
                "notes": "batch validator accepted the row audit",
            }
        },
    )

    assert outputs["eval_path"] == layout.mirrored_eval_path
    assert outputs["events_path"] == layout.mirrored_events_path

    with layout.mirrored_eval_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["answer_failure_summary"] == "The run queried the wrong source."
    assert rows[0]["answer_failure_types"] == "wrong_source_or_scope"
    assert rows[0]["answer_failure_event_count"] == "1"
    assert rows[0]["answer_failure_model_validation_status"] == "pass"
    assert rows[0]["answer_failure_model_validation_notes"] == "batch validator accepted the row audit"
    assert all(value == "" for key, value in rows[1].items() if key.startswith("answer_failure"))

    with layout.mirrored_events_path.open(newline="") as handle:
        events = list(csv.DictReader(handle))
    assert events == [
        {
            "task_id": task_id,
            "model_variant": "model",
            "mode_variant": "mode",
            "event_index": "1",
            "answer_failure_type": "wrong_source_or_scope",
            "answer_failure_subtype": "wrong_dataset",
            "failure_stage": "source_selection",
            "failure_summary": "The run queried the wrong source.",
            "failure_evidence": 'Turn 2 | Executing: query_file({"dataset_id": "wrong"})',
            "confidence": "high",
        }
    ]
