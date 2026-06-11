import csv
import json
from pathlib import Path

from sana_analysis.answer_failure_audit_runner import (
    CURRENT_AUDIT_SCHEMA_VERSION,
    CURRENT_TRACE_SCHEMA_VERSION,
    DEFAULT_AUDITOR_MODEL,
    DEFAULT_AUDITOR_REASONING,
    DEFAULT_ROW_AUDIT_PIPELINE,
    DEFAULT_ROW_MODEL,
    DEFAULT_ROW_REASONING,
    _build_row_model_validator_prompt,
    _build_row_prompt,
    _build_trace_extractor_prompt,
    _build_trace_labeler_prompt,
    _expand_trace_labeler_output,
    _append_journal_record,
    _answer_failure_output_summary,
    _audit_json_path,
    _default_journal_path,
    _load_journal_audits,
    _model_validator_stale_task_ids,
    _load_prompt_artifacts,
    _normalized_events,
    _openai_api_key,
    _temp_dir_for_layout,
    eval_pending_stats,
    _task_ids_for_deterministic_repair,
    _validated_batch_repair,
    build_arg_parser,
    choose_pending_eval_path,
    find_pending_eval_stats,
    find_pending_eval_paths,
    infer_layout,
    parse_json_object,
    run_row_audit,
    run_model_validators,
    write_mirrored_outputs,
)
from sana_analysis.answer_failure_taxonomy import ANSWER_FAILURE_FIGURE_GROUPS
from sana_analysis.answer_failure_validation import validate_answer_failure_row
from sana_analysis.combine_answer_failure_grouped_models import ANSWER_FAILURE_GROUPS


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

    assert "You are auditing one failed QA run." in prompt
    assert "Audit exactly this task_id and no other row:" in prompt
    assert "SKILL.md" not in prompt
    assert "answer_failure_audit_runner.py" not in prompt
    assert "spawn" not in prompt.lower()
    assert f"Task id: {task_id}" in prompt
    assert f"Raw log root: {layout.logs_root / 'model' / 'mode'}/ (.json -> .log)" in prompt
    assert "Return JSON only with keys: task_id, answer_failure_summary, events." in prompt
    assert "Allowed answer_failure_type values:" in prompt
    assert "- wrong_source_or_dataset: The agent used the wrong dataset" in prompt
    assert "- wrong_scope_or_filter: The agent used the right general source" in prompt
    assert "- computation_or_aggregation_error: The correct evidence population" in prompt
    assert "Boundary rules:" in prompt
    assert "failure_stage must be exactly one of:" in prompt
    assert '"failure_stage": "task_understanding"' in prompt
    assert '"failure_stage": "task_understanding | source_selection' not in prompt


def test_row_and_validator_defaults_use_mini_high_reasoning():
    args = build_arg_parser().parse_args([])

    assert DEFAULT_ROW_MODEL == "gpt-5.4-mini"
    assert DEFAULT_ROW_REASONING == "high"
    assert DEFAULT_AUDITOR_MODEL == "gpt-5.4-mini"
    assert DEFAULT_AUDITOR_REASONING == "high"
    assert args.row_model == "gpt-5.4-mini"
    assert args.row_reasoning_effort == "high"
    assert args.auditor_model == "gpt-5.4-mini"
    assert args.auditor_reasoning_effort == "high"


def test_default_row_audit_pipeline_is_two_stage():
    args = build_arg_parser().parse_args([])

    assert DEFAULT_ROW_AUDIT_PIPELINE == "two-stage"
    assert args.row_audit_pipeline == "two-stage"


