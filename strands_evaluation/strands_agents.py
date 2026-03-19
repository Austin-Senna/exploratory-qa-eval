#!/usr/bin/env python3
"""
Run Strands Evals SDK evaluation on data lake benchmark tasks.

This runner complements EM/F1 metrics with evaluator-based scoring:
- OutputEvaluator
- TrajectoryEvaluator
- FaithfulnessEvaluator
- ToolSelectionAccuracyEvaluator
- ToolParameterAccuracyEvaluator
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from strands_evals import Case, Experiment
from strands_evals.evaluators import (
    FaithfulnessEvaluator,
    GoalSuccessRateEvaluator,
    HelpfulnessEvaluator,
    OutputEvaluator,
    ToolParameterAccuracyEvaluator,
    ToolSelectionAccuracyEvaluator,
    TrajectoryEvaluator,
)
from strands_evals.extractors import tools_use_extractor
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry import StrandsEvalsTelemetry
from strands_evals.types.trace import Session

from strands_evaluation.agent import DataLakeAgent
from strands_evaluation.config import AgentConfig, RunConfig
from strands_evaluation.helper.logger import configure_logging

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT_RUBRIC = (
    "Score 1.0 when the answer is correct, complete, and in the requested response format. "
    "Score 0.5 when partially correct or incomplete. "
    "Score 0.0 when incorrect, missing key information, or format is violated."
)

DEFAULT_TRAJECTORY_RUBRIC = (
    "Score 1.0 when the tool usage trajectory is efficient, logically ordered, and avoids unnecessary calls. "
    "Score 0.5 when mostly reasonable but with avoidable detours. "
    "Score 0.0 when the trajectory is incoherent, wasteful, or fails to support the final answer."
)


@dataclass
class CaseExecution:
    output: str
    session: Session
    tool_trajectory: list[dict[str, Any]]
    success: bool
    error: str = ""


def _sanitize_name(value: str) -> str:
    return value.replace("/", "_").replace(":", "_")


def find_all_task_dirs(base_dir: str = "tasks") -> list[str]:
    return sorted(glob.glob(os.path.join(base_dir, "k-*-d-*")))


def _build_cases(task_files: list[str]) -> list[Case[str, str]]:
    cases: list[Case[str, str]] = []
    for task_file in task_files:
        with open(task_file) as f:
            task = json.load(f)

        question = task.get("question")
        if not question:
            raise ValueError(f"Task file '{task_file}' does not contain a 'question' field.")

        case = Case[str, str](
            name=os.path.basename(task_file),
            input=question,
            expected_output=task.get("answer"),
            metadata={
                "task_id": task_file,
                "datasets_used": task.get("datasets_used", []),
            },
        )
        cases.append(case)
    return cases


def _build_evaluator_suites(
    judge_model: str | None,
    output_rubric: str,
    trajectory_rubric: str,
    include_helpfulness: bool,
    include_goal_success: bool,
) -> tuple[list[Any], list[Any], list[Any]]:
    output_evaluators: list[Any] = [
        OutputEvaluator(rubric=output_rubric, model=judge_model, include_inputs=True),
    ]

    trajectory_evaluators: list[Any] = [
        TrajectoryEvaluator(rubric=trajectory_rubric, model=judge_model, include_inputs=True),
    ]

    trace_evaluators: list[Any] = [
        FaithfulnessEvaluator(model=judge_model),
        ToolSelectionAccuracyEvaluator(model=judge_model),
        ToolParameterAccuracyEvaluator(model=judge_model),
    ]
    if include_helpfulness:
        trace_evaluators.append(HelpfulnessEvaluator(model=judge_model))
    if include_goal_success:
        trace_evaluators.append(GoalSuccessRateEvaluator(model=judge_model))

    return output_evaluators, trajectory_evaluators, trace_evaluators


def _summarize_report(report: Any) -> dict[str, Any]:
    num_cases = len(report.scores)
    pass_rate = (
        sum(1 for x in report.test_passes if x) / len(report.test_passes)
        if report.test_passes
        else 0.0
    )
    return {
        "overall_score": report.overall_score,
        "pass_rate": pass_rate,
        "num_cases": num_cases,
    }


def _write_summary_csv(summary_csv_path: Path, evaluator_summary: dict[str, dict[str, Any]]) -> None:
    summary_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["evaluator", "overall_score", "pass_rate", "num_cases"])
        writer.writeheader()
        for evaluator_name in sorted(evaluator_summary):
            row = {"evaluator": evaluator_name, **evaluator_summary[evaluator_name]}
            writer.writerow(row)


def run_evaluation(
    task_dir: str,
    agent_config: AgentConfig,
    run_config: RunConfig,
    output_dir: str = "results",
    include_helpfulness: bool = False,
    include_goal_success: bool = False,
    judge_model: str | None = None,
    output_rubric: str = DEFAULT_OUTPUT_RUBRIC,
    trajectory_rubric: str = DEFAULT_TRAJECTORY_RUBRIC,
    tasks_per_dir: Optional[int] = None,
) -> dict[str, Any]:
    task_files = sorted(glob.glob(os.path.join(task_dir, "*.json")))
    if not task_files:
        logger.info(f"No task files found in {task_dir}")
        return {}

    if tasks_per_dir is not None:
        task_files = task_files[:tasks_per_dir]

    task_dir_name = os.path.basename(task_dir)
    model_id = agent_config.model_id
    safe_model_name = _sanitize_name(model_id)

    logger.info(f"Running Strands Evals on {len(task_files)} tasks from {task_dir_name}")
    logger.info(f"Agent model: {model_id}")

    cases = _build_cases(task_files)
    data_lake_agent = DataLakeAgent(agent_config=agent_config, run_config=run_config)

    telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
    memory_exporter = telemetry.in_memory_exporter
    mapper = StrandsInMemorySessionMapper()
    case_cache: dict[str, CaseExecution] = {}

    def _run_case_once(case: Case[str, str]) -> CaseExecution:
        cached = case_cache.get(case.session_id)
        if cached is not None:
            return cached

        memory_exporter.clear()
        try:
            result = data_lake_agent.run(str(case.input), session_id=case.session_id)
            spans = list(memory_exporter.get_finished_spans())
            session = mapper.map_to_session(spans, session_id=case.session_id)
            tool_trajectory = tools_use_extractor.extract_agent_tools_used(session)
            execution = CaseExecution(
                output=result.answer,
                session=session,
                tool_trajectory=tool_trajectory,
                success=result.success,
                error=result.error or "",
            )
        except Exception as e:
            logger.error(f"Task execution failed for case '{case.name}': {type(e).__name__}: {e}", exc_info=True)
            empty_session = mapper.map_to_session([], session_id=case.session_id)
            execution = CaseExecution(
                output="",
                session=empty_session,
                tool_trajectory=[],
                success=False,
                error=f"{type(e).__name__}: {e}",
            )
        finally:
            memory_exporter.clear()

        case_cache[case.session_id] = execution
        return execution

    def _task_output(case: Case[str, str]) -> str:
        execution = _run_case_once(case)
        return execution.output

    def _task_trace(case: Case[str, str]) -> dict[str, Any]:
        execution = _run_case_once(case)
        return {"output": execution.output, "trajectory": execution.session}

    def _task_trajectory(case: Case[str, str]) -> dict[str, Any]:
        execution = _run_case_once(case)
        return {"output": execution.output, "trajectory": execution.tool_trajectory}

    output_evaluators, trajectory_evaluators, trace_evaluators = _build_evaluator_suites(
        judge_model=judge_model,
        output_rubric=output_rubric,
        trajectory_rubric=trajectory_rubric,
        include_helpfulness=include_helpfulness,
        include_goal_success=include_goal_success,
    )

    all_reports: dict[str, Any] = {}

    output_experiment = Experiment[str, str](cases=cases, evaluators=output_evaluators)
    output_reports = output_experiment.run_evaluations(_task_output)
    for evaluator, report in zip(output_evaluators, output_reports):
        all_reports[evaluator.__class__.__name__] = report

    trajectory_experiment = Experiment[str, str](cases=cases, evaluators=trajectory_evaluators)
    trajectory_reports = trajectory_experiment.run_evaluations(_task_trajectory)
    for evaluator, report in zip(trajectory_evaluators, trajectory_reports):
        all_reports[evaluator.__class__.__name__] = report

    trace_experiment = Experiment[str, str](cases=cases, evaluators=trace_evaluators)
    trace_reports = trace_experiment.run_evaluations(_task_trace)
    for evaluator, report in zip(trace_evaluators, trace_reports):
        all_reports[evaluator.__class__.__name__] = report

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_dir = Path(output_dir) / "strands_evals" / safe_model_name / task_dir_name / timestamp
    artifact_dir.mkdir(parents=True, exist_ok=True)

    evaluator_summary: dict[str, dict[str, Any]] = {}
    report_paths: dict[str, str] = {}
    for evaluator_name, report in all_reports.items():
        report_path = artifact_dir / f"{evaluator_name}.json"
        report.to_file(str(report_path))
        report_paths[evaluator_name] = str(report_path)
        evaluator_summary[evaluator_name] = _summarize_report(report)

    summary = {
        "model": model_id,
        "task_dir": task_dir_name,
        "num_tasks": len(cases),
        "judge_model": judge_model,
        "evaluator_summary": evaluator_summary,
        "report_paths": report_paths,
    }

    with open(artifact_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    _write_summary_csv(artifact_dir / "summary.csv", evaluator_summary)

    logger.info(f"Saved evaluation artifacts to: {artifact_dir}")
    return {model_id: {"summary": summary, "artifact_dir": str(artifact_dir)}}


def print_comparison_table(results: dict[str, Any]) -> None:
    logger.info("\n" + "=" * 90)
    logger.info("STRANDS EVALS SUMMARY")
    logger.info("=" * 90)
    logger.info(f"{'Model':<40} {'Tasks':<8} {'Avg Overall Score':<18} {'Artifact Dir'}")
    logger.info("-" * 90)
    for model_id, data in results.items():
        summary = data.get("summary", {})
        evaluator_summary = summary.get("evaluator_summary", {})
        scores = [v.get("overall_score", 0.0) for v in evaluator_summary.values()]
        avg_overall = sum(scores) / len(scores) if scores else 0.0
        logger.info(
            f"{model_id:<40} {summary.get('num_tasks', 0):<8} {avg_overall:<18.4f} {data.get('artifact_dir', '')}"
        )
    logger.info("=" * 90)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Strands Evals SDK evaluation on benchmark tasks")

    parser.add_argument("--task-dir", "-d", help="Single task directory to evaluate")
    parser.add_argument("--all-tasks", action="store_true", help="Evaluate all k-*-d-* directories")
    parser.add_argument("--task-set", default="tasks", help="Base directory for --all-tasks")
    parser.add_argument("--tasks-per-dir", type=int, default=None, help="Limit tasks evaluated per directory")
    parser.add_argument("--output-dir", default="results", help="Output root for report artifacts")

    parser.add_argument("--model-name", default=None, help="Short model key from MODEL_REGISTRY")
    parser.add_argument("--provider", default="bedrock", help="LLM provider")
    parser.add_argument("--model-id", default="us.anthropic.claude-sonnet-4-5-20250929-v1:0", help="Model ID")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8096)

    parser.add_argument("--max-tool-calls", type=int, default=30)
    parser.add_argument("--sliding-window", type=int, default=40)
    parser.add_argument("--timeout", type=int, default=450)
    parser.add_argument("--judge-model", default=None, help="Optional evaluator judge model-id")
    parser.add_argument("--output-rubric", default=DEFAULT_OUTPUT_RUBRIC)
    parser.add_argument("--trajectory-rubric", default=DEFAULT_TRAJECTORY_RUBRIC)
    parser.add_argument("--include-helpfulness", action="store_true")
    parser.add_argument("--include-goal-success", action="store_true")

    args = parser.parse_args()

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    configure_logging(run_id=run_id)

    agent_config = AgentConfig(
        model_name=args.model_name,
        provider=args.provider,
        model_id=args.model_id,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    run_config = RunConfig(
        max_tool_calls=args.max_tool_calls,
        sliding_window_k=args.sliding_window,
        timeout_seconds=args.timeout,
    )

    judge_model = args.judge_model or agent_config.model_id

    all_results: dict[str, Any] = {}
    if args.all_tasks:
        task_dirs = find_all_task_dirs(args.task_set)
        logger.info(f"Found {len(task_dirs)} task directories in '{args.task_set}'")
        for task_dir in task_dirs:
            result = run_evaluation(
                task_dir=task_dir,
                agent_config=agent_config,
                run_config=run_config,
                output_dir=args.output_dir,
                include_helpfulness=args.include_helpfulness,
                include_goal_success=args.include_goal_success,
                judge_model=judge_model,
                output_rubric=args.output_rubric,
                trajectory_rubric=args.trajectory_rubric,
                tasks_per_dir=args.tasks_per_dir,
            )
            print_comparison_table(result)
        return
    elif args.task_dir:
        result = run_evaluation(
            task_dir=args.task_dir,
            agent_config=agent_config,
            run_config=run_config,
            output_dir=args.output_dir,
            include_helpfulness=args.include_helpfulness,
            include_goal_success=args.include_goal_success,
            judge_model=judge_model,
            output_rubric=args.output_rubric,
            trajectory_rubric=args.trajectory_rubric,
            tasks_per_dir=args.tasks_per_dir,
        )
        all_results.update(result)
    else:
        parser.print_help()
        return

    print_comparison_table(all_results)


if __name__ == "__main__":
    main()
