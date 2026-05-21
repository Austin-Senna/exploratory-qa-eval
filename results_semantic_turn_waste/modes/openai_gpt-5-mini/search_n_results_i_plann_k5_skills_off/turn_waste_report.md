# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_n_results_i_plann_k5_skills_off/eval_results.csv`
- Output directory: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5-mini/search_n_results_i_plann_k5_skills_off`
- Audited runtime-failure rows: 2
- Deterministic validation: 2 valid, 0 invalid, 0 missing log
- Model validation: 2 pass, 0 repaired, 0 invalid/untrusted

## File-Local Groups

### Relevant data found, then low-yield lookup/probe loop before crash

- Rows: 2
- Representative task ids: `tasks_mini/k-4-d-1/task_6.json`, `tasks_mini/k-5-d-2/task_3.json`
- Description: Runs made meaningful early progress by locating relevant datasets or context, then spent later turns on repeated search, file, or column probing instead of advancing through the next concrete query step. Both ultimately stopped because of an event-loop/runtime failure rather than turn-budget exhaustion.
- Distinguishing signals: a useful source or intermediate result was already available; later turns reformulated nearby lookup/schema questions; the attempt ended in ReadError/EventLoopException.

## Wasted Turns

- Total estimated wasted turns: 17
- Average estimated wasted turns per audited row: 8.5
- Longest wasted tail: `tasks_mini/k-4-d-1/task_6.json` with 13 estimated wasted turns across Turns 5-17.

## Row Notes

- `tasks_mini/k-4-d-1/task_6.json`: Productive through Turn 4, including Atlanta as top PIT destination and a relevant `boundaries-us-zip-codes` search result, then repeated ZCTA/ALAND/Atlanta searches through Turn 17 before a Turn 18 ReadError/EventLoopException.
- `tasks_mini/k-5-d-2/task_3.json`: Spent Turns 5-6 on metadata/column query errors, Turn 10 on a low-yield metadata query, and Turn 15 on a CECounty query returning no rows. The run later corrected to SiteCounty and reached child-center enrollment queries before a Turn 21 ReadError/EventLoopException.

## Unresolved Or Mixed Cases

No accepted rows were invalid, missing-log, or untrusted. Both cases are mixed in the narrow sense that turn waste did not directly exhaust the run; runtime event-loop crashes were the final stop condition.
