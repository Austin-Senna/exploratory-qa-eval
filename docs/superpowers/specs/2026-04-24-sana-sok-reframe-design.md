# SANA SoK Reframe — Paper Revision Design

**Date:** 2026-04-24
**Context:** Rewriting `paper.md` to align SANA's experimental structure and vocabulary with Mishra et al. (2026), *SoK: Agentic Retrieval-Augmented Generation (RAG)* (arXiv:2603.07379v1), while preserving the empirical preloaded-sources diagnostic lens.

**Deliverable:** a new file `new_paper.md` alongside the existing `paper.md`. `paper.md` is NOT deleted — it is retained as the legacy reference document. `experimental.md` is updated in place to match the new ablation structure.

---

## 1. Motivation

`paper.md` currently frames SANA as "four new runtime-control interventions" (richer dataset-profile APIs, plan bullets with exit conditions, micro-reflection around tool calls, macro-reflection every *k* turns) layered on a preloaded-sources baseline. Two problems:

1. **Reviewer-fragility of novelty claims.** Each of the four interventions has near-ancestors in the literature (ReAct, Reflexion, Self-Refine, Plan-and-Solve, LATS, Voyager). The paper already tries to defuse this in §6 ("Positioning Relative to Prior Work") by saying SANA is not reinventing any one of them. But that defense is piecemeal — a bullet per prior paper — and leaves the contribution statement vulnerable to "this is just ReAct + plan-and-solve stitched together."

2. **No published framework to position against.** The Mishra SoK (March 2026) now exists and formalizes the agentic-RAG space as a four-dimensional taxonomy (topology, retrieval strategy, reasoning paradigm, memory) plus seven named control-flow patterns and a POMDP cost objective. It is exactly the reference framework SANA's contribution needs.

**The reframe turns the contribution from "we invented four interventions" into "we empirically ablate a specific composition of SoK-catalogued primitives under a preloaded-retrieval diagnostic lens, with per-primitive cost-benefit."** This is defensible, testable, and cites prior work rather than fighting it.

## 2. Scope

**In scope:**

- Write `new_paper.md` as a full rewrite of `paper.md` incorporating the reframe. Keep `paper.md` as legacy.
- Update `experimental.md` in place to reflect the new 6-cell ablation and removed Stage 1.
- Rename intervention vocabulary: `micro_reflection` → `CoT`, `macro_reflection` + `plan_budget` → `short_plan` (bundled), `rich_apis` → `results_apis`, keep `long_plan` (existing `plan_standard`/`plan_ideal`).
- Add SoK as the umbrella citation in §6 (related work), with per-primitive prior work organized under SoK's four dimensions.
- Adopt the SoK cost-constrained objective `U(agent) = solve_rate − λ · mean_tokens_per_run` in §5 and §7.
- Add a failure-taxonomy cross-reference table mapping the existing 5 empirical categories to SoK's 9 failure modes.
- Rewrite the §9 hypotheses (H1, H2, H3) to be expressed in SoK-aligned vocabulary and λ-indexed.

**Out of scope:**

- Code changes. The existing three-axis infrastructure (`search_tool`, `search_results`, `agent_management`) already supports the new ablation. Mapping new primitive names to existing axis values is a cosmetic task for the follow-on implementation plan.
- Adopting the full POMDP formalization. The paper uses only the λ-cost objective from SoK §II; the POMDP tuple is cited but not specialized.
- Re-annotating failure taxonomy rows. The 5 existing empirical categories (with their 2025 counts) stay as the primary taxonomy; the cross-reference is added, not substituted.
- Additional experimental cells beyond the 6 specified here. Fine-grained factorial (12 cells) was considered and rejected in brainstorming.
- Changes to `paper.md` itself. It remains a legacy snapshot.

## 3. Vocabulary remap

| Old name (paper.md / experimental.md) | New name (new_paper.md) | SoK anchor |
|---|---|---|
| `rich_apis` (old Agent 1) | `results_apis` (A4) | §V-B retrieval interfaces (progressive disclosure) |
| plan-bullet decomposition (implicit in old §4.2) | `long_plan` (A2) — unbundled | Table VII Pattern 1 "Plan-Then-Retrieve" |
| `plan_budget` + `macro_reflection` (old Agents 2 & 4) | `short_plan` (A3, requires `long_plan`) | §IV-E cost/latency + §V-F PPAR + §X cost-aware orchestration gap |
| `micro_reflection` (old Agent 3) | `CoT` (A1) | Table VII Pattern 4 "Tool-Augmented Loop" |

