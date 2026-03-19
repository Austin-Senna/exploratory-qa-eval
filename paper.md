# Tools or Thinking? Disentangling Search and Planning for LLM Agents over Data Lakes

**Target:** ACL 2026 Workshop SURGeLLM  
**Deadline:** March 23, 2026 (AoE)  
**Format:** ACL style, 8 pages + unlimited refs  
**Submission:** Non-archival (LAKEQA is under review at ICML)

---

## Abstract

When an LLM agent fails at exploratory question answering over a data lake, is the bottleneck the quality of its search tools or the sophistication of its planning? We disentangle these factors through a controlled study on LAKEQA, a benchmark of 135 expert-annotated multi-hop questions over a 9.5 TB heterogeneous data lake. We design two complementary conditions: in the **tools-rich** condition, agents have access to a full suite of retrieval backends — SPLADE-v3, hybrid vector search with cross-encoder reranking, and graph-based relational discovery — but use only basic context management; in the **planning-rich** condition, agents are equipped with advanced planning capabilities — a structured skills plugin and explicit plan generation — but are limited to SPLADE-v3 alone. We evaluate four frontier LLMs (Claude Haiku 4.5, Claude Sonnet 4.5, GPT-5-mini, and Llama-3.3-70B) across both conditions and decompose failures into search failures, reasoning gaps, and execution errors. We further introduce per-call instrumentation that captures query-level latency, result provenance, and agent adaptation behavior — enabling fine-grained analysis of tool selection dynamics and query reformulation strategies. Our results reveal [TBD], suggesting that [TBD] is the dominant lever for improving EQA agents. We release our evaluation harness to support future work on agentic data discovery over structured data.

---

## 1. Introduction

### Motivation

Data lakes in enterprise and government settings contain millions of heterogeneous documents — tabular CSVs, metadata JSONs, unstructured text, PDFs. Answering analytical questions over these lakes requires discovering relevant datasets before reasoning over them. LAKEQA (under review) formalizes this as Exploratory QA (EQA): agents must iteratively search and reason over a 9.5 TB lake of ~40M documents from Data.gov and Wikipedia. Even frontier LLMs achieve < 30% exact match, and trace analysis reveals document discovery as the primary bottleneck.

### Research Question

This finding leaves a crucial question open: should we invest in better retrieval tools or better agent planning to close the gap? These are fundamentally different engineering investments — better search means building better indices, embeddings, and graph structures; better planning means improving prompting, context management, and task decomposition.

### Approach

We answer this through a clean A/B design:

- **Condition A (tools-rich):** Agent gets access to SPLADE-v3, hybrid search with cross-encoder reranking, and graph-based discovery (RAG-Anything) — but uses only a basic sliding-window context strategy.
- **Condition B (planning-rich):** Agent gets only SPLADE-v3 — but is equipped with a skills plugin and an explicit plan-generation tool.

