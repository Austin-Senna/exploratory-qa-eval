# Dataset Profile Stats for SANA Agent 1

**Date:** 2026-04-23
**Context:** Second pass on SANA Agent 1. The first pass (`feat/sana-agent-0-1`) wired an enriched-`peek_file` plumbing that attaches `schema_columns`, `table_kind`, `llm_description`, and `snippet` to each peek result when `sana_level >= 1`. Those fields reuse caches already on disk. They are not enough: paper.md §4.5 says the richer APIs should replace schema thrash — `read_file`, `grep_file`, and trivial SQL probing — which requires per-column statistics the existing caches do not carry.

This design adds a new `datagov_tables_profiles.jsonl` artifact produced by an offline precompute script and consumed at peek time.

---

## 1. Motivation

Schema + description + snippet tell the agent *what a dataset is*. They do not tell it *what's actually in it*. Agents still query to learn:

- how many rows there are
- whether a column is mostly null
- whether a column is a one-value constant
- the min/max of a numeric or date column
- what the first 2 rows look like once parsed

Every one of these probe patterns shows up in the current turn-waste traces as "schema thrash." The fix is to cache the answers once and return them with the peek.

## 2. Scope

**In scope:**
- New precompute script `scripts/profile_datasets.py` that walks every tabular entry in `datagov_tables_schemas_full.jsonl`, runs a single DuckDB query per dataset against S3, and writes `datagov_tables_profiles.jsonl`.
- New runtime path in `agent_tools_v2._load_dataset_profile` that loads `datagov_tables_profiles.jsonl` lazily and merges it into the Agent 1 peek response.
- Preflight check for `datagov_tables_profiles.jsonl` when `sana_level >= 1` — warn-only, not fatal, so the branch runs before the script has produced the file.
- Tests covering the loader, schema shape, and fall-through when the jsonl is missing or a URI is absent.

**Out of scope:**
- Changes to the `sana_level` axis, the axis-defaulting logic, or `inject_sana_prompt` — those shipped in the first pass and stay.
- Agent 2/3/4 interventions (plan budgeting, micro-reflection, macro-reflection).
- Lazy-compute fallback for URIs not in the precomputed jsonl. If an entry is missing, the profile falls back to the existing schema+snippet+description bundle; no compute happens at agent runtime.
- Statistics for JSON / XML / text datasets. Those families keep the existing `snippet` field; no columns/rows stats are attempted.

## 3. Profile schema

One JSONL row per `(slug, filename_stem)` entry — the same key used by the existing schemas jsonl.

**Tabular entry (`family == "csv"` or `"json"` and parseable as rows):**

```json
{
  "slug": "index-crimes-by-county",
  "filename": "rows",
  "family": "csv",
  "size_bytes": 987654,
  "row_count": 12345,
  "llm_description": "Annual violent and property crime totals by NY county, reported by...",
  "top_2_rows": [
    {"County": "Erie",   "STFIP": "36", "Year": 2020, "Violent_Crime": 832},
    {"County": "Monroe", "STFIP": "36", "Year": 2020, "Violent_Crime": 614}
  ],
  "columns": [
    {"name": "County",        "type": "string",  "null_rate": 0.00, "distinct_count": 62,   "min": null, "max": null,  "mean": null},
    {"name": "STFIP",         "type": "string",  "null_rate": 0.00, "distinct_count": 1,    "min": null, "max": null,  "mean": null},
    {"name": "Year",          "type": "integer", "null_rate": 0.00, "distinct_count": 15,   "min": 2010, "max": 2024,  "mean": 2017.0},
    {"name": "Violent_Crime", "type": "integer", "null_rate": 0.02, "distinct_count": 4821, "min": 0,    "max": 48293, "mean": 712.4}
  ]
}
```

**Non-tabular entry (xml / text / wikipedia):**

```json
{
  "slug": "...",
  "filename": "...",
  "family": "text",
  "size_bytes": 12345,
  "llm_description": "...",
  "snippet": "..."
}
```

`llm_description` is copied verbatim from `table_descriptions.jsonl` during precompute — same URI keying. Omitted if the source cache has no entry for the URI.

**Rules:**
- `columns[*].min/max/mean` are populated only when `type` is numeric or date; `null` otherwise.
- `columns[*].null_rate` is a float in [0, 1] with 2-decimal precision.
- `columns[*].distinct_count` is exact (full scan).
- `top_2_rows` is a list of dicts keyed by column name; string values are truncated to 80 chars, then the truncation is marked by trailing `…` if clipped.
- No `top_k`, `stddev`, `inferred_semantic`, `date_columns`, `year_range`, or `geographic_grain` fields. Everything those encoded is derivable by the agent from `columns` alone.
- Snippet is present only on non-tabular entries. Tabular entries rely on `top_2_rows` for the "show me actual values" signal.

