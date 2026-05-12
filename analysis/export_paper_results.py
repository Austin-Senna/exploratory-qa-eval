#!/usr/bin/env python3
"""Export SANA semantic-mode results into paper-ready LaTeX and figures."""

from __future__ import annotations

import argparse
import json
import math
import shutil
from pathlib import Path
from typing import Iterable, Mapping


MODEL_SPECS = [
    ("gpt-5.4-nano", ("gpt-5.4-nano", "openai_gpt-5.4-nano", "openai/gpt-5.4-nano")),
    ("gpt-5-mini", ("gpt-5-mini", "openai_gpt-5-mini", "openai/gpt-5-mini")),
]

PLANNED_CONDITIONS = [
    ("N-I-I-I", "naive", "ideal", "ideal", "ideal"),
    ("S-I-I-I", "standard", "ideal", "ideal", "ideal"),
    ("I-N-I-I", "ideal", "naive", "ideal", "ideal"),
    ("I-S-I-I", "ideal", "standard", "ideal", "ideal"),
    ("I-P-I-I", "ideal", "preloaded", "ideal", "ideal"),
    ("I-I-S-I", "ideal", "ideal", "standard", "ideal"),
    ("I-I-I-I", "ideal", "ideal", "ideal", "ideal"),
    ("N-N-S-N", "naive", "naive", "standard", "naive"),
    ("S-S-S-I", "standard", "standard", "standard", "ideal"),
    ("I-I-I-N", "ideal", "ideal", "ideal", "naive"),
]

MODE_DISPLAY = {
    "naive": "Naive",
    "standard": "Standard",
    "ideal": "Ideal",
    "preloaded": "Preloaded",
}

LETTER_TO_MODE = {"n": "naive", "d": "standard", "s": "standard", "i": "ideal", "p": "preloaded"}

SUPPORTING_FIGURES = {
    "fig6_cost_vs_semantic.pdf": "results_cost_vs_semantic.pdf",
    "fig03_semantic_x_error_variant.pdf": "results_semantic_x_error_variant.pdf",
    "fig01_semantic_buckets_variant.pdf": "results_semantic_buckets_variant.pdf",
    "fig2a_recall_semantic_combined.pdf": "results_recall_semantic_combined.pdf",
}


def _normalize_model_name(model: str) -> str:
    normalized = model.strip().replace("openai_", "").replace("openai/", "")
    for display, aliases in MODEL_SPECS:
        if normalized == display or model in aliases:
            return display
    return normalized


def _parse_variant_axes(variant: str) -> dict[str, str | None]:
    axes: dict[str, str | None] = {
        "agent_management": None,
        "search_tool": None,
        "computation_tool": "standard",
        "search_results": None,
    }
    parts = variant.split("_")
    for idx, token in enumerate(parts):
        if token == "search" and idx + 1 < len(parts):
            axes["search_tool"] = LETTER_TO_MODE.get(parts[idx + 1])
        elif token == "results" and idx + 1 < len(parts):
            axes["search_results"] = LETTER_TO_MODE.get(parts[idx + 1])
        elif token.startswith("plan") and len(token) > 4:
            axes["agent_management"] = LETTER_TO_MODE.get(token[4:])
        elif token.startswith("compute") and len(token) > 7:
            axes["computation_tool"] = LETTER_TO_MODE.get(token[7:])
        elif len(token) == 2 and token[0] in {"s", "r", "p", "c"}:
            mode = LETTER_TO_MODE.get(token[1])
            if token[0] == "s":
                axes["search_tool"] = mode
            elif token[0] == "r":
                axes["search_results"] = mode
            elif token[0] == "p":
                axes["agent_management"] = mode
            elif token[0] == "c":
                axes["computation_tool"] = mode
    return axes


def _axes_for_summary_row(row: Mapping[str, object]) -> dict[str, str | None]:
    axes = _parse_variant_axes(str(row.get("variant") or ""))
    for field in ("agent_management", "search_tool", "computation_tool", "search_results"):
        value = row.get(field)
        if value:
            axes[field] = str(value).lower()
    if not axes.get("computation_tool"):
        axes["computation_tool"] = "standard"
    return axes


def _format_rate(value: object, *, pending: bool = False) -> str:
    if pending:
        return "Pending"
    if value is None:
        return "N/A"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if math.isnan(number):
        return "N/A"
    return f"{number * 100.0:.1f}"


def _format_number(value: object, *, digits: int, pending: bool = False) -> str:
    if pending:
        return "Pending"
    if value is None:
        return "N/A"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if math.isnan(number):
        return "N/A"
    return f"{number:.{digits}f}"


def _find_observed_row(
    summary_rows: Iterable[Mapping[str, object]],
    *,
    model: str,
    plan: str,
    search: str,
    compute: str,
    results: str,
) -> Mapping[str, object] | None:
    for row in summary_rows:
        if _normalize_model_name(str(row.get("model") or "")) != model:
            continue
        axes = _axes_for_summary_row(row)
        if (
            axes.get("agent_management") == plan
            and axes.get("search_tool") == search
            and axes.get("computation_tool") == compute
            and axes.get("search_results") == results
        ):
            return row
    return None


