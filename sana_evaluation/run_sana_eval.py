#!/usr/bin/env python3
"""Run SANA-enabled multi-axis ablation evaluation.

Mirrors strands_evaluation.run_mode_eval but uses SanaBatchRunner and adds
SANA feature flags. Baseline axes (search_tool, search_results, agent_management)
behave identically to run_mode_eval.
"""

from __future__ import annotations

import argparse
import csv
import glob
import logging
import os
from datetime import datetime
from typing import List, Optional

from strands_evaluation import run_eval as base_eval
from strands_evaluation.config import AgentConfig, ConditionConfig
from strands_evaluation.helper.prompting import normalize_debug_mode
from strands_evaluation.preflight import PreflightError, run_preflight

from sana_evaluation.flags import SanaFlags
from sana_evaluation.sana_config import SanaRunConfig
from sana_evaluation.sana_runner import SanaBatchRunner

logger = logging.getLogger(__name__)

# Reuse run_eval orchestration while swapping the runner implementation.
base_eval.BatchRunner = SanaBatchRunner

_MODE_LETTERS = {
    "naive": "n",
    "preloaded": "p",
    "standard": "d",
    "ideal": "i",
}

_AXIS_DEFAULTS = {
    "search_tool": "preloaded",
    "search_results": "ideal",
    "agent_management": "standard",
}

_SANA_FEATURE_LETTERS = {
    "short_plan": "sp",
    "CoT": "cot",
    "results_apis": "ra",
    "confidence_advisory": "ca",
    "dashboard": "db",
}


def _variant_condition_label(
    *,
    search_tool: str,
    search_results: str,
    agent_management: str,
    k: Optional[int],
    search_calls: Optional[int],
    sana_flags: SanaFlags,
) -> str:
    parts = [
        f"search_{_MODE_LETTERS[search_tool]}",
        f"results_{_MODE_LETTERS[search_results]}",
        f"plan{_MODE_LETTERS[agent_management]}",
    ]
    if k is not None:
        parts.append(f"k{k}")
    if search_calls is not None:
        parts.append(f"sc{search_calls}")
    sana_letters = [
        _SANA_FEATURE_LETTERS[name]
        for name in ("short_plan", "CoT", "results_apis", "confidence_advisory", "dashboard")
        if getattr(sana_flags, name)
    ]
    if sana_letters:
        parts.append("sana_" + "_".join(sana_letters))
        if sana_flags.short_plan:
            parts.append(f"mrk{sana_flags.macro_reflection_k}")
    return "_".join(parts)


def _with_debug_suffix(label: str, debug_mode: Optional[str]) -> str:
    normalized = normalize_debug_mode(debug_mode)
    if normalized is None:
        return label
    return f"{label}__debug_{normalized}"


def _resolve_mode_axes(
    *,
    search_tool: Optional[str],
    search_results: Optional[str],
    agent_management: Optional[str],
) -> tuple[str, str, str]:
    return (
        search_tool or _AXIS_DEFAULTS["search_tool"],
        search_results or _AXIS_DEFAULTS["search_results"],
        agent_management or _AXIS_DEFAULTS["agent_management"],
    )


def _collect_task_files(args) -> list[str]:
    if args.task_continue or args.all_tasks:
        task_dirs = base_eval.find_all_task_dirs(args.task_set)
        out: list[str] = []
        for d in task_dirs:
            files = sorted(glob.glob(os.path.join(d, "*.json")))
            if args.tasks_per_dir is not None:
                files = files[: args.tasks_per_dir]
            out.extend(files)
        return out
    if args.task_dir:
        files = sorted(glob.glob(os.path.join(args.task_dir, "*.json")))
        if args.tasks_per_dir is not None:
            files = files[: args.tasks_per_dir]
        return files
    return []


