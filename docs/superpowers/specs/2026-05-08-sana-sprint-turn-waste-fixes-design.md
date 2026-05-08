# SANA Sprint Turn-Waste Fixes Design

## Goal

Reduce the main turn-waste failure modes observed in the SANA grouped audit by tightening the existing sprint primitive rather than adding a new mode. The target fixes are:

- Redundant verification and delayed pivot
- Source-contract churn during renewal
- Unnecessary source-switch contracts for related datasets
- Terminal lookup stalls at the end of the tool budget

## Scope

This design updates the current `sprint` tool schema, `SprintSteerHandler`, source-session state, prompt text, and tests. It does not change the baseline evaluator, add a new SANA feature flag, or introduce a separate `final_budget` sprint record.

## Approved Behavior

### Cadence Settled Facts

Cadence sprint records require a new field:

- `settled_facts: list[str]`

The field is required but may be empty. The prompt should instruct the agent that settled facts are durable working memory and should not be rechecked unless contradicted by later evidence. This keeps the record lightweight while directly targeting redundant verification.

### Commitment Related Sources

Commitment contracts accept a new optional field:

- `related_sources: list[str]`

The active source package is `current_source` plus `related_sources`. A tool call against any source in that package counts against the same source budget and does not trigger a source-switch contract. A source outside the package still triggers a new contract.

### Renewal Evidence

First source contracts stay cheap. Source switches also stay cheap unless they are renewing an exhausted package.

When the active source package budget is exhausted, the renewal contract must include:

- `evidence_gained`
- `remaining_gap`

These fields explain what the spent source budget produced and why more calls are justified. Renewal still uses `kind="commitment_contract"`; `commitment_reflection` remains optional.

### Final-Budget Gate

The final-budget rule applies in both cadence and commitment modes. When `tool_calls_left <= 2`, final-budget behavior overrides cadence and commitment bookkeeping.

On the first final-budget trigger, the runtime returns Guide text instructing the agent to submit if ready, otherwise choose exactly one final highest-value lookup. The cancelled tool call does not have to be retried; the agent may choose any one data/source tool next.

After that one final data/source tool call, further data/source tools are blocked. Administrative tools and `submit_answer` are still allowed, with the Guide text instructing the agent to submit using the best available evidence.

## Architecture

Keep the implementation local to the current SANA sprint stack:

- `sana_evaluation/tools/sprint_tool.py`: add schema fields, validation, record formatting, and persisted source-session data.
- `sana_evaluation/plugins/source_session.py`: store `related_sources`, expose package membership checks, and describe package budget.
- `sana_evaluation/plugins/sprint_plugin.py`: treat package sources as one session, require renewal evidence when budget is exhausted, and implement the final-budget state machine.
- `sana_evaluation/prompts/sprint.py`: document `settled_facts`, `related_sources`, renewal evidence, and final-budget behavior.
- `sana_evaluation/plugins/dashboard_plugin.py`: no major behavior change required; it already exposes `tool_calls_left`. It may render related sources if useful.

The final-budget state should live in `SprintSteerHandler` because that handler already owns tool gating. It needs only a small state machine:

- inactive before the threshold
- warned and awaiting one final lookup after the first final-budget Guide
- locked after the final lookup is consumed

The state resets on agent initialization.

## Data Flow

1. Cadence reflection fires and the agent calls `sprint(kind="cadence", settled_facts=[...], ...)`.
2. The sprint tool validates and writes `settled_facts` into `## CURRENT SPRINT`.
3. Commitment mode creates a source package from `current_source` and optional `related_sources`.
4. Source calls within the package increment one shared budget.
5. When budget is exhausted, the next package source call is cancelled and renewal requires `evidence_gained` plus `remaining_gap`.
6. When the global tool budget has two or fewer counted calls left, final-budget gating overrides other sprint gates.
7. The agent gets one final arbitrary data/source lookup, then must submit or use only administrative tools.

## Error Handling

Validation errors should be explicit and actionable:

- Missing cadence `settled_facts` reports that the field is required and may be `[]`.
- Non-list `settled_facts` or `related_sources` is rejected.
- Renewal contracts missing `evidence_gained` or `remaining_gap` are rejected only when the runtime is pending a renewal contract.
- Final-budget lock returns Guide text that names the budget state and directs the agent to `submit_answer`.

## Testing

Add focused tests for:

- Cadence rejects missing `settled_facts`.
- Cadence accepts `settled_facts=[]`.
- Prompt text mentions settled facts and the no-recheck rule.
- Commitment contract stores `related_sources`.
- Related-source tool calls do not trigger a switch and consume shared budget.
- Outside-package source calls still trigger a switch contract.
- Renewal contract requires `evidence_gained` and `remaining_gap`.
- First contract and non-renewal switch do not require renewal evidence.
- Final-budget gate overrides cadence reflection.
- Final-budget gate overrides commitment renewal/switch bookkeeping.
- Final-budget allows one arbitrary data/source tool after the warning.
- Final-budget then blocks data/source tools and allows `submit_answer`.

## Success Criteria

The implementation is successful when the targeted SANA unit tests pass and the sprint behavior is ready for a fresh SANA evaluation run. Behavioral success should be measured separately by regenerating semantic turn-waste and grouped turn-waste reports, then comparing the affected groups against the current audit baseline.
