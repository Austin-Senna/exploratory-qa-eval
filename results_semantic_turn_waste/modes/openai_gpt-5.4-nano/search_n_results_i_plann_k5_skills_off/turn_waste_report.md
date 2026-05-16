# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5.4-nano/search_n_results_i_plann_k5_skills_off/eval_results.csv`
- Audited row count: 1
- Trusted audited rows: 1
- Invalid or missing-log rows: 0
- Model-untrusted rows: 0

## Discovered File-Local Groups

### Repeated Dataset Reinspection and Query Reformulation (1)

The run found the relevant NCHS dataset and visible schema but spent later turns repeating metadata/file checks and trying near-duplicate county/category query variants, exhausting the tool budget before the final required lookup completed.

Distinguishing signals:
- Duplicate or low-yield schema/sample inspection after the dataset and columns were already known.
- Near-duplicate SQL query reformulations against the same NCHS county mortality data.
- Tool limit reached while attempting a late-stage required lookup.

Representative task ids:
- `tasks_mini/k-5-d-2/task_5.json`

## Wasted Turns

- Total estimated wasted turns: 6
- Average estimated wasted turns: 6.0

## Findings

The only trusted runtime-failure row shows late-stage repetition around an already-identified dataset rather than broad source discovery failure. It spent 6 estimated wasted turns on repeated NCHS sample/schema checks and county-name query variants before the required 2016 category lookup was cancelled by the 30-tool limit.

## Unresolved Or Mixed Cases

No unresolved, mixed, invalid, missing-log, or model-untrusted rows for this file.
