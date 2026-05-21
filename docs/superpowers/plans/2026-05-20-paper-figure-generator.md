# Paper Figure Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a paper figure generator that rebuilds or reuses semantic-mode analysis outputs, creates the NII/DII/III search-efficiency figure, and exports the curated paper figure set for LakeQA or Kramabench.

**Architecture:** Keep `analysis/run_mode_analysis_semantic.py` as the metrics source of truth and add one persisted CSV for per-search-call cumulative retrieval rows. Add `analysis/paper_figure_generator.py` as a thin orchestrator that resolves benchmark defaults, optionally runs analysis, renders the new figure from persisted outputs, and copies selected PDFs to paper destinations.

**Tech Stack:** Python standard library, existing `analysis.run_mode_analysis_semantic` APIs, existing CSV/JSON analysis outputs, matplotlib Agg backend, unittest/pytest.

---

### Task 1: Persist Per-Search-Call Retrieval Rows

**Files:**
- Modify: `analysis/run_mode_analysis_semantic.py`
- Modify: `test/test_run_mode_analysis_semantic.py`

- [ ] **Step 1: Write the failing test**

Add a focused unit test in `test/test_run_mode_analysis_semantic.py` that exercises a helper for writing per-call rows. Import the helper as `_search_call_cumulative_fieldnames`.

```python
from analysis.run_mode_analysis_semantic import (
    _search_call_cumulative_fieldnames,
)


def test_search_call_cumulative_fieldnames_include_plot_inputs(self):
    fieldnames = _search_call_cumulative_fieldnames()

    self.assertEqual(
        fieldnames,
        [
            "condition_model",
            "condition",
            "variant",
            "base_condition",
            "model",
            "task_id",
            "search_tool",
            "turn",
            "search_call_index",
            "results_returned",
            "n_gold_datasets",
            "cumulative_search_gold_count",
            "cumulative_search_gold_recall",
            "cumulative_read_gold_count",
            "cumulative_read_gold_recall",
            "gold_hits_top_1",
            "gold_in_top_1",
            "gold_recall_top_1",
            "gold_hits_top_3",
            "gold_in_top_3",
            "gold_recall_top_3",
            "gold_hits_top_5",
            "gold_in_top_5",
            "gold_recall_top_5",
        ],
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
pytest test/test_run_mode_analysis_semantic.py::TestRunModeAnalysisSemantic::test_search_call_cumulative_fieldnames_include_plot_inputs -q
```

Expected: FAIL because `_search_call_cumulative_fieldnames` does not exist.

- [ ] **Step 3: Add the helper and CSV export**

In `analysis/run_mode_analysis_semantic.py`, add:

```python
def _search_call_cumulative_fieldnames() -> List[str]:
    return [
        "condition_model",
        "condition",
        "variant",
        "base_condition",
        "model",
        "task_id",
        "search_tool",
        "turn",
        "search_call_index",
        "results_returned",
        "n_gold_datasets",
        "cumulative_search_gold_count",
        "cumulative_search_gold_recall",
        "cumulative_read_gold_count",
        "cumulative_read_gold_recall",
    ] + [
        field
        for cutoff in SEARCH_BOTTLENECK_CUTOFFS
        for field in (
            f"gold_hits_top_{cutoff}",
            f"gold_in_top_{cutoff}",
            f"gold_recall_top_{cutoff}",
        )
    ]
```

Then in `run_analysis`, after `search_tool_efficiency.csv` is written, add:

```python
    search_call_cumulative_csv = out_dir / "search_call_cumulative_retrieval.csv"
    search_call_cumulative_rows = search_bottleneck.get("per_call_rows", [])
    search_call_cumulative_fieldnames = _search_call_cumulative_fieldnames()
    write_search_bottleneck_csv(
        search_call_cumulative_rows,
        search_call_cumulative_csv,
        search_call_cumulative_fieldnames,
    )
    print(f"  Wrote {search_call_cumulative_csv} ({len(search_call_cumulative_rows)} rows)")
    csv_outputs["search_call_cumulative_retrieval.csv"] = (
        search_call_cumulative_rows,
        search_call_cumulative_fieldnames,
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run:

```bash
pytest test/test_run_mode_analysis_semantic.py::TestRunModeAnalysisSemantic::test_search_call_cumulative_fieldnames_include_plot_inputs -q
```

Expected: PASS.

### Task 2: Add Paper Figure Generator Core

**Files:**
- Create: `analysis/paper_figure_generator.py`
- Create: `test/test_paper_figure_generator.py`

- [ ] **Step 1: Write failing tests for benchmark defaults and figure selection**

Create `test/test_paper_figure_generator.py` with tests for `_benchmark_defaults`, `_selected_existing_figures`, and `_search_variant_label`.

```python
import unittest
from pathlib import Path

