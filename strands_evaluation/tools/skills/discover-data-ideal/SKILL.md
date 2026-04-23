---
name: discover-data
description: Ideal-mode discovery behavior for `search_ideal`. Load before your first search call in ideal mode.
---

## How `search_ideal` works

`search_ideal` is the only search tool in this mode. Each call advances an internal cursor through the planned source sequence — the query text does not change which targets are returned; `top_k` controls how many advance per call.

Use it until the sequence is exhausted (`plan_exhausted=true`). You will most likely need all the planned sources.

## After each call

1. Inspect the returned `dataset_id`, `s3_uri`, `llm_desc`, `columns`, and `dataset_snippet`
2. Pivot to `query_file` or `grep_file` for extraction — use `peek_file` / `peek_multiple` only if the file structure is unclear
3. Do not spend multiple searches on the same step; the cursor advances on every call
