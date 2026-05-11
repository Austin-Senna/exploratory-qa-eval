#!/usr/bin/env python3
"""
Generate all paper figures using matplotlib/seaborn.

Figures produced:
  fig2a_recall_em_combined.pdf — D_ret recall, D_acc recall, and EM
  fig3c_failure_deciles.pdf — EM × D_acc decile attribution
  fig3d_failure_deciles_dret.pdf — EM × D_ret decile attribution
  fig4_backend_provenance.pdf — Condition A: first-hit backend pie chart
  fig5_query_drift.pdf        — Condition B: Jaccard similarity distribution
  fig6_cost_vs_em.pdf         — Cost-accuracy frontier scatter
  fig7_latency_dist.pdf       — Tool call latency CDF by backend
  fig8_search_tool_precision_recall_f1.pdf — Per-search-tool avg precision, recall, and F1

Usage:
    python analysis/generate_figures.py [--results-dir results] [--sidecar-dir results/sidecar]
                                        [--tasks-dir tasks_mini] [--output-dir figures]
"""
import argparse
import re
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


def _short_model_label(model_name: str) -> str:
    return _pretty_model(model_name)


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return slug or "unknown"


def _pretty_model(model: str) -> str:
    """Strip provider prefixes/suffixes from a model dir name."""
    m = model.split("/")[-1]
    m = m.replace("bedrock_", "").replace("openai_", "")
    if m.endswith("-arn"):
        m = m[:-4]
    return m


_BASE_RENAMES = {"b_plan_soft": "b"}


def _rename_base(b: str) -> str:
    return _BASE_RENAMES.get(b, b)


def _pretty_condition(cond: str) -> str:
    """`naive_k5__baseline` -> `baseline/naive_k5`. Plain conditions pass through.
    Also collapses renamed base conditions (e.g. b_plan_soft -> b)."""
    if "__" in cond:
        variant, base = cond.split("__", 1)
        return f"{_rename_base(base)}/{variant}"
    return _rename_base(cond)


def _pretty_cm(cond: str, model: str) -> str:
    return f"{_pretty_model(model)}/{_pretty_condition(cond)}"


def _condition_sort_key(cond: str) -> tuple:
    """Sort by (base_condition, variant_family, k). Plain conditions sort first."""
    if "__" in cond:
        variant, base = cond.split("__", 1)
    else:
        variant, base = "", cond
    base = _rename_base(base)
    family = ""
    k = 0
    if variant:
        if "_k" in variant:
            family, _, ksuf = variant.rpartition("_k")
            try:
                k = int(re.match(r"\d+", ksuf).group()) if ksuf else 0
            except (ValueError, AttributeError):
                k = 0
        else:
            family = variant
    return (base, family, k)


def _cm_sort_key(cond: str, model: str) -> tuple:
    return _condition_sort_key(cond) + (_pretty_model(model),)


