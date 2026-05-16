# HotpotQA Work Log

Prepared on 2026-05-14 for the HotpotQA mini import, promotion, skill, and S3 context-upload work in this repository.

## Raw Data Location

- HotpotQA raw source file:
  - `other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json`
- Existing full raw imported task tree:
  - `other-benchmarks/tasks/hotpotqa/k-2-d-2/`
- Important raw-file shape:
  - Each raw example includes `_id`, `question`, `answer`, `supporting_facts`, `context`, `type`, and `level`.
  - `context` already contains Wikipedia-derived article snippets as `[title, sentences]` pairs.
  - These are not full Wikipedia page dumps; they are the HotpotQA distractor/supporting paragraphs included with the dataset.

## Mini Sampler

Implemented HotpotQA mini sampling in:

- `other-benchmarks/data-imports/_shared/sample_hard.py`

Added function:

```python
hotpotqa_mini(output_root: Path | None = None) -> list[Path]
```

Behavior:

- Samples 135 deterministic hard HotpotQA tasks.
- Uses the existing `equal_per_bucket(...)` logic to balance across imported HotpotQA buckets:
  - 67 comparison tasks from `other-benchmarks/tasks/hotpotqa/k-2-d-1/`
  - 68 bridge tasks from `other-benchmarks/tasks/hotpotqa/k-2-d-2/`
- Writes them to:
  - `other-benchmarks/tasks-hotpotqa-mini/k-2-d-1/task_*.json`
  - `other-benchmarks/tasks-hotpotqa-mini/k-2-d-2/task_*.json`
- Preserves the five previously authored bridge pilot source IDs inside the 68-task bridge sample.
- Preserves deterministic numbering.
- Wipes the output root before writing.
- Adds `_provenance.sample_source` pointing back to the original imported task path.
- The shared sampler CLI now runs `hotpotqa_mini()` after the existing MuSiQue, MMQA, and Kramabench mini samplers.

Command:

```bash
python3 other-benchmarks/data-imports/_shared/sample_hard.py
```

## HotpotQA Mini Promotion

Implemented the dedicated HotpotQA promoter in:

- `other-benchmarks/data-imports/hotpotqa/promote_sample.py`

Public API:

```python
promote_sample_tasks(
    input_root: Path | None = None,
    output_root: Path | None = None,
) -> list[Path]
```

Default input:

- `other-benchmarks/tasks-hotpotqa-mini/`

Default output:

- `tasks-hotpotqa-mini/`

Default raw source:

- `other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json`

Command:

```bash
python3 other-benchmarks/data-imports/hotpotqa/promote_sample.py
```

Promotion behavior:

- Promotion currently remains explicitly authored for the five bridge pilot tasks in `k-2-d-2`.
- Appends `Write your answer as [ANSWER].` to every top-level question.
- Rewrites node sources from `hotpotqa://wiki/<Title>` to:
  - `other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json#<source_id>:<Title>`
- Builds exactly two nodes per task.
- Writes source-agnostic natural-language node `subquestion` values.
- Uses `<NODE_1_ANSWER>` in second-hop subquestions where the second hop depends on the first hop.
- Sets `nodes[*].fact` to HotpotQA supporting evidence text, not executable Python.
- Verifies that the normalized node answer appears in the evidence text.
- Writes `reasoning_chain`, `reasoning_hops`, `datasets_used`, `_provenance.transform_run_id`, and `_provenance.verified_at`.
- Writes `tasks-hotpotqa-mini/SKIPPED.md`.
- Skips tasks instead of fabricating output if a source ID, supporting sentence, node answer, or terminal answer cannot be verified.
- With the 135-task raw sample, the current promoter writes the five explicitly authored bridge tasks and records the remaining unauthored tasks in `SKIPPED.md`.

Correction made during the work:

- The initial plan suggested executable Python `fact` fields.
- After review, HotpotQA facts were changed to evidence text because HotpotQA is already a text-evidence task.
- Tests now explicitly reject code-like facts containing markers such as `import json` or `print(`.

## Promoted Pilot Tasks

Current promoted files:

- `tasks-hotpotqa-mini/SKIPPED.md`
- `tasks-hotpotqa-mini/k-2-d-2/task_1.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_2.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_3.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_4.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_5.json`

Current `SKIPPED.md` content:

