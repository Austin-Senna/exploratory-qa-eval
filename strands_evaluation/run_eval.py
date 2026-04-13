#!/usr/bin/env python3
"""
Run evaluation across multiple models on benchmark tasks.

Usage:
    # Evaluate a single task directory
    python -m strands_evaluation.run_eval --task-dir tasks/k-3-d-2/

    # Evaluate a specific model by registry name
    python -m strands_evaluation.run_eval --task-dir tasks/k-3-d-2/ \
        --model-name bedrock/claude-sonnet-4.5

    # Evaluate all task directories
    python -m strands_evaluation.run_eval --all-tasks

    # Limit tasks per directory and increase parallelism
    python -m strands_evaluation.run_eval --all-tasks --tasks-per-dir 2 --parallel 4

    # condition B:
    python -m strands_evaluation.run_eval --task-dir tasks_mini/k-5-d-3 --tasks-per-dir 2 --parallel 2 --model-name bedrock/claude-haiku-4.5 --condition b

    # condition A:
    python -m strands_evaluation.run_eval --task-dir tasks_mini/k-5-d-3 --tasks-per-dir 2 --parallel 2 --model-name bedrock/claude-haiku-4.5 --condition a
"""

import argparse
import csv
import glob
import json
import logging
import os
from datetime import datetime
from typing import Optional

from strands_evaluation.agent import BatchRunner
from strands_evaluation.config import AgentConfig, ConditionConfig, RunConfig

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sanitize_model_name(model_id: str) -> str:
    return model_id.replace("/", "_").replace(":", "_")


def _display_name(agent_config) -> str:
    """Return a clean, human-readable slug for use in paths.

    Prefers model_name (e.g. 'bedrock/claude-haiku-4.5-arn') over raw model_id
    so ARN-based models don't produce garbage directory names. Appends
    reasoning_effort when set (e.g. 'openai_gpt-5.2-xhigh').
    """
    name = agent_config.model_name or agent_config.model_id
    slug = _sanitize_model_name(name)
    effort = (agent_config.extra_model_kwargs or {}).get("reasoning_effort")
    if effort:
        slug = f"{slug}-{effort}"
    return slug


def _results_root(run_config: RunConfig) -> str:
    return getattr(run_config, "results_output_dir", "results") or "results"


def find_all_task_dirs(base_dir: str = "tasks") -> list:
    """Return all task directories matching the k-*-d-* pattern."""
    return sorted(glob.glob(os.path.join(base_dir, "k-*-d-*")))


# ---------------------------------------------------------------------------
# Core evaluation loop
# ---------------------------------------------------------------------------

