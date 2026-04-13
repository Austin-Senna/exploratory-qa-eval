---
name: author-ideal-plans
description: Create, rewrite, and review repo-local `plans_mini` files used by ideal-mode `plan_ideal` and `search_ideal`. Use when Codex needs to draft a new mirrored `plans_mini/.../task_*.json` file, add or repair `source_sequence`, clean an existing `reasoning_chain_text`, or verify that `dataset_sequence`, `source_sequence`, and `reasoning_chain_text` are safe for ideal prompt injection.
---

# Author Ideal Plans

## Rule #1: Start From the Mirrored Task File

Read one source task under `tasks_mini/.../task_*.json` and write the mirrored plan under `plans_mini/.../task_*.json`.

Use `scripts/init_plan_file.py` first when the plan file does not exist yet. It initializes:
- `dataset_sequence` from the unique datasets referenced by `nodes`, in first-appearance node order
- `source_sequence` from node `source` values, one entry per node/use in node order
- `reasoning_chain_text` as a JSON list with one numbered placeholder step per dataset
- `original_final_question`
- `original_reasoning_chain`

Do not invent a different path layout.
Treat `datasets_used` as a coverage check: it should match the unique dataset IDs referenced by `nodes`, but it is not the ordering source of truth.
Treat the placeholder one-step-per-dataset scaffold from `init_plan_file.py` as a starting point only. Collapse it into cleaner grouped steps during the rewrite when adjacent datasets support the same logical action.
Treat `source_sequence` as the retrieval source of truth for `search_ideal`; do not deduplicate repeated node uses.

Resolve `source_sequence` entries with this initial rule:
1. start from each node's `source`
2. try the `.txt` version first
3. then try the original source
4. then try the `.json` version
5. for each candidate above, also try the normalized `/v1/files/` -> `/files/` form
6. if a candidate exists in `table_descriptions.jsonl`, store that file path
7. if no candidate is indexed, inspect likely real data files such as `files/data.txt`, or list the dataset files and choose the actual data body
8. if you still cannot verify the file choice, keep the best candidate temporarily and add `source_resolution_notes` so the plan is visibly blocked on manual review

`source_sequence` should now contain concrete dataset-relative file paths only.
Do not leave bare dataset ids in `source_sequence`.
If a chosen file path is not yet indexed in `table_descriptions.jsonl`, treat the plan as unresolved. Add or update that metadata entry, or mark the plan with `source_resolution_notes` until the file choice is verified.

## Draft the Plan in Dataset Order

Write `reasoning_chain_text` as a JSON list of numbered execution-scaffolding strings, not as a solved trace.

Keep the reasoning chain faithful to dataset order, but do not force a one-step-per-dataset rewrite when that makes the plan repetitive or reveals too much about the hidden dataset sequence.

Use these rules:
1. Preserve the overall first-appearance order from `dataset_sequence`.
2. State what must be verified or computed, but group adjacent datasets into a single step when they support the same subtask.
3. Split steps only when the user-facing operation genuinely changes.
4. When multiple yearly datasets share the same base source, mention the year or period explicitly in the relevant step or grouped step.

When a dataset is reused by multiple nodes, include it once in `dataset_sequence` using its first appearance in node order.
When a file is reused by multiple nodes, keep it repeated in `source_sequence` so ideal retrieval stays aligned to node order.

Prefer carry-forward language such as:
- `From the remaining counties, keep ...`
- `Using the city identified in step 4, determine ...`
- `For the counties from step 3, determine each county seat.`
- `For the county seats from step 4, determine when each was incorporated and keep the earliest one.`
- `For the universities identified in step 5, determine each founding year and return the earliest.`

Avoid oversplitting repeated lookups into dataset-by-dataset bookkeeping such as:
- `For one of the three counties from step 3, determine its county seat.`
- `For a second county from step 3, determine its county seat.`
- `For the remaining county from step 3, determine its county seat.`

Do not refer to datasets by raw URI or path inside `reasoning_chain_text`.
Describe each dataset by its role in the task rather than by its exact title when a neutral phrase is sufficient.
Do not refer to dataset positions, sequence slots, or hidden indexing machinery in `reasoning_chain_text`.
Do not write verification bookkeeping such as `verify it matches`; say directly what the agent should determine instead.
Aim for the middle ground:
- not raw dataset branding like `Chicago Cubs page` or `Chicago census data`
- not overly vague wording like `community-level income data` when the task really needs `Chicago community area` context

Prefer concrete task wording that names the place, entity type, and year or period when those details help readability.

Good:
- `Identify Chicago public elementary schools with the top performance rating in 2011-2012.`
- `Determine the Chicago community area for the schools that remain after the four school-performance filters.`
- `Return the year that MLB team was founded.`

