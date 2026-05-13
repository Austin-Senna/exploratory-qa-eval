# sana_evaluation

A SoK-aligned runtime-control framework layered on top of the `strands_evaluation` baseline. SANA composes prompt blocks and runtime plugins via the generic extension hooks exposed on `DataLakeAgent`. It never modifies the baseline.

---

## Feature flags

Four opt-in flags, all default off. Validated by `SanaFlags.validate(agent_management=...)` at startup.

| Flag      | What it does                                                                    | Dependencies                           |
|-----------|---------------------------------------------------------------------------------|----------------------------------------|
| `sprint`  | k-turn sprint reflection or source commitment control, submitted with a tool    | `agent_management ∈ {standard, ideal}` |
| `cot`     | Structured pre/post tool-use records                                            | incompatible with `delegation`         |
| `results` | `peek_file` returns a `profile` field (column stats, top rows, llm_description) | —                                      |
| `delegation` | Planner-only parent agent with bounded search/inspect subagents             | `agent_management ∈ {standard, ideal}`; incompatible with `sprint`/`cot` |

Two earlier flags have been folded into `sprint`:
- The state-of-task readout (formerly `dashboard`) renders inside the reflection Guide reason.
- Candidate-answer + answer-confidence fields (formerly `confidence_advisory`) are part of every sprint record.

CLI:

```bash
python -m sana_evaluation.run_sana_eval \
  --search_tool preloaded --search_results ideal --plans standard \
  --sana-feature sprint --sana-feature cot --sana-feature results \
  --sprint-mode commitment --commitment-budget-calls 3 \
  --task-set tasks_mini --model gpt-5.4-nano
```

---

## How wiring works

`SanaDataLakeAgent` (in `sana_bundle.py`) extends `DataLakeAgent` and overrides five generic extension hooks the baseline exposes:

| Hook                    | What SANA does with it                                                                 |
|-------------------------|----------------------------------------------------------------------------------------|
| `_pre_build_setup`      | No-op (currently). Reserved for runtime toggles.                                       |
| `_system_prompt_override` | Replaces the parent prompt with a lean planner prompt when `delegation=on`          |
| `_extra_prompt_text`    | Appends `cot_block` / `sprint_block` per active flag                                   |
| `_extra_plugins`        | Adds `CoTPostRecordPlugin`, `SprintSteerHandler`, `StateOfTaskDashboardPlugin`         |
| `_conversation_manager` | Returns a `SummarizingConversationManager` with the SANA-tuned summarization prompt    |
| `_decorate_tools`       | Swaps baseline `peek_file` when `results=on`, adds `sprint`, or prunes to delegation tools |

`SanaBatchRunner` (in `sana_runner.py`) is just `BatchRunner` with `_AGENT_CLASS = SanaDataLakeAgent`.

`SanaRunConfig` (in `sana_config.py`) is `RunConfig` with an extra `sana_flags: SanaFlags` field. SanaDataLakeAgent reads `run_config.sana_flags`; plain `RunConfig` degrades to all flags off.

---

## Per-primitive implementation

### `cot` — structured tool-use records

**Prompt** — `prompts/cot.py:cot_block(search_tool)`

Asks the agent to emit a 4-field pre-tool record (`goal`, `why_this_tool`, `what_success_looks_like`, `confidence: low|medium|high`) before each tool call, and a 4-field post-tool record (`current_step`, `next_step`, `sufficient_to_call_step_complete: bool`, `remaining_gap_if_not_complete`) after each tool result.

**Plugin** — `plugins/cot_post_record_plugin.py:CoTPostRecordPlugin`

System-prompt-only directives are unreliable for the post-record (smaller models tend to skip it). The plugin hooks `AfterToolCallEvent` and **mutates `event.result.content`** to append a short reminder of the post-record schema to each non-administrative tool result. The model sees the reminder as part of the tool response — a much more attention-grabbing channel than a static system rule.

Excluded tools (no reminder appended): `plan`, `plan_ideal`, `skills`, `submit_answer`.

