---
name: discover-data
description: How to find datasets and files in the data lake using search and directory tools. Load this skill before calling search_value, search_schema, search_prefix, or list_files. Reload it after 2 weak search results or when reformulating your search strategy.
---

## Step 1: Search with `search_value`

Always start with `search_value`. It's the broadest tool and works even when you don't know how datasets are named.

Shape queries as **source/program + grain + metric + time**. Government datasets use agency jargon — match it.

| Bad query | Good query | Why |
|---|---|---|
| `people entering prison system county` | `Texas county prison admissions fiscal year` | Specific program + geography + time |
| `NYC elementary school District 6 grade A` | `NYC school progress report grades District 6 2007-2011` | Dataset-shaped, not question-shaped |
| `food stamps by state` | `SNAP benefits state 2020` | Agency acronym, not colloquial name |

Use `search_schema` alongside `search_value` when you need to match on column or table names specifically.

---

## Step 2: Use `search_prefix` Only When You Know the Naming Convention

`search_prefix` does a direct path match on dataset names in the bucket. Only use it when you already know the naming pattern — typically lowercase with dashes or underscores (e.g. `index-crimes-by-county`, `public_school_locations`).

`search_prefix` returns **dataset IDs**, not file URIs. You still need `list_files` to see what's inside.

Do NOT start with `search_prefix` if you're guessing — use `search_value` first to learn how datasets are named, then `search_prefix` to narrow down.

---

## Step 3: Inspect the Dataset

When a search returns a **dataset ID** (not a direct file URI), call `list_files` to see its contents. **Never guess file paths** — guessed paths fail silently or hit the wrong file.

After `list_files` returns, call `peek_files` with all file paths at once (one tool call, not one per file).

### Two dataset types to recognize:

- **Wikipedia datasets** — `list_files` returns only `content.txt`. This is an encyclopedia article, not tabular data. Use `read_file` to extract facts (names, locations, dates, founding years). Do not try to query or download as data — move on once you have the fact you need.
- **datagov datasets** — Contain data files under `files/`. All files end in `.txt` (even CSVs). Use `query_file` or `grep_file` on these.

---

## Step 4: Verify Before You Trust

If the dataset name is **ambiguous or unfamiliar**, run `peek_files` before querying to confirm it's what you think it is. Dataset names can be misleading — two datasets with similar names may cover different states or time periods.

To verify:

1. Check headers for publisher, geographic scope, and date range
2. Run `SELECT * FROM t LIMIT 1` to confirm columns match your needs
3. If columns don't match, go back to search — don't force it

If the dataset name clearly matches your question (e.g. you searched for SNAP benefits and found `snap-benefits-by-state-2020`), you can skip peeking and go straight to querying.

---

## When Search Fails

If your first `search_value` returns fewer than 3 relevant results, do NOT repeat the same query. Reformulate:

1. **Swap to agency acronyms** — NCES, BLS, CDC, VA, HUD, FEMA, ETA
2. **Try `search_prefix`** if you picked up a naming pattern from earlier results
3. **Broaden geography** — search state-level, filter to county in code
4. **Use a proxy metric** — "median household income" instead of "poverty rate"

After two weak reformulations, replan. The dataset may not exist in this lake.
