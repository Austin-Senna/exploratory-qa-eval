import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory


def _load_setup_run_module():
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "sana_evaluation" / "setup_run.py"
    spec = importlib.util.spec_from_file_location("_test_sana_setup_run_module", module_path)
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


def _write_smoke_fixture(repo_root: Path) -> None:
    (repo_root / "lance_data").mkdir(parents=True, exist_ok=True)
    target = repo_root / "tasks_core_quality" / "k-5-d-4"
    target.mkdir(parents=True, exist_ok=True)
    (target / "task_1.json").write_text("{}")
    (target / "task_2.json").write_text("{}")


def test_sana_setup_uses_plan_axis_and_skills_toggle() -> None:
    with TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        _write_smoke_fixture(repo_root)
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
                "--skills",
                "on",
                "--db",
                "lance_data",
            ],
            runner=fake_runner,
            cwd=repo_root,
        )

    assert command == fake_runner.command
    assert command[command.index("--plan") + 1] == "ideal"
    assert command[command.index("--skills") + 1] == "on"
    assert "--agent_management" not in command


def test_sana_setup_defaults_skills_off_without_passing_flag() -> None:
    with TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        _write_smoke_fixture(repo_root)

        command = setup_run.run(
            [
                "smoke",
                "--search",
                "ideal",
                "--results",
                "ideal",
                "--plan",
                "standard",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert "--skills" not in command


def test_sana_setup_accepts_deprecated_agent_management_alias() -> None:
    with TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        _write_smoke_fixture(repo_root)

        command = setup_run.run(
            [
                "smoke",
                "--search",
                "ideal",
                "--results",
                "ideal",
                "--agent-management",
                "ideal",
                "--skills",
                "off",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert command[command.index("--plan") + 1] == "ideal"
    assert command[command.index("--skills") + 1] == "off"