def run_evaluation(
    task_dir: str,
    agent_config: AgentConfig,
    run_config: RunConfig,
    verbose: bool = False,
    only_new: bool = False,
    parallel: int = 6,
    tasks_per_dir: Optional[int] = None,
) -> dict:
    """Run evaluation on a task directory and return {model_id -> {summary, results}}."""
    cond = run_config.condition_config
    condition_label = cond.condition
    safe_model = _display_name(agent_config)
    output_dir = os.path.join(_results_root(run_config), condition_label, safe_model)
    os.makedirs(output_dir, exist_ok=True)

    task_files = sorted(glob.glob(os.path.join(task_dir, "*.json")))
    if not task_files:
        logger.info(f"No task files found in {task_dir}")
        return {}

    if tasks_per_dir is not None:
        task_files = task_files[:tasks_per_dir]

    task_dir_name = os.path.basename(task_dir)
    model_id = agent_config.model_id

    logger.info(f"\nEvaluating {len(task_files)} tasks from {task_dir_name}")
    logger.info(f"Model: {model_id}  Condition: {condition_label}")
    logger.info("=" * 60)

    # Load task metadata for CSV annotation
    tasks_by_id: dict = {}
    for path in task_files:
        with open(path) as f:
            task = json.load(f)
            task["id"] = path
            tasks_by_id[path] = task

    csv_path = os.path.join(output_dir, "eval_results.csv")

    # --only-new: skip tasks already present in the CSV
    task_files_to_run = task_files
    if only_new and os.path.exists(csv_path):
        existing_ids: set = set()
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("task_id"):
                    existing_ids.add(row["task_id"])
        task_files_to_run = [p for p in task_files if p not in existing_ids]
        if not task_files_to_run:
            logger.info("  No new tasks to evaluate.")
            return {model_id: {"summary": _empty_summary(model_id, task_dir_name), "results": []}}

    try:
        batch = BatchRunner(agent_config=agent_config, run_config=run_config, max_workers=parallel)
        results = batch.run_from_files(task_files_to_run, verbose=verbose)
    except Exception as e:
        logger.error(f"  Error: {e}", exc_info=True)
        return {model_id: {"error": str(e)}}

    # Summary stats
    total = len(results)
    exact_matches = sum(r.get("exact_match", 0) for r in results)
    f1_scores = [r["f1_score"] for r in results if "f1_score" in r]
    avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
    avg_time = sum(r.get("time", 0) for r in results) / total if total else 0.0

    total_cost = sum(r.get("cost_usd", 0.0) for r in results)
    total_tool_calls = sum(r.get("tool_calls_total", 0) for r in results)

    summary = {
        "model": model_id,
        "task_dir": task_dir_name,
        "total_tasks": total,
        "exact_match_count": exact_matches,
        "exact_match_rate": exact_matches / total if total else 0.0,
        "avg_f1_score": avg_f1,
        "avg_time": avg_time,
        "total_cost_usd": total_cost,
        "avg_cost_usd": total_cost / total if total else 0.0,
        "avg_tool_calls": total_tool_calls / total if total else 0.0,
    }

    logger.info(f"  Exact Match: {exact_matches}/{total} ({100 * exact_matches / total:.1f}%)" if total else "  No results")
    logger.info(f"  Avg F1: {avg_f1:.3f}")

    # Write main CSV (upsert pattern — preserve existing rows)
    _write_main_csv(csv_path, results, tasks_by_id)

    # Write per-tool breakdown CSV
    tools_csv_path = os.path.join(output_dir, "tools_breakdown.csv")
    _write_tools_csv(tools_csv_path, results)

    # Write agent_results JSONL (one line per task)
    jsonl_path = os.path.join(output_dir, "agent_results.jsonl")
    _write_agent_results_jsonl(jsonl_path, results)

    return {model_id: {"summary": summary, "results": results}}


def _empty_summary(model_id: str, task_dir_name: str) -> dict:
    return {
        "model": model_id,
        "task_dir": task_dir_name,
        "total_tasks": 0,
        "exact_match_count": 0,
        "exact_match_rate": 0.0,
        "avg_f1_score": 0.0,
        "avg_time": 0.0,
        "total_cost_usd": 0.0,
        "avg_cost_usd": 0.0,
        "avg_tool_calls": 0.0,
    }


def _json_list_count(raw) -> int:
    if isinstance(raw, list):
        return len(raw)
    text = str(raw or "").strip()
    if not text:
        return 0
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return 0
    return len(payload) if isinstance(payload, list) else 0


def _normalize_main_csv_row(row: dict) -> dict:
    return {
        "task_id": row.get("task_id", ""),
        "model": row.get("model", ""),
        "expected_answer": row.get("expected_answer", ""),
        "predicted_answer": row.get("predicted_answer", ""),
        "exact_match": row.get("exact_match", ""),
        "f1_score": row.get("f1_score", ""),
        "required_dataset_count": row.get(
            "required_dataset_count",
            _json_list_count(row.get("required_datasets", "")),
        ),
        "sources_used_count": row.get(
            "sources_used_count",
            _json_list_count(row.get("sources_used", "")),
        ),
        "runtime_seconds": row.get("runtime_seconds", 0),
        "cycle_count": row.get("cycle_count", ""),
        "input_tokens": row.get("input_tokens", 0),
        "output_tokens": row.get("output_tokens", 0),
        "total_tokens": row.get("total_tokens", 0),
        "cost_usd": row.get("cost_usd", 0.0),
        "tool_calls_total": row.get("tool_calls_total", 0),
        "api_tool_calls": row.get("api_tool_calls", 0),
        "success": row.get("success", False),
        "error": row.get("error", ""),
    }