The table captures two kinds of change: (a) pure renames (`rich_apis` → `results_apis`, `micro_reflection` → `CoT`) and (b) structural rebundling (`plan_budget` and `macro_reflection` merge into `short_plan`; plan-bullet decomposition surfaces as its own primitive `long_plan`).

**Bundling justification for `short_plan` (plan_budget + macro_reflection):**
- *Mechanical:* a per-step budget without a macro-reflection checkpoint is inert — nothing fires when the budget is hit, so they ship as one primitive.
- *Conceptual:* the SoK's §IV-E (cost/latency tradeoffs) and §V-F (PPAR cycle) treat budget-aware orchestration and periodic reflection as two faces of the same pattern; separating them in the earlier paper was an artifact of the four-intervention framing.

**Dependency constraint:** `short_plan` requires `long_plan`. It is a modifier of the decomposition, not an independent primitive. Ablation table (§5 below) reflects this.

## 4. Revised paper section map

| § | Title | Change type | Notes |
|---|---|---|---|
| 1 | Introduction | Minor rewrite | New thesis sentence: "We instantiate three of SoK's seven control-flow archetypes plus one interface-level primitive, and ablate them in a preloaded-retrieval tabular-QA regime." |
| 2 | Preloaded Sources as a Diagnostic Lens | Minor edit | Add one sentence in §2.1: the preloaded regime fixes the SoK retrieval-strategy dimension at 'none,' isolating control-flow and reasoning-paradigm choices. |
| 3 | Motivating Observations | Add cross-ref table | §3.2 adds the 5→9 failure-mode mapping table (§6 below). No new categories. |
| 4 | SANA Runtime Stack | **Rewritten** | Subsections §4.2–§4.5 become the four primitives `long_plan` / `short_plan` / `CoT` / `results_apis`. Figure 1 restructured as 4 panels. |
| 5 | Why This Is a Systems Problem | Add λ-cost paragraph | One paragraph introducing `U(agent) = solve_rate − λ · mean_tokens_per_run` from SoK §II. POMDP apparatus NOT adopted. |
| 6 | Related Work | **Restructured** | SoK umbrella paragraph + four sub-paragraphs organized under SoK's 4 dimensions. All existing citations preserved. |
| 7 | What an Experimental Paper Must Show | Ablation table rewrite | §7.1 becomes the 6-cell table below (replaces paper.md's Agent 0 / Agents 1–4 / Agent Full structure). §7.2 adds λ-cost metric. |
| 8 | Limitations | One added bullet | "Our instantiation fixes the SoK retrieval-strategy dimension at 'none' (preloaded); findings about control-flow primitives do not directly speak to agents that must perform iterative retrieval." |
| 9 | Conclusion | Hypotheses rewritten | H1, H2, H3 → H1, H2, H3a, H3b (all λ-indexed; see §7 below). |

**`experimental.md` updates in parallel** (in place, not forked):
- §6 "Stage 1: Planning Scaffolding Under Preloaded Sources" removed entirely (subsumed by the new main ablation)
- §7 "Stage 2: SANA Ablation" table replaced with the 6-cell table below
- §9 metric list expanded with the λ-cost objective
- §12 submission-gate checklist updated to reference the 6-cell structure

## 5. Revised §4 primitives (detailed content)

**§4.1 Summarized memory (infrastructure, unchanged).** Held fixed across all cells. Not an ablation toggle.

**§4.2 `long_plan` — Plan-Then-Retrieve.** (SoK Table VII, Pattern 1)
Upfront decomposition into plan bullets, each with `goal` and optional `expected_source`. Without `short_plan`, `estimated_tool_calls` is logged but not runtime-enforced. Corresponds to existing `plan_standard` and `plan_ideal` code paths.

**§4.3 `short_plan` — Plan-Then-Retrieve with cost-aware reflection.** (SoK §IV-E + §V-F)
**Dependency:** requires `long_plan`. Adds two runtime-enforced modifiers:
1. `estimated_tool_calls` becomes a hard budget with forced macro-reflection on exhaustion (`REPLAN` / `ABANDON` / limited override).
2. Macro-reflection fires every *k* turns or on event triggers, producing `{global_status: ON_TRACK | NEEDS_REPLAN | ANSWER_READY, should_submit}`.

The bundling paragraph (mechanical + conceptual reasons from §3 above) opens §4.3.

**§4.4 `CoT` — Tool-Augmented Loop.** (SoK Table VII, Pattern 4)
Renamed from `micro_reflection`. Pre-tool record (`goal`, `why_this_tool`, `what_success_looks_like`, `confidence` — each ≤20 words). Post-tool record (`current_step`, `next_step`, `sufficient_to_call_step_complete`, `remaining_gap_if_not_complete`). One paragraph distinguishes this from narrative ReAct: `sufficient_to_call_step_complete` is evaluated by the runtime for step-advancement, making this a control primitive rather than a narrative reasoning trace.

**§4.5 `results_apis` — Progressive disclosure.** (SoK §V-B)
`peek_file` returns cached column stats, top_2_rows, llm_description. Flagged in prose as "not a control-flow primitive but an interface-level intervention on the observation model" — orthogonal to the plan/CoT axes.

**Figure 1 restructure.** Four panels instead of nested rings:
- (a) `long_plan` producing the step list
- (b) `short_plan` overlaying budget + macro-reflection on the step list
- (c) `CoT` wrapping each tool call
- (d) `results_apis` sitting next to the tool surface

Caption names each panel with its SoK archetype label.

## 6. Revised §3.2 failure-taxonomy cross-reference

Single inline table added to §3.2 (preserves existing 2025 counts):

| Empirical category (our data) | Count | Share | SoK nearest failure mode |
|---|---:|---:|---|
| Duplicate evidence re-querying | 54 | 26.2% | Systemic Risk Amplification (SoK 6) / Infinite Loops (SoK 8) |
| Rediscovery and re-orientation churn | 47 | 22.8% | Systemic Risk Amplification (SoK 6) |
| Answer-ready closure chasing | 31 | 15.0% | Hallucination Despite Retrieval (SoK 2) / Infinite Loops (SoK 8) |
| Constraint-driven workaround thrash | 30 | 14.6% | Tool Misuse and Cascading Errors (SoK 3) |
| On-path budget exhaustion | 25 | 12.1% | Cost Explosion (SoK 9) |
| Unassigned | 19 | 9.2% | — |

Paragraph under table: our categories are a finer-grained specialization. SoK's 9 modes cover the full agentic-RAG failure space (including retrieval drift, prompt injection, memory poisoning — all inert under preloaded sources). Within the subset of SoK modes that can occur post-retrieval, our taxonomy is a substantively sharper decomposition, and the mapping above makes it auditable against SoK's framework without re-annotation.

## 7. Revised §7.1 ablation table

| Agent | Composition | SoK archetype | Δ measured vs |
|---|---|---|---|
| **A0** | preloaded + summarizing mem + naive results | Baseline Grounded Generation | — |
| **A1** | A0 + CoT | Tool-Augmented Loop | A0 |
| **A2** | A0 + long_plan | Plan-Then-Retrieve | A0 |
| **A3** | A2 + short_plan | PTR with cost-aware reflection (compositional gap, SoK §X cost-aware orchestration) | **A2** |
| **A4** | A0 + rich_apis | interface primitive (SoK §V-B) | A0 |
| **Full** | long + short + CoT + rich | composite | A0 (cumulative) |

**Explicit methodological commitment.** A3's delta is reported against A2, not A0, because `short_plan` is definitionally a modifier of `long_plan`. This is stated in §7.1 as a well-motivated exception, not buried.

## 7.2 Revised metrics

All existing metrics preserved: solve rate / semantic match, turn waste %, `TTFSA`, preloaded-source engagement rate, token overhead, cost per solved task.

**Added:** `U(agent) = solve_rate − λ · mean_tokens_per_run` — the SoK cost-constrained objective. Reported at three λ values (low / medium / high = token-indifferent / balanced / token-sensitive). Replaces "cost per solved task" as the headline cost-benefit number and lets §7/§9 make λ-conditional claims like "A3 beats A2 at λ=low but loses at λ=high."

## 8. Revised §6 related work structure

Opens with:

> "We position SANA within the framework of Mishra et al. (2026), which formalizes agentic RAG as a finite-horizon POMDP and catalogs the field across four orthogonal dimensions: architectural topology, retrieval strategy, reasoning paradigm, and memory/context management. SANA specializes one cell of that space: single-agent topology, a degenerate retrieval strategy (preloaded; the source list is authoritative and no retrieval actions are available to the policy), a mixed reasoning paradigm (CoT and reflection each toggleable), and summarization-based memory. Our contribution is an empirical ablation of reasoning-paradigm and control-flow primitives within this cell. Prior work below is organized under the same four dimensions."

Then four sub-paragraphs:

- **§6.1 Architectural topology** — SANA is single-agent. Planner-executor systems (HuggingGPT, OpenAI Agents) noted as alternative realizations of `long_plan`. Multi-agent (AutoGen, CrewAI) out of scope.
- **§6.2 Retrieval strategy** — the preloaded regime fixes this dimension at a degenerate value. IRCoT, Self-RAG, and the legacy `search_ideal` cursor cited as iterative/self-refining strategies factored out.
- **§6.3 Reasoning paradigm** — ReAct and plan-and-solve map to A1. Reflexion and Self-Refine map to A3. Plan-Then-Retrieve (Khot et al. decomposition prompting) maps to A2. Tree-of-Thoughts out of scope (branching vs committed trajectory).
- **§6.4 Memory** — summarization substrate held fixed as infrastructure. Voyager cross-episode skill library and MemoryBank/MemGPT noted as SoK-catalogued alternatives deliberately NOT adopted (keeps the ablation single-episode).

## 9. Revised §9 hypotheses

**H1 (capability-robust failure existence):** "Under preloaded sources with a frontier base model, at least one SoK-catalogued control-flow primitive — A1 (Tool-Augmented Loop) or A2 (Plan-Then-Retrieve) — recovers a non-trivial share of A0's failures. If neither does, runtime-control at the control-flow level is not load-bearing at frontier under preloaded, which is itself a cite-worthy null result."

**H2 (archetype distinctness):** "A1 and A2 exhibit distinct cost-benefit profiles under the λ-parameterized objective. Expected: A1 dominates at low λ (token-indifferent) via local pruning; A2 dominates at higher λ (token-sensitive) via upfront scope reduction. `results_apis` (A4) provides interface-level utility orthogonal to control flow and is expected to add net utility at all λ."

**H3a (short_plan modifier effect):** "Δ(A3 − A2) is non-strict-dominant: adding per-step budget + macro-reflection to a plan improves net utility at high λ (early termination saves tokens) but loses net utility at low λ (reflection overhead is itself a token cost). Directly tests SoK §X cost-aware-orchestration gap."

**H3b (composition interactions):** "Agent Full exhibits non-additive interaction relative to the sum of A1/A2/A3/A4 deltas on A0. Positive interaction supports the composition claim; negative interaction indicates attention-budget contention (SoK §IX cost explosion / context exhaustion)."

## 10. Open questions deferred to implementation

- Whether to write `new_paper.md` from scratch or by forking `paper.md` and editing. Recommendation: fork, because §1/§2/§8 only need minor edits and a fork preserves prose quality.
- Whether `experimental.md` should also be forked (`new_experimental.md`) or updated in place. Recommendation: in place, because its content is operational and kept current with code.
- Exact λ values for the three-point report. Recommendation: defer to the implementation plan — pick based on inspection of baseline token distribution once A0 numbers are in.
- Whether Figure 1 is redrawn now or deferred. Recommendation: defer — placeholder stays in §4 until ablation results land and the figure can be checked against actual observed behavior.

## 11. Success criteria

- `new_paper.md` exists alongside `paper.md`; `paper.md` is unchanged.
- `experimental.md` §6 "Stage 1" section removed; §7 table replaced with the 6-cell ablation; λ-cost metric added to §7.2.
- Every SoK citation in `new_paper.md` resolves to a specific section in arXiv:2603.07379v1.
- Every existing prior-work citation from `paper.md` §6 is preserved in `new_paper.md` §6, reorganized under the four SoK dimensions.
- The 5 empirical failure-category counts in `new_paper.md` §3.2 match those in `paper.md` (26.2% / 22.8% / 15.0% / 14.6% / 12.1% / 9.2%).
- H1, H2, H3a, H3b are all stated in λ-indexed form and each falsifiable against the 6-cell ablation table.

---
