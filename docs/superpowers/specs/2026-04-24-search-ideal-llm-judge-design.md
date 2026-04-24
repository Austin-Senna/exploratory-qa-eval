# search_ideal — LLM-as-Judge Redesign

**Date:** 2026-04-24
**Scope target:** `strands_evaluation/tools/external/ideal/search_ideal.py` and minor edits to `strands_evaluation/tools/external/ideal/search_wrapper.py`
**Replaces:** cursor-walk `search_ideal` (source-driven retrieval by fixed plan order)

---

## 1. Motivation

The current `search_ideal` walks the pre-authored `source_sequence` in fixed order and ignores the agent's `query`. Two problems:

1. **Ordering artifact.** When the agent's query implies a specific planned dataset, it has no way to steer to it — the tool returns whichever entry is next in the plan. This creates a brittle dependency on plan-authored order that is orthogonal to what "ideal retrieval" should mean.
2. **Too-loose upper bound.** An "ideal" baseline should still require the agent to form a good query. A cursor that ignores the query is a freebie, not an upper bound — it collapses the retrieval dimension entirely and makes ablation deltas harder to interpret.

The redesign makes `search_ideal` query-driven by interposing a small LLM judge between the agent's query and the planned candidate pool. The judge reads the query plus the remaining (unused) planned candidates and picks the most relevant one. If the query clearly implies an aggregate (year ranges, "all of X", multiple regions), the judge may pick several related candidates in one call. Already-returned candidates are excluded from future calls.

This aligns with the SANA SoK reframe's §6.2 positioning of the legacy `search_ideal` cursor as a "degenerate retrieval strategy factored out" — the judge-based version still fixes the retrieval dimension at "preloaded" (the candidate pool is the plan's authored list), but restores a non-trivial query→pick decision inside that regime.

## 2. Scope

**In scope:**

- Rewrite `search_ideal.py`: replace cursor-walk with LLM-judge sub-agent using Strands "agents-as-tools" pattern.
- Minor edits to `search_wrapper.py`: force `fixed_k=100` for `search_ideal` so the agent's tool-visible signature is `search_ideal(query)`; rewrite the search_ideal description sentence; delete the `ideal_source_driven` strip block.
- Rewrite `test/test_search_ideal.py` with a live-LLM + stub hybrid.
- Add a live-test log sink: `test_logs/search_ideal_judge_samples.jsonl` (gitignored).

**Out of scope:**

- Changes to the plan authoring format or `plan_store.py` schema.
- Changes to other search tools (`search_value`, `search_schema`, `search_reranked`, `search_prefix`).
- Changes to `run_mode_eval.py` CLI axes. The `--search ideal` axis value continues to select `search_ideal`; its behavior changes, but its name and wiring do not.
- New axis value (e.g., `ideal_judge`). The cursor behavior is replaced, not added alongside. Past eval CSVs against the cursor version become non-comparable to new runs; this is accepted.

## 3. Locked design decisions

From the brainstorming session, these are confirmed and non-negotiable without re-discussion:

- **Judge model:** `openai/gpt-5.4-nano` (already aliased in `setup_run.py`).
- **Judge scope per call:** unbounded 1..N picks; default 1; more if query implies aggregation. `top_k` is not exposed to the agent and is not enforced by the judge.
- **Dedup granularity:** per source-entry (each returned `s3_uri` marked used). Multi-file datasets can come back for their remaining entries on later calls.
- **Sub-agent lifecycle:** fresh `Agent(...)` per `search_ideal` call. No caching. No shared message history across calls.
- **Replacement, not addition:** the cursor code path is deleted. `_PLAN_CURSOR`, `_TASK_CONTEXT` (in `search_ideal.py`; the `plan_store.py` copy stays), `_CURRENT_PLAN`, `_require_plan`, `_normalize_top_k`, `_build_file_result`, `_canonical_uri`, `_dataset_id_from_source` either removed or folded into the new code path.
- **Judge tool contract:** one tool, `pick(s3_uris: list[str], reason: str)`, called exactly once; raises `ValueError` on empty/invalid input; Strands handles the re-prompt.

## 4. File layout & module structure

### 4.1 `search_ideal.py`

Net structural change: replace cursor state with judge state. Public API stays stable so no callers need edits.

**Retained public API (signatures unchanged):**

