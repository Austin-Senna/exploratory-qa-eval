#!/usr/bin/env python3
"""
Run search-ablation evaluation with explicit search controls.

This runner isolates experiment variants by writing outputs to:
  results/{condition_variant}/{model}/...
where condition_variant encodes:
  - k setting
  - search call budget setting
  - search description mode
"""

import argparse
import csv
import glob
import logging
import os
from datetime import datetime
from typing import Optional

from strands_evaluation import run_eval as base_eval
from strands_evaluation.config import AgentConfig, ConditionConfig, RunConfig

logger = logging.getLogger(__name__)


def _variant_condition_label(
    base_condition: str,
    *,
    k: Optional[int],
    search_calls: Optional[int],
    search_descriptions: str,
) -> str:
    parts = [search_descriptions]
    if k is not None:
        parts.append(f"k{k}")
    if search_calls is not None:
        parts.append(f"sc{search_calls}")
    _ = base_condition  # retained for stable call signature with existing call sites
    return "_".join(parts)


def _base_condition_label(base_condition: str) -> str:
    return base_condition


def _run_continue(args, agent_config, run_config) -> None:
    """Re-run over task_set, skipping tasks already recorded for this variant."""
    condition_label = run_config.condition_config.condition
    safe_model = base_eval._display_name(agent_config)
    results_dir = os.path.join(run_config.results_output_dir, condition_label, safe_model)
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
            task_files = task_files[:args.tasks_per_dir]
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
    parser = argparse.ArgumentParser(description="Run search-ablation evaluation on benchmark tasks")

    # Task selection
    parser.add_argument("--task-dir", "-d", help="Single task directory to evaluate")
    parser.add_argument("--all-tasks", action="store_true", help="Evaluate all k-*-d-* directories")
    parser.add_argument("--task-set", default="tasks", help="Base directory for --all-tasks (default: tasks)")
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
        help="Short model name from MODEL_REGISTRY e.g. bedrock/claude-sonnet-4.5",
    )
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8096)
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        default=None,
        help="Optional reasoning effort for OpenAI chat models (passed as reasoning_effort).",
    )

    # RunConfig core
    parser.add_argument("--max-tool-calls", type=int, default=30, help="Max tool calls per task")
    parser.add_argument("--sliding-window", type=int, default=40, help="Conversation last-k window")
    parser.add_argument("--timeout", type=int, default=450, help="Per-task timeout in seconds")

    # Base condition
    parser.add_argument(
        "--condition",
        choices=["baseline", "a", "b"],
        default="baseline",
        help="Base condition before variant suffixing: baseline | a | b",
    )
    parser.add_argument(
        "--sparse-backend",
        choices=["bm25", "splade"],
        default="bm25",
        help="Sparse backend for Condition A setup metadata",
    )
    parser.add_argument(
        "--results-output-dir",
        default="results",
        help="Base directory for evaluation outputs",
    )
    parser.add_argument(
        "--logs-output-dir",
        default="logs",
        help="Base directory for per-task log files",
    )
    parser.add_argument(
        "--db-path",
        default=None,
        help="Path to LanceDB search index directory (overrides default ./lance_data).",
    )

    # Search-ablation knobs
    parser.add_argument(
        "--k",
        type=int,
        default=None,
        help="Hard-coded search result limit. Removes user-configurable top_k/limit from search tool schemas.",
    )
    parser.add_argument(
        "--search-calls",
        type=int,
        default=None,
        help="Hard cap for total search calls. Search calls beyond this budget are blocked.",
    )
    parser.add_argument(
        "--search-descriptions",
        choices=["naive", "description"],
        default="naive",
        help="Result payload mode for search wrappers (default: naive).",
    )

    # Execution
    parser.add_argument("--parallel", type=int, default=6, help="Number of parallel worker processes")
    parser.add_argument("--only-new", action="store_true", help="Skip tasks already present in the results CSV")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    if args.k is not None and args.k <= 0:
        parser.error("--k must be > 0")
    if args.search_calls is not None and args.search_calls <= 0:
        parser.error("--search-calls must be > 0")

    variant_condition = _variant_condition_label(
        args.condition,
        k=args.k,
        search_calls=args.search_calls,
        search_descriptions=args.search_descriptions,
    )
    base_condition_label = _base_condition_label(args.condition)
    condition_label = f"{variant_condition}/{base_condition_label}"

    extra_model_kwargs = {}
    if args.reasoning_effort is not None:
        extra_model_kwargs["reasoning_effort"] = args.reasoning_effort

    agent_config = AgentConfig(
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        extra_model_kwargs=extra_model_kwargs,
    )
    safe_model_name = base_eval._display_name(agent_config)
    traces_root = os.path.join(args.results_output_dir, "traces")
    trace_dir = os.path.join(traces_root, condition_label, safe_model_name)

    run_config = RunConfig(
        results_output_dir=args.results_output_dir,
        logs_output_dir=args.logs_output_dir,
        max_tool_calls=args.max_tool_calls,
        sliding_window_k=args.sliding_window,
        timeout_seconds=args.timeout,
        search_k=args.k,
        search_calls_limit=args.search_calls,
        search_descriptions=args.search_descriptions,
        search_db_path=args.db_path,
        condition_config=ConditionConfig(
            condition=condition_label,
            base_condition=args.condition,
            sparse_backend=args.sparse_backend,
            trace_output_dir=trace_dir,
        ),
    )

    logger.info(
        "Search eval variant: %s (base=%s, k=%s, search_calls=%s, search_descriptions=%s, db_path=%s)",
        condition_label,
        args.condition,
        args.k,
        args.search_calls,
        args.search_descriptions,
        args.db_path or "./lance_data",
    )

    start_time = datetime.now()

    if args.task_continue:
        _run_continue(args, agent_config, run_config)
    elif args.all_tasks:
        task_dirs = base_eval.find_all_task_dirs(args.task_set)
        logger.info(f"Found {len(task_dirs)} task directories in '{args.task_set}'")
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
    logger.info(f"\nTotal evaluation time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
