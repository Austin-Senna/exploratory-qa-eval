#!/usr/bin/env python3
"""
Generate all paper figures using matplotlib/seaborn.

Figures produced:
  fig1_em_comparison.pdf     — EM rate by condition × model (grouped bar)
  fig2_discovery_metrics.pdf — D_ret vs D_acc by condition
  fig3_failure_breakdown.pdf — 100% stacked bar: EM × D_acc attribution per condition
  fig3b_failure_by_model.pdf — Heatmap: EM × D_acc attribution per condition × model
  fig4_backend_provenance.pdf — Condition A: first-hit backend pie chart
  fig5_query_drift.pdf        — Condition B: Jaccard similarity distribution
  fig6_cost_vs_em.pdf         — Cost-accuracy frontier scatter
  fig7_latency_dist.pdf       — Tool call latency CDF by backend
  fig8_tool_precision_recall.pdf — Per-search-tool avg precision & recall (grouped bar)

Usage:
    python analysis/generate_figures.py [--results-dir results] [--sidecar-dir results/sidecar]
                                        [--tasks-dir tasks_mini] [--output-dir figures]
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path


_FAILURE_COLORS = {
    "em1_dacc_ge_0_8": "#1A9850",
    "em1_dacc_0_5_to_0_8": "#66BD63",
    "em1_dacc_0_2_to_0_5": "#A6D96A",
    "em1_dacc_lt_0_2": "#D9EF8B",
    "em0_dacc_ge_0_8": "#D73027",
    "em0_dacc_0_5_to_0_8": "#F46D43",
    "em0_dacc_0_2_to_0_5": "#FDAE61",
    "em0_dacc_lt_0_2": "#FEE08B",
}

_FAILURE_LABEL_TEXT = {
    "em1_dacc_ge_0_8": "EM=1, 0.8<=D_acc<=1.0",
    "em1_dacc_0_5_to_0_8": "EM=1, 0.5<=D_acc<0.8",
    "em1_dacc_0_2_to_0_5": "EM=1, 0.2<=D_acc<0.5",
    "em1_dacc_lt_0_2": "EM=1, D_acc<0.2",
    "em0_dacc_ge_0_8": "EM=0, 0.8<=D_acc<=1.0",
    "em0_dacc_0_5_to_0_8": "EM=0, 0.5<=D_acc<0.8",
    "em0_dacc_0_2_to_0_5": "EM=0, 0.2<=D_acc<0.5",
    "em0_dacc_lt_0_2": "EM=0, D_acc<0.2",
}


def _import_plot_libs():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
        return plt, sns
    except ImportError:
        print("matplotlib/seaborn not installed. Install with: pip install matplotlib seaborn")
        sys.exit(1)


def _present_failure_labels(grouped_counts: dict[str, dict[str, int]], label_order: list[str]) -> list[str]:
    """Return observed labels in the configured order, with unknown labels appended."""
    observed = {
        label
        for counts in grouped_counts.values()
        for label, value in counts.items()
        if value
    }
    ordered = [label for label in label_order if label in observed]
    return ordered + sorted(observed - set(label_order))


def _failure_label_text(label: str) -> str:
    return _FAILURE_LABEL_TEXT.get(label, label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results/figures")
    args = parser.parse_args()

    plt, sns = _import_plot_libs()
    sns.set_theme(style="whitegrid", palette="muted")

    repo_root = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_root))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    from analysis.compute_em import load_results, compute_stats, _count_search_calls
    from analysis.discovery_metrics import (
        load_traces, load_task_gold_ids, compute_discovery_metrics, compute_tools_discovery, make_task_stem_key
    )
    from analysis.failure_attribution import _LABEL_ORDER, classify_failure

    records = load_results(args.results_dir)
    em_table = compute_stats(records)

    # -----------------------------------------------------------------------
    # Fig 1: EM by condition × model
    # -----------------------------------------------------------------------
    if em_table:
        fig, ax = plt.subplots(figsize=(9, 5))
        conditions = sorted(set(k[0] for k in em_table))
        models = sorted(set(k[1] for k in em_table))
        x = range(len(models))
        width = 0.8 / max(len(conditions), 1)

        for i, cond in enumerate(conditions):
            ems = [em_table.get((cond, m), {}).get("em") or 0.0 for m in models]
            offset = (i - len(conditions) / 2 + 0.5) * width
            bars = ax.bar([xi + offset for xi in x], [e * 100 for e in ems],
                          width=width * 0.9, label=f"Condition {cond}")
            for bar, val in zip(bars, ems):
                if val:
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                            f"{val*100:.1f}", ha="center", va="bottom", fontsize=8)

        ax.set_xticks(list(x))
        ax.set_xticklabels([m.split("/")[-1] for m in models], rotation=20, ha="right")
        ax.set_ylabel("Exact Match (%)")
        ax.set_title("Exact Match by Condition × Model")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fig1_em_comparison.pdf")
        plt.close(fig)
        print(f"Saved fig1_em_comparison.pdf")

    # -----------------------------------------------------------------------
    # Fig 2: D_ret vs D_acc by condition × model (grouped bar)
    # -----------------------------------------------------------------------
    task_gold = load_task_gold_ids(args.tasks_dir)
    traces_root = Path(args.traces_dir)

    # Collect D_ret, D_acc per (condition, model)
    discovery_by_cm: dict = {}
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        cond_name = condition_dir.name
        for model_dir in condition_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model_name = model_dir.name
            cond_traces = load_traces(str(model_dir))
            if cond_traces:
                disc = compute_discovery_metrics(cond_traces, task_gold)
                if disc["aggregate"]:
                    discovery_by_cm[(cond_name, model_name)] = disc["aggregate"]

    if discovery_by_cm:
        conditions = sorted(set(k[0] for k in discovery_by_cm))
        models = sorted(set(k[1] for k in discovery_by_cm))

        # Create grouped bar chart for D_ret and D_acc
        x = range(len(models))
        width = 0.35 / max(len(conditions), 1)
        fig, ax = plt.subplots(figsize=(12, 6))

        for i, cond in enumerate(conditions):
            d_rets = [discovery_by_cm.get((cond, m), {}).get("D_ret", 0) for m in models]
            d_accs = [discovery_by_cm.get((cond, m), {}).get("D_acc", 0) for m in models]

            offset_base = (i - len(conditions) / 2 + 0.5) * width * 2
            bars_ret = ax.bar([xi + offset_base - width / 2 for xi in x], d_rets,
                              width=width * 0.9, label=f"{cond.upper()} D_ret", alpha=0.8)
            bars_acc = ax.bar([xi + offset_base + width / 2 for xi in x], d_accs,
                              width=width * 0.9, label=f"{cond.upper()} D_acc", alpha=0.8, hatch="//")

            for bar in list(bars_ret) + list(bars_acc):
                h = bar.get_height()
                if h > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01,
                            f"{h:.2f}", ha="center", va="bottom", fontsize=7, rotation=45)

        ax.set_xticks(list(x))
        ax.set_xticklabels([m.replace("bedrock_", "").replace("-arn", "") for m in models],
                          rotation=20, ha="right")
        ax.set_ylim(0, 1.15)
        ax.set_ylabel("Rate")
        ax.set_title("Discovery Metrics (D_ret & D_acc) by Condition × Model")
        ax.legend(loc="upper right", fontsize=8, ncol=2)
        fig.tight_layout()
        fig.savefig(output_dir / "fig2_discovery_metrics.pdf")
        plt.close(fig)
        print("Saved fig2_discovery_metrics.pdf")

    # -----------------------------------------------------------------------
    # Fig 3: EM × D_acc attribution by condition (100% stacked)
    # -----------------------------------------------------------------------
    # Load all traces for failure classification
    all_traces = load_traces(args.traces_dir)

    if records:
        failure_by_cond: dict = defaultdict(lambda: defaultdict(int))
        failure_by_cm: dict = defaultdict(lambda: defaultdict(int))
        totals_by_cm: dict = defaultdict(int)
        task_metrics_by_cm: dict = {}
        for condition_dir in sorted(traces_root.iterdir()):
            if not condition_dir.is_dir():
                continue
            cond_name = condition_dir.name
            for model_dir in sorted(condition_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                model_name = model_dir.name
                cm_key = f"{cond_name}/{model_name}"
                model_traces = load_traces(str(model_dir))
                if not model_traces:
                    continue
                disc = compute_discovery_metrics(model_traces, task_gold)
                task_metrics_by_cm[cm_key] = {
                    m["task_id"]: m for m in disc["task_metrics"]
                }

        for r in records:
            cond = r.get("condition", "?")
            model = r.get("model_label", r.get("model", "?"))
            model_label = model.split("/")[-1].replace("bedrock_", "").replace("-arn", "")
            cm_key = f"{cond}/{model}"
            cm_label = f"{cond}/{model_label}"
            tid = make_task_stem_key(str(r.get("task_id", "")))
            m = task_metrics_by_cm.get(cm_key, {}).get(tid, {})
            label = classify_failure(
                r,
                m.get("d_ret", 0),
                m.get("d_acc", 0),
                num_read_calls=m.get("num_read_calls", 0),
            )
            failure_by_cond[cond][label] += 1
            failure_by_cm[cm_label][label] += 1
            totals_by_cm[cm_label] += 1

        failure_labels = _present_failure_labels(
            failure_by_cm or failure_by_cond,
            list(_LABEL_ORDER),
        )

        conds = sorted(failure_by_cond)

        if conds:
            fig, ax = plt.subplots(figsize=(7, 5))
            bottoms = [0] * len(conds)
            totals_by_cond = {
                cond: sum(failure_by_cond[cond].values())
                for cond in conds
            }
            for cat in failure_labels:
                vals = [
                    100 * failure_by_cond[c].get(cat, 0) / totals_by_cond[c]
                    if totals_by_cond[c] else 0.0
                    for c in conds
                ]
                ax.bar(
                    conds,
                    vals,
                    bottom=bottoms,
                    label=_failure_label_text(cat),
                    color=_FAILURE_COLORS.get(cat, "#CB181D"),
                )
                bottoms = [bottoms[i] + vals[i] for i in range(len(conds))]
            ax.set_ylabel("Tasks (%)")
            ax.set_ylim(0, 100)
            ax.set_title("EM × D_acc Attribution by Condition")
            ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8)
            fig.tight_layout()
            fig.savefig(output_dir / "fig3_failure_breakdown.pdf")
            plt.close(fig)
            print("Saved fig3_failure_breakdown.pdf")

        # -----------------------------------------------------------------------
        # Fig 3b: EM × D_acc attribution by condition × model (heatmap)
        # -----------------------------------------------------------------------
        cm_keys = sorted(failure_by_cm)
        if cm_keys:
            import numpy as np

            matrix = np.zeros((len(failure_labels), len(cm_keys)))
            for i, cat in enumerate(failure_labels):
                for j, cm in enumerate(cm_keys):
                    matrix[i, j] = (
                        100 * failure_by_cm[cm].get(cat, 0) / totals_by_cm[cm]
                        if totals_by_cm[cm] else 0.0
                    )

            fig, ax = plt.subplots(figsize=(max(8, len(cm_keys) * 1.2), max(4.5, len(failure_labels) * 0.75)))
            im = ax.imshow(matrix, aspect="auto", cmap="YlGnBu", vmin=0, vmax=100)
            plt.colorbar(im, ax=ax, label="Tasks (%)")

            ax.set_xticks(range(len(cm_keys)))
            ax.set_xticklabels(cm_keys, rotation=25, ha="right")
            ax.set_yticks(range(len(failure_labels)))
            ax.set_yticklabels([_failure_label_text(label) for label in failure_labels], fontsize=9)
            ax.set_title("EM × D_acc Attribution by Condition × Model")

            for i in range(len(failure_labels)):
                for j in range(len(cm_keys)):
                    val = matrix[i, j]
                    if val <= 0:
                        continue
                    text_color = "white" if val >= 50 else "black"
                    ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7, color=text_color)

            fig.tight_layout()
            fig.savefig(output_dir / "fig3b_failure_by_model.pdf")
            plt.close(fig)
            print("Saved fig3b_failure_by_model.pdf")

    # -----------------------------------------------------------------------
    # Fig 6: Cost vs EM frontier
    # -----------------------------------------------------------------------
    if em_table:
        fig, ax = plt.subplots(figsize=(7, 5))
        for (cond, model), s in em_table.items():
            if s["em"] is not None:
                ax.scatter(s["avg_cost_usd"], s["em"] * 100,
                           label=f"{cond}/{model.split('/')[-1]}", s=80, zorder=3)
                ax.annotate(model.split("/")[-1],
                            (s["avg_cost_usd"], s["em"] * 100),
                            textcoords="offset points", xytext=(5, 3), fontsize=7)
        ax.set_xlabel("Avg Cost per Task (USD)")
        ax.set_ylabel("Exact Match (%)")
        ax.set_title("Cost–Accuracy Frontier")
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(output_dir / "fig6_cost_vs_em.pdf")
        plt.close(fig)
        print("Saved fig6_cost_vs_em.pdf")

    # -----------------------------------------------------------------------
    # Fig 7: Tool latency CDF
    # -----------------------------------------------------------------------
    by_tool: dict = defaultdict(list)
    for t in all_traces.values():
        for trace in t:
            tool = trace.get("tool", "?")
            lat = trace.get("latency_ms", 0)
            by_tool[tool].append(lat)

    if by_tool:
        fig, ax = plt.subplots(figsize=(7, 5))
        for tool, lats in sorted(by_tool.items()):
            sorted_lats = sorted(lats)
            n = len(sorted_lats)
            cdf = [(i + 1) / n for i in range(n)]
            ax.plot(sorted_lats, cdf, label=tool)
        ax.set_xlabel("Latency (ms)")
        ax.set_ylabel("CDF")
        ax.set_title("Tool Call Latency CDF")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fig7_latency_dist.pdf")
        plt.close(fig)
        print("Saved fig7_latency_dist.pdf")

    # -----------------------------------------------------------------------
    # Fig 8: Per-search-tool avg precision & recall — one chart per condition
    # -----------------------------------------------------------------------
    traces_root = Path(args.traces_dir)
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        cond_name = condition_dir.name
        cond_traces: dict = {}
        for model_dir in condition_dir.iterdir():
            if model_dir.is_dir():
                cond_traces.update(load_traces(str(model_dir)))
        if not cond_traces:
            continue
        tools_disc = compute_tools_discovery(cond_traces, task_gold)
        if not tools_disc:
            continue
        tool_names = sorted(tools_disc.keys())
        precisions = [tools_disc[t].get("avg_precision", 0) for t in tool_names]
        recalls = [tools_disc[t].get("avg_recall", 0) for t in tool_names]

        x = range(len(tool_names))
        width = 0.35
        fig, ax = plt.subplots(figsize=(max(6, len(tool_names) * 1.5), 5))
        bars_p = ax.bar([xi - width / 2 for xi in x], precisions, width, label="Avg Precision", color="steelblue")
        bars_r = ax.bar([xi + width / 2 for xi in x], recalls, width, label="Avg Recall", color="coral")
        for bar in list(bars_p) + list(bars_r):
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01,
                        f"{h:.2f}", ha="center", va="bottom", fontsize=8)
        ax.set_xticks(list(x))
        ax.set_xticklabels(tool_names, rotation=20, ha="right")
        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Score")
        ax.set_title(f"Search Tool Precision & Recall — Condition {cond_name.upper()}")
        ax.legend()
        fig.tight_layout()
        fname = f"fig8_{cond_name}_tool_precision_recall.pdf"
        fig.savefig(output_dir / fname)
        plt.close(fig)
        print(f"Saved {fname}")

    # -----------------------------------------------------------------------
    # Fig 8b: Per-search-tool precision & recall — per condition × model
    # -----------------------------------------------------------------------
    for condition_dir in sorted(traces_root.iterdir()):
        if not condition_dir.is_dir():
            continue
        cond_name = condition_dir.name
        for model_dir in condition_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model_name = model_dir.name.replace("bedrock_", "").replace("-arn", "")
            cm_traces = load_traces(str(model_dir))
            if not cm_traces:
                continue
            tools_disc = compute_tools_discovery(cm_traces, task_gold)
            if not tools_disc:
                continue
            tool_names = sorted(tools_disc.keys())
            precisions = [tools_disc[t].get("avg_precision", 0) for t in tool_names]
            recalls = [tools_disc[t].get("avg_recall", 0) for t in tool_names]

            x = range(len(tool_names))
            width = 0.35
            fig, ax = plt.subplots(figsize=(max(6, len(tool_names) * 1.5), 5))
            bars_p = ax.bar([xi - width / 2 for xi in x], precisions, width, label="Avg Precision", color="steelblue")
            bars_r = ax.bar([xi + width / 2 for xi in x], recalls, width, label="Avg Recall", color="coral")
            for bar in list(bars_p) + list(bars_r):
                h = bar.get_height()
                if h > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01,
                            f"{h:.2f}", ha="center", va="bottom", fontsize=8)
            ax.set_xticks(list(x))
            ax.set_xticklabels(tool_names, rotation=20, ha="right")
            ax.set_ylim(0, 1.1)
            ax.set_ylabel("Score")
            ax.set_title(f"Search Tool Precision & Recall — {cond_name.upper()}/{model_name}")
            ax.legend()
            fig.tight_layout()
            fname = f"fig8b_{cond_name}_{model_name}_tool_precision_recall.pdf"
            fig.savefig(output_dir / fname)
            plt.close(fig)
            print(f"Saved {fname}")

    # -----------------------------------------------------------------------
    # Fig 9: Avg search calls per condition × model
    # -----------------------------------------------------------------------
    if em_table:
        conditions = sorted(set(k[0] for k in em_table))
        models = sorted(set(k[1] for k in em_table))
        search_calls_data = {k: v.get("avg_search_calls", 0) or 0 for k, v in em_table.items()}

        if any(search_calls_data.values()):
            x = range(len(models))
            width = 0.8 / max(len(conditions), 1)
            fig, ax = plt.subplots(figsize=(9, 5))
            for i, cond in enumerate(conditions):
                vals = [search_calls_data.get((cond, m), 0) for m in models]
                offset = (i - len(conditions) / 2 + 0.5) * width
                bars = ax.bar([xi + offset for xi in x], vals, width=width * 0.9, label=f"Condition {cond}")
                for bar, val in zip(bars, vals):
                    if val:
                        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                                f"{val:.1f}", ha="center", va="bottom", fontsize=8)
            ax.set_xticks(list(x))
            ax.set_xticklabels([m.split("/")[-1] for m in models], rotation=20, ha="right")
            ax.set_ylabel("Avg Search Calls per Task")
            ax.set_title("Search Calls by Condition × Model")
            ax.legend()
            fig.tight_layout()
            fig.savefig(output_dir / "fig9_search_calls.pdf")
            plt.close(fig)
            print("Saved fig9_search_calls.pdf")

    # -----------------------------------------------------------------------
    # Fig 10: Search depth curve — EM% vs search-call bin per condition
    # -----------------------------------------------------------------------
    repo_root2 = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_root2))
    from analysis.search_depth import compute_search_depth_curve
    depth_records = load_results(args.results_dir)
    depth_curve = compute_search_depth_curve(depth_records)

    if depth_curve:
        bin_labels = ["1", "2-3", "4-6", "7-10", "11-30"]
        fig, ax = plt.subplots(figsize=(8, 5))
        for cond, bins in sorted(depth_curve.items()):
            xs = []
            ys = []
            for i, label in enumerate(bin_labels):
                entry = bins.get(label, {})
                em = entry.get("mean_em")
                n = entry.get("n", 0)
                if em is not None and n > 0:
                    xs.append(i)
                    ys.append(em * 100)
            if xs:
                ax.plot(xs, ys, marker="o", label=f"Condition {cond}")
                for xi, yi in zip(xs, ys):
                    ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                                xytext=(0, 6), ha="center", fontsize=8)
        ax.set_xticks(range(len(bin_labels)))
        ax.set_xticklabels(bin_labels)
        ax.set_xlabel("Search Calls per Task")
        ax.set_ylabel("Mean EM (%)")
        ax.set_title("Search Depth Curve — EM vs. Search Call Budget Used")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fig10_search_depth_curve.pdf")
        plt.close(fig)
        print("Saved fig10_search_depth_curve.pdf")

    # -----------------------------------------------------------------------
    # Fig 10b: Search depth curve per model within each condition
    # -----------------------------------------------------------------------
    from analysis.search_depth import _assign_bin, _BINS
    # Group records by (condition, model)
    records_by_cm: dict = defaultdict(list)
    for r in depth_records:
        cond = r.get("condition", "?")
        model = r.get("model", "?").split("/")[-1].replace("bedrock_", "").replace("-arn", "")
        records_by_cm[(cond, model)].append(r)

    for (cond, model), cm_records in sorted(records_by_cm.items()):
        # Compute search depth curve for this (condition, model)
        bin_data: dict = defaultdict(list)
        for r in cm_records:
            em = r.get("exact_match")
            if em is None:
                continue
            search_calls = _count_search_calls(r)
            bin_label = _assign_bin(search_calls)
            bin_data[bin_label].append(float(em))

        if not bin_data:
            continue

        bin_labels = [label for label, _ in _BINS]
        xs = []
        ys = []
        for i, label in enumerate(bin_labels):
            vals = bin_data.get(label, [])
            if vals:
                xs.append(i)
                ys.append(sum(vals) / len(vals) * 100)

        if xs:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(xs, ys, marker="o", color="steelblue")
            for xi, yi in zip(xs, ys):
                ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                            xytext=(0, 6), ha="center", fontsize=8)
            ax.set_xticks(range(len(bin_labels)))
            ax.set_xticklabels(bin_labels)
            ax.set_xlabel("Search Calls per Task")
            ax.set_ylabel("Mean EM (%)")
            ax.set_title(f"Search Depth Curve — {cond.upper()}/{model}")
            fig.tight_layout()
            fname = f"fig10b_{cond}_{model}_search_depth.pdf"
            fig.savefig(output_dir / fname)
            plt.close(fig)
            print(f"Saved {fname}")

    # -----------------------------------------------------------------------
    # Fig 11: Planning overhead — Condition B dual-axis (EM% + output tokens vs cycle bin)
    # -----------------------------------------------------------------------
    from analysis.planning_overhead import compute_planning_overhead
    planning = compute_planning_overhead(depth_records)

    if planning.get("n_cond_b", 0) > 0:
        cycle_bin_labels = ["1-3", "4-6", "7-10", "11+"]
        by_bin = planning["by_bin"]
        xs = []
        em_ys = []
        tok_ys = []
        for i, label in enumerate(cycle_bin_labels):
            entry = by_bin.get(label, {})
            em = entry.get("mean_em")
            tok = entry.get("mean_output_tokens")
            n = entry.get("n", 0)
            if em is not None and n > 0:
                xs.append(i)
                em_ys.append(em * 100)
                tok_ys.append(tok if tok is not None else 0)

        if xs:
            fig, ax1 = plt.subplots(figsize=(8, 5))
            ax2 = ax1.twinx()
            ax1.plot(xs, em_ys, marker="o", color="steelblue", label="Mean EM%")
            ax2.plot(xs, tok_ys, marker="s", color="coral", linestyle="--", label="Mean Output Tokens")
            ax1.set_xticks(range(len(cycle_bin_labels)))
            ax1.set_xticklabels(cycle_bin_labels)
            ax1.set_xlabel("Cycle Count Bin (planning proxy)")
            ax1.set_ylabel("Mean EM (%)", color="steelblue")
            ax2.set_ylabel("Mean Output Tokens", color="coral")
            ax1.set_title(
                f"Planning Overhead — Condition B  "
                f"(r={planning['pearson_cycle_em']}, n={planning['n_cond_b']})"
            )
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
            fig.tight_layout()
            fig.savefig(output_dir / "fig11_planning_overhead.pdf")
            plt.close(fig)
            print("Saved fig11_planning_overhead.pdf")

    # -----------------------------------------------------------------------
    # Fig 12: EM by reasoning density (gold-doc count) — reproduces LakeQA Fig 4
    # -----------------------------------------------------------------------
    from analysis.reasoning_density import compute_reasoning_density_curve, load_task_gold_counts
    task_gold_counts = load_task_gold_counts(args.tasks_dir)
    density_curve = compute_reasoning_density_curve(depth_records, task_gold_counts)

    if density_curve:
        bin_labels = ["<=2", "3-4", "5-7", "8-10", ">10"]
        fig, ax = plt.subplots(figsize=(8, 5))
        for cond, bins in sorted(density_curve.items()):
            xs = []
            ys = []
            for i, label in enumerate(bin_labels):
                entry = bins.get(label, {})
                em = entry.get("mean_em")
                n = entry.get("n", 0)
                if em is not None and n > 0:
                    xs.append(i)
                    ys.append(em * 100)
            if xs:
                ax.plot(xs, ys, marker="o", label=f"Condition {cond}")
                for xi, yi in zip(xs, ys):
                    ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                                xytext=(0, 6), ha="center", fontsize=8)
        ax.set_xticks(range(len(bin_labels)))
        ax.set_xticklabels(bin_labels)
        ax.set_xlabel("Number of Gold Documents per Task")
        ax.set_ylabel("Mean EM (%)")
        ax.set_title("EM vs. Reasoning Density (LakeQA Fig 4 reproduction)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fig12_reasoning_density.pdf")
        plt.close(fig)
        print("Saved fig12_reasoning_density.pdf")

    # -----------------------------------------------------------------------
    # Fig 12b: Reasoning density per model within each condition
    # -----------------------------------------------------------------------
    from analysis.reasoning_density import _assign_bin as _assign_density_bin, _BINS as _DENSITY_BINS

    for (cond, model), cm_records in sorted(records_by_cm.items()):
        # Compute reasoning density curve for this (condition, model)
        bin_data: dict = defaultdict(list)
        for r in cm_records:
            em = r.get("exact_match")
            if em is None:
                continue
            task_id = str(r.get("task_id", ""))
            p = Path(task_id)
            key = f"{p.parent.name}/{p.stem}"
            n_docs = task_gold_counts.get(key)
            if n_docs is None:
                continue
            bin_label = _assign_density_bin(n_docs)
            bin_data[bin_label].append(float(em))

        if not bin_data:
            continue

        density_bin_labels = [label for label, _ in _DENSITY_BINS]
        xs = []
        ys = []
        for i, label in enumerate(density_bin_labels):
            vals = bin_data.get(label, [])
            if vals:
                xs.append(i)
                ys.append(sum(vals) / len(vals) * 100)

        if xs:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(xs, ys, marker="o", color="steelblue")
            for xi, yi in zip(xs, ys):
                ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                            xytext=(0, 6), ha="center", fontsize=8)
            ax.set_xticks(range(len(density_bin_labels)))
            ax.set_xticklabels(density_bin_labels)
            ax.set_xlabel("Number of Gold Documents per Task")
            ax.set_ylabel("Mean EM (%)")
            ax.set_title(f"EM vs. Reasoning Density — {cond.upper()}/{model}")
            fig.tight_layout()
            fname = f"fig12b_{cond}_{model}_reasoning_density.pdf"
            fig.savefig(output_dir / fname)
            plt.close(fig)
            print(f"Saved {fname}")

    # -----------------------------------------------------------------------
    # Fig 13: Tool error rate heatmap — rows=tools, cols=condition×model
    # -----------------------------------------------------------------------
    from analysis.tool_error_analysis import compute_tool_error_rates, _DATA_TOOLS
    error_rates = compute_tool_error_rates(depth_records)

    if error_rates:
        import numpy as np
        all_tools = sorted(
            {t for cm_data in error_rates.values() for t in cm_data if t in _DATA_TOOLS}
        )
        cm_keys = sorted(error_rates.keys())

        if all_tools and cm_keys:
            matrix = np.zeros((len(all_tools), len(cm_keys)))
            for j, cm in enumerate(cm_keys):
                for i, tool in enumerate(all_tools):
                    matrix[i, j] = error_rates[cm].get(tool, {}).get("error_rate", 0.0) * 100

            fig, ax = plt.subplots(figsize=(max(6, len(cm_keys) * 2), max(4, len(all_tools) * 0.7)))
            im = ax.imshow(matrix, aspect="auto", cmap="Reds", vmin=0, vmax=50)
            plt.colorbar(im, ax=ax, label="Error Rate (%)")

            ax.set_xticks(range(len(cm_keys)))
            ax.set_xticklabels([k.replace("bedrock_", "") for k in cm_keys], rotation=30, ha="right", fontsize=8)
            ax.set_yticks(range(len(all_tools)))
            ax.set_yticklabels(all_tools, fontsize=9)

            # Annotate cells
            for i in range(len(all_tools)):
                for j in range(len(cm_keys)):
                    val = matrix[i, j]
                    color = "white" if val > 25 else "black"
                    ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=8, color=color)

            ax.set_title("Tool Error Rates by Condition × Model (%)")
            fig.tight_layout()
            fig.savefig(output_dir / "fig13_tool_error_rates.pdf")
            plt.close(fig)
            print("Saved fig13_tool_error_rates.pdf")

    print(f"\nAll figures saved to {output_dir}/")


if __name__ == "__main__":
    main()
