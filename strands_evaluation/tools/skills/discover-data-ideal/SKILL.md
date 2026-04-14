---
name: discover-data
description: Ideal-mode discovery workflow for `search_ideal`. Load this skill before using the ideal search tool in ideal search mode.
---

## Rule #1: `search_ideal` Must Be Used Until Exhaustion

`search_ideal` is the only search tool in this mode.

Each call:
- consumes up to `top_k` planned source targets
- returns concrete file-backed results with dataset id, file URI, indexed description, and `dataset_snippet` when available

Use it until exhaustion.
You will most likely need all the planned sources.

## Step 1: Inspect The Returned Source

After each `search_ideal` call:
- pivot directly to extraction on the returned files

Do not spend multiple broad searches on the same step. The cursor advances on every `search_ideal` call.

## Step 2: Pivot Quickly After The Source Is Revealed

After `search_ideal` returns:
1. use `peek_file` or `peek_multiple` to confirm file structure when needed
2. use `query_file` or `grep_file` for extraction
