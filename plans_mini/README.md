# plans_mini

`plans_mini` stores per-task plans used by ideal search + ideal management tooling.

## Path mapping
Use the same relative path as `tasks_mini`, replacing the root folder:

- Task: `tasks_mini/k-5-d-3/task_1.json`
- Plan: `plans_mini/k-5-d-3/task_1.json`

## Required file format
Each plan file must be JSON and must include these required fields:

```json
{
  "dataset_sequence": [
    "public-school-locations-2021-22-5a116",
    "private-school-locations-current-f7d96",
    "school-district-office-locations-2021-22-d5dd7"
  ],
  "reasoning_chain_text": "1. Sum December overdose deaths by year and select the maximum."
}
```

- `dataset_sequence`: ordered list of **dataset IDs only** (no `datagov/` prefix, no URI).
- `reasoning_chain_text`: canonical long-form plan text used for ideal prompt injection.
  - Keep this as scaffolding instructions only.
  - Do **not** include final answers, computed values, or phrases like `Final answer:`.
  - Do **not** include node labels like `Node 1:`.

## Optional convenience fields
These fields are optional and ignored by ideal-mode loaders, but useful for review:

- `original_final_question`: verbatim `question` copied from the source task file.
- `original_reasoning_chain`: verbatim `reasoning_chain` copied from the source task file.

## Current behavior in `search_ideal.py`
- `search_ideal` is the only search tool in ideal search mode.
- Each `search_ideal` call consumes exactly one dataset from `dataset_sequence` in order.
- When `dataset_sequence` is exhausted, `search_ideal` returns empty results with `plan_exhausted=true`.
- Missing/invalid plan files are treated as hard errors (no fallback to `tasks_mini`).

## Current behavior in `plan_ideal.py`
- `plan_ideal` is file-backed and loads from `plans_mini` for the active task.
- Manual `plan_text` input is ignored in file-backed ideal mode.
