# Search Agent Navigation Assembly

Status: experimental paper skeleton

## Purpose

This document is the stricter experimental-paper version of the SANA project. It is not allowed to make claims that are not backed by measured results. If a section below does not yet have numbers, tables, confidence intervals, or figures, then the corresponding claim should remain a placeholder rather than prose.

## 1. Working Title

Possible title:

**When Retrieval Is Given, Budgeted Search Agents Still Fail on Execution**

Alternative title:

**Search Agent Navigation Assembly: Cost-Benefit Tradeoffs in Budgeted Tabular QA**

## 2. Claims Allowed Versus Not Yet Allowed

### Claims that are currently safe

- Idealized retrieval is a useful diagnostic lens.
- Runtime-failure traces suggest recurrent navigation failures such as repeated evidence gathering, rediscovery, and endgame overshoot.
- SANA is a concrete proposed intervention stack.

### Claims that are **not** yet safe without experiments

- “Planning is not the bottleneck.”
- “SANA improves accuracy.”
- “SANA is cost-neutral.”
- “These findings generalize to tool-using agents broadly.”

Any of these claims must be gated on actual results with uncertainty estimates.

## 3. Required Experimental Setup Section

The paper must define the following precisely:

- benchmark name
- number of tasks
- task distribution
- models used
- decoding settings
- number of seeds / reruns
- tool APIs exposed to the agent
- runtime budget definition
- operational definition of `results_ideal`
- operational definition of `plan_ideal`
- exact role of `SummarizingConversationManager`

Without this section, the paper is not reviewable.

### 3.1 Ideal retrieval must be operationalized

The paper must state exactly what “ideal retrieval” means. For example:

- gold dataset injection
- oracle top-k dataset family retrieval
- benchmark-authored curated source bundle

Different operationalizations imply different conclusions. This must not remain implicit.

## 4. Related Work Section Required

This paper needs a real related work section.

Minimum topics to position against:

- ReAct
- Reflexion
- Self-Refine
- Tree of Thoughts
- plan-and-solve prompting
- agent planning / controller papers
- long-horizon memory / summarization for agents
- prior systems work on tool-use efficiency or budgeted agents

The contribution must be framed as a runtime-control and systems-efficiency contribution, not as if reflection or planning were new.

## 5. Taxonomy Section Must Become Methodologically Defensible

The failure taxonomy cannot remain purely post-hoc narrative.

The paper needs:

- annotation protocol
- category definitions
- inclusion / exclusion rules
- boundary-case discussion
- representative examples per category
- ideally double annotation or at least adjudication procedure

At minimum, the paper should say who annotated the rows and how disagreements were resolved.

### 5.1 Current grouped counts to preserve

From `results-ec2_semantic_turn_waste_grouped/turn_waste_global_report.md`:

| Group | Count | Share |
| --- | ---: | ---: |
| Duplicate evidence re-querying | 54 | 26.2% |
| Rediscovery and re-orientation churn | 47 | 22.8% |
| Answer-ready closure chasing | 31 | 15.0% |
| Constraint-driven workaround thrash | 30 | 14.6% |
| On-path budget exhaustion | 25 | 12.1% |
| Unassigned | 19 | 9.2% |

These counts can be used descriptively, but the paper must explain how they were produced.

## 6. Stage 1: Planning Under Ideal Retrieval

This section should test the narrow claim that planning quality may be relatively strong under ideal retrieval.

### Required comparisons

- `plan_naive, results_naive`
- `plan_default, results_ideal`
- `plan_ideal, results_ideal`

### Required reporting

- sample size
- means
- variance or standard deviation
- confidence intervals
- seed count
- significance test or bootstrap comparison

### Rule

Do **not** write “planning is not the bottleneck” unless the 3% gap is shown to be robust and not plausibly noise.

## 7. Stage 2: SANA Ablation

Summarized memory is held fixed everywhere as default runtime infrastructure.

### Main additive ablation

- `Agent 0`: Ideal Retrieval + Default Plan + Basic Tools + `SummarizingConversationManager`
- `Agent 1`: Agent 0 + richer APIs and batched tools
- `Agent 2`: Agent 1 + plan budgeting and exit conditions
- `Agent 3`: Agent 2 + micro-reflection around each tool call
- `Agent 4`: Agent 3 + macro-reflection every `k` turns

