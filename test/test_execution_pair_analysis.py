from pathlib import Path

from analysis.execution_pair_analysis import (
    IDEAL_MODE,
    PAIR_MODES,
    build_pair_rows,
    extract_execution_excerpt,
    judge_pending_rows,
    load_tmp_audits,
    merge_existing_audits,
    summarize_rows,
    validate_judge_payload,
)


def _write_log(path: Path, *, runner: str = "gpt-test", ideal_compute: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    query_tool = "query_ideal" if ideal_compute else "query_file"
    lines = [
        "2026 | INFO | x | NEW TASK: " + runner,
        "2026 | INFO | x | --- Turn 1 ---",
        '2026 | INFO | x | Executing: plan_ideal({"plan_text": "do work"})',
        "2026 | DEBUG | x | Tool result: Plan recorded.",
        '2026 | INFO | x | Executing: search_ideal({"query": "dataset"})',
        '2026 | DEBUG | x | Tool result: {"results": [{"dataset_id": "ds"}]}',
        f'2026 | INFO | x | Executing: {query_tool}({{"dataset_id": "ds", "query": "select avg(x) from t"}})',
        '2026 | DEBUG | x | Tool result: {"rows": [{"avg": 4}]}',
        '2026 | INFO | x | Executing: submit_answer({"answer": "4"})',
        "2026 | INFO | x | ANSWER: 4 (1.2s)",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_extract_execution_excerpt_keeps_execution_not_search_or_plan(tmp_path: Path) -> None:
    log_path = tmp_path / "task.log"
    _write_log(log_path)

    events = extract_execution_excerpt(log_path, start_after_line=3)

    joined = "\n".join(events)
    assert "plan_ideal" not in joined
    assert "search_ideal" not in joined
    assert "query_file" in joined
    assert "submit_answer" in joined


def test_build_pair_rows_creates_iid_vs_iii_rows(tmp_path: Path) -> None:
    root = tmp_path / "logs"
    task_rel = Path("tasks_mini/k-1-d-1/task_1.log")
    model = "openai_gpt-test"
    _write_log(root / "modes" / model / PAIR_MODES["iid_vs_iii"] / task_rel)
    _write_log(root / "modes" / model / IDEAL_MODE / task_rel, ideal_compute=True)

    rows = build_pair_rows(benchmark="lakeqa", log_root=root)

    assert len(rows) == 1
    assert rows[0]["pair_label"] == "iid_vs_iii"
    assert rows[0]["comparison_mode"] == PAIR_MODES["iid_vs_iii"]
    assert rows[0]["ideal_mode"] == IDEAL_MODE
    assert rows[0]["audit_status"] == "pending"
    assert rows[0]["comparison_event_count"] != "0"
    assert rows[0]["ideal_event_count"] != "0"


def test_build_pair_rows_marks_missing_ideal_not_comparable(tmp_path: Path) -> None:
    root = tmp_path / "logs"
    task_rel = Path("tasks_mini/k-1-d-1/task_1.log")
    model = "openai_gpt-test"
    _write_log(root / "modes" / model / PAIR_MODES["iid_vs_iii"] / task_rel)

    rows = build_pair_rows(benchmark="lakeqa", log_root=root)

    assert len(rows) == 1
    assert rows[0]["execution_similarity"] == "not_comparable"
    assert rows[0]["execution_error_type"] == "ideal_log_missing"
    assert rows[0]["audit_status"] == "complete"


def test_summarize_rows_counts_execution_correct_and_pending() -> None:
    rows = [
        {
            "benchmark": "lakeqa",
            "model_variant": "openai_gpt-test",
            "pair_label": "iid_vs_iii",
            "execution_similarity": "executes_correctly",
            "audit_status": "complete",
        },
        {
            "benchmark": "lakeqa",
            "model_variant": "openai_gpt-test",
            "pair_label": "iid_vs_iii",
            "execution_similarity": "wrong_filter",
            "audit_status": "complete",
        },
        {
            "benchmark": "lakeqa",
            "model_variant": "openai_gpt-test",
            "pair_label": "iid_vs_iii",
            "execution_similarity": "",
            "audit_status": "pending",
        },
    ]

    summary, breakdown = summarize_rows(rows)

    assert summary[0]["n_total"] == 3
    assert summary[0]["n_execution_correct"] == 1
    assert summary[0]["execution_correct_fraction_all"] == "1/3"
    assert summary[0]["execution_correct_pct_all"] == 33.3
    assert summary[0]["n_pending_label"] == 1
    assert {row["execution_similarity"] for row in breakdown} == {
        "executes_correctly",
        "wrong_filter",
        "pending",
    }


def test_tmp_json_audits_are_loaded_by_full_pair_key(tmp_path: Path) -> None:
    rows = [
        {
            "benchmark": "lakeqa",
            "pair_label": "iid_vs_iii",
            "model_variant": "openai_gpt-test",
            "task_id": "tasks_mini/k/task.json",
            "execution_similarity": "",
            "execution_error_type": "",
            "comparison_execution_summary": "",
            "ideal_execution_summary": "",
            "aligned_operations": "",
            "divergent_operations": "",
            "similarity_reason": "",
            "evidence": "",
            "auditor_model": "",
            "audit_status": "pending",
        }
    ]
    audit_path = tmp_path / "tmp" / "lakeqa" / "openai_gpt-test" / "iid_vs_iii" / "row.json"
    audit_path.parent.mkdir(parents=True)
    audit_path.write_text(
        """{
          "row_key": {
            "benchmark": "lakeqa",
            "pair_label": "iid_vs_iii",
            "model_variant": "openai_gpt-test",
            "task_id": "tasks_mini/k/task.json"
          },
          "row_update": {
            "execution_similarity": "minor_execution_drift",
            "execution_error_type": "none",
            "comparison_execution_summary": "comparison",
            "ideal_execution_summary": "ideal",
            "aligned_operations": "same",
            "divergent_operations": "",
            "similarity_reason": "reason",
            "evidence": "evidence",
            "auditor_model": "gpt-5.4-mini",
            "audit_status": "complete"
          }
        }""",
        encoding="utf-8",
    )

    merge_existing_audits(rows, load_tmp_audits(tmp_path / "tmp"))

    assert rows[0]["execution_similarity"] == "minor_execution_drift"


def test_validate_judge_payload_requires_known_label_and_required_fields() -> None:
    assert validate_judge_payload(
        {
            "execution_similarity": "executes_correctly",
            "execution_error_type": "none",
            "comparison_execution_summary": "comparison",
            "ideal_execution_summary": "ideal",
            "aligned_operations": "",
            "divergent_operations": "",
            "similarity_reason": "reason",
            "evidence": "evidence",
            "audit_status": "complete",
        }
    ) == []
    errors = validate_judge_payload({"execution_similarity": "correct", "audit_status": "done"})
    assert any("execution_similarity" in error for error in errors)
    assert any("audit_status" in error for error in errors)


def test_judge_pending_rows_retries_invalid_json_until_valid(tmp_path: Path, monkeypatch) -> None:
    comparison_log = tmp_path / "comparison.log"
    ideal_log = tmp_path / "ideal.log"
    _write_log(comparison_log)
    _write_log(ideal_log, ideal_compute=True)
    row = {
        "benchmark": "lakeqa",
        "pair_label": "iid_vs_iii",
        "model_variant": "openai_gpt-test",
        "runner_model": "gpt-test",
        "task_id": "tasks_mini/k/task.json",
        "comparison_mode": PAIR_MODES["iid_vs_iii"],
        "ideal_mode": IDEAL_MODE,
        "comparison_log": str(comparison_log),
        "ideal_log": str(ideal_log),
        "comparison_start_line": "3",
        "ideal_start_line": "3",
        "comparison_event_count": "1",
        "ideal_event_count": "1",
        "execution_similarity": "",
        "execution_error_type": "",
        "comparison_execution_summary": "",
        "ideal_execution_summary": "",
        "aligned_operations": "",
        "divergent_operations": "",
        "similarity_reason": "",
        "evidence": "",
        "auditor_model": "",
        "audit_status": "pending",
    }
    responses = iter(
        [
            '{"execution_similarity": "correct", "audit_status": "done"}',
            """{
              "execution_similarity": "wrong_filter",
              "execution_error_type": "filter_binding",
              "comparison_execution_summary": "comparison",
              "ideal_execution_summary": "ideal",
              "aligned_operations": "query",
              "divergent_operations": "filter",
              "similarity_reason": "valid after repair",
              "evidence": "lines",
              "audit_status": "complete"
            }""",
        ]
    )

    monkeypatch.setattr("analysis.execution_pair_analysis.call_judge_model", lambda *_args, **_kwargs: next(responses))

    judged = judge_pending_rows(
        [row],
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
    assert row["execution_similarity"] == "wrong_filter"
    assert len(list((tmp_path / "tmp").rglob("*.attempt1.last_message.txt"))) == 1
    assert len(list((tmp_path / "tmp").rglob("*.attempt2.last_message.txt"))) == 1
    assert '"status": "retry"' in (tmp_path / "journal.jsonl").read_text()
