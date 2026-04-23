# Search Agent Navigation Assembly

Status: position paper / research agenda draft

## Abstract

Search is an obvious bottleneck in tool-using agents, but it is not the only one. This paper argues for a diagnostic lens in which retrieval is factored out entirely — the agent is handed the gold source list in its prompt and given no search tools — so that a different systems problem becomes visible: navigation after the right evidence is already available.

Our contribution is a **methodology**: a preloaded-sources experimental setup, a five-level ablation (Agent 0 baseline plus four independent intervention toggles) called Search Agent Navigation Assembly (SANA), and a metric set that separates "did the agent engage with the evidence" from "did it extract the right answer." We do *not* yet claim which of the four interventions — richer dataset-profile APIs, plan bullets with exit conditions, micro-reflection around tool calls, or macro-reflection every *k* turns — carries the most weight. Which wins is the empirical question the setup is built to answer. The paper's value is a structured map of the control surface, together with falsifiable per-intervention hypotheses, not a premature claim about the optimal intervention mix.

## 1. Introduction

When budgeted tool-using agents fail on tabular QA, it is tempting to blame retrieval first. Often that is correct. But an interesting failure mode appears when retrieval is removed from the picture: agents still thrash. They inspect schema instead of extracting. They re-query evidence they already have. They keep validating after the answer is effectively available. They fail to open some of the preloaded sources at all.

This paper proposes a research methodology for studying that residual failure. We ask:

> If the agent is given the complete set of datasets needed to answer the task — as an authoritative list in its system prompt, with no search tools available — can it then reason over tabular data under budget, and which runtime-control interventions most cheaply close the remaining gap?

We do not yet have a definitive answer to the second half of that question, and we say so explicitly. The paper's contribution is the methodology to answer it: a preloaded-sources diagnostic lens, a SANA ablation that tests four runtime-control interventions in isolation on a common baseline, and a metric set designed to separate engagement failures from extraction failures.

## 2. Preloaded Sources as a Diagnostic Lens

The point of this setup is not to claim that search is solved in deployment. The point is to isolate the residual problem. If we do not control retrieval, every later failure can be explained away as "the agent never found the right source." That makes it impossible to learn whether the agent is also failing after it has already reached the correct evidence.

We operationalize "retrieval is removed from the attribution surface" in the strongest way available: the agent receives the complete gold `source_sequence` for each task as an authoritative block in its system prompt, and is given **no search tools at all**. We call this setup *preloaded sources*. Softer idealizations — such as a gold-sequence cursor search tool — still force the agent through pacing decisions (when to call search again, when to stop, how to interpret partial results) that contaminate the navigation signal we are trying to measure. Preloaded sources removes that confound.

### 2.1 What preloading changes, beyond removing retrieval

Preloading is not a neutral intervention on the task. It changes the agent's priors over what is relevant, anchors attention to the listed URIs, and may create new failure modes — for example, the agent may over-trust the preloaded set and ignore cues that should trigger broader reasoning, or it may engage with every listed source whether or not it is needed for the current task. A diagnostic lens is only useful if the failures it surfaces resemble the failures that occur in deployment; we explicitly note that this is an assumption, not a demonstrated equivalence. The experimental follow-up should compare the failure-category distribution under preloaded against the same distribution under a genuinely-search-free control (e.g. `search_ideal`) to bound how much of the signal is preloading-induced rather than intrinsic to post-retrieval execution.

### 2.2 What the lens supports

Under this lens, the paper can make two kinds of claim:

- if failure persists with the gold sources already in the prompt, retrieval is not the full story
- if a specific intervention recovers a measurable share of those failures, that intervention is load-bearing for post-retrieval execution in the preloaded regime

Claims beyond "in the preloaded regime" require separate evidence; we do not make them in this paper.

## 3. Motivating Observations

This paper is motivated by two preliminary observations rather than by a complete validated experiment.