### Why this order

- `Agent 1` addresses the “this is just bad tools” objection.
- `Agent 2` adds cheap static control.
- `Agent 3` adds local dynamic control.
- `Agent 4` adds long-horizon control and therefore must justify its overhead.

### Additive ablation is not enough

The experimental paper should also include at least one of:

- leave-one-out from `Agent 4`
- targeted pairwise comparisons
- selective disablements for interacting components

Otherwise component interactions cannot be isolated cleanly.

## 8. SANA Runtime Schemas

These schemas are design hypotheses, not truths. The experiments should validate whether they help.

### 8.1 Plan bullet

```json
{
  "goal": "short string",
  "estimated_tool_calls": 2,
  "exit_condition": "short string"
}
```

### 8.2 Pre-tool micro-check

```json
{
  "goal": "short phrase, <= 12 words",
  "why_this_tool": "one short sentence, <= 20 words",
  "what_success_looks_like": "one short sentence, <= 20 words",
  "confidence": 0.64
}
```

### 8.3 Post-tool micro-check

```json
{
  "current_step": "short phrase, <= 12 words",
  "next_step": "short phrase, <= 12 words",
  "sufficient_to_call_step_complete": true,
  "remaining_gap_if_not_complete": "short phrase, <= 15 words, empty if complete"
}
```

These fields should be treated as bounded natural-language control records, not as open-ended free-text reflections. The hard completion field is retained so that the runtime can still make explicit step-advancement decisions.

### 8.4 Macro-reflection

```json
{
  "evidence_retrieved": ["short label"],
  "remaining_budget": 8,
  "potential_answer": "short string",
  "confidence": 0.71,
  "global_status": "ON_TRACK | NEEDS_REPLAN | ANSWER_READY",
  "next_k_turn_objective": "short label",
  "should_submit": false
}
```

### 8.5 Hard-stop behavior

The paper should specify what happens when a step exhausts its estimated budget:

- forced checkpoint
- allowed outcomes: `REPLAN`, `ABANDON`, limited override

This should not be left to vague prompting.

## 9. Metrics

The experimental paper must report both benefit and overhead.

### Task metrics

- exact match
- semantic match
- solve rate

### Process metrics

- tool calls per run
- estimated wasted turns
- turn waste percentage
- time to first sufficient answer (`TTFSA`)
- turns-to-dataset-access at 50% coverage (`TDA@50`)
- turns-to-dataset-access at 100% coverage (`TDA@100`)
- token overhead per run
- cost per solved task
- fraction of runs whose answer was likely available before the final turn

### Required metric definition

`TTFSA` must be defined precisely as the first turn where the information needed for the correct final answer is already available in the trace.

`TDA@p` must be defined as the earliest turn at which the agent has accessed at least `p%` of the required datasets for the task.

These metrics are important because they separate:

- reaching the right datasets
from
- using those datasets well

If `TDA@100` is early but final performance is still poor, that is evidence for a navigation bottleneck rather than a retrieval bottleneck.

## 10. Required Tables and Figures

The final experimental paper should contain at least:

### Tables

1. Benchmark / setup table
2. Stage 1 planning comparison table with CIs
3. Stage 2 ablation table
4. Overhead / cost-benefit table

### Figures

1. Failure-category distribution
2. At least one example trace of rediscovery or closure chasing
3. Optional plot of `TTFSA` versus final solve outcome
4. Optional plot of `TDA@100` versus final solve outcome

Without trace examples, the taxonomy will read abstract and subjective.

## 11. Minimal Discussion Section

The discussion should stay within what the experiments support.

Allowed if supported:

- richer APIs reduce schema thrash
- plan budgeting reduces repeated work
- micro-reflection reduces duplicate evidence gathering
- macro-reflection improves long-horizon control but has overhead

Not allowed unless broadened experimentally:

- sweeping claims about all tool-using agents
- claims that retrieval is no longer important
- claims that the architecture generalizes beyond this benchmark family

## 12. Submission Gate

This document becomes a paper only when all of the following are true:

- benchmark and ideal-retrieval setup are defined
- Stage 1 numbers have uncertainty estimates
- Stage 2 ablation has been run
- overhead is measured
- related work is added
- taxonomy protocol is described
- the paper no longer contains proposal-only language where results should be
