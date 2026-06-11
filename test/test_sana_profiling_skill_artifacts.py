import json
import subprocess
import sys
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


def test_sample_benchmark_artifacts_rejects_non_positive_limit(tmp_path):
    root = tmp_path / "benchmark"
    root.mkdir()
    (root / "one.json").write_text(json.dumps({"question": "q1"}), encoding="utf-8")

    script = AUDITOR / "scripts" / "sample_benchmark_artifacts.py"
    result = subprocess.run(
        [sys.executable, str(script), str(root), "--limit", "0"],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "must be a positive integer" in result.stderr
