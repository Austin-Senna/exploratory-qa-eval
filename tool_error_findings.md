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
| ✅ **`download` docstring + validation messages rewritten** with CORRECT/WRONG envelope and a loud 5-file cap | ~151 (132 missing-files-wrapper + 19 too-many-files) | `agent_tools.py` `download`: docstring now leads with REQUIRED ARGUMENT SHAPE / CORRECT / WRONG block listing the actual malformations from logs; the three validation errors (non-list, empty, >5) each echo the right envelope shape inline and the >5 case tells the agent to split into multiple calls |
| ✅ **Backtick auto-fix at the source** in `query_file` SQL — converts `` `col` `` → `"col"` while preserving backticks inside string literals | ~17 | `agent_tools_v2.py` `_normalize_sql_backticks` (state machine that respects `'...'` and `"..."`); called at the top of `query_file` |
| ✅ **`wikipedia/` / `datagov/` dataset_id prefix auto-strip** in `peek_file`, `read_file`, `grep_file` | ~41 | `agent_tools_v2.py` `_strip_folder_prefix` (case-insensitive, handles leading slash); called at the top of each tool right after the empty-arg check. `peek_multiple` gets the fix for free via delegation to `peek_file`. |
| ✅ **`SANDBOX_DIR` in `os.environ`** during `execute_code` exec | ~14 | `agent_tools.py` `execute_code`: save `os.environ.get('SANDBOX_DIR')` before exec, set `os.environ['SANDBOX_DIR'] = str(sandbox)`, restore in `finally`. Both `os.environ['SANDBOX_DIR']` (the agent's preferred form) and the local `SANDBOX_DIR` now work. |
| ✅ **`ijson` pre-installed and pre-imported** in the sandbox | ~8 | `requirements.txt` adds `ijson>=3.2`; `agent_tools.py` `execute_code` adds `import ijson` to `pre_imports` block; docstring updated to list it and show the streaming pattern. The agent reaches for ijson to stream-parse 100+ MB GeoJSON FeatureCollections. |
| ✅ **`execute_code` error rewrite helper** — appends `hint` field to known traceback patterns | ~20 | `agent_tools.py` `_rewrite_execute_code_error`: pattern-matches `KeyError 'features'`, `JSONDecodeError line 1 column 1`, `NoneType + str`, `infer_datetime_format`, empty `max()/min()/argmax`, `Usecols do not match`, `ModuleNotFoundError`, `ParseError not well-formed`. Wired into the `except BaseException` branch so the `hint` is additive (original `error`/`traceback` unchanged). |
| ✅ **Skill bundle consolidation** — `skill_imperative` promoted to default, soft bundle deleted | prevention | Deleted `strands_evaluation/tools/skills/` (soft) and renamed `strands_evaluation/tools/skill_imperative/` → `strands_evaluation/tools/skills/`. Removed the `plan_mode` field from `ConditionConfig`, the conditional branching in `agent.py` (`:474–497`), and the `--plan {imperative,soft}` CLI flag from both `run_eval.py` and `run_search_eval.py`. `_base_condition_label` simplified to return the bare base condition; condition B labels collapse from `b_plan_soft`/`b_plan_imperative` to plain `b`. The imperative bundle's description-field load triggers (e.g. "ALWAYS load this skill first before calling plan() or any search tool") are now the default — they're the single biggest cue that makes the strands skill dispatcher actually fire on the right turns. Historical `logs/*/b_plan_soft/` and `results/*/b_plan_soft/` paths remain frozen; `analysis/generate_figures.py:96` already collapses them to `b` in figures via `_BASE_RENAMES`. |

**Total errors addressed: ~835 of ~877 (~95%)** if the prompt rule lands as expected. Direct fixes (~525 errors): JSON serializer, error rewrites, text-family, backtick auto-fix, peek_multiple rename, download docstring/validation, `wikipedia/` prefix strip, SANDBOX_DIR env, ijson pre-install, execute_code hints. Prompt-rule prevention (~310 errors): peek-before-query — needs an eval run to confirm impact. (The execute_code recount across both naive_k5 and description_k5 yielded 82 errors vs the 63 in the original tally, hence the updated denominator.)

**Tests**: `test/test_query_file_json_safe.py` — 68 unit tests covering `_to_json_safe`, `_rewrite_query_error`, `_rewrite_unqueryable_family_error`, `_normalize_sql_backticks`, the `peek_files → peek_multiple` rename, the `download` validation/docstring rewrite, the `_strip_folder_prefix` helper (13 tests), the `_rewrite_execute_code_error` helper (10 tests), and integration tests for `execute_code` SANDBOX_DIR env var, ijson pre-import, and hint wiring (6 tests). All pass. Sibling tests (`test_s3_public_bucket_mode.py`, `test_pricing_lookup.py`) still green.

**Still TODO**: Lance phrase-query bug (~25 — platform, fix is in external `process.py` index-build script), `peek_file` 404 path-guessing (~18), the residual ~20 `execute_code` agent-logic errors that don't match a known pattern.

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

## TOOL: download — 41.4% (156/377). ~100% agent-fault. ✅ FIXED via docstring + validation rewrite.

| # | Failure mode | Count | Fault | Status | Example |
|---|---|---|---|---|---|
| 1 | **Missing `files` wrapper** | ~132 | AGENT | ✅ FIXED | Calls `download({"dataset_id": X, "file_path": Y})` instead of `download({"files":[{...}]})`. Docstring now leads with REQUIRED ARGUMENT SHAPE / CORRECT / WRONG block listing this exact malformation; validation error on non-list inputs echoes the correct shape inline. |
| 2 | **`Maximum 5 files per download call`** | 19 | AGENT | ✅ FIXED | Six `moving-violations-issued-in-january-201{7..22}` in one call. Validation error now mentions the actual count, repeats the cap, and tells the agent to split into multiple `download` calls. |

## TOOL: execute_code — 82 errors total. ✅ DIRECT FIXES + HINT REWRITES SHIPPED.

Recount across both `naive_k5` and `description_k5` gives **82 total errors** (the original tally said ~63). Breakdown by exact error class:

| Failure mode | Count | Fault | Status | Example |
|---|---|---|---|---|
| **`KeyError: 'SANDBOX_DIR'`** | 14 | AGENT | ✅ FIXED | `os.environ['SANDBOX_DIR']` instead of the injected local. `execute_code` now sets it in the env before exec and restores in `finally`. Both forms work. |
| **`ModuleNotFoundError: 'ijson'`** | 8 | AGENT | ✅ FIXED | Agent reaches for ijson to stream-parse 100+ MB GeoJSON. Now in `requirements.txt` AND pre-imported in the sandbox. |
| **`JSONDecodeError: line 1 column 1`** | 7 | AGENT | ✅ HINT | `json.load` on a non-JSON file (often `.txt` that's actually CSV). Hint suggests `peek_file` to check the family first. |
| **`KeyError: 'features'`** | 4 | AGENT | ✅ HINT | Assumes any JSON is a GeoJSON FeatureCollection. Hint suggests `peek_file` (json_keys) before `data['features']`. |
| **`TypeError: NoneType + str`** | 6 | AGENT | ✅ HINT | A `.get(key)` returned `None` and was concatenated. Hint suggests confirming the field exists with `peek_file`. |
| **`ValueError: max()/min()/argmax of empty`** | 6 | AGENT | ✅ HINT | Empty filter result. Hint suggests `len(...)` or `if not df.empty` check. |
| **`ValueError: Usecols do not match columns`** | 2 | AGENT | ✅ HINT | Same Binder-class mistake as `query_file`. Hint suggests `peek_file` for real header columns. |
| **`TypeError: infer_datetime_format`** | 1 | AGENT | ✅ HINT | pandas 3.0 removed the arg. Hint says to drop it (auto-detected now). |
| **`ParseError: not well-formed`** | 1 | AGENT | ✅ HINT | XML parser on a JSON file. Hint suggests `peek_file` to check family. |
| **`ModuleNotFoundError`** (other) | ~5 | AGENT | ✅ HINT | Generic catch — hint lists what IS pre-installed (`pandas, json, csv, os, glob, re, pathlib, ijson`) and notes that network is blocked. |
| Other (one-offs: `s3fs`, `NameError`, `FileNotFoundError`, etc.) | ~7 | mixed | ⬜ | Tail of long-tail. |

**Direct fixes (22 errors eliminated outright)**: SANDBOX_DIR env var save/set/restore; ijson pip-install + pre-import; docstring updated to list both. Pinned by 6 integration tests in `test/test_query_file_json_safe.py::TestExecuteCodeSandboxEnvAndIjson` — env var is set during exec, restored after, ijson is importable without an explicit import, and unknown-module errors get a hint listing what's available.

**Hint rewrites (~20 additional errors get actionable next-step guidance)**: `_rewrite_execute_code_error` helper in `agent_tools.py` pattern-matches the traceback and appends a `hint` field on top of the existing `error`/`traceback`. Hints are purely additive — never modify the original error fields. Pinned by 10 unit tests in `test/test_query_file_json_safe.py::TestRewriteExecuteCodeError`, each driven by a real traceback fragment from the eval logs.

## TOOL: read_file — 10.9% (39/357). 100% one mistake. ✅ FIXED via prefix auto-strip.

**All 38 errors: `Dataset not found or ambiguous: wikipedia/<X>`.** The agent treats every Wikipedia mention as a readable dataset under the bogus prefix `wikipedia/<pagename>`. The actual dataset_id is the bare name (`Logan_Fontenelle`).

Canonical example — `logs/naive_k5/baseline/openai-gpt-5.2/k-4-d-4/task_3.log:82–84`:
```
Executing: read_file({"dataset_id": "wikipedia/Logan_Fontenelle", "file_path": "content.txt", ...})
Tool logical error: {"error": "Dataset not found or ambiguous: wikipedia/Logan_Fontenelle"}
```
The same hallucinated `wikipedia/` prefix bled into `peek_file` (2 errors) and `grep_file` (1 error).

**Fix shipped**: `_strip_folder_prefix` helper in `agent_tools_v2.py` silently strips a leading `wikipedia/` or `datagov/` (case-insensitive, also handles a leading `/`) from the `dataset_id` argument of `peek_file`, `read_file`, and `grep_file`. The helper is called immediately after the empty-arg check and before `_resolve_dataset_folder`, so the resolution logic sees the bare id. `peek_multiple` is fixed for free via delegation to `peek_file`. Pinned by 13 unit tests in `test/test_query_file_json_safe.py::TestStripFolderPrefix` covering the wikipedia/datagov cases, case-insensitivity, leading-slash, idempotence, empty/None/non-string defensives, and substring near-misses (`wiki/`, `wikipediathing`).

## TOOL: peek_files — 92.3% (36/39). Catastrophic but tiny sample. ✅ FIXED via rename.

**36/36 = missing `files` wrapper.** The agent confused `peek_file` (singular: `dataset_id`+`file_path`) with `peek_files` (plural: `files: [...]`). Example: `peek_files({"max_rows": 5})` with no files at all. One call used the wrong key (`entries` instead of `files`).

**Fix shipped**: renamed to `peek_multiple` and rewrote both docstrings with explicit "ONE file" vs "SEVERAL files" framing. The new `peek_multiple` docstring includes a CORRECT/WRONG block showing the exact envelope shape, and the validation error returned on misuse names the alternative tool by name. Test pinned in `test/test_query_file_json_safe.py::TestPeekMultipleRename`.

## TOOL: peek_file — 1.0% (~21/2160)

- **`HeadObject failed: 404 Not Found`** ~18 — AGENT. Guesses `files/rows.csv` when the real path is `files/data.txt`. Doesn't `list_files` first.
- **`wikipedia/...` hallucination** — 2. ✅ FIXED via `_strip_folder_prefix`.

## TOOL: search_value / search_schema — <1% but a real platform bug

**All 24 errors:** `lance error: position is not found but required for phrase queries`. Triggered whenever the agent quotes a phrase, e.g.:
```
search_value({"query":"\"top 20\" contractor \"Washington State\" \"2017\" \"2018\""})
```
The Lance index was built without positions → phrase queries unsupported. **PLATFORM** config issue.

## TOOL: list_files — 0.6% (7/1254)

**3 validation errors**: `dataset_id` (singular) instead of `dataset_ids` (list). AGENT.

## TOOL: grep_file — <0.5% ✅ FIXED via `_strip_folder_prefix`.

1 error, same `wikipedia/Houston_Rockets` hallucination. Now silently normalized at the top of `grep_file`.

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
2. ✅ **One-shot envelope examples** for `download` and `peek_multiple`. Both tool docstrings now contain a CORRECT/WRONG block showing the exact envelope shape, listing the actual malformations from the eval logs. `download`'s validation error messages also echo the correct shape inline.
3. ✅ **Disambiguate `peek_file` vs `peek_files`.** Renamed `peek_files` → `peek_multiple` and rewrote both docstrings. The new docstring's CORRECT/WRONG block + the validation error message both name the alternative tool explicitly. Test pinned.
4. ✅ **Stop the `wikipedia/<Page>` hallucination.** Took option (b): `_strip_folder_prefix` silently strips a leading `wikipedia/` or `datagov/` (case-insensitive, also handles a leading `/`) at the top of `peek_file`, `read_file`, and `grep_file`. The agent's `wikipedia/<page>` form now resolves to the bare name without surfacing an error. ~41 errors addressed.
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