The pre-record stays in the system prompt only — its compliance is naturally high since the model has to write something before calling a tool.

---

### `sprint` — tool-submitted sprint reflection and source commitments

**Prompt** — `prompts/sprint.py:sprint_block(search_tool)`

Tells the agent that every k non-administrative tool calls, or at source commitment boundaries, the next tool call is cancelled and a Guide-style synthetic result will arrive containing:
1. A state-of-task readout (current plan step, remaining tool budget, concise source-session state, and candidate answer when available).
2. An instruction to call the `sprint` tool. The model must call that tool before any data tool or `submit_answer`.

The sprint tool records the current sprint and upserts a persistent `## CURRENT SPRINT` section into the agent's system prompt after `## CURRENT PLAN`. This keeps the reflection inside the agent's durable working context without creating a text-only assistant turn.

Cadence sprint fields: `kind="cadence"`, `global_status`, `should_submit`, `potential_answer`, `answer_confidence`, `settled_facts`, `short_forward_plan`. `settled_facts` is required but may be `[]`; the agent should treat listed facts as already established unless later findings contradict them.

Commitment fields:
- `kind="commitment_contract"`: `current_source`, `commitment_goal`, `max_source_calls`, `plan_step` (`related_sources` and `success_condition` optional). `current_source + related_sources` form one source package with a shared budget.
- Renewal contracts after budget exhaustion also require `evidence_gained` and `remaining_gap`.
- `kind="commitment_reflection"`: `current_source`, `calls_used`, `commitment_goal`, `evidence_gained`, `remaining_gap`, `next_action`, `revised_budget`.

**Plugin** — `plugins/sprint_plugin.py:SprintSteerHandler`

Subclass of Strands' `SteeringHandler`. Counts non-administrative tool calls or source-session calls. When a sprint is due, `steer_before_tool` returns `Guide(reason=...)` which:
- cancels the tool the model just tried to call,
- feeds the reason text back as a synthetic tool result,
- blocks all tools except `sprint` until the sprint tool succeeds.

In commitment mode, a pending source contract blocks source/data tools but does not block `submit_answer`; if the answer is already ready, the final answer can be submitted without spending another bookkeeping turn. When the global counted-tool budget reaches the final two calls, sprint bookkeeping is bypassed: the agent gets a Guide to submit if ready or spend exactly one final lookup, then further data/source tools are blocked and only `submit_answer` plus administrative tools can proceed.

After the model calls `sprint`, the tool updates shared sprint state, refreshes `## CURRENT SPRINT`, and clears the pending gate so normal tool use can resume.

