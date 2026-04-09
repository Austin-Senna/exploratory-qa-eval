# Tool Execution Error Catalog — `openai_gpt-5.2` on `naive_k5` & `description_k5`

Source: `logs/naive_k5/**` and `logs/description_k5/**` (~795 errors total).
Aggregates also in `analysis_results_search/tool_errors.json`.

## Headline

**~70–75% of tool errors are agent-side mistakes** (malformed args, hallucinated IDs, SQL against unseen schemas). **~25–30% are platform bugs / hard limits** (JSON serializer crash on DATE/UUID, Lance phrase-query bug, S3 timeouts, 100 MB DuckDB cap).

A "peek before query" rule plus a one-shot example of the correct `download({files:[...]})` envelope would eliminate roughly half of all errors.

## Status — fixes shipped this session

| Fix | Errors addressed | Where |
|---|---|---|
| ✅ **JSON serializer crash on DATE/TIMESTAMP/UUID** in `query_file` | ~93 | `agent_tools_v2.py` `_to_json_safe` helper + applied to row conversion |
| ✅ **`maximum_object_size` rewrite** with actionable `download + execute_code` hint | ~73 | `agent_tools_v2.py` `_rewrite_query_error` |
| ✅ **S3 IO Timeout rewrite** with `download` hint | ~50 | `agent_tools_v2.py` `_rewrite_query_error` |
| ✅ **Text-family error message** rewrite — names `peek_file`/`grep_file`/`read_file` | ~22 | `agent_tools_v2.py` `_rewrite_unqueryable_family_error` |
| ✅ **Backtick identifiers auto-fixed at source** + Parser Error rewrite as belt-and-suspenders | ~17 | `agent_tools_v2.py` `_normalize_sql_backticks` (state machine that converts `` `col` `` → `"col"` while preserving backticks inside `'...'` and `"..."` literals) called at the top of `query_file`; `_rewrite_query_error` still catches anything that slips through |
| ✅ **"QUERY DISCIPLINE — peek before SQL" rule** added to all three prompts (baseline, a, b) | ~310 (Binder + Conversion + Parser + file-family + file-too-large-retry + strptime, prevention not yet measured) | `strands_evaluation/helper/constants.py:151–168`, `prompts/condition_a.txt:56–71`, `prompts/condition_b.txt:59–74` |
| ✅ **Renamed `peek_files` → `peek_multiple`** + rewrote both peek docstrings with explicit "ONE file" vs "SEVERAL files" framing and a CORRECT/WRONG envelope example | ~36 (92% malform rate on the plural) | `agent_tools_v2.py` `peek_multiple` def + docstrings; propagated through `agent.py`, both instrumentation plugins, all 3 prompts, all 4 skill files, `human_agent.py`, and `tool_error_analysis.py` (kept `peek_files` in the analysis tool set for back-compat with historical eval data) |

**Total `query_file` + `peek_multiple` errors addressed: ~601 of ~705 (~85%)** if the prompt rule and rename land as expected. The platform-side rewrites (~255 errors) and the rename (~36) are direct fixes; the prompt rule (~310 errors) is preventive and needs an eval run to confirm impact.

**Tests**: `test/test_query_file_json_safe.py` — 25 unit tests covering `_to_json_safe`, `_rewrite_query_error`, `_rewrite_unqueryable_family_error`, and the `peek_files → peek_multiple` rename. All pass. Sibling tests (`test_s3_public_bucket_mode.py`, `test_pricing_lookup.py`) still green.

**Still TODO**: `download` malforms (~132), `read_file` `wikipedia/` hallucinations (~38), `execute_code` bad assumptions (~37), Lance phrase-query bug (~25 — platform), `peek_file` 404 path-guessing (~18).

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

