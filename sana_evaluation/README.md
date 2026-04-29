# sana_evaluation

A SoK-aligned runtime-control framework layered on top of the `strands_evaluation` baseline. SANA composes prompt blocks and runtime plugins via the generic extension hooks exposed on `DataLakeAgent`. It never modifies the baseline.

---

## Feature flags

Three opt-in flags, all default off. Validated by `SanaFlags.validate(agent_management=...)` at startup.

| Flag           | What it does                                                                     | Dependencies                                  |
|----------------|----------------------------------------------------------------------------------|-----------------------------------------------|
| `short_plan`   | k-turn sprint reflection + bundled state-of-task readout + candidate-answer fields | `agent_management ∈ {standard, ideal}`        |
| `CoT`          | Structured pre/post tool-use records                                             | —                                             |
| `results_apis` | `peek_file` returns a `profile` field (column stats, top rows, llm_description)  | —                                             |

Two earlier flags have been folded into `short_plan`:
- The state-of-task readout (formerly `dashboard`) renders inside the reflection Guide reason.
- Candidate-answer + answer-confidence fields (formerly `confidence_advisory`) are part of every reflection JSON.

CLI:

```bash
python -m sana_evaluation.run_sana_eval \
  --search-tool preloaded --search-results ideal --agent-management standard \
  --sana-feature short_plan --sana-feature CoT --sana-feature results_apis \
  --macro-reflection-k 5 \
  --task-set tasks_mini --model gpt-5.4-nano
```

---

## How wiring works

`SanaDataLakeAgent` (in `sana_bundle.py`) extends `DataLakeAgent` and overrides five generic extension hooks the baseline exposes:

| Hook                    | What SANA does with it                                                                 |
|-------------------------|----------------------------------------------------------------------------------------|
| `_pre_build_setup`      | No-op (currently). Reserved for runtime toggles.                                       |
| `_extra_prompt_text`    | Appends `cot_block` / `short_plan_block` per active flag                               |
| `_extra_plugins`        | Adds `CoTPostRecordPlugin`, `ShortPlanSteerHandler`, `StateOfTaskDashboardPlugin`      |
| `_conversation_manager` | Returns a `SummarizingConversationManager` with the SANA-tuned summarization prompt    |
| `_decorate_tools`       | Swaps baseline `peek_file` with SANA's profile-aware wrapper when `results_apis=on`    |

`SanaBatchRunner` (in `sana_runner.py`) is just `BatchRunner` with `_AGENT_CLASS = SanaDataLakeAgent`.

`SanaRunConfig` (in `sana_config.py`) is `RunConfig` with an extra `sana_flags: SanaFlags` field. SanaDataLakeAgent reads `run_config.sana_flags`; plain `RunConfig` degrades to all flags off.

---

## Per-primitive implementation

### `CoT` — structured tool-use records

**Prompt** — `prompts/cot.py:cot_block(search_tool)`

Asks the agent to emit a 4-field pre-tool record (`goal`, `why_this_tool`, `what_success_looks_like`, `confidence: low|medium|high`) before each tool call, and a 4-field post-tool record (`current_step`, `next_step`, `sufficient_to_call_step_complete: bool`, `remaining_gap_if_not_complete`) after each tool result.

**Plugin** — `plugins/cot_post_record_plugin.py:CoTPostRecordPlugin`

System-prompt-only directives are unreliable for the post-record (smaller models tend to skip it). The plugin hooks `AfterToolCallEvent` and **mutates `event.result.content`** to append a short reminder of the post-record schema to each non-administrative tool result. The model sees the reminder as part of the tool response — a much more attention-grabbing channel than a static system rule.

Excluded tools (no reminder appended): `plan`, `plan_ideal`, `skills`, `summarize_context`, `submit_answer`.

The pre-record stays in the system prompt only — its compliance is naturally high since the model has to write something before calling a tool.

---

### `short_plan` — k-turn sprint reflection (with state-of-task readout + candidate answer)

**Prompt** — `prompts/short_plan.py:short_plan_block(search_tool)`

Tells the agent that every k non-administrative tool calls, the next tool call is cancelled and a Guide-style synthetic result will arrive containing:
1. A state-of-task readout (turn count, plan progress, candidate answer, confidence trend, evidence consumed).
2. An instruction to emit a single JSON object with the new richer schema:
   ```json
   {
     "global_status": "ON_TRACK" | "NEEDS_REPLAN" | "ANSWER_READY",
     "should_submit": true | false,
     "potential_answer": "<best current candidate, or null>",
     "answer_confidence": "low" | "medium" | "high",
     "short_forward_plan": [
       "turns 1-2: peek X, check schema",
       "turns 3-5: query Y, validate vs expected"
     ]
   }
   ```

`short_forward_plan` is turn-budgeted free-text strings — each entry is prefixed with a turn range and covers actions for that range. The total plan covers up to k turns (one sprint ahead). `potential_answer` and `answer_confidence` capture the agent's current best answer + how confident it is in that answer (distinct from the per-tool-call `confidence` in CoT records).

**Plugin** — `plugins/short_plan_plugin.py:ShortPlanSteerHandler`

