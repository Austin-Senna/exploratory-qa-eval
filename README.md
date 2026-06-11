# SANA

SANA is a diagnostic ablation framework for exploratory QA over data lakes. It
turns benchmark tasks into runtime profiles containing gold source sequences,
sanitized subquestions, and execution records, then uses those profiles to
ablate search, planning, and data-analysis tools under a fixed agent runtime.

## Repository Layout

- `sana_evaluation/`: runtime package for runners, preflight checks, agent
  configuration, tools, instrumentation, and model adapters.
- `sana_analysis/`: canonical import package for analysis and paper-result
  generation scripts.
- `benchmarks/{benchmark}/{task-set}/tasks/`: benchmark task JSON files.
- `benchmarks/{benchmark}/{task-set}/runtime-profiles/`: SANA runtime profiles
  used by ideal planning, search, and execution.
- `benchmarks/{benchmark}/{task-set}/artifacts/`: benchmark-local JSONL
  dependencies such as descriptions, snippets, schemas, and file profiles.

Maintained examples:

| Benchmark | Task set | Tasks | Runtime profiles | Artifacts |
| --- | --- | --- | --- | --- |
| LakeQA | `tasks-mini` | `benchmarks/lakeqa/tasks-mini/tasks/` | `benchmarks/lakeqa/tasks-mini/runtime-profiles/` | `benchmarks/lakeqa/tasks-mini/artifacts/` |
| Kramabench | `tasks-mini` | `benchmarks/kramabench/tasks-mini/tasks/` | `benchmarks/kramabench/tasks-mini/runtime-profiles/` | `benchmarks/kramabench/tasks-mini/artifacts/` |

## Inspect Maintained Artifacts

```bash
python -m sana_evaluation.artifacts --benchmark lakeqa --check
python -m sana_evaluation.artifacts --benchmark kramabench --check
```

The report prints required roots, optional/generated roots, and copy-paste run
and analysis commands.

## Run Smoke Evaluations

LakeQA:

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

Kramabench:

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

## Analyze Existing Results

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

See `documentation/maintained-examples.md` for more detail.
