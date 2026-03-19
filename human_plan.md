# Implementation Plan: Tools or Thinking? Eval Harness

## Repo: EXPLORATORY-QA-EVAL
## Agent: Claude Code (Opus)
## Deadline: March 23, 2026 AoE (~4 days)

---

## Phase 0: Orientation & Setup (Day 1 morning)

### 0.1 Understand existing code
- Read `strands_evaluation/` — understand the current agent loop, how tools are registered, how tasks are loaded from `tasks_mini/`
- Read `human_agent.py` — understand the baseline tool interface (search, list_files, download, inspect_file, execute_code, submit_answer)
- Read `external-tools/simple_bm25/` and `external-tools/simple_hybrid_search/` — understand the current index format, API shape, what's already indexed
- Read `external-tools/rag-anything/` — understand what's built, whether the knowledge graph is already constructed over the lake
- Identify: what is the current `search` tool's backend? Is it the LAKEQA default ontology keyword search, or already one of these?

### 0.2 Environment
- Confirm AWS credentials / S3 access for the data lake
- Confirm API keys: Anthropic (Haiku, Sonnet), OpenAI (GPT-5-mini), together/vllm for Llama-3.3-70B
- Confirm Strands SDK version, check that `AgentResult` exposes `elapsed_time`, `cycle_count`, `tool_metrics`, `cost_usd`
- Set up `.env` with all keys and endpoints

---

## Phase 1: Index Construction (Day 1)

### 1.1 Tier 1 Index (must-have, no LLM calls)
Build one document per dataset:
```
{
  "dataset_id": "...",
  "text": "{title}\n{schema_name}\n{col1}, {col2}, ...\nSample values: {tfidf_val1}, {tfidf_val2}, ..."
}
```

- [ ] Script: `build_index_tier1.py`
  - Input: Parquet column profiles (you said 1.2 GB precomputed — confirm these exist)
  - For each dataset: concatenate title + schema + column names + top 3-5 TF-IDF sampled string values per column
  - Output: JSONL file, one doc per dataset
  - Skip numerical columns for TF-IDF sampling
- [ ] Ingest into SPLADE index (`external-tools/simple_bm25/` or wherever the SPLADE server lives)
- [ ] Ingest into hybrid search index (`external-tools/simple_hybrid_search/`)
- [ ] Verify: run 5 known queries from `tasks_mini/`, confirm gold datasets appear in top-20

### 1.2 Tier 2 Index (stretch goal, requires LLM calls)
Only if Tier 1 is done and working by end of Day 1:
- [ ] Script: `build_index_tier2.py`
  - For each dataset, call Claude Haiku with column profiles + sample rows
  - Prompt 1: Generate AutoDDG SFD (keyword-rich, synonym-packed description)
  - Prompt 2: Expand abbreviated column names (PLN_END_DT → Planned End Date)
  - Prompt 3: Extract temporal/spatial coverage as natural phrases
  - Concatenate into enriched document
  - Output: JSONL, same schema as Tier 1 but richer text
- [ ] Estimate token cost before running (count input tokens across all datasets × Haiku pricing)
- [ ] Re-ingest into both indices
- [ ] Same verification: 5 known queries, compare rank positions vs Tier 1

---

## Phase 2: Strands Agent — Condition A (Day 1 afternoon → Day 2 morning)

### 2.1 Tool definitions
Create three search tools as Strands tool functions:

- [ ] `tools/search_sparse.py` — wraps SPLADE-v3 endpoint
  - Input: query string
  - Output: list of {dataset_id, title, snippet, score}
  - Returns top-10 results
  
- [ ] `tools/search_hybrid.py` — wraps hybrid search endpoint  
  - Input: query string
  - Output: same schema
  - Internally: dense + SPLADE fusion → cross-encoder rerank → top-10
  