Excluded tools (don't advance the sprint counter): `plan`, `plan_ideal`, `skills`, `submit_answer`, `sprint`.

**Peer plugin** — `plugins/dashboard_plugin.py:StateOfTaskDashboardPlugin`

Always wired alongside `SprintSteerHandler` when `sprint=on`. The plugin observes runtime state but does not inject any messages on its own:
- `on_after_tool` increments a tool-call ledger (excludes admin tools) and captures the latest numbered plan from `plan` / `plan_ideal`.
- `render_block()` formats those signals into:
  ```
  [State of Task]
  current_plan_step: 2) Query qualifying counties.
  tool_calls_left: 25/30
  sprint_status: ON_TRACK | next: turns 1-2: query county totals
  candidate_answer: 1.2M | answer_confidence: medium
  source_session: bridge-conditions-nys-department-of-transportation | source_calls: 2/3
  source_goal: Find NY counties with at least 65 poor bridges.
  ```

The `candidate_answer` line appears once a reflection has produced `potential_answer` + `answer_confidence` (i.e. from the second sprint onward).

`SprintSteerHandler.steer_before_tool` calls `self.dashboard_plugin.render_block()` when triggering a Guide and prepends it to the sprint-tool instruction. Read-then-act layout.

---

### `results` — `peek_file` profile enrichment

**No system prompt block.** The information is documented in the shared baseline `peek_file` docstring. Baseline `strands_evaluation` peek tools are profile-aware by default.

**Tool wrapper** — `tools/peek_file_with_profile.py:peek_file`

Compatibility `@tool`-decorated functions whose bodies delegate to the shared baseline peek tools. They remain for older imports, but SANA no longer swaps them into the active tool list.

`SanaDataLakeAgent._decorate_tools` keeps the baseline `peek_file` and `peek_multiple` because they already attach raw profile rows when available.

**Profile loader** — `strands_evaluation.helper.peek_profile:load_dataset_profile(s3_uri)`

Single source:
1. Precomputed raw profile rows from repo-root `datagov_tables_profiles.jsonl` — keyed by S3 URI or by `(slug, filename)` stems.

Returns `None` softly if no profile row is available; `peek_file` then omits the field. Search-result ideal enrichment owns schema/snippet fallbacks separately.

---

## Conversation manager — `helper/conversation.py`

When any SANA flag is active, `SanaDataLakeAgent` returns a `SummarizingConversationManager` wired with `SANA_SUMMARIZATION_PROMPT`.

The prompt tells the summarization LLM to:
- **Preserve verbatim**: the original user question, the plan emitted by `plan_ideal`/`plan_agent`, and the most recent `## CURRENT SPRINT` section.
- **Render plan progress as a checklist**: walk through the preserved plan and mark each bullet with `✓` (done — bullet appeared before the most recent `current_step` line), `▸` (in progress — the `current_step` value), or `☐` (pending — bullets after `current_step`). Cross-checks `sufficient_to_call_step_complete: true` lines for explicit completions.
- Summarize technical findings, failed approaches, and best current answer candidate alongside.

This means after a summarization pass, the agent still sees its plan as a checklist of where it has been and where it is going — even when raw turns have been compacted away.

---

## Module layout

```
sana_evaluation/
  __init__.py
  flags.py                              SanaFlags dataclass + _VALID_FEATURE_NAMES + validation
  sana_bundle.py                        SanaDataLakeAgent — composes hooks
  sana_runner.py                        SanaBatchRunner = BatchRunner with _AGENT_CLASS swap
  sana_config.py                        SanaRunConfig = RunConfig + sana_flags field
  run_sana_eval.py                      CLI entrypoint
  data/
    datagov_tables_profiles.jsonl       Precomputed profiles for results
  helper/
    conversation.py                     SANA-tuned SummarizingConversationManager
    peek_profile.py                     Profile loader (precomputed + legacy fallback)
  plugins/
    sprint_plugin.py                    SprintSteerHandler (SteeringHandler.Guide)
    dashboard_plugin.py                 StateOfTaskDashboardPlugin (observe + render_block)
    cot_post_record_plugin.py           CoTPostRecordPlugin (AfterToolCallEvent.result mutation)
  prompts/
    sprint.py                           sprint_block (sprint tool + state-of-task readout)
    cot.py                              cot_block (pre/post-tool record schema)
  tools/
    peek_file_with_profile.py           SANA's @tool peek_file wrapping baseline + profile attach
    sprint_tool.py                      SANA's @tool sprint persistent reflection
  tests/
    test_flags.py
    test_prompts.py
    test_plugins.py
    test_conversation.py
    test_decorate_tools.py
    test_peek_profile.py
    test_results_docstring.py
```

---

## Design conventions

- **No "SANA" vocabulary in agent-facing prompts.** Empirically confusing. Tests assert this.
- **Prompt blocks live in the cached system prefix.** Agent-authored persistent state is limited to `## CURRENT PLAN` and `## CURRENT SPRINT`, both written by tools.
- **Compliance via channel choice.** Behavior the model must follow on every turn goes in the system prompt (cached). High-priority interrupts go through `AfterToolCallEvent.result` mutation (CoT post-records) or `SteeringHandler.Guide` (sprint gating). Both are higher-attention channels than system rules.
- **Baseline isolation.** `strands_evaluation/` knows nothing about SANA. The SANA module imports the baseline. The five `_*` extension hooks on `DataLakeAgent` are generic — they don't carry any SANA-specific names or data.
