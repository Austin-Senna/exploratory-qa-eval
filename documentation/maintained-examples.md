# Maintained LakeQA And Kramabench Examples

This guide covers the repository-maintained LakeQA and Kramabench artifacts. It
does not cover converting a new benchmark into SANA artifacts.

## Artifact Inventory

Use the inventory command before running or analyzing a benchmark:

```bash
python -m sana_evaluation.artifacts --benchmark lakeqa --check
python -m sana_evaluation.artifacts --benchmark kramabench --check
```

`--check` exits with status `2` if a required runtime-profile, task, prompt, or
artifact root is missing.

## LakeQA Tasks Mini

Required roots:

- `benchmarks/lakeqa/tasks-mini/tasks/`
- `benchmarks/lakeqa/tasks-mini/runtime-profiles/`
- `benchmarks/lakeqa/tasks-mini/artifacts/descriptions.jsonl`
- `benchmarks/lakeqa/tasks-mini/artifacts/snippets.jsonl`
- `benchmarks/lakeqa/tasks-mini/artifacts/table_schemas_full.jsonl`
- `prompts/`

Optional/generated roots:

- `benchmarks/lakeqa/tasks-mini/artifacts/table_profiles.jsonl`
- `lance_data/`
- `results/`
- `results_semantic/`
- `analysis_results_mode_semantic/`

## Kramabench Tasks Mini

Required roots:

- `benchmarks/kramabench/tasks-mini/tasks/`
- `benchmarks/kramabench/tasks-mini/runtime-profiles/`
- `benchmarks/kramabench/tasks-mini/artifacts/descriptions.jsonl`
- `benchmarks/kramabench/tasks-mini/artifacts/snippets.jsonl`
- `benchmarks/kramabench/tasks-mini/artifacts/table_schemas_full.jsonl`
- `prompts/`

Optional/generated roots:

- `benchmarks/kramabench/tasks-mini/artifacts/table_profiles.jsonl`
- `lance_data/`
- `results-kramabench/`
- `results-kramabench_semantic/`
- `analysis_results_mode_kramabench_semantic/`

## Runtime Commands

The supported runner entrypoint is `sana_evaluation.setup_run`. It wraps
`sana_evaluation.run_mode_eval`, applies benchmark defaults, and prints the
resolved command before execution.

LakeQA smoke:

```bash
python -m sana_evaluation.setup_run smoke \
  --benchmark lakeqa \
  --search ideal \
  --results ideal \
  --plans ideal \
  --compute ideal \
  --k 5 \
  --db lance_data \
  --model openai/gpt-5.4-nano
```

Kramabench smoke:

```bash
python -m sana_evaluation.setup_run smoke \
  --benchmark kramabench \
  --search ideal \
  --results ideal \
  --plans ideal \
  --compute ideal \
  --k 5 \
  --db lance_data \
  --model openai/gpt-5.4-nano
```

Use `full --continue` for resumable full runs over the maintained task set.

## Analysis Commands

LakeQA:

```bash
python -m sana_analysis.run_mode_analysis_semantic \
  --results-dir results_semantic/modes \
  --base-results-dir results/modes \
  --traces-dir results/traces/modes \
  --tasks-dir benchmarks/lakeqa/tasks-mini/tasks \
  --output-dir analysis_results_mode_semantic
```

Kramabench:

```bash
python -m sana_analysis.run_mode_analysis_semantic \
  --results-dir results-kramabench_semantic/modes \
  --base-results-dir results-kramabench/modes \
  --traces-dir results-kramabench/traces/modes \
  --tasks-dir benchmarks/kramabench/tasks-mini/tasks \
  --output-dir analysis_results_mode_kramabench_semantic
```

## Terminology

Use **runtime profile** for the ground-truth SANA artifact consumed by idealized
planning, search, and execution. Older code and flags may still say `plans`
during the migration, but the canonical artifact folder is
`runtime-profiles/`.