## 4. Architecture

### 4.1 Precompute script (`scripts/profile_datasets.py`)

Driver:

1. Parse `--input datagov_tables_schemas_full.jsonl` (default) and `--output datagov_tables_profiles.jsonl`.
2. Support `--resume` (skip entries already in the output jsonl, keyed by `(slug, filename)`) and `--parallel N` (DuckDB can scan S3 concurrently; default 4).
3. For each `(slug, table)` in the schemas jsonl:
   - Resolve S3 URI via the same `_slug_stem_from_uri` inverse used by `search_wrapper`.
   - `HEAD` the object for `size_bytes`.
   - Detect family: trust the schema's `table_kind` first, fall back to reading first 8 KB and calling the existing `detect_family` helper on mismatch.
   - Fetch `llm_description` from the existing `table_descriptions.jsonl` cache (keyed by full S3 URI) and pass it through verbatim. Omit the field if no entry.
   - **Tabular path:**
     - Issue one DuckDB query against `s3://<uri>` via httpfs. The query uses dynamic SQL generated from the schema's column list:
       ```sql
       SELECT
         COUNT(*) AS row_count,
         COUNT(*) FILTER (WHERE "col1" IS NULL) AS null_count_col1,
         COUNT(DISTINCT "col1")                  AS distinct_count_col1,
         MIN("col1")                             AS min_col1,
         MAX("col1")                             AS max_col1,
         AVG("col1")                             AS mean_col1,
         ...
       FROM read_csv_auto('s3://...', SAMPLE_SIZE=-1);
       ```
       DuckDB returns `NULL` for `MIN/MAX/AVG` on non-numeric, non-temporal columns — that's the type signal we use to decide whether `min/max/mean` are emitted vs left `null`.
     - Issue a second `LIMIT 2` query to fetch `top_2_rows`; truncate string columns inline via `substr(col, 1, 80)`.
     - Both queries fit in a single `duckdb.connect()` session; run them back-to-back.
   - **Non-tabular path:**
     - Look up the URI in `snippet.jsonl`; emit `{slug, filename, family, size_bytes, snippet}`.
     - If the snippet is absent, read first 2 KB via range-GET and use that as the snippet.
4. Write one jsonl line per entry. Flush after each write (survives interruption; pairs with `--resume`).
5. Catch and log per-entry errors; skip the entry rather than aborting the run.

Runtime expectation: a few hours across the full lake. `--parallel 8` with 4-vCPU workers is a reasonable starting point. Not a one-shot — rerun when the lake grows.

### 4.2 Runtime lookup (`strands_evaluation/tools/agent_tools_v2.py`)

Add a second lazy-loaded cache alongside the existing `_load_dataset_profile` logic:

```python
_PROFILES_PATH = Path("datagov_tables_profiles.jsonl")
_PROFILE_BY_SLUG_FILENAME: Dict[Tuple[str, str], Dict[str, Any]] = {}
_PROFILES_LOADED: bool = False

def _load_profiles_cache() -> None:
    global _PROFILES_LOADED
    if _PROFILES_LOADED:
        return
    if not _PROFILES_PATH.exists():
        _PROFILES_LOADED = True  # soft-load: absence is allowed
        return
    for line in _PROFILES_PATH.open():
        ...
    _PROFILES_LOADED = True
```

Change `_load_dataset_profile(s3_uri)` to:

1. Derive `(slug, filename_stem)` from the URI (reuse `search_wrapper._slug_stem_from_uri`).
2. `_load_profiles_cache()`; if a profile entry exists for the key, return it directly.
3. Otherwise fall back to the existing behavior (schema + llm_description + snippet from the three legacy caches).

**Precompute-is-authoritative:** the profile entry, when present, is returned *as-is*. The precompute script is the single place that decides whether `snippet` or `top_2_rows` appears — the runtime does not try to merge or reconcile.

### 4.3 Preflight (`strands_evaluation/preflight.py`)

When `sana_level >= 1`:

- The existing three-jsonl check stays (`_check_desc_cache_for_enrichment` etc.).
- Add a new `_check_profiles_jsonl` that reports `ok=True, detail="found: N entries"` when present, `ok=True, detail="missing: <path> (Agent 1 falls back to legacy schema+snippet+description)"` when absent. **Warn-only, not fatal** — the branch must be runnable before the precompute script has produced the file.