### 3.1 Long traces destabilize agents

Agents often degrade after enough turns. They lose track of what has already been established, reopen stale branches, and start making locally plausible but globally unhelpful moves. This is why the default runtime in our proposal uses summarized memory rather than a pure sliding context. The point is not only token compression. The point is to preserve structured progress state.

### 3.2 The dominant failure patterns are execution failures

In grouped runtime-failure analysis, the recurring patterns are not only “could not find the dataset.” They are also:

- repeated evidence re-querying
- rediscovery and re-orientation churn
- answer-ready closure chasing
- schema and workaround thrash

These categories still need a more rigorous annotation protocol before they can function as a formal measurement artifact in a submission-ready paper. For this position paper, they serve as descriptive motivation for the architecture.

## 4. SANA: The Proposed Runtime Stack

Search Agent Navigation Assembly is a runtime control stack layered on top of a budgeted tool-using agent with summarized memory. §4.1 is infrastructure (held fixed everywhere). §4.2–§4.5 are four independent intervention toggles that the experimental setup tests one at a time on the Agent 0 baseline, plus as a combined stack. The paper does not commit to a ranking among them; which one dominates is the empirical question.

### Figure 1 (placeholder)

Intended diagram: a single control-loop figure showing, from the outside in — `SummarizingConversationManager` as the base memory substrate, a plan with per-step `estimated_tool_calls` and `exit_condition` as the static schedule, a pre-tool micro-check record → tool call → post-tool micro-check record as the local control loop, a macro-reflection checkpoint firing every *k* turns or on budget-threshold events, and a dataset-profile API drawn as a separate tool surface that sits alongside the basic data tools. One figure, ~1/3 page. The final paper should produce this; it is load-bearing for reader retention.

### 4.1 Summarized memory as infrastructure

SANA assumes that the default runtime already maintains a structured running summary of:

- solved subgoals
- current subgoal
- active source family
- key evidence retrieved
- current best answer
- confidence
- remaining budget

This is treated as infrastructure, not as one of the later interventions.

### 4.2 Plan bullets with exit conditions and tool budgets

Each plan step should specify:

- `goal`
- `estimated_tool_calls`
- `exit_condition`

The objective is to make progress explicit and to give the runtime a notion of when a step should be considered done or over-budget.

### 4.3 Micro-control around each tool call

Before each tool call, the agent should produce a tiny control record. After each tool call, it should produce another tiny control record. These checks should use bounded natural language rather than unrestricted free text: short phrases or one-sentence fields with explicit length limits.

The goal is local control:

- what is this tool call for?
- what would count as success?
- did it complete the current step?
- what is the next step if not?

The recommended before-tool fields are:

- `goal`
- `why_this_tool`
- `what_success_looks_like`
- `confidence`

The recommended after-tool fields are:

- `current_step`
- `next_step`
- `sufficient_to_call_step_complete`
- `remaining_gap_if_not_complete`

The important design constraint is that these fields stay short. The purpose is local control, not essay-style self-explanation.

The right schema granularity for bounded-NL fields — exact length caps, whether enforcement is structural (validator) or social (prompt instruction), the failure mode when an agent emits a plausible-sounding short phrase that does not actually reflect its internal state — is an open design question. We flag it for the experimental follow-up rather than resolving it here.

### 4.4 Macro-reflection every `k` turns

Sparse macro-reflection should happen every `k` turns and on event triggers such as:

- repeated failure to finish a step
- source-family switching attempts
- low remaining budget
- timeout warnings

The goal here is not local step completion but thread-level control:

- are we still on the right path?
- should we submit?
- should we replan?
- what is the cheapest useful next block of work?

### 4.5 Better dataset-profile APIs

The runtime should expose deterministic dataset profiles so the agent does not need to rediscover:

- column names
- types
- row counts
- family names
- ranges
- missingness
- distinct-count summaries
- obvious temporal coverage