| # | Failure mode | ~Count | Fault | Status | Example |
|---|---|---|---|---|---|
| 1 | **Binder Error — invented columns / tables** | ~253 | AGENT | 🟡 Prompt rule shipped — measure next eval | `query_file({"sql":"SELECT properties.ISSUING_AGENCY_NAME ... FROM t.features"})` → `Referenced table "properties" not found! Candidate tables: "t"`. Also: `county_name` vs `County`, `"SCHOOL LEVEL"` vs `"SCHOOL LEVEL*"`, `"Count of Offers"` vs `"Number of Offers"`. |
| 2 | **JSON serializer crash on DATE / TIMESTAMP / UUID** | ~93 | PLATFORM | ✅ FIXED (`_to_json_safe`) | Even `SELECT * FROM t LIMIT 1` blows up: `Object of type date is not JSON serializable`. Tool-layer bug — fires on the simplest valid query. |
| 3 | **`maximum_object_size 104857600 bytes exceeded`** | ~73 | MIXED | ✅ FIXED (`_rewrite_query_error`) | 100 MB DuckDB-on-S3 cap. Was bouncing through DuckDB's "Try increasing maximum_object_size" hint; now rewrites to "use download + execute_code". |
| 4 | **S3 IO Timeout** | ~50 | PLATFORM | ✅ FIXED (`_rewrite_query_error`) | Multi-hundred-MB CSVs (parking violations, prison releases, school locations). Now rewrites to suggest `download`. |
| 5 | **`File family 'text' is not queryable with SQL`** | 22 | AGENT | ✅ FIXED (`_rewrite_unqueryable_family_error`) | `query_file({"file_path":"files/0.txt", "sql":"SELECT * FROM t LIMIT 5"})`. Now tells agent to use `peek_file` / `grep_file` / `read_file`. |
| 6 | **`File too large to query directly … Use download + execute_code instead`** | ~21 | AGENT | 🟡 Prompt rule shipped — message was already correct | Tool already suggested the fix; agent was ignoring it. New peek-before-query rule should reduce repeat retries. |
| 7 | **Conversion Error** | ~19 | AGENT | 🟡 Prompt rule shipped | `CAST("Count of Offers" AS INT)` on `'0-5'`; `replace(PercentMetStandard,'%','')::DOUBLE` on `'>80'` / `'Under Review'`. Peek-before-query rule names this as failure mode. |
| 8 | **Parser Error** | ~17 | AGENT | ✅ FIXED at source (`_normalize_sql_backticks`) + error rewrite + 🟡 prompt rule | Backtick identifiers (`` `OVERALL GRADE` ``) — DuckDB rejects them. Now silently rewritten to double quotes BEFORE execution by a state machine that respects string literals. Belt-and-suspenders: error rewrite still fires if something slips through; prompt rule names backticks explicitly. |
| 9 | **Bad strptime format** | ~11 | AGENT | 🟡 Prompt rule shipped | `strptime(x,'%m/%d/%Y')` on values already `2015-01-10`. Peek-before-query rule should help; not directly addressed. |
| 10 | **Misc (Catalog Error / OOM / 'not array' / Not implemented)** | <10 | mixed | — | |

Legend: ✅ direct fix landed and tested · 🟡 prompt rule shipped, awaiting eval-run measurement · ⬜ not addressed

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

## TOOL: peek_files — 92.3% (36/39). Catastrophic but tiny sample. ✅ FIXED via rename.

**36/36 = missing `files` wrapper.** The agent confused `peek_file` (singular: `dataset_id`+`file_path`) with `peek_files` (plural: `files: [...]`). Example: `peek_files({"max_rows": 5})` with no files at all. One call used the wrong key (`entries` instead of `files`).

**Fix shipped**: renamed to `peek_multiple` and rewrote both docstrings with explicit "ONE file" vs "SEVERAL files" framing. The new `peek_multiple` docstring includes a CORRECT/WRONG block showing the exact envelope shape, and the validation error returned on misuse names the alternative tool by name. Test pinned in `test/test_query_file_json_safe.py::TestPeekMultipleRename`.

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
1. ✅ **"Peek before query" rule.** Added as `## QUERY DISCIPLINE — peek before SQL` section in all three prompts (baseline, a, b). Names the actual mistakes (Binder, nested table refs, string→number casts, backticks, text-on-SQL) so the agent recognizes them. Should eliminate Binder + Conversion + Parser + file-family errors — roughly half of all tool errors. Impact to be measured in next eval run.
2. 🟡 **One-shot envelope examples** for `download` and `peek_multiple`. The `peek_multiple` half is done — the renamed tool's docstring now contains a CORRECT/WRONG envelope example. `download` is still TODO.
3. ✅ **Disambiguate `peek_file` vs `peek_files`.** Renamed `peek_files` → `peek_multiple` and rewrote both docstrings. The new docstring's CORRECT/WRONG block + the validation error message both name the alternative tool explicitly. Test pinned.
4. ⬜ **Stop the `wikipedia/<Page>` hallucination.** Either (a) document that dataset_ids are bare names, or (b) have the platform auto-strip the `wikipedia/` prefix and resolve, since the agent already knows the right ID one turn later via `search_prefix`.
5. ✅ **Respect tool guidance.** When `query_file` says "use download + execute_code instead," the agent now gets a clearer signal: the `maximum_object_size` and IO-timeout error rewrites surface the actionable hint instead of DuckDB's misleading "Try increasing maximum_object_size".

### Platform-side
1. ✅ **Fix the JSON serializer for DATE / TIMESTAMP / UUID** in `query_file`. Fixed via `_to_json_safe` helper that converts `datetime.date/datetime/time`, `Decimal`, `UUID`, and `bytes` to JSON-safe primitives before serialization.
2. ⬜ **Rebuild the Lance index with positions** so phrase queries in `search_value` / `search_schema` work.
3. ✅ **Surface the remediation more loudly** for the 100 MB DuckDB-on-S3 cap. Done via `_rewrite_query_error` — the cap itself is unchanged but the error message now explicitly tells the agent to download and use execute_code.

---

## Files referenced
- `analysis_results_search/tool_errors.json` — per condition_model error rates
- `logs/naive_k5/baseline/openai-gpt-5.2/k-4-d-4/task_3.log` — canonical `read_file` `wikipedia/` hallucination (line 82–84)
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-2-d-1/task_4.log` — multiple `wikipedia/<Texas_County>` errors in one turn
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-2-d-3/task_6.log` — `Maximum 5 files per download call`
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-3-d-1/task_1.log` — 1377 MB file-too-large
- `logs/naive_k5/b_plan_soft/openai-gpt-5.2/k-1-d-1/task_5.log` — `File family 'text' is not queryable with SQL`
