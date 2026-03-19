# Analysis Methods Reference

Single reference for understanding the post-eval analysis pipeline.
All scripts read from `results/` (eval CSVs / agent JSONL) and/or `results/sidecar/` (per-call traces).

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
- **D_ret** (retrieval discovery): 1 if any gold dataset ID appeared in any search tool result during the task, 0 otherwise. Determined by joining sidecar traces on `gold_dataset_ids_in_results`.
- **D_acc** (accuracy discovery): 1 if the agent cited at least one gold dataset in its final answer's `sources_used` field, 0 otherwise.

**Inputs:**
- `results/sidecar/{condition}/{model}/{task_id}.jsonl` — per-call trace records with `result_dataset_ids`, `gold_dataset_ids_in_results`
- `results/{condition}/{model}/agent_results.jsonl` — final `sources_used` per task
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

**Inputs:** `results/sidecar/`, `results/`, `tasks_mini/` (delegated to `discovery_metrics.py`)

**Output:** Printed table of counts and percentages per category.

---

## 4. `provenance.py` — first-hit backend attribution

**What it computes:** For each correctly-answered task (EM=1), which search backend first returned a gold dataset ID.

**Attribution rule:** Scan sidecar traces for a given task in turn order (`turn` field ascending). The first trace entry where `gold_dataset_ids_in_results` is non-empty determines the backend. Ties (same turn) are broken by the order they appear in the JSONL file (i.e., write order).

**Inputs:** `results/sidecar/{condition}/{model}/{task_id}.jsonl`

**Output columns:** `task_id`, `first_hit_backend`, `first_hit_turn`, `condition`, `model`

---

## 5. `behavioral.py` — tool switching and query drift

**What it computes:** Two behavioral signatures, one per condition.

**Condition A — tool switching:**
- Per task: count consecutive backend changes in turn-ordered trace sequence.
  - `switches = Σ [backend[i] ≠ backend[i-1]]` for i in 1..n
- Aggregates: `avg_switches`, `max_switches`, `backend_task_coverage` (tasks that used each backend ≥ once)

**Condition B — query drift (Jaccard and cosine):**
For each consecutive pair of queries `(q_{i-1}, q_i)` within a task:
- **Jaccard**: `|tok(q_{i-1}) ∩ tok(q_i)| / |tok(q_{i-1}) ∪ tok(q_i)|`
- **Cosine (TF)**: `dot(tf(q_{i-1}), tf(q_i)) / (‖tf(q_{i-1})‖ · ‖tf(q_i)‖)`

where `tok(q)` = set of lowercase word tokens. Average across pairs per task, then average across tasks.
Lower similarity = more reformulation / drift.

**Inputs:** `results/sidecar/` (uses `query` and `tool` fields from trace records)

---

## 6. `efficiency.py` — cost, latency, and runtime distributions

**What it computes:** Distributions and correlations for resource usage metrics.

**Metrics computed:**
- Cost distribution: min/median/p95/max of `cost_usd` per condition
- Latency distribution: same for `runtime_seconds`
- Tool call distribution: same for `tool_calls_total`
- **Pearson r** between `tool_calls_total` and `exact_match` across tasks:
  `r = cov(tool_calls, em) / (σ_tools · σ_em)`

**Inputs:** `results/{condition}/{model}/eval_results.csv`

---

## 7. `generate_figures.py` — figure generation

| Figure | Script producing it | Data source |
|--------|---------------------|-------------|
| EM rate bar chart (condition × model) | `generate_figures.py::fig_em_bar` | `compute_em.py` output |
| D_ret / D_acc heatmap | `generate_figures.py::fig_discovery_heatmap` | `discovery_metrics.py` output |
| Failure attribution pie/stacked bar | `generate_figures.py::fig_failure_pie` | `failure_attribution.py` output |
| Provenance Sankey / stacked bar | `generate_figures.py::fig_provenance` | `provenance.py` output |
| Query drift violin plot (Condition B) | `generate_figures.py::fig_drift_violin` | `behavioral.py` output |
| Tool switching heatmap (Condition A) | `generate_figures.py::fig_switch_heatmap` | `behavioral.py` output |
| Cost vs. EM scatter | `generate_figures.py::fig_cost_scatter` | `efficiency.py` output |

All figures are written to `results/figures/` as PDF + PNG.
