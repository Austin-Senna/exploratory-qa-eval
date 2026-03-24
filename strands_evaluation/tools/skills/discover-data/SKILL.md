---
name: discover-data
description: How to find datasets and files in the data lake using search and directory tools
---

## Finding Datasets

Use search to get dataset IDs, then `list_files` to inspect structure.

**Search tools:**
- `search_value` — hybrid RRF search (keyword + semantic); good broad recall for most queries
- `search_schema` — hybrid search over column/field names; use when you know the data structure you need
- `search_prefix` — S3 prefix search by dataset name fragment; use when you know part of the dataset or entity name

**Tips:**
- Dataset IDs often encode the answer — read the name before searching further (e.g. a dataset named `public-school-locations-by-county-2020` tells you its contents without opening it)
- Try at least two reformulations before giving up: broader terms, agency names (VA, HUD, BLS, CDC, FEMA), or government-specific terminology
- **Lexical pivot**: swap broad concept for agency term (e.g. "food stamps" → "SNAP", "unemployment benefits" → "ETA")
- **Granularity pivot**: if city-level fails, search state-level and filter in code
- **Proxy pivot**: if exact metric missing, find a standard proxy (e.g. "median income" for "poverty rate")

---

## Inspecting Dataset Structure

**NEVER guess file paths.** Always call `list_files` first to see what files exist, then use the exact paths returned.

Once you have a dataset id, call `list_files` to see what's inside. Then call `peek_files` with all the returned file paths at once — one tool call instead of one `peek_file` per file.

**Two dataset types:**

- **Wikipedia datasets** — `list_files` returns only `content.txt`. This is an encyclopedia article, not tabular data. Use `read_file` to extract facts (names, locations, dates, founding years). Do not try to query or download as data — move on once you have the fact you need.

- **datagov datasets** — contain actual data files under `files/` (CSV, JSON, TXT). These are the datasets you query for numerical answers. Activate the `query-data` skill for how to extract from them.

---

## Entity Resolution

Before searching, resolve the question's entities to government terminology:
- "food stamps" → "SNAP"
- "unemployment benefits" → "ETA", "insured unemployment", "UI beneficiaries"
- State/county names → FIPS codes (2-digit state, 5-digit county)
- School counts → NCES datasets (public-school-locations, private-school-locations, postsecondary)
