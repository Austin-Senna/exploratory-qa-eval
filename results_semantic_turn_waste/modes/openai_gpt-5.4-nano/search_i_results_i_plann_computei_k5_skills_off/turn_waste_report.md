# Turn Waste Report

Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5.4-nano/search_i_results_i_plann_computei_k5_skills_off/eval_results.csv`
Audited runtime-failure rows: 2
Accepted rows for grouping: 2
Total estimated wasted turns: 11
Average estimated wasted turns: 5.5

## File-local groups

### Redundant data-query loops after useful progress (2)
Runs found relevant datasets and produced useful intermediate results, then spent limited remaining turns on repeated low-yield query or parsing variants instead of advancing to the final lookup or answer submission.

Signals:
- Relevant datasets or candidate results were already found before the wasted tail
- Repeated near-duplicate data operations with small filter/grouping changes
- Hard timeout occurred before final answer submission

Representative task ids:
- `tasks_mini/k-4-d-3/task_6.json`
- `tasks_mini/k-4-d-4/task_10.json`

## Row summaries

### `tasks_mini/k-4-d-4/task_10.json`
- Group: Redundant data-query loops after useful progress
- Estimated wasted turns: 9
- Wasted ranges: 7-11; 15-17; 24
- Summary: Found the relevant datasets and several Iowa rankings, but timed out before submitting an answer.
- Repeated behavior: Repeated public-school XML parsing with small changes to grouping/limit, often without the known STFIP filter.
- Stop point: By turn 23 it had top county counts for the main datasets; turn 24 then used an empty query_ideal SQL on the XML file and hit an XML unsupported error.

### `tasks_mini/k-4-d-3/task_6.json`
- Group: Redundant data-query loops after useful progress
- Estimated wasted turns: 2
- Wasted ranges: 24-25
- Summary: Located the relevant Chicago budget datasets and computed ordinance and salary metrics, but never reached the department-head lookup or final answer.
- Repeated behavior: Repeated 2019 salary recommendation variants after already getting 2019-2021 salary results for the candidate departments.
- Stop point: By turn 23 it had 2019-2021 salary recommendation results, then shifted into 2019-only recomputations and timed out.

## Validation
No invalid, missing-log, or model-untrusted audited rows in this file.

## Global summary
Both accepted failures show useful early dataset progress followed by redundant or low-yield data-query loops that consumed the remaining turn budget before submission.

- The common failure mode is not initial discovery, but failure to transition from intermediate results to the remaining final step.
- Repeated query reformulations appeared after enough information had been gathered to advance.
- One row wasted only the final two turns, while the XML case had a larger repeated-parsing tail across multiple turn ranges.