def _write_main_csv(csv_path: str, results: list, tasks_by_id: dict) -> None:
    fieldnames = [
        "task_id", "model",
        "expected_answer", "predicted_answer", "exact_match", "f1_score",
        "required_dataset_count", "sources_used_count",
        "runtime_seconds", "cycle_count",
        "input_tokens", "output_tokens", "total_tokens", "cost_usd",
        "tool_calls_total", "api_tool_calls",
        "success", "error",
    ]
    existing_rows: dict = {}
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("task_id"):
                    existing_rows[row["task_id"]] = _normalize_main_csv_row(row)

    for r in results:
        task_id = r.get("task_id", "")
        task = tasks_by_id.get(task_id, {})
        required = task.get("datasets_used", [])
        sources_used = r.get("sources_used", []) or []
        existing_rows[str(task_id)] = {
            "task_id": task_id,
            "model": r.get("model", ""),
            "expected_answer": task.get("answer", ""),
            "predicted_answer": r.get("predicted_answer", ""),
            "exact_match": r.get("exact_match", ""),
            "f1_score": r.get("f1_score", ""),
            "required_dataset_count": len({str(item) for item in required}),
            "sources_used_count": len({str(item) for item in sources_used}),
            "runtime_seconds": r.get("time", 0),
            "cycle_count": r.get("cycle_count", ""),
            "input_tokens": r.get("input_tokens", 0),
            "output_tokens": r.get("output_tokens", 0),
            "total_tokens": r.get("total_tokens", 0),
            "cost_usd": r.get("cost_usd", 0.0),
            "tool_calls_total": r.get("tool_calls_total", 0),
            "api_tool_calls": r.get("api_tool_calls", 0),
            "success": r.get("success", False),
            "error": r.get("error", ""),
        }

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task_id in sorted(existing_rows.keys()):
            writer.writerow(existing_rows[task_id])