Avoid:
- `Using the Chicago census data, ...`
- `Using the community-level income data, ...`
- `On the Chicago Cubs page, ...`
- `Using the university article in dataset position 6, verify it matches the university from step 5 and determine ...`
- `Using the first university article in the sequence after step 5, determine ...`
- `Determine node 6's headquarters city.`

Only surface a proper noun from a dataset title when the question already names it or the step would become ambiguous without it.

## Keep the Chain Clean

Treat `reasoning_chain_text` as prompt scaffolding for `plan_ideal`.

Keep it clean:
- no final answers
- no solved intersections
- no leaked entity names that should be discovered later
- no leaked numeric results that should be computed later
- no dataset-position or sequence-index narration
- no `verify it matches` bookkeeping language
- no repetitive one-dataset-at-a-time enumeration when one grouped step is clearer
- no `Node`, `node_`, `HOP`, `Final answer:`, or angle-bracket placeholders
- no raw `datagov/` or `wikipedia/` paths
- no audit-log narration of the original reasoning chain

Current ideal tooling prefers a cleaner execution plan than the source `reasoning_chain`.

Load `references/plan-format-and-rubric.md` when you need the exact lint rules.
Load `references/examples.md` when you need examples of clean rewrites and known bad patterns.

## Validate Before Accepting

Run `scripts/check_plan_cleanliness.py <plan_json_path>` on every authored or rewritten plan.

The validator must pass before the plan is considered ready.
It now validates both `dataset_sequence` and `source_sequence`.
It also fails when `source_resolution_notes` is still present or when a `source_sequence` entry is not indexed in `table_descriptions.jsonl`.

Store `reasoning_chain_text` as a JSON list so each step stays readable in the raw file. `plan_ideal` joins the list with `\n` at load time. Legacy string plans still load, but new and rewritten plans should use the list form. During review, render the list as plain lines:

```bash
jq -r '.reasoning_chain_text[]' plans_mini/k-2-d-4/task_1.json
```

If the validator reports issues:
1. revise `reasoning_chain_text`
2. rerun the validator
3. repeat until the output status is `clean`

## Run an Independent Review Subagent

After local validation passes, launch a fresh subagent for an independent cleanliness review.
If `source_resolution_notes` is present, launch a subagent before the final cleanliness pass to resolve those file choices first.

Give the subagent only:
- the task question
- the proposed `dataset_sequence`
- the proposed `source_sequence`
- the proposed `reasoning_chain_text`
- the cleanliness rubric

Do not give it the intended final answer.
Do not ask it to solve the task.

Use a prompt shaped like this:

```text
Use $author-ideal-plans at /absolute/path/to/author-ideal-plans to review the cleanliness of the reasoning chain for /absolute/path/to/plans_mini/.../task_X.json.

Return JSON only with:
- status: clean | needs_revision
- issues: [short strings]
- revision_notes: [short strings]

Review only for:
- dataset-sequence alignment
- source-sequence alignment
- answer leakage
- unnecessary exposure of dataset titles or page names
- over-split repetitive steps that should be grouped
- dataset-position or `verify it matches` phrasing
- placeholder/node/hop phrasing
- duplicate or underspecified steps
- whether each step is safe prompt scaffolding for plan_ideal

Do not solve the task.
Do not infer the final answer.
```

When `source_resolution_notes` is present, use a separate subagent prompt shaped like this:

```text
Use $author-ideal-plans at /absolute/path/to/author-ideal-plans to review unresolved source choices for /absolute/path/to/plans_mini/.../task_X.json.

Return JSON only with:
- status: resolved | needs_manual_review
- resolutions: [{index, chosen_source, rationale}]
- review_notes: [short strings]

Review only for:
- whether files/data.txt is the real data body
- whether another listed file is the real data body
- whether the chosen source is indexed in table_descriptions.jsonl

If you cannot verify a better file, say needs_manual_review and explain why.
Do not solve the task.
```

Accept the plan only after:
- `check_plan_cleanliness.py` returns `clean`
- the independent subagent returns `clean`

## Workflow Summary

1. Initialize the mirrored plan file with `scripts/init_plan_file.py` if needed.
2. Read the source task's `question`, `datasets_used`, `nodes`, and `reasoning_chain`.
3. Derive `dataset_sequence` from the unique datasets in node order, derive `source_sequence` from node `source` values in node order, cross-check the dataset coverage against `datasets_used`, and rewrite `reasoning_chain_text` into clean scaffolding that respects the dataset order without exposing hidden indexing.
4. If any source choice is unresolved, add `source_resolution_notes` and run the source-resolution subagent before accepting the file choice.
5. Run `scripts/check_plan_cleanliness.py`.
6. Run the independent review subagent.
7. Revise until all checks pass and `source_resolution_notes` is gone.
