---
name: discover-data
description: Sparse dataset discovery workflow for `search_value`, `search_schema`, and `search_prefix`. Load this skill before calling search tools or list_files in naive search mode.
---

## Step 1: Start with `search_value`

Always start with `search_value`. It is the broadest sparse search tool and works even when you do not know how datasets are named.

Shape queries as **source/program + grain + metric + time**.

| Bad query | Good query | Why |
|---|---|---|
| `people entering prison system county` | `Texas county prison admissions fiscal year` | Specific program + geography + time |
| `food stamps by state` | `SNAP benefits state 2020` | Agency acronym, not colloquial name |

Use `search_schema` when you need column or table-name matching specifically.

## Step 2: Use `search_prefix` Only After You Learn the Naming Pattern

`search_prefix` is a direct path match on dataset names in the bucket.

Only use it when you already know part of the dataset naming convention. Do not start with it if you are guessing.

## Step 3: Inspect the Dataset

When search returns a dataset ID, call `list_files`. Never guess file paths.

After `list_files`, use:
- `peek_multiple(files=[{dataset_id, file_path}, ...], max_rows=5)` for 2+ relevant files
- `peek_file(dataset_id, file_path)` for one file

## When Search Fails

If the first `search_value` result set is weak:
1. tighten terms with program + geography + time
2. try `search_schema` for exact field/table matches
3. use `search_prefix` only if you have learned a likely dataset name fragment