from analysis.paper_figure_generator import (
    _benchmark_defaults,
    _search_variant_label,
    _selected_existing_figures,
)


class TestPaperFigureGenerator(unittest.TestCase):
    def test_benchmark_defaults_choose_expected_roots(self):
        lakeqa = _benchmark_defaults("lakeqa")
        kramabench = _benchmark_defaults("kramabench")

        self.assertEqual(lakeqa.results_dir, Path("results_semantic/modes"))
        self.assertEqual(lakeqa.base_results_dir, Path("results/modes"))
        self.assertEqual(lakeqa.traces_dir, Path("results/traces/modes"))
        self.assertEqual(lakeqa.tasks_dir, Path("tasks_mini"))
        self.assertEqual(lakeqa.analysis_dir, Path("analysis_results_mode_semantic"))

        self.assertEqual(kramabench.results_dir, Path("results-kramabench_semantic/modes"))
        self.assertEqual(kramabench.base_results_dir, Path("results-kramabench/modes"))
        self.assertEqual(kramabench.traces_dir, Path("results-kramabench/traces/modes"))
        self.assertEqual(kramabench.tasks_dir, Path("tasks-mini-kramabench"))
        self.assertEqual(kramabench.analysis_dir, Path("analysis_results_mode_kramabench_semantic"))

    def test_selected_existing_figures_include_benchmark_specific_fig21b(self):
        self.assertIn(
            "fig21b_lakeqa_semantic_delta_ablation.pdf",
            _selected_existing_figures("lakeqa"),
        )
        self.assertIn(
            "fig21b_krama_semantic_delta_ablation.pdf",
            _selected_existing_figures("kramabench"),
        )

    def test_search_variant_label_maps_canonical_trio(self):
        self.assertEqual(
            _search_variant_label("search_n_results_i_plani_computei_k5_skills_off"),
            "NII",
        )
        self.assertEqual(
            _search_variant_label("search_d_results_i_plani_computei_k5_skills_off"),
            "DII",
        )
        self.assertEqual(
            _search_variant_label("search_i_results_i_plani_computei_k5_skills_off"),
            "III",
        )
        self.assertIsNone(_search_variant_label("search_p_results_i_plani_computei_k5_skills_off"))
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
pytest test/test_paper_figure_generator.py -q
```

Expected: FAIL because `analysis/paper_figure_generator.py` does not exist.

- [ ] **Step 3: Implement CLI skeleton and helpers**

Create `analysis/paper_figure_generator.py` with:

```python
#!/usr/bin/env python3
"""Generate and export paper figures for semantic mode analyses."""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.run_mode_analysis_semantic import run_analysis


SEARCH_VARIANTS = {
    "search_n_results_i_plani_computei_k5_skills_off": ("NII", "BM25"),
    "search_d_results_i_plani_computei_k5_skills_off": ("DII", "Pneuma"),
    "search_i_results_i_plani_computei_k5_skills_off": ("III", "Ideal"),
}

SEARCH_ORDER = ["NII", "DII", "III"]
SEARCH_COLORS = {"NII": "#4C78A8", "DII": "#F58518", "III": "#54A24B"}


@dataclass(frozen=True)
class BenchmarkDefaults:
    benchmark: str
    results_dir: Path
    base_results_dir: Path
    traces_dir: Path
    tasks_dir: Path
    analysis_dir: Path
    turn_waste_grouped_dir: Path
    fig21b_name: str


