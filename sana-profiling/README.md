# SANA Profiling

This folder contains public-facing framework artifacts for turning external QA
benchmarks into LakeQA-style tasks and ideal-mode artifacts.

## Benchmark conversion skills

- `skills/benchmark-lakeqa-conversion-auditor/`: infer and document a
  benchmark-to-LakeQA conversion recipe.
- `skills/benchmark-lakeqa-skill-scaffolder/`: turn an approved conversion
  report into a benchmark-specific transform skill.
- `skills/author-ideal-plans/`: author clean ideal planning runtime profiles
  under `benchmarks/<benchmark>/tasks-mini/runtime-profiles`.
- `skills/author-ideal-code/`: author `ideal_code` and `ideal_query` records
  inside runtime profiles.
- `skills/plan-verifier/`: check runtime-profile fidelity and leakage safety.

The intended handoff is:

```text
raw benchmark -> conversion report -> transform skill -> LakeQA tasks
  -> runtime profiles -> author-ideal-plans -> plan-verifier -> author-ideal-code
```

## Example runs

- `runs/hotpotqa-generated-conversion/`: dry-run output from applying a
  generated HotpotQA transform skill to one `other-benchmarks` smoke example.
