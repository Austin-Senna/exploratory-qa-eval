---
name: discover-data
description: Ideal-mode discovery workflow for `search_ideal`. Load this skill before using the ideal search tool in ideal search mode.
---

## Rule #1: `search_ideal` Must Be Used Until Exhaustion

`search_ideal` is the only search tool in this mode.

Each call:
- consumes up to `top_k` planned source targets
- returns concrete file-backed results with `dataset_id`, `s3_uri`, and, in ideal result mode, `llm_desc`, `columns` or `type`, and `dataset_snippet`

Use it until exhaustion.
You will most likely need all the planned sources.

## Step 1: Inspect The Returned Source

After each `search_ideal` call:
- pivot directly to extraction on the returned files

Do not spend multiple broad searches on the same step. The cursor advances on every `search_ideal` call.

## Step 2: Pivot Quickly After The Source Is Revealed

After `search_ideal` returns:
1. use `peek_file` for one file or `peek_multiple(files=[{dataset_id, file_path}, ...], max_rows=5)` for 2+ files to confirm file structure when needed
2. use `query_file` or `grep_file` for extraction