- [ ] `tools/search_graph.py` — wraps RAG-Anything endpoint
  - Input: query string
  - Output: same schema
  - Check: is RAG-Anything already built and serving? If not, this is the riskiest piece — may need to fall back to 2 backends

- [ ] Shared tools (unchanged from baseline): `list_files`, `download`, `inspect_file`, `execute_code`, `submit_answer`

### 2.2 Condition A agent
- [ ] `agents/condition_a.py`
  - Strands agent with all 3 search tools + shared tools
  - System prompt: task preamble + tool descriptions + output format
  - Context management: basic sliding window (last K=5 turns)
  - No skills plugin, no plan generation tool
  - Model parameterized (pass via config)

### 2.3 Instrument decorator
- [ ] `instrumentation/sidecar.py`
  - Decorator that wraps any tool function
  - Logs to JSONL: task_id, turn, tool name, query, query_length_tokens, latency_ms, num_results, result_dataset_ids, gold_dataset_ids_in_results, gold_rank, timestamp_ms
  - Gold overlap computed by passing gold_dataset_ids into the decorator at task init
  - Must not modify the tool's return value or Strands' internal metrics

---

## Phase 3: Strands Agent — Condition B (Day 2)

### 3.1 Skills plugin
- [ ] `plugins/skills.md`
  - Strands skills format (check https://strandsagents.com/docs/user-guide/concepts/plugins/skills/)
  - Content: data lake organization, naming conventions, metadata patterns, search strategies
  - This is the document that gets injected into the system prompt
  - **Critical check**: does this leak retrieval information? It should describe *how to search*, not *what to search for*. No dataset-specific hints.

### 3.2 Planning tools
- [ ] `tools/generate_plan.py`
  - Input: question string
  - Output: structured plan (sub-tasks with search strategies)
  - Implementation: LLM call (same model as the agent) with a planning prompt
  - Plan gets appended to the system prompt as persistent context

- [ ] `tools/generate_reflective_plan.py`
  - Input: none (reads current plan + conversation history from context)
  - Output: revised plan
  - Replaces previous plan in system prompt

### 3.3 Condition B agent
- [ ] `agents/condition_b.py`
  - Strands agent with ONLY `search_sparse` + shared tools + `generate_plan` + `generate_reflective_plan`
  - Skills plugin loaded at init
  - System prompt: same skeleton as Condition A (matched structure, within 10% token count)
  - Same sliding window context management as Condition A (this is the baseline for both)

### 3.4 Prompt matching
- [ ] Write both system prompts side by side
- [ ] Count tokens for each, confirm within 10%
- [ ] If Condition B is shorter (no tool descriptions for hybrid/graph), pad with additional task context
- [ ] Save both prompts as version-controlled files: `prompts/condition_a.txt`, `prompts/condition_b.txt`

---

## Phase 4: Eval Runner (Day 2 afternoon)

### 4.1 Runner script
- [ ] `run_eval.py`
  - Args: `--condition {a,b,c}`, `--model {haiku,sonnet,gpt5mini,llama70b}`, `--tasks_dir tasks_mini/`, `--output_dir results/`
  - For each task in tasks_dir:
    1. Load task (question, gold answer, gold dataset IDs, reasoning chain)
    2. Init agent with appropriate condition config
    3. Pass gold_dataset_ids to sidecar decorator for overlap tracking
    4. Run agent, capture AgentResult
    5. Write sidecar JSONL to `results/{condition}/{model}/{task_id}.jsonl`
    6. Write AgentResult summary to `results/{condition}/{model}/agent_results.jsonl`
  - Resume support: skip tasks that already have output files
  - Error handling: catch agent timeouts/crashes, log as failed, continue

### 4.2 Cost guard
- [ ] Per-task cost check: if `AgentResult.cost_usd` exceeds threshold (e.g., $2/task for Haiku, $5/task for Sonnet), kill and log
- [ ] Running total cost tracker printed to stdout after each task
- [ ] Abort flag: if cumulative cost exceeds $250 for a condition×model pair, stop

---

## Phase 5: Run Experiments (Day 2 evening → Day 3)

### 5.1 Haiku runs (~$200 budget)
- [ ] Condition A × Haiku (135 tasks) — estimate ~$100
- [ ] Condition B × Haiku (135 tasks) — estimate ~$100
- [ ] Spot-check: after 10 tasks each, verify sidecar traces are logging correctly, EM is computable, costs are in range
- [ ] If costs are way under estimate, proceed to Sonnet immediately

### 5.2 Sonnet runs (~$250-300 budget)
- [ ] Condition A × Sonnet (135 tasks)
- [ ] Condition B × Sonnet (135 tasks)
- [ ] Monitor costs closely — Sonnet is the expensive one

---

## Phase 6: Analysis (Day 3)

### 6.1 Analysis scripts
- [ ] `analysis/compute_em.py` — EM per condition × model
- [ ] `analysis/discovery_metrics.py` — D_ret, D_acc, precision/recall/F1 per condition × model
- [ ] `analysis/failure_attribution.py` — classify each failed task into search/discovery-reasoning/execution/hallucination
- [ ] `analysis/provenance.py` — for Condition A: per-backend unique contribution to D_ret
- [ ] `analysis/behavioral.py` — tool switching rates (A), query drift (B), adaptation effectiveness
- [ ] `analysis/efficiency.py` — cost, runtime, latency distributions, latency vs query length
- [ ] `analysis/generate_figures.py` — all paper figures: main results table, stacked failure bars, provenance pie/bar, latency scatter

### 6.2 Key figures
1. **Table 1**: EM per model × condition (+ baseline column)
2. **Figure 1**: Stacked failure attribution bars (model × condition)
3. **Figure 2**: Discovery provenance — per-backend contribution in Condition A
4. **Figure 3**: Latency vs query length scatter, split by backend
5. **Table 2**: D_ret and D_acc recall per condition × model
6. **Table 3**: Cost and runtime per condition × model

---

## Phase 7: Write Paper (Day 3 evening → Day 4)

- [ ] Fill in [TBD] sections: abstract, results, conclusion
- [ ] Results section: narrate the main finding, failure attribution, provenance, behavioral
- [ ] Discussion: which lever matters more, model-dependent effects, practical recommendations
- [ ] Limitations: update based on what actually happened (Tier 1 vs Tier 2, 2 models vs 4, etc.)
- [ ] Format check: ACL style, 8 pages, refs don't count
- [ ] Submit

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| RAG-Anything not ready / KG not built | Condition A drops to 2 backends | Run with SPLADE + hybrid only; note in limitations. Still tests tools vs planning. |
| Sonnet costs blow past budget | Only get Haiku results | Haiku-only paper is still publishable at a workshop. Frame as "efficient model" study. |
| SPLADE index doesn't cover all gold datasets | Condition B is unfairly disadvantaged | Pre-check: run gold dataset IDs against index, report coverage. If <80%, the finding itself is interesting (tools matter). |
| Tier 2 enrichment too expensive / slow | Stuck on Tier 1 index | Tier 1 is the planned baseline. Note in limitations. |
| Strands SDK doesn't expose cost_usd for non-Anthropic models | Missing cost data for GPT-5-mini / Llama | Compute manually from token counts × published pricing. Only relevant if you run step 3. |
| 4-day deadline too tight | Incomplete results | Priority order: Phase 1 → 2 → 3 → 4 → 5.1 → 6 → 7. Everything after 5.1 is the minimum viable paper. |

---

## Minimum Viable Paper (if everything goes wrong)

Haiku only, Tier 1 index, 2 backends (SPLADE + hybrid, no graph), Conditions A + B. That's still a controlled comparison of tools vs planning on a real data lake benchmark with failure attribution. Budget: ~$200. Leaves $300 buffer for retries.