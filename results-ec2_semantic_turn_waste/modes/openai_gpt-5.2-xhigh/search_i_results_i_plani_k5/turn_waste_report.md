# Turn Waste Report

- Source file: `results-ec2_semantic/modes/openai_gpt-5.2-xhigh/search_i_results_i_plani_k5/eval_results.csv`
- Audited row count: 37
- Total estimated wasted turns: 118
- Average estimated wasted turns: 3.19

## Global Summary
Across 37 failed rows, the main waste modes were duplicate query loops on an already-known target and repeated school-location/NCES inspection spirals. A smaller set of runs drifted into unrelated or overly broad source hunting, while four rows were mostly on-track and simply ran out of budget before the final extraction.

## File-Local Groups
### On-track token cap (4)
Runs that were still following the intended path and hit the token or time limit before the final extraction or submission step, with no clear wasted-turn loop visible.

Signals: No meaningful repetition before the stop; MaxTokensReachedException or timeout while still on the intended trail; Useful source discovery was still in progress
Representative task ids: tasks_mini/k-2-d-3/task_2.json; tasks_mini/k-3-d-1/task_1.json; tasks_mini/k-3-d-4/task_3.json

### Duplicate query loops (13)
Runs that already had the candidate set or target dataset in hand, but kept rerunning the same or near-identical search, query, count, or validation step instead of closing out.

Signals: Repeated identical or near-identical queries; Same year, same table, or same candidate set rechecked after it was already visible; Stagnation warnings or tool-limit pressure after requerying
Representative task ids: tasks_mini/k-2-d-3/task_8.json; tasks_mini/k-3-d-3/task_1.json; tasks_mini/k-4-d-4/task_8.json

### Source drift and rediscovery (8)
Runs that widened or switched source families, reopened discovery after the path was already clear, or spent the tail on a small side-track instead of narrowing to the answer.

Signals: Generic continue, remaining sources, or baseline-source searches; Pivot to a mismatched dataset family; Rechecking already-known source families or a side article instead of finishing the intersection
Representative task ids: tasks_mini/k-3-d-4/task_7.json; tasks_mini/k-3-d-4/task_8.json; tasks_mini/k-5-d-3/task_5.json

### NCES school-location spiral (12)
Runs centered on NCES or school-location data that kept cycling through public, private, postsecondary, and district-office files, with repeated peeks, schema checks, or county/FIPS retries before the final aggregation.

Signals: Repeated discover-data, search, and peek cycles on the same school-location family; Public/private/postsecondary/district-office file rotation; Schema, GeoJSON, or binder retries while trying to finish a county-level count
Representative task ids: tasks_mini/k-6-d-4/task_1.json; tasks_mini/k-7-d-4/task_8.json; tasks_mini/k-7-d-4/task_9.json

## Global Findings
- The largest waste class is repeated querying of the same candidate set, usually after the answer path was already visible.
- NCES and school-location tasks form a distinct spiral pattern: repeated discover-data, peeks, and schema retries across public, private, postsecondary, and district-office files.
- A separate smaller pattern is source drift, where the agent reopens discovery or switches dataset families instead of narrowing to the final intersection.

## Unresolved Or Mixed Cases
- `tasks_mini/k-2-d-3/task_2.json`: estimated_wasted_turns=0; group=On-track token cap; The run ended while still in broad dataset discovery, before a college-count computation or ranking.
- `tasks_mini/k-3-d-1/task_1.json`: estimated_wasted_turns=0; group=On-track token cap; It exhausted tokens before mapping the final district back to taser incidents and Austin's incorporation-year calculation.
- `tasks_mini/k-3-d-4/task_3.json`: estimated_wasted_turns=0; group=On-track token cap; It was still following the right trail, but the run hit the token cap before the final year could be extracted.
- `tasks_mini/k-4-d-4/task_1.json`: estimated_wasted_turns=0; group=On-track token cap; It appears to have been on the right target but simply ran out of budget before producing the final date.
