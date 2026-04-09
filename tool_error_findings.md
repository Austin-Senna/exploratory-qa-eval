# Tool Execution Error Catalog — `openai_gpt-5.2` on `naive_k5` & `description_k5`

Source: `logs/naive_k5/**` and `logs/description_k5/**` (~795 errors total).
Aggregates also in `analysis_results_search/tool_errors.json`.

## Headline

**~70–75% of tool errors are agent-side mistakes** (malformed args, hallucinated IDs, SQL against unseen schemas). **~25–30% are platform bugs / hard limits** (JSON serializer crash on DATE/UUID, Lance phrase-query bug, S3 timeouts, 100 MB DuckDB cap).

A "peek before query" rule plus a one-shot example of the correct `download({files:[...]})` envelope would eliminate roughly half of all errors.

## Error rates (from `tool_errors.json`)

| Tool | naive_k5/baseline | naive_k5/b_plan_soft | description_k5/baseline | description_k5/b_plan_soft |
|---|---|---|---|---|
| download | 42.6% (29/68) | 44.0% (55/125) | 42.7% (32/75) | 45.8% (49/107) |
| query_file | 26.2% (224/855) | 25.8% (191/741) | 25.1% (202/806) | 25.2% (172/683) |
| execute_code | 22.1% (17/77) | 21.8% (29/133) | 13.3% (15/113) | 15.0% (18/120) |
| read_file | 8.7% (8/92) | 14.7% (15/102) | 10.4% (8/77) | 21.2% (18/85) |
| peek_files | — | 91.7% (22/24) | — | 93.3% (14/15) |
| peek_file | 2.7% (15/564) | 4.5% (22/490) | 1.3% (7/536) | 4.8% (27/565) |
| search_prefix | 0.8% (4/476) | 7.2% (27/373) | 0.4% (2/495) | 6.5% (26/400) |
| search_value | 1.8% (12/686) | 5.6% (49/869) | 0.5% (3/639) | 4.5% (35/781) |
| list_files | 1.6% (5/313) | 3.5% (11/315) | 1.3% (4/317) | 0.7% (2/306) |
| grep_file | 3.1% (2/64) | 0% (0/43) | 2.6% (2/76) | 0% (0/40) |
| search_schema | 0% | 3.4% (3/89) | 0% | 7.6% (6/79) |
| submit_answer / plan / skills | 0% | 0% | 0% | 0% |

---

## TOOL: query_file — 21.6% error rate (~669/3100). Biggest bucket.

| # | Failure mode | ~Count | Fault | Example |
|---|---|---|---|---|
| 1 | **Binder Error — invented columns / tables** | ~253 | AGENT | `query_file({"sql":"SELECT properties.ISSUING_AGENCY_NAME ... FROM t.features"})` → `Referenced table "properties" not found! Candidate tables: "t"`. Also: `county_name` vs `County`, `"SCHOOL LEVEL"` vs `"SCHOOL LEVEL*"`, `"Count of Offers"` vs `"Number of Offers"`. |
| 2 | **JSON serializer crash on DATE / TIMESTAMP / UUID** | ~93 | PLATFORM | Even `SELECT * FROM t LIMIT 1` blows up: `Object of type date is not JSON serializable`. Tool-layer bug — fires on the simplest valid query. |
| 3 | **`maximum_object_size 104857600 bytes exceeded`** | ~73 | MIXED | 100 MB DuckDB-on-S3 cap. Agent has been told "use download + execute_code" and keeps retrying anyway. |
| 4 | **S3 IO Timeout** | ~50 | PLATFORM | Multi-hundred-MB CSVs (parking violations, prison releases, school locations). |
| 5 | **`File family 'text' is not queryable with SQL`** | 22 | AGENT | `query_file({"file_path":"files/0.txt", "sql":"SELECT * FROM t LIMIT 5"})`. Should `peek_file` first. |
| 6 | **`File too large to query directly … Use download + execute_code instead`** | ~21 | AGENT | Tool literally tells the agent the fix; agent ignores it. |
| 7 | **Conversion Error** | ~19 | AGENT | `CAST("Count of Offers" AS INT)` on `'0-5'`; `replace(PercentMetStandard,'%','')::DOUBLE` on `'>80'` / `'Under Review'`. |
| 8 | **Parser Error** | ~17 | AGENT | Backtick identifiers (`` `OVERALL GRADE` ``) — DuckDB rejects them. Bad `SELECT col alias` lacking AS. |
| 9 | **Bad strptime format** | ~11 | AGENT | `strptime(x,'%m/%d/%Y')` on values already `2015-01-10`. |
| 10 | **Misc (Catalog Error / OOM / 'not array' / Not implemented)** | <10 | mixed | |

## TOOL: download — 41.4% (156/377). ~100% agent-fault.

| # | Failure mode | Count | Fault | Example |
|---|---|---|---|---|
| 1 | **Missing `files` wrapper** | ~132 | AGENT | Calls `download({"dataset_id": X, "file_path": Y})` instead of `download({"files":[{...}]})`. Schema requires a list under `files`. |
| 2 | **`Maximum 5 files per download call`** | 19 | AGENT | Six `moving-violations-issued-in-january-201{7..22}` in one call. Limit is documented. |

## TOOL: execute_code — 14.2% (~63/444). Nearly all agent-fault.

