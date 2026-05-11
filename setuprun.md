# Setup Run

Use the friendly wrapper:

```bash
python -m strands_evaluation.setup_run smoke ...
python -m strands_evaluation.setup_run full ...
```

When you ask me to run an eval in chat, use a request like:

```text
--search ideal --results ideal --plans ideal --k 5 --model gpt5.2 --reasoning-effort xhigh
```

I will always ask which Lance DB to load before running anything. Valid repo-local choices right now are:

- `lance_data`
- any custom path you provide

Use `--skills on` only when you want to attach the Strands AgentSkills planning/discovery plugin. It defaults to off; `--plans` controls the `plan` versus `plan_ideal` tool axis.

## Smoke Run

Smoke runs are lightweight checks:

- task set: `tasks_core_quality`
- default scope: `tasks_core_quality/k-5-d-4`
- task count: first 2 task files in that directory
- logs: `test_logs`
- results: `test_results`

Example:

```bash
python -m strands_evaluation.setup_run smoke \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data
```

Override the smoke directory:

```bash
python -m strands_evaluation.setup_run smoke \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data \
  --task-dir tasks_core_quality/k-5-d-3
```

## Full Run

Full runs execute the whole `tasks_core_quality` split:

- scope: `--all-tasks --task-set tasks_core_quality`
- logs: `logs`
- results: `results`

Example:

```bash
python -m strands_evaluation.setup_run full \
  --search ideal \
  --results ideal \
  --plans ideal \
  --k 5 \
  --model gpt5.2 \
  --reasoning-effort xhigh \
  --db lance_data
```

## What The Wrapper Does

The wrapper translates the friendly flags onto:

```bash
python -m strands_evaluation.run_mode_eval ...
```

Before execution it prints:

- the resolved command
- the selected Lance DB
- the task scope
- the log root
- the results root
