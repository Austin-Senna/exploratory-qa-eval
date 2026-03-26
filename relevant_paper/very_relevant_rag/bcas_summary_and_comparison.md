# BCAS Paper Summary & Comparison to Our Work

**Paper:** "Quantifying the Accuracy and Cost Impact of Design Decisions in Budget-Constrained Agentic LLM Search"
**Authors:** Kyle A. McCleary & James M. Ghawaly (LSU)
**ArXiv:** 2603.08877v1 (9 Mar 2026)
**Code:** https://github.com/kmccleary3301/BCAS_RAG

---

## 1. What BCAS Is

A **controlled measurement harness** for agentic RAG under explicit budget constraints. Not a new trained agent or SOTA claim — the contribution is isolating which design choices matter when search calls and completion tokens are capped.

**Three architectural principles:**
- **Explicit budget management:** remaining search + token counts surfaced to the model at every step; search tool removed from action list once exhausted
- **Composable component pipeline:** retrieval tools, planning hooks, reflection toggled via config — enables clean ablations
- **Model-agnostic design:** single shared prompt template across all 6 LLMs, no per-model tuning

---

## 2. Experimental Setup

| Dimension | BCAS |
|---|---|
| Models | o4-mini, DeepSeek V3 (0324), GPT-4.1-mini, Gemma 3 27B, Qwen 3 14B, LLaMA 3.1 8B |
| Datasets | TriviaQA, HotpotQA, 2WikiMultihopQA (~467–537 samples each) |
| Retrieval | BM25 baseline → Hybrid (BM25+vector, BGE-M3) → HS+Rerank (100 candidates → top-5 via bge-reranker-v2-m3) |
| Planning | Optional pre-planning (question → step-by-step plan before search) |
| Reflection | Optional mid-search strategy review |
| Budget levers | `max_searches` ∈ {1, 2, 3, unlimited}; `max_total_tokens` ∈ {500, 1K, 2K, 4K, 16K} |
| Eval metric | Binary LLM judge (GPT-4o-mini); manually validated 97–100% accuracy on 600 samples |

**IR stack:** ParadeDB (PostgreSQL), BGE-M3 embeddings, cosine similarity, bge-reranker-v2-m3 cross-encoder.
**Key design choice:** Final context window fixed at **top-5 chunks** to keep search policy (not context flooding) as the primary lever.

---

## 3. Key Findings

### RQ1 — Model Size
- Iterative search **narrows capacity gaps**: smaller models with more searches can match larger models at single-search
- Qwen 3 14B (unlimited + planning) = 75.33% on HotpotQA, exceeding o4-mini at 1 search (70.17%) but not at 2 (86.05%)

### RQ2 — Component Tuning (HotpotQA ablation, net accuracy shift vs. BM25 baseline)

| Component | Avg gain | Notes |
|---|---|---|
| HS+Rerank | **+9.29 pts** | Most consistent; 6–18 pts depending on model |
| Hybrid Search | +6.36 pts | Strong baseline improvement |
| Plan+RF | +6.40 pts | Planning + reflection combined |
| Planning only | +5.69 pts | |
| Reflection only | +4.71 pts | |

- **Smaller models benefit most** from planning (+4–12 pts); o4-mini gains <1.1 pts (redundant with internal CoT)
- Combining plan+reflection can slightly *degrade* some models (adaptive re-planning counter-productive mid-search)

### RQ3 — Accuracy-Budget Tradeoff
- Accuracy improves **monotonically with search steps, plateaus at ~3 searches** across all models/datasets
- Context scaling is **dataset-dependent**:
  - TriviaQA: flat across all token budgets (retrieval-easy)
  - HotpotQA: sharp lift from 4K→16K tokens (synthesis-bound)
  - 2WikiMultihopQA: retrieval-bound — benefits more from search depth than token budget
- **Surprising finding:** tight token budgets (500–2K) + multiple searches can **outperform** large single-search allocations — constrained models make efficient tool calls; unconstrained models generate verbose single responses

### Deployment Recommendation
**Priority order:** search depth first → retrieval quality (HS+RR) → completion budget (only for synthesis-heavy tasks)

---

## 4. Limitations Acknowledged by Authors
- Ablation only on HotpotQA — ordering may not generalize
- Single prompt template (not per-model tuned) — cross-model comparisons measure scaffold sensitivity, not best-case
- No non-agentic single-pass baseline
- No RL-trained agent comparison
- Static benchmark corpora (no open-web, no multilingual, no multimodal)
- Binary judge metric misses partial correctness

