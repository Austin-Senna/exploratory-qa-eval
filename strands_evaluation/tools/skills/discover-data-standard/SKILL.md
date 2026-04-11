---
name: discover-data
description: Hybrid dataset discovery workflow for `search_reranked`, `search_value`, `search_schema`, and `search_prefix`. Load this skill before calling search tools or list_files in standard search mode.
---

## Step 1: Start Precise, Then Broaden

Prefer `search_reranked` for the first high-precision discovery pass when you need the right dataset quickly.

Use:
- `search_reranked` for the first precise retrieval attempt
- `search_schema` when the question depends on column names or table titles
- `search_value` when you need broader recall or reformulation
- `search_prefix` when you already know the dataset naming pattern

## Step 2: Shape Queries Like Datasets

Write search queries as **source/program + grain + metric + time**.

| Bad query | Good query | Why |
|---|---|---|
| `school count` | `NCES public school locations county` | Agency + grain + metric |
| `violent crime` | `New York index crimes by county 2021` | Geography + metric + time |

## Step 3: Inspect the Dataset

When search returns a dataset ID, call `list_files`. Never guess file paths.

After `list_files`, use:
- `peek_multiple` for many files
- `peek_file` for one file

## When Search Fails

If the first precise result is weak:
1. reformulate with more exact program/geography/time terms
2. try `search_schema` for column-level matching
3. broaden with `search_value`
4. use `search_prefix` only after you have learned a likely dataset name fragment
