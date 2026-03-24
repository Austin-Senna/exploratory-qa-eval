#!/usr/bin/env python3
"""
Generate all paper figures using matplotlib/seaborn.

Figures produced:
  fig1_em_comparison.pdf     — EM rate by condition × model (grouped bar)
  fig2_discovery_metrics.pdf — D_ret vs D_acc by condition
  fig3_failure_breakdown.pdf — Stacked bar: failure attribution per condition
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
import json
import sys
from collections import defaultdict
from pathlib import Path


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

    from analysis.compute_em import load_results, compute_stats
    from analysis.discovery_metrics import (
        load_traces, load_task_gold_ids, compute_discovery_metrics, compute_tools_discovery
    )

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
    # Fig 2: D_ret vs D_acc by condition
    # -----------------------------------------------------------------------
    traces = load_traces(args.traces_dir)
    task_gold = load_task_gold_ids(args.tasks_dir)
    disc = compute_discovery_metrics(traces, task_gold)

    if disc["aggregate"]:
        agg = disc["aggregate"]
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.bar(["D_ret", "D_acc"], [agg["D_ret"], agg["D_acc"]], color=["steelblue", "coral"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Rate")
        ax.set_title("Discovery Metrics")
        for i, v in enumerate([agg["D_ret"], agg["D_acc"]]):
            ax.text(i, v + 0.02, f"{v:.3f}", ha="center")
        fig.tight_layout()
        fig.savefig(output_dir / "fig2_discovery_metrics.pdf")
        plt.close(fig)
        print("Saved fig2_discovery_metrics.pdf")

    # -----------------------------------------------------------------------
    # Fig 3: Failure attribution stacked bar
    # -----------------------------------------------------------------------
    if records:
        from analysis.failure_attribution import classify_failure

        failure_by_cond: dict = defaultdict(lambda: defaultdict(int))
        task_metrics_by_id = {m["task_id"]: m for m in disc["task_metrics"]}
        for r in records:
            cond = r.get("condition", "?")
            tid = str(r.get("task_id", ""))
            m = task_metrics_by_id.get(tid, {})
            label = classify_failure(r, m.get("d_ret", 0), m.get("d_acc", 0))
            failure_by_cond[cond][label] += 1

        categories = ["correct", "search", "discovery-reason", "execution", "hallucination"]
        colors = ["#2ecc71", "#e74c3c", "#e67e22", "#3498db", "#9b59b6"]
        conds = sorted(failure_by_cond)

        if conds:
            fig, ax = plt.subplots(figsize=(7, 5))
            bottoms = [0] * len(conds)
            for cat, color in zip(categories, colors):
                vals = [failure_by_cond[c].get(cat, 0) for c in conds]
                ax.bar(conds, vals, bottom=bottoms, label=cat, color=color)
                bottoms = [bottoms[i] + vals[i] for i in range(len(conds))]
            ax.set_ylabel("Number of Tasks")
            ax.set_title("Failure Attribution by Condition")
            ax.legend(loc="upper right")
            fig.tight_layout()
            fig.savefig(output_dir / "fig3_failure_breakdown.pdf")
            plt.close(fig)
            print("Saved fig3_failure_breakdown.pdf")

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
    for t in traces.values():
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
    # Fig 8: Per-search-tool avg precision & recall
    # -----------------------------------------------------------------------
    tools_disc = compute_tools_discovery(traces, task_gold)
    if tools_disc:
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
        ax.set_title("Search Tool Precision & Recall")
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fig8_tool_precision_recall.pdf")
        plt.close(fig)
        print("Saved fig8_tool_precision_recall.pdf")

    print(f"\nAll figures saved to {output_dir}/")


if __name__ == "__main__":
    main()
