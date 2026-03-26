# Paper Analysis Notes
# Relevant Papers: very_relevant_rag/

---

## Paper 1: BrowseComp-Plus (2603.08877v1.pdf)
**"A More Fair and Transparent Evaluation Benchmark"**
University of Waterloo, CSIRO, CMU

### Setup
- Fixed 100,195-doc corpus, 830 queries, human-verified evidence
- Explicitly separates retrieval effectiveness from reasoning capability
- Metrics: Accuracy (LLM-as-judge), Recall, **Search Calls per query**, Calibration Error, Citation metrics

### Key Numbers
- Avg 6.1 evidence docs / query; avg 76.28 negative docs / query; avg 2.9 gold docs / query
- 86.5% of queries have gold answer in top-5 retrieved docs (512-token truncation)

### Search Calls vs. Accuracy (Table 1)
| Model | Retriever | Accuracy | Recall | Search Calls |
|-------|-----------|----------|--------|--------------|
| gpt-5 | Qwen3-8B | 70.12% | 78.98% | 21.74 |
| o3 | Qwen3-8B | 63.49% | 73.24% | 23.97 |
| gpt-4.1 | Qwen3-8B | 35.42% | 36.89% | 8.67 |
| Search-R1-32B | Qwen3-8B | 10.36% | 10.17% | 1.69 |
| Qwen3-32B | Qwen3-8B | 0.94% | 7.80% | 0.94 |

Better retrieval → fewer search calls AND higher accuracy (stronger model uses search more effectively).

### Retrieval Quality (Table 2) — Recall@5 / Recall@100 / nDCG@10
- BM25: 1.2% / 4.7% / 1.6
- Qwen3-Embed-8B: 14.5% / 47.7% / 20.3
- ReasonIR-8B: 12.2% / 43.6% / 16.8

### Surprising Findings
- Open-source models (Qwen3-32B, Search-R1) make <2 searches even when budget allows — "learned frugality"
- Oracle setting: gpt-4.1 hits 93.49% with perfect retrieval (vs. 35.42% normally) — proves retrieval is the bottleneck
- Citation precision: Qwen3-8B retriever → 83.4%; BM25 → 37.0%

### Analysis Dimensions to Adopt
- Track **search calls per task** as a first-class metric
- Track **retrieval recall@k** independently from answer accuracy
- Calibration error: does model's confidence match actual accuracy?
- Citation precision/recall: did agent cite the sources it actually used?

---

## Paper 2: BCAS — Budget-Constrained Agentic LLM Search (2603.02473v1.pdf)
**Kyle McCleary, James Ghawaly — Louisiana State University**
LREC 2026

### Setup
- Budget-constrained harness: hard-caps search tool, surfaces remaining budget to model
- 6 LLMs × 3 benchmarks (TriviaQA, HotpotQA, 2WikiMultihopQA)
- Budget dimensions: search depth (1/2/3/unlimited), token budget (500/1K/2K/4K/16K)

### Search Depth Scaling — HotpotQA (multi-hop synthesis)
| Model | 1 Search | 2 Searches | 3 Searches | Unlimited | +Planning | +Planning+Reflection |
|-------|----------|-----------|-----------|-----------|-----------|-------------|
| o4-mini | 70.17% | 86.05% | 86.70% | 92.92% | 91.43% | 92.36% |
| DeepSeek V3 | 60.95% | 72.02% | 80.48% | 77.94% | 83.74% | 82.87% |
| GPT-4.1-mini | 66.38% | 74.30% | 78.16% | 80.47% | 85.10% | 84.73% |
| LLaMA 3.1 8B | 49.68% | 61.03% | 63.38% | 65.31% | 69.83% | 70.52% |

**Pattern**: Diminishing returns after 3 searches. Planning adds ~5-11 pts for small models, ~0-1 pt for o4-mini.

