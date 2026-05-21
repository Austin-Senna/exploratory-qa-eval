# Turn Waste Report

- Source file: `results_semantic/modes/openai_gpt-5.4-nano/search_d_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited row count: 1
- Trusted audited rows summarized: 1
- Total estimated wasted turns: 8
- Average estimated wasted turns: 8.00

## Discovered File-Local Groups

### Repeated low-yield probing of an already-found intermediate dataset (1)

The run located the relevant population source and extracted useful county rows, but then spent the remaining budget retrying and elaborating population-file queries instead of moving to the downstream school district enrollment lookup.

Distinguishing signals:
- Repeated query_ideal calls against the same population file after the dataset was already found
- Repeated grep_file probes over county population rows
- Progress stopped before the final required source lookup
- Hard timeout occurred during another population-file grep

Representative task ids:
- `tasks_mini/k-4-d-2/task_15.json`

## Global Summary

One accepted failed row was grouped. The file-local pattern is repeated low-yield work on an intermediate population source after locating it, ending in a hard timeout before the run reached the final enrollment evidence needed for submission.

## Global Findings

- The main waste pattern was not failure to find an initial source, but over-investment in the first-hop population dataset.
- The run made intermittent productive progress, including finding the dataset and retrieving county rows, but spent an estimated 8 turns on repeated or low-yield population queries and greps.
- The final failure was a hard timeout during another complex grep_file call, before the 2017-18 school district enrollment lookup was attempted.

## Unresolved Or Mixed Cases

- None. Deterministic validation status: `valid`; model validation status: `pass`.
