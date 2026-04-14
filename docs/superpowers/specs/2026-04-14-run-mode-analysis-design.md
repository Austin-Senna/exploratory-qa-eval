# run_mode_analysis.py Design

## Context

The multi-axis ablation framework (see `ablation_framework.md`) runs eval variants under `results/modes/{model}/{variant}/agent_results.jsonl`, where `{variant}` encodes the three axes `search_{s}_results_{r}_plan{p}` (each ∈ `{n, d, i}` = naive, standard, ideal) plus optional `_kN` / `_scN` suffixes. Mode runs have no `base_condition` layer — that's a legacy/search-variant construct.

We have `analysis/search_analysis.py` that produces `analysis_results_search/` from the 3-level `{variant}/{base_condition}/{model}/` layout. We want a parallel `analysis/run_mode_analysis.py` that produces `analysis_results_mode/` from the 2-level `{model}/{variant}/` layout used by `run_mode_eval.py`.

All existing metric modules under `analysis/` (`compute_em`, `discovery_metrics`, `failure_attribution`, `search_depth`, `reasoning_density`, plus `efficiency` and `tool_error_analysis` style computation) are reusable without modification; they operate on records/traces that have already been loaded into memory.

## Goals

- Produce per-variant-cell analysis (one row per (model, variant) combination) comparable to what `search_analysis.py` emits today.
- Parse the variant string into explicit `search_tool`, `search_results`, `agent_management`, `k`, and `sc` columns so downstream filtering in pandas/Excel is trivial.
- Generate figures using the existing `generate_figures.py` via a symlink-flattened layout (same trick `search_analysis.py` uses), default on with `--no-figures` opt-out.
- Zero modifications to any existing `analysis/*` module — the new file imports them as-is.

## Non-Goals

- No per-axis marginal rollups (e.g., "average across all `search_tool=standard` variants"). User chose "compare each full variant" only.
- No provenance analysis. Mode runs don't have the Condition-A/B base concept and provenance is specific to Condition A.
- No planning-overhead analysis. Same reason — specific to Condition B.
- No refactor of `search_analysis.py` to share code. Copy-pattern is consistent with how the repo already has `run_analysis.py` (legacy) and `search_analysis.py` side-by-side.

## Architecture

Single new file: `analysis/run_mode_analysis.py`.

Structurally mirrors `search_analysis.py` but with a 2-level path parser and reduced output set.

### Path parsing

Mode results layout:
- `{results_dir}/{model}/{variant}/agent_results.jsonl`
- `{traces_dir}/{model}/{variant}/{task_dir}/{task}.jsonl`

Parser helpers:

```python
def _parse_results_jsonl_path(path: Path, results_root: Path) -> tuple[str, str]:
    # returns (model, variant)
    rel = path.relative_to(results_root)
    parts = rel.parts
    if len(parts) >= 3:
        return parts[-3], parts[-2]
    return "unknown", "unknown"

def _parse_trace_jsonl_path(path: Path, traces_root: Path) -> tuple[str, str, str]:
    # returns (model, variant, task_id)
    rel = path.relative_to(traces_root)
    parts = rel.parts
    if len(parts) >= 4:
        task_id = f"{parts[-2]}/{Path(parts[-1]).stem}"
        return parts[-4], parts[-3], task_id
    return "unknown", "unknown", "unknown/unknown"

def _cm_key(model: str, variant: str) -> str:
    return f"{model}/{variant}"
```

### Variant parsing

```python
_LETTER_TO_MODE = {"n": "naive", "d": "standard", "i": "ideal"}

def _parse_variant(variant: str) -> dict:
    """search_i_results_i_plani_k5_sc20 -> structured axes."""
    out = {"variant": variant, "search_tool": None, "search_results": None,
           "agent_management": None, "k": None, "sc": None}
    parts = variant.split("_")
    for idx, token in enumerate(parts):
        if token == "search" and idx + 1 < len(parts):
            out["search_tool"] = _LETTER_TO_MODE.get(parts[idx + 1])
        elif token == "results" and idx + 1 < len(parts):
            out["search_results"] = _LETTER_TO_MODE.get(parts[idx + 1])
        elif token.startswith("plan") and len(token) > 4:
            out["agent_management"] = _LETTER_TO_MODE.get(token[4:])
        elif token.startswith("k") and token[1:].isdigit():
            out["k"] = int(token[1:])
        elif token.startswith("sc") and token[2:].isdigit():
            out["sc"] = int(token[2:])
    return out
```

