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

- Preloaded sources — gold `source_sequence` injected into the prompt with no search tools — is a useful diagnostic lens for isolating navigation failures.
- Runtime-failure traces suggest recurrent navigation failures such as repeated evidence gathering, rediscovery, and endgame overshoot.
- SANA is a concrete proposed intervention stack.

### Claims that are **not** yet safe without experiments

- "Planning scaffolding recovers most preloaded failures."
- "SANA improves accuracy."
- "SANA is cost-neutral."
- "These findings generalize to tool-using agents that must search."

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
- operational definition of **preloaded sources**
- operational definition of `plan_standard` and `plan_ideal` management modes
- exact role of `SummarizingConversationManager`

Without this section, the paper is not reviewable.

### 3.1 Preloaded sources — operational definition

Preloaded sources is the sole retrieval condition in the main experimental table. For each task:

- The gold `source_sequence` from the benchmark-authored plan is injected into the system prompt as a `## PRELOADED DATASETS` block listing `dataset_id` and S3 URI for every source.
- The agent is told explicitly that the list is complete and authoritative; it should not attempt to search.
- **No search tools are exposed** to the agent. `list_files`, `peek_file`, `read_file`, `grep_file`, `query_file`, `download`, `execute_code`, and `submit_answer` remain available.

Softer idealizations (e.g. a gold-sequence cursor search tool) are not used in the main paper because they reintroduce the pacing decisions — when to call search again, when to stop, how to interpret partial results — that the paper's thesis asks us to factor out. The `search_ideal` mode remains in the repository as a legacy comparison condition but is not part of the main results.

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

## 6. Stage 1: Planning Scaffolding Under Preloaded Sources

This section tests the narrow claim that planning scaffolding recovers or does not recover failures once retrieval is removed.

### Required comparisons

Two conditions, both with preloaded sources:

- **Oracle-Sources (no planning)** — `search=preloaded, plan=naive`. Agent has gold sources, no `plan()` tool, no skills plugin, no `summarize_context`.
- **Oracle-Sources + Planning** — `search=preloaded, plan=standard`. Same preloaded sources, plus the managed stack (`plan()`, skills, `summarize_context`, category-stagnation handler).

Interpretation:

- If Oracle-Sources + Planning substantially beats Oracle-Sources, planning scaffolding is load-bearing even when retrieval is solved.
- If the two conditions are close, failures under preloaded are not primarily addressable by planning scaffolding — they are deeper navigation/reasoning issues, motivating the SANA interventions in Stage 2.

### Required reporting

- sample size
- means
- variance or standard deviation
- confidence intervals
- seed count
- significance test or bootstrap comparison

### Rule

Do **not** write "planning scaffolding is sufficient" or "planning scaffolding does not help" unless the gap is shown to be robust and not plausibly noise.

## 7. Stage 2: SANA Ablation

Preloaded sources and `SummarizingConversationManager` are held fixed everywhere as default runtime infrastructure.

### Agent 0 — the baseline

- `Agent 0`: Preloaded sources + Default Plan + Basic Tools + `SummarizingConversationManager`.

Agent 0 is the Oracle-Sources (no planning) condition from §6. It is the baseline against which each intervention is measured.

### One-at-a-time interventions on top of Agent 0

Each of the following adds a single intervention to Agent 0. The interventions are independent toggles; none of them compose with each other in the main ablation.

- `Agent 1 = Agent 0 + rich_apis` — richer dataset-profile APIs (`peek_file` returns cached column stats, `top_2_rows`, `llm_description`).
- `Agent 2 = Agent 0 + plan_budget` — plan bullets with explicit `estimated_tool_calls` and `exit_condition`; hard-stop behavior on budget exhaustion.
- `Agent 3 = Agent 0 + micro_reflection` — structured pre-tool and post-tool check records around each tool call.
- `Agent 4 = Agent 0 + macro_reflection` — k-turn global reflection with `should_submit` / `global_status` decisions.

### Cumulative stack

A sixth condition — `Agent Full = Agent 0 + rich_apis + plan_budget + micro_reflection + macro_reflection` — runs all four interventions together and serves as the cumulative-stack result. Reporting both one-at-a-time and cumulative lets the paper distinguish "each intervention helps" from "only the combination helps."

### Why this structure

One-at-a-time isolates each intervention's contribution to the Oracle-Sources baseline. Strict additive ordering (Agent k = Agent k-1 + intervention k) cannot answer "does intervention k help?" because the answer is always entangled with everything before it. One-at-a-time also makes the structure symmetric: the same five numbers (Agents 0-4) are directly comparable deltas on the same baseline.

Cumulative (`Agent Full`) is kept because interactions may be non-additive — the paper should be able to report both the isolated effects and the combined effect.

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
- preloaded-source engagement rate — fraction of preloaded URIs the agent ever opens
- token overhead per run
- cost per solved task
- fraction of runs whose answer was likely available before the final turn

### Required metric definitions

`TTFSA` must be defined precisely as the first turn where the information needed for the correct final answer is already available in the trace.

**Preloaded-source engagement rate** is the per-task fraction `|opened ∩ preloaded| / |preloaded|`, where `opened` is the set of URIs the agent inspected via any read tool. Under preloaded sources, the classical "turns-to-dataset-access" metrics (`TDA@50`, `TDA@100`) are degenerate — the agent has all sources at turn 0 — so we replace them with engagement rate, which measures whether the agent *uses* what it was given.

These metrics are important because they separate:

- engaging with the preloaded sources
from
- extracting the right answer from them

If engagement rate is high but final performance is low, that is evidence for a post-retrieval navigation bottleneck rather than a "did not look at the data" failure.

## 10. Required Tables and Figures

The final experimental paper should contain at least:

### Tables

1. Benchmark / setup table (including the preloaded-sources operationalization per §3.1)
2. Stage 1 two-cell comparison table (Oracle-Sources vs Oracle-Sources + Planning) with CIs
3. Stage 2 ablation table: rows for Agent 0, Agent 1–4 (each = Agent 0 + single intervention), Agent Full (all four interventions)
4. Overhead / cost-benefit table — per-intervention token and turn cost

### Figures

1. Failure-category distribution across the Stage 1 cells
2. At least one example trace of rediscovery or closure chasing under preloaded
3. Optional plot of `TTFSA` versus final solve outcome
4. Optional plot of preloaded-source engagement rate versus final solve outcome

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

- benchmark and preloaded-sources setup are defined
- Stage 1 numbers (Oracle-Sources, Oracle-Sources + Planning) have uncertainty estimates
- Stage 2 ablation has been run (Agent 0, Agents 1–4 one-at-a-time, Agent Full)
- overhead is measured per intervention
- related work is added
- taxonomy protocol is described
- the paper no longer contains proposal-only language where results should be
