import sys
from types import SimpleNamespace
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sana_analysis import answer_failure_audit_runner
from sana_analysis import trajectory_pair_analysis


def _assert_codex_prompt_is_sent_on_stdin(cmd, *, input=None, **kwargs):
    assert cmd[-1] == "-"
    assert input == "judge prompt with \0 embedded nul"
    assert all("\0" not in str(part) for part in cmd)
    return SimpleNamespace(returncode=0, stdout="fallback stdout")


def test_trajectory_pair_call_codex_sends_prompt_on_stdin(tmp_path, monkeypatch):
    monkeypatch.setattr(trajectory_pair_analysis.subprocess, "run", _assert_codex_prompt_is_sent_on_stdin)

    text = trajectory_pair_analysis.call_codex(
        "judge prompt with \0 embedded nul",
        repo_root=tmp_path,
        model="gpt-test",
        reasoning_effort="low",
        last_message_path=tmp_path / "last.txt",
        stdout_path=tmp_path / "stdout.log",
        timeout=30,
    )

    assert text == "fallback stdout"


def test_answer_failure_call_codex_sends_prompt_on_stdin(tmp_path, monkeypatch):
    monkeypatch.setattr(answer_failure_audit_runner.subprocess, "run", _assert_codex_prompt_is_sent_on_stdin)

    text = answer_failure_audit_runner._call_codex(
        "judge prompt with \0 embedded nul",
        cwd=tmp_path,
        model="gpt-test",
        reasoning_effort="low",
        last_message_path=tmp_path / "last.txt",
        stdout_path=tmp_path / "stdout.log",
        timeout=30,
    )

    assert text == "fallback stdout"