def _has_trace_dirs(root: Path) -> bool:
    return root.exists() and any(root.iterdir())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--traces-dir", default="results/traces")
    parser.add_argument("--tasks-dir", default="tasks_mini")
    parser.add_argument("--output-dir", default="analysis_results/figures")
    parser.add_argument(
        "--model-filter",
        default=None,
        help="Substring filter on model label; only models whose label contains this are included. "
             "Repeat with commas for OR (e.g. 'haiku,sonnet').",
    )
    args = parser.parse_args()

    model_filters = [s.strip().lower() for s in args.model_filter.split(",")] if args.model_filter else None

    def _keep_model(model_label: str) -> bool:
        if not model_filters:
            return True
        m = (model_label or "").lower()
        return any(f in m for f in model_filters)

    plt, sns = _import_plot_libs()
    sns.set_theme(style="whitegrid", palette="muted")

    repo_root = Path(__file__).parent.parent
    sys.path.insert(0, str(repo_root))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    traces_root = Path(args.traces_dir)
    traces_available = _has_trace_dirs(traces_root)
    # Remove stale legacy outputs that are no longer generated.
    stale_patterns = [
        "fig1_em_comparison.pdf",
        "fig2_discovery_metrics.pdf",
        "fig2b*.pdf",
        "fig2c*.pdf",
        "fig3_failure_breakdown.pdf",
        "fig8_search_tool_precision_recall.pdf",
    ]
    for pattern in stale_patterns:
        for stale in output_dir.glob(pattern):
            stale.unlink(missing_ok=True)

    from analysis.compute_em import load_results, compute_stats, _count_search_calls
    from analysis.discovery_metrics import (
        load_traces, load_task_gold_ids, compute_discovery_metrics, compute_tools_discovery, make_task_stem_key
    )
    from analysis.failure_attribution import classify_failure
    from analysis.failure_attribution_deciles import (
        _LABEL_ORDER as _DECILE_LABEL_ORDER,
        classify_failure_decile,
    )

    records = load_results(args.results_dir)
    if model_filters:
        records = [r for r in records if _keep_model(r.get("model_label", r.get("model", "")))]
    em_table = compute_stats(records)

    # -----------------------------------------------------------------------
    # Discovery aggregates used by Fig 2a / 2b.
    # -----------------------------------------------------------------------
    task_gold = load_task_gold_ids(args.tasks_dir)

    # Collect discovery aggregates per (condition, model)
    discovery_by_cm: dict = {}
    if traces_available:
        for condition_dir in sorted(traces_root.iterdir()):
            if not condition_dir.is_dir():
                continue
            cond_name = condition_dir.name
            for model_dir in condition_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                model_name = model_dir.name
                if not _keep_model(model_name):
                    continue
                cond_traces = load_traces(str(model_dir))
                if cond_traces:
                    disc = compute_discovery_metrics(cond_traces, task_gold)
                    if disc["aggregate"]:
                        discovery_by_cm[(cond_name, model_name)] = disc["aggregate"]

    if discovery_by_cm:
        conditions = sorted(set(k[0] for k in discovery_by_cm), key=_condition_sort_key)
        models = sorted(set(k[1] for k in discovery_by_cm))

        # -------------------------------------------------------------------
        # Fig 2a: Combined D_ret recall + D_acc recall + EM per condition × model
        # -------------------------------------------------------------------
        cm_pairs = sorted(discovery_by_cm.keys(), key=lambda cm: _cm_sort_key(*cm))
        if cm_pairs:
            labels = [_pretty_cm(c, m) for (c, m) in cm_pairs]
            d_ret_vals = [float(discovery_by_cm[(c, m)].get("D_ret", 0) or 0) for (c, m) in cm_pairs]
            d_acc_vals = [
                float(discovery_by_cm[(c, m)].get("D_acc_recall", discovery_by_cm[(c, m)].get("D_acc", 0)) or 0)
                for (c, m) in cm_pairs
            ]
            em_vals = [
                (em_table.get((c, m), {}).get("em") or 0.0)
                for (c, m) in cm_pairs
            ]

            x = list(range(len(labels)))
            width = 0.27
            fig, ax = plt.subplots(figsize=(max(8, len(labels) * 1.1), 5.5))
            b1 = ax.bar([xi - width for xi in x], d_ret_vals, width, label="D_ret recall", color="steelblue")
            b2 = ax.bar(x, d_acc_vals, width, label="D_acc recall", color="mediumseagreen")
            b3 = ax.bar([xi + width for xi in x], em_vals, width, label="EM", color="coral")
            for bar_group in (b1, b2, b3):
                for bar in bar_group:
                    h = bar.get_height()
                    if h > 0:
                        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01,
                                f"{h:.2f}", ha="center", va="bottom", fontsize=7, rotation=45)

            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=8)
            ax.set_ylim(0, 1.15)
            ax.set_ylabel("Score")
            ax.set_title("Discovery Recall & EM by Condition × Model")
            ax.legend(loc="upper right", fontsize=9)
            fig.tight_layout()
            fig.savefig(output_dir / "fig2a_recall_em_combined.pdf")
            plt.close(fig)
            print("Saved fig2a_recall_em_combined.pdf")

    # -----------------------------------------------------------------------
    # Fig 3: EM × D_acc attribution by condition (100% stacked)
    # -----------------------------------------------------------------------
    # Load all traces for failure classification
    all_traces = load_traces(args.traces_dir) if traces_available else {}

    if records:
        failure_by_cond: dict = defaultdict(lambda: defaultdict(int))
        failure_by_cm: dict = defaultdict(lambda: defaultdict(int))
        totals_by_cm: dict = defaultdict(int)
        decile_by_cond: dict = defaultdict(lambda: defaultdict(int))
        decile_by_cm: dict = defaultdict(lambda: defaultdict(int))
        dret_decile_by_cond: dict = defaultdict(lambda: defaultdict(int))
        dret_decile_by_cm: dict = defaultdict(lambda: defaultdict(int))
        task_metrics_by_cm: dict = {}
        if traces_available:
            for condition_dir in sorted(traces_root.iterdir()):
                if not condition_dir.is_dir():
                    continue
                cond_name = condition_dir.name
                for model_dir in sorted(condition_dir.iterdir()):
                    if not model_dir.is_dir():
                        continue
                    model_name = model_dir.name
                    if not _keep_model(model_name):
                        continue
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
            d_label = classify_failure_decile(r, m.get("d_acc", 0))
            decile_by_cond[cond][d_label] += 1
            decile_by_cm[cm_label][d_label] += 1
            dret_label = classify_failure_decile(r, m.get("d_ret", 0))
            dret_decile_by_cond[cond][dret_label] += 1
            dret_decile_by_cm[cm_label][dret_label] += 1

        # -----------------------------------------------------------------------
        # Fig 3c / 3d helpers
        # -----------------------------------------------------------------------
        import matplotlib.cm as _mcm
        em1_labels = [l for l in _DECILE_LABEL_ORDER if l.startswith("em1_")]
        em0_labels = [l for l in _DECILE_LABEL_ORDER if l.startswith("em0_")]
        greens = _mcm.get_cmap("Greens")
        reds = _mcm.get_cmap("Reds")
        decile_colors = {
            **{l: greens(0.25 + 0.07 * i) for i, l in enumerate(em1_labels)},
            **{l: reds(0.25 + 0.07 * i) for i, l in enumerate(em0_labels)},
        }

        def _decile_legend(label: str, metric: str) -> str:
            em_part, _, rest = label.partition("_dacc_")
            em_val = em_part.replace("em", "")
            low_a, low_b, _, hi_a, hi_b = rest.split("_")
            low = f"{low_a}.{low_b}"
            high = f"{hi_a}.{hi_b}"
            return f"EM={em_val}  {metric} [{low}–{high})"

        def _cm_label_sort(cm_label: str) -> tuple:
            if "/" in cm_label:
                cond, model = cm_label.split("/", 1)
                return _cm_sort_key(cond, model)
            return (cm_label, "", 0, "")

        def _draw_decile_stack(by_cm: dict, metric: str, fname: str, title: str) -> None:
            keys = sorted(by_cm.keys(), key=_cm_label_sort)
            if not keys:
                return
            pretty = [
                _pretty_cm(*k.split("/", 1)) if "/" in k else k for k in keys
            ]
            fig, ax = plt.subplots(figsize=(max(8, len(keys) * 0.9), 5.5))
            bottoms = [0.0] * len(keys)
            totals = {k: sum(by_cm[k].values()) for k in keys}
            x = list(range(len(keys)))
            for cat in _DECILE_LABEL_ORDER:
                vals = [
                    100 * by_cm[k].get(cat, 0) / totals[k] if totals[k] else 0.0
                    for k in keys
                ]
                if not any(vals):
                    continue
                ax.bar(
                    x,
                    vals,
                    bottom=bottoms,
                    label=_decile_legend(cat, metric),
                    color=decile_colors[cat],
                )
                bottoms = [bottoms[i] + vals[i] for i in range(len(keys))]
            ax.set_xticks(x)
            ax.set_xticklabels(pretty, rotation=25, ha="right", fontsize=8)
            ax.set_ylabel("Tasks (%)")
            ax.set_ylim(0, 100)
            ax.set_title(title)
            ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=7, ncol=1)
            fig.tight_layout(rect=(0, 0, 0.78, 1))
            fig.savefig(output_dir / fname)
            plt.close(fig)
            print(f"Saved {fname}")

        # -----------------------------------------------------------------------
        # Fig 3c: EM × D_acc decile attribution by condition × model
        # -----------------------------------------------------------------------
        _draw_decile_stack(
            decile_by_cm,
            "D_acc",
            "fig3c_failure_deciles.pdf",
            "EM × D_acc Decile Attribution by Condition × Model",
        )

        # -----------------------------------------------------------------------
        # Fig 3d: EM × D_ret decile attribution by condition × model
        # -----------------------------------------------------------------------
        _draw_decile_stack(
            dret_decile_by_cm,
            "D_ret",
            "fig3d_failure_deciles_dret.pdf",
            "EM × D_ret Decile Attribution by Condition × Model",
        )

    # -----------------------------------------------------------------------
    # Fig 6: Cost vs EM frontier
    # -----------------------------------------------------------------------
    if em_table:
        fig, ax = plt.subplots(figsize=(7, 5))
        for (cond, model), s in em_table.items():
            if s["em"] is not None:
                avg_cost = s.get("avg_total_cost_with_ideal_subagents_usd", s["avg_cost_usd"])
                ax.scatter(avg_cost, s["em"] * 100,
                           label=_pretty_cm(cond, model), s=80, zorder=3)
                ax.annotate(model.split("/")[-1],
                            (avg_cost, s["em"] * 100),
                            textcoords="offset points", xytext=(5, 3), fontsize=7)
        ax.set_xlabel("Avg Cost per Task incl. Ideal Subagents (USD)")
        ax.set_ylabel("Exact Match (%)")
        ax.set_title("Cost–Accuracy Frontier")
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=7)
        fig.tight_layout(rect=(0, 0, 0.82, 1))
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
    # Fig 8: Search-tool precision, recall, and F1
    # -----------------------------------------------------------------------
    tool_metrics: dict = defaultdict(lambda: {"weight": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0})
    if traces_available:
        for condition_dir in sorted(traces_root.iterdir()):
            if not condition_dir.is_dir():
                continue
            cond_name = condition_dir.name
            for model_dir in sorted(condition_dir.iterdir()):
                if not model_dir.is_dir() or not _keep_model(model_dir.name):
                    continue
                cm_traces = load_traces(str(model_dir))
                if not cm_traces:
                    continue
                tools_disc = compute_tools_discovery(cm_traces, task_gold)
                if not tools_disc:
                    continue
                # Aggregate over search tools only (exclude read tools, submit_answer)
                search_tool_names = [t for t in tools_disc if t.startswith("search")]
                if not search_tool_names:
                    search_tool_names = list(tools_disc.keys())
                for tool_name in search_tool_names:
                    stats = tools_disc[tool_name]
                    weight = float(stats.get("n_tasks", 0) or stats.get("calls", 0) or 1)
                    bucket = tool_metrics[tool_name]
                    bucket["weight"] += weight
                    bucket["precision"] += float(stats.get("avg_precision", 0) or 0) * weight
                    bucket["recall"] += float(stats.get("avg_recall", 0) or 0) * weight
                    bucket["f1"] += float(stats.get("avg_f1", 0) or 0) * weight

    if tool_metrics:
        labels = sorted(tool_metrics)
        rows = []
        for tool_name in labels:
            weight = tool_metrics[tool_name]["weight"]
            rows.append(
                {
                    "tool": tool_name,
                    "precision": tool_metrics[tool_name]["precision"] / weight if weight else 0.0,
                    "recall": tool_metrics[tool_name]["recall"] / weight if weight else 0.0,
                    "f1": tool_metrics[tool_name]["f1"] / weight if weight else 0.0,
                }
            )
        x = list(range(len(rows)))
        fields = [
            ("precision", "Avg Precision", "steelblue"),
            ("recall", "Avg Recall", "coral"),
            ("f1", "Avg F1", "mediumseagreen"),
        ]
        width = 0.8 / len(fields)
        fig, ax = plt.subplots(figsize=(max(8, len(rows) * 1.2), 5))
        for idx, (field, label, color) in enumerate(fields):
            values = [row[field] for row in rows]
            offset = (idx - len(fields) / 2 + 0.5) * width
            bars = ax.bar([xi + offset for xi in x], values, width * 0.9, label=label, color=color)
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01,
                            f"{h:.2f}", ha="center", va="bottom", fontsize=7)
        ax.set_xticks(x)
        ax.set_xticklabels([row["tool"] for row in rows], rotation=25, ha="right", fontsize=8)
        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Average Score")
        ax.set_title("Search Tool Precision, Recall, and F1")
        ax.legend(loc="upper right")
        fig.tight_layout()
        fig.savefig(output_dir / "fig8_search_tool_precision_recall_f1.pdf")
        plt.close(fig)
        print("Saved fig8_search_tool_precision_recall_f1.pdf")

    # -----------------------------------------------------------------------
    # Fig 9: Avg search calls per condition × model
    # -----------------------------------------------------------------------
    if em_table:
        conditions = sorted(set(k[0] for k in em_table), key=_condition_sort_key)
        models = sorted(set(k[1] for k in em_table))
        search_calls_data = {k: v.get("avg_search_calls", 0) or 0 for k, v in em_table.items()}

        if any(search_calls_data.values()):
            x = range(len(models))
            width = 0.8 / max(len(conditions), 1)
            fig, ax = plt.subplots(figsize=(9, 5))
            for i, cond in enumerate(conditions):
                vals = [search_calls_data.get((cond, m), 0) for m in models]
                offset = (i - len(conditions) / 2 + 0.5) * width
                bars = ax.bar([xi + offset for xi in x], vals, width=width * 0.9, label=_pretty_condition(cond))
                for bar, val in zip(bars, vals):
                    if val:
                        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                                f"{val:.1f}", ha="center", va="bottom", fontsize=8)
            ax.set_xticks(list(x))
            ax.set_xticklabels([_pretty_model(m) for m in models], rotation=20, ha="right")
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
    if model_filters:
        depth_records = [r for r in depth_records if _keep_model(r.get("model_label", r.get("model", "")))]
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
                ax.plot(xs, ys, marker="o", label=_pretty_condition(cond))
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
        model = _pretty_model(r.get("model_label", r.get("model", "?")))
        records_by_cm[(cond, model)].append(r)


    # -----------------------------------------------------------------------
    # Fig 10b: Search depth curve per model (one line per condition)
    # -----------------------------------------------------------------------
    by_model: dict = defaultdict(dict)  # model -> cond -> [(bin_label, em)]
    for (cond, model), cm_records in sorted(records_by_cm.items()):
        bin_data: dict = defaultdict(list)
        for r in cm_records:
            em = r.get("exact_match")
            if em is None:
                continue
            search_calls = _count_search_calls(r)
            bin_data[_assign_bin(search_calls)].append(float(em))
        if bin_data:
            by_model[model][cond] = bin_data

    bin_labels_sd = [label for label, _ in _BINS]
    for model, cond_map in sorted(by_model.items()):
        fig, ax = plt.subplots(figsize=(8, 5))
        for cond, bin_data in sorted(cond_map.items()):
            xs, ys = [], []
            for i, label in enumerate(bin_labels_sd):
                vals = bin_data.get(label, [])
                if vals:
                    xs.append(i)
                    ys.append(sum(vals) / len(vals) * 100)
            if xs:
                ax.plot(xs, ys, marker="o", label=_pretty_condition(cond))
        ax.set_xticks(range(len(bin_labels_sd)))
        ax.set_xticklabels(bin_labels_sd)
        ax.set_xlabel("Search Calls per Task")
        ax.set_ylabel("Mean EM (%)")
        ax.set_title(f"Search Depth Curve — {_pretty_model(model)}")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fname = f"fig10b_{_safe_slug(_pretty_model(model))}_search_depth.pdf"
        fig.savefig(output_dir / fname)
        plt.close(fig)
        print(f"Saved {fname}")

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
                ax.plot(xs, ys, marker="o", label=_pretty_condition(cond))
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
    # Fig 12b: Reasoning density per model (one line per condition)
    # -----------------------------------------------------------------------
    from analysis.reasoning_density import _assign_bin as _assign_density_bin, _BINS as _DENSITY_BINS

    rd_by_model: dict = defaultdict(dict)  # model -> cond -> bin_data
    for (cond, model), cm_records in sorted(records_by_cm.items()):
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
            bin_data[_assign_density_bin(n_docs)].append(float(em))
        if bin_data:
            rd_by_model[model][cond] = bin_data

    density_bin_labels = [label for label, _ in _DENSITY_BINS]
    for model, cond_map in sorted(rd_by_model.items()):
        fig, ax = plt.subplots(figsize=(8, 5))
        for cond, bin_data in sorted(cond_map.items()):
            xs, ys = [], []
            for i, label in enumerate(density_bin_labels):
                vals = bin_data.get(label, [])
                if vals:
                    xs.append(i)
                    ys.append(sum(vals) / len(vals) * 100)
            if xs:
                ax.plot(xs, ys, marker="o", label=_pretty_condition(cond))
        ax.set_xticks(range(len(density_bin_labels)))
        ax.set_xticklabels(density_bin_labels)
        ax.set_xlabel("Number of Gold Documents per Task")
        ax.set_ylabel("Mean EM (%)")
        ax.set_title(f"EM vs. Reasoning Density — {_pretty_model(model)}")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fname = f"fig12b_{_safe_slug(_pretty_model(model))}_reasoning_density.pdf"
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
        cm_keys = sorted(error_rates.keys(), key=lambda k: _cm_sort_key(*k.split("/", 1)) if "/" in k else (k, "", 0, ""))

        if all_tools and cm_keys:
            matrix = np.zeros((len(all_tools), len(cm_keys)))
            for j, cm in enumerate(cm_keys):
                for i, tool in enumerate(all_tools):
                    matrix[i, j] = error_rates[cm].get(tool, {}).get("error_rate", 0.0) * 100

            fig, ax = plt.subplots(figsize=(max(6, len(cm_keys) * 2), max(4, len(all_tools) * 0.7)))
            im = ax.imshow(matrix, aspect="auto", cmap="Reds", vmin=0, vmax=50)
            plt.colorbar(im, ax=ax, label="Error Rate (%)")

            ax.set_xticks(range(len(cm_keys)))
            ax.set_xticklabels(
                [_pretty_cm(*k.split("/", 1)) if "/" in k else k for k in cm_keys],
                rotation=30, ha="right", fontsize=8,
            )
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

    # -----------------------------------------------------------------------
    # Fig 14: Tool call counts heatmap — rows=tools, cols=condition×model
    # -----------------------------------------------------------------------
    _UNIMPORTANT_TOOLS = {"get_sandbox_info", "submit_answer", "plan", "think"}
    if depth_records:
        import numpy as np
        # Aggregate total tool call counts and task counts by (cond/model, tool)
        tc_acc: dict = defaultdict(lambda: defaultdict(int))
        n_tasks_by_cm: dict = defaultdict(int)
        for r in depth_records:
            cond = r.get("condition", "?")
            model = r.get("model_label", r.get("model", "?"))
            cm = f"{cond}/{model}"
            n_tasks_by_cm[cm] += 1
            for tc in r.get("tool_counts", []):
                name = tc.get("name", "")
                if not name or name in _UNIMPORTANT_TOOLS:
                    continue
                tc_acc[cm][name] += tc.get("call_count", 0)

        cm_keys = sorted(tc_acc.keys(), key=lambda k: _cm_sort_key(*k.split("/", 1)) if "/" in k else (k, "", 0, ""))
        all_tools = sorted({t for cm_d in tc_acc.values() for t in cm_d})
        if cm_keys and all_tools:
            matrix = np.zeros((len(all_tools), len(cm_keys)))
            for j, cm in enumerate(cm_keys):
                n = n_tasks_by_cm.get(cm, 0)
                for i, tool in enumerate(all_tools):
                    matrix[i, j] = (tc_acc[cm].get(tool, 0) / n) if n else 0.0

            fig, ax = plt.subplots(figsize=(max(6, len(cm_keys) * 2), max(4, len(all_tools) * 0.7)))
            vmax = max(1.0, float(matrix.max()))
            from matplotlib.colors import LinearSegmentedColormap
            white_green = LinearSegmentedColormap.from_list("white_green", ["#ffffff", "#1b7837"])
            im = ax.imshow(matrix, aspect="auto", cmap=white_green, vmin=0, vmax=vmax)
            plt.colorbar(im, ax=ax, label="Avg Calls / Task")

            ax.set_xticks(range(len(cm_keys)))
            ax.set_xticklabels(
                [_pretty_cm(*k.split("/", 1)) if "/" in k else k for k in cm_keys],
                rotation=30, ha="right", fontsize=8,
            )
            ax.set_yticks(range(len(all_tools)))
            ax.set_yticklabels(all_tools, fontsize=9)

            for i in range(len(all_tools)):
                for j in range(len(cm_keys)):
                    val = matrix[i, j]
                    color = "white" if val > vmax * 0.6 else "black"
                    if val > 0:
                        ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8, color=color)

            ax.set_title("Avg Tool Calls per Task by Condition × Model")
            fig.tight_layout()
            fig.savefig(output_dir / "fig14_tool_call_counts.pdf")
            plt.close(fig)
            print("Saved fig14_tool_call_counts.pdf")

    print(f"\nAll figures saved to {output_dir}/")


if __name__ == "__main__":
    main()
