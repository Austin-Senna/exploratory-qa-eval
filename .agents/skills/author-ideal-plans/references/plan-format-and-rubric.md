# Plan Format And Rubric

## Required JSON Shape

Each plan file mirrors one `tasks_mini/.../task_*.json` file and must stay in `plans_mini/.../task_*.json`.

Required keys:

```json
{
  "dataset_sequence": ["dataset-id-one", "dataset-id-two"],
  "source_sequence": [
    "datagov/example-dataset/files/rows.txt",
    "wikipedia/Example_Page/content.txt"
  ],
  "reasoning_chain_text": ["1. ...", "2. ..."]
}
```

Optional review-only keys:
- `original_final_question`
- `original_reasoning_chain`

## Dataset Sequence Rules

- Use bare dataset IDs only.
- Do not include `datagov/`, `wikipedia/`, full URIs, or file paths.
- Derive the order from the unique datasets referenced by `nodes`, using first appearance in numeric node order.
- If a dataset appears in multiple nodes, include it once at its first appearance.
- `datasets_used` should cover the same unique dataset IDs as `nodes`, but it is a coverage check rather than the ordering source of truth.
- Keep the reasoning chain aligned to this order, but adjacent datasets may be grouped into a single step when they support the same subtask.

## Source Sequence Rules

- Use one entry per node/use in numeric node order.
- Keep repeated file uses; do not deduplicate `source_sequence`.
- Each entry must be a dataset-relative file path such as `datagov/example-dataset/files/rows.txt`.
- Resolve node `source` values in this order:
  1. `.txt`
  2. original source
  3. `.json`
  4. for each of the above, also try `/v1/files/` -> `/files/`
- If one of those candidates exists in `table_descriptions.jsonl`, store the file path.
- If none are indexed yet, store the first normalized file-path candidate and then add/update the corresponding `table_descriptions.jsonl` entry.

## Clean Reasoning Chain Rules

Keep `reasoning_chain_text` as prompt scaffolding for `plan_ideal`.
Store it as a JSON list with numbered step strings.
Legacy single-string plans are still accepted on read, but rewrites should use the list form.

Required:
- Number steps `1.` through `N.` with no gaps.
- Keep the overall action order consistent with `dataset_sequence`, even when multiple adjacent datasets are grouped into one step.
- State the verification or computation clearly for each step.
- Use natural carry-forward references to prior steps when needed.
- Prefer concrete task descriptions over exact dataset titles or page names.
- Include the place, entity type, and year or period when those details help make the step readable.
- Prefer grouped wording when multiple parallel lookups are being performed over the same derived set.
- Avoid both extremes:
  - too dataset-literal: `On the Chicago Cubs page, record the year the team was founded.`
  - too generic: `Using the community-level income data, keep the schools ...`

Forbidden:
- `Node`, `node_`, `HOP`
- `dataset position`, `first article in the sequence`, or similar hidden-index phrasing
- `verify it matches` bookkeeping language
- `Final answer:`
- angle-bracket placeholders such as `<node_5 answer>`
- raw source paths such as `datagov/...` or `wikipedia/...`
- solved intersections
- discovered entity names not already present in the question
- computed values not already present in the question
- exact duplicate steps

## Known Failure Patterns

- Copied audit-trace style:
  - `HOP 1 ...`
  - `Node 4 ...`
  - `Intersection(1,2,3) -> {...}`
- Solved prompt scaffolding:
  - `What is the capital of Vermont?`
  - `Final answer: 1781`
- Repeated yearly steps with missing year context:
  - three identical steps for 2021, 2022, and 2023 datasets
- Over-split parallel lookups:
  - `For one of the three counties ...`
  - `For a second county ...`
  - `For the remaining county ...`
- Placeholder-heavy wording:
  - `What is <node_5 answer>?`
  - `Which of <intersection of node_1, node_2> ...`

## Good Style

Prefer wording like:
- `For fiscal year 2021, identify counties with prison-system entries between 700 and 4,600.`
- `Intersect the qualifying county sets across the four fiscal years.`
- `From the remaining counties, keep those with 2020 Census population under 900,000.`
- `For the counties from step 3, determine each county seat.`
- `For the county seats from step 4, determine when each was incorporated and keep the earliest one.`
- `For the universities identified in step 5, determine each founding year and return the earliest.`
- `Return the county names in alphabetical order, separated by comma and space.`
- `Identify Chicago public elementary schools with the top performance rating in 2011-2012.`
- `Determine the Chicago community area for the schools that remain after the four school-performance filters.`
- `Return the year that MLB team was founded.`

## Validation Commands

Initialize a mirrored scaffold:

```bash
python .agents/skills/author-ideal-plans/scripts/init_plan_file.py tasks_mini/k-2-d-4/task_1.json
```

Check a plan:

```bash
python .agents/skills/author-ideal-plans/scripts/check_plan_cleanliness.py plans_mini/k-2-d-4/task_1.json
```

Render the reasoning chain as actual lines during review:

```bash
jq -r '.reasoning_chain_text[]' plans_mini/k-2-d-4/task_1.json
```
