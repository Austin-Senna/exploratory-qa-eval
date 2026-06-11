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
