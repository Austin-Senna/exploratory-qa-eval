# Benchmark LakeQA Conversion Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the public benchmark conversion workflow as two skills under `sana-profiling/skills/`.

**Architecture:** `benchmark-lakeqa-conversion-auditor` writes a conversion report; `benchmark-lakeqa-skill-scaffolder` turns an approved report into a benchmark-specific transform skill. The folder is self-contained under `sana-profiling/` and references existing ideal-plan, plan-verifier, and ideal-computation skills by handoff contract rather than duplicating them.

**Tech Stack:** Markdown skills, Python standard library scripts, pytest artifact checks.

---

## File Structure

- Create `sana-profiling/README.md`: short index for public profiling/conversion workflows.
- Create `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/SKILL.md`: workflow for auditing arbitrary benchmark artifacts and writing a report.
- Create `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/references/report-template.md`: stable report headings used by the scaffolder.
- Create `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/scripts/sample_benchmark_artifacts.py`: deterministic helper that lists candidate examples and emits a structural sampling manifest.
- Create `sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/SKILL.md`: workflow for converting an approved report into a benchmark-specific transform skill.
- Create `sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/scripts/scaffold_benchmark_skill.py`: deterministic scaffold helper.
- Create `test/test_sana_profiling_skill_artifacts.py`: tests the folder, report template, script behavior, and generated skill shape.

## Task 1: Add Folder Index And Artifact Test Skeleton

**Files:**
- Create: `sana-profiling/README.md`
- Create: `test/test_sana_profiling_skill_artifacts.py`

- [ ] **Step 1: Write the failing artifact tests**

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SANA_PROFILING = ROOT / "sana-profiling"


def test_sana_profiling_folder_has_public_index():
    readme = SANA_PROFILING / "README.md"

    assert readme.is_file()
    text = readme.read_text(encoding="utf-8")
    assert "Benchmark conversion skills" in text
    assert "benchmark-lakeqa-conversion-auditor" in text
    assert "benchmark-lakeqa-skill-scaffolder" in text
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: failure because `sana-profiling/README.md` does not exist.

- [ ] **Step 3: Add the folder index**

```markdown
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
```

- [ ] **Step 4: Run the test and verify it passes**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: `1 passed`.

- [ ] **Step 5: Commit**

```bash
git add sana-profiling/README.md test/test_sana_profiling_skill_artifacts.py
git commit -m "Add SANA profiling skill index"
```

## Task 2: Add Conversion Auditor Skill

**Files:**
- Create: `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/SKILL.md`
- Create: `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/references/report-template.md`
- Modify: `test/test_sana_profiling_skill_artifacts.py`

- [ ] **Step 1: Extend tests for auditor artifacts**

Append:

```python
AUDITOR = SANA_PROFILING / "skills" / "benchmark-lakeqa-conversion-auditor"


def test_conversion_auditor_skill_contract():
    skill = AUDITOR / "SKILL.md"
    template = AUDITOR / "references" / "report-template.md"

    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "name: benchmark-lakeqa-conversion-auditor" in text
    assert "docs/benchmark-conversions/<benchmark>-lakeqa-conversion.md" in text
    assert "structural diversity first" in text
    assert "author-ideal-plans" in text
    assert "plan-verifier" in text
    assert "author-ideal-computations" in text

    assert template.is_file()
    template_text = template.read_text(encoding="utf-8")
    for heading in [
        "Benchmark artifact inventory",
        "Auto-sampled examples and rationale",
        "Evidence/source model",
        "LakeQA task mapping",
        "Ideal artifact feasibility",
        "Recommended benchmark-specific transform skill structure",
    ]:
        assert f"## {heading}" in template_text
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: failure because the auditor skill files do not exist.

- [ ] **Step 3: Add the auditor `SKILL.md`**

```markdown
---
name: benchmark-lakeqa-conversion-auditor
description: Use when Codex needs to infer how an arbitrary benchmark can be converted into LakeQA-style task artifacts without a benchmark-specific importer, especially when reading benchmark examples, raw data, solution code, LakeQA exemplars, Kramabench transform patterns, source mirroring rules, k/d/s topology, fairness risks, or ideal artifact feasibility.
---