The letter map mirrors `run_mode_eval.py`'s `_MODE_LETTERS`.

### Load functions

- `load_results_grouped(results_dir)` → `(records, by_key, meta_by_key)`:
  - `records`: flat list with each record tagged with `model_label`, `variant`, and `_cm_key`.
  - `by_key`: `dict[key, list[records]]`.
  - `meta_by_key`: `dict[key, {"model": str, "variant": str}]`.
- `load_traces_grouped(traces_dir)` → `(grouped_traces, meta_by_key)`:
  - `grouped_traces`: `dict[key, dict[task_id, list[events]]]`.

Each record also gets `condition = _cm_key(model, variant) = f"{model}/{variant}"` stored on it so the existing metric modules that key on a `condition` field (`compute_search_depth_curve` at `analysis/search_depth.py:50`, `compute_reasoning_density_curve` at `analysis/reasoning_density.py:68`) bucket per (model, variant) cell. This is a deliberate deviation from `search_analysis.py`, which sets `condition = variant` and silently collapses across models for these two metrics — an aggregation-level mismatch versus the rest of the pipeline (em_f1, discovery, efficiency, failure, tool_errors, tools_discovery), all of which are per-cell. Choosing `condition = _cm_key` keeps every output at the same per-cell granularity.

### Metric runners (reused)

Called identically to `search_analysis.py`:

- `run_em(records)` → `em` keyed by `_cm_key`.
- `run_discovery(grouped_traces, tasks_dir)` → `discovery` keyed by `_cm_key`.
- `run_failure(by_key, grouped_traces, tasks_dir)` → `failure`.
- `run_efficiency(by_key)` → `efficiency`.
- `run_tools_discovery(grouped_traces, tasks_dir)` → `tools_discovery`.
- `run_search_depth(records)` → `search_depth`.
- `run_reasoning_density(records, tasks_dir)` → `reasoning_density`.
- `run_tool_errors(by_key)` → `tool_errors`.

**Not called:** `run_provenance`, `run_planning_overhead`.

### Summary assembly

`build_summary(em, discovery, failure, efficiency, search_depth, reasoning_density, tool_errors)` → list of rows; each row starts with:

```python
axes = _parse_variant(variant)
row = {
    "condition_model": key,
    "model": model,
    "variant": variant,
    "search_tool": axes["search_tool"],
    "search_results": axes["search_results"],
    "agent_management": axes["agent_management"],
    "k": axes["k"],
    "sc": axes["sc"],
    # ... em, discovery, failure, search_depth, reasoning_density, tool_errors fields
}
```

Fields added per metric group match `search_analysis.py`'s `build_summary` exactly (n, em, f1, D_ret, D_acc, dacc_precision/recall/f1, failure buckets, tool error rates, depth bins, reasoning-density bins) minus any fields that depended on `base_condition`.

`build_variant_summary(summary_rows)` → rollup grouped by `variant` (across models). Each variant row includes `search_tool`, `search_results`, `agent_management`, `k`, `sc`, `n_total`, `num_model_rows`, weighted-average `em`, `f1`, `D_ret`, `D_acc`, `D_acc_precision/recall/f1`, `avg_cost_usd`, `avg_tool_calls`, `avg_search_calls`, `total_cost_usd`, `search_efficiency`.

### CSV output

`per_task_retrieval.csv` with the same columns `search_analysis.py` emits:
`condition_model, task_id, search_calls_count, gold_datasets_needed_count, datasets_retrieved_count, datasets_retrieved_unique_count, gold_datasets_retrieved_count, retrieval_recall, retrieval_precision, retrieval_f1`.

