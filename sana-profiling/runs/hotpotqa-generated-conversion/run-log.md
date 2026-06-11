# HotpotQA Generated Conversion Run

## Commands

```bash
python sana-profiling/skills/benchmark-lakeqa-conversion-auditor/scripts/sample_benchmark_artifacts.py other-benchmarks/tasks-hotpotqa-mini --limit 6
python sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/scripts/scaffold_benchmark_skill.py sana-profiling/runs/hotpotqa-generated-conversion/hotpotqa-lakeqa-conversion-report.md --benchmark hotpotqa --output-root sana-profiling/runs/hotpotqa-generated-conversion/generated-skills --force
```

## Skill Interaction

1. Loaded `benchmark-lakeqa-conversion-auditor` and sampled HotpotQA mini artifacts.
2. Wrote a redacted conversion report that describes method, source model, k/d rules, and leakage risks without answer strings.
3. Loaded `benchmark-lakeqa-skill-scaffolder` and generated `hotpotqa-lakeqa-transform` from the report.
4. Applied the generated transform skill to one smoke example.
5. Wrote one converted task and one runtime profile under the current repo convention.
6. Checked prompt/report/runtime-profile surfaces for answer leakage.

## Outputs

- `sampled-artifacts.json`
- `hotpotqa-lakeqa-conversion-report.md`
- `generated-skills/hotpotqa-lakeqa-transform/SKILL.md`
- `converted/benchmarks/hotpotqa/tasks-mini/tasks/k-1-d-2/task_1.json`
- `converted/benchmarks/hotpotqa/tasks-mini/runtime-profiles/k-1-d-2/task_1.json`
- `source-mirroring-manifest.json`
- `validation.json`
- `error_log.json`

## Leakage Boundary

The converted task JSON includes answer fields because LakeQA task artifacts require them. The conversion report, generated skill, run log, and runtime-profile reasoning text are checked not to include the final answer or intermediate date answers.
