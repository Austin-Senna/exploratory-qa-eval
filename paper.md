# Search Agent Navigation Assembly

Status: position paper / research agenda draft

## Abstract

Search is an obvious bottleneck in tool-using agents, but it is not the only one. This paper argues for a diagnostic lens in which retrieval quality is deliberately idealized so that a different systems problem becomes visible: navigation after the right evidence is already available. In this setting, agents still waste budget on schema inspection, repeated evidence gathering, source rediscovery, and late-stage overvalidation. We argue that these failures are better understood as execution-control failures than as pure search failures.

We propose Search Agent Navigation Assembly (SANA), a runtime control stack for budgeted search agents. The stack assumes summarized memory as default infrastructure, then adds plan bullets with explicit exit conditions and estimated tool budgets, cheap local control checks around each tool call, sparse global reflection every `k` turns, and richer dataset-profile APIs that replace low-value inspection. The goal of this paper is not to claim that SANA has already been fully validated. Instead, it positions navigation as the next bottleneck once retrieval quality improves and lays out a concrete experimental agenda for testing that claim.

## 1. Introduction

When search agents fail, it is tempting to blame retrieval first. Often that is correct. An agent may not find the right dataset, may retrieve the wrong page, or may spend too many turns on broad discovery. But a different failure mode appears when retrieval is made easier: even after the agent has access to the right datasets, it can still fail to execute the task efficiently.

This paper focuses on that residual problem. We ask:

> If the agent is already given the datasets it needs at each search step, can it then reason over tabular data in the right way under budget?

The motivating answer is: not reliably. Even under idealized retrieval, agents can still thrash. They inspect schema instead of extracting. They re-query evidence they already have. They reopen source discovery after the path is already known. They keep validating after the answer is effectively available. These are not primarily retrieval failures. They are navigation failures.

The central claim of this position paper is therefore modest but important: once retrieval is improved, a major remaining bottleneck is runtime control over progress, memory, stopping, and tool use.

## 2. Ideal Retrieval as a Diagnostic Lens

The point of ideal retrieval is not to pretend that search is solved in deployment. The point is to isolate the residual problem. If we do not control retrieval, then every later failure can be explained away as “the agent never found the right source.” That makes it hard to learn whether the agent is also failing after it has already reached the correct evidence.

In this framing, “ideal retrieval” means a setup in which the agent is substantially helped at the search stage, for example by being given the right dataset family or gold-supporting sources at each retrieval step. The exact operationalization must be stated precisely in any empirical paper. Here, it serves as a conceptual lens:

- if failure persists after access to the right datasets, then retrieval is not the full story
- if planning remains strong but execution is weak, then the next systems bottleneck is navigation

This is why we continue to call the setting “search agent” design. The search agent is still the object of study, but we temporarily hold retrieval quality fixed in order to expose downstream control failures more clearly.

## 3. Motivating Observations

This paper is motivated by three preliminary observations rather than by a complete validated experiment.

### 3.1 Planning may already be relatively strong

In our current internal work, agents with only tool descriptions and no special skill scaffolding can still produce plausible decompositions. More importantly, the gap between default plans and benchmark-authored ideal plans appears smaller than expected in the ideal-retrieval regime.

This does **not** justify a final empirical claim yet. It is only a motivating observation. A future experimental paper must report task counts, seeds, variance, and confidence intervals before saying that planning is or is not the bottleneck. But the observation is strong enough to motivate a shift in attention: if planning quality is already decent, then what remains broken?

### 3.2 Long traces destabilize agents

Agents often degrade after enough turns. They lose track of what has already been established, reopen stale branches, and start making locally plausible but globally unhelpful moves. This is why the default runtime in our proposal uses summarized memory rather than a pure sliding context. The point is not only token compression. The point is to preserve structured progress state.

### 3.3 The dominant failure patterns are execution failures

In grouped runtime-failure analysis, the recurring patterns are not only “could not find the dataset.” They are also:

- repeated evidence re-querying
- rediscovery and re-orientation churn
- answer-ready closure chasing
- schema and workaround thrash

These categories still need a more rigorous annotation protocol before they can function as a formal measurement artifact in a submission-ready paper. For this position paper, they serve as descriptive motivation for the architecture.

## 4. SANA: The Proposed Runtime Stack

Search Agent Navigation Assembly is a runtime control stack layered on top of a search agent with summarized memory.

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

The problem is not simply that the model needs to “think harder.” The problem is that the runtime gives the model too little structured support for:

- knowing when a step is complete
- tracking remaining budget
- preserving long-horizon state
- deciding when to stop
- choosing cheap tools over expensive exploratory rituals

Under this view, many wasted turns are interface failures and control failures, not just reasoning failures.

## 6. Positioning Relative to Prior Work

A final paper must situate SANA against existing agent-control work rather than presenting these ideas as if they appeared in a vacuum.

Relevant lines of work include:

- ReAct-style interleaving of reasoning and acting
- Reflexion-style self-evaluation and retry loops
- Self-Refine and related iterative critique methods
- Tree-of-Thought and deliberate search over intermediate states
- plan-and-solve prompting and explicit decomposition
- long-horizon agent systems such as Voyager
- runtime planning or controller architectures for tool-using LLMs

The claim here is not that reflection, planning, or memory summaries are new in isolation. The intended contribution is a specific systems assembly for budgeted, dataset-centric agents under idealized retrieval, together with an evaluation agenda that focuses on cost versus saved turns.

## 7. What an Experimental Paper Must Show

This position paper becomes a real experimental paper only if the following are demonstrated:

1. The benchmark and ideal-retrieval setup are specified precisely.
2. The planning-gap claim is reported with proper uncertainty.
3. The failure taxonomy is operationalized with a coding protocol and examples.
4. SANA is validated through ablations, not only proposed.
5. The cost of control is measured alongside the benefit.

The most important evaluation dimensions are:

- solve rate / semantic match
- turn waste percentage
- time to first sufficient answer
- turns-to-dataset-access (`TDA@50`, `TDA@100`)
- token overhead
- cost per solved task

The core question is whether the navigation layer buys back more wasted budget than it consumes.

## 8. Limitations

This document is intentionally a position paper, not a finished empirical submission.

Its main limitations are:

- the planning observation is preliminary
- the taxonomy is descriptive rather than fully validated
- the intervention stack is proposed, not yet experimentally established
- the benchmark setting is currently narrow and table-centric

These limitations are acceptable for a research agenda memo, but not for a final results paper.

## 9. Conclusion

Once retrieval is improved, the remaining bottleneck in search agents may be navigation rather than search itself. Agents can still waste turns after they have reached the right datasets because they lack strong runtime support for progress tracking, stopping, budget control, and state preservation.

Search Agent Navigation Assembly is a proposal for that missing layer. Its value is not yet proven. But it gives a concrete systems hypothesis:

> Better navigation over already-accessed evidence may matter as much as, or more than, further improvements in retrieval quality for budgeted tabular QA agents.

That hypothesis is what the experimental paper should test.
