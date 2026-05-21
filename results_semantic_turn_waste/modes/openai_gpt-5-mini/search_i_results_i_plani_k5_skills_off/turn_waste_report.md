# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_i_results_i_plani_k5_skills_off/eval_results.csv`
- Audited row count: 7
- Deterministic validation: 7 valid, 0 valid_with_warnings, 0 invalid/missing
- Model validation: 3 pass, 4 repaired_pass, 0 untrusted
- Total estimated wasted turns: 81
- Average estimated wasted turns: 11.6

## File-local groups

### Known-target search loops after the path was clear (4 rows, 46 estimated wasted turns)

The run had already narrowed the task to a specific remaining lookup, source family, or returned dataset, but spent the late budget on near-duplicate search reformulations instead of reading, aggregating, or moving to downstream hops.

Signals: Repeated search_ideal calls for the same target after no-result responses, after relevant datasets had already been returned, or after enough evidence existed to proceed; failures ended with unsupported estimates because later steps were starved of tool calls.

Representative task ids: tasks_mini/k-4-d-2/task_1.json, tasks_mini/k-6-d-2/task_4.json, tasks_mini/k-4-d-4/task_4.json

### Extraction and aggregation retries on located datasets (3 rows, 35 estimated wasted turns)

The run found the relevant state, source families, or datasets, then stalled on converting those sources into exact grouped counts through repeated incompatible parsing, schema, or aggregation attempts.

Signals: Repeated XML, GeoJSON, SQL, JSON, or unfiltered aggregation attempts after the relevant datasets were known; progress stopped at exact county or school-type counts rather than at source discovery.

Representative task ids: tasks_mini/k-4-d-4/task_10.json, tasks_mini/k-4-d-4/task_11.json, tasks_mini/k-5-d-3/task_14.json

## Global summary

Across the seven accepted failed rows, wasted turns concentrated in two local patterns: four rows repeated searches around an already-narrowed target or already-returned source, while three rows stalled on extraction and aggregation mechanics after finding the relevant datasets. Both patterns converted early productive discovery into unsupported final estimates by exhausting the tool budget before exact downstream facts were computed.

## Global findings

- The dominant failure mode was not initial task understanding; every row made meaningful early progress before the wasted tail.
- Four rows wasted budget on near-duplicate searches after the remaining target or relevant dataset family was already clear.
- Three rows wasted budget on repeated parsing, schema, or aggregation attempts against already-located education datasets.
- Several runs failed because they kept optimizing the current hop and left no tool calls for later required hops.
- No mixed or unclear group was needed because each row fit one of the two discovered patterns cleanly.

## Unresolved or mixed cases

None. All audited rows passed deterministic validation and model validation after conservative repairs where needed; the synthesis subagent assigned every accepted row to one of two local groups.

## Accepted rows

- `tasks_mini/k-4-d-4/task_10.json`: Extraction and aggregation retries on located datasets (12 wasted turns) - Found STFIP 19 and several relevant school-location datasets, but submitted an estimate without exact county-level aggregations.
- `tasks_mini/k-4-d-4/task_11.json`: Extraction and aggregation retries on located datasets (12 wasted turns) - Followed a Missouri Princeton/Mercer record, found the public-school dataset and a Missouri public-school count, then submitted an estimated answer without extracting private-school, district-office, or postsecondary counts.
- `tasks_mini/k-5-d-3/task_14.json`: Extraction and aggregation retries on located datasets (11 wasted turns) - Found ACT's Iowa City origin, resolved Johnson County and state FIPS 19, and got Iowa public-school top counties, but submitted an estimate before completing private-school, district-office, and postsecondary aggregations.
- `tasks_mini/k-4-d-2/task_1.json`: Known-target search loops after the path was clear (15 wasted turns) - Identified the qualifying school and ZIP, then failed to retrieve the final 2010 Census race-percentage source and submitted an unsupported estimate.
- `tasks_mini/k-6-d-2/task_4.json`: Known-target search loops after the path was clear (11 wasted turns) - The agent found the 500 Cities release files, confirmed their available obesity years, eventually retrieved top-city obesity rows showing Gary among the leading cities, then hit the tool limit while still searching for additional obesity data and submitted an estimated Pittsburgh Police Bureau expenditure.
- `tasks_mini/k-4-d-4/task_4.json`: Known-target search loops after the path was clear (10 wasted turns) - Agent found the health datasets, chose Chicago, identified Police as the overtime leader, found a relevant Chicago Police Department source, then spent the remaining budget on repeated salary searches and rechecking health data.
- `tasks_mini/k-5-d-3/task_11.json`: Known-target search loops after the path was clear (10 wasted turns) - Computed the crime-count top wards as 5 and 2, found street-sweeping datasets once, then never completed the street-sweeping counts or downstream charter school and birthplace hops.
