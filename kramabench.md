# Kramabench Work Log

This file records the Kramabench work done in this repo so far. It is written
as an implementation ledger: what exists, where it lives, how it behaves, and
what is still only a design note.

## Current Decision

Kramabench data will be mirrored into a separate S3 bucket:

```text
s3://kramabench
```

The current direction is to reuse the existing LakeQA/S3 data tooling wherever
possible instead of building a separate local-only Kramabench tool runtime.

The S3 layout chosen for pilot files follows the existing data-lake style:

```text
s3://kramabench/datagov/<dataset_id>/files/<filename>
```

### 2026-05-14 Correction: Raw-All Promotion Truth

Final `tasks-mini-kramabench` promotion should run directly from all 104 main
Kramabench workload tasks, not from the import-stage `k-d-j-f` inventory and
not from a strict `dr-input` filtered subset.

The direct raw-all candidate list is:

```text
tasks-mini-kramabench/candidate_list.json
tasks-mini-kramabench/candidates/<source_id>.json
```

It is generated with:

```bash
python scripts/build_kramabench_raw_candidate_list.py --output-root tasks-mini-kramabench
```

Promotion uses the upstream workload, solution files, and full raw data roots:

```text
other-benchmarks/Kramabench/workload/
other-benchmarks/Kramabench/solutions/
other-benchmarks/Kramabench/data/<domain>/input/
```

`dr-input` bundles remain useful context when present, but absence of `dr-input`
is no longer a reason to skip a task.

Final S3 sources should use one per-task dataset id:

```text
s3://kramabench/datagov/kramabench-<source_id>/files/<filename>
```

That keeps each promoted task's local authoring files, retrieval-visible S3
objects, and final task source refs aligned.

## Source Of Truth

The local Kramabench clone is treated as read-only source material:

```text
other-benchmarks/Kramabench/
```

The converter reads from:

```text
other-benchmarks/Kramabench/workload/
other-benchmarks/Kramabench/solutions/
other-benchmarks/Kramabench/data/
```

The final promotion step now reads from:

```text
other-benchmarks/Kramabench/workload/
other-benchmarks/Kramabench/solutions/
other-benchmarks/Kramabench/data/<domain>/input/
```

Optional `dr-input` bundles may be recorded in provenance if they exist:

```text
other-benchmarks/Kramabench/dr-input/
```

I did not modify `other-benchmarks/Kramabench/`.

Important repo note: `other-benchmarks/` is ignored by `.gitignore`, so scripts
and generated tasks under that tree are local workspace artifacts unless the
ignore rule changes.

## Import-Stage Converter

Created:

```text
other-benchmarks/data-imports/kramabench/convert.py
other-benchmarks/data-imports/kramabench/slicer.py
```

The converter generates import-stage tasks here:

```text
other-benchmarks/tasks/kramabench/
```

Current generated count:

```text
104 task_*.json files
```

The import buckets use this four-axis grammar:

```text
k-<hops>-d-<declared_datasets>-j-<difficulty>-f-<fanout>
```

Axis meanings:

```text
k = number of Kramabench subtasks / reasoning hops
d = number of normalized top-level declared data_sources
j = difficulty parsed from task id: easy=1, medium=2, hard=3
f = maximum number of normalized file refs used by any one subtask
```

Each task keeps these top-level keys:

```text
question
answer
nodes
reasoning_chain
datasets_used
reasoning_hops
_provenance
```

Each node source is emitted in Kramabench slash form:

```text
kramabench/<domain>/files/<file_ref>
```

Glob references are preserved as one virtual source, for example:

```text
kramabench/legal/files/State MSA Identity Theft Data/*
```

The converter records exact import axes in:

```text
_provenance.bucket_axes
```

and records how each node fact was constructed in:

```text
_provenance.fact_origin_per_node
```

Known fact origins:

```text
ast_sliced
glob_loop
whole_solution_fallback
syntax_error
```