### Component Ablation (HotpotQA, avg across models)
| Component | Avg Gain |
|-----------|----------|
| Pre-planning | +5.69 pts |
| Reflection | +4.71 pts |
| Hybrid Search | +6.36 pts |
| Hybrid + Re-ranking | +9.29 pts |

**Hybrid + re-ranking is the single biggest lever** (+9.29 avg) — bigger than planning or reflection.

### Task Type Sensitivity
- **Retrieval-bound** (2WikiMultihopQA): More searches > more tokens
- **Synthesis-bound** (HotpotQA): More tokens helps after ~3 searches
- **Saturation** (TriviaQA): Single search often sufficient; budget scaling flat

### Surprising / Non-Obvious Findings
- Moderately restrictive token budget BEATS generous budget in some configs: GPT-4.1-mini at 500 tokens beats 16K tokens on some tasks — budget awareness > raw context size
- o4-mini anomaly: barely responds to planning/reflection (<1.1 pt HotpotQA), BUT +25 pts on 2WikiMultihopQA — task type determines whether reasoning helps
- Smaller models benefit 4-12x more from retrieval enhancements than larger models

### Analysis Dimensions to Adopt
- **Search depth curve**: plot accuracy at 1, 2, 3, 5, 10, 30 search calls (find saturation point per task type)
- **Planning impact by model size**: measure delta from planning on small vs. large models
- **Token budget × search depth interaction**: don't analyze in isolation
- Label tasks as retrieval-bound vs. synthesis-bound (drives which budget axis matters)

---

## Paper 3: Diagnosing Retrieval vs. Utilization Bottlenecks (2508.06600v1.pdf)
**Boqin Yuan (UCSD), Yue Su (CMU), Kun Yao (UNC)**
MemAgents Workshop, ICLR 2026 — LoCoMo dataset (1,540 questions)

### Setup
3×3 factorial: write strategy (Basic RAG / Extracted Facts / Summarized Episodes) × retrieval (Cosine / BM25 / Hybrid+Rerank)
Three diagnostic probes at retrieval-to-generation boundary.

### Central Result — Retrieval Dominates (Table 1)
| Write Strategy | Cosine | BM25 | Hybrid+Rerank | Avg |
|----------------|--------|------|----------------|-----|
| Basic RAG | 77.9% | 59.2% | 81.1% | 72.7% |
| Extracted Facts | 72.2% | 49.4% | 77.3% | 66.3% |
| Summ. Episodes | 70.1% | 62.7% | 73.3% | 68.7% |

- **Retrieval method**: 20-point spread (Hybrid vs. BM25)
- **Write strategy**: 3-8 point spread
- Retrieval effect is **3-5× larger** than write strategy effect

### Failure Mode Analysis (Table 2)
| Config | Retrieval Failure | Utilization Failure | Hallucination |
|--------|-------------------|---------------------|---------------|
| Basic RAG + Hybrid | 11.4% | 6.2% | 1.2% |
| Basic RAG + BM25 | 35.3% | 5.1% | 0.4% |
| Ext. Facts + BM25 | 46.3% | 3.9% | 0.5% |

Hybrid re-ranking cuts retrieval failures by ~3× vs. BM25.

### Three-Probe Diagnostic Framework
1. **Probe 1 — Retrieval Relevance**: Precision@k (LLM judge rates retrieved docs)
2. **Probe 2 — Memory Utilization**: Classify retrieved context as Beneficial/Harmful/Ignored/Neutral
3. **Probe 3 — Failure Classification**: Retrieval failure / Utilization failure / Hallucination

### Key Correlations
- Retrieval Precision@k ↔ Accuracy: r = 0.98 (near-perfect) — can use retrieval precision as early proxy
- When relevant context is surfaced, LLM uses it 79% of the time (high utilization)
- Ignored rate: only 6.6% — model *does* use what it retrieves, when retrieval is good

### Surprising Findings
- Raw chunking (Basic RAG) beats Extracted Facts and Summarized Episodes consistently
- Expensive write strategies (1-3 LLM calls/session) are not worth the cost
- Implication: Condition B's planning doesn't compensate for inferior retrieval — retrieval quality is structural

