---
name: discover-data
description: Ideal-mode discovery behavior for `search_ideal`. Load before your first search call in ideal mode.
---

## How `search_ideal` works

`search_ideal` is the only search tool in this mode. It selects from the planned source pool based on your query text. Default behavior is to return one source. If your query clearly asks for an aggregate such as multiple years, all years, or multiple regions, it may return a matching group.

Use specific queries when you want one source, and explicit aggregate wording when you want a group. Once the remaining planned sources are exhausted, the tool returns `plan_exhausted=true`.

## After each call

1. Inspect the returned `dataset_id`, `s3_uri`, `llm_desc`, `columns`, and `dataset_snippet`
2. Pivot to `query_file` or `grep_file` for extraction — use `peek_file` / `peek_multiple` only if the file structure is unclear
3. Avoid repeating the same vague query. Refine the query toward the exact dataset or aggregate you need next