def _run_continue(args, agent_config: AgentConfig, run_config: SanaRunConfig) -> None:
    condition_label = run_config.condition_config.condition
    safe_model = base_eval._display_name(agent_config)
    results_dir = base_eval._results_dir(run_config, agent_config)
    csv_path = os.path.join(results_dir, "eval_results.csv")

    completed_ids: set = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                tid = row.get("task_id", "").strip()
                if tid:
                    completed_ids.add(tid)

    all_task_dirs = base_eval.find_all_task_dirs(args.task_set)
    pending: dict[str, list[str]] = {}
    for task_dir in all_task_dirs:
        task_files = sorted(glob.glob(os.path.join(task_dir, "*.json")))
        if args.tasks_per_dir is not None:
            task_files = task_files[: args.tasks_per_dir]
        remaining = [p for p in task_files if p not in completed_ids]
        if remaining:
            pending[task_dir] = remaining

    if not pending:
        print("Nothing to do — all tasks already recorded.")
        return

    total_pending = sum(len(v) for v in pending.values())
    print(f"\nCondition : {condition_label}")
    print(f"Model     : {safe_model}")
    print(f"Task set  : {args.task_set}")
    print(f"Results   : {results_dir}")
    print(f"Completed : {len(completed_ids)} tasks already recorded")
    print(f"\nDirectories to evaluate ({len(pending)} dirs, {total_pending} tasks remaining):")
    for task_dir, files in sorted(pending.items()):
        print(f"  {task_dir:<40}  {len(files)} task(s)")

    print()
    answer = input("Proceed? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        return

    print()
    for task_dir, task_files in sorted(pending.items()):
        base_eval._run_task_files(
            task_dir=task_dir,
            task_files=task_files,
            agent_config=agent_config,
            run_config=run_config,
            verbose=args.verbose,
            parallel=args.parallel,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run SANA-enabled multi-axis ablation evaluation on benchmark tasks",
    )

    # Task selection
    parser.add_argument("--task-dir", "-d", help="Single task directory to evaluate")
    parser.add_argument("--all-tasks", action="store_true", help="Evaluate all k-*-d-* directories")
    parser.add_argument(
        "--task-set",
        default="tasks_core_quality",
        help="Base directory for --all-tasks (default: tasks_core_quality)",
    )
    parser.add_argument("--tasks-per-dir", type=int, default=None, help="Limit tasks per directory")
    parser.add_argument(
        "--task-continue",
        action="store_true",
        help="Continue evaluation, skipping tasks already recorded in results for this variant.",
    )

    # Model
    parser.add_argument(
        "--model-name",
        default="bedrock/claude-sonnet-4.5",
        help="Short model name from MODEL_REGISTRY",
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8096)
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        default=None,
    )
    parser.add_argument("--openai-prompt-cache-key", default=None)
    parser.add_argument("--openai-prompt-cache-retention", default=None)
    parser.add_argument(
        "--debug-mode",
        choices=["none", "decision_notes"],
        default="none",
    )
    parser.add_argument("--decision-notes", action="store_true")

    # RunConfig core
    parser.add_argument("--max-tool-calls", type=int, default=30)
    parser.add_argument("--sliding-window", type=int, default=40)
    parser.add_argument(
        "--conversation-manager-strategy",
        choices=["summarizing", "sliding_window"],
        default="summarizing",
    )
    parser.add_argument("--summary-ratio", type=float, default=0.4)
    parser.add_argument("--preserve-recent-messages", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--submit-grace-seconds", type=int, default=30)
    parser.add_argument("--submit-only-max-tokens", type=int, default=2048)

    # Base condition + storage
    parser.add_argument(
        "--condition",
        choices=["baseline", "a", "b"],
        default="baseline",
    )
    parser.add_argument(
        "--sparse-backend",
        choices=["bm25", "splade"],
        default="bm25",
    )
    parser.add_argument("--results-output-dir", default="results")
    parser.add_argument("--logs-output-dir", default="logs")
    parser.add_argument("--db-path", default=None)

    # Search controls
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--search-calls", type=int, default=None)
    parser.add_argument(
        "--search-descriptions",
        choices=["naive", "description"],
        default="naive",
    )

    # Ablation axes (existing baseline)
    parser.add_argument(
        "--search_tool",
        choices=["naive", "preloaded", "standard", "ideal"],
        default=None,
    )
    parser.add_argument(
        "--search_results",
        choices=["naive", "ideal"],
        default=None,
    )
    parser.add_argument(
        "--agent_management",
        choices=["naive", "standard", "ideal"],
        default=None,
    )

    # SANA feature flags
    parser.add_argument(
        "--sana-feature",
        action="append",
        default=[],
        choices=sorted({"short_plan", "CoT", "results_apis", "confidence_advisory", "dashboard"}),
        help=(
            "Enable a SANA feature. Repeat for multiple features. "
            "Options: short_plan, CoT, results_apis, confidence_advisory, dashboard."
        ),
    )
    parser.add_argument(
        "--macro-reflection-k",
        type=int,
        default=5,
        help="Tool-call cadence for macro-reflection when short_plan is on (default: 5).",
    )

    # Execution
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--only-new", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    if args.decision_notes:
        args.debug_mode = "decision_notes"

    if args.k is not None and args.k <= 0:
        parser.error("--k must be > 0")
    if args.search_calls is not None and args.search_calls <= 0:
        parser.error("--search-calls must be > 0")
    if args.macro_reflection_k <= 0:
        parser.error("--macro-reflection-k must be > 0")

    extra_model_kwargs = {}
    if args.reasoning_effort is not None:
        extra_model_kwargs["reasoning_effort"] = args.reasoning_effort

    agent_config = AgentConfig(
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        openai_prompt_cache_key=args.openai_prompt_cache_key,
        openai_prompt_cache_retention=args.openai_prompt_cache_retention,
        extra_model_kwargs=extra_model_kwargs,
    )
    search_tool_mode, search_results_mode, agent_management_mode = _resolve_mode_axes(
        search_tool=args.search_tool,
        search_results=args.search_results,
        agent_management=args.agent_management,
    )

    try:
        sana_flags = SanaFlags.from_feature_names(
            args.sana_feature,
            macro_reflection_k=args.macro_reflection_k,
        )
        sana_flags.validate(agent_management=agent_management_mode)
    except ValueError as exc:
        parser.error(str(exc))

    safe_model_name = base_eval._display_name(agent_config)
    variant_condition = _variant_condition_label(
        search_tool=search_tool_mode,
        search_results=search_results_mode,
        agent_management=agent_management_mode,
        k=args.k,
        search_calls=args.search_calls,
        sana_flags=sana_flags,
    )
    variant_condition = _with_debug_suffix(variant_condition, args.debug_mode)
    condition_label = f"sana/{safe_model_name}/{variant_condition}"
    base_eval._maybe_autoset_openai_cache_key(agent_config, condition_label)
    traces_root = os.path.join(args.results_output_dir, "traces")
    trace_dir = os.path.join(traces_root, condition_label)

    run_config = SanaRunConfig(
        results_output_dir=args.results_output_dir,
        logs_output_dir=args.logs_output_dir,
        debug_mode=normalize_debug_mode(args.debug_mode),
        max_tool_calls=args.max_tool_calls,
        conversation_manager_strategy=args.conversation_manager_strategy,
        sliding_window_k=args.sliding_window,
        summary_ratio=args.summary_ratio,
        preserve_recent_messages=args.preserve_recent_messages,
        timeout_seconds=args.timeout,
        submit_grace_seconds=args.submit_grace_seconds,
        submit_only_max_tokens=args.submit_only_max_tokens,
        search_k=args.k,
        search_calls_limit=args.search_calls,
        search_descriptions=args.search_descriptions,
        search_db_path=args.db_path,
        search_tool_mode=search_tool_mode,
        search_results_mode=search_results_mode,
        agent_management_mode=agent_management_mode,
        sana_flags=sana_flags,
        condition_config=ConditionConfig(
            condition=condition_label,
            base_condition=args.condition,
            sparse_backend=args.sparse_backend,
            trace_output_dir=trace_dir,
        ),
    )

    logger.info(
        "SANA variant: %s (sana_features=%s mrk=%d)",
        condition_label,
        sana_flags.active_features() or ["none"],
        sana_flags.macro_reflection_k,
    )

    task_files = _collect_task_files(args)
    try:
        run_preflight(run_config, task_files)
    except PreflightError as exc:
        parser.exit(2, f"{exc}\n")

    start_time = datetime.now()

    if args.task_continue:
        _run_continue(args, agent_config, run_config)
    elif args.all_tasks:
        task_dirs = base_eval.find_all_task_dirs(args.task_set)
        logger.info("Found %d task directories in '%s'", len(task_dirs), args.task_set)
        for task_dir in task_dirs:
            results = base_eval.run_evaluation(
                task_dir=task_dir,
                agent_config=agent_config,
                run_config=run_config,
                verbose=args.verbose,
                only_new=args.only_new,
                parallel=args.parallel,
                tasks_per_dir=args.tasks_per_dir,
            )
            base_eval.print_comparison_table(results)
    elif args.task_dir:
        results = base_eval.run_evaluation(
            task_dir=args.task_dir,
            agent_config=agent_config,
            run_config=run_config,
            verbose=args.verbose,
            only_new=args.only_new,
            parallel=args.parallel,
            tasks_per_dir=args.tasks_per_dir,
        )
        base_eval.print_comparison_table(results)
    else:
        parser.print_help()

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info("\nTotal evaluation time: %.1fs", elapsed)


if __name__ == "__main__":
    main()