This is a direct response to schema thrash and repetitive probing with `read_file`, `grep_file`, and trivial SQL queries.

## 5. Why This Is a Systems Problem

SANA is motivated by a systems view of agent failure.

The problem is not simply that the model needs to "think harder." The problem is that the runtime gives the model too little structured support for:

- knowing when a step is complete
- tracking remaining budget
- preserving long-horizon state
- deciding when to stop
- choosing cheap tools over expensive exploratory rituals

Under this view, many wasted turns are interface failures and control failures, not just reasoning failures.

### 5.1 Why runtime control, not better models

A reader may reasonably object that most of SANA would be unnecessary with a sufficiently strong base model — one that handles long context reliably, follows complex instructions without scaffolding, and stops on its own once the answer is evident. We address this directly rather than assuming the systems frame.

Three arguments for why runtime control remains load-bearing even at the frontier:

1. **Degradation on long-horizon budgeted tool use persists at the top of the model ladder.** In internal runs on a frontier-class model, agents still exhibit the same degradation patterns — schema thrash, duplicate evidence gathering, closure chasing — on tasks that require more than ~20 tool calls. The experiments in this paper are intentionally run on a strong base model so that any remaining SANA benefit cannot be dismissed as "weaker models need scaffolding."

2. **Runtime control is orthogonal to model capability.** Plan bullets with exit conditions, micro-reflection around tool calls, and richer APIs help a weak model and a strong model for different reasons: the weak model needs the guardrails, the strong model uses them as inexpensive coordination primitives. Orthogonality is testable; we do not assume it, but the preloaded setup with a frontier model puts the claim on falsifiable ground.

3. **Scaling is not the cheapest path.** Even if a 10× larger model closes some of the gap, runtime control is strictly cheaper per unit improvement for many operators. The paper's cost-benefit framing (§7) is built to make that comparison quantitative rather than rhetorical.

None of these arguments prove SANA matters; they establish why the systems frame is a legitimate candidate explanation rather than a foregone conclusion. If the experimental ablation finds that all four interventions provide negligible gains on a frontier model, that is itself an interesting finding — and the paper should report it honestly.

## 6. Positioning Relative to Prior Work

Several lines of prior work overlap with SANA's primitives. Each bullet below gives one sentence on what the prior method does and one sentence on how SANA is not a reinvention of it.