| Failure mode | Count | Example |
|---|---|---|
| **`ModuleNotFoundError: 'ijson'`** | 8 | Wrong assumption about sandbox env. |
| **`KeyError: 'SANDBOX_DIR'`** | 7 | `os.environ['SANDBOX_DIR']` instead of using the injected local. One run hardcoded an absolute sandbox path → `FileNotFoundError`. |
| **NoneType concat / KeyError `'features'` / `max() empty`** | ~15 | Treats non-GeoJSON as GeoJSON; assumes `distribution.downloadURL` exists. |
| **Stale pandas args** | few | `to_datetime(infer_datetime_format=...)` (removed). |
| **XML parser on JSON file** | few | `ParseError: not well-formed`. |

## TOOL: read_file — 10.9% (39/357). 100% one mistake.

**All 38 errors: `Dataset not found or ambiguous: wikipedia/<X>`.** The agent treats every Wikipedia mention as a readable dataset under the bogus prefix `wikipedia/<pagename>`. The actual dataset_id is the bare name (`Logan_Fontenelle`).

Canonical example — `logs/naive_k5/baseline/openai-gpt-5.2/k-4-d-4/task_3.log:82–84`:
```
Executing: read_file({"dataset_id": "wikipedia/Logan_Fontenelle", "file_path": "content.txt", ...})
Tool logical error: {"error": "Dataset not found or ambiguous: wikipedia/Logan_Fontenelle"}
```
The same hallucinated `wikipedia/` prefix bleeds into `peek_file` (2 errors) and `grep_file` (1 error).

## TOOL: peek_files — 92.3% (36/39). Catastrophic but tiny sample.

**36/36 = missing `files` wrapper.** The agent confuses `peek_file` (singular: `dataset_id`+`file_path`) with `peek_files` (plural: `files: [...]`). Example: `peek_files({"max_rows": 5})` with no files at all. One call used the wrong key (`entries` instead of `files`).

## TOOL: peek_file — 1.0% (~21/2160)

- **`HeadObject failed: 404 Not Found`** ~18 — AGENT. Guesses `files/rows.csv` when the real path is `files/data.txt`. Doesn't `list_files` first.
- **`wikipedia/...` hallucination** — 2.

## TOOL: search_value / search_schema — <1% but a real platform bug

**All 24 errors:** `lance error: position is not found but required for phrase queries`. Triggered whenever the agent quotes a phrase, e.g.:
```
search_value({"query":"\"top 20\" contractor \"Washington State\" \"2017\" \"2018\""})
```
The Lance index was built without positions → phrase queries unsupported. **PLATFORM** config issue.

## TOOL: list_files — 0.6% (7/1254)

**3 validation errors**: `dataset_id` (singular) instead of `dataset_ids` (list). AGENT.

## TOOL: grep_file — <0.5%

1 error, same `wikipedia/Houston_Rockets` hallucination.

## TOOL: search_prefix — 0% out of 1745 calls

No errors. The one tool the agent cannot misuse.

---

## Fault summary

| Bucket | Share | Contents |
|---|---|---|
| **Agent-side** | **~70–75%** | All download malforms, all peek_files malforms, all `wikipedia/` hallucinations, ~60% of query_file (Binder/Parser/Conversion/file-too-large-retry/wrong file family), ~55/63 execute_code (bad imports, wrong env, wrong file shape) |
| **Platform-side** | **~25–30%** | `date/UUID not JSON serializable` (~93 — fires on `SELECT *`), S3 timeouts (~50), 100 MB DuckDB cap (partial), Lance phrase-query bug (25) |

---

## Recommended fixes

### Agent-side (prompt / scaffolding)
1. **"Peek before query" rule.** Force a `peek_file` (or `search_schema`) on every new dataset before the first `query_file`. Eliminates Binder + Conversion + Parser + file-family errors — roughly half of all tool errors.
2. **One-shot envelope examples** for `download` and `peek_files`. The agent consistently flattens these into the wrong shape — show it the right one in the system prompt.
3. **Disambiguate `peek_file` vs `peek_files`.** 92% failure on the plural confirms the agent doesn't internalize the distinction. Either rename one or unify the signature.
4. **Stop the `wikipedia/<Page>` hallucination.** Either (a) document that dataset_ids are bare names, or (b) have the platform auto-strip the `wikipedia/` prefix and resolve, since the agent already knows the right ID one turn later via `search_prefix`.
5. **Respect tool guidance.** When `query_file` says "use download + execute_code instead," the agent should switch tactics — currently it retries the same call.

### Platform-side
1. **Fix the JSON serializer for DATE / TIMESTAMP / UUID** in `query_file`. ~14% of all `query_file` errors fire on the simplest valid query and have nothing to do with the agent.
2. **Rebuild the Lance index with positions** so phrase queries in `search_value` / `search_schema` work.
3. **Either raise the 100 MB DuckDB-on-S3 cap or surface the remediation more loudly** so the agent doesn't burn turns retrying.

---

## Files referenced
- `analysis_results_search/tool_errors.json` — per condition_model error rates
- `logs/naive_k5/baseline/openai-gpt-5.2/k-4-d-4/task_3.log` — canonical `read_file` `wikipedia/` hallucination (line 82–84)
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-2-d-1/task_4.log` — multiple `wikipedia/<Texas_County>` errors in one turn
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-2-d-3/task_6.log` — `Maximum 5 files per download call`
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-3-d-1/task_1.log` — 1377 MB file-too-large
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-1-d-1/task_5.log` — `File family 'text' is not queryable with SQL`
