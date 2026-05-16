# Turn Waste Audit Report

Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_d_results_i_pland_k5_skills_off/eval_results.csv`

## Summary

- Audited runtime-failure rows: 8
- Trusted audited rows: 8
- Total estimated wasted turns: 44
- Average estimated wasted turns: 5.5
- Deterministic validation: all audited rows valid after rewrite
- Model validation: 7 pass, 1 repaired_pass

## File-Local Groups

### Over-narrow candidate verification blocked downstream lookup

The run narrowed to plausible candidate records, but spent late turns repeating similar filters or candidate checks rather than pivoting to the remaining linked lookup steps.

- Rows: 2
- Estimated wasted turns: 10
- Representative task ids: tasks_mini/k-4-d-4/task_13.json, tasks_mini/k-4-d-4/task_2.json

### Redundant dataset discovery before core aggregation

The run found the relevant datasets and inspected enough context to proceed, but continued broad discovery or re-opened known datasets instead of running the decisive aggregation or annual computation.

- Rows: 2
- Estimated wasted turns: 9
- Representative task ids: tasks_mini/k-3-d-4/task_5.json, tasks_mini/k-4-d-1/task_1.json

### Source access and parsing thrash after dataset found

The run located the relevant dataset or file family, but spent late turns retrying schema checks, wrong-file probes, malformed queries, or parser/code attempts instead of extracting the needed rows and completing the next reasoning step.

- Rows: 4
- Estimated wasted turns: 25
- Representative task ids: tasks_mini/k-3-d-3/task_2.json, tasks_mini/k-4-d-3/task_6.json, tasks_mini/k-4-d-3/task_7.json, tasks_mini/k-4-d-5/task_2.json

## Global Findings

- All rows show meaningful early progress before failure; the waste is concentrated in late turns after the likely data path was known.
- The largest group is source access and parsing thrash, covering 4 of 8 rows and 25 estimated wasted turns.
- Repeated discovery and reinspection accounted for 2 rows where the core aggregation was never executed or completed.
- Two rows stalled on over-narrow candidate verification, where similar filters were retried instead of pivoting to downstream lookups.
- The file-local pattern suggests budget failures were less about initial source discovery and more about failing to batch decisive extraction or aggregation once sources were found.

## Unresolved Or Mixed Cases

- None.

## Invalid, Missing, Or Untrusted Rows

- None.