def _write_tools_csv(tools_csv_path: str, results: list) -> None:
    fieldnames = ["task_id", "tool_name", "call_count", "success_count", "avg_time_seconds"]
    existing_rows: dict = {}
    if os.path.exists(tools_csv_path):
        with open(tools_csv_path, newline="") as f:
            for row in csv.DictReader(f):
                key = (row.get("task_id", ""), row.get("tool_name", ""))
                existing_rows[key] = row

    for r in results:
        task_id = str(r.get("task_id", ""))
        for tool in r.get("tool_counts", []):
            key = (task_id, tool["name"])
            existing_rows[key] = {
                "task_id": task_id,
                "tool_name": tool["name"],
                "call_count": tool["call_count"],
                "success_count": tool["success_count"],
                "avg_time_seconds": tool["average_time"],
            }

    with open(tools_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(existing_rows.keys()):
            writer.writerow(existing_rows[key])


def _write_agent_results_jsonl(jsonl_path: str, results: list) -> None:
    """Append agent results to a JSONL file (one object per task)."""
    with open(jsonl_path, "a") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")


# ---------------------------------------------------------------------------
# Comparison table
# ---------------------------------------------------------------------------

def print_comparison_table(results: dict) -> None:
    logger.info("\n" + "=" * 100)
    logger.info("MODEL COMPARISON")
    logger.info("=" * 100)
    logger.info(f"{'Model':<40} {'EM Rate':<10} {'Avg F1':<10} {'Avg Time':<12} {'Avg Cost':<12} {'Avg Tools':<10}")
    logger.info("-" * 100)
    for model_id, data in results.items():
        if "error" in data:
            logger.info(f"{model_id:<40} ERROR: {data['error'][:55]}")
        else:
            s = data["summary"]
            logger.info(
                f"{model_id:<40} {s['exact_match_rate']*100:>5.1f}%    "
                f"{s['avg_f1_score']:>6.3f}    {s['avg_time']:>8.1f}s    "
                f"${s['avg_cost_usd']:>7.4f}    {s['avg_tool_calls']:>6.1f}"
            )
    logger.info("=" * 100)


# ---------------------------------------------------------------------------
# Continue mode
# ---------------------------------------------------------------------------

def _run_continue(args, agent_config, run_config) -> None:
    """Re-run evaluation over task_set, skipping already-recorded tasks."""
    condition = run_config.condition_config.condition
    safe_model = _display_name(agent_config)
    results_dir = os.path.join(_results_root(run_config), condition, safe_model)
    csv_path = os.path.join(results_dir, "eval_results.csv")

    # Collect already-completed task_ids from the CSV
    completed_ids: set = set()
    if os.path.exists(csv_path):
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                tid = row.get("task_id", "").strip()
                if tid:
                    completed_ids.add(tid)

    # Find all task dirs and their pending task files
    all_task_dirs = find_all_task_dirs(args.task_set)
    pending: dict[str, list[str]] = {}  # task_dir -> [task_files not yet done]
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

    # Print summary of what will be evaluated
    total_pending = sum(len(v) for v in pending.values())
    print(f"\nCondition : {condition}")
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
        # Temporarily override task_files_to_run by passing only pending files.
        # We reuse run_evaluation with only_new=False and pass a sliced file list
        # via a thin wrapper that bypasses glob inside run_evaluation.
        _run_task_files(
            task_dir=task_dir,
            task_files=task_files,
            agent_config=agent_config,
            run_config=run_config,
            verbose=args.verbose,
            parallel=args.parallel,
        )


def _run_task_files(
    task_dir: str,
    task_files: list,
    agent_config,
    run_config,
    verbose: bool,
    parallel: int,
) -> None:
    """Run evaluation on an explicit list of task files (bypass glob in run_evaluation)."""
    cond = run_config.condition_config
    condition_label = cond.condition
    safe_model = _display_name(agent_config)
    output_dir = os.path.join(_results_root(run_config), condition_label, safe_model)
    os.makedirs(output_dir, exist_ok=True)

    task_dir_name = os.path.basename(task_dir)
    model_id = agent_config.model_id

    tasks_by_id: dict = {}
    for path in task_files:
        with open(path) as f:
            task = json.load(f)
            task["id"] = path
            tasks_by_id[path] = task

    logger.info(f"\nEvaluating {len(task_files)} tasks from {task_dir_name}")
    logger.info(f"Model: {model_id}  Condition: {condition_label}")
    logger.info("=" * 60)

    try:
        batch = BatchRunner(agent_config=agent_config, run_config=run_config, max_workers=parallel)
        results = batch.run_from_files(task_files, verbose=verbose)
    except Exception as e:
        logger.error(f"  Error: {e}", exc_info=True)
        return

    csv_path = os.path.join(output_dir, "eval_results.csv")
    _write_main_csv(csv_path, results, tasks_by_id)
    _write_tools_csv(os.path.join(output_dir, "tools_breakdown.csv"), results)
    _write_agent_results_jsonl(os.path.join(output_dir, "agent_results.jsonl"), results)

    total = len(results)
    exact_matches = sum(r.get("exact_match", 0) for r in results)
    logger.info(f"  Exact Match: {exact_matches}/{total} ({100*exact_matches/total:.1f}%)" if total else "  No results")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run evaluation on data lake benchmark tasks")

    # Task selection
    parser.add_argument("--task-dir", "-d", help="Single task directory to evaluate")
    parser.add_argument("--all-tasks", action="store_true", help="Evaluate all k-*-d-* directories")
    parser.add_argument("--task-set", default="tasks",
                        help="Base directory for --all-tasks (default: tasks)")
    parser.add_argument("--tasks-per-dir", type=int, default=None,
                        help="Limit number of tasks evaluated per directory")
    parser.add_argument("--task-continue", action="store_true",
                        help="Continue evaluation, skipping tasks already recorded in results. "
                             "Requires --condition, --model-name, and --task-set.")

    # Model — use a short name from MODEL_REGISTRY
    parser.add_argument("--model-name", default="bedrock/claude-sonnet-4.5",
                        help="Short model name from MODEL_REGISTRY e.g. bedrock/claude-sonnet-4.5 "
                             "or bedrock/claude-haiku-4.5-arn. Resolves provider/model-id automatically.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8096)
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        default=None,
        help="Optional reasoning effort for OpenAI chat models (passed as reasoning_effort).",
    )

    # RunConfig
    parser.add_argument("--max-tool-calls", type=int, default=30,
                        help="Max tool calls per task before agent is stopped")
    parser.add_argument("--sliding-window", type=int, default=40,
                        help="Conversation window size (last-k turns kept)")
    parser.add_argument("--timeout", type=int, default=450,
                        help="Per-task timeout in seconds")

    # Condition flags (ConditionConfig)
    parser.add_argument("--condition", choices=["baseline", "a", "b"], default="baseline",
                        help="Experiment condition: 'a' (tools-rich), 'b' (planning-rich), or 'baseline'")
    parser.add_argument("--sparse-backend", choices=["bm25", "splade"], default="bm25",
                        help="Sparse search backend for Condition A (default: bm25)")
    parser.add_argument("--results-output-dir", default="results",
                        help="Base directory for evaluation outputs (default: results)")
    parser.add_argument("--logs-output-dir", default="logs",
                        help="Base directory for per-task log files (default: logs)")

    # Execution
    parser.add_argument("--parallel", type=int, default=6,
                        help="Number of parallel worker processes")
    parser.add_argument("--only-new", action="store_true",
                        help="Skip tasks already present in the results CSV")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    extra_model_kwargs = {}
    if args.reasoning_effort is not None:
        extra_model_kwargs["reasoning_effort"] = args.reasoning_effort

    agent_config = AgentConfig(
        model_name=args.model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        extra_model_kwargs=extra_model_kwargs,
    )
    safe_model_name = _display_name(agent_config)
    condition_label = args.condition
    traces_root = os.path.join(args.results_output_dir, "traces")
    trace_dir = os.path.join(traces_root, condition_label, safe_model_name)

    run_config = RunConfig(
        results_output_dir=args.results_output_dir,
        logs_output_dir=args.logs_output_dir,
        max_tool_calls=args.max_tool_calls,
        sliding_window_k=args.sliding_window,
        timeout_seconds=args.timeout,
        condition_config=ConditionConfig(
            condition=condition_label,
            base_condition=args.condition,
            sparse_backend=args.sparse_backend,
            trace_output_dir=trace_dir,
        ),
    )

    start_time = datetime.now()

    if args.task_continue:
        _run_continue(args, agent_config, run_config)

    elif args.all_tasks:
        task_dirs = find_all_task_dirs(args.task_set)
        logger.info(f"Found {len(task_dirs)} task directories in '{args.task_set}'")
        for task_dir in task_dirs:
            results = run_evaluation(
                task_dir=task_dir,
                agent_config=agent_config,
                run_config=run_config,
                verbose=args.verbose,
                only_new=args.only_new,
                parallel=args.parallel,
                tasks_per_dir=args.tasks_per_dir,
            )
            print_comparison_table(results)

    elif args.task_dir:
        results = run_evaluation(
            task_dir=args.task_dir,
            agent_config=agent_config,
            run_config=run_config,
            verbose=args.verbose,
            only_new=args.only_new,
            parallel=args.parallel,
            tasks_per_dir=args.tasks_per_dir,
        )
        print_comparison_table(results)

    else:
        parser.print_help()

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"\nTotal evaluation time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
