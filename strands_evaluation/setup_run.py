#!/usr/bin/env python3
"""Friendly preset wrapper around ``run_mode_eval``."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional, Sequence

_SEARCH_MODE_CHOICES = ("naive", "preloaded", "standard", "ideal")
_MANAGEMENT_MODE_CHOICES = ("naive", "standard", "ideal")
_RESULT_MODE_CHOICES = ("naive", "ideal")
_REASONING_EFFORT_CHOICES = ("none", "minimal", "low", "medium", "high", "xhigh")
_DEFAULT_TASK_SET = "tasks_core_quality"
_DEFAULT_SMOKE_TASK_DIR = "k-5-d-4"
_DEFAULT_SMOKE_TASK_LIMIT = 2
_MODEL_ALIASES = {
    "gpt5.2": "openai/gpt-5.2",
    "gpt-5.2": "openai/gpt-5.2",
}
_DB_HINTS = ("lance_data",)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Friendly presets for strands_evaluation.run_mode_eval",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--search", choices=_SEARCH_MODE_CHOICES, default="standard")
    common.add_argument("--results", choices=_RESULT_MODE_CHOICES, default="naive")
    common.add_argument("--plan", choices=_MANAGEMENT_MODE_CHOICES, default="standard")
    common.add_argument("--k", type=int, default=None)
    common.add_argument("--model", default="bedrock/claude-sonnet-4.5")
    common.add_argument(
        "--reasoning-effort",
        choices=_REASONING_EFFORT_CHOICES,
        default=None,
    )
    common.add_argument("--openai-prompt-cache-key", default=None)
    common.add_argument("--openai-prompt-cache-retention", default=None)
    common.add_argument("--db", default=None, help="Lance DB root, required on every run.")
    common.add_argument(
        "--condition",
        choices=("baseline", "b"),
        default="baseline",
    )
    common.add_argument("--parallel", type=int, default=None)
    common.add_argument("--verbose", "-v", action="store_true")

    smoke = subparsers.add_parser("smoke", parents=[common], help="Run a lightweight smoke eval.")
    smoke.add_argument(
        "--task-dir",
        default=None,
        help="Optional task directory override inside the default task set.",
    )

    full = subparsers.add_parser("full", parents=[common], help="Run the full default task-set eval.")
    full.add_argument(
        "--task-continue",
        action="store_true",
        help="Resume: skip tasks already recorded in this variant's CSV.",
    )
    return parser


def _known_db_choices(cwd: Path) -> list[str]:
    return [name for name in _DB_HINTS if (cwd / name).exists()]


def _missing_db_error(cwd: Path) -> str:
    choices = _known_db_choices(cwd)
    if choices:
        return (
            "--db is required. Choose one of: "
            + ", ".join(choices)
            + ", or provide a custom path."
        )
    return (
        "--db is required. Use a Lance DB root such as lance_data, "
        "or provide a custom path."
    )


def _normalize_model_name(raw: str) -> str:
    model = (raw or "").strip()
    if not model:
        raise ValueError("--model cannot be empty.")

    alias = _MODEL_ALIASES.get(model.lower())
    if alias:
        return alias
    if "/" in model:
        return model
    raise ValueError(
        f"Unknown model shorthand '{model}'. Use a canonical model name like "
        f"'openai/gpt-5.2' or one of: {', '.join(sorted(_MODEL_ALIASES))}."
    )


def _validate_db_arg(db_arg: Optional[str], cwd: Path) -> str:
    if not db_arg:
        raise ValueError(_missing_db_error(cwd))

    db_path = Path(db_arg).expanduser()
    if not db_path.is_absolute():
        db_path = cwd / db_path
    if not db_path.exists():
        raise ValueError(f"--db path not found: {db_arg}")
    return _display_path(db_path, cwd)


def _display_path(path: Path, cwd: Path) -> str:
    try:
        return str(path.relative_to(cwd))
    except ValueError:
        return str(path)


def _resolve_smoke_task_dir(task_dir_arg: Optional[str], cwd: Path) -> Path:
    if task_dir_arg:
        candidate = Path(task_dir_arg).expanduser()
        if not candidate.is_absolute():
            candidate = cwd / candidate
        if not candidate.is_dir():
            raise ValueError(f"--task-dir does not exist: {task_dir_arg}")
        return candidate

    candidate = cwd / _DEFAULT_TASK_SET / _DEFAULT_SMOKE_TASK_DIR
    if not candidate.is_dir():
        raise ValueError(
            f"Default smoke task dir {_DEFAULT_TASK_SET}/{_DEFAULT_SMOKE_TASK_DIR} "
            "not found. Pass --task-dir explicitly."
        )
    return candidate


def _display_command(command: Sequence[str]) -> str:
    if not command:
        return ""
    printable = list(command)
    if Path(printable[0]) == Path(sys.executable):
        printable[0] = "python"
    return shlex.join(printable)


def _build_run_mode_command(args: argparse.Namespace, cwd: Path) -> tuple[list[str], dict[str, str]]:
    model_name = _normalize_model_name(args.model)
    db_arg = _validate_db_arg(args.db, cwd)

    command = [
        sys.executable,
        "-m",
        "strands_evaluation.run_mode_eval",
        "--search_tool",
        args.search,
        "--search_results",
        args.results,
        "--agent_management",
        args.plan,
        "--model-name",
        model_name,
        "--condition",
        args.condition,
        "--db-path",
        db_arg,
    ]

    if args.k is not None:
        command.extend(["--k", str(args.k)])
    if args.reasoning_effort is not None:
        command.extend(["--reasoning-effort", args.reasoning_effort])
    if args.openai_prompt_cache_key is not None:
        command.extend(["--openai-prompt-cache-key", args.openai_prompt_cache_key])
    if args.openai_prompt_cache_retention is not None:
        command.extend(["--openai-prompt-cache-retention", args.openai_prompt_cache_retention])
    if args.parallel is not None:
        command.extend(["--parallel", str(args.parallel)])
    if args.verbose:
        command.append("--verbose")

    if args.subcommand == "smoke":
        task_dir = _resolve_smoke_task_dir(args.task_dir, cwd)
        task_dir_display = _display_path(task_dir, cwd)
        command.extend(
            [
                "--task-dir",
                task_dir_display,
                "--tasks-per-dir",
                str(_DEFAULT_SMOKE_TASK_LIMIT),
                "--logs-output-dir",
                "test_logs",
                "--results-output-dir",
                "test_results",
            ]
        )
        metadata = {
            "db_path": db_arg,
            "task_scope": f"{task_dir_display} (first {_DEFAULT_SMOKE_TASK_LIMIT} tasks)",
            "logs_output_dir": "test_logs",
            "results_output_dir": "test_results",
        }
        return command, metadata

    task_continue = bool(getattr(args, "task_continue", False))
    if task_continue:
        command.extend(
            [
                "--task-continue",
                "--task-set",
                _DEFAULT_TASK_SET,
                "--logs-output-dir",
                "logs",
                "--results-output-dir",
                "results",
            ]
        )
        scope = f"resume pending tasks under {_DEFAULT_TASK_SET}"
    else:
        command.extend(
            [
                "--all-tasks",
                "--task-set",
                _DEFAULT_TASK_SET,
                "--logs-output-dir",
                "logs",
                "--results-output-dir",
                "results",
            ]
        )
        scope = f"all tasks under {_DEFAULT_TASK_SET}"
    metadata = {
        "db_path": db_arg,
        "task_scope": scope,
        "logs_output_dir": "logs",
        "results_output_dir": "results",
    }
    return command, metadata


def run(
    argv: Optional[Sequence[str]] = None,
    *,
    runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
    cwd: Optional[Path] = None,
) -> list[str]:
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo_root = Path.cwd() if cwd is None else Path(cwd)

    if args.k is not None and args.k <= 0:
        parser.error("--k must be > 0")
    if args.parallel is not None and args.parallel <= 0:
        parser.error("--parallel must be > 0")

    try:
        command, metadata = _build_run_mode_command(args, repo_root)
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Resolved command: {_display_command(command)}")
    print(f"Lance DB: {metadata['db_path']}")
    print(f"Task scope: {metadata['task_scope']}")
    print(f"Logs root: {metadata['logs_output_dir']}")
    print(f"Results root: {metadata['results_output_dir']}")

    runner(command, check=True, cwd=str(repo_root))
    return command


def main(argv: Optional[Sequence[str]] = None) -> int:
    run(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
