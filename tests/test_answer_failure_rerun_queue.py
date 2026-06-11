import csv
import sys
from pathlib import Path

from analysis import answer_failure_rerun_queue as queue


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_candidate_counts_invalid_rows_even_without_events(tmp_path):
    source_eval = (
        tmp_path
        / "results_semantic"
        / "modes"
        / "model"
        / "mode"
        / "eval_results.csv"
    )
    answer_failure_eval = (
        tmp_path
        / "results_semantic_answer_failures"
        / "modes"
        / "model"
        / "mode"
        / "eval_results.csv"
    )
    fields = [
        "task_id",
        "semantic_bucket",
        "semantic_match",
        "answer_failure_event_count",
        "answer_failure_validation_status",
        "answer_failure_model_validation_status",
    ]
    _write_csv(source_eval, ["task_id", "semantic_bucket", "semantic_match"], [])
    _write_csv(
        answer_failure_eval,
        fields,
        [
            {
                "task_id": "invalid_blank_events",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "",
                "answer_failure_validation_status": "invalid",
                "answer_failure_model_validation_status": "",
            },
            {
                "task_id": "valid_blank_model_validation",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "valid",
                "answer_failure_model_validation_status": "",
            },
            {
                "task_id": "warnings_untrusted_model_validation",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "valid_with_warnings",
                "answer_failure_model_validation_status": "invalid_untrusted",
            },
            {
                "task_id": "missing_log",
                "semantic_bucket": "semantic_incorrect",
                "semantic_match": "0",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "missing_log",
                "answer_failure_model_validation_status": "",
            },
            {
                "task_id": "correct_row_ignored",
                "semantic_bucket": "semantic_correct",
                "semantic_match": "1",
                "answer_failure_event_count": "1",
                "answer_failure_validation_status": "invalid",
                "answer_failure_model_validation_status": "",
            },
        ],
    )

    candidate = queue.candidate_for_answer_failure_eval(
        answer_failure_eval,
        answer_failure_root=tmp_path / "results_semantic_answer_failures",
        source_root=tmp_path / "results_semantic",
    )

    assert candidate is not None
    assert candidate.hard_invalid_rows == 1
    assert candidate.missing_log_rows == 1
    assert candidate.stale_model_validator_rows == 2
    assert candidate.rows_with_events == 3


def test_command_for_candidate_uses_expected_repair_rounds(tmp_path):
    candidate = queue.EvalRerunCandidate(
        source_eval_path=tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv",
        answer_failure_eval_path=tmp_path
        / "results_semantic_answer_failures"
        / "modes"
        / "model"
        / "mode"
        / "eval_results.csv",
        hard_invalid_rows=2,
        missing_log_rows=0,
        stale_model_validator_rows=3,
        rows_with_events=5,
    )

    invalid_repair_command = queue.command_for_candidate(
        candidate,
        phase="invalid-repair",
        repair_invalid_rounds=2,
        concurrency=3,
    )
    stale_validator_command = queue.command_for_candidate(
        candidate,
        phase="stale-validator",
        repair_invalid_rounds=2,
        concurrency=3,
    )

    assert invalid_repair_command[-5:] == [
        "--repair-invalid-rounds",
        "2",
        "--concurrency",
        "3",
        "--model-validator-repaired-only",
    ]
    assert stale_validator_command[-5:] == [
        "--repair-invalid-rounds",
        "0",
        "--concurrency",
        "3",
        "--model-validator-stale-only",
    ]


def test_execute_all_rediscovers_between_phases(monkeypatch, tmp_path):
    calls: list[str] = []
    candidate = queue.EvalRerunCandidate(
        source_eval_path=tmp_path / "results_semantic" / "modes" / "model" / "mode" / "eval_results.csv",
        answer_failure_eval_path=tmp_path
        / "results_semantic_answer_failures"
        / "modes"
        / "model"
        / "mode"
        / "eval_results.csv",
        hard_invalid_rows=1,
        missing_log_rows=0,
        stale_model_validator_rows=1,
        rows_with_events=1,
    )

    def fake_discover_candidates(**kwargs):
        calls.append(f"discover:{kwargs['source_root'].name}:{kwargs['answer_failure_root'].name}")
        return [candidate]

    def fake_run_phase(candidates, *, phase, repair_invalid_rounds, concurrency):
        assert candidates == [candidate]
        assert repair_invalid_rounds == 2
        assert concurrency == 4
        calls.append(f"run:{phase}:concurrency={concurrency}")

    def fake_refresh_validation(answer_failure_root, logs_dir):
        calls.append(f"refresh:{answer_failure_root.name}:{logs_dir.name}")
        return {"audited_rows": 10, "invalid_rows": []}

    monkeypatch.setattr(queue, "discover_candidates", fake_discover_candidates)
    monkeypatch.setattr(queue, "run_phase", fake_run_phase)
    monkeypatch.setattr(queue, "refresh_validation", fake_refresh_validation)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "answer_failure_rerun_queue",
            "--source-root",
            str(tmp_path / "results_semantic"),
            "--answer-failure-root",
            str(tmp_path / "results_semantic_answer_failures"),
            "--phase",
            "all",
            "--repair-invalid-rounds",
            "2",
            "--concurrency",
            "4",
            "--execute",
        ],
    )

    queue.main()

    assert calls == [
        "refresh:results_semantic_answer_failures:modes",
        "discover:results_semantic:results_semantic_answer_failures",
        "run:invalid-repair:concurrency=4",
        "refresh:results_semantic_answer_failures:modes",
        "discover:results_semantic:results_semantic_answer_failures",
        "run:stale-validator:concurrency=4",
    ]
