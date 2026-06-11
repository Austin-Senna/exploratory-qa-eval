# Dataindexing Package Design

## Context

The repository owns maintained benchmark artifacts under `benchmarks/{benchmark}/tasks-mini/artifacts`, but the artifact generation and hybrid-search index building code currently lives in the sibling `tools-for-lakeagent` repository. The relevant existing generators are:

- `s3_loader/parquet_writer.py`: builds a document parquet cache from S3-backed table schema metadata.
- `s3_loader/parquet_to_description.py`: builds `table_descriptions.jsonl` and optional `table_descriptions.parquet` from parquet or manifest inputs.
- `hybrid_search/kramabench_extractor.py`: extracts Kramabench source files into table parquet, schema JSONL, manifest JSONL, copied local tables, and a report.
- `hybrid_search/process.py`: builds the LanceDB hybrid search index from parquet, descriptions, and schema metadata.
- `hybrid_search/api.py`: exposes the runtime search API used by SANA search tools.

SANA search wrappers currently import the runtime API through a `sys.path` insertion pointed at `external-tools/hybrid_search/api.py`. The new package must replace that path-level dependency with a normal package import while preserving the runtime API symbols.

## Goals

Create a root-level `dataindexing/` package that owns artifact generation, hybrid-index construction, and runtime search exports.

The package should:

- Preserve the current data flow from source manifests/S3 to parquet, descriptions, schemas, and LanceDB indexes.
- Keep expensive offline builders separate from normal SANA runtime evaluation code.
- Provide importable modules with thin CLI entrypoints.
- Export the runtime hybrid-search API needed by `sana_evaluation.tools.external.search_standard_tools` and `sana_evaluation.tools.external.search_naive_tools`.
- Keep current artifact row contracts compatible with existing benchmark artifact consumers.

## Non-Goals

This design does not replace `sana_evaluation.artifacts`, benchmark task formats, or ideal-search enrichment artifacts. It also does not redesign the search ranking algorithm, embedding presets, LanceDB table names, or Kramabench task conversion logic.

## Package Layout

```text
dataindexing/
  README.md
  __init__.py

  cli/
    __init__.py
    to_parquet.py
    parquet_to_description.py
    extract_kramabench_tables.py
    build_hybrid_search.py

  sources/
    __init__.py
    s3.py
    manifests.py
    parquet_cache.py
    kramabench.py

  descriptions/
    __init__.py
    generator.py
    prompts.py
    pricing.py
    rows.py

  hybrid_search/
    __init__.py
    api.py
    builder.py
    config.py
    embeddings.py
    text_builders.py
    uri_matching.py

  schemas/
    __init__.py
    table_schemas.py

  tests/
    test_descriptions.py
    test_hybrid_text_builders.py
    test_uri_matching.py
    test_kramabench_extractor.py
```

## Module Responsibilities

### CLI

The `dataindexing.cli` modules should only parse arguments and call importable package functions. Target commands:

```bash
python -m dataindexing.cli.to_parquet ...
python -m dataindexing.cli.parquet_to_description ...
python -m dataindexing.cli.extract_kramabench_tables ...
python -m dataindexing.cli.build_hybrid_search ...
```

### Source Adapters

`dataindexing.sources` owns input normalization and source extraction:

- `s3.py`: S3 config, URI parsing, bounded async fetch, file skipping helpers.
- `manifests.py`: plain-text and JSONL manifest readers.
- `parquet_cache.py`: parquet row iteration and description parquet loading helpers.
- `kramabench.py`: Kramabench source-ref collection and local table extraction.

The Kramabench adapter should preserve current outputs:

- `kramabench_tables.parquet`
- `kramabench_table_schemas.jsonl`
- `kramabench_table_manifest.jsonl`
- `kramabench_extract_report.json`
- copied local table files under a tables directory

### Description Artifacts

`dataindexing.descriptions` owns prompt construction, optional OpenAI inference, no-inference fallbacks, retry-error filtering, row validation, JSONL output, and optional parquet output.

The description row contract remains:

```text
dataset_uri
metadata
content
original_metadata
generated_metadata
description
input_tokens
output_tokens
input_cost_usd
output_cost_usd
cost_usd
error
```

