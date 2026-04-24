import contextlib
import importlib.util
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


def _load_setup_run_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "strands_evaluation" / "setup_run.py"
    spec = importlib.util.spec_from_file_location("_test_setup_run_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


setup_run = _load_setup_run_module()


class _FakeRunner:
    def __init__(self) -> None:
        self.command = None
        self.kwargs = None

    def __call__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        return None


class SetupRunTests(unittest.TestCase):
    def _write_smoke_fixture(self, repo_root: Path) -> None:
        (repo_root / "lance_data").mkdir(parents=True, exist_ok=True)
        for task_dir in ("k-1-d-1", "k-5-d-4"):
            target = repo_root / "tasks_core_quality" / task_dir
            target.mkdir(parents=True, exist_ok=True)
            (target / "task_1.json").write_text("{}")
            (target / "task_2.json").write_text("{}")

    def test_smoke_builds_expected_command_and_normalizes_model_alias(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_smoke_fixture(repo_root)
            fake_runner = _FakeRunner()

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                command = setup_run.run(
                    [
                        "smoke",
                        "--search",
                        "ideal",
                        "--results",
                        "ideal",
                        "--plan",
                        "ideal",
                        "--k",
                        "5",
                        "--model",
                        "gpt5.2",
                        "--reasoning-effort",
                        "xhigh",
                        "--openai-prompt-cache-key",
                        "assistant-v3:tools-v1",
                        "--openai-prompt-cache-retention",
                        "24h",
                        "--verbose",
                        "--db",
                        "lance_data",
                    ],
                    runner=fake_runner,
                    cwd=repo_root,
                )

            self.assertEqual(command, fake_runner.command)
            self.assertEqual(command[1:3], ["-m", "strands_evaluation.run_mode_eval"])
            self.assertIn("--search_tool", command)
            self.assertIn("ideal", command)
            self.assertEqual(command[command.index("--model-name") + 1], "openai/gpt-5.2")
            self.assertEqual(command[command.index("--db-path") + 1], "lance_data")
            self.assertEqual(command[command.index("--task-dir") + 1], "tasks_core_quality/k-5-d-4")
            self.assertEqual(command[command.index("--tasks-per-dir") + 1], "2")
            self.assertEqual(command[command.index("--logs-output-dir") + 1], "test_logs")
            self.assertEqual(command[command.index("--results-output-dir") + 1], "test_results")
            self.assertEqual(command[command.index("--reasoning-effort") + 1], "xhigh")
            self.assertEqual(command[command.index("--openai-prompt-cache-key") + 1], "assistant-v3:tools-v1")
            self.assertEqual(command[command.index("--openai-prompt-cache-retention") + 1], "24h")
            self.assertIn("--verbose", command)
            self.assertEqual(fake_runner.kwargs, {"check": True, "cwd": str(repo_root)})
            self.assertIn("Task scope: tasks_core_quality/k-5-d-4 (first 2 tasks)", stdout.getvalue())

    def test_full_builds_expected_command(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "lance_data").mkdir(parents=True, exist_ok=True)
            fake_runner = _FakeRunner()

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                command = setup_run.run(
                    [
                        "full",
                        "--search",
                        "ideal",
                        "--results",
                        "ideal",
                        "--plan",
                        "ideal",
                        "--k",
                        "5",
                        "--model",
                        "openai/gpt-5.2",
                        "--db",
                        "lance_data",
                    ],
                    runner=fake_runner,
                    cwd=repo_root,
                )

            self.assertEqual(command[1:3], ["-m", "strands_evaluation.run_mode_eval"])
            self.assertIn("--all-tasks", command)
            self.assertEqual(command[command.index("--task-set") + 1], "tasks_core_quality")
            self.assertEqual(command[command.index("--logs-output-dir") + 1], "logs")
            self.assertEqual(command[command.index("--results-output-dir") + 1], "results")

    def test_full_continue_alias_and_timeout_passthrough(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            (repo_root / "lance_data").mkdir(parents=True, exist_ok=True)
            fake_runner = _FakeRunner()

            command = setup_run.run(
                [
                    "full",
                    "--continue",
                    "--search",
                    "ideal",
                    "--results",
                    "ideal",
                    "--plan",
                    "ideal",
                    "--model",
                    "openai/gpt-5.2",
                    "--timeout",
                    "600",
                    "--submit-grace-seconds",
                    "15",
                    "--db",
                    "lance_data",
                ],
                runner=fake_runner,
                cwd=repo_root,
            )

            self.assertIn("--task-continue", command)
            self.assertNotIn("--all-tasks", command)
            self.assertEqual(command[command.index("--timeout") + 1], "600")
            self.assertEqual(command[command.index("--submit-grace-seconds") + 1], "15")

    def test_smoke_normalizes_new_openai_model_alias(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_smoke_fixture(repo_root)
            fake_runner = _FakeRunner()

            command = setup_run.run(
                [
                    "smoke",
                    "--search",
                    "ideal",
                    "--results",
                    "ideal",
                    "--plan",
                    "ideal",
                    "--model",
                    "gpt-5.4-nano",
                    "--db",
                    "lance_data",
                ],
                runner=fake_runner,
                cwd=repo_root,
            )

            self.assertEqual(command[command.index("--model-name") + 1], "openai/gpt-5.4-nano")

    def test_smoke_normalizes_gpt_5_nano_alias(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_smoke_fixture(repo_root)
            fake_runner = _FakeRunner()

            command = setup_run.run(
                [
                    "smoke",
                    "--search",
                    "ideal",
                    "--results",
                    "ideal",
                    "--plan",
                    "ideal",
                    "--model",
                    "gpt-5-nano",
                    "--db",
                    "lance_data",
                ],
                runner=fake_runner,
                cwd=repo_root,
            )

            self.assertEqual(command[command.index("--model-name") + 1], "openai/gpt-5-nano")

    def test_smoke_accepts_preloaded_search_mode(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_smoke_fixture(repo_root)
            fake_runner = _FakeRunner()

            command = setup_run.run(
                [
                    "smoke",
                    "--search",
                    "preloaded",
                    "--results",
                    "naive",
                    "--plan",
                    "ideal",
                    "--model",
                    "bedrock/claude-haiku-4.5",
                    "--db",
                    "lance_data",
                ],
                runner=fake_runner,
                cwd=repo_root,
            )

            self.assertEqual(command, fake_runner.command)
            self.assertEqual(command[command.index("--search_tool") + 1], "preloaded")
            self.assertEqual(command[command.index("--agent_management") + 1], "ideal")

    def test_missing_db_has_helpful_error(self):
        with TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_smoke_fixture(repo_root)
            stderr = io.StringIO()

            with self.assertRaises(SystemExit) as captured, contextlib.redirect_stderr(stderr):
                setup_run.run(
                    [
                        "smoke",
                        "--search",
                        "ideal",
                        "--results",
                        "ideal",
                        "--plan",
                        "ideal",
                    ],
                    runner=_FakeRunner(),
                    cwd=repo_root,
                )

            self.assertEqual(captured.exception.code, 2)
            message = stderr.getvalue()
            self.assertIn("--db is required", message)
            self.assertIn("lance_data", message)


if __name__ == "__main__":
    unittest.main()
