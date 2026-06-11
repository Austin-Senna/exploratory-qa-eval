# Dataindexing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a root-level `dataindexing/` package that owns artifact generation, hybrid-search index construction, and runtime search API exports used by SANA search tools.

**Architecture:** Port the existing sibling `tools-for-lakeagent` generators into focused importable modules, with thin CLI entrypoints and tests around pure behavior. Runtime wrappers in `sana_evaluation.tools.external` will import `dataindexing.hybrid_search.api` instead of manipulating `sys.path`.

**Tech Stack:** Python 3.12, pytest, pyarrow, pandas, aioboto3/boto3, OpenAI SDK, LanceDB, sentence-transformers/torch.

---

## File Structure

- Create `dataindexing/` package root and subpackages `cli`, `sources`, `descriptions`, `hybrid_search`, and `schemas`.
- Create `dataindexing/sources/parquet_cache.py` from the existing parquet/description/schema loaders.
- Create `dataindexing/descriptions/generator.py`, `prompts.py`, `pricing.py`, and `rows.py` from the current description pipeline.
- Create `dataindexing/sources/kramabench.py` from the current Kramabench extractor.
- Create `dataindexing/hybrid_search/config.py`, `embeddings.py`, `text_builders.py`, `uri_matching.py`, `builder.py`, and `api.py` from current hybrid search modules.
- Create thin CLIs under `dataindexing/cli/`.
- Modify `sana_evaluation/tools/external/search_standard_tools.py` and `search_naive_tools.py` to import the new runtime API.
- Add focused tests under `test/` for the new package import paths and migrated behavior.
- Add `dataindexing/README.md` with runbook commands.

### Task 1: Package Skeleton and Pure URI/Text Helpers

**Files:**
- Create: `dataindexing/__init__.py`
- Create: `dataindexing/hybrid_search/__init__.py`
- Create: `dataindexing/hybrid_search/uri_matching.py`
- Create: `dataindexing/hybrid_search/text_builders.py`
- Test: `test/test_dataindexing_hybrid_helpers.py`

- [ ] **Step 1: Write failing tests**

```python
from dataindexing.hybrid_search.text_builders import (
    build_description_chunk,
    build_schema_text,
    tokenize_column_name,
)
from dataindexing.hybrid_search.uri_matching import uri_to_schema_stem


def test_uri_to_schema_stem_strips_bucket_v1_and_extension():
    assert uri_to_schema_stem("s3://bucket/datagov/foo/v1/files/rows.csv") == "datagov/foo/files/rows"


def test_basic_and_infused_text_builders_preserve_mode_boundaries():
    desc = {
        "generated_metadata": "Generated metadata",
        "description": "Generated description",
        "original_metadata": "original uri words",
    }
    infused = build_schema_text(
        build_mode="infused",
        uri="s3://bucket/datagov/example/files/rows.txt",
        doc="fallback raw words",
        desc_row=desc,
        schema_cols=["PermitNumber", "agency_name"],
    )
    basic = build_schema_text(
        build_mode="basic",
        uri="s3://bucket/datagov/example/files/rows.txt",
        doc="fallback raw words",
        desc_row=desc,
        schema_cols=["PermitNumber", "agency_name"],
    )
    assert "Generated metadata" in infused
    assert "Generated description" not in infused
    assert "original uri words" in infused
    assert "Generated metadata" not in basic
    assert "datagov example files rows" in basic
    assert tokenize_column_name("PermitNumber") == "Permit Number"
    assert build_description_chunk("infused", desc) == "Generated metadata Generated description"
    assert build_description_chunk("basic", desc) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_dataindexing_hybrid_helpers.py -q`

Expected: FAIL because `dataindexing` does not exist.

- [ ] **Step 3: Implement helpers**

Implement `uri_to_schema_stem`, `metadata_from_uri`, `tokenize_column_name`, `build_schema_text`, and `build_description_chunk` by porting current behavior from `tools-for-lakeagent/hybrid_search/process.py`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/test_dataindexing_hybrid_helpers.py -q`

Expected: PASS.

### Task 2: Source, Schema, and Description Row Utilities

**Files:**
- Create: `dataindexing/sources/__init__.py`
- Create: `dataindexing/sources/parquet_cache.py`
- Create: `dataindexing/schemas/__init__.py`
- Create: `dataindexing/schemas/table_schemas.py`
- Create: `dataindexing/descriptions/__init__.py`
- Create: `dataindexing/descriptions/rows.py`
- Test: `test/test_dataindexing_description_rows.py`

- [ ] **Step 1: Write failing tests**

```python
import json
from pathlib import Path

from dataindexing.descriptions.rows import build_row
from dataindexing.sources.parquet_cache import load_descriptions_full


def test_build_row_normalizes_text_and_content():
    row = build_row(
        dataset_uri="s3://bucket/data.csv",
        original_metadata="original   metadata",
        generated_metadata="generated   metadata",
        description="short   description",
    )
    assert row["metadata"] == "generated metadata"
    assert row["content"] == "generated metadata short description"
    assert row["error"] is None