`descriptions.rows` should centralize row construction and compatibility validation so runtime consumers and tests do not duplicate assumptions.

### Hybrid Search Builder

`dataindexing.hybrid_search.builder` owns offline LanceDB construction. It should preserve:

- content table name: `lakeqa`
- schema table name: `lakeqa_schema`
- `infused` and `basic` build modes
- description chunks only in `infused` mode
- schema text construction from generated metadata, original metadata, URI metadata, and tokenized columns according to mode
- FTS and ANN index construction

`text_builders.py` should contain testable pure functions such as schema-text construction, description chunk construction, column-name tokenization, and document chunking.

`uri_matching.py` should contain S3 URI normalization and schema lookup-key matching. The current behavior of stripping any bucket prefix, removing `/v1/`, and dropping extensions must be preserved.

### Runtime Search API Exports

`dataindexing.hybrid_search.api` must export the runtime functions currently provided by `tools-for-lakeagent/hybrid_search/api.py`:

```python
cfg
setup_hybrid()
setup_sparse()
hybrid_search()
hybrid_search_schema()
hybrid_search_with_reranker()
sparse_search()
sparse_search_schema()
vector_search()
get_connection()
get_table()
get_schema_table()
```

The SANA wrappers should import the API with:

```python
from dataindexing.hybrid_search import api as _api
```

This replaces the current `sys.path` insertion into `external-tools/hybrid_search`. During migration, a short fallback can be kept if needed, but the target state is package imports only.

## Data Flows

Generic LakeQA/Data.gov indexing:

```text
schema JSONL / S3 manifest
  -> dataindexing.cli.to_parquet
  -> document parquet
  -> dataindexing.cli.parquet_to_description
  -> descriptions JSONL/parquet
  -> dataindexing.cli.build_hybrid_search
  -> LanceDB index
```

Kramabench indexing:

```text
tasks/plans/source-list + local Kramabench raw data
  -> dataindexing.cli.extract_kramabench_tables
  -> parquet + schemas + manifest + report + copied tables
  -> dataindexing.cli.parquet_to_description
  -> descriptions JSONL/parquet
  -> dataindexing.cli.build_hybrid_search
  -> LanceDB index
```

Runtime search:

```text
sana_evaluation.tools.external.search_* wrappers
  -> dataindexing.hybrid_search.api
  -> LanceDB tables
```

## Error Handling

Builder CLIs should fail fast for explicitly provided missing paths. Optional/default artifact paths may warn when absent only if the selected mode can run without them.

Description generation should preserve row-level errors in JSONL and exclude failed or empty-content rows from parquet output.

Hybrid index building should raise when `--descriptions` or `--schemas` is explicitly provided but loads zero usable records.

Kramabench extraction should write a report with skipped sources, parse errors, written table counts, and output paths even when some sources fail.

## Testing

Focused tests should cover:

- Description row building, JSON parsing fallback, retry-error filtering, and Kramabench manifest no-inference behavior.
- URI normalization for arbitrary S3 buckets, `/v1/` removal, and extension stripping.
- `basic` versus `infused` schema-text and description-chunk behavior.
- Runtime search wrapper imports from `dataindexing.hybrid_search.api`.
- Kramabench extraction for CSV parsing, local path resolution, schema writing, parquet writing, and manifest writing.

Heavy integration tests that require S3, OpenAI, embeddings, GPU, or LanceDB index construction should remain opt-in.

## Migration Steps

1. Add the `dataindexing/` package skeleton.
2. Port pure helpers and tests first: URI matching, schema text, description rows, manifest readers.
3. Port description generator and Kramabench extractor behind importable functions plus thin CLIs.
4. Port the hybrid index builder and runtime `api.py`.
5. Update `sana_evaluation.tools.external.search_standard_tools` and `search_naive_tools` to import `dataindexing.hybrid_search.api`.
6. Update smoke tests to patch the new package API.
7. Add README runbook commands for LakeQA/Data.gov and Kramabench index generation.

## Open Decisions

No unresolved design blockers remain. Implementation may choose a temporary compatibility fallback for the old external-tools import path if local environments still depend on it, but the intended final dependency is the root-level `dataindexing` package.