`condition_model` is `{model}/{variant}` for mode runs.

### Figure generation

When `--no-figures` is absent, flatten each `(model, variant)` pair into a synthetic `{variant}/{model}/` layout under a `TemporaryDirectory` using symlinks, then subprocess-call `generate_figures.py` pointed at the flattened roots. Same pattern as `search_analysis.py:generate_search_figures` but simplified (no base_condition collapse).

```python
def generate_mode_figures(results_dir, traces_dir, tasks_dir, output_dir, model_filter):
    # For each (model, variant) in results_dir:
    #   symlink results/modes/{model}/{variant}/agent_results.jsonl
    #        -> tmp/results/{variant}/{model}/agent_results.jsonl
    # For each (model, variant) with traces:
    #   symlink results/traces/modes/{model}/{variant}
    #        -> tmp/traces/{variant}/{model}
    # Then: subprocess.run([python, generate_figures.py, --results-dir, ..., --output-dir, fig_dir])
```

### CLI

```python
argparse:
  --results-dir         default="results/modes"
  --traces-dir          default="results/traces/modes"
  --tasks-dir           default="tasks_mini"
  --output-dir          default="analysis_results_mode"
  --no-figures          flag; if set, skip generate_mode_figures
  --model-filter        comma-separated OR substring filter on model name
```

## Output Files

Under `--output-dir` (default `analysis_results_mode/`):

- `em_f1.json` — per-key EM/F1/cost/tool-call averages.
- `discovery.json` — per-key D_ret, D_acc, precision/recall/F1 (aggregate only; `task_metrics` stripped from serialized form as in search_analysis).
- `tools_discovery.json` — per-key per-tool discovery rates.
- `failure.json` — per-key EM × D_acc threshold bucket counts/percentages.
- `efficiency.json` — per-key cost/time/tool-call distributions.
- `search_depth.json` — per-condition (variant) EM by search-call count bins.
- `reasoning_density.json` — per-condition EM by gold-doc count bins.
- `tool_errors.json` — per-key per-tool error rates.
- `summary.json` — flat list; one row per `{model}/{variant}` with parsed axes + all metrics.
- `variant_summary.json` — rollup by variant across models.
- `per_task_retrieval.csv` — task-level retrieval details.
- `figures/` — PNG outputs from `generate_figures.py` when `--no-figures` is not set.

**Not emitted:** `provenance.json`, `planning_overhead.json`.

## Error Handling

- Empty `results_dir` (no `agent_results.jsonl` found): print a message and exit cleanly, same as search_analysis.
- Missing `traces_dir`: discovery/failure/tools_discovery output empty dicts for affected keys; not fatal.
- Malformed variant string: `_parse_variant` returns `None` for axes it can't parse; row still emitted, just with null axes.
- Figure generation failure: catch `subprocess.CalledProcessError`, print the exit code, continue (don't abort the JSON outputs).

## Testing

Manual smoke test (the user already has mode-run outputs in `test_results/modes/`):

```
python -m analysis.run_mode_analysis \
  --results-dir test_results/modes \
  --traces-dir test_results/traces/modes \
  --tasks-dir tasks_mini \
  --output-dir /tmp/analysis_mode_smoke \
  --no-figures
```

Expected: `summary.json` non-empty, each row has `search_tool`, `search_results`, `agent_management`, `k` populated; no `provenance.json` or `planning_overhead.json` present.

Unit tests are not included in this spec — the new file is thin glue around already-tested metric modules. Any test additions are optional and not part of the core deliverable.

## Files Touched

- `analysis/run_mode_analysis.py` — new file (~400–500 lines, structurally mirrors `search_analysis.py`).

## Out of Scope

- Marginal per-axis summaries (confirmed with user).
- Refactor of `search_analysis.py` / shared loader extraction.
- Any changes to `generate_figures.py` or existing analysis modules.
- Tooling for diffing two mode-run outputs (e.g., comparing an `analysis_results_mode/` from main vs a branch).
