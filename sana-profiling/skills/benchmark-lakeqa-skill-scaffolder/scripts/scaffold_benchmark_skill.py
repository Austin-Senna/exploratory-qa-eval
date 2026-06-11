#!/usr/bin/env python3
"""Scaffold a benchmark-specific LakeQA transform skill from an approved report."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


REQUIRED_HEADINGS = (
    "## Benchmark artifact inventory",
    "## Recommended benchmark-specific transform skill structure",
)


def _slugify(raw: str) -> str:
    slug = "-".join(re.findall(r"[a-z0-9]+", raw.lower()))
    if not slug:
        raise argparse.ArgumentTypeError("benchmark must contain a letter or digit")
    return slug


def _load_report(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Report not found: {path}")
    return path.read_text(encoding="utf-8")


def _validate_report(text: str) -> None:
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"Report is missing required heading(s): {joined}")


def _skill_text(slug: str) -> str:
    skill_name = f"{slug}-lakeqa-transform"
    title = skill_name.replace("-", " ").title()
    return f"""---
name: {skill_name}
description: Use when Codex needs to convert {slug} benchmark artifacts into LakeQA-style task artifacts according to the approved benchmark conversion report.
---

# {title}

## Source of Truth

Read `references/conversion-report.md` before implementing or running this
transform. Do not re-infer the conversion method; the approved conversion report
defines the benchmark artifacts, evidence/source model, LakeQA mapping, k/d/s
bucket proposal, mirroring convention, validation strategy, and known risks.

If the report is incomplete or appears wrong, stop and revise the report through
the benchmark conversion audit process before changing this transform skill.

## Workflow

1. Read the approved conversion report in `references/conversion-report.md`.
2. Implement or run only the benchmark-to-LakeQA transform described there.
3. Generate LakeQA task JSON and mirrored source artifacts using the report's
   naming, bucketing, and validation guidance.
4. Validate the generated LakeQA tasks against the report's validation strategy.
5. Defer ideal plan, ideal code, and verifier handoff until LakeQA tasks exist.

## Handoff Boundary

After converted LakeQA tasks exist, use `author-ideal-plans`,
`plan-verifier`, and `author-ideal-computations` as appropriate. Do not duplicate
those workflows inside this transform skill.
"""


def scaffold(report: Path, benchmark: str, output_root: Path) -> Path:
    text = _load_report(report)
    _validate_report(text)

    slug = _slugify(benchmark)
    skill_root = output_root / f"{slug}-lakeqa-transform"
    references = skill_root / "references"
    references.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(report, references / "conversion-report.md")
    (skill_root / "SKILL.md").write_text(_skill_text(slug), encoding="utf-8")
    return skill_root


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--benchmark", required=True, type=_slugify)
    parser.add_argument("--output-root", default="sana-profiling/skills")
    args = parser.parse_args()

    report = Path(args.report).expanduser().resolve()
    output_root = Path(args.output_root).expanduser()
    scaffold(report, args.benchmark, output_root)


if __name__ == "__main__":
    main()