---

## 5. Comparison to Our Paper (LakeQA)

### Where We Are Aligned

| Claim in BCAS | Status in our paper |
|---|---|
| Explicit budget constraints matter | ✅ We enforce 30-tool-call hard cap (identical philosophy) |
| Hybrid+rerank is the strongest retrieval component (+9.29 avg) | ✅ Directly motivates our **Condition A** (hybrid RRF + cross-encoder reranker) |
| Planning helps smaller models most | ✅ Partially motivates **Condition B**; we test Haiku vs. Sonnet |
| Search depth saturates early (~3 calls) | ✅ Our search depth curve analysis (`fig10_search_depth_curve.pdf`) — same saturation finding expected |
| Retrieval bottleneck > reasoning bottleneck on hard multi-hop | ✅ This is our **primary thesis** — LakeQA paper finds document discovery is the primary bottleneck |

### Where We Go Further / Differ

| Dimension | BCAS | Our Work |
|---|---|---|
| **Task type** | Standard multi-hop QA (HotpotQA etc.) — given document corpus, known gold answers | **Data lake QA** — open-ended, 1M+ doc search space, structured + unstructured government data, SQL execution required |
| **Search space** | Closed per-dataset corpus (~500K docs max) | Open data lake (>1M docs, heterogeneous schemas) |
| **Answer format** | Short factoid | Numerical/analytical — requires data download, code execution, joins |
| **Metric** | Binary judge (LLM grader) | **Exact Match + Dacc P/R/F1 + Dret P/R/F1** — far more demanding, measures retrieval quality separately from answer quality |
| **Budget constraint** | search cap + token cap (explicit signal to model) | 30 tool calls (all tool types, not just search) — more realistic multi-tool budget |
| **Planning mechanism** | Pre-planning prompt + optional reflection | Condition B: persistent `plan()` tool (writes to system prompt, updates across turns) + 3 skills plugins + context summarization + stagnation detection |
| **Retrieval comparison** | BM25 vs. Hybrid vs. HS+RR (ablation) | Condition A (hybrid RRF + reranker) vs. Condition B (BM25 + planning scaffold) vs. Baseline — **disentangles search quality from planning quality** |
| **Models** | 6 models incl. reasoning models (o4-mini) | Claude Haiku 4.5, Claude Sonnet 4.5, Llama 3.3 70B — focused on production-tier models |
| **Dataset scale** | 467–537 tasks per benchmark | 135 tasks (mini), 1005 tasks (full) — fewer but harder |
| **Difficulty type** | Multi-hop reasoning | Multi-hop + dataset discovery + schema matching + code execution |

### Key Differentiation for Paper Positioning

**BCAS answers:** "Which search/planning *components* give the most accuracy per search call on standard QA?"
**Our paper answers:** "Does better search infrastructure or better planning scaffolding matter more for agents operating over real data lakes?"

BCAS's retrieval bottleneck finding supports our thesis, but their setting doesn't expose the **dataset discovery problem** (finding the right table among 1M+ docs with heterogeneous schemas). In our setting, Dacc recall (did the agent retrieve the right datasets?) is the primary driver of EM — the retrieval challenge is qualitatively harder.

**Points to cite from BCAS:**
1. Hybrid+rerank +9.29 pts avg (validates Condition A design choice — Section X, related work / motivation)
2. Planning helps smaller models 4–12 pts (validates Condition B design for Haiku)
3. Search saturation at ~3 calls (motivates our search depth curve analysis — our data lakes require more calls, interesting contrast)
4. Tight token budget + multiple searches > large single-search (validates our 30-call shared budget design)

### Potential Weakness in Our Paper That BCAS Highlights
- BCAS uses a **single shared prompt template** across models and flags this as a limitation. We also use condition-level prompts, not per-model tuning — we should acknowledge this similarly.
- BCAS's ablation is HotpotQA-only; we should not over-generalize BCAS numbers to our setting, but the directional findings hold.

---

## 6. Citation Recommendation

Cite in **Related Work** (agentic RAG / budget-constrained search) and in **Results Discussion** when interpreting Condition A vs. Condition B outcomes:

> McCleary & Ghawaly (2026) find that hybrid retrieval with re-ranking yields +9.29 points average on HotpotQA and that planning helps smaller models by 4–12 points but has negligible effect on strong reasoning models. Our results on LakeQA [compare/contrast finding here].