## Fact Slicing

The facts in import-stage Kramabench tasks are made from the upstream reference
solutions:

```text
other-benchmarks/Kramabench/solutions/<domain>/<task_id>.py
```

The slicer in `other-benchmarks/data-imports/kramabench/slicer.py` does a
conservative AST-based pass:

1. Parse the solution with Python `ast`.
2. Keep shared imports and shared path assignments.
3. For each workload file reference, search top-level solution statements for
   string literals matching the file name, basename, or glob prefix.
4. Emit the matched statements plus shared imports/helpers as that node's
   `fact`.
5. If the task uses multiple file refs, append the full upstream solution as a
   terminal integration tail so cross-file computations are not lost.
6. If the slicer cannot find a reliable per-file statement, keep the full
   solution and mark that node as `whole_solution_fallback`.

This means the import-stage facts are not always fair final benchmark facts.
They are traceable import facts. Some include answer-bearing upstream solution
logic, especially when an integration tail is attached.

## Hard Mini Import

Updated:

```text
other-benchmarks/data-imports/_shared/sample_hard.py
```

The shared sampler now has a `kramabench_mini()` path. It copies all imported
Kramabench tasks whose provenance difficulty is `hard`.

Output:

```text
other-benchmarks/tasks-kramabench-mini/
```

Current generated count:

```text
62 task_*.json files
```

The mini import preserves the same import bucket grammar:

```text
k-<hops>-d-<declared_datasets>-j-<difficulty>-f-<fanout>
```

Every copied mini task gets:

```text
_provenance.sample_source
```

## Five-Task Promotion Sample

This section is historical. The current direction is the raw-all candidate list
and batched skill-driven promotion under `./tasks-mini-kramabench/`; the
five-task script is not the path for the 104-task run.

Created:

```text
other-benchmarks/data-imports/kramabench/promote_sample.py
```

This script originally promoted five curated hard Kramabench mini tasks into a
more LakeQA-like `k-d` sample. That first version used the full domain data
pool and was superseded by a later `dr-input`-strict version. The 104-task plan
now supersedes both.

The later sample script version enforced per-task `dr-input` truth:

```text
other-benchmarks/Kramabench/dr-input/<domain>/<source_id>/
```

Its default output was the final top-level directory:

```text
tasks-mini-kramabench/
```

That script skips candidates whose bundle is missing or incomplete and writes
the reason to:

```text
tasks-mini-kramabench/error_log.json
```

Input:

```text
other-benchmarks/tasks-kramabench-mini/
```

Superseded sample output:

```text
other-benchmarks/tasks-kramabench-promoted-sample/
```

Generated sample count:

```text
5 task_*.json files
```

Promoted sample buckets:

```text
k-1-d-1: 2 tasks
k-2-d-1: 3 tasks
```

The original five curated source ids were:

```text
biomedical-hard-3
biomedical-hard-4
biomedical-hard-7
legal-hard-6
legal-hard-7
```

Under per-task truth, only candidates with complete task bundles can be
promoted. In the original five:

```text
biomedical-hard-3: skipped, missing dr-input bundle
biomedical-hard-4: skipped, missing dr-input bundle
biomedical-hard-7: skipped, missing dr-input bundle
legal-hard-6: skipped, bundle exists but lacks 2024_CSN_Top_Three_Identity_Theft_Reports_by_Year.csv
legal-hard-7: promotable, bundle contains 2024_CSN_Top_Three_Identity_Theft_Reports_by_Year.csv
```

The promotion script rewrites promotable tasks by hand into fairer executable
nodes:

```text
question ends with "Write your answer as [ANSWER]."
node facts execute locally and print exactly node.answer
datasets_used uses task-bundle dataset ids such as kramabench-legal-hard-7
_provenance.original_bucket_axes preserves the import-stage k-d-j-f axes
_provenance.dr_input_bundle records the task-local input bundle
_provenance.promotion_status = verified_sample
_provenance.promotion_rule = curated_kramabench_dr_input_sample_v1
```

