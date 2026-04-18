# Semantic Evaluation Procedure

This document defines the new first-pass evaluation procedure for `results-ec2`.

The goal is to stop treating every non-EM submission as equally wrong, and to separate:

1. `Equivalent`
2. `Wrong Answer`
3. `Error-Turns exhausted`
4. `Error-Context exhausted`

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

## Label Definitions

### 1. `Equivalent`

The agent submitted a final answer, and the submitted answer is semantically equivalent to the gold answer.

Use the same semantic-equivalence logic as `analysis/build_semantic_results.py` as the starting point.

Examples that should upgrade from exact-match failure to `Equivalent`:

- `El Paso, Hidalgo` vs `El Paso County, Hidalgo County`
- formatting-only differences like surrounding brackets
- canonical name variants already handled by the semantic matcher

### 2. `Wrong Answer`

The agent submitted a final answer, but the answer is not semantically equivalent to the gold answer.

Important: this only applies when there is no exhaustion warning in the log tail.

Example from `results-ec2`:

- a task may hit `Tool limit reached ... submit_answer immediately`
- then still submit `[UNKNOWN]` or another incorrect answer
- under the stricter rule, this should still be an error bucket

### 3. `Error-Turns exhausted`

The log tail shows the run hit a turns / tool budget / time budget exhaustion signal.

Tail markers:

- `Tool limit reached`
- `Timeout reached`
- `Search call budget exhausted`
- `Call submit_answer NOW`

Under the stricter rule, this bucket still applies even if the agent later calls `submit_answer`.

### 4. `Error-Context exhausted`

The log tail shows the run hit a context or token exhaustion signal.

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

Submission markers are still useful, but they do not override exhaustion markers.

If the tail contains both:

- an exhaustion marker, and
- a later submit marker

the row should still be classified as an error bucket.

## Decision Order

For each task, classify in this order:

1. Read the last 20-30 lines of the task log.
2. Check whether the tail contains a context-exhaustion marker.
3. Else check whether the tail contains a turns-exhaustion marker.
4. Else check whether a final submission happened in that tail.
5. If context-exhausted:
   - `Error-Context exhausted`
6. Else if turns-exhausted:
   - `Error-Turns exhausted`
7. Else if submitted:
   - if semantic match is true: `Equivalent`
   - else: `Wrong Answer`
8. Else:
   - keep separate as infra/manual-review if it does not match the four buckets

Exhaustion beats submission.

If both context and turns exhaustion appear in the same tail, context should win.

## Why The Log Tail Matters

`results-ec2` contains many cases where the agent was warned about exhaustion and still submitted afterward.

So:

- do not classify from the first warning in the log
- do not classify from `error` alone
- use the tail to decide whether exhaustion happened, and which exhaustion type it was

Observed patterns in `results-ec2`:

- successful endings contain `submit_answer` and a final `ANSWER: ...`
- context-exhausted failures usually end with `MaxTokensReachedException`
- many logs show `Tool limit reached` or `Timeout reached` and then still submit; under the stricter policy those still count as error rows

## Current Scope

This four-way scheme is for answer quality plus exhaustion-style failures.

There are also a small number of infrastructure/API failures in `results-ec2` such as:

- `EventLoopException: Error code: 400 ... invalid JSON body`

Those do not naturally fit the four buckets above.

For `results-ec2`, `EventLoopException` is a Strands wrapper around an underlying event-loop failure. The concrete cases observed here are OpenAI `400` request failures saying the JSON request body was invalid. Treat these as infra/manual-review, not as turns exhausted or context exhausted.

## Short Version

- tail shows token/context overflow -> `Error-Context exhausted`
- else if tail shows tool/time/search-budget exhaustion -> `Error-Turns exhausted`
- else if submitted + semantic match -> `Equivalent`
- else if submitted + not semantic match -> `Wrong Answer`