def _benchmark_defaults(benchmark: str) -> BenchmarkDefaults:
    if benchmark == "lakeqa":
        return BenchmarkDefaults(
            benchmark="lakeqa",
            results_dir=Path("results_semantic/modes"),
            base_results_dir=Path("results/modes"),
            traces_dir=Path("results/traces/modes"),
            tasks_dir=Path("tasks_mini"),
            analysis_dir=Path("analysis_results_mode_semantic"),
            turn_waste_grouped_dir=Path("results_semantic_turn_waste_grouped"),
            fig21b_name="fig21b_lakeqa_semantic_delta_ablation.pdf",
        )
    if benchmark == "kramabench":
        return BenchmarkDefaults(
            benchmark="kramabench",
            results_dir=Path("results-kramabench_semantic/modes"),
            base_results_dir=Path("results-kramabench/modes"),
            traces_dir=Path("results-kramabench/traces/modes"),
            tasks_dir=Path("tasks-mini-kramabench"),
            analysis_dir=Path("analysis_results_mode_kramabench_semantic"),
            turn_waste_grouped_dir=Path("results-kramabench_semantic_turn_waste_grouped"),
            fig21b_name="fig21b_krama_semantic_delta_ablation.pdf",
        )
    raise ValueError(f"Unsupported benchmark: {benchmark}")


def _selected_existing_figures(benchmark: str) -> list[str]:
    defaults = _benchmark_defaults(benchmark)
    return [
        "fig05_turn_waste_groups_by_model.pdf",
        "fig05b_turn_waste_groups_by_condition.pdf",
        defaults.fig21b_name,
    ]


def _search_variant_label(variant: str) -> Optional[str]:
    payload = SEARCH_VARIANTS.get(str(variant))
    return payload[0] if payload else None
```

Continue the file with functions in Tasks 3 and 4.

- [ ] **Step 4: Run tests to verify helpers pass**

Run:

```bash
pytest test/test_paper_figure_generator.py -q
```

Expected: PASS for the helper tests once the imported functions exist.

### Task 3: Render Search Efficiency Figure

**Files:**
- Modify: `analysis/paper_figure_generator.py`
- Modify: `test/test_paper_figure_generator.py`

- [ ] **Step 1: Add failing tests for loading and aggregating canonical rows**

Append tests that create a temporary analysis directory containing `summary.json` and `search_call_cumulative_retrieval.csv`, then assert only NII/DII/III rows are loaded.

```python
import csv
import json
from tempfile import TemporaryDirectory

from analysis.paper_figure_generator import _load_search_figure_data


def test_load_search_figure_data_filters_canonical_trio(self):
    with TemporaryDirectory() as tmpdir:
        analysis_dir = Path(tmpdir)
        summary_rows = [
            {
                "model": "openai_gpt-5-mini",
                "variant": "search_n_results_i_plani_computei_k5_skills_off",
                "avg_search_calls": 3,
                "D_ret": 0.5,
                "D_acc": 0.25,
            },
            {
                "model": "openai_gpt-5-mini",
                "variant": "search_d_results_i_plani_computei_k5_skills_off",
                "avg_search_calls": 4,
                "D_ret": 0.6,
                "D_acc": 0.4,
            },
            {
                "model": "openai_gpt-5-mini",
                "variant": "search_i_results_i_plani_computei_k5_skills_off",
                "avg_search_calls": 1,
                "D_ret": 1.0,
                "D_acc": 1.0,
            },
            {
                "model": "openai_gpt-5-mini",
                "variant": "search_p_results_i_plani_computei_k5_skills_off",
                "avg_search_calls": 0,
                "D_ret": 1.0,
                "D_acc": 1.0,
            },
        ]
        (analysis_dir / "summary.json").write_text(json.dumps(summary_rows))
        with (analysis_dir / "search_call_cumulative_retrieval.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "model",
                    "variant",
                    "task_id",
                    "search_call_index",
                    "cumulative_search_gold_recall",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "model": "openai_gpt-5-mini",
                    "variant": "search_n_results_i_plani_computei_k5_skills_off",
                    "task_id": "k-1/task_1",
                    "search_call_index": "1",
                    "cumulative_search_gold_recall": "0.5",
                }
            )

        data = _load_search_figure_data(analysis_dir)

        self.assertEqual(list(data["summary_by_model"].keys()), ["openai_gpt-5-mini"])
        self.assertEqual(
            [row["label"] for row in data["summary_by_model"]["openai_gpt-5-mini"]],
            ["NII", "DII", "III"],
        )
        self.assertEqual(data["curves"][("openai_gpt-5-mini", "NII")][1], 0.5)
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
pytest test/test_paper_figure_generator.py::test_load_search_figure_data_filters_canonical_trio -q
```

Expected: FAIL because `_load_search_figure_data` is not implemented.

- [ ] **Step 3: Implement loading, aggregation, and plotting**

In `analysis/paper_figure_generator.py`, add:

```python
def _as_float(value: object) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def _model_sort_key(model: str) -> tuple[int, str]:
    lowered = model.lower()
    if "gpt-5-mini" in lowered:
        return (0, model)
    if "gpt-5.4-nano" in lowered:
        return (1, model)
    return (2, model)