- `set_db_path(path)` — no-op, kept for wrapper compat.
- `set_plans_root(path)` — clears candidate pool + used set.
- `set_task_context(task_context)` — loads plan, populates candidate pool, clears used set; still calls `plan_store._set_task_context_shared(ctx)` so other modules that read `plan_store`'s task-context copy remain correct.
- `reset_state()` — clears all module state.
- `@tool search_ideal(query: str, top_k: int = 100) -> dict` — signature preserved for the wrapper; `top_k` is ignored in the body (`_ = top_k`).

**New private helpers:**

- `_format_judge_prompt(query, remaining) -> str` — user message builder.
- `_build_judge(remaining) -> (Agent, state_dict)` — constructs the sub-agent and its `pick` tool closure per call.
- `_fallback_pick(remaining) -> list[str]` — returns `[remaining[0][0]]` when the judge fails to pick.

**Removed:**

- `_PLAN_CURSOR`, `_TASK_CONTEXT`, `_CURRENT_PLAN`, `_require_plan`, `_normalize_top_k`, `_build_file_result`.
- The cursor-walk loop and its payload fields (`plan_step_indices`, `plan_step_numbers`, `plan_steps_total`, `dataset_ids`, `plan_step_index`, `plan_step_number`, `dataset_id`, `task_id`, `plan_path`, `ideal_source_driven`).

**Retained (needed for candidate materialization):**

- `_S3_PREFIX`, `_canonical_uri`, `_dataset_id_from_source`. Used inside `set_task_context` to transform each `source_sequence` entry into an `(s3_uri, dataset_id)` tuple for `_CANDIDATES`.

### 4.2 `search_wrapper.py`

Three small edits:

1. **`_wrap_query_tool`** — when `tool_name == "search_ideal"`, override the effective `fixed_k` to `100` regardless of the caller's `fixed_k`. The existing `if fixed_k is not None:` branch then emits a `_wrapped(query: str)` signature, which is what the agent sees. `--k` no longer affects `search_ideal`.
2. **`_compose_description`** — replace the current `search_ideal` special-case sentence (lines 370–372) with: `"Returns the planned sources most relevant to your query. Count is chosen automatically based on query intent."`. Drop the "up to K" claim.
3. **`reshape_search_payload`** — delete the `if payload.get("ideal_source_driven"):` strip block (lines 337–347). The new payload emits no noise keys; nothing to strip.

No other edits to `search_wrapper.py`.

## 5. Module-level state & lifecycle

```python
_CANDIDATES: list[tuple[str, str]] = []   # (s3_uri, dataset_id), populated from plan.source_sequence
_USED_S3_URIS: set[str] = set()           # mutates during the run
```

**Lifecycle:**

- `set_task_context(ctx)` — `plan = plan_store.load_plan_for_context(ctx)`; materialize `_CANDIDATES = [(canonical_uri(s), dataset_id_from(s)) for s in plan.source_sequence]`; `_USED_S3_URIS.clear()`. The plan dataclass itself is discarded after materialization.
- `set_plans_root(path)` — calls `plan_store.set_plans_root(path)`; clears `_CANDIDATES` + `_USED_S3_URIS`.
- `reset_state()` — clears both globals; calls `plan_store._set_task_context_shared({})` to sync the shared module.

**Concurrency:** `_USED_S3_URIS` is module-level mutable state. The eval framework runs tasks serially per process; `--parallel` spawns subprocesses, not threads. `set_task_context` resets between tasks. No lock needed. A one-line comment documents this assumption above the global.

## 6. Judge sub-agent + `pick` tool

Constructed inline inside `search_ideal` on every call. Closure `state` dict holds the pick result; `pick` writes into it; tool body reads it back after the agent terminates.

```python
def _build_judge(remaining: list[tuple[str, str]]) -> tuple[Agent, dict]:
    valid_uris = {uri for uri, _ in remaining}
    state = {"picked": None, "reason": None}

    @tool
    def pick(s3_uris: list[str], reason: str) -> str:
        """Record the s3_uris most relevant to the query. Call EXACTLY once."""
        if not isinstance(s3_uris, list) or not s3_uris:
            raise ValueError("s3_uris must be a non-empty list of strings")
        bad = [u for u in s3_uris if u not in valid_uris]
        if bad:
            raise ValueError(
                f"Picked s3_uri(s) not in candidate list: {bad}. "
                f"You must pick from the provided list only."
            )
        state["picked"] = list(dict.fromkeys(s3_uris))
        state["reason"] = reason
        return f"Recorded {len(state['picked'])} pick(s)."

    judge = Agent(
        model="openai/gpt-5.4-nano",
        system_prompt=_JUDGE_SYSTEM_PROMPT,
        tools=[pick],
        callback_handler=None,
    )
    return judge, state
```