Subclass of Strands' `SteeringHandler`. Counts non-administrative tool calls. On the k-th call, `steer_before_tool` returns `Guide(reason=...)` which:
- cancels the tool the model just tried to call,
- feeds the reason text back as a synthetic tool result,
- does **not** consume an extra agent turn — the cancelled tool's slot becomes the reflection slot.

After the model produces its JSON-only response, `on_after_model` parses the JSON and stores it in `self.last_reflection`. Internal state resets (`_tool_calls_since_reflection = 0`) so the next sprint begins.

Excluded tools (don't advance the sprint counter, don't get cancelled): `plan`, `plan_ideal`, `skills`, `summarize_context`, `submit_answer`.

**Peer plugin** — `plugins/dashboard_plugin.py:StateOfTaskDashboardPlugin`

Always wired alongside `ShortPlanSteerHandler` when `short_plan=on`. The plugin observes runtime state but does not inject any messages on its own:
- `on_after_tool` increments a tool-call ledger (excludes admin tools).
- `on_after_model` regex-parses the assistant CoT text for `confidence: low|medium|high` (3-deep deque) and `sufficient_to_call_step_complete: true|false` (bumps complete/incomplete counters).
- `render_block()` formats those signals into:
  ```
  [State of Task — Turn 5 / 30]
  long_plan: 2 step(s) marked complete, 1 step(s) flagged incomplete
  short_plan: step 1/3 (turns 1-2: peek customer_orders) | status: ON_TRACK | reflections: 1
  candidate_answer: 1.2M | answer_confidence: medium
  confidence (last 3): low, low, medium
  evidence: 5 tool call(s) consumed
  ```

The `candidate_answer` line appears once a reflection has produced `potential_answer` + `answer_confidence` (i.e. from the second sprint onward).

`ShortPlanSteerHandler.steer_before_tool` calls `self.dashboard_plugin.render_block()` when triggering the k-th-call Guide and prepends it to the JSON-emit instruction. Read-then-act layout.

---

### `results_apis` — `peek_file` profile enrichment

**No system prompt block.** The information is documented in the wrapped `peek_file`'s docstring — the baseline tool's docstring does not mention profiles, the SANA wrapper's does.

**Tool wrapper** — `tools/peek_file_with_profile.py:peek_file`

A `@tool`-decorated function whose body delegates to `_baseline_peek_file._tool_func(...)` and then attaches a `profile` field to the result when one can be loaded for the URI. The wrapper docstring tells the agent that `peek_file` returns column statistics, top rows, and an LLM-generated description.

`SanaDataLakeAgent._decorate_tools` swaps the baseline `peek_file` for the SANA wrapper when `results_apis=on` (identified by `tool_name == "peek_file"`).

**Profile loader** — `helper/peek_profile.py:load_dataset_profile(s3_uri)`

Two sources, in priority order:
1. Precomputed profile rows from `data/datagov_tables_profiles.jsonl` — keyed by S3 URI or by `(slug, filename)` stems.
2. Legacy fallback to the ideal-search wrapper's schema/description/snippet caches when no precomputed row is available.

Returns `None` softly if no profile can be assembled; `peek_file` then omits the field.

---

## Conversation manager — `helper/conversation.py`

When any SANA flag is active, `SanaDataLakeAgent` returns a `SummarizingConversationManager` wired with `SANA_SUMMARIZATION_PROMPT`.

The prompt tells the summarization LLM to:
- **Preserve verbatim**: the original user question, the plan emitted by `plan_ideal`/`plan_agent`, and the most recent macro-reflection JSON.
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
    datagov_tables_profiles.jsonl       Precomputed profiles for results_apis
  helper/
    conversation.py                     SANA-tuned SummarizingConversationManager
    peek_profile.py                     Profile loader (precomputed + legacy fallback)
  plugins/
    short_plan_plugin.py                ShortPlanSteerHandler (SteeringHandler.Guide)
    dashboard_plugin.py                 StateOfTaskDashboardPlugin (observe + render_block)
    cot_post_record_plugin.py           CoTPostRecordPlugin (AfterToolCallEvent.result mutation)
  prompts/
    short_plan.py                       short_plan_block (reflection JSON + state-of-task readout)
    cot.py                              cot_block (pre/post-tool record schema)
  tools/
    peek_file_with_profile.py           SANA's @tool peek_file wrapping baseline + profile attach
  tests/
    test_flags.py
    test_prompts.py
    test_plugins.py
    test_conversation.py
    test_decorate_tools.py
    test_peek_profile.py
    test_results_apis_docstring.py
```

---

## Design conventions

- **No "SANA" vocabulary in agent-facing prompts.** Empirically confusing. Tests assert this.
- **Prompt blocks live in the cached system prefix.** Per-task content (plan, dashboard) goes through tool results / steering Guide reasons / `BeforeModelCallEvent`-injected user messages — never the system prompt.
- **Compliance via channel choice.** Behavior the model must follow on every turn goes in the system prompt (cached). High-priority interrupts go through `AfterToolCallEvent.result` mutation (CoT post-records) or `SteeringHandler.Guide` (k-turn reflection). Both are higher-attention channels than system rules.
- **Baseline isolation.** `strands_evaluation/` knows nothing about SANA. The SANA module imports the baseline. The five `_*` extension hooks on `DataLakeAgent` are generic — they don't carry any SANA-specific names or data.
