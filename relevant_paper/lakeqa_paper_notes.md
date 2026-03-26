# LakeQA Paper Notes
# 33696_LakeQA_A_Benchmark_for_C.pdf
# "LakeQA: An Exploratory QA Benchmark over a Million-Scale Data Lake"
# ICML 2026 (under review, double-blind)

---

## What This Is

This IS our paper. It defines the benchmark that our eval harness (`exploratory-qa-eval`) is built to run. Everything in this repo is the evaluation framework for LakeQA.

---

## Core Concept: Exploratory Question Answering (EQA)

- Agent starts with only a question; evidence is distributed across a massive data lake
- Agent must alternate between: (i) reasoning about missing evidence, (ii) searching for documents
- NOT reading comprehension — evidence is NOT provided upfront
- Scale: ~9.5 TB, ~40 million heterogeneous documents (Wikipedia + Data.gov)

---

## Benchmark Statistics

| Stat | Value |
|------|-------|
| LakeQA-full tasks | 1,005 |
| LakeQA-mini tasks | 135 (stratified subset, same reasoning density distribution) |
| Avg Wikipedia dataset IDs per task | 1.98 |
| Avg Data.gov dataset IDs per task | 5.23 |
| Unique Wikipedia dataset IDs | 376 |
| Unique Data.gov dataset IDs | 555 |
| Avg question length | 110.5 tokens |
| **Avg docs required per task (reasoning density)** | **7.67** |
| Search space | >1 million candidates |

Domain distribution: Government & Admin (27.1%), Health & Social (16.8%), Environment (18.8%), Transportation (9%), Demographics (9%), Research (7.8%), Public Safety (6.9%), Economy & Infrastructure (6.9%), Education (6.5%)

---

## The Two Key Density Metrics (Table 1)

**Reasoning Density** = avg number of documents required to answer a task
- LakeQA: **7.67** (more than double HotpotQA's 2.04, MuSiQue's 2.49)
- Topology: **Graph** (not chain like most benchmarks — dependencies can branch)