**System prompt** (module constant `_JUDGE_SYSTEM_PROMPT`):

```
You are a dataset selector. The user gives you a search query and a list of
candidate datasets (each with s3_uri and dataset_id). Call the `pick` tool
exactly once with the s3_uris most relevant to the query. Default to 1. If
the query is clearly aggregate (year ranges, "all of", multiple regions),
pick the matching group. Never pick an s3_uri not in the list.
```

**User message format** (built by `_format_judge_prompt`):

```
Query: <query>

Candidates:
1. s3_uri=s3://lakeqa-yc4103-datalake/datagov/parks/files/trees.csv  dataset_id=parks
2. s3_uri=s3://lakeqa-yc4103-datalake/datagov/crime-2017/files/data.csv  dataset_id=crime-2017
...
```

Indices in the list are display-only. The judge must pass full `s3_uri` strings to `pick`, not indices.

**Validation contract:** `pick` raises `ValueError` on (a) empty list, (b) non-list input, (c) any URI not in `valid_uris`. Strands surfaces tool errors back to the model, producing one re-prompt. If the retry also fails to record a pick, `state["picked"]` remains `None` and the tool body falls back per §8.

## 7. `search_ideal` tool body & data flow

```python
@tool
def search_ideal(query: str, top_k: int = 100) -> dict:
    """Return the planned sources most relevant to `query`. Judge decides count."""
    _ = top_k

    if not _CANDIDATES:
        return {"error": "search_ideal called before set_task_context; no plan loaded."}

    remaining = [(uri, dsid) for uri, dsid in _CANDIDATES if uri not in _USED_S3_URIS]
    if not remaining:
        return {"results": [], "count": 0, "query": query, "plan_exhausted": True}

    judge, state = _build_judge(remaining)
    judge(_format_judge_prompt(query, remaining))

    picked = state["picked"] or _fallback_pick(remaining)  # _fallback_pick logs WARNING internally
    _USED_S3_URIS.update(picked)
    logger.info(
        "search_ideal judge picked %d uri(s) reason=%r",
        len(picked),
        state["reason"],
    )

    dsid_by_uri = dict(remaining)
    results = [{"s3_uri": u, "dataset_id": dsid_by_uri[u]} for u in picked]
    return {
        "results": results,
        "count": len(results),
        "query": query,
        "plan_exhausted": len(_USED_S3_URIS) >= len(_CANDIDATES),
    }
```

**Data flow:** `query + _CANDIDATES − _USED_S3_URIS → judge(with pick tool) → picked URIs → _USED_S3_URIS.update → results → wrapper.reshape_search_payload → agent`.

**Response payload:** `{results, count, query, plan_exhausted}`. Nothing else. `judge_reason` goes to the logger, not the payload. `ideal_source_driven` is deleted entirely (along with its strip block in the wrapper).

## 8. Error handling & edge cases

| Case | Behavior |
|---|---|
| Judge never calls `pick` (token limit / double ValueError / silence) | `state["picked"]` is `None` → `_fallback_pick(remaining)` returns `[remaining[0][0]]`. Log a WARNING so post-hoc audit can count fallbacks. Parent agent still gets a valid result and makes forward progress. |
| Judge picks an invalid URI | `pick` raises `ValueError` → Strands re-prompts once. If retry also fails, falls into the row above. |
| `_CANDIDATES` empty at call time | Return `{"error": "search_ideal called before set_task_context; no plan loaded."}`. Defense in depth — the eval framework's preflight already catches misconfigured runs. |
| All candidates exhausted | Early-return `{results: [], count: 0, query, plan_exhausted: True}`. Judge is never invoked. |
| Judge sub-agent raises (network error, 429, provider outage) | Let the exception bubble out of the `judge(...)` call. Do not swallow into a fallback — silent fallback on provider outage would corrupt eval attribution. Parent agent sees the tool failure like any other. |
| Judge picks the same URI twice in one call | `dict.fromkeys` in `pick` deduplicates, preserving order. Returned as a single entry. |
| Judge picks zero URIs | `pick` raises on empty list → re-prompt. The judge's job is to pick the closest match, not to abstain. |

