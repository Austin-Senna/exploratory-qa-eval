# Turn Waste Report

Source file: `results_semantic/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off/eval_results.csv`
Mirrored output directory: `results_semantic_turn_waste/modes/openai_gpt-5-mini/search_i_results_i_pland_computei_k5_skills_off`

## Summary

- Audited runtime-failure rows: 8
- Deterministic validation: {'valid': 8}
- Model validation: {'repaired_pass': 3, 'pass': 5}
- Total estimated wasted turns: 57
- Average estimated wasted turns: 7.12

Most wasted turns came from budget-exhaustion tails after partial progress, especially repeated searches or parsing attempts around one unresolved fact. Two rows were runtime failures with no visible wasted tail, and one row showed a distinct post-answer-probing regression.

## Discovered File-Local Groups

### Repeated unresolved final-hop retrieval

- Count: 3
- Estimated wasted turns: 30
- Description: Runs made substantial progress, then spent the tail on near-duplicate searches, parsing, or extraction attempts for a missing final fact or dataset until the tool budget was exhausted.
- Representative task ids: tasks_mini/k-4-d-4/task_4.json; tasks_mini/k-4-d-4/task_6.json; tasks_mini/k-5-d-3/task_3.json
- Distinguishing signals: last productive chain was mostly complete; tail focuses on one missing fact/source; repeated no-result searches or low-yield parsing attempts; tool limit reached before final extraction

### Overworked intermediate step blocked later hops

- Count: 2
- Estimated wasted turns: 20
- Description: Runs got stuck re-querying or over-inspecting an intermediate stage, consuming budget before reaching later required datasets or computations.
- Representative task ids: tasks_mini/k-4-d-2/task_4.json; tasks_mini/k-5-d-4/task_2.json
- Distinguishing signals: progress stopped before all planned hops were attempted; repeated queries target an intermediate dataset or comparison; later required datasets remained untouched or unresolved; waste came from staying too long on a partially solved stage

### Post-answer probing after usable result

- Count: 1
- Estimated wasted turns: 7
- Description: The run had an answer-relevant result, but continued checking paths or parsing details until the hard stop caused a worse final answer.
- Representative task ids: tasks_mini/k-5-d-1/task_4.json
- Distinguishing signals: clear useful output was already available; later turns inspected parsing or file-location details; continued probing did not materially improve the answer; final answer regressed because the run hit the limit

### Runtime failure with no visible wasted tail

- Count: 2
- Estimated wasted turns: 0
- Description: Runs stopped because of streaming, event-loop, or runtime errors before a repeated low-yield tail was visible.
- Representative task ids: tasks_mini/k-5-d-3/task_13.json; tasks_mini/k-5-d-3/task_9.json
- Distinguishing signals: estimated wasted turns are zero; failure is runtime-level rather than search-strategy exhaustion; no repeated wasted behavior is visible; progress stopped because execution crashed or errored

## Row Notes

- `tasks_mini/k-4-d-2/task_4.json`: Overworked intermediate step blocked later hops; wasted turns 15; Found the relevant council, APD searches, CAD, and public-school datasets, but inferred the APD sector as Unknown from an overbroad search result and hit the tool limit before resolving CAD and Austin public-school counts.
- `tasks_mini/k-5-d-4/task_2.json`: Overworked intermediate step blocked later hops; wasted turns 5; The agent found the expenditure datasets, identified Transportation/MoDOT, found Springfield and Route 66 termini, then spent the tail repeatedly querying 500 Cities binge-drinking data and never reached the Chicago overtime datasets.
- `tasks_mini/k-5-d-1/task_4.json`: Post-answer probing after usable result; wasted turns 7; The agent found the relevant NYPD datasets, made several computation attempts, got output 258 at Turn 29, then continued with parsing/path checks until the tool limit forced [0].
- `tasks_mini/k-4-d-4/task_4.json`: Repeated unresolved final-hop retrieval; wasted turns 15; Found Chicago higher on binge drinking and Police highest for 2014-2017 overtime, then exhausted tools while searching for the 2025 Chicago Police starting salary and guessed [57000].
- `tasks_mini/k-5-d-3/task_3.json`: Repeated unresolved final-hop retrieval; wasted turns 11; Computed the release-county and county-seat chain, then submitted a guess after failing to retrieve the identified-student-percentage dataset.
- `tasks_mini/k-4-d-4/task_6.json`: Repeated unresolved final-hop retrieval; wasted turns 4; Computed candidate top-five capital-outlay counties, then spent the final tool calls trying to extract original-23 county text and submitted a best estimate without retrieving the criminal-release or VA recipient datasets.
- `tasks_mini/k-5-d-3/task_13.json`: Runtime failure with no visible wasted tail; wasted turns 0; The run failed during the first model response before any tool calls or answer submission.
- `tasks_mini/k-5-d-3/task_9.json`: Runtime failure with no visible wasted tail; wasted turns 0; Located the 2019-2021 library metric datasets, inspected them, and retrieved 2019 top branches for circulation, visitors, and computer sessions before crashing.

## Unresolved Or Mixed Cases

- No audited rows remain invalid or missing-log after deterministic validation.
- Runtime-failure rows are intentionally grouped apart because they show no visible behavioral waste tail.
