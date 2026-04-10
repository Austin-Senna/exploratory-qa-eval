# Strands Evaluation Framework

## Scope
This project evaluates a tool-using data-lake QA agent under different condition designs and search-ablation settings, then analyzes accuracy, retrieval behavior, efficiency, and failure modes.

## End-to-End Flow
1. Task inputs come from `tasks_mini/k-*-d-*/*.json` (`question`, `answer`, `datasets_used`).
2. Evaluation runs via:
   - `python -m strands_evaluation.run_eval` (baseline / A / B)
   - `python -m strands_evaluation.run_search_eval` (search ablations: fixed `k`, search-call cap, description mode)
3. Raw outputs are written to:
   - `results/{condition}/{model}/eval_results.csv`
   - `results/{condition}/{model}/tools_breakdown.csv`
   - `results/{condition}/{model}/agent_results.jsonl`
   - `results/traces/{condition}/{model}/{task_dir}/{task}.jsonl`
4. Analysis runs via:
   - `analysis/run_analysis.py` (standard conditions)
   - `analysis/search_analysis.py` (variant-aware search ablations)
5. Analysis artifacts are written to `analysis_results/` or `analysis_results_search/` (+ figures).

## Condition Design
- `baseline`: sparse search (`search_value`, `search_schema`, `search_prefix`) + core data tools.
- `a` (tools-rich): hybrid + reranked search (`search_value`, `search_schema`, `search_reranked`, `search_prefix`) + core data tools; prompt pushes early reranked retrieval.
- `b` (planning-rich): sparse search + `plan` + `summarize_context` + skills (`plan-agent`, `discover-data`, `query-data`) + core data tools; prompt enforces explicit skill-loading cadence.

## Runtime Controls
- Sliding context window (`sliding_window_k`, default 40).
- Hard task budget (`max_tool_calls`, default 30) and timeout (`timeout_seconds`, default 450).
- Optional search budget (`search_calls_limit`) enforced by `SearchCallBudgetHandler`.
- Optional fixed search result limit (`search_k`) and result-description enrichment via `build_search_tools(...)`.
- Condition B loop guard (`CategoryStagnationHandler`) to reduce repetitive tool-category loops.

## Instrumentation (What Gets Logged)
- `TracePlugin` logs each search call: tool, query, latency, result dataset IDs, gold hits, rank.
- `ReadTracePlugin` logs each read/access call: dataset IDs read and gold-read overlap.
- Traces are normalized to dataset IDs and used for retrieval/access metrics.

## Core Metrics
- Accuracy: `EM`, `F1` (`analysis/compute_em.py`).
- Discovery/access:
  - `D_ret`: gold retrieval coverage.
  - `D_acc`: gold access coverage via read/query tools.
  - Precision/recall/F1 variants for both retrieval and access (`analysis/discovery_metrics.py`).
- Failure attribution: `EM × D_acc` bins (+ decile variant) (`analysis/failure_attribution*.py`).
- Provenance: first backend that retrieved gold datasets (Condition A focused) (`analysis/provenance.py`).
- Efficiency: cost/time/tool-call distributions (`analysis/efficiency.py`).
- Search depth: EM by search-call bin (`analysis/search_depth.py`).
- Reasoning density: EM by required gold-doc count (`analysis/reasoning_density.py`).
- Planning overhead: Condition B cycle count vs EM/tokens (`analysis/planning_overhead.py`).
- Tool reliability: per-tool error rates from `tool_counts` (`analysis/tool_error_analysis.py`).

## Figure Generation
`analysis/generate_figures.py` creates the paper-style plots from analysis outputs (EM comparison, discovery heatmaps, failure breakdowns, provenance, cost/accuracy, etc.) into `analysis_results/figures/`.