- **ReAct** interleaves a free-text reasoning step before each action, giving the model space to plan a tool call in natural language. SANA's micro-reflection is structurally similar but bounded (short fields with length limits and a hard `sufficient_to_call_step_complete` boolean), is paired with a post-tool record that ReAct does not specify, and exists to drive runtime step-advancement decisions rather than to provide a narrative trace.
- **Reflexion** runs an episode, generates a long-form self-evaluation, and retries the whole episode with that critique appended. SANA's micro-reflection is lightweight and per-turn (no retry loop, no episode rollback) and its macro-reflection is sparse and primarily concerned with budget and should-submit decisions, not post-hoc critique. The closer analogy is a budget-aware watchdog, not an episode-level critic.
- **Self-Refine** and related iterative-critique methods add a critique-and-revise loop around the final answer. SANA does not do answer-level critique; its control records are about whether the *current step* is complete and whether the *global trajectory* is still on track. A final-answer Self-Refine step is compatible with SANA but orthogonal to it.
- **Tree-of-Thought** and deliberate-search methods explore multiple intermediate states and pick the best. SANA does not branch; it commits to a single trajectory and controls it with explicit exit conditions and budget. The engineering trade-off is different: ToT spends exploration budget, SANA spends coordination budget.
- **Plan-and-solve prompting** asks the model to produce a decomposition before acting. SANA's plan bullets are a decomposition of the same flavor, but with two additions prior work does not specify: an `estimated_tool_calls` budget per step, and an `exit_condition` that the runtime can evaluate. Those two fields are what make SANA's plans a runtime-control primitive rather than a one-shot prompt pattern.
- **Voyager** and long-horizon agent systems build a growing skill library across episodes. SANA does not propose cross-episode memory; its macro-reflection operates within a single task and uses the summarized-memory substrate rather than a skill repository.
- **Runtime planning / controller architectures** for tool-using LLMs (e.g. LATS, AutoGen's group-chat patterns) also layer control on top of the model. SANA is narrower than most of these — it targets budgeted, single-agent, dataset-centric tabular QA — and trades off generality for a cleaner cost-benefit evaluation.

The intended contribution is therefore not that any one of SANA's primitives is new in isolation. It is the specific selection, the preloaded-sources evaluation regime that lets us attribute residual failures cleanly, and the per-intervention cost-benefit accounting.

## 7. What an Experimental Paper Must Show

This position paper becomes a real experimental paper only if the following are demonstrated:

1. The benchmark and preloaded-sources setup are specified precisely.
2. The planning-scaffolding effect under preloaded is reported with proper uncertainty.
3. The failure taxonomy is operationalized with a coding protocol and examples.
4. SANA is validated through one-at-a-time ablations (Agent 0 + single intervention) plus the cumulative stack, not only proposed.
5. The cost of control is measured alongside the benefit on a per-intervention basis.

### 7.1 Baselines the experiment must include

A single "SANA vs. no-SANA" comparison is not enough. The table must include:

- **Agent 0** (preloaded sources + `SummarizingConversationManager` + basic tools, no SANA interventions) — establishes what a strong base model can do with only retrieval removed.
- **Each SANA intervention individually** on top of Agent 0 — isolates the marginal contribution of each.
- **Agent Full** (all four interventions active) — measures cumulative effect and catches non-additive interactions.
- **A frontier-class model as the default model choice.** The main table is run on a frontier-class base model (e.g. GPT-5.2 at high reasoning). This is deliberate: any SANA benefit that remains at the top of the model ladder is evidence that runtime control is orthogonal to capability, not a crutch for weaker models. If SANA provides no measurable benefit at frontier, that is itself a reportable finding.

### 7.2 Metrics

- solve rate / semantic match
- turn waste percentage
- time to first sufficient answer (`TTFSA`)
- preloaded-source engagement rate — fraction of preloaded URIs the agent ever opens
- token overhead per run
- cost per solved task

The core question is whether each navigation-layer intervention buys back more wasted budget than it consumes — and which, if any, dominate.

## 8. Limitations

This document is intentionally a position paper, not a finished empirical submission.

Its main limitations are:

- preloaded sources is a diagnostic lens, not a deployment pattern; findings do not directly transfer to agents that must search
- the taxonomy is descriptive rather than fully validated
- the intervention stack is proposed, not yet experimentally established
- the benchmark setting is currently narrow and table-centric

These limitations are acceptable for a research agenda memo, but not for a final results paper.

## 9. Conclusion

This paper contributes a methodology — preloaded-sources as a diagnostic lens plus a SANA ablation designed around four independent runtime-control interventions — and a set of falsifiable per-intervention hypotheses. It does not claim which intervention wins, or that any of them necessarily will.

The hypotheses the experimental follow-up should test:

- **H1:** Under preloaded sources with a frontier base model, a measurable fraction of runs fail in ways addressable by *some* runtime-control intervention.
- **H2:** Interface-level interventions (richer dataset-profile APIs) and control-level interventions (plan budgets, micro/macro reflection) have distinct cost-benefit profiles, testable separately via the one-at-a-time ablation.
- **H3:** The cumulative stack (Agent Full) is not strictly additive; interaction effects exist and are either positive (interventions compose) or negative (interventions contend for attention budget).

If all three hypotheses hold, the paper has a contribution. If any fail — for example, if a frontier model obviates all four interventions — that failure is itself a cite-worthy result, and the methodology is what makes it cleanly reportable.
