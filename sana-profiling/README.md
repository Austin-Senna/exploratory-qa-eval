# SANA Profiling

This folder contains public-facing framework artifacts for turning external QA
benchmarks into LakeQA-style tasks and ideal-mode artifacts.

## Benchmark conversion skills

- `skills/benchmark-lakeqa-conversion-auditor/`: infer and document a
  benchmark-to-LakeQA conversion recipe.
- `skills/benchmark-lakeqa-skill-scaffolder/`: turn an approved conversion
  report into a benchmark-specific transform skill.

The intended handoff is:

```text
raw benchmark -> conversion report -> transform skill -> LakeQA tasks
  -> author-ideal-plans -> plan-verifier -> author-ideal-computations
```
