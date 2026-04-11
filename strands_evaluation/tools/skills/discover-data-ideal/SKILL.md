---
name: discover-data
description: Ideal-mode discovery workflow for `search_ideal`. Load this skill before using the ideal search tool or list_files in ideal search mode.
---

## Rule #1: `search_ideal` Is Not Broad Discovery

`search_ideal` is the only search tool in this mode.

Each call:
- searches only within the next dataset from `dataset_sequence`
- consumes that step

Do not use it for broad exploratory probing.

## Step 1: Decide What the Next Dataset Must Answer

Before each `search_ideal` call, infer from your current plan:
- what this dataset is supposed to verify
- which entity, field, or value signal you need from it

Ask only for that exact signal.

## Step 2: Pivot Quickly After the Search

After `search_ideal` returns a relevant result:
- use `list_files` if you need file structure
- use `peek_file` or `peek_multiple` to confirm schema
- use `query_file` or `grep_file` for extraction

Do not spend multiple broad searches on the same step. The cursor advances on every `search_ideal` call.

## When a Step Looks Weak

If a `search_ideal` result is weak:
1. inspect the returned dataset/file context directly if possible
2. continue the extraction workflow instead of broadening search
3. only advance if the current step is exhausted and the next dataset is required by the plan