def test_trace_extractor_prompt_is_stage_a_evidence_only(tmp_path):
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
    plan_path.write_text('{"reasoning_chain_text": "Find source then compute"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: evidence line\n")

    prompt = _build_trace_extractor_prompt(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        task_id=task_id,
        log_path=log_path,
    )

    assert "Stage A: extract a compact evidence trace" in prompt
    assert "Do not assign answer_failure_type" in prompt
    assert "answer_failure_subtype" not in prompt
    assert "Allowed answer_failure_type values:" not in prompt
    assert "candidate_failures" not in prompt
    assert "material_observations" in prompt
    assert "These are factual observations, not taxonomy labels." in prompt
    assert "role must be exactly one of:" in prompt
    assert '"role": "source_choice | extraction | computation | final_answer | blocker | plan_mismatch | other"' not in prompt
    assert '"uncertainty": "low | medium | high"' not in prompt
    assert '"role": "source_choice"' in prompt
    assert '"uncertainty": "low"' in prompt
    assert "Turn 12 | Executing: query_ideal(... year=2022 ...)" in prompt
    assert "The task asks for 2023, but this query uses 2022." in prompt
    assert "The run used 2022 data for a 2023 question." in prompt
    assert "final_answer" in prompt
    assert "Turn 2" in prompt
    assert "evidence line" in prompt


def test_trace_labeler_prompt_uses_trace_and_taxonomy_without_full_raw_log(tmp_path):
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
    plan_path.write_text('{"reasoning_chain_text": "Find source then compute"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: full raw log text should not be embedded here\n")
    trace = {
        "task_id": task_id,
        "trace_summary": "The agent used the wrong source.",
        "evidence_items": [
            {
                "evidence_id": "E1",
                "turn": 2,
                "raw_log_excerpt": "Turn 2 | Tool result: trace excerpt",
                "role": "source_choice",
                "why_relevant": "Shows the source choice.",
            }
        ],
        "material_observations": [
            {
                "observation_id": "O1",
                "evidence_ids": ["E1"],
                "observation": "The source does not match the requested scope.",
                "materiality": "The final answer is based on this source.",
                "uncertainty": "low",
            }
        ],
    }

    prompt = _build_trace_labeler_prompt(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        task_id=task_id,
        trace=trace,
        log_path=log_path,
    )

    assert "Stage B: label answer-failure events" in prompt
    assert "Your primary job is classification, not summarization." in prompt
    assert "Do not read or request the full raw log" in prompt
    assert "Do not choose answer_failure_figure_group" in prompt
    assert "Return JSON only with keys: task_id, events." in prompt
    assert "Trace JSON:" in prompt
    assert "Allowed answer_failure_type values:" in prompt
    assert "wrong_source_or_dataset" in prompt
    assert "wrong_scope_or_filter" in prompt
    assert "computation_or_aggregation_error" in prompt
    assert "Turn 2 | Tool result: trace excerpt" in prompt
    assert '"observation_id": "O1"' in prompt
    assert '"evidence_ids": ["E1"]' in prompt
    assert "answer_failure_summary" not in prompt
    assert "failure_stage" not in prompt
    assert "failure_summary" not in prompt
    assert "confidence" not in prompt
    assert "CSV row JSON:" not in prompt
    assert "Task JSON:" not in prompt
    assert "Plan JSON:" not in prompt
    assert "Raw log:" not in prompt
    assert "full raw log text should not be embedded here" not in prompt


def test_expand_trace_labeler_output_fills_validation_fields_from_trace():
    task_id = "tasks_mini/k-4-d-1/task_3.json"
    trace = {
        "task_id": task_id,
        "trace_summary": "The run used the wrong year.",
        "evidence_items": [
            {
                "evidence_id": "E1",
                "turn": 12,
                "raw_log_excerpt": "Turn 12 | Executing: query_ideal(... year=2022 ...)",
                "role": "source_choice",
                "why_relevant": "The task asks for 2023, but this query uses 2022.",
            }
        ],
        "material_observations": [
            {
                "observation_id": "O1",
                "evidence_ids": ["E1"],
                "observation": "The run used 2022 data for a 2023 question.",
                "materiality": "The final answer was computed from that wrong-year query.",
                "uncertainty": "low",
            }
        ],
    }
    label_payload = {
        "task_id": task_id,
        "events": [
            {
                "event_index": 1,
                "observation_id": "O1",
                "answer_failure_type": "wrong_scope_or_filter",
                "answer_failure_subtype": "wrong_year",
                "evidence_ids": ["E1"],
            }
        ],
    }

    audit = _expand_trace_labeler_output(task_id=task_id, trace=trace, label_payload=label_payload)

    assert audit == {
        "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
        "task_id": task_id,
        "answer_failure_summary": "The run used 2022 data for a 2023 question.",
        "events": [
            {
                "event_index": 1,
                "answer_failure_type": "wrong_scope_or_filter",
                "answer_failure_subtype": "wrong_year",
                "failure_stage": "source_selection",
                "failure_summary": "The run used 2022 data for a 2023 question.",
                "failure_evidence": "Turn 12 | Executing: query_ideal(... year=2022 ...)",
                "confidence": "high",
            }
        ],
    }


def test_expand_trace_labeler_output_keeps_missing_evidence_invalid():
    task_id = "tasks_mini/k-4-d-1/task_3.json"
    trace = {
        "answer_failure_trace_schema_version": CURRENT_TRACE_SCHEMA_VERSION,
        "task_id": task_id,
        "trace_summary": "The run used the wrong source.",
        "evidence_items": [
            {
                "evidence_id": "E1",
                "turn": 12,
                "raw_log_excerpt": "Turn 12 | Tool result: useful evidence",
                "role": "source_choice",
                "why_relevant": "Shows the source.",
            }
        ],
        "material_observations": [
            {
                "observation_id": "O1",
                "evidence_ids": ["MISSING"],
                "observation": "The labeler selected unavailable evidence.",
                "materiality": "The final answer cannot be grounded by that selected evidence.",
                "uncertainty": "low",
            }
        ],
    }
    label_payload = {
        "task_id": task_id,
        "events": [
            {
                "event_index": 1,
                "observation_id": "O1",
                "answer_failure_type": "wrong_scope_or_filter",
                "answer_failure_subtype": "wrong_source",
                "evidence_ids": ["MISSING"],
            }
        ],
    }

    audit = _expand_trace_labeler_output(task_id=task_id, trace=trace, label_payload=label_payload)

    assert audit["events"][0]["failure_evidence"] == ""


def test_two_stage_row_audit_runs_trace_then_labeler_per_row(tmp_path, monkeypatch):
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
    plan_path.write_text('{"reasoning_chain_text": "Find source then compute"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: evidence\n")
    prompts: list[str] = []

    def fake_call_model(prompt, **kwargs):
        prompts.append(prompt)
        if "Stage A: extract a compact evidence trace" in prompt:
            return json.dumps(
                {
                    "task_id": task_id,
                    "trace_summary": "Wrong source.",
                    "evidence_items": [
                        {
                            "evidence_id": "E1",
                            "turn": 2,
                            "raw_log_excerpt": "Turn 2 | Tool result: evidence",
                            "role": "source_choice",
                            "why_relevant": "Wrong source evidence.",
                        }
                    ],
                    "material_observations": [
                        {
                            "observation_id": "O1",
                            "evidence_ids": ["E1"],
                            "observation": "Wrong source.",
                            "materiality": "Answer depended on it.",
                            "uncertainty": "low",
                        }
                    ],
                }
            )
        return json.dumps(
            {
                "task_id": task_id,
                "events": [
                    {
                        "event_index": 1,
                        "observation_id": "O1",
                        "answer_failure_type": "wrong_source_or_dataset",
                        "answer_failure_subtype": "wrong_source",
                        "evidence_ids": ["E1"],
                    }
                ],
            }
        )

    monkeypatch.setattr("sana_analysis.answer_failure_audit_runner._call_model", fake_call_model)

    returned_task_id, audit = run_row_audit(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        tmp_root=tmp_path / ".tmp",
        backend="codex",
        model="gpt-test",
        reasoning_effort="low",
        timeout=30,
        force=False,
        pipeline="two-stage",
    )

    trace_path = _audit_json_path(tmp_path / ".tmp", layout, task_id).with_suffix(".trace.json")
    audit_path = _audit_json_path(tmp_path / ".tmp", layout, task_id)
    assert returned_task_id == task_id
    assert [("Stage A" in prompt, "Stage B" in prompt) for prompt in prompts] == [(True, False), (False, True)]
    assert trace_path.exists()
    assert audit_path.exists()
    assert json.loads(trace_path.read_text())["answer_failure_trace_schema_version"] == CURRENT_TRACE_SCHEMA_VERSION
    assert json.loads(audit_path.read_text())["answer_failure_audit_schema_version"] == CURRENT_AUDIT_SCHEMA_VERSION
    assert audit["events"][0]["answer_failure_type"] == "wrong_source_or_dataset"
    assert audit["events"][0]["failure_stage"] == "source_selection"
    assert audit["events"][0]["failure_summary"] == "Wrong source."
    assert audit["events"][0]["failure_evidence"] == "Turn 2 | Tool result: evidence"


def test_two_stage_row_audit_ignores_stale_schema_cache(tmp_path, monkeypatch):
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
    plan_path.write_text('{"reasoning_chain_text": "Find source then compute"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: fresh evidence\n")
    tmp_root = tmp_path / ".tmp"
    stale_path = _audit_json_path(tmp_root, layout, task_id)
    stale_trace_path = stale_path.with_suffix(".trace.json")
    stale_path.parent.mkdir(parents=True)
    stale_path.write_text(json.dumps({"task_id": task_id, "answer_failure_summary": "stale", "events": []}))
    stale_trace_path.write_text(json.dumps({"task_id": task_id, "trace_summary": "stale trace"}))
    prompts: list[str] = []

    def fake_call_model(prompt, **kwargs):
        prompts.append(prompt)
        if "Stage A: extract a compact evidence trace" in prompt:
            return json.dumps(
                {
                    "task_id": task_id,
                    "trace_summary": "Fresh trace.",
                    "evidence_items": [
                        {
                            "evidence_id": "E1",
                            "turn": 2,
                            "raw_log_excerpt": "Turn 2 | Tool result: fresh evidence",
                            "role": "source_choice",
                            "why_relevant": "Fresh source evidence.",
                        }
                    ],
                    "material_observations": [
                        {
                            "observation_id": "O1",
                            "evidence_ids": ["E1"],
                            "observation": "Fresh source issue.",
                            "materiality": "Answer depended on it.",
                            "uncertainty": "low",
                        }
                    ],
                }
            )
        return json.dumps(
            {
                "task_id": task_id,
                "events": [
                    {
                        "event_index": 1,
                        "observation_id": "O1",
                        "answer_failure_type": "wrong_source_or_dataset",
                        "answer_failure_subtype": "wrong_source",
                        "evidence_ids": ["E1"],
                    }
                ],
            }
        )

    monkeypatch.setattr("sana_analysis.answer_failure_audit_runner._call_model", fake_call_model)

    _, audit = run_row_audit(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        tmp_root=tmp_root,
        backend="codex",
        model="gpt-test",
        reasoning_effort="low",
        timeout=30,
        force=False,
        pipeline="two-stage",
    )

    assert [("Stage A" in prompt, "Stage B" in prompt) for prompt in prompts] == [(True, False), (False, True)]
    assert audit["answer_failure_summary"] == "Fresh source issue."


def test_repair_row_prompt_uses_self_contained_taxonomy_language(tmp_path):
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
        repair_notes="event 1: invalid answer_failure_type",
    )

    assert "Use only allowed answer_failure_type taxonomy labels from the allowed list above." in prompt
    assert "from the skill" not in prompt


def test_row_model_validator_prompt_is_one_row_and_embeds_context(tmp_path):
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
    plan_path.write_text('{"reasoning_chain_text": "Find source then compute"}\n')
    log_path.write_text("--- Turn 2 ---\nTool result: useful evidence\n")

    prompt = _build_row_model_validator_prompt(
        layout=layout,
        source_row={"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        task_id=task_id,
        audit={"task_id": task_id, "answer_failure_summary": "bad source", "events": []},
        deterministic_status={"status": "valid", "notes": ""},
        log_path=log_path,
    )

    assert "You are validating one answer-failure row audit." in prompt
    assert "Do not validate any other task_id." in prompt
    assert "final batch auditor" not in prompt
    assert f"Task id: {task_id}" in prompt
    assert "Row audit JSON:" in prompt
    assert "CSV row JSON:" in prompt
    assert "Task JSON:" in prompt
    assert "Plan JSON:" in prompt
    assert "Raw log:" in prompt
    assert "useful evidence" in prompt


def test_run_model_validators_calls_one_prompt_per_valid_row(tmp_path, monkeypatch):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    first_task = "tasks_mini/k-1-d-1/task_1.json"
    second_task = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        eval_path,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": first_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": second_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        ],
    )
    layout = infer_layout(eval_path)
    audits_by_task = {
        first_task: {"task_id": first_task, "answer_failure_summary": "first", "events": [{"event_index": 1}]},
        second_task: {"task_id": second_task, "answer_failure_summary": "second", "events": [{"event_index": 1}]},
    }
    deterministic_by_task = {
        first_task: {"status": "valid", "notes": ""},
        second_task: {"status": "valid_with_warnings", "notes": "warning"},
    }
    prompts: list[str] = []

    def fake_call_model(prompt, **kwargs):
        prompts.append(prompt)
        task_id = first_task if first_task in prompt else second_task
        return json.dumps({"task_id": task_id, "verdict": "pass", "problems": []})

    monkeypatch.setattr("sana_analysis.answer_failure_audit_runner._call_model", fake_call_model)

    validation_by_task, repaired_audits = run_model_validators(
        layout=layout,
        tmp_root=tmp_path / ".tmp",
        audits_by_task=audits_by_task,
        deterministic_by_task=deterministic_by_task,
        backend="codex",
        model="gpt-test",
        reasoning_effort="low",
        timeout=30,
        allow_downgrade=True,
        concurrency=1,
    )

    assert len(prompts) == 2
    assert all("You are validating one answer-failure row audit." in prompt for prompt in prompts)
    assert validation_by_task[first_task]["status"] == "pass"
    assert validation_by_task[second_task]["status"] == "pass"
    assert repaired_audits == audits_by_task


def test_model_validator_stale_task_ids_only_selects_usable_blank_or_untrusted_rows():
    audits_by_task = {
        "valid_pass": {},
        "valid_blank": {},
        "valid_untrusted": {},
        "warning_repaired": {},
        "invalid_untrusted": {},
    }
    deterministic_by_task = {
        "valid_pass": {"status": "valid"},
        "valid_blank": {"status": "valid"},
        "valid_untrusted": {"status": "valid"},
        "warning_repaired": {"status": "valid_with_warnings"},
        "invalid_untrusted": {"status": "invalid"},
    }
    model_validation_by_task = {
        "valid_pass": {"status": "pass"},
        "valid_blank": {"status": ""},
        "valid_untrusted": {"status": "invalid_untrusted"},
        "warning_repaired": {"status": "repaired_pass"},
        "invalid_untrusted": {"status": "invalid_untrusted"},
    }

    assert _model_validator_stale_task_ids(
        audits_by_task=audits_by_task,
        deterministic_by_task=deterministic_by_task,
        existing_model_validation_by_task=model_validation_by_task,
    ) == ["valid_blank", "valid_untrusted"]
    assert _model_validator_stale_task_ids(
        audits_by_task=audits_by_task,
        deterministic_by_task=deterministic_by_task,
        existing_model_validation_by_task=model_validation_by_task,
        only_task_ids={"valid_untrusted", "warning_repaired"},
    ) == ["valid_untrusted"]


def test_run_model_validators_can_limit_to_selected_stale_rows(tmp_path, monkeypatch):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    first_task = "tasks_mini/k-1-d-1/task_1.json"
    second_task = "tasks_mini/k-1-d-1/task_2.json"
    _write_csv(
        eval_path,
        ["task_id", "semantic_bucket", "semantic_match"],
        [
            {"task_id": first_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
            {"task_id": second_task, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"},
        ],
    )
    layout = infer_layout(eval_path)
    audits_by_task = {
        first_task: {"task_id": first_task, "answer_failure_summary": "first", "events": [{"event_index": 1}]},
        second_task: {"task_id": second_task, "answer_failure_summary": "second", "events": [{"event_index": 1}]},
    }
    deterministic_by_task = {
        first_task: {"status": "valid", "notes": ""},
        second_task: {"status": "valid", "notes": ""},
    }
    prompts: list[str] = []

    def fake_call_model(prompt, **kwargs):
        prompts.append(prompt)
        return json.dumps({"task_id": second_task, "verdict": "pass", "problems": []})

    monkeypatch.setattr("sana_analysis.answer_failure_audit_runner._call_model", fake_call_model)

    validation_by_task, _ = run_model_validators(
        layout=layout,
        tmp_root=tmp_path / ".tmp",
        audits_by_task=audits_by_task,
        deterministic_by_task=deterministic_by_task,
        backend="codex",
        model="gpt-test",
        reasoning_effort="low",
        timeout=30,
        allow_downgrade=True,
        concurrency=1,
        task_ids_to_validate={second_task},
    )

    assert len(prompts) == 1
    assert first_task not in validation_by_task
    assert validation_by_task[second_task]["status"] == "pass"


def test_run_model_validators_marks_malformed_validator_json_untrusted(tmp_path, monkeypatch):
    eval_path = tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv"
    task_id = "tasks_mini/k-1-d-1/task_1.json"
    _write_csv(
        eval_path,
        ["task_id", "semantic_bucket", "semantic_match"],
        [{"task_id": task_id, "semantic_bucket": "semantic_incorrect", "semantic_match": "0"}],
    )
    layout = infer_layout(eval_path)

    def fake_call_model(prompt, **kwargs):
        return '{"task_id": "tasks_mini/k-1-d-1/task_1.json", "verdict": "pass" "problems": []}'

    monkeypatch.setattr("sana_analysis.answer_failure_audit_runner._call_model", fake_call_model)

    validation_by_task, repaired_audits = run_model_validators(
        layout=layout,
        tmp_root=tmp_path / ".tmp",
        audits_by_task={task_id: {"task_id": task_id, "answer_failure_summary": "summary", "events": [{"event_index": 1}]}},
        deterministic_by_task={task_id: {"status": "valid", "notes": ""}},
        backend="codex",
        model="gpt-test",
        reasoning_effort="low",
        timeout=30,
        allow_downgrade=True,
        concurrency=1,
    )

    assert validation_by_task[task_id]["status"] == "invalid_untrusted"
    assert "JSONDecodeError" in validation_by_task[task_id]["notes"]
    assert repaired_audits[task_id]["answer_failure_summary"] == "summary"


def test_combiner_uses_shared_answer_failure_figure_group_mapping():
    assert ANSWER_FAILURE_GROUPS is ANSWER_FAILURE_FIGURE_GROUPS
    assert ANSWER_FAILURE_GROUPS["wrong_source_or_dataset"] == "Wrong source target failures"
    assert ANSWER_FAILURE_GROUPS["wrong_scope_or_filter"] == "Execution/computation failures"
    assert ANSWER_FAILURE_GROUPS["computation_or_aggregation_error"] == "Execution/computation failures"
    assert ANSWER_FAILURE_GROUPS["query_execution_error_loop"] == "Turn-waste failures"


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
    out_path.write_text(
        json.dumps(
            {
                "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
                "task_id": cached_task,
                "answer_failure_summary": "cached",
                "events": [],
            }
        )
    )

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
    audit = {
        "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
        "task_id": cached_task,
        "answer_failure_summary": "cached",
        "events": [],
    }
    _append_journal_record(journal_path, layout=layout, task_id=cached_task, status="ok", audit=audit)

    stats = eval_pending_stats(source_eval, journal_path=journal_path)

    assert stats.pending_rows == 1
    assert stats.pending_task_ids == (missing_task,)


def test_eval_pending_stats_counts_invalid_rows_with_existing_temp_json_audits(tmp_path):
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
    out_path.write_text(
        json.dumps(
            {
                "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
                "task_id": cached_invalid,
                "answer_failure_summary": "cached",
                "events": [],
            }
        )
    )

    stats = eval_pending_stats(source_eval, tmp_root=tmp_root)

    assert stats.pending_rows == 0
    assert stats.invalid_rows == 2
    assert stats.invalid_task_ids == (cached_invalid, still_invalid)
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
    first_audit = {
        "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
        "task_id": task_id,
        "answer_failure_summary": "old",
        "events": [],
    }
    latest_audit = {
        "answer_failure_audit_schema_version": CURRENT_AUDIT_SCHEMA_VERSION,
        "task_id": task_id,
        "answer_failure_summary": "new",
        "events": [],
    }

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


def test_validation_warns_on_non_turn_anchored_evidence_for_existing_logs(tmp_path):
    log_path = tmp_path / "task.log"
    log_path.write_text("--- Turn 1 ---\nTool result: grounded evidence\n")
    row = {
        "task_id": "tasks_mini/k-1-d-1/task_1.json",
        "semantic_bucket": "semantic_incorrect",
        "semantic_match": "0",
    }
    events = [
        {
            "event_index": 1,
            "answer_failure_type": "wrong_source_or_dataset",
            "answer_failure_subtype": "wrong_dataset",
            "failure_stage": "source_selection",
            "failure_summary": "The source was wrong.",
            "failure_evidence": "trace did not include selected raw-log evidence",
            "confidence": "high",
        }
    ]

    result = validate_answer_failure_row(row, events, log_path)

    assert result["status"] == "valid_with_warnings"
    assert "failure_evidence must start with `Turn N |`" in result["notes"]


def test_validation_warns_on_exact_snippet_mismatch_for_existing_logs(tmp_path):
    log_path = tmp_path / "task.log"
    log_path.write_text("--- Turn 1 ---\nTool result: grounded evidence\n")
    row = {
        "task_id": "tasks_mini/k-1-d-1/task_1.json",
        "semantic_bucket": "semantic_incorrect",
        "semantic_match": "0",
    }
    events = [
        {
            "event_index": 1,
            "answer_failure_type": "wrong_source_or_dataset",
            "answer_failure_subtype": "wrong_dataset",
            "failure_stage": "source_selection",
            "failure_summary": "The source was wrong.",
            "failure_evidence": "Turn 1 | Tool result: paraphrased evidence",
            "confidence": "high",
        }
    ]

    result = validate_answer_failure_row(row, events, log_path)

    assert result["status"] == "valid_with_warnings"
    assert "exact evidence snippet for turn 1 does not match the raw log" in result["notes"]


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
    assert events[2]["answer_failure_type"] == "wrong_source_or_dataset"


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
                        "answer_failure_type": "wrong_source_or_dataset",
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
    assert rows[0]["answer_failure_types"] == "wrong_source_or_dataset"
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
            "answer_failure_type": "wrong_source_or_dataset",
            "answer_failure_subtype": "wrong_dataset",
            "failure_stage": "source_selection",
            "failure_summary": "The run queried the wrong source.",
            "failure_evidence": 'Turn 2 | Executing: query_file({"dataset_id": "wrong"})',
            "confidence": "high",
        }
    ]


def test_answer_failure_output_summary_reports_selected_file_counts(tmp_path):
    eval_path = tmp_path / "results_semantic_answer_failures" / "modes" / "model" / "mode" / "eval_results.csv"
    events_path = eval_path.parent / "answer_failure_events.csv"
    _write_csv(
        eval_path,
        [
            "task_id",
            "semantic_bucket",
            "semantic_match",
            "answer_failure_event_count",
            "answer_failure_validation_status",
            "answer_failure_model_validation_status",
        ],
        [
            {
                "task_id": "task_1",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "2",
                "answer_failure_validation_status": "valid",
                "answer_failure_model_validation_status": "pass",
            },
            {
                "task_id": "task_2",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "valid",
                "answer_failure_model_validation_status": "",
            },
            {
                "task_id": "task_3",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "invalid",
                "answer_failure_model_validation_status": "invalid_untrusted",
            },
            {
                "task_id": "task_4",
                "semantic_bucket": "semantic_correct",
                "semantic_match": "1",
                "answer_failure_event_count": "",
                "answer_failure_validation_status": "",
                "answer_failure_model_validation_status": "",
            },
        ],
    )
    _write_csv(
        events_path,
        [
            "task_id",
            "model_variant",
            "mode_variant",
            "event_index",
            "answer_failure_type",
            "answer_failure_subtype",
            "failure_stage",
            "failure_summary",
            "failure_evidence",
            "confidence",
        ],
        [
            {"task_id": "task_1", "event_index": "1", "answer_failure_type": "wrong_scope_or_filter"},
            {"task_id": "task_1", "event_index": "2", "answer_failure_type": "tool_or_data_blocker"},
            {"task_id": "task_2", "event_index": "1", "answer_failure_type": "wrong_source_or_dataset"},
            {"task_id": "task_3", "event_index": "1", "answer_failure_type": "extraction_or_parsing_error"},
        ],
    )

    summary = _answer_failure_output_summary(eval_path, events_path)

    assert summary == {
        "selected_eval_rows": 4,
        "selected_eligible_rows": 3,
        "selected_rows_with_events": 3,
        "selected_event_rows": 4,
        "selected_invalid_rows": 1,
        "selected_missing_log_rows": 0,
        "selected_valid_missing_model_validation_rows": 1,
        "selected_trusted_rows": 1,
        "selected_trusted_event_rows": 2,
    }