Example collapse:

```text
biomedical-hard-4
from: other-benchmarks/tasks-kramabench-mini/k-3-d-2-j-3-f-2/task_1.json
to:   other-benchmarks/tasks-kramabench-promoted-sample/k-2-d-1/task_2.json
```

This answers the earlier `k-d-j-f` to `k-d` question for the sample path:

```text
import-stage k-d-j-f = provenance / source import metadata
promoted k-d = actual task topology for runs
```

The stale top-level `./tasks-mini-kramabench/` directory created from the
full-data promotion was removed after this correction.

## S3 Pilot Upload Script

Created a tracked script:

```text
scripts/upload_kramabench_sample_to_s3.py
```

Created tests:

```text
test/test_kramabench_s3_upload.py
```

The script receives a bucket URI:

```bash
python scripts/upload_kramabench_sample_to_s3.py --bucket-uri s3://kramabench
```

It also supports prefixes:

```bash
python scripts/upload_kramabench_sample_to_s3.py --bucket-uri s3://kramabench/pilot
```

The script originally staged three full-data-derived pilot objects. It now
stages files directly from per-task `dr-input` bundles. By default it stages
the currently promotable sample bundle:

```text
s3://kramabench/datagov/kramabench-legal-hard-7/files/...
```

Local source bundle:

```text
other-benchmarks/Kramabench/dr-input/legal/legal-hard-7/
```

Materialization behavior:

```text
copy task-bundle files byte-for-byte into datagov/kramabench-<source_id>/files/
```

The script supports:

```text
--dry-run
--staging-dir
--dr-input-root
--source-id
--uploader auto
--uploader boto3
--uploader aws-cli
```

The `aws-cli` uploader path was added because the bundled Python runtime can
read Excel with `pandas`/`openpyxl`, while this local environment may not have
`boto3` installed in that same runtime.

Dry run command used:

```bash
/Users/austinsenna/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/upload_kramabench_sample_to_s3.py --bucket-uri s3://kramabench --staging-dir /tmp/kramabench-s3-pilot-dry-run --uploader aws-cli --dry-run
```

Real upload command:

```bash
/Users/austinsenna/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/upload_kramabench_sample_to_s3.py --bucket-uri s3://kramabench --uploader aws-cli
```

I did not run the real upload.

## Superseded Direct dr-input Candidate List

Created a tracked sampler:

```text
scripts/build_kramabench_dr_candidate_list.py
```

Created tests:

```text
test/test_kramabench_direct_candidate_list.py
```

This sampler bypasses the older `k-d-j-f` import inventory. It reads raw
Kramabench workload files directly and keeps only tasks matching:

```text
difficulty == hard
normalized top-level data_sources >= 3
len(subtasks) <= 6
dr-input/<domain>/<source_id>/ exists
every required file ref is present in the dr-input bundle by relative path or basename
```

Command:

```bash
python scripts/build_kramabench_dr_candidate_list.py \
  --output-root tasks-mini-kramabench \
  --target-count 135 \
  --min-datasets 3 \
  --max-subtasks 6 \
  --seed 20260514
```

Output:

```text
tasks-mini-kramabench/candidate_list.json
tasks-mini-kramabench/candidates/environment-hard-16.json
tasks-mini-kramabench/candidates/legal-hard-18.json
```

Observed result with the current local clone:

```text
target_count: 135
selected_count: 2
selection_mode: take_all_eligible_because_pool_smaller_than_target
```

Rejected counts:

```text
missing_dr_input_bundle: 3
missing_dr_input_file: 1
not_hard: 42
too_few_datasets: 22
too_many_subtasks: 34
```

This means the strict direct-dr rule does not currently produce a 135-task
pool. It produces two fully eligible candidates:

```text
environment-hard-16
legal-hard-18
```

This strict direct-dr list is retained as historical tooling only. It is not
the current path for the full Kramabench promotion run.

## Raw-All Candidate List

Created the current tracked sampler:

```text
scripts/build_kramabench_raw_candidate_list.py
```

Created tests:

```text
test/test_kramabench_raw_candidate_list.py
```

This sampler bypasses both the `k-d-j-f` import inventory and the strict
`dr-input` filter. It reads the six main Kramabench workload files directly and
emits one candidate per upstream task:

```text
archeology.json
astronomy.json
biomedical.json
environment.json
legal.json
wildfire.json
```

Command:

```bash
python scripts/build_kramabench_raw_candidate_list.py --output-root tasks-mini-kramabench
```

Output:

```text
tasks-mini-kramabench/candidate_list.json
tasks-mini-kramabench/candidates/<source_id>.json
tasks-mini-kramabench/error_log.json
```

Observed result with the current local clone:

```text
candidate_set: kramabench_raw_all_main_workload
candidate_version: kramabench_raw_all_v1
selection_mode: all_main_workload_no_filters
selected_count: 104
filters: {}
```

Domain counts:

```text
archeology: 12
astronomy: 12
biomedical: 9
environment: 20
legal: 30
wildfire: 21
```

Difficulty counts:

```text
easy: 42
hard: 62
```

Source-resolution status:

```text
ready: 84
needs_source_resolution: 20
```

Each candidate records:

```text
source_id
domain
difficulty
question
answer
subtask_count
normalized_data_sources
required_file_refs
raw_data_root
raw_data_files
raw_data_ref_matches
solution_path
solution_file_refs
solution_ref_matches
dr_input_bundle, if present
s3_mirror_prefix = datagov/kramabench-<source_id>/files/
task = original upstream workload object
```

This raw-all candidate list is now the source for `$kramabench-mini-transform`.

The old dr-input-only promoted sample and old dr-input skip errors were removed
from `tasks-mini-kramabench/` so the directory now contains a clean raw-all
promotion queue: 104 candidates plus an empty raw-all `error_log.json`.

## Promoter Skill

Updated the local Codex skill:

```text
.agents/skills/kramabench-mini-transform/SKILL.md
.agents/skills/kramabench-mini-transform/agents/openai.yaml
```

The skill now says the active promotion path is:

```text
tasks-mini-kramabench/candidates/<source_id>.json
  -> tasks-mini-kramabench/k-*-d-*/task_N.json
```

It explicitly points workers at an existing LakeQA exemplar:

```text
tasks_mini/k-5-d-1/
```

Final bucket definitions in the skill are:

```text
k = number of reasoning hops in the final promoted task
d = max(len(hop["node_ids"]) for hop in reasoning_hops)
```

The skill now requires the all-104 raw candidate list:

```text
candidate_set: kramabench_raw_all_main_workload
filters: {}
```

and records raw source provenance:

```text
raw_data_root = other-benchmarks/Kramabench/data/<domain>/input
s3_mirror_prefix = datagov/kramabench-<source_id>/files/
promotion_rule = curated_kramabench_raw_all_batch_v1
```

The older `dr-input` candidate list is mentioned only as a historical path, not
as the active promotion contract.

## Design Notes Written

Created:

```text
docs/superpower/2026-05-13-kramabench-import-lakeqa-shaped.md
docs/superpower/2026-05-13-kramabench-local-tools-design.md
```

The first document captures the original import plan and the LakeQA-shaped
mapping. Some early text in that document refers to a simpler `k-d` import
layout; the implementation was later changed to the four-axis `k-d-j-f` layout
described above.

The second document captures a local Kramabench tool design with:

```text
search_kramabench(query, top_k=10, domain=None)
search_kramabench_schema(query, top_k=10, domain=None)
peek_file
read_file
grep_file
query_file
download
execute_code
submit_answer
```

