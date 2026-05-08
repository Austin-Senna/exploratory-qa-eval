"""Tests for the SANA setup_run wrapper delegation options."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from sana_evaluation import setup_run


class _FakeRunner:
    def __init__(self) -> None:
        self.command = None
        self.kwargs = None

    def __call__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        return None


def _write_smoke_fixture(repo_root: Path) -> None:
    (repo_root / "lance_data").mkdir(parents=True, exist_ok=True)
    task_dir = repo_root / "tasks_core_quality" / "k-5-d-4"
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "task_1.json").write_text("{}")


def test_smoke_passes_delegation_feature_and_budget_caps() -> None:
    with TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        _write_smoke_fixture(repo_root)
        fake_runner = _FakeRunner()

        command = setup_run.run(
            [
                "smoke",
                "--sana-feature",
                "delegation",
                "--sana-feature",
                "results",
                "--max-search-subagent-calls",
                "4",
                "--max-inspect-subagent-calls",
                "9",
                "--model",
                "gpt-5.4-nano",
                "--db",
                "lance_data",
            ],
            runner=fake_runner,
            cwd=repo_root,
        )

        assert command == fake_runner.command
        assert command[1:3] == ["-m", "sana_evaluation.run_sana_eval"]
        assert command.count("--sana-feature") == 2
        assert "delegation" in command
        assert "results" in command
        assert command[command.index("--max-search-subagent-calls") + 1] == "4"
        assert command[command.index("--max-inspect-subagent-calls") + 1] == "9"
