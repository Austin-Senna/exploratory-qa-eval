#!/usr/bin/env python3
"""Summarize recorded runtime across LakeQA and Kramabench runs.

The source of truth is each run's ``eval_results.csv`` ``runtime_seconds``
column. The script treats every CSV row as one task run and sums those recorded
durations; this is total agent runtime, not wall-clock elapsed time for a batch
that may have run tasks in parallel.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class RuntimeRow:
    benchmark: str
    model: str
    mode: str
    task_id: str
    runtime_seconds: float
    logged_total_cost_usd: float
    total_cost_usd: float
    cost_source: str
    source_path: str


@dataclass(frozen=True)
class RuntimeComputation:
    rows: list[RuntimeRow]
    by_model_mode: dict[tuple[str, str, str], dict[str, Any]]
    by_mode: dict[tuple[str, str], dict[str, Any]]
    by_benchmark: dict[str, dict[str, Any]]
    overall: dict[str, Any]


def _read_eval_rows(path: Path) -> list[dict[str, str]]:
    text = path.read_text(errors="replace").replace("\x00", "")
    return list(csv.DictReader(io.StringIO(text)))


def _parse_eval_path(path: Path, modes_root: Path) -> tuple[str, str]:
    rel = path.relative_to(modes_root)
    parts = rel.parts
    if len(parts) != 3 or parts[-1] != "eval_results.csv":
        raise ValueError(f"Expected <model>/<mode>/eval_results.csv under {modes_root}, got {path}")
    return parts[0], parts[1]


def _runtime_seconds(value: object, *, path: Path, row_number: int) -> float:
    if value in (None, ""):
        raise ValueError(f"Missing runtime_seconds in {path} row {row_number}")
    try:
        runtime = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid runtime_seconds={value!r} in {path} row {row_number}") from exc
    if runtime < 0:
        raise ValueError(f"Negative runtime_seconds={runtime!r} in {path} row {row_number}")
    return runtime


def _load_model_pricing() -> Mapping[str, Mapping[str, float]]:
    constants_path = Path(__file__).resolve().parent.parent / "strands_evaluation" / "helper" / "constants.py"
    spec = importlib.util.spec_from_file_location("_runtime_summary_constants", constants_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load pricing constants from {constants_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MODEL_PRICING


MODEL_PRICING = _load_model_pricing()


def _as_float(value: object) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _pricing_for_model(model_name: str) -> Mapping[str, float]:
    candidates = [model_name]
    if model_name.startswith("openai_"):
        candidates.append(model_name.replace("openai_", "openai/", 1))
        candidates.append(model_name.replace("openai_", "", 1))
    if "/" in model_name:
        candidates.append(model_name.split("/", 1)[1].strip())
    for candidate in candidates:
        pricing = MODEL_PRICING.get(candidate)
        if pricing:
            return pricing
    raise KeyError(f"No pricing configured for model {model_name!r}")


def _full_input_cost(model_name: str, *, input_tokens: float, output_tokens: float) -> float:
    pricing = _pricing_for_model(model_name)
    return (
        float(pricing["input"]) * input_tokens / 1_000_000.0
        + float(pricing["output"]) * output_tokens / 1_000_000.0
    )


def _logged_total_cost_usd(row: Mapping[str, str]) -> float:
    for field in (
        "total_cost_with_all_subagents_usd",
        "total_cost_with_ideal_subagents_usd",
        "cost_usd",
    ):
        value = row.get(field)
        if value not in (None, ""):
            if field == "cost_usd":
                return (
                    _as_float(row.get("cost_usd"))
                    + _as_float(row.get("ideal_subagent_cost_usd"))
                    + _as_float(row.get("delegation_subagent_cost_usd"))
                )
            return _as_float(value)
    return 0.0


def _trace_path_for_task(trace_root: Path, model: str, mode: str, task_id: str) -> Path:
    task_path = Path(task_id)
    if len(task_path.parts) < 2:
        raise ValueError(f"Cannot infer trace path from task_id={task_id!r}")
    return trace_root / model / mode / task_path.parent.name / f"{task_path.stem}.jsonl"


def _iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _uncached_ideal_cost_from_trace(path: Path) -> tuple[float, int]:
    total = 0.0
    event_count = 0
    for event in _iter_jsonl(path):
        if event.get("event") != "ideal_subagent_cost":
            continue
        total += _full_input_cost(
            str(event.get("model_name") or ""),
            input_tokens=_as_float(event.get("input_tokens")),
            output_tokens=_as_float(event.get("output_tokens")),
        )
        event_count += 1
    return total, event_count


def _uncached_total_cost_usd(
    row: Mapping[str, str],
    *,
    model: str,
    mode: str,
    trace_root: Path | None,
) -> tuple[float, str]:
    main_cost = _full_input_cost(
        model,
        input_tokens=_as_float(row.get("input_tokens")),
        output_tokens=_as_float(row.get("output_tokens")),
    )
    ideal_cost_source = "aggregate"
    ideal_cost = 0.0
    if trace_root is not None:
        trace_path = _trace_path_for_task(trace_root, model, mode, str(row.get("task_id") or ""))
        if trace_path.exists():
            ideal_cost, event_count = _uncached_ideal_cost_from_trace(trace_path)
            if event_count:
                ideal_cost_source = "trace"
    if ideal_cost_source == "aggregate":
        ideal_cost = _full_input_cost(
            model,
            input_tokens=_as_float(row.get("ideal_subagent_input_tokens")),
            output_tokens=_as_float(row.get("ideal_subagent_output_tokens")),
        )
    delegation_cost = _full_input_cost(
        model,
        input_tokens=_as_float(row.get("delegation_subagent_input_tokens")),
        output_tokens=_as_float(row.get("delegation_subagent_output_tokens")),
    )
    return main_cost + ideal_cost + delegation_cost, f"uncached-{ideal_cost_source}"


def _summarize(rows: list[RuntimeRow]) -> dict[str, Any]:
    runtimes = [row.runtime_seconds for row in rows]
    costs = [row.total_cost_usd for row in rows]
    logged_costs = [row.logged_total_cost_usd for row in rows]
    total_seconds = sum(runtimes)
    total_cost_usd = sum(costs)
    logged_total_cost_usd = sum(logged_costs)
    tasks = len(runtimes)
    return {
        "tasks": tasks,
        "total_seconds": total_seconds,
        "total_minutes": total_seconds / 60.0,
        "total_hours": total_seconds / 3600.0,
        "total_cost_usd": total_cost_usd,
        "logged_total_cost_usd": logged_total_cost_usd,
        "cost_delta_usd": total_cost_usd - logged_total_cost_usd,
        "cost_multiplier": total_cost_usd / logged_total_cost_usd if logged_total_cost_usd else 0.0,
        "avg_seconds": total_seconds / tasks if tasks else 0.0,
        "avg_cost_usd": total_cost_usd / tasks if tasks else 0.0,
        "avg_logged_cost_usd": logged_total_cost_usd / tasks if tasks else 0.0,
        "min_seconds": min(runtimes) if runtimes else 0.0,
        "max_seconds": max(runtimes) if runtimes else 0.0,
    }


def _group_by(rows: list[RuntimeRow], key_parts: tuple[str, ...]) -> dict[tuple[str, ...], dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[RuntimeRow]] = defaultdict(list)
    for row in rows:
        key = tuple(str(getattr(row, part)) for part in key_parts)
        grouped[key].append(row)
    return {key: _summarize(group_rows) for key, group_rows in sorted(grouped.items())}


def compute_runtime_summary(
    benchmark_roots: Mapping[str, Path | str],
    trace_roots: Mapping[str, Path | str] | None = None,
) -> RuntimeComputation:
    rows: list[RuntimeRow] = []
    trace_roots = trace_roots or {}

    for benchmark, raw_root in sorted(benchmark_roots.items()):
        modes_root = Path(raw_root)
        if not modes_root.exists():
            raise FileNotFoundError(f"Missing modes root for {benchmark}: {modes_root}")
        trace_root = Path(trace_roots[benchmark]) if benchmark in trace_roots else None

        for csv_path in sorted(modes_root.rglob("eval_results.csv")):
            model, mode = _parse_eval_path(csv_path, modes_root)
            for row_number, eval_row in enumerate(_read_eval_rows(csv_path), start=2):
                total_cost, cost_source = _uncached_total_cost_usd(
                    eval_row,
                    model=model,
                    mode=mode,
                    trace_root=trace_root,
                )
                rows.append(
                    RuntimeRow(
                        benchmark=benchmark,
                        model=model,
                        mode=mode,
                        task_id=str(eval_row.get("task_id") or ""),
                        runtime_seconds=_runtime_seconds(
                            eval_row.get("runtime_seconds"),
                            path=csv_path,
                            row_number=row_number,
                        ),
                        logged_total_cost_usd=_logged_total_cost_usd(eval_row),
                        total_cost_usd=total_cost,
                        cost_source=cost_source,
                        source_path=str(csv_path),
                    )
                )

    by_model_mode_raw = _group_by(rows, ("benchmark", "model", "mode"))
    by_mode_raw = _group_by(rows, ("benchmark", "mode"))

    by_model_mode = {
        (key[0], key[1], key[2]): value for key, value in by_model_mode_raw.items()
    }
    by_mode = {(key[0], key[1]): value for key, value in by_mode_raw.items()}

    by_benchmark_groups: dict[str, list[RuntimeRow]] = defaultdict(list)
    for row in rows:
        by_benchmark_groups[row.benchmark].append(row)
    by_benchmark = {
        benchmark: _summarize(group_rows)
        for benchmark, group_rows in sorted(by_benchmark_groups.items())
    }

    return RuntimeComputation(
        rows=rows,
        by_model_mode=by_model_mode,
        by_mode=by_mode,
        by_benchmark=by_benchmark,
        overall=_summarize(rows),
    )


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _summary_fields(prefix: list[str]) -> list[str]:
    return prefix + [
        "tasks",
        "total_seconds",
        "total_minutes",
        "total_hours",
        "total_cost_usd",
        "logged_total_cost_usd",
        "cost_delta_usd",
        "cost_multiplier",
        "avg_seconds",
        "avg_cost_usd",
        "avg_logged_cost_usd",
        "min_seconds",
        "max_seconds",
    ]


def write_outputs(summary: RuntimeComputation, output_dir: Path | str) -> None:
    output_root = Path(output_dir)

    model_mode_rows = [
        {"benchmark": benchmark, "model": model, "mode": mode, **values}
        for (benchmark, model, mode), values in sorted(summary.by_model_mode.items())
    ]
    _write_csv(
        output_root / "runtime_by_model_mode.csv",
        _summary_fields(["benchmark", "model", "mode"]),
        model_mode_rows,
    )

    mode_rows = [
        {"benchmark": benchmark, "mode": mode, **values}
        for (benchmark, mode), values in sorted(summary.by_mode.items())
    ]
    _write_csv(
        output_root / "runtime_by_mode.csv",
        _summary_fields(["benchmark", "mode"]),
        mode_rows,
    )

    benchmark_rows = [
        {"benchmark": benchmark, **values}
        for benchmark, values in sorted(summary.by_benchmark.items())
    ]
    _write_csv(
        output_root / "runtime_by_benchmark.csv",
        _summary_fields(["benchmark"]),
        benchmark_rows,
    )

    _write_csv(
        output_root / "runtime_overall.csv",
        _summary_fields([]),
        [summary.overall],
    )


def _format_duration(seconds: float) -> str:
    hours = seconds / 3600.0
    return f"{seconds:,.2f}s ({hours:,.2f}h)"


def print_summary(summary: RuntimeComputation) -> None:
    print("Runtime and uncached cost totals by benchmark and mode")
    print(
        f"{'Benchmark':<13} {'Mode':<52} {'Tasks':>6} {'Total Runtime':>24} "
        f"{'Uncached Cost':>15} {'Logged Cost':>13} {'Avg Sec':>10}"
    )
    print("-" * 141)
    for (benchmark, mode), values in sorted(summary.by_mode.items()):
        print(
            f"{benchmark:<13} {mode:<52} {values['tasks']:>6} "
            f"{_format_duration(values['total_seconds']):>24} "
            f"${values['total_cost_usd']:>14,.4f} "
            f"${values['logged_total_cost_usd']:>12,.4f} {values['avg_seconds']:>10.2f}"
        )

    print("\nRuntime and uncached cost totals by benchmark")
    print(
        f"{'Benchmark':<13} {'Tasks':>6} {'Total Runtime':>24} "
        f"{'Uncached Cost':>15} {'Logged Cost':>13} {'Avg Sec':>10}"
    )
    print("-" * 89)
    for benchmark, values in sorted(summary.by_benchmark.items()):
        print(
            f"{benchmark:<13} {values['tasks']:>6} "
            f"{_format_duration(values['total_seconds']):>24} "
            f"${values['total_cost_usd']:>14,.4f} "
            f"${values['logged_total_cost_usd']:>12,.4f} {values['avg_seconds']:>10.2f}"
        )

    overall = summary.overall
    print("\nOverall")
    print(
        f"{overall['tasks']:,} task runs, "
        f"{_format_duration(overall['total_seconds'])}, "
        f"${overall['total_cost_usd']:,.4f} uncached "
        f"(${overall['logged_total_cost_usd']:,.4f} logged), "
        f"{overall['avg_seconds']:.2f}s average"
    )


def _default_roots(repo_root: Path) -> dict[str, Path]:
    return {
        "kramabench": repo_root / "results-kramabench" / "modes",
        "lakeqa": repo_root / "results" / "modes",
    }


def _default_trace_roots(repo_root: Path) -> dict[str, Path]:
    return {
        "kramabench": repo_root / "results-kramabench" / "traces" / "modes",
        "lakeqa": repo_root / "results" / "traces" / "modes",
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "analysis_results_runtime",
        help="Directory for CSV outputs.",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Only print totals; do not write CSV outputs.",
    )
    args = parser.parse_args()

    summary = compute_runtime_summary(_default_roots(repo_root), _default_trace_roots(repo_root))
    print_summary(summary)
    if not args.no_write:
        write_outputs(summary, args.output_dir)
        print(f"\nWrote CSV summaries to {args.output_dir}")


if __name__ == "__main__":
    main()
