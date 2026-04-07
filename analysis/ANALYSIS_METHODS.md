# Analysis Methods Reference

Single reference for understanding the post-eval analysis pipeline.
All scripts read from `results/` (eval CSVs / agent JSONL) and/or `results/traces/` (per-call traces).

### Trace file format

Per-call traces are written by `TracePlugin` to `results/traces/{condition}/{model}/{task_id}.jsonl`.
Each file contains one JSON record per line. Two record types:

**Search tool record** (one per `search_sparse` / `search_hybrid` / `search_graph` / `search` / `search_keyword` call):
```json
{
  "task_id": "tasks_mini/k-1-d-1/task_001.json",
  "turn": 3,
  "tool": "search_sparse",
  "query": "unemployment county 2019",
  "latency_ms": 142,
  "result_dataset_ids": ["unemployment-county-2019", "bls-laus-2019"],
  "gold_dataset_ids_in_results": ["unemployment-county-2019"],
  "gold_rank": 1,
  "timestamp_ms": 1710000000000
}
```

**submit_answer record** (one per task, written when the agent calls `submit_answer`):
```json
{
  "task_id": "tasks_mini/k-1-d-1/task_001.json",
  "tool": "submit_answer",
  "sources_cited": ["unemployment-county-2019"],
  "timestamp_ms": 1710000000000
}
```

Dataset IDs are normalized: S3 prefix `s3://lakeqa-yc4103-datalake/` stripped, first path component taken.

---

## 1. `compute_em.py` — EM/F1/cost table

**What it computes:** Exact Match (EM) rate, average F1, average cost (USD), and average tool calls per condition × model.

**Inputs:**
- `results/{condition}/{model}/eval_results.csv` — one row per task with `exact_match`, `f1_score`, `cost_usd`, `tool_calls_total`

**Group-by key:** `(condition, model_id)`

**Output columns:**
| Column | Definition |
|--------|------------|
| `condition` | `a`, `b`, or `baseline` |
| `model` | canonical model ID |
| `n_tasks` | number of evaluated tasks |
| `em_rate` | `exact_match_count / n_tasks` |
| `avg_f1` | mean F1 across tasks |
| `avg_cost_usd` | mean cost per task |
| `avg_tool_calls` | mean total tool calls per task |

---

## 2. `discovery_metrics.py` — D_ret and D_acc

**What it computes:** One binary retrieval metric and one continuous access metric per task.

**Metric definitions:**
- **D_ret** (retrieval discovery): 1 if any gold dataset ID appeared in any search tool result during the task, 0 otherwise. Determined from `result_dataset_ids` in search trace records.
- **D_acc** (D_accessed): fraction of gold datasets accessed by the agent via read tools — `|read ∩ gold| / |gold|` (0.0–1.0). Used as a continuous score in the failure taxonomy.

**Inputs:**
- `results/traces/{condition}/{model}/{task_id}.jsonl` — per-call trace records
- `tasks_mini/**/*.json` — ground-truth `datasets_used` field (gold dataset IDs)

**Precision/recall formulas (aggregate):**
- Per-search-call precision: `|gold in call results| / |call results|`
- Per-search-call recall: `|gold in call results| / |gold|`
- Task precision/recall: mean of the per-call values over search calls in that task
- Aggregate precision/recall/F1: mean of the task-level values over tasks

---

## 3. `failure_attribution.py` — EM × D_acc attribution

**What it computes:** Classifies every task (not just failures) into `EM × D_acc` bins using explicit thresholds.

**Decision tree:**
```
EM == 1:
  0.8 <= D_acc <= 1.0  → em1_dacc_ge_0_8
  0.5 <= D_acc < 0.8   → em1_dacc_0_5_to_0_8
  0.2 <= D_acc < 0.5   → em1_dacc_0_2_to_0_5
  0.0 <= D_acc < 0.2   → em1_dacc_lt_0_2

EM == 0:
  0.8 <= D_acc <= 1.0  → em0_dacc_ge_0_8
  0.5 <= D_acc < 0.8   → em0_dacc_0_5_to_0_8
  0.2 <= D_acc < 0.5   → em0_dacc_0_2_to_0_5
  0.0 <= D_acc < 0.2   → em0_dacc_lt_0_2
```

**Inputs:** `results/traces/`, `results/`, `tasks_mini/` (delegated to `discovery_metrics.py`)

**Output:** Printed table of counts and percentages for all labels.

### 3b. `failure_attribution_deciles.py` — EM × D_acc deciles

**What it computes:** Same as above, but with 0.1-wide `D_acc` bins:
`[0.0,0.1)`, `[0.1,0.2)`, …, `[0.9,1.0]`, crossed with `EM ∈ {0,1}`.

---

## 4. `provenance.py` — first-hit backend attribution

**What it computes:** For each correctly-answered task (EM=1), which search backend first returned a gold dataset ID.

**Attribution rule:** Scan trace records for a given task in turn order (`turn` field ascending). The first search record where `gold_dataset_ids_in_results` is non-empty determines the backend. Ties (same turn) are broken by write order in the JSONL file.

**Inputs:** `results/traces/{condition}/{model}/{task_id}.jsonl`

**Output columns:** `task_id`, `first_hit_backend`, `first_hit_turn`, `condition`, `model`

---

## 5. `efficiency.py` — cost, latency, and runtime distributions

**What it computes:** Distributions and correlations for resource usage metrics.

**Metrics computed:**
- Cost distribution: min/median/p95/max of `cost_usd` per condition
- Latency distribution: same for `runtime_seconds`
- Tool call distribution: same for `tool_calls_total`
- **Pearson r** between `tool_calls_total` and `exact_match` across tasks:
  `r = cov(tool_calls, em) / (σ_tools · σ_em)`

**Inputs:** `results/{condition}/{model}/eval_results.csv`

---

## 6. `generate_figures.py` — figure generation

| Figure | Script producing it | Data source |
|--------|---------------------|-------------|
| EM rate bar chart (condition × model) | `generate_figures.py::fig_em_bar` | `compute_em.py` output |
| D_ret / D_acc heatmap | `generate_figures.py::fig_discovery_heatmap` | `discovery_metrics.py` output |
| EM × D_acc attribution stacked bar + heatmap | `generate_figures.py` (Fig 3 / Fig 3b) | `failure_attribution.py` output |
| Provenance Sankey / stacked bar | `generate_figures.py::fig_provenance` | `provenance.py` output |
| Cost vs. EM scatter | `generate_figures.py::fig_cost_scatter` | `efficiency.py` output |

All figures are written to `results/figures/` as PDF + PNG.
