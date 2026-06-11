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
SCAFFOLDER = SANA_PROFILING / "skills" / "benchmark-lakeqa-skill-scaffolder"


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


def test_sample_benchmark_artifacts_includes_common_tabular_and_jsonl_formats(tmp_path):
    root = tmp_path / "benchmark"
    root.mkdir()
    (root / "tasks.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"question": "q1", "answer": "a1"}),
                json.dumps({"question": "q2", "answer": "a2", "evidence": ["doc"]}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "metadata.csv").write_text(
        "question,answer,split\nq3,a3,dev\nq4,a4,test\n",
        encoding="utf-8",
    )
    (root / "events.ndjson").write_text(
        json.dumps({"question": "q5", "answer": "a5"}) + "\n",
        encoding="utf-8",
    )
    (root / "table.parquet").write_bytes(b"PAR1")

    script = AUDITOR / "scripts" / "sample_benchmark_artifacts.py"
    result = subprocess.run(
        [sys.executable, str(script), str(root), "--limit", "6"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    relative_paths = {sample["relative_path"] for sample in payload["samples"]}
    assert "tasks.jsonl" in relative_paths
    assert "metadata.csv" in relative_paths
    assert "events.ndjson" in relative_paths
    assert "table.parquet" in relative_paths
    assert payload["candidate_count"] == 4


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


def test_scaffolder_skill_contract():
    skill = SCAFFOLDER / "SKILL.md"

    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "name: benchmark-lakeqa-skill-scaffolder" in text
    assert "approved conversion report" in text
    assert "must not invent" in text


def test_scaffold_benchmark_skill_creates_transform_skill(tmp_path):
    report = tmp_path / "demo-report.md"
    report.write_text(
        "\n".join(
            [
                "# Demo LakeQA Conversion Report",
                "",
                "## Benchmark artifact inventory",
                "",
                "Demo inventory.",
                "",
                "## Recommended benchmark-specific transform skill structure",
                "",
                "Demo transform structure.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    script = SCAFFOLDER / "scripts" / "scaffold_benchmark_skill.py"
    output_root = tmp_path / "skills"
    subprocess.run(
        [
            sys.executable,
            str(script),
            str(report),
            "--benchmark",
            "Demo Benchmark!",
            "--output-root",
            str(output_root),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    generated_root = output_root / "demo-benchmark-lakeqa-transform"
    skill = generated_root / "SKILL.md"
    copied_report = generated_root / "references" / "conversion-report.md"

    assert skill.is_file()
    assert copied_report.is_file()
    assert copied_report.read_text(encoding="utf-8") == report.read_text(encoding="utf-8")
    skill_text = skill.read_text(encoding="utf-8")
    assert "name: demo-benchmark-lakeqa-transform" in skill_text
    assert "Do not re-infer the conversion method" in skill_text


def test_scaffold_benchmark_skill_rejects_missing_headings(tmp_path):
    report = tmp_path / "demo-report.md"
    report.write_text(
        "# Demo LakeQA Conversion Report\n\n"
        "This mentions ## Benchmark artifact inventory in prose only.\n",
        encoding="utf-8",
    )

    script = SCAFFOLDER / "scripts" / "scaffold_benchmark_skill.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            str(report),
            "--benchmark",
            "demo",
            "--output-root",
            str(tmp_path / "skills"),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "Report is missing required heading" in result.stderr


def test_scaffold_benchmark_skill_refuses_existing_destination(tmp_path):
    report = tmp_path / "demo-report.md"
    report.write_text(
        "# Demo LakeQA Conversion Report\n\n"
        "## Benchmark artifact inventory\n\n"
        "## Recommended benchmark-specific transform skill structure\n\n",
        encoding="utf-8",
    )
    output_root = tmp_path / "skills"
    existing = output_root / "demo-lakeqa-transform"
    existing.mkdir(parents=True)

    script = SCAFFOLDER / "scripts" / "scaffold_benchmark_skill.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            str(report),
            "--benchmark",
            "demo",
            "--output-root",
            str(output_root),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    assert "Skill directory already exists" in result.stderr
