#!/usr/bin/env python3
"""Combine model-scoped turn-waste grouper outputs into cross-model artifacts."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote
from typing import Iterable


COMBINED_CSV_NAME = "combined_turn_waste_global_failures.csv"
COMBINED_REPORT_NAME = "combined_turn_waste_global_report.md"
COMBINED_FIGURE_NAME = "fig05_turn_waste_groups_by_model.pdf"
COMBINED_CONDITION_FIGURE_NAME = "fig05b_turn_waste_groups_by_condition.pdf"
PREFIX_COLUMNS = ["model_variant", "mode_variant", "source_file"]
RECONCILED_COLUMNS = ["reconciled_turn_waste_global_group"]
MODEL_COLORS = {
    "openai_gpt-5-mini": "#4C78A8",
    "gpt-5-mini": "#4C78A8",
    "openai_gpt-5.4-nano": "#F58518",
    "gpt-5.4-nano": "#F58518",
}
GROUP_COLORS = {
    "Data/source access and repair loops": "#4C78A8",
    "Redundant same-hop work after evidence": "#72B7B2",
    "Wrong-source and lookup fixation": "#F58518",
    "Final-hop retrieval/finalization failure": "#E45756",
}
FIGURE_EXCLUDED_GROUPS = {"Runtime/blocker fallback"}
CONDITION_FIGURE_ORDER = [
    ("No Plan", "search_i_results_i_plann_computei_k5_skills_off"),
    ("Standard Plan", "search_i_results_i_pland_computei_k5_skills_off"),
    ("BM25", "search_n_results_i_plani_computei_k5_skills_off"),
    ("Pneuma Hybrid", "search_d_results_i_plani_computei_k5_skills_off"),
    ("Standard Computation", "search_i_results_i_plani_k5_skills_off"),
    ("Ideal", "search_i_results_i_plani_computei_k5_skills_off"),
]
CONDITION_FIGURE_MODEL_ORDER = ["openai_gpt-5.4-nano", "openai_gpt-5-mini", "gpt-5.4-nano", "gpt-5-mini"]
CONDITION_FIGURE_MODEL_LABELS = {
    "openai_gpt-5.4-nano": "5.4\nnano",
    "gpt-5.4-nano": "5.4\nnano",
    "openai_gpt-5-mini": "5\nmini",
    "gpt-5-mini": "5\nmini",
}
CONDITION_FIGURE_LABELS = {
    "No Plan": "No\nPlan",
    "Standard Plan": "Standard\nPlan",
    "BM25": "BM25",
    "Pneuma Hybrid": "Pneuma\nHybrid",
    "Standard Computation": "Standard\nComputation",
    "Ideal": "Ideal",
}
PREFERRED_GROUP_ORDER = [
    "Data/source access and repair loops",
    "Redundant same-hop work after evidence",
    "Wrong-source and lookup fixation",
    "Final-hop retrieval/finalization failure",
]

RECONCILED_GLOBAL_GROUPS = {
    "Data-shape and source-access loops": "Data/source access and repair loops",
    "Ideal repair and status-error loops": "Data/source access and repair loops",
    "Located Data Extraction Thrash": "Data/source access and repair loops",
    "Hop Fixation Blocking Progress": "Redundant same-hop work after evidence",
    "Redundant Reconfirmation After Evidence": "Redundant same-hop work after evidence",
    "Same-hop recomputation churn": "Redundant same-hop work after evidence",
    "Late Broad Probe After Narrowing": "Wrong-source and lookup fixation",
    "Wrong Source Computation Loop": "Wrong-source and lookup fixation",
    "Wrong-source or lookup fixation": "Wrong-source and lookup fixation",
    "Incomplete finalization after key evidence": "Final-hop retrieval/finalization failure",
    "Known Target Retrieval Loop": "Final-hop retrieval/finalization failure",
    "Premature blocker fallback": "Runtime/blocker fallback",
    "Runtime-Dominated Failure": "Runtime/blocker fallback",
}


@dataclass(frozen=True)
class SourceFile:
    path: Path
    model_variant: str
    mode_variant: str
    relative_path: str


def clean_label(value: str | None, fallback: str = "(blank)") -> str:
    value = (value or "").strip()
    return value if value else fallback


def reconcile_global_group(value: str | None) -> str:
    label = clean_label(value)
    return RECONCILED_GLOBAL_GROUPS.get(label, label)


def plan_path_for_task(task_id: str) -> Path:
    path = Path(task_id)
    if not path.parts:
        return path
    plan_roots = {
        "tasks_mini": "plans_mini",
        "tasks-mini-kramabench": "plans-mini-kramabench",
        "tasks-hotpotqa-mini": "plans-hotpotqa-mini",
    }
    return Path(plan_roots.get(path.parts[0], path.parts[0]), *path.parts[1:])


def log_path_for_row(row: dict[str, str]) -> Path:
    task_path = Path(str(row.get("task_id", "")))
    log_parts = list(task_path.parts)
    if log_parts:
        log_parts[-1] = Path(log_parts[-1]).with_suffix(".log").name
    return Path("logs") / "modes" / row["model_variant"] / row["mode_variant"] / Path(*log_parts)


def markdown_link(label: str, target: Path, base_dir: Path) -> str:
    relative = target.relative_to(base_dir) if target.is_absolute() and target.is_relative_to(base_dir) else None
    href_path = relative if relative is not None else target
    try:
        href = Path("../") / href_path
    except TypeError:
        href = href_path
    return f"[{label}]({quote(href.as_posix())})"


def parse_int(value: str | None) -> int:
    try:
        return int(float((value or "").strip()))
    except ValueError:
        return 0


def discover_source_files(grouped_root: Path) -> list[SourceFile]:
    files = sorted(grouped_root.rglob("turn_waste_global_failures.csv"))
    sources: list[SourceFile] = []

    for path in files:
        rel = path.relative_to(grouped_root)
        parts = rel.parts
        model_variant = ""
        mode_variant = ""

        if len(parts) >= 5 and parts[1] == "modes":
            model_variant = parts[0]
            mode_variant = parts[3]
        elif len(parts) >= 4 and parts[0] == "modes":
            model_variant = parts[1]
            mode_variant = parts[2]
        elif "modes" in parts:
            mode_index = parts.index("modes")
            if mode_index + 2 < len(parts):
                model_variant = parts[mode_index + 1]
                mode_variant = parts[mode_index + 2]

        if not model_variant:
            model_variant = parts[0] if parts else "(unknown-model)"
        if not mode_variant:
            mode_variant = path.parent.name

        sources.append(
            SourceFile(
                path=path,
                model_variant=model_variant,
                mode_variant=mode_variant,
                relative_path=rel.as_posix(),
            )
        )

    return sources


def read_combined_rows(sources: Iterable[SourceFile]) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    source_columns: list[str] = []
    seen_columns: set[str] = set()

    for source in sources:
        with source.path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            for column in reader.fieldnames or []:
                if column not in seen_columns and column not in PREFIX_COLUMNS:
                    source_columns.append(column)
                    seen_columns.add(column)

            for row in reader:
                combined = {
                    "model_variant": source.model_variant,
                    "mode_variant": source.mode_variant,
                    "source_file": source.relative_path,
                    "reconciled_turn_waste_global_group": reconcile_global_group(row.get("turn_waste_global_group")),
                }
                combined.update({column: row.get(column, "") for column in source_columns})
                rows.append(combined)

    for row in rows:
        for column in source_columns:
            row.setdefault(column, "")

    rows.sort(
        key=lambda row: (
            row["source_file"],
            clean_label(row.get("reconciled_turn_waste_global_group")),
            clean_label(row.get("turn_waste_global_group")),
            -parse_int(row.get("estimated_wasted_turns")),
            row.get("task_id", ""),
        )
    )
    return rows, PREFIX_COLUMNS + RECONCILED_COLUMNS + source_columns


def write_combined_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pretty_model(model: str) -> str:
    return model.replace("openai_", "").replace("openai/", "")


def _is_figure_group(group_name: str) -> bool:
    return clean_label(group_name) not in FIGURE_EXCLUDED_GROUPS


def _label_text_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "black"
    r, g, b = (int(hex_color[index : index + 2], 16) for index in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "black" if luminance > 0.55 else "white"


def _ordered_groups_from_counts(group_totals: Counter[str]) -> list[str]:
    preferred = [
        group
        for group in PREFERRED_GROUP_ORDER
        if group_totals.get(group, 0) > 0 and _is_figure_group(group)
    ]
    extras = sorted(
        group
        for group, count in group_totals.items()
        if count > 0 and group not in preferred and _is_figure_group(group)
    )
    return preferred + extras


def write_model_group_figure(path: Path, rows: list[dict[str, str]]) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    counts_by_group_model: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        group_name = clean_label(row.get("reconciled_turn_waste_global_group"))
        if not _is_figure_group(group_name):
            continue
        counts_by_group_model[group_name][row["model_variant"]] += 1

    if not counts_by_group_model:
        return False

    ordered_groups = sorted(
        counts_by_group_model,
        key=lambda group: (-sum(counts_by_group_model[group].values()), group),
    )
    preferred_models = ["openai_gpt-5.4-nano", "openai_gpt-5-mini", "gpt-5.4-nano", "gpt-5-mini"]
    ordered_models: list[str] = []
    for model in preferred_models:
        if any(counts_by_group_model[group].get(model, 0) for group in ordered_groups) and model not in ordered_models:
            ordered_models.append(model)
    for group_counts in counts_by_group_model.values():
        for model in sorted(group_counts):
            if model not in ordered_models:
                ordered_models.append(model)

    y_positions = list(range(len(ordered_groups)))
    bar_height = 0.34 if len(ordered_models) <= 2 else max(0.18, 0.72 / max(1, len(ordered_models)))
    max_count = max(max(counter.values(), default=0) for counter in counts_by_group_model.values())
    fig, ax = plt.subplots(figsize=(10.5, max(3.3, 0.62 * len(ordered_groups) + 1.3)))

    for model_index, model in enumerate(ordered_models):
        offset = (model_index - (len(ordered_models) - 1) / 2) * bar_height
        values = [counts_by_group_model[group].get(model, 0) for group in ordered_groups]
        bars = ax.barh(
            [y + offset for y in y_positions],
            values,
            height=bar_height * 0.88,
            color=MODEL_COLORS.get(model, "#6F6F6F"),
            label=pretty_model(model),
        )
        for bar, value in zip(bars, values):
            if value <= 0:
                continue
            ax.text(
                value + max(0.15, max_count * 0.012),
                bar.get_y() + bar.get_height() / 2,
                str(value),
                ha="left",
                va="center",
                fontsize=8,
            )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(ordered_groups, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Grouped failed rows")
    ax.set_title("Reconciled Turn-Waste Error Groups by Model")
    ax.grid(axis="x", alpha=0.22, linestyle="--", linewidth=0.7)
    ax.set_xlim(0, max(1, max_count + max(4, max_count * 0.16)))
    ax.legend(loc="lower right", frameon=True, framealpha=0.95, fontsize=9)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return True


def condition_group_counts(rows: list[dict[str, str]]) -> tuple[list[tuple[str, str]], list[str], dict[tuple[str, str], Counter[str]]]:
    counts_by_variant_model_group: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    group_totals: Counter[str] = Counter()

    variant_lookup = {variant: label for label, variant in CONDITION_FIGURE_ORDER}
    for row in rows:
        variant = str(row.get("mode_variant", ""))
        if variant not in variant_lookup:
            continue
        group_name = clean_label(row.get("reconciled_turn_waste_global_group"))
        if not _is_figure_group(group_name):
            continue
        counts_by_variant_model_group[(variant, row["model_variant"])][group_name] += 1
        group_totals[group_name] += 1

    ordered_groups = _ordered_groups_from_counts(group_totals)
    active_conditions = [
        (label, variant)
        for label, variant in CONDITION_FIGURE_ORDER
        if any(sum(counts.values()) > 0 for (observed_variant, _), counts in counts_by_variant_model_group.items() if observed_variant == variant)
    ]
    return active_conditions, ordered_groups, counts_by_variant_model_group


def ordered_condition_models(
    active_conditions: list[tuple[str, str]],
    counts_by_variant_model_group: dict[tuple[str, str], Counter[str]],
) -> list[tuple[str, str, str]]:
    observed_by_variant: dict[str, set[str]] = defaultdict(set)
    observed_models: set[str] = set()
    for variant, model in counts_by_variant_model_group:
        observed_models.add(model)
        if sum(counts_by_variant_model_group[(variant, model)].values()) > 0:
            observed_by_variant[variant].add(model)

    model_order: list[str] = []
    for model in CONDITION_FIGURE_MODEL_ORDER:
        if model in observed_models and model not in model_order:
            model_order.append(model)
    for model in sorted(observed_models):
        if model not in model_order:
            model_order.append(model)

    ordered: list[tuple[str, str, str]] = []
    for label, variant in active_conditions:
        for model in model_order:
            ordered.append((label, variant, model))
    return ordered


def write_condition_group_figure(path: Path, rows: list[dict[str, str]]) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    active_conditions, ordered_groups, counts_by_variant_model_group = condition_group_counts(rows)
    if not active_conditions or not ordered_groups:
        return False
    condition_models = ordered_condition_models(active_conditions, counts_by_variant_model_group)
    if not condition_models:
        return False

    gap = 1.55
    x_positions: list[float] = []
    current_x = 0.0
    previous_variant = None
    for _, variant, _ in condition_models:
        if previous_variant is not None and variant != previous_variant:
            current_x += gap
        x_positions.append(current_x)
        current_x += 1.0
        previous_variant = variant
    totals = [
        sum(counts_by_variant_model_group.get((variant, model), Counter()).values())
        for _, variant, model in condition_models
    ]
    ymax = max(totals, default=0)
    fig, ax = plt.subplots(figsize=(15.6, 7.2))
    bottoms = [0 for _ in condition_models]

    for group_name in ordered_groups:
        values = [
            counts_by_variant_model_group.get((variant, model), Counter()).get(group_name, 0)
            for _, variant, model in condition_models
        ]
        color = GROUP_COLORS.get(group_name, "#7F7F7F")
        bars = ax.bar(x_positions, values, bottom=bottoms, color=color, label=group_name, width=0.74)
        label_color = _label_text_color(color)
        for bar, value, bottom in zip(bars, values, bottoms):
            if value <= 0:
                continue
            if value >= max(2, ymax * 0.08):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bottom + value / 2,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=12,
                    color=label_color,
                )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    for x_pos, total in zip(x_positions, totals):
        ax.text(
            x_pos,
            total + max(0.25, ymax * 0.025),
            str(total),
            ha="center",
            va="bottom",
            fontsize=13,
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        [CONDITION_FIGURE_MODEL_LABELS.get(model, pretty_model(model).replace("gpt-", "gpt\n")) for _, _, model in condition_models],
        fontsize=12,
    )
    for label, variant in active_conditions:
        variant_positions = [x for x, (_, observed_variant, _) in zip(x_positions, condition_models) if observed_variant == variant]
        if not variant_positions:
            continue
        center = sum(variant_positions) / len(variant_positions)
        ax.text(
            center,
            -0.135,
            CONDITION_FIGURE_LABELS.get(label, label),
            ha="center",
            va="top",
            fontsize=15,
            transform=ax.get_xaxis_transform(),
        )
    ax.set_ylabel("Grouped failed rows", fontsize=15)
    ax.set_title("Turn-Waste Error Groups by SANA Condition and Model", fontsize=20, pad=12)
    ax.grid(axis="y", alpha=0.22, linestyle="--", linewidth=0.7)
    ax.set_ylim(0, max(1, ymax + max(3, ymax * 0.18)))
    ax.tick_params(axis="y", labelsize=13)
    ax.legend(loc="upper right", frameon=True, framealpha=0.94, fontsize=13)
    fig.tight_layout(rect=(0, 0.085, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return True


def model_counts_text(counter: Counter[str]) -> str:
    return "; ".join(f"{model}: {count}" for model, count in sorted(counter.items()))


def add_table(lines: list[str], headers: list[str], table_rows: list[list[str]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in table_rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    lines.append("")


def count_by_key(rows: list[dict[str, str]], key_fn) -> list[tuple[tuple[str, ...], int, Counter[str]]]:
    counts: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for row in rows:
        key = key_fn(row)
        counts[key][row["model_variant"]] += 1
    return sorted(
        ((key, sum(model_counts.values()), model_counts) for key, model_counts in counts.items()),
        key=lambda item: (-item[1], item[0]),
    )


def build_report(rows: list[dict[str, str]], grouped_root: Path, csv_path: Path) -> str:
    report_dir = csv_path.parent
    lines: list[str] = [
        "# Combined Turn-Waste Global Report",
        "",
        f"Grouped root: `{grouped_root}`",
        f"Combined CSV: `{csv_path.name}`",
        f"Total grouped failure rows: {len(rows)}",
        "",
        "## Counts by Model",
        "",
    ]

    by_model = Counter(row["model_variant"] for row in rows)
    add_table(lines, ["Model", "Errors"], [[model, str(count)] for model, count in sorted(by_model.items())])

    lines.extend(["## Counts by Reconciled Global Group", ""])
    group_rows = count_by_key(rows, lambda row: (clean_label(row.get("reconciled_turn_waste_global_group")),))
    add_table(
        lines,
        ["Reconciled Global Group", "Errors", "Errors by Model"],
        [[key[0], str(total), model_counts_text(model_counts)] for key, total, model_counts in group_rows],
    )

    lines.extend(["## Counts by Reconciled Global Group and Subtype", ""])
    subtype_rows = count_by_key(
        rows,
        lambda row: (
            clean_label(row.get("reconciled_turn_waste_global_group")),
            clean_label(row.get("turn_waste_global_subtype"), "(none)"),
        ),
    )
    add_table(
        lines,
        ["Global Group", "Subtype", "Errors", "Errors by Model"],
        [[key[0], key[1], str(total), model_counts_text(model_counts)] for key, total, model_counts in subtype_rows],
    )

    lines.extend(["## Counts by Original Global Group", ""])
    original_group_rows = count_by_key(rows, lambda row: (clean_label(row.get("turn_waste_global_group")),))
    add_table(
        lines,
        ["Original Global Group", "Reconciled Global Group", "Errors", "Errors by Model"],
        [
            [
                key[0],
                reconcile_global_group(key[0]),
                str(total),
                model_counts_text(model_counts),
            ]
            for key, total, model_counts in original_group_rows
        ],
    )

    lines.extend(["## Counts by Error Bucket", ""])
    bucket_rows = count_by_key(rows, lambda row: (clean_label(row.get("log_error_bucket")),))
    add_table(
        lines,
        ["Error Bucket", "Errors", "Errors by Model"],
        [[key[0], str(total), model_counts_text(model_counts)] for key, total, model_counts in bucket_rows],
    )

    lines.extend(["## Representative Evidence", ""])
    rows_by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_group[clean_label(row.get("reconciled_turn_waste_global_group"))].append(row)

    for group, group_items in sorted(rows_by_group.items()):
        lines.extend([f"### {group}", ""])
        for row in sorted(
            group_items,
            key=lambda item: (-parse_int(item.get("estimated_wasted_turns")), item["model_variant"], item.get("task_id", "")),
        )[:5]:
            task_path = Path(clean_label(row.get("task_id"), ""))
            plan_path = plan_path_for_task(task_path.as_posix())
            log_path = log_path_for_row(row)
            links = " | ".join(
                [
                    markdown_link("task", task_path, report_dir),
                    markdown_link("plan", plan_path, report_dir),
                    markdown_link("log", log_path, report_dir),
                ]
            )
            evidence = clean_label(row.get("turn_waste_evidence"), "(no evidence)")
            if len(evidence) > 260:
                evidence = evidence[:257].rstrip() + "..."
            lines.append(
                f"- {links} | `{row['model_variant']}` `{row.get('mode_variant', '')}` "
                f"(original group: {clean_label(row.get('turn_waste_global_group'))}; "
                f"{clean_label(row.get('log_error_bucket'))}; "
                f"wasted turns: {parse_int(row.get('estimated_wasted_turns'))}): "
                f"{evidence}"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def combine_grouped_models(grouped_root: str | Path, output_root: str | Path | None = None) -> dict[str, Path]:
    grouped_root = Path(grouped_root)
    output_root = Path(output_root) if output_root is not None else grouped_root.with_name(grouped_root.name + "_combined")

    sources = discover_source_files(grouped_root)
    if not sources:
        raise FileNotFoundError(f"No turn_waste_global_failures.csv files found under {grouped_root}")

    rows, fieldnames = read_combined_rows(sources)
    csv_path = output_root / COMBINED_CSV_NAME
    report_path = output_root / COMBINED_REPORT_NAME
    figure_path = output_root / COMBINED_FIGURE_NAME
    condition_figure_path = output_root / COMBINED_CONDITION_FIGURE_NAME

    write_combined_csv(csv_path, rows, fieldnames)
    report_path.write_text(build_report(rows, grouped_root, csv_path))
    wrote_figure = write_model_group_figure(figure_path, rows)
    wrote_condition_figure = write_condition_group_figure(condition_figure_path, rows)

    outputs = {"csv_path": csv_path, "report_path": report_path}
    if wrote_figure:
        outputs["figure_path"] = figure_path
    if wrote_condition_figure:
        outputs["condition_figure_path"] = condition_figure_path
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grouped-root", required=True, type=Path)
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args()

    outputs = combine_grouped_models(grouped_root=args.grouped_root, output_root=args.output_root)
    print(f"Wrote {outputs['csv_path']}")
    print(f"Wrote {outputs['report_path']}")
    if "figure_path" in outputs:
        print(f"Wrote {outputs['figure_path']}")
    if "condition_figure_path" in outputs:
        print(f"Wrote {outputs['condition_figure_path']}")


if __name__ == "__main__":
    main()