**Search Density** = avg candidate documents per gold document
- LakeQA: **>1M** (vs. OTT-QA's >1M, but LakeQA is structured + unstructured)

---

## Tool Interface (Table 2) — Ground Truth for Our Agent Tools

| Tool | Input | Output |
|------|-------|--------|
| `search(query)` | keyword or tag string | ranked list of dataset IDs |
| `listdata(dataset-ids)` | list of dataset IDs | files under each dataset ID dir |
| `download(dataset-ids)` | list of dataset IDs | downloads to per-task sandbox |
| `inspect(path)` | file path | first k characters (preview) |
| `query(path, q)` | file path + query | filter/aggregate over local data |

This is the **baseline** tool suite. Our conditions A and B extend/modify this.

---

## Experimental Results

### LakeQA-full (Table 4)

| Model | EM (%) | Runtime (s) | Cost ($) | Dacc P | Dacc R | Dacc F1 | Dret P | Dret R | Dret F1 |
|-------|--------|-------------|----------|--------|--------|---------|--------|--------|---------|
| Llama-3.3-70B | 6.57 | 25.69 | 0.02 | 5.24 | 2.68 | 1.86 | 23.59 | — | — |
| DeepSeek-R1 | 20.60 | 92.00 | 0.11 | 33.91 | 11.01 | 7.88 | 25.68 | — | — |
| Claude-haiku-4.5 | 11.94 | 70.51 | 0.31 | 29.23 | 26.73 | 21.66 | — | — | — |
| Claude-sonnet-4.5 | **23.08** | 124.45 | 0.96 | 34.18 | 30.72 | 41.14 | 33.27 | 40.03 | — |
| GPT-5-mini | 10.95 | 197.75 | 0.08 | 32.18 | — | 32.56 | 26.91 | 34.20 | — |
| GPT-5.2 | 14.73 | 66.49 | 0.39 | 35.89 | — | 24.88 | 25.68 | 38.93 | — |

### LakeQA-mini (Table 5)

| Model | EM (%) | Runtime (s) | Cost ($) |
|-------|--------|-------------|----------|
| Llama-3.3-70B | 8.89 | 27.67 | 0.03 |
| DeepSeek-R1 | 23.70 | 83.62 | 0.10 |
| Claude-haiku-4.5 | 12.59 | 67.77 | 0.30 |
| Claude-opus-4.5 | **37.04** | 113.28 | 1.55 |
| Claude-sonnet-4.5 | 25.93 | 129.69 | 0.92 |
| GPT-5-mini | 11.85 | 192.32 | 0.08 |
| GPT-5.2 | 14.81 | 67.14 | 0.39 |

**Key takeaway**: Best model (Claude-opus-4.5) achieves only 37% on mini. All under 30% on full. EQA is very hard.

---

## Key Research Questions & Findings

### RQ1: How do different LLMs perform?
- Best on full: Claude-sonnet-4.5 (23.08%)
- Best on mini: Claude-opus-4.5 (37.04%)
- All models < 30% on full — EQA remains unsolved
- Three-way trade-off: accuracy × runtime × cost. Current Pareto front is low.
- GPT-5-mini: longest runtime (often writes inefficient code to query large datasets); larger models avoid this

### RQ2: Main reason for failure?
- **Primary bottleneck: document discovery (search/retrieval), not reasoning**
- Recall of Dret and Dacc are both low; gap between them is small → models fail to surface relevant datasets during search, not just fail to open them
- GPT-5.2 has higher Dacc precision than Claude-sonnet-4.5 but lower EM → **conservative exploration (high precision, low recall) is fatal in EQA**
- Effective agents must balance precision with recall — broad exploration even at cost of irrelevant docs

### RQ3: How does performance change with reasoning density?
- **Clear monotonic drop as doc count increases** (Figure 4)
- ≤4 docs: highest EM across all models (manageable search)
- ≥7 docs: sharp degradation
- >10 docs: EM approaches <10% for all models
- Long-horizon exploration amplifies error accumulation from: imperfect retrieval, missed constraints, faulty cross-document aggregation

---

## Task Structure: Question Decomposition Graph (QDG)

Tasks are DAGs, not chains. Each node is an atomic sub-question answered by exactly one data source. This is why:
- Reasoning density = 7.67 (many nodes)
- Topology = Graph (branches possible)
- Errors at early nodes propagate downstream

The paper uses three key annotation stats:
- **S1**: Minimum node count across all valid QDGs
- **S2**: Shortest path from Q to A across all QDGs
- **S3**: Maximum-cardinality minimal Q-A cut (parallel search paths)

---

## Evaluation Metrics — Official Definition

The paper's official metrics (directly relevant to our analysis):

**Dret** (retrieval set) = union of all dataset-IDs surfaced through discovery, regardless of whether subsequently opened
**Dacc** (accessed set) = dataset-IDs the agent actually opened/queried

For each: compute precision, recall, F1 vs. gold set D*

**Interpretation**:
- Low Dret recall = **searching failure** — agent couldn't find relevant datasets
- Gap between Dret recall and Dacc recall = **reasoning failure** — agent found but didn't open relevant datasets

This matches our `D_ret` and `D_acc` metrics exactly. ✓

---

## Things We Should Update / Align With

### In paper_analysis_notes.md, update these items:

1. **Failure attribution labels should use paper's terminology**:
   - `search_failed` → maps to "searching failure" (low Dret recall)
   - `search_not_read` → maps to "reasoning failure" (found but not opened)
   - Our new `search_failed_budget` / `search_failed_quality` split is novel — not in the paper, but scientifically motivated

2. **Search depth curve (Item 2)** — Figure 4 in the paper is exactly this, but they use "number of documents per task" (a gold property) not "search calls used" (a behavioral property). Our version is complementary — measures what the agent *actually did* vs. what was *required*.

3. **The paper's RQ structure maps to our conditions**:
   - RQ2 (why do models fail?) → answered by failure attribution + our search_failed_budget/quality split
   - RQ3 (performance vs. density) → answered by our search depth curve, but we should also stratify by **task reasoning density** (num_gold_docs), not just search calls used

4. **New analysis idea from RQ3**: Plot EM vs. `len(datasets_used)` (gold doc count per task) — this is Figure 4 from the paper. We should reproduce it with our conditions to see if Condition A vs. B handles high-density tasks differently.

5. **Conservative vs. broad exploration** (from RQ2 finding): GPT-5.2 example — high Dacc precision but low EM. This is measurable in our data: compare Dacc precision vs. Dacc recall per condition. Conditions that are too conservative (high P, low R) will underperform despite "confident" retrievals.

---

## New Analysis Ideas (from LakeQA paper)

### HIGH PRIORITY

**A. EM stratified by reasoning density (gold doc count)**
- Bin tasks by `len(datasets_used)`: ≤2, 3-4, 5-7, 8-10, >10
- Plot mean EM per bin per condition
- This is Figure 4 from the paper — directly comparable
- Key question: does Condition A's richer search toolkit flatten the degradation curve vs. Condition B?

**B. Dacc recall vs. Dacc precision tradeoff per condition**
- From RQ2: conservative exploration (high P, low R) is fatal
- Compute P and R of Dacc per condition per model — which condition encourages broader exploration?
- Already have the data; just need to surface it in summary/figures

### MEDIUM PRIORITY

**C. Dret recall vs. Dacc recall gap per condition**
- Paper defines: gap = reasoning failure (found but didn't open)
- We already compute both; compute the gap explicitly as a metric
- `exploration_gap = D_ret_recall - D_acc_recall` per task, then average per condition

**D. Domain-stratified performance**
- Paper shows domain distribution (Gov 27%, Health 17%, etc.)
- If tasks have domain labels, stratify EM by domain per condition
- Do conditions differ in which domains they handle better?

---

## Summary: What the Paper Tells Us About Our Experiment Design

1. **Our baseline measures are correct** — EM, D_ret, D_acc, P/R/F1 match the paper's official metrics
2. **The main story is search quality** — both the paper and our analysis items 1-6 point to this
3. **Graph topology matters** — tasks require branching reasoning chains, not just linear hops; Condition B's linear planning may miss this
4. **Broad exploration >> conservative exploration** — our search efficiency metric (EM/search_calls) should be interpreted carefully: fewer searches with same EM could mean efficiency, or could mean the agent was too conservative and got lucky
5. **Mini vs. full** — our `tasks_mini` (135 tasks) matches LakeQA-mini. Results should be comparable to the paper's Table 5.
