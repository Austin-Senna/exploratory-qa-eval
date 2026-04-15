# Design — Fix snippet/description redundancy in ideal-mode search results

## Context

In `search_results=ideal` (and to a lesser extent `standard`), every
result's `dataset_snippet`/`content` is nearly identical to the accompanying
`description`. Root cause traced to two places:

1. **`external-tools/hybrid_search/process.py:347-354`** inserts a
   "description chunk" (= `generated_metadata + description`) as the first
   chunk per URI in the `lakeqa` content table, *in addition* to the
   actual content chunks on lines 358-367.
2. **`external-tools/hybrid_search/api.py:_fmt` (lines 51-69)** dedupes by
   URI and keeps the *highest-ranked* chunk's text. For NL queries, the
   dense description chunk outranks content chunks, so the surviving
   payload per URI is the description prose.

Net effect: description text is returned twice (once as `description` via
`search_wrapper.py`, once as `dataset_snippet`/`content` via the hybrid
search payload), and the agent never sees actual row data.

We want to fix this without losing the retrieval quality the description
chunk provides for NL queries.

## Design: C3 — `chunk_kind` column, score-by-max, snippet-from-content

Rebuild `lance_data/lakeqa` into a **new sibling DB** (leave the current
`lance_data/` untouched) with a `chunk_kind` column tagging each chunk as
`"description"` or `"content"`. At query time, over-fetch, group by URI,
rank URIs by max chunk score (any kind), and use the best-scoring
*content* chunk as the returned snippet. Fall back to description text
(internally flagged) only when no content chunk exists for a URI.

### New DB path

`lance_data_v2/` (sibling of `lance_data/`, selected via existing
`--db`/`set_db_path` plumbing — no new config surface).

### Fallback tiers

- **T1** (common): URI has ≥1 `chunk_kind='content'` chunk in the
  over-fetched slice → snippet = top-scoring content chunk's text.
- **T2**: URI present in slice only via description chunks → issue a
  targeted filter query `.where("uri = '<uri>' AND chunk_kind =
  'content'").limit(1)` (metadata-only, no embeddings). ~0-3 misses per
  call at `k*3` over-fetch.
- **T3** (rare): URI has no content chunks in the DB at all →
  `document` = description text, `snippet_kind = "description"` flag set
  on the raw payload. **Flag stays internal** (api.py only); wrappers do
  not propagate it to the agent. Used for logging/eval metrics.

### Over-fetch

Fixed multiplier of `3 * k` in `_fmt`'s upstream callers. Hardcoded
constant in `api.py` (e.g. `_OVERFETCH_MULTIPLIER = 3`). No config knob.

## Files to modify

### `external-tools/hybrid_search/process.py`
- `make_table_schema` (line 186) — add `pa.field("chunk_kind", pa.string())`.
- Description-chunk insertion (lines 347-354) — emit
  `chunk_kind="description"` into the row dict added to `state["chunk_*"]`
  (requires restructuring state into dicts or parallel lists; easiest is
  a fourth list `state["chunk_kinds"]`).
- Content-chunk insertion (lines 358-367) — emit `chunk_kind="content"`.
- `flush_chunks` (line 294) — include `chunk_kind` in the `table.add`
  row dicts.
- `lakeqa_schema` table: **no change** — it's already single-purpose
  (description/metadata); add a `chunk_kind` column only if consistency
  matters. Skip for now.

### `external-tools/hybrid_search/api.py`
- All `.select([...])` lists (`sparse_search_schema`,
  `hybrid_search_schema`, `hybrid_search`, `hybrid_search_with_reranker`)
  — include `"chunk_kind"` so `_fmt` can read it.
- Replace `_fmt` with a grouping implementation:
  1. Walk ranked rows, bucket by URI, track per-URI: `max_score`,
     `best_content_chunk_text` (highest-score content chunk), and
     `best_desc_chunk_text` (fallback).
  2. Order URIs by `max_score` descending.
  3. For each top-k URI: if `best_content_chunk_text` present → use it
     (Tier 1). Else issue a targeted `.where(uri AND
     chunk_kind='content').limit(1)` (Tier 2). Else use description text
     with `snippet_kind="description"` flag (Tier 3).
- Preserve current `score`/`uri`/`document` output keys (wrappers depend
  on them). Add `snippet_kind` key only on Tier 3 rows.
- Plumb the `table` object into `_fmt` (it lives in each caller's scope
  already — pass it through).

### `external-tools/hybrid_search/config.py`
- No change required unless we expose `_OVERFETCH_MULTIPLIER`. Keep it
  inline in `api.py` for now.

### No changes to
- `strands_evaluation/tools/external/search_a_tools.py` /
  `search_b_tools.py` — they already accept a `db_path` override via
  `set_db_path`. Pointing them at `lance_data_v2/` is a runtime config
  concern, not a code concern.
