# Paper Figure Generator Design

## Goal

Create `analysis/paper_figure_generator.py`, a paper-focused figure orchestration entrypoint that can regenerate or reuse mode semantic analyses and export the paper figure set to both:

- `sana_framework_paper/figures/`
- `paper_figures/`

The generator must support LakeQA and Kramabench through a simple benchmark flag and optional path overrides.

## Command Interface

Primary commands:

```bash
python analysis/paper_figure_generator.py --benchmark lakeqa
python analysis/paper_figure_generator.py --benchmark kramabench
python analysis/paper_figure_generator.py --benchmark lakeqa --force
```

Arguments:

- `--benchmark {lakeqa,kramabench}`: required benchmark selector.
- `--force`: rerun semantic analysis even if the expected analysis output already exists.
- `--results-dir`: optional semantic `eval_results.csv` root override.
- `--base-results-dir`: optional raw `agent_results.jsonl` root override.
- `--traces-dir`: optional raw trace root override.
- `--tasks-dir`: optional task root override.
- `--analysis-dir`: optional analysis output directory override.
- `--turn-waste-grouped-dir`: optional grouped turn-waste root override.
- `--model-filter`: optional comma-separated model substring filter, forwarded to semantic analysis.
- `--paper-dir`: optional paper figures destination, default `sana_framework_paper/figures`.
- `--mirror-dir`: optional export mirror, default `paper_figures`.

Default benchmark mapping:

| Benchmark | Semantic results | Base results | Traces | Tasks | Analysis output |
| --- | --- | --- | --- | --- | --- |
| `lakeqa` | `results_semantic/modes` | `results/modes` | `results/traces/modes` | `tasks_mini` | `analysis_results_mode_semantic` |
| `kramabench` | `results-kramabench_semantic/modes` | `results-kramabench/modes` | `results-kramabench/traces/modes` | `tasks-mini-kramabench` | `analysis_results_mode_kramabench_semantic` |

## Analysis Flow

The new script should be a thin orchestrator over existing analysis code, not a duplicate metrics implementation.

1. Resolve benchmark defaults and command-line overrides.
2. If `summary.json` exists in the analysis output directory and `--force` is not set, reuse the existing analysis output.
3. Otherwise call `analysis.run_mode_analysis_semantic.run_analysis(...)` with the resolved paths and figure generation enabled.
4. Generate the new search comparison figure from persisted analysis outputs.
5. Copy the curated paper figure set to both destinations.

## New Search Comparison Figure

Filename:

- `search_efficiency_cumulative_retrieval_<benchmark>.pdf`

Scope:

- Compare exactly the search-axis variants:
  - `search_n_results_i_plani_computei_k5_skills_off` as `NII`
  - `search_d_results_i_plani_computei_k5_skills_off` as `DII`
  - `search_i_results_i_plani_computei_k5_skills_off` as `III`
- Do not aggregate different models together.
- Render vertical model rows so each model remains separate but appears in one figure.

Layout:

- Each model gets one row.
- Left panel: scatter plot of average search calls per task vs average `D_ret`.
- Point color encodes `NII`, `DII`, or `III`.
- A hollow ring around each point encodes `D_acc`; label the ring with the numeric `D_acc` value.
- Right panel: cumulative `D_ret` by search call, one line per `NII`, `DII`, and `III`.
- Axes should be shared across model rows where possible so the reader can compare models visually.

Data sources:

- Summary-level means should come from `summary.json`, using `per_task_retrieval.csv` as a fallback if a field is missing.
- Cumulative per-search-call retrieval should come from the existing search bottleneck per-call data (`per_call_rows`) computed by `analysis.search_bottleneck.compute_search_bottleneck`.
- Extend `run_mode_analysis_semantic.py` to write `search_call_cumulative_retrieval.csv` from `per_call_rows` so the paper generator can reuse existing analysis output without recomputing traces.

## Existing Figure Exports

Export these generated files when present:

- `fig05_turn_waste_groups_by_model.pdf`
- `fig05b_turn_waste_groups_by_condition.pdf`
- Benchmark-specific compact semantic delta:
  - LakeQA: `fig21b_lakeqa_semantic_delta_ablation.pdf`
  - Kramabench: `fig21b_krama_semantic_delta_ablation.pdf`

If a source figure is missing, the generator should report it clearly and continue exporting the figures that do exist unless the missing file is the new search comparison figure.

## Integration Points

Preferred changes:

- Add `analysis/paper_figure_generator.py`.
- Add a small CSV export in `run_mode_analysis_semantic.py` for per-call search bottleneck rows.
- Reuse existing functions for variant parsing, labels, model ordering, and delta figure generation where practical.
- Create destination directories automatically.

Avoid:

- Recomputing discovery metrics from scratch in the paper generator.
- Hard-coding only one model.
- Averaging models together in the new figure.
- Renaming existing numbered figures unnecessarily.

## Verification

Run at least:

```bash
python analysis/paper_figure_generator.py --benchmark lakeqa
python analysis/paper_figure_generator.py --benchmark kramabench
```

Verify:

- The script exits successfully.
- `paper_figures/` is created if absent.
- Both destinations contain the new search comparison figure.
- Both destinations contain `fig05_turn_waste_groups_by_model.pdf`, `fig05b_turn_waste_groups_by_condition.pdf`, and the benchmark-specific `fig21b` figure when available.
- The new figure has separate vertical rows per model, not an aggregate over models.