def test_load_descriptions_full_jsonl_skips_error_rows(tmp_path: Path):
    path = tmp_path / "descriptions.jsonl"
    path.write_text(
        json.dumps({"dataset_uri": "s3://bucket/ok.csv", "generated_metadata": "meta", "description": "desc", "original_metadata": "orig", "error": None})
        + "\n"
        + json.dumps({"dataset_uri": "s3://bucket/bad.csv", "generated_metadata": "bad", "description": "bad", "original_metadata": "bad", "error": "failed"})
        + "\n"
    )
    assert load_descriptions_full(str(path)) == {
        "s3://bucket/ok.csv": {
            "generated_metadata": "meta",
            "description": "desc",
            "original_metadata": "orig",
        }
    }
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_dataindexing_description_rows.py -q`

Expected: FAIL because modules do not exist.

- [ ] **Step 3: Implement utilities**

Port `build_row`, `compose_content`, parquet description loaders, parquet record iteration, and table schema loading into the new package.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/test_dataindexing_description_rows.py -q`

Expected: PASS.

### Task 3: Port Description Generator and Kramabench Extractor

**Files:**
- Create: `dataindexing/descriptions/prompts.py`
- Create: `dataindexing/descriptions/pricing.py`
- Create: `dataindexing/descriptions/generator.py`
- Create: `dataindexing/sources/kramabench.py`
- Create: `dataindexing/cli/parquet_to_description.py`
- Create: `dataindexing/cli/extract_kramabench_tables.py`
- Test: `test/test_dataindexing_descriptions_and_kramabench.py`

- [ ] **Step 1: Write failing tests**

Port the current focused tests from `tools-for-lakeagent/s3_loader/test_kramabench_descriptions.py` and `hybrid_search/tests/test_kramabench_extractor.py` for:

- auto-detecting Kramabench manifest JSONL
- Kramabench no-inference description output
- retry-error filtering
- CSV extraction writing parquet, schemas, manifest, report, and copied table files

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_dataindexing_descriptions_and_kramabench.py -q`

Expected: FAIL because generator and Kramabench modules are not implemented.

- [ ] **Step 3: Implement generator and extractor**

Port the existing generator and extractor code. Update imports to use `dataindexing.sources.parquet_cache`, `dataindexing.descriptions.rows`, and package-local helpers.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/test_dataindexing_descriptions_and_kramabench.py -q`

Expected: PASS.

### Task 4: Port Hybrid Builder, Runtime API, and CLIs

**Files:**
- Create: `dataindexing/hybrid_search/config.py`
- Create: `dataindexing/hybrid_search/embeddings.py`
- Create: `dataindexing/hybrid_search/builder.py`
- Create: `dataindexing/hybrid_search/api.py`
- Create: `dataindexing/cli/build_hybrid_search.py`
- Create: `dataindexing/cli/to_parquet.py`
- Create: `dataindexing/sources/s3.py`
- Create: `dataindexing/sources/manifests.py`
- Test: `test/test_dataindexing_runtime_api_imports.py`

- [ ] **Step 1: Write failing tests**

```python
from dataindexing.hybrid_search import api


def test_runtime_api_exports_expected_symbols():
    for name in (
        "cfg",
        "setup_hybrid",
        "setup_sparse",
        "hybrid_search",
        "hybrid_search_schema",
        "hybrid_search_with_reranker",
        "sparse_search",
        "sparse_search_schema",
        "vector_search",
        "get_connection",
        "get_table",
        "get_schema_table",
    ):
        assert hasattr(api, name)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_dataindexing_runtime_api_imports.py -q`

Expected: FAIL because `api.py` is not implemented.

- [ ] **Step 3: Implement runtime API and builders**

Port `hybrid_search/api.py`, `config.py`, `embedding_utils.py`, `process.py`, `s3_loader/config.py`, `s3_loader/streams.py`, and `s3_loader/parquet_writer.py` behavior into package modules. Keep heavy imports lazy where possible to avoid import-time GPU/model setup.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/test_dataindexing_runtime_api_imports.py -q`

Expected: PASS without connecting to LanceDB or loading embedding models.

### Task 5: Switch SANA Search Wrappers to Package Imports

**Files:**
- Modify: `sana_evaluation/tools/external/search_standard_tools.py`
- Modify: `sana_evaluation/tools/external/search_naive_tools.py`
- Modify: `test/test_external_search_tools_smoke.py`

- [ ] **Step 1: Write or update tests**

Update smoke tests so patching still targets `search_standard_tools._api` and `search_naive_tools._api`, but assert the `_api.__name__` starts with `dataindexing.hybrid_search.api`.

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test/test_external_search_tools_smoke.py -q`

Expected: FAIL while wrappers still import through `external-tools`.

- [ ] **Step 3: Update wrapper imports**

Replace `sys.path.insert(... external-tools/hybrid_search)` and `import api as _api` with:

```python
from dataindexing.hybrid_search import api as _api
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test/test_external_search_tools_smoke.py -q`

Expected: PASS.

### Task 6: README and Verification

**Files:**
- Create: `dataindexing/README.md`
- Modify: none unless verification exposes import or docs gaps.

- [ ] **Step 1: Add README**

Document the LakeQA/Data.gov and Kramabench flows with the four CLI commands.

- [ ] **Step 2: Run focused verification**

Run:

```bash
pytest \
  test/test_dataindexing_hybrid_helpers.py \
  test/test_dataindexing_description_rows.py \
  test/test_dataindexing_descriptions_and_kramabench.py \
  test/test_dataindexing_runtime_api_imports.py \
  test/test_external_search_tools_smoke.py \
  -q
```

Expected: PASS.

- [ ] **Step 3: Check git diff**

Run: `git status --short`

Expected: new `dataindexing/` files, new focused tests, modified search wrappers, plan file, and no intentional edits to unrelated dirty files.