That local-tool design was not implemented. It was superseded by the decision
to mirror Kramabench into `s3://kramabench` and reuse the existing S3 tooling.

## Tests Added

Created:

```text
test/test_kramabench_import.py
test/test_kramabench_promotion.py
test/test_kramabench_s3_upload.py
test/test_kramabench_direct_candidate_list.py
test/test_kramabench_raw_candidate_list.py
```

The import tests assert:

```text
converter emits 104 tasks
every output bucket matches k-*-d-*-j-*-f-*
bucket axes match _provenance.bucket_axes
k == len(reasoning_hops)
d == len(_provenance.normalized_data_sources)
j matches parsed difficulty
f == max hop fanout
legal glob sources are preserved and marked glob_loop
kramabench-mini keeps only hard tasks and preserves k-d-j-f dirs
```

The historical promotion tests assert:

```text
only candidates backed by complete per-task dr-input bundles are promoted
skipped candidates are recorded in error_log.json
promoted buckets use k-d only
j and f do not appear in promoted bucket names
each promoted node fact executes and prints node.answer
facts read dr-input paths, not other-benchmarks/Kramabench/data paths
legal-hard-7 collapses from k-7-d-1-j-3-f-1 to k-1-d-1
```

The raw-all candidate-list tests assert:

```text
candidate_list.json contains all 104 main workload tasks
candidate_set == kramabench_raw_all_main_workload
selection_mode == all_main_workload_no_filters
filters == {}
every candidate_path exists
each candidate records raw_data_root, source_id, task.id, and s3_mirror_prefix
sample source ids include biomedical-hard-8, wildfire-hard-21, environment-easy-1
```

The S3 tests assert:

```text
s3://bucket and s3://bucket/prefix parse correctly
per-task dr-input bundle files materialize without contacting S3
materialized files preserve raw bundle contents
S3 keys use datagov/kramabench-<source_id>/files/...
injected S3 clients receive the right bucket/key calls
aws-cli upload mode emits aws s3 cp commands
```

## Verification Commands

Focused S3 verification run:

```bash
/Users/austinsenna/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest test.test_kramabench_s3_upload -v
```

Observed result:

```text
Ran 4 tests
OK
```

S3 dry run:

```bash
/Users/austinsenna/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/upload_kramabench_sample_to_s3.py --bucket-uri s3://kramabench --staging-dir /tmp/kramabench-s3-pilot-dry-run --uploader aws-cli --dry-run
```

Observed dry-run targets:

```text
s3://kramabench/datagov/kramabench-legal-hard-7/files/...
```

Earlier import/promotion tests were authored and used while building the local
Kramabench import and five-task promotion sample:

```bash
python -m unittest test.test_kramabench_import -v
python -m unittest test.test_kramabench_promotion -v
```

Raw-all candidate-list verification:

```bash
python3 -m unittest test.test_kramabench_raw_candidate_list -v
```

Observed result:

```text
Ran 1 test
OK
```

## Open Work

The S3 upload script currently uploads selected per-task `dr-input` bundles. It
does not yet mirror the raw-all per-task object layout for all 104 candidates.

The raw-all candidate list exists, but the 104 final LakeQA-style tasks have
not all been promoted yet. Promotion should happen through
`$kramabench-mini-transform` in batches of five workers, writing final tasks to:

```text
tasks-mini-kramabench/k-*-d-*/
```

and unpromotable tasks to:

```text
tasks-mini-kramabench/error_log.json
```

The old promoted five-task sample under:

```text
other-benchmarks/tasks-kramabench-promoted-sample/
```

is superseded by the direct raw-all candidate path.

The Kramabench local-tool design was documented but not implemented.

The import-stage facts are traceable to upstream solutions, but they are not
all fair final benchmark facts. The promotion step is where fairness is curated
and verified.

The S3 bucket was not written by me in this session; only the dry run was
executed.
