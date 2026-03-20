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

**What it computes:** Two binary discovery metrics per task.

**Metric definitions:**
- **D_ret** (retrieval discovery): 1 if any gold dataset ID appeared in any search tool result during the task, 0 otherwise. Determined from `result_dataset_ids` in search trace records.
- **D_acc** (accuracy discovery): 1 if the agent cited at least one gold dataset in its `submit_answer` call's `sources_cited` field, 0 otherwise.

**Inputs:**
- `results/traces/{condition}/{model}/{task_id}.jsonl` — per-call trace records
- `tasks_mini/**/*.json` — ground-truth `datasets_used` field (gold dataset IDs)

**Precision/recall formulas (aggregate):**
- Retrieval precision: `sum(D_ret) / n_tasks`
- Source precision: `|cited ∩ gold| / |cited|` averaged over tasks where `|cited| > 0`
- Source recall: `|cited ∩ gold| / |gold|` averaged over tasks where `|gold| > 0`

---

## 3. `failure_attribution.py` — failure taxonomy

**What it computes:** Classifies each failed task into one of five categories.

**Decision tree:**
```
EM == 1                          → correct
EM == 0 ∧ D_ret == 0 ∧ sources == []  → hallucination
EM == 0 ∧ D_ret == 0                  → search
EM == 0 ∧ D_ret == 1 ∧ D_acc == 0    → discovery-reason
EM == 0 ∧ D_ret == 1 ∧ D_acc == 1    → execution
```

**Inputs:** `results/traces/`, `results/`, `tasks_mini/` (delegated to `discovery_metrics.py`)

**Output:** Printed table of counts and percentages per category.

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
| Failure attribution pie/stacked bar | `generate_figures.py::fig_failure_pie` | `failure_attribution.py` output |
| Provenance Sankey / stacked bar | `generate_figures.py::fig_provenance` | `provenance.py` output |
| Cost vs. EM scatter | `generate_figures.py::fig_cost_scatter` | `efficiency.py` output |

All figures are written to `results/figures/` as PDF + PNG.