# Benchmark LakeQA Conversion Auditor

## Scope

Infer and document a conversion recipe. Do not write converted task JSON, do not
scaffold a transform skill, and do not author ideal plans or computation records.

Write the report to:

```text
docs/benchmark-conversions/<benchmark>-lakeqa-conversion.md
```

## Inputs

- Benchmark root directory.
- Optional hints for task examples, raw data, or solution code.
- LakeQA task exemplars, usually `tasks_mini/...`.
- Kramabench transform skill as the strongest local example of a mature
  benchmark-to-LakeQA conversion workflow.

## Sampling Rule

Auto-sample examples. Prefer structural diversity first: evidence type, source
count, hop shape, answer type, executable computation likelihood, and available
raw code/data. Use split, domain, difficulty, or other metadata diversity only
as a tie-breaker.

Run the helper when useful:

```bash
python sana-profiling/skills/benchmark-lakeqa-conversion-auditor/scripts/sample_benchmark_artifacts.py <benchmark-root>
```

## Report Contract

Start from `references/report-template.md`. Fill every section with concrete
evidence from inspected artifacts. If a section is not applicable, state why.

The report must cover:

- benchmark artifact inventory
- sampled examples and rationale
- evidence/source model
- LakeQA task mapping
- k/d/s bucket proposal
- source mirroring convention
- executable fact feasibility
- ideal artifact feasibility for `ideal_query` and `ideal_code`
- fairness and leakage risks
- validation strategy
- recommended transform skill structure

## Handoff Contract

After converted LakeQA tasks exist, use:

- `author-ideal-plans` to create or rewrite mirrored ideal plans
- `plan-verifier` to check fidelity and leakage
- `author-ideal-computations` to fill `ideal_query` and `ideal_code`

Do not duplicate those workflows in this skill.
```

- [ ] **Step 4: Add the report template**

```markdown
# <Benchmark> LakeQA Conversion Report

## Benchmark artifact inventory

## Auto-sampled examples and rationale

## Evidence/source model

## LakeQA task mapping

## k/d/s bucket proposal

## Source mirroring convention

## Executable fact feasibility

## Ideal artifact feasibility

Cover both `ideal_query` and `ideal_code`.

## Fairness and leakage risks

## Validation strategy

## Recommended benchmark-specific transform skill structure

## Handoff contract to adjacent ideal-artifact skills

- `author-ideal-plans`:
- `plan-verifier`:
- `author-ideal-computations`:
```

- [ ] **Step 5: Run tests**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: auditor test passes, sampler tests not yet present.

- [ ] **Step 6: Commit**

```bash
git add sana-profiling/skills/benchmark-lakeqa-conversion-auditor test/test_sana_profiling_skill_artifacts.py
git commit -m "Add benchmark conversion auditor skill"
```

## Task 3: Add Auditor Sampling Helper

**Files:**
- Create: `sana-profiling/skills/benchmark-lakeqa-conversion-auditor/scripts/sample_benchmark_artifacts.py`
- Modify: `test/test_sana_profiling_skill_artifacts.py`

- [ ] **Step 1: Add sampler behavior test**

Append:

```python
import json
import subprocess
import sys


