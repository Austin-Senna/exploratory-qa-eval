---
name: discover-data
description: Ideal-mode discovery workflow for `search_ideal`. Load this skill before using the ideal search tool or list_files in ideal search mode.
---

## Rule #1: `search_ideal` Must Be Used Until Exhaustion

`search_ideal` is the only search tool in this mode.

Each call:
- consumes up to five datasets
- searches only within those datasets

Use it until exhaustion.
You will most likely need all the datasets.

## Step 1: Decide What the Next Batch Must Answer

Before each `search_ideal` call, infer from your current plan:
- what these datasets are supposed to verify
- which entity, field, or value signal you need from them

Ask only for that exact signal.

## Step 2: Pivot Quickly After the Search

After `search_ideal` returns a relevant result:
- use `list_files` if you need file structure
- use `peek_file` or `peek_multiple` to confirm schema
- use `query_file` or `grep_file` for extraction

Do not spend multiple broad searches on the same batch. The cursor advances on every `search_ideal` call.

## When a Step Looks Weak

If a `search_ideal` result is weak:
1. inspect the returned dataset/file context directly if possible
2. continue the extraction workflow instead of broadening search
3. only advance if the current batch is exhausted and the next batch is required by the plan
