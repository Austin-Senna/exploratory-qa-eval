# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_plani_k5_skills_off/eval_results.csv`
- Audited row count: 3
- Trusted audited rows: 3
- Invalid/missing/untrusted rows: 0
- Total estimated wasted turns: 27
- Average estimated wasted turns: 9.0

## File-Local Groups

### Redundant Re-querying Before Advancing
- Count: 3
- Description: Runs repeatedly queried or validated already-sufficient intermediate data instead of moving to the remaining reasoning steps, causing the tool budget to expire before final lookup or aggregation.
- Distinguishing signals: repeated searches or query_file calls against the same datasets or candidate rows; intermediate evidence was already sufficient to proceed; final unresolved work was downstream of the repeated queries; hard tool limit was reached before completion.
- Representative task ids: `tasks_mini/k-5-d-4/task_6.json`, `tasks_mini/k-3-d-4/task_3.json`, `tasks_mini/k-3-d-4/task_7.json`

## Row Assignments

- `tasks_mini/k-3-d-4/task_3.json`: 8 wasted turns. The run repeated census-population searches and low-yield enrollment/assessment filter retries, leaving too little budget for the corrected final Math proficiency aggregation.
- `tasks_mini/k-3-d-4/task_7.json`: 7 wasted turns. After enough top-school candidate data was available, the run kept validating school-progress rows and DBNs instead of moving to neighborhood and museum lookup.
- `tasks_mini/k-5-d-4/task_6.json`: 12 wasted turns. The run repeatedly queried the same CDC diabetes and population subsets after recurring under-100k candidates were already identified, preventing completion of the bordering-city, county, and age-percentage steps.

## Global Findings

- All accepted rows show the same pattern: useful early progress, followed by rechecking or reformulating queries over already-touched data instead of advancing to unresolved hops.
- The repeated work clustered around already-located datasets, candidate validation, or filter/schema retries.
- No unresolved or mixed trusted cases remained after deterministic and model validation.