def test_sample_benchmark_artifacts_prefers_structural_diversity(tmp_path):
    root = tmp_path / "benchmark"
    root.mkdir()
    (root / "one.json").write_text(
        json.dumps({"question": "q1", "answer": "a1", "evidence": ["doc1"]}),
        encoding="utf-8",
    )
    (root / "two.json").write_text(
        json.dumps({"question": "q2", "answer": "a2", "evidence": ["doc1", "doc2"]}),
        encoding="utf-8",
    )
    (root / "notes.txt").write_text("not json", encoding="utf-8")

    script = AUDITOR / "scripts" / "sample_benchmark_artifacts.py"
    result = subprocess.run(
        [sys.executable, str(script), str(root), "--limit", "2"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert payload["benchmark_root"] == str(root)
    assert len(payload["samples"]) == 2
    signatures = {sample["signature"] for sample in payload["samples"]}
    assert any("evidence:list:1" in signature for signature in signatures)
    assert any("evidence:list:2" in signature for signature in signatures)
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py::test_sample_benchmark_artifacts_prefers_structural_diversity -q
```

Expected: failure because the sampler script does not exist.

- [ ] **Step 3: Add sampler script**

```python
#!/usr/bin/env python3
"""Sample benchmark artifacts with simple structural diversity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _signature(value: Any) -> str:
    if isinstance(value, dict):
        parts: list[str] = []
        for key in sorted(value):
            item = value[key]
            if isinstance(item, list):
                parts.append(f"{key}:list:{len(item)}")
            elif isinstance(item, dict):
                parts.append(f"{key}:dict:{len(item)}")
            else:
                parts.append(f"{key}:{type(item).__name__}")
        return "|".join(parts)
    if isinstance(value, list):
        return f"root:list:{len(value)}"
    return f"root:{type(value).__name__}"


def sample(root: Path, limit: int) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.json")):
        payload = _load_json(path)
        if payload is None:
            continue
        candidates.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(root)),
                "signature": _signature(payload),
            }
        )

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate["signature"] in seen:
            continue
        selected.append(candidate)
        seen.add(candidate["signature"])
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        for candidate in candidates:
            if candidate in selected:
                continue
            selected.append(candidate)
            if len(selected) >= limit:
                break

    return {
        "benchmark_root": str(root),
        "candidate_count": len(candidates),
        "sampling_rule": "structural diversity first, metadata diversity second",
        "samples": selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark_root")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    root = Path(args.benchmark_root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Benchmark root not found: {root}")
    print(json.dumps(sample(root, args.limit), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add sana-profiling/skills/benchmark-lakeqa-conversion-auditor/scripts/sample_benchmark_artifacts.py test/test_sana_profiling_skill_artifacts.py
git commit -m "Add benchmark artifact sampler"
```

## Task 4: Add Skill Scaffolder

**Files:**
- Create: `sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/SKILL.md`
- Create: `sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/scripts/scaffold_benchmark_skill.py`
- Modify: `test/test_sana_profiling_skill_artifacts.py`

- [ ] **Step 1: Add scaffolder tests**

Append:

```python
SCAFFOLDER = SANA_PROFILING / "skills" / "benchmark-lakeqa-skill-scaffolder"


def test_scaffolder_skill_contract():
    skill = SCAFFOLDER / "SKILL.md"

    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "name: benchmark-lakeqa-skill-scaffolder" in text
    assert "approved conversion report" in text
    assert "must not invent" in text


def test_scaffold_benchmark_skill_creates_transform_skill(tmp_path):
    report = tmp_path / "demo-lakeqa-conversion.md"
    report.write_text(
        "# Demo LakeQA Conversion Report\n\n"
        "## Benchmark artifact inventory\n\n"
        "## Recommended benchmark-specific transform skill structure\n\n",
        encoding="utf-8",
    )
    output_root = tmp_path / "skills"
    script = SCAFFOLDER / "scripts" / "scaffold_benchmark_skill.py"

    subprocess.run(
        [
            sys.executable,
            str(script),
            str(report),
            "--benchmark",
            "demo",
            "--output-root",
            str(output_root),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    skill_dir = output_root / "demo-lakeqa-transform"
    assert (skill_dir / "SKILL.md").is_file()
    assert (skill_dir / "references" / "conversion-report.md").is_file()
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "name: demo-lakeqa-transform" in text
    assert "Do not re-infer the conversion method" in text
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: failure because scaffolder files do not exist.

- [ ] **Step 3: Add scaffolder `SKILL.md`**

```markdown
---
name: benchmark-lakeqa-skill-scaffolder
description: Use when Codex needs to turn an approved benchmark-to-LakeQA conversion report into a benchmark-specific transform skill folder, especially under sana-profiling skills, without re-inferring the conversion method or authoring converted benchmark tasks directly.
---

# Benchmark LakeQA Skill Scaffolder

## Scope

Read an approved conversion report and scaffold a benchmark-specific transform
skill. The scaffolder must not invent or re-infer the conversion method.

Default output:

```text
sana-profiling/skills/<benchmark>-lakeqa-transform/
```

## Workflow

1. Read the approved report.
2. Confirm it includes artifact inventory and recommended skill structure.
3. Run the scaffold helper.
4. Review the generated `SKILL.md` against the report.
5. Leave actual task conversion to the generated benchmark-specific skill.

```bash
python sana-profiling/skills/benchmark-lakeqa-skill-scaffolder/scripts/scaffold_benchmark_skill.py \
  docs/benchmark-conversions/<benchmark>-lakeqa-conversion.md \
  --benchmark <benchmark> \
  --output-root sana-profiling/skills
```
```

- [ ] **Step 4: Add scaffold script**

```python
#!/usr/bin/env python3
"""Scaffold a benchmark-specific LakeQA transform skill from a report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def _skill_name(raw: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    if not slug:
        raise ValueError("benchmark name cannot be empty")
    return f"{slug}-lakeqa-transform"


def scaffold(report: Path, benchmark: str, output_root: Path) -> Path:
    if not report.is_file():
        raise FileNotFoundError(report)
    report_text = report.read_text(encoding="utf-8")
    required = [
        "## Benchmark artifact inventory",
        "## Recommended benchmark-specific transform skill structure",
    ]
    missing = [heading for heading in required if heading not in report_text]
    if missing:
        raise ValueError(f"report missing required headings: {', '.join(missing)}")

    name = _skill_name(benchmark)
    skill_dir = output_root / name
    references = skill_dir / "references"
    references.mkdir(parents=True, exist_ok=True)
    (references / "conversion-report.md").write_text(report_text, encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(
        f"""---
name: {name}
description: Use when converting {benchmark} benchmark artifacts into LakeQA-style task JSON according to the approved conversion report bundled with this skill.
---

# {benchmark} LakeQA Transform

## Source Of Truth

Read `references/conversion-report.md` before converting tasks. Do not re-infer
the conversion method, source mirroring convention, k/d/s rule, or fairness
constraints unless the user asks to revise the report.

## Workflow

1. Read the approved conversion report.
2. Select a small batch of benchmark examples.
3. Convert only promotable examples into LakeQA task JSON.
4. Write skipped examples to a structured error log with precise reasons.
5. Validate JSON shape, source refs, k/d/s bucket placement, executable facts,
   and leakage constraints.
6. Hand off to `author-ideal-plans`, `plan-verifier`, and
   `author-ideal-computations` only after LakeQA tasks exist.
""",
        encoding="utf-8",
    )
    return skill_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--benchmark", required=True)
    parser.add_argument("--output-root", default="sana-profiling/skills")
    args = parser.parse_args()
    created = scaffold(Path(args.report), args.benchmark, Path(args.output_root))
    print(created)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add sana-profiling/skills/benchmark-lakeqa-skill-scaffolder test/test_sana_profiling_skill_artifacts.py
git commit -m "Add benchmark skill scaffolder"
```

## Task 5: Final Verification

**Files:**
- Verify only.

- [ ] **Step 1: Run artifact tests**

Run:

```bash
.venv/bin/python -m pytest test/test_sana_profiling_skill_artifacts.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Scan for accidental placeholders**

Run:

```bash
rg -n "TB[D]|TO[D]O|FI[X]ME|\\?\\?" sana-profiling
```

Expected: no matches.

- [ ] **Step 3: Check final status**

Run:

```bash
git status --short --branch
```

Expected: only intentional untracked user files remain outside the implemented
skill artifacts.
