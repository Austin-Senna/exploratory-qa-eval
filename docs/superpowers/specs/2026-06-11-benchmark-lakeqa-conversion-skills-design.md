# Benchmark LakeQA Conversion Skills Design

## Goal

Make the repository usable as a public framework for converting arbitrary QA
benchmarks into LakeQA-style artifacts without maintaining benchmark-specific
importers. The conversion path should be CLI-first and skill-driven:

```text
raw benchmark
  -> conversion audit report
  -> benchmark-specific transform skill
  -> LakeQA task artifacts
  -> ideal plans
  -> verified plans
  -> ideal_query / ideal_code records
```

This design focuses only on new-benchmark conversion. Running existing LakeQA
or Kramabench artifacts is out of scope for this spec.

## Skill 1: benchmark-lakeqa-conversion-auditor

Purpose: infer a benchmark-to-LakeQA conversion recipe from benchmark artifacts
and examples, then write a human-reviewable report. It must not create converted
tasks, author ideal artifacts, or scaffold a new skill.

Inputs:

- Benchmark root directory.
- Optional hints for raw data roots, code/solution roots, and task/example roots.
- Existing LakeQA task exemplars, usually `tasks_mini/...`.
- Kramabench transform skill as a worked example of a mature conversion skill.

Auto-sampling:

- Scan candidate benchmark task/example files.
- Prefer structural diversity first: evidence type, source count, hop shape,
  answer type, executable computation likelihood, and presence of raw code/data.
- Use metadata diversity as a tie-breaker when fields exist: split, domain,
  difficulty, source benchmark labels, or question category.
- Write the sampled example list and rationale into the report.

Report artifact:

```text
docs/benchmark-conversions/<benchmark>-lakeqa-conversion.md
```

Required report sections:

- Benchmark artifact inventory.
- Auto-sampled examples and rationale.
- Evidence/source model.
- LakeQA task mapping.
- k/d/s bucket proposal.
- Source mirroring convention.
- Executable fact feasibility.
- Ideal artifact feasibility for `ideal_query` and `ideal_code`.
- Fairness and leakage risks.
- Validation strategy.
- Recommended benchmark-specific transform skill structure.
- Handoff contract to adjacent ideal-artifact skills.

The report should be specific enough that a separate agent can scaffold a
benchmark-specific transform skill without re-inferring the conversion method.

## Skill 2: benchmark-lakeqa-skill-scaffolder

Purpose: turn an approved conversion report into a benchmark-specific transform
skill under:

```text
.agents/skills/<benchmark>-lakeqa-transform/
```

The scaffolder must not invent a conversion method independently. It reads the
approved report, checks that required sections exist, and operationalizes that
report into a skill.

Scaffolded contents:

- `SKILL.md` with trigger metadata and concise conversion workflow.
- `references/conversion-report.md`, copied from the approved report or reduced
  to the operational portions needed by agents.
- Optional `scripts/` only when deterministic helpers are justified by the
  report.
- Worker assignment template for batch conversion when subagents are available.
- Validation checklist covering JSON shape, source refs, k/d/s placement,
  executable facts, and leakage checks.

The generated skill handles task conversion only. It should produce LakeQA task
JSON files and any conversion error logs needed for skipped examples.

## Adjacent Skills And Handoff Contract

The two new skills should route into existing ideal-artifact skills instead of
duplicating their responsibilities.

Use `author-ideal-plans` after converted LakeQA tasks exist and the user wants
ideal-mode plans. It creates or rewrites mirrored plan files from task reasoning
chains.

Use `plan-verifier` after ideal plans are drafted. It checks whether plans remain
faithful to the task while avoiding answer leakage or over-specific intermediate
clues.

Use `author-ideal-computations` after plans are verified and executable
computation records are needed. It fills `ideal_query` and `ideal_code` records
where the benchmark evidence supports deterministic computation.

The public workflow should explicitly allow stopping points:

- Stop after the conversion audit report for feasibility review.
- Stop after the benchmark-specific transform skill for repeatable conversion.
- Stop after LakeQA tasks for non-ideal evaluation.
- Continue into ideal plans and computations when ideal-mode evaluation is
  needed.

## CLI-First Public Workflow

The public interface should be expressed as commands or command-like prompts,
even though the implementation is skill-driven.

Suggested command shape:

```text
lakeqa benchmark audit <benchmark-root> --name <benchmark>
lakeqa benchmark scaffold-skill docs/benchmark-conversions/<benchmark>-lakeqa-conversion.md
lakeqa benchmark convert <benchmark-root> --skill <benchmark>-lakeqa-transform
lakeqa ideal plans <task-root>
lakeqa ideal verify <plan-root>
lakeqa ideal computations <plan-root>
```

These commands can initially be thin wrappers around skill-triggering workflows.
They should preserve the same artifact boundaries as the skills.

## Non-Goals

- Do not build one-off benchmark-specific importers into the framework.
- Do not fold ideal-plan or ideal-computation authoring into the conversion
  skills.
- Do not require users to manually select representative samples by default.
- Do not depend on private submodules, external-tools repos, or paper-only
  artifacts.

## Open Implementation Questions

- Whether the first CLI wrapper should live as a repo-local script or an
  installable console entry point.
- How strict the report parser should be in the scaffolder: heading-based checks
  may be enough initially.
- Whether generated benchmark skills should include deterministic scripts by
  default or only after a first successful manual conversion batch.
