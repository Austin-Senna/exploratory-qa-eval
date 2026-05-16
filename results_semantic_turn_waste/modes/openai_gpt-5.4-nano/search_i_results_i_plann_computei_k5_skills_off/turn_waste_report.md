# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_plann_computei_k5_skills_off/eval_results.csv`
- Output eval: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_i_results_i_plann_computei_k5_skills_off/eval_results.csv`
- Audited runtime-failure rows: 2
- Total estimated wasted turns: 18
- Average estimated wasted turns: 9.0

## File-Local Groups

### Repeated intermediate recomputation after locating the path

- Count: 2
- Description: Runs made meaningful early progress locating relevant sources and computing several needed intermediates, then spent late budget on near-duplicate aggregation, ranking, or repair queries instead of advancing to the final lookup or submission.
- Distinguishing signals: relevant datasets or key intermediates were already found; later turns repeated similar aggregation or ranking work with small variations; the run stalled on intermediate validation or repair before the final answer step; failure came from hard timeout after repeated rechecking.
- Representative task ids:
  - `tasks_mini/k-4-d-3/task_6.json`: 9 estimated wasted turns
  - `tasks_mini/k-4-d-4/task_10.json`: 9 estimated wasted turns

## Findings

- Both failures involved 9 estimated wasted turns.
- The repeated work centered on intermediate computations: ordinance/salary rankings in one task and school county-count aggregations in the other.
- Both runs stopped after repair or rechecking behavior, not after a genuinely new reasoning branch.

## Unresolved Or Mixed Cases

- None. Both audited rows passed deterministic validation and model validation.
