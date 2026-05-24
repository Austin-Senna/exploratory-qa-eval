#!/usr/bin/env python3
"""Recompute SANA run costs with cached input billed at full input price.

The eval CSVs already contain logged costs that use the local pricing table's
cached-input discount. This script keeps the same token logs and model prices,
but computes a counterfactual cost where cached and uncached input tokens are
both billed at the model's normal input rate. Ideal-helper subagent costs are
recomputed from per-call trace events so mixed helper models are handled
correctly.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands_evaluation.helper.constants import MODEL_PRICING


@dataclass(frozen=True)
class CostRow:
    model: str
    variant: str
    task_id: str
    logged_main_cost_usd: float
    uncached_main_cost_usd: float
    logged_ideal_cost_usd: float
    uncached_ideal_cost_usd: float
    logged_total_cost_usd: float
    uncached_total_cost_usd: float
    delta_total_cost_usd: float
    cost_multiplier: float
    trace_path: str
    trace_event_count: int
    ideal_cost_source: str


@dataclass(frozen=True)
class CostComputation:
    rows: list[CostRow]
    variant_summaries: dict[tuple[str, str], dict[str, float | int | str]]
    model_summaries: dict[str, dict[str, float | int | str]]
    overall_summary: dict[str, float | int | str]


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


def _parse_eval_csv_path(path: Path, results_dir: Path) -> tuple[str, str]:
    rel = path.relative_to(results_dir)
    parts = rel.parts
    if len(parts) < 3 or parts[-1] != "eval_results.csv":
        raise ValueError(f"Expected <model>/<variant>/eval_results.csv under {results_dir}, got {path}")
    return parts[0], parts[1]


def _trace_path_for_task(traces_dir: Path, model: str, variant: str, task_id: str) -> Path:
    task_path = Path(task_id)
    if len(task_path.parts) < 2:
        raise ValueError(f"Cannot infer trace path from task_id={task_id!r}")
    return traces_dir / model / variant / task_path.parent.name / f"{task_path.stem}.jsonl"


def _iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _uncached_ideal_cost_from_trace(path: Path) -> tuple[float, int, float]:
    total_uncached = 0.0
    total_logged = 0.0
    count = 0
    for event in _iter_jsonl(path):
        if event.get("event") != "ideal_subagent_cost":
            continue
        model_name = str(event.get("model_name") or "")
        total_uncached += _full_input_cost(
            model_name,
            input_tokens=_as_float(event.get("input_tokens")),
            output_tokens=_as_float(event.get("output_tokens")),
        )
        total_logged += _as_float(event.get("cost_usd"))
        count += 1
    return total_uncached, count, total_logged


def _summarize(rows: list[CostRow], *, model: str | None = None, variant: str | None = None) -> dict[str, float | int | str]:
    n = len(rows)
    logged_main = sum(row.logged_main_cost_usd for row in rows)
    uncached_main = sum(row.uncached_main_cost_usd for row in rows)
    logged_ideal = sum(row.logged_ideal_cost_usd for row in rows)
    uncached_ideal = sum(row.uncached_ideal_cost_usd for row in rows)
    logged_total = sum(row.logged_total_cost_usd for row in rows)
    uncached_total = sum(row.uncached_total_cost_usd for row in rows)
    summary: dict[str, float | int | str] = {
        "n": n,
        "logged_main_cost_usd": logged_main,
        "uncached_main_cost_usd": uncached_main,
        "logged_ideal_cost_usd": logged_ideal,
        "uncached_ideal_cost_usd": uncached_ideal,
        "logged_total_cost_usd": logged_total,
        "uncached_total_cost_usd": uncached_total,
        "delta_total_cost_usd": uncached_total - logged_total,
        "cost_multiplier": uncached_total / logged_total if logged_total else 0.0,
        "avg_logged_total_cost_usd": logged_total / n if n else 0.0,
        "avg_uncached_total_cost_usd": uncached_total / n if n else 0.0,
        "avg_delta_total_cost_usd": (uncached_total - logged_total) / n if n else 0.0,
        "avg_logged_main_cost_usd": logged_main / n if n else 0.0,
        "avg_uncached_main_cost_usd": uncached_main / n if n else 0.0,
        "avg_logged_ideal_cost_usd": logged_ideal / n if n else 0.0,
        "avg_uncached_ideal_cost_usd": uncached_ideal / n if n else 0.0,
        "trace_event_count": sum(row.trace_event_count for row in rows),
        "logged_ideal_fallback_rows": sum(1 for row in rows if row.ideal_cost_source != "trace"),
    }
    if model is not None:
        summary["model"] = model
    if variant is not None:
        summary["variant"] = variant
    return summary


def compute_uncached_costs(
    results_dir: Path | str,
    traces_dir: Path | str,
    *,
    missing_trace_policy: str = "error",
) -> CostComputation:
    if missing_trace_policy not in {"error", "logged-ideal"}:
        raise ValueError("missing_trace_policy must be 'error' or 'logged-ideal'")
    results_root = Path(results_dir)
    traces_root = Path(traces_dir)
    rows: list[CostRow] = []
    for csv_path in sorted(results_root.rglob("eval_results.csv")):
        model, variant = _parse_eval_csv_path(csv_path, results_root)
        with csv_path.open(newline="") as f:
            for eval_row in csv.DictReader(f):
                task_id = str(eval_row.get("task_id") or "")
                trace_path = _trace_path_for_task(traces_root, model, variant, task_id)
                logged_ideal = _as_float(eval_row.get("ideal_subagent_cost_usd"))
                ideal_cost_source = "trace"
                if trace_path.exists():
                    uncached_ideal, event_count, trace_logged_ideal = _uncached_ideal_cost_from_trace(trace_path)
                    if event_count == 0 and logged_ideal:
                        if missing_trace_policy == "error":
                            raise ValueError(
                                f"No ideal_subagent_cost events in {trace_path}, but CSV logged {logged_ideal}"
                            )
                        uncached_ideal = logged_ideal
                        trace_logged_ideal = logged_ideal
                        ideal_cost_source = "logged-ideal-no-events"
                elif missing_trace_policy == "logged-ideal":
                    uncached_ideal = logged_ideal
                    trace_logged_ideal = logged_ideal
                    event_count = 0
                    ideal_cost_source = "logged-ideal-missing-trace"
                else:
                    raise FileNotFoundError(f"Missing trace for {task_id}: {trace_path}")

                logged_main = _as_float(eval_row.get("cost_usd"))
                uncached_main = _full_input_cost(
                    model,
                    input_tokens=_as_float(eval_row.get("input_tokens")),
                    output_tokens=_as_float(eval_row.get("output_tokens")),
                )
                logged_total = _as_float(eval_row.get("total_cost_with_all_subagents_usd"))
                if not logged_total:
                    logged_total = logged_main + logged_ideal + _as_float(eval_row.get("delegation_subagent_cost_usd"))
                uncached_total = uncached_main + uncached_ideal + _as_float(eval_row.get("delegation_subagent_cost_usd"))
                rows.append(
                    CostRow(
                        model=model,
                        variant=variant,
                        task_id=task_id,
                        logged_main_cost_usd=logged_main,
                        uncached_main_cost_usd=uncached_main,
                        logged_ideal_cost_usd=logged_ideal or trace_logged_ideal,
                        uncached_ideal_cost_usd=uncached_ideal,
                        logged_total_cost_usd=logged_total,
                        uncached_total_cost_usd=uncached_total,
                        delta_total_cost_usd=uncached_total - logged_total,
                        cost_multiplier=uncached_total / logged_total if logged_total else 0.0,
                        trace_path=str(trace_path),
                        trace_event_count=event_count,
                        ideal_cost_source=ideal_cost_source,
                    )
                )

    variant_keys = sorted({(row.model, row.variant) for row in rows})
    model_keys = sorted({row.model for row in rows})
    variant_summaries = {
        key: _summarize([row for row in rows if (row.model, row.variant) == key], model=key[0], variant=key[1])
        for key in variant_keys
    }
    model_summaries = {
        model: _summarize([row for row in rows if row.model == model], model=model)
        for model in model_keys
    }
    return CostComputation(
        rows=rows,
        variant_summaries=variant_summaries,
        model_summaries=model_summaries,
        overall_summary=_summarize(rows),
    )


def _write_rows(path: Path, rows: list[CostRow]) -> None:
    fieldnames = list(CostRow.__dataclass_fields__.keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: getattr(row, field) for field in fieldnames})


def _write_summaries(path: Path, summaries: Iterable[Mapping[str, float | int | str]]) -> None:
    rows = list(summaries)
    if not rows:
        return
    preferred = [
        "model",
        "variant",
        "n",
        "logged_total_cost_usd",
        "uncached_total_cost_usd",
        "delta_total_cost_usd",
        "cost_multiplier",
        "avg_logged_total_cost_usd",
        "avg_uncached_total_cost_usd",
        "avg_delta_total_cost_usd",
        "avg_logged_main_cost_usd",
        "avg_uncached_main_cost_usd",
        "avg_logged_ideal_cost_usd",
        "avg_uncached_ideal_cost_usd",
        "logged_main_cost_usd",
        "uncached_main_cost_usd",
        "logged_ideal_cost_usd",
        "uncached_ideal_cost_usd",
        "trace_event_count",
        "logged_ideal_fallback_rows",
    ]
    fieldnames = [field for field in preferred if any(field in row for row in rows)]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True, help="Directory containing <model>/<variant>/eval_results.csv")
    parser.add_argument("--traces-dir", required=True, help="Directory containing <model>/<variant>/<task-dir>/<task>.jsonl")
    parser.add_argument("--output-dir", required=True, help="Directory for uncached cost CSV outputs")
    parser.add_argument(
        "--missing-trace-policy",
        choices=["error", "logged-ideal"],
        default="error",
        help="Use logged ideal cost when a trace is missing or has no ideal events. Main-agent uncached cost is still recomputed.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = compute_uncached_costs(
        args.results_dir,
        args.traces_dir,
        missing_trace_policy=args.missing_trace_policy,
    )
    _write_rows(output_dir / "per_task_uncached_costs.csv", result.rows)
    _write_summaries(output_dir / "variant_uncached_cost_summary.csv", result.variant_summaries.values())
    _write_summaries(output_dir / "model_uncached_cost_summary.csv", result.model_summaries.values())
    _write_summaries(output_dir / "overall_uncached_cost_summary.csv", [result.overall_summary])

    overall = result.overall_summary
    print(
        "Wrote uncached cost summaries to "
        f"{output_dir} (rows={overall['n']}, "
        f"logged=${overall['logged_total_cost_usd']:.2f}, "
        f"uncached=${overall['uncached_total_cost_usd']:.2f}, "
        f"delta=${overall['delta_total_cost_usd']:.2f})"
    )


if __name__ == "__main__":
    main()
