# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results-ec2_semantic/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/eval_results.csv`
- Audited row count: 46
- Total estimated wasted turns: 150
- Average estimated wasted turns: 3.26

## Global Summary
Across 46 audited failures, the dominant waste came from school-location county schema hunts and same-dataset recomputation loops, with smaller clusters for duplicate search noise and late speculative verification. A smaller set of runs were mostly productive and stopped before any clear redundant tail emerged.

## Discovered Groups
### Late Verification and Fallback Checks (6)
Runs that were mostly solved, then spent the last turns on speculative verification, off-track pivots, heavy download fallbacks, or one last lookup that timed out.
Signals: One last speculative lookup or rough compute after the answer path was already assembled; Fallbacks into unrelated dataset families or heavy downloads instead of submitting; Final verification peeks that were cut off by timeout or stagnation warnings
Representative task ids: tasks_mini/k-3-d-1/task_1.json, tasks_mini/k-3-d-4/task_9.json, tasks_mini/k-4-d-4/task_3.json, tasks_mini/k-4-d-4/task_7.json, tasks_mini/k-4-d-4/task_8.json

### NYC School-Report Ranking Loops (8)
Runs that kept circling NYC school progress reports across years, rechecking similar report variants or clue pages even after the likely school or neighborhood was already narrowed.
Signals: Repeated NYC school progress-report queries across years; Reopening similar report variants or clue pages after the likely school was already in hand; Final neighborhood/location checks tied to museum, Park Slope, Prospect Park, or Bedford NTA clues
Representative task ids: tasks_mini/k-2-d-4/task_5.json, tasks_mini/k-3-d-3/task_1.json, tasks_mini/k-3-d-3/task_10.json, tasks_mini/k-3-d-3/task_3.json, tasks_mini/k-3-d-4/task_3.json

### No Clear Wasted Tail (6)
Runs that stayed mostly productive and hit the budget before a clear redundant tail emerged.
Signals: No obvious redundant loop before the budget stopped; Mostly productive exploration with only brief or unproven waste; Budget exhaustion happened before a clear repeated pattern emerged
Representative task ids: tasks_mini/k-2-d-3/task_2.json, tasks_mini/k-2-d-3/task_8.json, tasks_mini/k-2-d-4/task_3.json, tasks_mini/k-3-d-3/task_2.json, tasks_mini/k-4-d-3/task_5.json

### Redundant Search Reruns (7)
Runs that wasted turns on exact or near-exact search repeats, placeholder queries, or repeated first-pass topic searches that added little or no new information.
Signals: Exact or near-exact duplicate search terms; Placeholder or no-op searches such as `continue`; Repeating the first search pass before advancing to a new source
Representative task ids: tasks_mini/k-3-d-4/task_10.json, tasks_mini/k-5-d-3/task_3.json, tasks_mini/k-6-d-3/task_5.json, tasks_mini/k-6-d-4/task_5.json, tasks_mini/k-7-d-3/task_10.json

### Same-Dataset Recompute Loops (9)
Runs that kept rerunning the same metric, summary, or extraction on the same dataset family after the structure or answer path was already clear.
Signals: Rerunning the same metric, summary, or extraction on the same dataset family; Adjacent-year or same-file re-queries after the pattern was already visible; Repeated raw-file re-reads, count recomputations, or schema validation on the same evidence
Representative task ids: tasks_mini/k-2-d-4/task_2.json, tasks_mini/k-2-d-4/task_9.json, tasks_mini/k-3-d-4/task_7.json, tasks_mini/k-4-d-3/task_9.json, tasks_mini/k-5-d-3/task_5.json

### School-Location County Schema Hunts (10)
Runs that spent the tail probing school-location datasets for county fields or county counts, cycling through near-duplicate public/private/district/postsecondary files and schema keys instead of collapsing the result.
Signals: Repeated greps or peeks for county fields like `NMCNTY` and `STFIP`; Cycling across public, private, district, and postsecondary school-location files; Trying to turn school-location schemas into county counts without collapsing the result
Representative task ids: tasks_mini/k-4-d-4/task_5.json, tasks_mini/k-6-d-4/task_6.json, tasks_mini/k-6-d-4/task_8.json, tasks_mini/k-7-d-3/task_4.json, tasks_mini/k-7-d-3/task_8.json

## File-Level Findings
- The biggest recurring waste is repeated source inspection on near-duplicate school-location files, especially when hunting county fields or county counts.
- A second major pattern is same-dataset recomputation, where agents rerun the same query or summary with only minor parameter changes after the answer path is already visible.
- Duplicate search noise is a smaller but distinct cluster, including exact reruns, placeholder `continue` searches, and repeated first-pass topic searches.
- NYC school-progress tasks waste turns by circling year-by-year rankings and clue pages even after the target school or neighborhood has already been narrowed.
- Several runs are not very waste-heavy; they just hit token limits while still making forward progress.

## Unresolved Or Mixed Cases
- `tasks_mini/k-2-d-3/task_2.json`: No Clear Wasted Tail; wasted turns=0; The run was still in exploratory mode and hit the token cap before it could consolidate the yearly results.
- `tasks_mini/k-2-d-3/task_8.json`: No Clear Wasted Tail; wasted turns=0; The budget went into broad extraction across all six datasets, and the run crashed before the answer was assembled.
- `tasks_mini/k-2-d-4/task_3.json`: No Clear Wasted Tail; wasted turns=0; The run spent its budget on a long but mostly productive evidence-gathering pass and ended right at the timeout.
- `tasks_mini/k-3-d-3/task_2.json`: No Clear Wasted Tail; wasted turns=0; Most of the budget went into chasing the right linked datasets, and the crash came before the final join could finish.
- `tasks_mini/k-4-d-3/task_5.json`: No Clear Wasted Tail; wasted turns=0; The run spent almost all of its budget on exploratory joins and schema discovery and hit the token cap before finishing the last dataset.
- `tasks_mini/k-4-d-4/task_1.json`: NYC School-Report Ranking Loops; wasted turns=0; The agent was still comparing candidate files when the token budget collapsed, so it never reached a clean extraction path.
- `tasks_mini/k-4-d-4/task_4.json`: NYC School-Report Ranking Loops; wasted turns=0; The run was still in the discovery phase and hit the token limit before the honorific/family lookup was completed.
- `tasks_mini/k-5-d-4/task_4.json`: No Clear Wasted Tail; wasted turns=0; The run kept trying to reconcile county and assessment filters and ran out of budget before it could settle on the right county set.
- `tasks_mini/k-7-d-4/task_1.json`: School-Location County Schema Hunts; wasted turns=0; The task was still in dataset-discovery and schema-checking when the token cap hit.

## Output Files
- `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results-ec2_semantic_turn_waste/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/eval_results.csv`
- `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results-ec2_semantic_turn_waste/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/turn_waste_failures.csv`
- `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results-ec2_semantic_turn_waste/modes/openai_gpt-5.2-xhigh/search_i_results_i_pland_k5/turn_waste_report.md`