### 4.4 No prompt-surface change

`inject_sana_prompt` already documents `schema_columns`, `table_kind`, `llm_description`, `snippet`. Extend it by one sentence listing `row_count`, `size_bytes`, `top_2_rows`, and per-column `null_rate / distinct_count / min / max / mean`. Keep the total section under 12 lines.

## 5. Data flow

```
datagov_tables_schemas_full.jsonl
        │
        ▼ scripts/profile_datasets.py (offline, DuckDB on S3)
datagov_tables_profiles.jsonl
        │
        ▼ _load_profiles_cache (lazy, at first peek)
in-memory _PROFILE_BY_SLUG_FILENAME
        │
        ▼ peek_file(..., dataset_id, file_path) — sana_level >= 1
result["profile"] populated from profiles.jsonl when available,
        else from legacy schema+snippet+description caches
```

## 6. Testing

- **Unit (profile lookup):** a known cached URI returns the full profile; an uncached URI falls back to the legacy bundle; a URI with no entry anywhere returns `None`.
- **Unit (schema shape):** a fixture profiles.jsonl file is loaded and asserts on field presence (tabular vs non-tabular entries carry the expected keys).
- **Unit (precompute script):** small fixture S3 bucket (or local `read_csv` over a sample CSV) produces a profile matching hand-computed expected values for `row_count`, `null_rate`, `distinct_count`, `min/max/mean`.
- **Unit (prompt injection):** after the one-sentence extension, the DATASET PROFILE section still matches prompt-contract expectations (`DATASET PROFILE` heading present; total length bounded).
- **Integration:** smoke run with `--sana 1` on a single task, local `datagov_tables_profiles.jsonl` fixture — verify at least one peek_file result carries `row_count` and `top_2_rows`.
- **Preflight:** `sana_level=1` with `datagov_tables_profiles.jsonl` renamed away — preflight emits the warn-only check; run proceeds.

## 7. Validation and execution

Post-landing:

1. Run the precompute script against a 10-dataset sample to validate schema + runtime. Hand-check a couple of profiles for accuracy.
2. Run against the full lake with `--parallel 8 --resume`. Expected wall-clock: a few hours.
3. Commit `datagov_tables_profiles.jsonl` to git (the three existing jsonls are tracked; match precedent for reproducibility).
4. Smoke run of `--sana 1` on 5 tasks; confirm peek_file responses include the new fields and agent behavior shifts (spot-check that follow-up grep_file / read_file calls drop out when the profile is present).

## 8. Open risks

- **DuckDB type inference drift.** `read_csv_auto` sometimes infers columns as VARCHAR when a handful of rows contain sentinels like `>80` or `0-5`. The resulting profile reports `type="string"` and empty `min/max/mean`. This is correct but less informative than it could be; downstream the agent's peek-before-query discipline already accounts for it.
- **Large-file timeouts.** The full-scan query on multi-GB CSVs can be slow. `--parallel 8` + per-dataset timeouts (e.g. 10 min hard cap) should cover this; datasets that time out get skipped and can be revisited with `--resume` + a longer cap.
- **`top_2_rows` with huge per-cell text.** The 80-char-per-cell cap handles this for CSV. For JSONL with nested objects, stringify then truncate — `{"nested":{"a":1,"b":{...}}}` becomes `{"nested":{"a":1,"b":{...}}}` truncated at 80 chars. Agent still sees the structure hint.
- **Snippet redundancy on non-tabular.** `snippet.jsonl` is already loaded; the profiles jsonl re-emits snippets for non-tabular entries. Slight disk duplication but simplifies the runtime lookup path (single authoritative source per URI).

## 9. Decisions locked in

- Storage: new `datagov_tables_profiles.jsonl` (not extending `datagov_tables_schemas_full.jsonl`)
- Compute: offline precompute script; no lazy-compute fallback in the runtime
- Scan strategy: full scan, always; `--resume` for interruption tolerance
- Per-column stats: `type`, `null_rate`, `distinct_count`, `min`, `max`, `mean` — no `stddev`, no `top_k`, no `inferred_semantic`
- Dataset-level stats: `row_count`, `size_bytes`, `family`, `llm_description`, `top_2_rows` for tabular; `llm_description` + `snippet` for non-tabular — no `date_columns`, `year_range`, `geographic_grain`
- Cell size cap: 80 chars per string value in `top_2_rows`
- Non-tabular families: profile carries only `family + size_bytes + snippet`
- Missing profile: runtime falls back to existing schema+description+snippet bundle (same as today's Agent 1)
- Preflight: warn-only on missing profiles file, not fatal