```markdown
# Skipped HotpotQA Mini Tasks

- other-benchmarks/tasks-hotpotqa-mini/k-2-d-1/task_1.json - missing_pilot_authoring:...
...
```

The current default promotion run skips 130 unauthored raw-sample tasks and promotes the five explicitly authored bridge pilot tasks.

Pilot authoring map:

| Task | Source ID | Node 1 answer | Final answer |
|---|---|---|---|
| `task_1.json` | `5a70eee85542994082a3e3f0` | `Ida` | `The Yoruba` |
| `task_2.json` | `5a70f0a75542994082a3e403` | `Spettekaka` | `Scanian dialects` |
| `task_3.json` | `5a70f1685542994082a3e40f` | `Ludwig van Beethoven` | `Symphony No. 7` |
| `task_4.json` | `5a70f39c5542994082a3e429` | `Libby Mitchell` | `Eliot Cutler` |
| `task_5.json` | `5a70f4c45542994082a3e437` | `Gian Carlo Menotti` | `Gian Carlo Menotti` |

Example promoted node source:

```text
other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json#5a70eee85542994082a3e3f0:Ida (sword)
```

Example promoted fact:

```text
Ida (sword): It is a long sword with a narrow to wide blade and sheathe.
```

## Dedicated Skill

Created a repo-local Codex skill for HotpotQA mini transformation:

- `.agents/skills/hotpotqa-mini-transform/SKILL.md`
- `.agents/skills/hotpotqa-mini-transform/agents/openai.yaml`

Skill purpose:

- Use this skill for HotpotQA mini sampling, promotion, authoring, and validation.
- Prefer it over the generic imported-benchmark transformer for HotpotQA.
- Keep HotpotQA `fact` fields as evidence text, not Python code.

Skill workflow:

```bash
python3 other-benchmarks/data-imports/_shared/sample_hard.py
python3 other-benchmarks/data-imports/hotpotqa/promote_sample.py
.venv/bin/python -m pytest test/test_hotpotqa_mini_promotion.py -q
```

Skill validation command that was used:

```bash
.venv/bin/python /Users/austinsenna/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/hotpotqa-mini-transform
```

Expected validation result:

```text
Skill is valid!
```

## LakeQA Judge Skill

Created a repo-local Codex skill for auditing LakeQA-style task shape and coherence:

- `.agents/skills/lakeqa-task-judge/SKILL.md`
- `.agents/skills/lakeqa-task-judge/agents/openai.yaml`

Skill purpose:

- Audit task JSON files for LakeQA `k` and `d` correctness.
- Use one LLM subagent per five tasks.
- Compute `k = len(reasoning_hops)`.
- Compute `d = max(len(hop["node_ids"]) for hop in reasoning_hops)`.
- Check whether the bucket path `k-X-d-Y` matches computed `k` and `d`.
- Judge whether the question, nodes, subquestions, reasoning chain, and hop grouping make sense.
- For HotpotQA and other text-evidence tasks, allow empty or non-executable facts; do not fail a task just because facts are not Python.

Skill validation command:

```bash
.venv/bin/python /Users/austinsenna/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/lakeqa-task-judge
```

Observed validation result:

```text
Skill is valid!
```

## Promotion Tests

Added:

- `test/test_hotpotqa_mini_promotion.py`

Coverage:

- `hotpotqa_mini()` writes exactly 135 raw mini tasks.
- The 135-task sample is balanced as 67 `k-2-d-1` comparison tasks and 68 `k-2-d-2` bridge tasks.
- All sampled tasks are HotpotQA hard tasks.
- The five authored bridge pilot source IDs are included in the sample.
- `_provenance.sample_source` points back to `other-benchmarks/tasks/hotpotqa/k-2-d-*/task_*.json`.
- `promote_sample_tasks()` writes five promoted tasks in `k-2-d-2` from the authored bridge pilot and skips unauthored tasks.
- `tasks-hotpotqa-mini/SKIPPED.md` exists.
- Every promoted question ends with `Write your answer as [ANSWER].`.
- Every promoted task has exactly two nodes.
- Terminal node answer equals the top-level answer.
- Every node has exactly `source`, `fact`, `subquestion`, and `answer`.
- No promoted source starts with `hotpotqa://`.
- Every promoted source starts with `other-benchmarks/raw/hotpotqa/`.
- Node facts are evidence text, not code.
- Every normalized node answer appears in its fact text.
- `_provenance.transform_run_id` and `_provenance.verified_at` are present.

