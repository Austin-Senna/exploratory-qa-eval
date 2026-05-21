# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Output mirror: `results_semantic_turn_waste/modes/openai_gpt-5.4-nano/search_n_results_i_plani_computei_k5_skills_off/`
- Audited runtime-failure rows: 18
- Deterministically invalid or missing-log rows: 0
- Model validation: 14 pass, 4 repaired_pass, 0 invalid_untrusted
- Total estimated wasted turns: 156
- Average estimated wasted turns: 8.67

## File-Local Groups

### Redundant tabular recomputation and repair loops
- Count: 9
- Estimated wasted turns: 83
- Description: Runs repeatedly re-queried already-inspected tabular datasets, schema samples, ranking filters, or repaired SQL instead of advancing to the next reasoning hop.
- Representative task ids: `tasks_mini/k-3-d-3/task_2.json`, `tasks_mini/k-3-d-3/task_4.json`

### School or place lookup drift after identity found
- Count: 4
- Estimated wasted turns: 32
- Description: Runs identified the main school/place candidate but then drifted into repeated neighborhood, location, demographic, or structure lookups before resolving the downstream answer.
- Representative task ids: `tasks_mini/k-3-d-4/task_7.json`, `tasks_mini/k-3-d-5/task_1.json`

### Final-hop lookup left unresolved after key intermediate
- Count: 3
- Estimated wasted turns: 31
- Description: Runs found a key intermediate entity or winner, then spent turns on confirmation or broad lookup instead of resolving and submitting the final requested entity.
- Representative task ids: `tasks_mini/k-3-d-3/task_6.json`, `tasks_mini/k-5-d-3/task_6.json`

### Residual source probing for remaining denominator or evidence
- Count: 2
- Estimated wasted turns: 10
- Description: Runs had partial numeric or geographic progress, then used the remaining budget probing sources needed for one unresolved denominator or downstream evidence piece.
- Representative task ids: `tasks_mini/k-4-d-2/task_4.json`, `tasks_mini/k-5-d-4/task_2.json`

## Unresolved Or Mixed Cases

- No deterministically invalid rows, missing logs, or model-untrusted rows remained after repair.
- Group synthesis subagent attempt was blocked by a Codex usage-limit response after all row/model validation subagents completed; group labels above were synthesized from accepted row summaries in this session.

## Global Findings

- Most waste came from repeated tabular recomputation or schema/repair loops after useful intermediate evidence was already available.
- Several failures stalled after identifying a key school, place, county, agency, or winner, then failed to complete the final lookup hop before tool exhaustion.
- The highest-waste rows were usually not early crashes; they made real progress and then spent the tail on confirmation, duplicate filters, or source probing.