## 9. Testing

Hybrid: live-LLM tests for quality + plumbing, stub tests for failure-path coverage that a real model can't reliably produce.

### 9.1 Live-LLM tests (`@pytest.mark.llm`, require `OPENAI_API_KEY`)

Each test appends one record per judge call to `test_logs/search_ideal_judge_samples.jsonl` via a `_log_judge_call` helper: `{timestamp, test, query, candidates, picked, reason, count}`.

1. `test_live_single_match` — 11-candidate fixture, query `"crime data in Chicago 2017"`. Assert picked URI's `dataset_id` matches the expected crime-2017 entry.
2. `test_live_aggregation_multi_pick` — fixture with 3 crime-year entries + 8 unrelated. Query `"all years of Chicago crime data"`. Assert ≥2 crime-year URIs picked.
3. `test_live_dedup_across_calls` — two sequential calls with the same query. Assert the second call's picks don't overlap with the first; `_USED_S3_URIS` grows.
4. `test_live_specific_query_ignores_aggregate` — query `"Chicago crime 2017 specifically"` against the same fixture as (2). Assert exactly 1 pick.

### 9.2 Stub tests (always run)

Patch `Agent` construction inside `search_ideal` to return a fake whose `__call__` synchronously invokes its `pick` tool with a preset URI list (or deliberately never invokes `pick`).

5. `test_invalid_pick_raises_in_pick_tool` — direct `pick` invocation with a URI not in `valid_uris`; assert `ValueError`.
6. `test_fallback_pick_on_judge_no_pick` — stub Agent whose judge terminates without calling `pick`. Assert fallback URI returned, warning logged.
7. `test_set_task_context_resets_used` — populate `_USED_S3_URIS`, call `set_task_context(...)`, assert cleared.
8. `test_plan_exhausted_returns_empty` — pre-seed `_USED_S3_URIS` with all candidates; assert early-exit payload; assert stubbed Agent was never constructed.
9. `test_wrapper_hides_top_k_from_agent` — build wrapped search_ideal via `build_search_tools`; assert the wrapped tool's `inputSchema.json.properties` has only `query`, not `top_k`.
10. `test_wrapper_applies_naive_vs_ideal_shaping` — end-to-end with stubbed pick; `results_mode="ideal"` produces an `llm_desc` field, `results_mode="naive"` does not.

### 9.3 CI policy

- Stub tests (5–10) run on every PR.
- Live tests (1–4) are gated behind `pytest -m llm` and run on manual trigger or nightly.
- The jsonl log file is retained as a CI artifact on live runs and is gitignored in working copies.

## 10. Success criteria

- `search_ideal(query)` is the only surface the parent agent sees; `top_k` is invisible.
- `--k` has no effect on `search_ideal`'s behavior.
- `--results naive` and `--results ideal` continue to shape `search_ideal`'s payload richness via the existing wrapper.
- With a clear single-dataset query (live test 1), the judge picks exactly 1 URI whose `dataset_id` matches the expected entry.
- With an aggregate query over the aggregation fixture (live test 2), the judge picks ≥2 URIs.
- With a specific query against an aggregate-capable fixture (live test 4), the judge picks exactly 1 URI.
- Re-calling `search_ideal` after a task's candidates are exhausted returns `{results: [], plan_exhausted: True}` without invoking the judge.
- The cursor-walk code path is fully deleted; `grep _PLAN_CURSOR strands_evaluation/` returns no matches.

## 11. Open questions deferred to implementation

- **Fallback-rate logging aggregation.** Do we want a CSV column in `results/` recording how often the judge fell back? Recommendation: start with just the WARNING log line; add a column later if fallback rate proves interesting.
- **Schema for live-test fixture plan.** The 11-candidate test fixture needs to exist in a stable location under `test/fixtures/` — exact URIs and dataset_ids to be chosen during implementation.
- **Retry count on invalid pick.** Strands defaults to one tool-error re-prompt. If nano-model invalid-pick rates prove high in practice, consider configuring a second retry via Strands agent options.
- **Live-test cost budget.** Four live tests × one judge call each × ~500 tokens ≈ trivial per run, but nightly CI adds up. Recommendation: defer until a month of runs gives real data.