Command:

```bash
.venv/bin/python -m pytest test/test_hotpotqa_mini_promotion.py -q
```

Observed result:

```text
2 passed
```

## Backend And Tooling Decision

We considered adding HotpotQA-specific runtime tools under `tools/hotpotqa/`, including a custom `search_hotpotqa`.

That was not implemented.

The plan changed to uploading sanitized HotpotQA context files to S3 so the existing backend and hybrid-search tooling can be reused without breaking old tools.

Relevant existing backend facts:

- `strands_evaluation/tools/agent_tools.py` hardcodes:
  - `BUCKET = "lakeqa-yc4103-datalake"`
  - `FOLDERS = ["wikipedia", "datagov"]`
- `strands_evaluation/tools/agent_tools.py` accepts S3 references only when the key starts with a known folder such as `wikipedia/` or `datagov/`.
- `strands_evaluation/tools/agent_tools_v2.py` reuses `_resolve_file_reference` from `agent_tools.py` for `peek_file`, `read_file`, `grep_file`, and `query_file`.
- `external-tools/hybrid_search/process.py` can read a manifest where each JSONL row has `s3_uri`.

Consequence:

- For compatibility with the current `agent_tools` backend, HotpotQA S3 objects should be uploaded under:
  - `s3://lakeqa-yc4103-datalake/wikipedia/...`
- A bucket URI with an extra prefix, such as `s3://lakeqa-yc4103-datalake/hotpotqa-pilot/wikipedia/...`, is useful for staging but will not parse with the current old backend unless that backend is changed.
- Custom buckets also require backend changes because the current backend expects `lakeqa-yc4103-datalake`.

## HotpotQA S3 Context Upload Script

Added:

- `scripts/upload_hotpotqa_context_to_s3.py`

Purpose:

- Materialize sanitized HotpotQA context snippets as text files.
- Upload those text files to S3.
- Write a manifest suitable for `external-tools/hybrid_search/process.py`.

Default raw input:

- `other-benchmarks/raw/hotpotqa/hotpot_dev_distractor_v1.json`

Default staging output:

- `other-benchmarks/data-imports/hotpotqa/_s3_context_staging`

Default manifest:

- `manifests/hotpotqa_context_manifest.jsonl`

CLI:

```bash
python3 scripts/upload_hotpotqa_context_to_s3.py \
  --bucket-uri s3://lakeqa-yc4103-datalake
```

Useful pilot dry run:

```bash
python3 scripts/upload_hotpotqa_context_to_s3.py \
  --bucket-uri s3://lakeqa-yc4103-datalake \
  --limit 1 \
  --staging-dir /tmp/hotpotqa_s3_stage \
  --manifest-path /tmp/hotpotqa_context_manifest.jsonl \
  --dry-run
```

Optional filters:

- `--source-id <hotpotqa_id>` can be repeated.
- `--limit <n>` limits selected raw examples after source ID filtering.
- `--dry-run` stages files and prints the upload plan without calling S3.

Python API:

```python
materialize_uploads(
    bucket_uri: str,
    staging_dir: Path = DEFAULT_STAGING_DIR,
    raw_path: Path = DEFAULT_RAW_PATH,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    source_ids: set[str] | None = None,
    limit: int | None = None,
) -> list[UploadItem]

upload_materialized_files(items: list[UploadItem], s3_client=None) -> list[UploadItem]
```

S3 key shape:

```text
wikipedia/hotpotqa__<source_id>/files/<title_slug>.txt
```

Example full URI:

```text
s3://lakeqa-yc4103-datalake/wikipedia/hotpotqa__5a8b57f25542995d1e6f1371/files/Scott_Derrickson.txt
```

If `--bucket-uri` contains a prefix, the prefix is prepended before `wikipedia/`.

Text-file shape:

```text
Title: <Wikipedia title>
HotpotQA Source ID: <source_id>

[0] <sentence 0>
[1] <sentence 1>
```

Sanitization:

- The script writes only title, source ID, and context sentences.
- It does not write the raw `answer` field.
- It does not write the raw `supporting_facts` labels.
- It does not write the raw question.

Manifest row shape:

```json
{"s3_uri":"s3://...","dataset_id":"hotpotqa__<source_id>","source_id":"<source_id>","title":"<title>"}
```

