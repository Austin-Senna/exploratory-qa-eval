# Turn Waste Report

- Source file: `/Users/austinsenna/Documents/projects/daplab/exploratory-qa-eval/results_semantic/modes/openai_gpt-5-mini/search_i_results_i_plani_computei_k5_skills_off/eval_results.csv`
- Audited runtime-failure rows: 1
- Deterministic validation: 1 valid, 0 valid_with_warnings, 0 invalid, 0 missing_log
- Model validation: 1 pass, 0 repaired_pass, 0 invalid_untrusted
- Total estimated wasted turns: 9
- Average estimated wasted turns: 9.0

## Discovered File-Local Groups

### Post-answer cross-checking until timeout (1 row)

The run had enough information to answer but spent the remaining budget on repeated low-yield validation searches and checks.

Distinguishing signals:
- Key county/population comparison already available.
- Repeated population, unemployment, and biofuel checks.
- Multiple exhausted or empty follow-up searches.
- Hard timeout before submission.

Representative task ids:
- `tasks_mini/k-4-d-3/task_11.json`

## Findings

The only accepted row shows a solved-or-nearly-solved run that failed because it kept validating after the answer path was clear. By Turn 16, the run had Black Hawk County and Scott County populations with Scott County larger; Turns 21-29 continued cross-checking and the run hit the hard timeout at Turn 30.

## Unresolved Or Mixed Cases

None. The single audited row passed deterministic and model validation.