---

## New Analysis Ideas for Our Harness

### HIGH PRIORITY

**1. Search Calls Per Task (new metric, not currently tracked)**
Currently `efficiency.py` tracks `tool_calls_total`. Need to also extract *search-only* calls separately.
- Tools that count: `search_sparse`, `search_hybrid`, `search_graph` (Cond A), `search_sparse` (Cond B), `search`, `search_keyword` (baseline)
- Report: mean search calls per task, distribution (p50/p90/p99), search calls vs. EM scatter
- Analogous to BrowseComp-Plus Table 1 — key axis for the paper

**2. Search Depth Curve (budget sensitivity)**
Does accuracy increase with search calls? At what point do we get diminishing returns?
- Bin tasks by total search calls used (1, 2-3, 4-6, 7-10, 11-30)
- Plot mean EM per bin, per condition
- Analogous to BCAS Table 1 — reveals retrieval-bound vs. synthesis-bound tasks

**3. Retrieval Precision@k (already implemented)**
`discovery_metrics.py` already computes per-call precision/recall from `result_dataset_ids` in traces, and `compute_tools_discovery()` breaks this down per tool. Also reports `avg_search_calls` in aggregate. No new work needed — just ensure this is surfaced in `run_analysis.py` / `generate_figures.py`.

**4. Search-Only Failure Attribution (extend failure_attribution.py)**
Currently `search_failed` vs. `search_not_read` are two buckets. Refine:
- `search_failed_budget`: search failed AND agent hit the 30-call budget
- `search_failed_quality`: search failed AND budget was not exhausted (retrieval quality issue, not budget issue)
- This directly tests the BCAS finding: is budget the bottleneck, or retrieval quality?

### MEDIUM PRIORITY

**5. Search Call Efficiency = EM / search_calls**
Measures "information value per search" — Condition A should score higher if tools are genuinely better.
A condition that achieves same EM with fewer searches is more efficient.

**6. Planning Overhead vs. EM Delta (Condition B specific)**
Condition B adds generate_plan / generate_reflective_plan (excluded from 30-call budget).
Track: does planning token overhead correlate with EM gains? (Does plan quality predict task success?)
From BCAS: pre-planning gains 5.69 pts avg; reflection 4.71 pts avg — but these vary by model.

### LOWER PRIORITY / FUTURE

**7. Calibration Error**
Does model's final confidence (if we log it) match actual EM? From BrowseComp-Plus.
Requires storing a confidence field in agent_results.jsonl.

**8. Citation Precision/Recall**
Already track `sources_used`. Add: precision (were cited sources actually gold datasets?) and recall (were all gold datasets cited?).
From BrowseComp-Plus: BM25→37% citation precision vs. dense→83% — directly comparable axis.

**9. BM25 vs. SPLADE Search Call Count**
Condition B supports `SEARCH_SPARSE_BACKEND` = bm25 or splade. Are search calls different?
From Paper 1: BM25 recall@5=1.2% vs. dense=14.5% — this would show up as more searches needed with BM25.

---

## Summary of What's Missing from Current Analysis

| Gap | Where to fix | Priority |
|-----|-------------|----------|
| Search calls tracked separately from all tool calls | `efficiency.py` → new `search_calls.py` | HIGH |
| Search depth curve (accuracy vs. #searches) | New `analysis/search_depth.py` | HIGH |
| Retrieval precision@k | Already in `discovery_metrics.py` — done | — |
| Budget exhaustion vs. quality failure distinction | `failure_attribution.py` | MED |
| Search efficiency (EM / search_calls) | New metric in any summary script | MED |
| Planning overhead correlation | New analysis for Condition B | MED |
| Utilization rate (retrieved → actually used) | Already covered by D_acc | — |
| Retrieval-bound vs. synthesis-bound task labels | Not needed | — |