Upload implementation:

- Uses `boto3.client("s3").upload_file(...)` when no client is injected.
- Accepts an injected `s3_client` for tests.

## S3 Upload Tests

Added:

- `test/test_hotpotqa_s3_upload.py`

Coverage:

- `parse_bucket_uri()` accepts bucket-only and bucket-plus-prefix S3 URIs.
- `materialize_uploads()` writes deterministic context files and a JSONL manifest.
- Materialized context files include `HotpotQA Source ID` and sentence indexes.
- Materialized context files do not include raw labels such as `supporting_facts`.
- Manifest rows match the generated `UploadItem.s3_uri` values.
- `upload_materialized_files()` calls an injected fake client with expected bucket/key values.

Command:

```bash
.venv/bin/python -m pytest test/test_hotpotqa_s3_upload.py -q
```

Observed result:

```text
3 passed
```

## Hybrid Search Follow-Up

After uploading HotpotQA context files to S3, the generated manifest can be used as input to the existing hybrid-search index builder.

Example command shape:

```bash
python3 external-tools/hybrid_search/process.py \
  --manifest manifests/hotpotqa_context_manifest.jsonl \
  --build-mode basic \
  --output lance_data_hotpotqa
```

This follow-up was not run as part of the HotpotQA work log captured here.

## Current Workflow

Regenerate the raw mini set:

```bash
python3 other-benchmarks/data-imports/_shared/sample_hard.py
```

Promote it into LakeQA-style tasks:

```bash
python3 other-benchmarks/data-imports/hotpotqa/promote_sample.py
```

Validate the mini promotion:

```bash
.venv/bin/python -m pytest test/test_hotpotqa_mini_promotion.py -q
```

Dry-run one HotpotQA S3 example:

```bash
python3 scripts/upload_hotpotqa_context_to_s3.py \
  --bucket-uri s3://lakeqa-yc4103-datalake \
  --limit 1 \
  --staging-dir /tmp/hotpotqa_s3_stage \
  --manifest-path /tmp/hotpotqa_context_manifest.jsonl \
  --dry-run
```

Upload all HotpotQA raw context snippets to the current backend-compatible bucket root:

```bash
python3 scripts/upload_hotpotqa_context_to_s3.py \
  --bucket-uri s3://lakeqa-yc4103-datalake \
  --manifest-path manifests/hotpotqa_context_manifest.jsonl
```

Use `--limit` or repeated `--source-id` first if you want a smaller pilot upload.

## Files Added Or Changed For HotpotQA

HotpotQA mini import and promotion:

- `other-benchmarks/data-imports/_shared/sample_hard.py`
- `other-benchmarks/data-imports/hotpotqa/promote_sample.py`
- `other-benchmarks/tasks-hotpotqa-mini/k-2-d-1/task_*.json`
- `other-benchmarks/tasks-hotpotqa-mini/k-2-d-2/task_*.json`
- `tasks-hotpotqa-mini/SKIPPED.md`
- `tasks-hotpotqa-mini/k-2-d-2/task_1.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_2.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_3.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_4.json`
- `tasks-hotpotqa-mini/k-2-d-2/task_5.json`
- `test/test_hotpotqa_mini_promotion.py`

HotpotQA skill:

- `.agents/skills/hotpotqa-mini-transform/SKILL.md`
- `.agents/skills/hotpotqa-mini-transform/agents/openai.yaml`

LakeQA judge skill:

- `.agents/skills/lakeqa-task-judge/SKILL.md`
- `.agents/skills/lakeqa-task-judge/agents/openai.yaml`

HotpotQA S3 upload:

- `scripts/upload_hotpotqa_context_to_s3.py`
- `test/test_hotpotqa_s3_upload.py`

This log:

- `hotpotqa.md`

## Git And Ignore Notes

- `other-benchmarks/` is ignored by the repository, so the raw mini files and promoter files under that tree may not appear in normal `git status --short`.
- `.agents/` is ignored by the repository, so the HotpotQA skill may not appear in normal `git status --short`.
- `scripts/upload_hotpotqa_context_to_s3.py`, `test/test_hotpotqa_s3_upload.py`, `test/test_hotpotqa_mini_promotion.py`, `tasks-hotpotqa-mini/`, and this `hotpotqa.md` are visible to normal Git status unless another ignore rule is added.
