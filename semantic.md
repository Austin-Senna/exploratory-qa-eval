# Semantic Evaluation Procedure

This document defines the new first-pass evaluation procedure for `results-ec2`.

The goal is to stop treating every non-EM submission as equally wrong.

The reporting should separate:

1. submitted answer quality
2. exhaustion status

## Core Rule

Do not use `exact_match` alone.

Use two signals together:

1. Semantic answer matching
2. The last few lines of the task log, especially whether the agent actually submitted a final answer

## Files To Read

For each task:

- answer/result row:
  - `results-ec2/modes/<model>/<mode>/eval_results.csv`
  - or `results-ec2/modes/<model>/<mode>/agent_results.jsonl`
- task log:
  - `logs-ec2/modes/<model>/<mode>/<k-*-d-*>/task_<n>.log`

The log tail is the source of truth for error classification.

## Reported Buckets

The final reported buckets should be:

- `semantic_equivalents`
- `semantic_equivalents_but_exhausted`
- `wrong_answers`
- `wrong_answers_but_exhausted`
- `unsubmitted_turns_exhausted`
- `unsubmitted_context_exhausted`
- `infra_event_loop_exception`

These are derived from two separate dimensions:

1. whether the agent submitted an answer and whether it was semantically correct
2. whether the log tail shows turns exhaustion or context exhaustion

### 1. `semantic_equivalents`

The agent submitted a final answer, the answer is semantically equivalent to the gold answer, and there is no exhaustion marker in the log tail.

Use the same semantic-equivalence logic as `analysis/build_semantic_results.py` as the starting point.

Examples that should upgrade from exact-match failure to `Equivalent`:

- `El Paso, Hidalgo` vs `El Paso County, Hidalgo County`
- formatting-only differences like surrounding brackets
- canonical name variants already handled by the semantic matcher

### 2. `semantic_equivalents_but_exhausted`

The agent submitted a final answer, the answer is semantically equivalent to the gold answer, but the log tail still shows exhaustion.

This is the bucket that captures the previously confusing cases where the answer was right but the run had already hit `Tool limit reached` or `Timeout reached`.

### 3. `wrong_answers`

The agent submitted a final answer, the answer is not semantically equivalent to the gold answer, and there is no exhaustion marker in the log tail.

### 4. `wrong_answers_but_exhausted`

The agent submitted a final answer, the answer is not semantically equivalent to the gold answer, and the log tail shows exhaustion.

### 5. `unsubmitted_turns_exhausted`

The agent did not successfully submit a final answer, and the log tail shows a turns / tool budget / time budget exhaustion signal.

Tail markers:

- `Tool limit reached`
- `Timeout reached`
- `Search call budget exhausted`
- `Call submit_answer NOW`

### 6. `unsubmitted_context_exhausted`

The agent did not successfully submit a final answer, and the log tail shows a context or token exhaustion signal.

Tail markers:

- `MaxTokensReachedException`
- `max_tokens limit`
- `Context window overflow`
- `ValidationException` together with a message that the context/request was too long

## Submission Detection

When checking the last few lines of the log, treat the run as submitted if any of these appear near the end:

- `Executing: submit_answer(`
- `Tool result: Answer submitted:`
- `Answer submitted! Triggering native agent cancellation.`
- `ANSWER:`

Submission markers are still useful because they tell us whether the row belongs in one of the submitted-answer buckets or one of the unsubmitted exhaustion buckets.

## Decision Order

For each task, classify in this order:

1. Read the last 20-30 lines of the task log.
2. Detect whether the tail shows:
   - context exhaustion
   - turns exhaustion
   - submission
3. If context exhaustion is present:
   - if submitted and semantic match is true: `semantic_equivalents_but_exhausted`
   - if submitted and semantic match is false: `wrong_answers_but_exhausted`
   - if not submitted: `unsubmitted_context_exhausted`
4. Else if turns exhaustion is present:
   - if submitted and semantic match is true: `semantic_equivalents_but_exhausted`
   - if submitted and semantic match is false: `wrong_answers_but_exhausted`
   - if not submitted: `unsubmitted_turns_exhausted`
5. Else if submitted:
   - if semantic match is true: `semantic_equivalents`
   - else: `wrong_answers`
6. Else if the row has `EventLoopException`:
   - `infra_event_loop_exception`
7. Else:
   - manual review / infra

If both context and turns exhaustion appear in the same tail, context should win.

## Why The Log Tail Matters

`results-ec2` contains many cases where the agent was warned about exhaustion and still submitted afterward.

So:

- do not classify from the first warning in the log
- do not classify from `error` alone
- use the tail to decide whether exhaustion happened, which exhaustion type it was, and whether the agent still submitted afterward

Observed patterns in `results-ec2`:

- successful endings contain `submit_answer` and a final `ANSWER: ...`
- context-exhausted failures usually end with `MaxTokensReachedException`
- many logs show `Tool limit reached` or `Timeout reached` and then still submit; these should be counted as `semantic_equivalents_but_exhausted` or `wrong_answers_but_exhausted`

## Current Scope

This four-way scheme is for answer quality plus exhaustion-style failures.

There are also a small number of infrastructure/API failures in `results-ec2` such as:

- `EventLoopException: Error code: 400 ... invalid JSON body`

Those do not naturally fit the semantic/exhaustion buckets above.

For `results-ec2`, `EventLoopException` is a Strands wrapper around an underlying event-loop failure. The concrete cases observed here are OpenAI `400` request failures saying the JSON request body was invalid. Treat these as infra/manual-review, not as turns exhausted or context exhausted.

## Short Version

- submitted + semantic match + no exhaustion -> `semantic_equivalents`
- submitted + semantic match + exhaustion -> `semantic_equivalents_but_exhausted`
- submitted + wrong answer + no exhaustion -> `wrong_answers`
- submitted + wrong answer + exhaustion -> `wrong_answers_but_exhausted`
- no submit + turns exhaustion -> `unsubmitted_turns_exhausted`
- no submit + context exhaustion -> `unsubmitted_context_exhausted`
