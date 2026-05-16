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
    target = repo_root / "tasks_mini" / "k-5-d-4"
    target.mkdir(parents=True, exist_ok=True)
    (target / "task_1.json").write_text("{}")
    (target / "task_2.json").write_text("{}")


def test_sana_setup_uses_plans_axis_and_skills_toggle() -> None:
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
                "--plans",
                "ideal",
                "--skills",
                "on",
                "--benchmark",
                "kramabench",
                "--db",
                "lance_data",
            ],
            runner=fake_runner,
            cwd=repo_root,
        )

    assert command == fake_runner.command
    assert command[command.index("--plans") + 1] == "ideal"
    assert command[command.index("--skills") + 1] == "on"
    assert command[command.index("--benchmark") + 1] == "kramabench"


def test_sana_setup_defaults_skills_off() -> None:
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
                "--plans",
                "standard",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert "--skills" not in command


def test_sana_setup_legacy_plan_alias_maps_to_plans_axis() -> None:
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
                "ideal",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert command[command.index("--plans") + 1] == "ideal"
    assert "--skills" not in command


def test_sana_setup_passes_explicit_skills_off() -> None:
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
                "--plans",
                "standard",
                "--skills",
                "off",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert command[command.index("--skills") + 1] == "off"


def test_sana_setup_passes_search_free_and_lessguide_aliases() -> None:
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
                "--plans",
                "standard",
                "--search-free",
                "--search_lessguide",
                "--db",
                "lance_data",
            ],
            runner=_FakeRunner(),
            cwd=repo_root,
        )

    assert "--search-free" in command
    assert "--search-lessguide" in command


def test_sana_setup_rejects_skills_on_with_naive_plans() -> None:
    with TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        _write_smoke_fixture(repo_root)

        try:
            setup_run.run(
                [
                    "smoke",
                    "--search",
                    "ideal",
                    "--results",
                    "ideal",
                    "--plans",
                    "naive",
                    "--skills",
                    "on",
                    "--db",
                    "lance_data",
                ],
                runner=_FakeRunner(),
                cwd=repo_root,
            )
        except SystemExit as exc:
            assert exc.code == 2
        else:
            raise AssertionError("Expected SystemExit for --skills on with --plans naive")