def _load_json_rows(path: Path) -> list[dict]:
    with path.open() as handle:
        rows = json.load(handle)
    if not isinstance(rows, list):
        raise ValueError(f"Expected {path} to contain a list")
    return [dict(row) for row in rows]


def _load_search_figure_data(analysis_dir: Path) -> dict:
    summary_by_model: dict[str, list[dict]] = {}
    for row in _load_json_rows(analysis_dir / "summary.json"):
        label = _search_variant_label(str(row.get("variant", "")))
        if label is None:
            continue
        model = str(row.get("model", "unknown"))
        avg_search_calls = _as_float(row.get("avg_search_calls"))
        d_ret = _as_float(row.get("D_ret"))
        d_acc = _as_float(row.get("D_acc_recall", row.get("D_acc")))
        if avg_search_calls is None or d_ret is None or d_acc is None:
            continue
        summary_by_model.setdefault(model, []).append(
            {
                "label": label,
                "variant": str(row.get("variant", "")),
                "avg_search_calls": avg_search_calls,
                "d_ret": d_ret,
                "d_acc": d_acc,
            }
        )

    for model, rows in summary_by_model.items():
        rows.sort(key=lambda row: SEARCH_ORDER.index(str(row["label"])))

    curve_values: dict[tuple[str, str, int], list[float]] = {}
    per_task_latest: dict[tuple[str, str, str, int], float] = {}
    call_csv = analysis_dir / "search_call_cumulative_retrieval.csv"
    if call_csv.exists():
        with call_csv.open(newline="") as handle:
            for row in csv.DictReader(handle):
                label = _search_variant_label(str(row.get("variant", "")))
                if label is None:
                    continue
                model = str(row.get("model", "unknown"))
                task_id = str(row.get("task_id", ""))
                call_index_raw = row.get("search_call_index")
                recall = _as_float(row.get("cumulative_search_gold_recall"))
                if not task_id or recall is None:
                    continue
                try:
                    call_index = int(float(call_index_raw))
                except (TypeError, ValueError):
                    continue
                per_task_latest[(model, label, task_id, call_index)] = recall
        for (model, label, _task_id, call_index), recall in per_task_latest.items():
            curve_values.setdefault((model, label, call_index), []).append(recall)

    curves: dict[tuple[str, str], dict[int, float]] = {}
    for (model, label, call_index), values in curve_values.items():
        if values:
            curves.setdefault((model, label), {})[call_index] = sum(values) / len(values)

    return {"summary_by_model": summary_by_model, "curves": curves}
```

Add `render_search_efficiency_figure(analysis_dir: Path, benchmark: str, output_path: Path) -> Path` that imports matplotlib with `Agg`, creates vertical model rows, plots scatter plus D_acc rings/labels on the left, cumulative D_ret lines on the right, writes the PDF, and returns `output_path`. It must raise `FileNotFoundError` if `summary.json` is missing and `ValueError` if no canonical NII/DII/III rows are available.

- [ ] **Step 4: Run loading test**

Run:

```bash
pytest test/test_paper_figure_generator.py::test_load_search_figure_data_filters_canonical_trio -q
```

Expected: PASS.

### Task 4: Orchestrate Analysis And Export

**Files:**
- Modify: `analysis/paper_figure_generator.py`
- Modify: `test/test_paper_figure_generator.py`

- [ ] **Step 1: Add failing export test**

Append a test for copying curated figures to two destinations.

```python
from analysis.paper_figure_generator import export_paper_figures