def build_main_result_rows(summary_rows: list[Mapping[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for model, _aliases in MODEL_SPECS:
        for condition, plan, search, compute, results in PLANNED_CONDITIONS:
            observed = _find_observed_row(
                summary_rows,
                model=model,
                plan=plan,
                search=search,
                compute=compute,
                results=results,
            )
            pending = observed is None
            d_acc_value = None if pending else (observed.get("D_acc_recall") or observed.get("D_acc"))
            d_ret_value = None if pending else observed.get("D_ret")
            cost_value = None if pending else (
                observed.get("avg_total_cost_with_ideal_subagents_usd") or observed.get("avg_cost_usd")
            )
            calls_value = None if pending else (
                observed.get("avg_tool_calls_total") or observed.get("avg_tool_calls")
            )
            out.append(
                {
                    "model": model,
                    "condition": condition,
                    "plan": MODE_DISPLAY[plan],
                    "search": MODE_DISPLAY[search],
                    "compute": MODE_DISPLAY[compute],
                    "results": MODE_DISPLAY[results],
                    "n": "Pending" if pending else str(int(observed.get("n") or observed.get("n_total") or 0)),
                    "semantic_match": _format_rate(None if pending else observed.get("semantic_match"), pending=pending),
                    "avg_cost": _format_number(cost_value, digits=3, pending=pending),
                    "avg_calls": _format_number(calls_value, digits=1, pending=pending),
                    "D_acc": _format_rate(d_acc_value, pending=pending),
                    "D_ret": _format_rate(d_ret_value, pending=pending),
                    "status": "pending" if pending else "observed",
                }
            )
    return out


def _latex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def render_results_table(rows: list[Mapping[str, str]]) -> str:
    lines = [
        "\\begin{table*}[t]",
        "  \\caption{Main SANA ablation results. Pending cells mark planned runs that are not yet present in the current semantic analysis bundle.}",
        "  \\label{tab:sana-main-results}",
        "  \\centering",
        "  \\scriptsize",
        "  \\setlength{\\tabcolsep}{3pt}",
        "  \\begin{tabular}{llllllllrrrl}",
        "    \\toprule",
        "    Model & ID & Plan & Search & Compute & Results & $n$ & Sem. (\\%) & Cost & Calls & $D_{acc}$ (\\%) & $D_{ret}$ (\\%) \\\\",
        "    \\midrule",
    ]
    for row in rows:
        cells = [
            row["model"],
            row["condition"],
            row["plan"],
            row["search"],
            row["compute"],
            row["results"],
            row["n"],
            row["semantic_match"],
            row["avg_cost"],
            row["avg_calls"],
            row["D_acc"],
            row["D_ret"],
        ]
        lines.append("    " + " & ".join(_latex_escape(str(cell)) for cell in cells) + " \\\\")
    lines.extend(
        [
            "    \\bottomrule",
            "  \\end{tabular}",
            "\\end{table*}",
            "",
        ]
    )
    return "\n".join(lines)


def write_semantic_heatmap(rows: list[Mapping[str, str]], output_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    models = [model for model, _aliases in MODEL_SPECS]
    condition_ids = [condition for condition, *_rest in PLANNED_CONDITIONS]
    values = np.full((len(models), len(condition_ids)), np.nan)
    for row in rows:
        if row["semantic_match"] == "Pending":
            continue
        model_idx = models.index(row["model"])
        condition_idx = condition_ids.index(row["condition"])
        values[model_idx, condition_idx] = float(row["semantic_match"])

    cmap = plt.cm.Greens.copy()
    cmap.set_bad("#ECEFF3")
    fig, ax = plt.subplots(figsize=(8.6, 2.4))
    im = ax.imshow(values, cmap=cmap, vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(condition_ids)))
    ax.set_xticklabels(condition_ids, rotation=35, ha="right", fontsize=8)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=9)
    ax.set_title("Semantic Match by SANA Ablation Cell", fontsize=11)
    for i in range(len(models)):
        for j in range(len(condition_ids)):
            if np.isnan(values[i, j]):
                label = "pending"
                color = "#667085"
            else:
                label = f"{values[i, j]:.1f}%"
                color = "white" if values[i, j] >= 45 else "#1f2937"
            ax.text(j, i, label, ha="center", va="center", fontsize=7, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cbar.ax.set_ylabel("Semantic match (%)", rotation=270, labelpad=14, fontsize=8)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)


def copy_supporting_figures(analysis_dir: Path, paper_figures_dir: Path) -> list[Path]:
    copied: list[Path] = []
    source_dir = analysis_dir / "figures"
    paper_figures_dir.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in SUPPORTING_FIGURES.items():
        source = source_dir / source_name
        if source.exists():
            target = paper_figures_dir / target_name
            shutil.copyfile(source, target)
            copied.append(target)
    return copied


def export_paper_results(analysis_dir: Path, paper_dir: Path) -> dict[str, Path | list[Path]]:
    summary_path = analysis_dir / "summary.json"
    variant_summary_path = analysis_dir / "variant_summary.json"
    with summary_path.open() as handle:
        summary_rows = json.load(handle)
    if variant_summary_path.exists():
        with variant_summary_path.open() as handle:
            json.load(handle)

    rows = build_main_result_rows(summary_rows)
    generated_tex = paper_dir / "subsections" / "generated_main_results.tex"
    generated_tex.parent.mkdir(parents=True, exist_ok=True)
    generated_tex.write_text(render_results_table(rows), encoding="utf-8")

    heatmap_path = paper_dir / "figures" / "results_semantic_match_heatmap.pdf"
    write_semantic_heatmap(rows, heatmap_path)
    copied = copy_supporting_figures(analysis_dir, paper_dir / "figures")
    return {"table": generated_tex, "heatmap": heatmap_path, "supporting_figures": copied}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-dir", default="analysis_results_mode_semantic")
    parser.add_argument("--paper-dir", default="sana_framework_paper")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = export_paper_results(Path(args.analysis_dir), Path(args.paper_dir))
    print(f"Wrote {outputs['table']}")
    print(f"Wrote {outputs['heatmap']}")
    for figure in outputs["supporting_figures"]:
        print(f"Wrote {figure}")


if __name__ == "__main__":
    main()