- `strands_evaluation/tools/external/ideal/search_wrapper.py` — the
  existing `_extract_search_text` reads `document`/`text`/`content`;
  works unchanged. `snippet_kind` is filtered out because the wrapper
  only copies known fields.

## Implementation phases

### Phase 1 — Index build
1. Modify `process.py` per above (schema + two insertion points +
   `flush_chunks`).
2. Run `process.py --output-path lance_data_v2` (or equivalent) using
   the **same** parquet cache / manifest / descriptions / schemas the
   current `lance_data/` was built from, so URI sets align.
3. Verify row counts: new `lakeqa` should match current `lance_data/`
   (~65,570 rows) and show ~10k `chunk_kind='description'` +
   ~55k `chunk_kind='content'`.

### Phase 2 — Query path rewrite
1. Update all `.select()` lists in `api.py` to include `chunk_kind`.
2. Implement new `_fmt` with grouping + three-tier fallback.
3. Add targeted lookup helper (single `.where().limit(1)` per missing
   URI).
4. Unit test locally: point `set_db_path("lance_data_v2")`, run a small
   set of NL + value queries, inspect `document` texts and verify
   they look like row data (values, columns) rather than description
   prose.

### Phase 3 — End-to-end validation
1. Re-run `test/test_search_matrix.py --search-tool standard --db
   lance_data_v2` — confirm `content` field in `search_results=standard`
   is row-shaped, not description-shaped.
2. Re-run `test/test_search_matrix.py --search-tool standard --db
   lance_data` — confirm old behavior is unchanged (regression control).
3. Compare a handful of results side-by-side (old DB vs new DB) for the
   same queries.

### Phase 4 — Switchover (out of scope for this plan)
Not deciding yet whether to make `lance_data_v2` the default. Ship the
code + new DB, run evals against both, then decide.

## Verification

- **Schema check**:
  ```
  python3 -c "import lancedb; t = lancedb.connect('lance_data_v2').open_table('lakeqa'); print(t.schema.names); print(t.count_rows())"
  ```
  Expect `chunk_kind` in schema and ~65k rows.
- **Kind distribution**:
  ```
  python3 -c "import lancedb; t=lancedb.connect('lance_data_v2').open_table('lakeqa'); print(t.to_pandas()['chunk_kind'].value_counts())"
  ```
  Expect description ≈ 10k, content ≈ 55k.
- **Snippet sanity** (via `test_search_matrix.py`): run
  `--search-tool standard --db lance_data_v2`, grep the output log,
  confirm that `content`/`dataset_snippet` values contain row-like
  tokens (column headers, values) rather than description prose.
- **Regression** (via `test_search_matrix.py`): run
  `--search-tool standard --db lance_data` (old DB) — payload shape
  should be identical to before.
- **Eval pass**: run one of the mode-variant eval tasks against the new
  DB, confirm no runtime errors and results look sensible.

## Risks & open questions

- **Targeted lookup correctness with FTS filter**: LanceDB's `.where()`
  on a non-indexed column + `fts_columns` may not work as expected.
  Confirm by test during Phase 2 — if filter returns empty due to
  indexing, fall back to a `to_pandas()` post-filter (acceptable at
  small miss counts).
- **Re-index time**: 65k-row rebuild with embedding model on GPU takes
  non-trivial time. Schedule accordingly.
- **URI-alignment with `lance_table_descriptions`**: not used in this
  design, so no concern. Leave that DB alone.
- **GPU OOM during rebuild**: recent eval logs showed CUDA OOM on the
  reranker path (shared GPU). Ensure the rebuild happens when no other
  model is using the GPU, or set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
  as process.py already does.

## Implementation status (as of 2026-04-15)

Submodule work landed upstream in commit
[`36e0026`](https://github.com/Austin-Senna/tools-for-lakeagent/commit/36e0026):
"Tag chunks by kind and return content-only snippets". Changes match this
design:

- `process.py` — `make_table_schema(with_chunk_kind=True)` for `lakeqa`;
  `state["chunk_kinds"]` tracked; `flush_chunks` emits the field;
  description chunks tagged `"description"`, content chunks tagged
  `"content"`.
- `api.py` — `_fmt_grouped` implements all three tiers; T2 helper
  `_fetch_content_chunk` includes `to_pandas` fallback for the
  `.where()` indexing risk called out above; tier counters
  (`_tier_counters`, `get_tier_counters`, `reset_tier_counters`) added
  for eval observability (beyond the plan).
- `config.py` — `document_word_cutoff = 100` (word-based, not character).
- `lakeqa_schema` remains single-kind; `search_value`-style functions
  use `_fmt_grouped`, schema functions keep simple `_fmt`.

**Remaining parent-repo work:**
1. Bump submodule SHA in parent repo (`external-tools` → `36e0026`).
2. Rebuild `lance_data_v2/` using the new `process.py` (~5h).
3. Run Phase 3 validation once the rebuild completes.