def test_export_paper_figures_copies_existing_and_new_outputs(self):
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        analysis_dir = root / "analysis"
        figures_dir = analysis_dir / "figures"
        figures_dir.mkdir(parents=True)
        for name in [
            "fig05_turn_waste_groups_by_model.pdf",
            "fig05b_turn_waste_groups_by_condition.pdf",
            "fig21b_lakeqa_semantic_delta_ablation.pdf",
        ]:
            (figures_dir / name).write_bytes(b"%PDF-1.4\n")
        new_figure = analysis_dir / "search_efficiency_cumulative_retrieval_lakeqa.pdf"
        new_figure.write_bytes(b"%PDF-1.4\n")

        copied = export_paper_figures(
            benchmark="lakeqa",
            analysis_dir=analysis_dir,
            search_figure_path=new_figure,
            destinations=[root / "paper", root / "mirror"],
        )

        self.assertIn(root / "paper" / new_figure.name, copied)
        self.assertTrue((root / "mirror" / "fig05_turn_waste_groups_by_model.pdf").exists())
        self.assertTrue((root / "paper" / "fig21b_lakeqa_semantic_delta_ablation.pdf").exists())
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
pytest test/test_paper_figure_generator.py::test_export_paper_figures_copies_existing_and_new_outputs -q
```

Expected: FAIL because `export_paper_figures` is not implemented.

- [ ] **Step 3: Implement orchestration and export**

In `analysis/paper_figure_generator.py`, add:

```python
def export_paper_figures(
    *,
    benchmark: str,
    analysis_dir: Path,
    search_figure_path: Path,
    destinations: Iterable[Path],
) -> list[Path]:
    copied: list[Path] = []
    source_paths = [search_figure_path]
    figure_dir = analysis_dir / "figures"
    for filename in _selected_existing_figures(benchmark):
        path = figure_dir / filename
        if path.exists():
            source_paths.append(path)
        else:
            print(f"Missing optional figure: {path}")
    for destination in destinations:
        destination.mkdir(parents=True, exist_ok=True)
        for source in source_paths:
            target = destination / source.name
            shutil.copy2(source, target)
            copied.append(target)
    return copied
```

Add `parse_args()`, `_resolve_config(args)`, `ensure_analysis_outputs(...)`, and `main()`:

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=["lakeqa", "kramabench"], required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--results-dir", default=None)
    parser.add_argument("--base-results-dir", default=None)
    parser.add_argument("--traces-dir", default=None)
    parser.add_argument("--tasks-dir", default=None)
    parser.add_argument("--analysis-dir", default=None)
    parser.add_argument("--turn-waste-grouped-dir", default=None)
    parser.add_argument("--model-filter", default=None)
    parser.add_argument("--paper-dir", default="sana_framework_paper/figures")
    parser.add_argument("--mirror-dir", default="paper_figures")
    return parser.parse_args()
```

`ensure_analysis_outputs` should call `run_analysis(...)` only if `--force` is set or `analysis_dir / "summary.json"` does not exist. It should pass `no_figures=False` so existing figures are regenerated when analysis runs.

- [ ] **Step 4: Run export test**

Run:

```bash
pytest test/test_paper_figure_generator.py::test_export_paper_figures_copies_existing_and_new_outputs -q
```

Expected: PASS.

### Task 5: Run End-To-End Checks

**Files:**
- Modify only if verification reveals a bug: `analysis/paper_figure_generator.py`, `analysis/run_mode_analysis_semantic.py`, or tests.

- [ ] **Step 1: Run targeted tests**

Run:

```bash
pytest test/test_paper_figure_generator.py test/test_run_mode_analysis_semantic.py::TestRunModeAnalysisSemantic::test_search_call_cumulative_fieldnames_include_plot_inputs -q
```

Expected: PASS.

- [ ] **Step 2: Run LakeQA generator**

Run:

```bash
python analysis/paper_figure_generator.py --benchmark lakeqa
```

Expected: creates `paper_figures/search_efficiency_cumulative_retrieval_lakeqa.pdf` and `sana_framework_paper/figures/search_efficiency_cumulative_retrieval_lakeqa.pdf`. If the existing analysis directory lacks `search_call_cumulative_retrieval.csv`, run again with `--force`.

- [ ] **Step 3: Run Kramabench generator**

Run:

```bash
python analysis/paper_figure_generator.py --benchmark kramabench
```

Expected: creates `paper_figures/search_efficiency_cumulative_retrieval_kramabench.pdf` and `sana_framework_paper/figures/search_efficiency_cumulative_retrieval_kramabench.pdf`. If the existing analysis directory lacks `search_call_cumulative_retrieval.csv`, run again with `--force`.

- [ ] **Step 4: Inspect generated files**

Run:

```bash
ls -lh paper_figures sana_framework_paper/figures | sed -n '1,120p'
```

Expected: both destinations contain the new search-efficiency PDF and copied `fig05`, `fig05b`, and benchmark-specific `fig21b` files.