Critically, we instrument every tool call with a lightweight wrapper that logs query text, token-level query length, per-call latency, and result dataset IDs — without modifying the underlying agent framework. This enables three analyses that go beyond aggregate EM scores: per-backend discovery attribution (which tool first surfaced each gold dataset), query-length-conditioned latency analysis (testing whether SPLADE's known short-query overhead affects agent behavior), and adaptation strategy comparison (tool switching in Condition A vs. query reformulation in Condition B).

### Contributions

1. A controlled comparison isolating tools vs. planning as factors for EQA, evaluated on a realistic million-scale data lake benchmark
2. Per-call instrumentation framework enabling discovery provenance tracking, latency profiling, and behavioral analysis — implemented as tool wrappers with no framework modifications
3. Cross-model analysis across 4 frontier LLMs showing whether the effect is model-dependent
4. Dual adaptation analysis: tool selection behavior (Condition A) and query reformulation behavior (Condition B) as parallel agent strategies
5. Open-source evaluation harness with modular search backend integration

---

## 2. Methods

### 2.1 Task and Benchmark

We evaluate on LAKEQA-mini (135 tasks), a stratified subset of LAKEQA preserving the distribution of reasoning density. Each task consists of a natural language question requiring multi-hop reasoning over a data lake of ~40M documents (~9.5 TB). Gold annotations include the correct answer, required dataset IDs, and the full reasoning chain.

Agents interact with the lake through LAKEQA's tool interface: `search`, `list_files`, `download`, `inspect_file`, `execute_code`, and `submit_answer`. We modify only the `search` tool's backend implementation across conditions.

### 2.2 Agent Framework

All agents are implemented with the **Strands Agents SDK**, which provides the event loop, tool dispatch, and built-in telemetry we rely on throughout the study. Strands natively records per-task metrics including elapsed time, cycle count, per-cycle durations, per-tool call counts and timings, input/output token counts, and USD cost — all exposed through the `AgentResult` object. This eliminates the need for custom token counting or cost estimation and ensures consistent measurement across all conditions and models.

Strands also provides the **skills plugin system** used in Condition B (Section 2.3). Skills are structured Markdown documents loaded at agent initialization and injected into the system prompt, giving the agent persistent reference knowledge without requiring additional tool calls to access it.

### 2.3 Experimental Conditions

We structure our study around a central question: if you can only improve one thing — the agent's tools or the agent's thinking — which matters more?

#### Condition A — Tools-Rich, Basic Planning

The agent has access to three search backends simultaneously and can choose which to invoke on each search call:

| Tool | Type | What it does | Why it's distinct |
|------|------|-------------|-------------------|
| `search_sparse(query)` | Learned sparse | SPLADE-v3 with learned term expansion over enriched dataset documents | Lexical precision + learned synonym expansion |
| `search_hybrid(query)` | Dense + sparse + reranker | Fused dense embedding (BGE/E5/GTE) + SPLADE retrieval, followed by cross-encoder reranking | Semantic recall for queries with no lexical overlap with target metadata |
| `search_graph(query)` | Graph-based | RAG-Anything: heterogeneous knowledge graph over dataset schemas; retrieves via graph traversal + embedding similarity | Relational discovery — surfaces datasets connected by shared foreign keys and schema overlap, not textual similarity |

These three backends cover complementary failure modes: SPLADE handles term expansion, hybrid handles semantic gaps, and graph handles structural/relational discovery. Context management is basic: sliding-window conversation history truncated to the last K tool-call turns. No explicit planning scaffolding is provided.

#### Condition B — Planning-Rich, Basic Tools

The agent has access to only SPLADE-v3 for search, but is equipped with advanced planning and context management:

| Capability | What it does |
|-----------|-------------|
| **Skills plugin** (`skills.md`) | A Strands skills plugin loaded at agent initialization. Contains a structured reference describing the data lake's organization, common dataset naming patterns, metadata conventions, and effective search strategies. Injected into the system prompt as persistent context — the agent can reference it at any turn without a tool call. |
| `generate_plan(question)` | Tool the agent can invoke to produce a structured decomposition of the question into sub-tasks with explicit search strategies for each. Appended to the system prompt as a persistent plan. |
| `generate_reflective_plan()` | Tool the agent can invoke to revise the current plan based on what has been discovered so far, replacing the previous plan in the system prompt. |

The agent adapts by rewriting queries and replanning rather than switching tools. This is a fundamentally different adaptation strategy from Condition A, and we instrument both.

#### Condition C — Combined (conditional on A/B results)

All tools + all planning on a subset of models. Tests whether effects are additive or one subsumes the other.

### 2.4 Index Construction

All search backends (SPLADE-v3, hybrid, and graph) operate over a shared corpus of **enriched dataset documents** — one document per dataset in the lake. The document construction pipeline determines what textual representation each retrieval backend sees, and is therefore a critical design choice.

We implement two index tiers depending on available compute budget for the enrichment pipeline:

#### Tier 1 (Baseline Index)

Constructed without LLM calls. Each document concatenates:

1. **Dataset title** (from Data.gov metadata)
2. **Schema name / source identifier**
3. **All column names**, verbatim
4. **3–5 TF-IDF-sampled row values per column** — selected by computing TF-IDF scores across all string values in the column and retaining the highest-scoring (most distinctive) entries. Numerical columns are excluded.

This tier can be built entirely offline from Parquet files with no API cost.

#### Tier 2 (Enriched Index)

Extends Tier 1 with LLM-generated content. Each document contains:

1. **Dataset title**
2. **Natural-language description** generated following the AutoDDG Search-Focused Description (SFD) strategy (Zhang et al., 2025): the LLM receives the dataset's column profiles and sample rows, then generates a keyword-rich description packed with synonyms, related concepts, and use-case terms — optimized for search engine indexing rather than human readability.
3. **All column names with abbreviations expanded** into natural language (e.g., `PLN_END_DT` → "Planned End Date", `GEO_CD` → "Geographic Code"). Expansion is performed by an LLM given the column name, data type, and 3 sample values as context.
4. **3–5 representative sample values per categorical/text column**, selected by TF-IDF frequency.
5. **Temporal and spatial coverage as natural phrases** (e.g., "covers January 2015 through December 2023, all US counties"), extracted from column profiles and metadata fields.

The enriched index produces documents that serve both BM25/SPLADE (keyword-dense, synonym-rich) and dense embedding retrieval (natural-language context for semantic matching) from a single shared representation. This follows recent evidence that one NL-enriched document format works for both sparse and dense retrieval without requiring separate index documents (Zhang et al., 2025; Fan et al., 2023).

**Which tier is used in the experiments** depends on the compute budget available for the enrichment pipeline at run time. We report the tier used and note any effect on retrieval quality in the results. If both tiers are feasible, we report Tier 2 as the primary result and include a Tier 1 comparison in the appendix.

Column profiles for both tiers are precomputed by sampling the first 10K rows per dataset from Parquet files, extracting column names, data types, null rates, distinct count ratios, and sample values (1.2 GB index total for Tier 1).

### 2.5 Models

| Model | Type | LAKEQA baseline EM (mini) |
|-------|------|--------------------------|
| Claude Haiku 4.5 | Proprietary (efficient) | 12.59% |
| Claude Sonnet 4.5 | Proprietary (strong) | 25.93% |
| GPT-5-mini | Proprietary (OpenAI) | 11.85% |
| Llama-3.3-70B | Open source | 8.89% |

All 4 models have published LAKEQA baselines using the default ontology keyword search + basic prompting. Our Condition A and B results are directly comparable to these baselines.

### 2.6 Instrumentation

We wrap each search backend and planning tool with a lightweight logger that captures per-call traces without modifying the Strands agent framework or its `EventLoopMetrics`. This produces two complementary trace streams:

**Sidecar traces** (one JSONL file per task): capture per-call details including query text, query length, wall-clock latency, result dataset IDs, gold overlap, and rank positions. For `generate_plan` calls, we additionally log the full plan text and whether it is a replan.

**Strands `AgentResult` metrics** (per task): capture aggregate telemetry including total elapsed time, cycle count, per-cycle durations, per-tool call counts and timings, total input/output tokens, and computed USD cost.

The two streams are joined on `task_id` at analysis time. This dual-stream design lets us analyze fine-grained per-call behavior (from the sidecar) in the context of aggregate task-level performance (from Strands), without modifying either system.

### 2.7 Evaluation

#### 2.7.1 End-to-End

Exact Match (EM) against gold answers, following LAKEQA's protocol.

#### 2.7.2 Data Discovery Metrics

- **D_ret** (retrieval set): all dataset IDs surfaced by any search call, regardless of whether the agent used them. Measures search tool quality.
- **D_acc** (accessed set): dataset IDs the agent actually opened/queried downstream. Measures agent judgment.
- Precision, recall, F1 against gold dataset IDs for both sets.

**Discovery provenance** (new, from sidecar traces): for each gold dataset ID that appears in D_ret, we record which backend first surfaced it and at what rank. This enables per-backend recall decomposition in Condition A — e.g., "graph search uniquely contributed 18% of gold datasets that neither SPLADE nor hybrid found."

#### 2.7.3 Failure Attribution

| Failure type | Detection method |
|-------------|-----------------|
| Search failure | Gold dataset not in D_ret — no tool surfaced it |
| Discovery-reasoning gap | Gold dataset in D_ret but not in D_acc — agent found it but didn't use it |
| Execution error | Correct datasets accessed, wrong answer — code bug, wrong aggregation |
| Hallucination | Agent references datasets or columns that don't exist in the lake |

We report failure attribution as a stacked bar per model × condition, enabling direct comparison of where each condition breaks.

#### 2.7.4 Efficiency

- **Runtime:** total elapsed time (from Strands `AgentResult.elapsed_time`) + per-call latency distribution (from sidecar)
- **Cost:** USD from token usage (from Strands `AgentResult.cost_usd`)
- **Tool calls:** total count + breakdown by backend (from sidecar and Strands `AgentResult.tool_metrics`)
- **Latency vs. query length:** scatter plot of per-call latency against query token count, split by backend. Tests whether SPLADE's short-query overhead (Won et al., 2025) manifests in practice and whether agents adapt to it.

#### 2.7.5 Behavioral Analysis

**Condition A — Tool Selection:**
- Distribution of calls across sparse / hybrid / graph per model
- Whether agents shift toward stronger backends on harder tasks (higher reasoning density)
- Whether tool selection correlates with task success
- Whether latency influences subsequent tool choice (does a slow SPLADE call cause the agent to switch backends?)

**Condition B — Query Reformulation:**
- Query similarity between pre-plan and post-plan search calls (Jaccard or embedding cosine)
- Whether replanning correlates with task success

**Cross-condition comparison:** Condition A agents adapt by switching tools; Condition B agents adapt by rewriting queries. We compare the effectiveness of these two adaptation strategies by measuring D_ret recall improvement from the first search call to the last.

### 2.8 Prompt Optimization

To ensure Conditions A and B are fairly compared, and that differences reflect the structural intervention rather than prompt quality, we follow a manual prompt-matching protocol:

**Matched structure:** Both system prompts use the same template skeleton — identical preamble describing the task, identical instructions for tool calling conventions, identical output format. Only the tool descriptions and (for Condition B) the skills plugin content differ.

**Matched length:** Both prompts are within 10% of each other in token count, padded with task-relevant context if needed, so that neither condition benefits from a longer or shorter prompt.

**Blind review:** A co-author not involved in prompt drafting reviews both prompts side-by-side (with condition labels removed) and flags any asymmetry in specificity, tone, or implicit hints.

All 135 tasks are used for evaluation (no dev holdout). We note in limitations that prompts are hand-written and structure-matched but not automatically optimized; prompt optimization (e.g., via DSPy) is left to future work.

### 2.9 Implementation

All agents are implemented with the Strands Agents SDK. Each search backend is implemented as a modular Strands tool behind a common API (`api.py`, `config.py`, `process.py`). The instrument decorator (Section 2.6) wraps each tool function. The skills plugin for Condition B is implemented as a Strands skills Markdown file loaded at agent initialization per the Strands plugin specification.

---

## 3. Expected Results

### 3.1 Main Comparison: Tools-Rich vs. Planning-Rich

| | Condition A (tools-rich) | Condition B (planning-rich) | LAKEQA baseline |
|---|---|---|---|
| Haiku 4.5 | [TBD] | [TBD] | 12.59% |
| Sonnet 4.5 | [TBD] | [TBD] | 25.93% |
| GPT-5-mini | [TBD] | [TBD] | 11.85% |
| Llama-3.3-70B | [TBD] | [TBD] | 8.89% |

Key comparison per model: EM(A) vs EM(B). If EM(A) > EM(B) consistently → tools dominate. If model-dependent → interesting interaction (e.g., stronger models extract more value from planning).

### 3.2 Failure Attribution

Stacked bar chart per model × condition decomposing failures into search / discovery-reasoning / execution / hallucination. Key questions:

- Condition A: does D_ret recall increase (tools surface more gold datasets) but discovery-reasoning gap persist (agent doesn't use them)?
- Condition B: does the agent make better use of what it finds (smaller gap) but hit a ceiling because SPLADE alone can't surface certain datasets?

### 3.3 Discovery Provenance (Condition A)

Per-backend contribution to D_ret recall:

- What fraction of gold datasets are uniquely surfaced by each backend (only that backend found it)?
- What is the marginal contribution of hybrid and graph over SPLADE alone?
- Does graph search disproportionately contribute on higher-reasoning-density tasks?

### 3.4 Tool Selection and Adaptation Behavior

**Condition A:**
- Call distribution across backends per model
- Tool switching rate: how often does the agent change backends between consecutive turns?
- Latency-conditioned switching: after a slow SPLADE call, does the agent shift to another backend?
- Success correlation: do tasks where the agent uses all three backends succeed more often?

**Condition B:**
- Query drift: how much do search queries change after replanning?
- Success correlation: do tasks with replanning succeed more often?

### 3.5 Efficiency

- Total runtime and cost per condition × model
- Latency distribution per backend, conditioned on query length (testing the SPLADE short-query hypothesis)
- Cycle count comparison: do Condition A agents take more cycles (exploring tools) or fewer (finding datasets faster)?

### 3.6 Condition C: Additivity

- EM(both) vs. max(EM(A), EM(B))
- Does the combined condition reduce search failures (from tools) AND discovery-reasoning gaps (from planning) simultaneously?

---

## 4. Discussion

- **Practical recommendation:** should practitioners invest in better retrieval infrastructure or better agent prompting/architecture? We frame this as a decision tree based on the failure attribution: if your system's bottleneck is search failures, invest in tools; if it's discovery-reasoning gaps, invest in planning.
- **Per-backend value:** which search backend contributes most to the marginal improvement in Condition A? If graph search uniquely surfaces datasets that neither SPLADE nor hybrid finds, that justifies the engineering cost of maintaining a knowledge graph.
- **Model-dependent effects:** do stronger models (Sonnet) extract more value from planning (because they can reason better over a plan) while weaker models (Haiku, Llama) benefit more from tools (because better retrieval compensates for weaker reasoning)?
- **Adaptation strategies:** how do tool switching (Condition A) and query reformulation (Condition B) compare as agent adaptation mechanisms? Which leads to faster convergence on the right datasets?
- **Index construction:** if Tier 2 (enriched) indices are used, how much of the tools-rich condition's advantage (if any) is attributable to the index quality vs. the backend diversity? If Tier 1 results are available, this comparison isolates the effect of LLM-generated descriptions on downstream retrieval.
- **SPLADE latency in agentic settings:** does the short-query overhead observed at billion-scale (Won et al., 2025) manifest in our setting, and does it visibly affect agent behavior?
- **Connection to LAKEQA:** they identified search as the bottleneck; we quantify how much better search needs to be and whether planning can partially compensate.

---

## 5. Limitations

- Single benchmark (LAKEQA-mini, 135 eval tasks)
- Column profiling uses 10K-row sample — may miss rare values
- Prompts are hand-written and structure-matched but not automatically optimized (e.g., via DSPy); prompt optimization is left to future work
- Three search backends; future work could include ColBERT, Aurum, or learned dense retrievers
- Condition B's planning tools are hand-designed; learned planning strategies could perform differently
- `query_length_tokens` in the sidecar uses whitespace splitting as an approximation; should be validated against the actual SPLADE tokenizer for the latency analysis
- Sidecar traces add I/O overhead to each tool call (~1–2ms for JSONL append); negligible relative to search latency but noted for completeness
- If only Tier 1 indexing is feasible, the enriched-document comparison is deferred to future work. Tier 1 documents lack LLM-generated descriptions and column name expansion, which may understate the tools-rich condition's potential.

---

## 6. Conclusion

[TBD — summarize which lever mattered more, key finding from behavioral analysis, release code]

---

## Budget Summary

| Condition | Models | Runs | Est. cost |
|-----------|--------|------|-----------|
| A (tools-rich) | 4 | 540 | ~$430 |
| B (planning-rich) | 4 | 540 | ~$430 |
| C (both, 2 models) | 2 | 270 | ~$250 |
| **Total** | | **~1,350** | **~$1,110** |

### Execution Order

1. **A + B on Haiku only (~$200)** → establishes whether the hypothesis holds
2. **A + B on Sonnet (~$400)** → tests model-dependency
3. A + B on GPT-5-mini + Llama (~$300) → full model coverage
4. C on 2 models with best deltas (~$250) → additivity test

**$500 budget plan:** Execute steps 1–2 only. Haiku and Sonnet bracket the weakest and strongest LAKEQA baselines (12.59% vs 25.93%), maximizing the dynamic range of model capability within budget. Steps 3–4 are deferred pending additional funding.

---

## Appendix: Trace Schema Reference

### Sidecar Trace (JSONL, one file per task)

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | str | LAKEQA task identifier |
| `turn` | int | Agent turn number within the task |
| `tool` | str | Backend name: `search_sparse`, `search_hybrid`, `search_graph`, `generate_plan` |
| `query` | str | Raw query text sent to the backend |
| `query_length_tokens` | int | Approximate token count (whitespace split) |
| `latency_ms` | float | Wall-clock time for this call |
| `num_results` | int | Number of results returned |
| `result_dataset_ids` | list[str] | Ordered list of dataset IDs in results |
| `gold_dataset_ids_in_results` | list[str] | Subset of results matching gold annotations |
| `gold_rank` | list[int] | 1-indexed rank positions of gold datasets |
| `timestamp_ms` | int | Unix timestamp in milliseconds |

**Additional fields for `generate_plan` calls:**

| Field | Type | Description |
|-------|------|-------------|
| `plan_text` | str | Full text of the generated plan |
| `is_replan` | bool | Whether this is a revision of a prior plan |

### Strands `AgentResult` (per task)

| Field | Source | Description |
|-------|--------|-------------|
| `elapsed_time` | Strands | Total task runtime in seconds |
| `cycle_count` | Strands | Number of agent loop cycles |
| `cycle_times` | Strands | List of per-cycle durations |
| `tool_metrics` | Strands | Per-tool aggregate: call_count, success_count, total_time |
| `input_tokens` | Strands | Total input tokens consumed |
| `output_tokens` | Strands | Total output tokens generated |
| `cost_usd` | Computed | USD cost from token usage |

### Join Key

Sidecar traces and Strands metrics are joined on `task_id` at analysis time.