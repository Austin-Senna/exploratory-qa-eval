"""Compatibility profile-enriched peek tools.

The baseline `strands_evaluation` peek tools are profile-aware now. This module
remains import-compatible for older SANA callers and tests.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from strands import tool
from strands_evaluation.helper.peek_profile import select_dataset_profile_fields
from strands_evaluation.tools.agent_tools_v2 import peek_file as _baseline_peek_file

from sana_evaluation.helper.peek_profile import load_dataset_profile


# The strands @tool decorator wraps the original function; access the bare
# callable so we can call it directly without going through the tool runtime.
_baseline_peek_file_impl = _baseline_peek_file._tool_func


@tool
def peek_file(
    dataset_id: str | None = None,
    file_path: str | None = None,
    max_rows: int = 20,
    s3_uri: str | None = None,
) -> Dict[str, Any]:
    """
    Inspect a SINGLE file via a budget range-GET. Returns the content family
    (csv/json/xml/text), column headers or XML tags/schema hints, and a
    preview — no full download.

    USE THIS for one file at a time. For multiple files in one call, use
    `peek_multiple` instead (different signature: takes a `files` list).

    Prefer `s3_uri` when search/preloaded results gave you one; it is less
    error-prone than reconstructing dataset_id + file_path. For datagov files,
    both "rows.txt" and "files/rows.txt" are accepted, but "files/rows.txt" is
    the canonical path.

    Args:
        dataset_id: ONE dataset identifier as a bare string, e.g. "Barack_Obama"
        file_path:  ONE relative path within the dataset, e.g. "files/data.txt"
        s3_uri:     Optional full object URI instead of dataset_id/file_path
        max_rows:   Maximum preview rows to include (default 20)

    Example call:
        peek_file(dataset_id="index-crimes-by-county", file_path="files/rows.txt")

    Returns:
        Dict with keys: family, preview_text, header_columns, row_count_estimate,
        size_bytes, dataset_id, file_path. XML previews may also include
        xml_root_tag, xml_namespaces, xml_schema_fields,
        xml_record_tag_candidates, xml_preview_mode.

        May also include a `profile` field with selected cached metadata for
        the dataset: `family`, `schema_status`, `schema_error`, `columns`
        as name/type pairs, `llm_description`, `snippet`, `row_count`,
        `size_bytes`, and `top_2_rows`.

        On error: {error: ...}
    """
    result = _baseline_peek_file_impl(
        dataset_id=dataset_id,
        file_path=file_path,
        max_rows=max_rows,
        s3_uri=s3_uri,
    )
    if isinstance(result, dict) and "error" not in result:
        uri = result.get("s3_uri")
        if uri:
            try:
                profile = load_dataset_profile(uri)
            except Exception:
                profile = None
            profile = select_dataset_profile_fields(profile)
            if profile is not None:
                result["profile"] = profile
    return result


@tool
def peek_multiple(
    files: Optional[List[Dict[str, str]]] = None,
    entries: Optional[List[Dict[str, str]]] = None,
    max_rows: int = 20,
) -> Dict[str, Any]:
    """
    Inspect SEVERAL files in ONE call — a batch wrapper around enriched
    peek_file.

    USE THIS when you already know which 2+ files you need. For a single file,
    use `peek_file` instead — its signature is simpler.

    Prefer per-entry `s3_uri` when search/preloaded results gave you one.

    REQUIRED ARGUMENT SHAPE: pass a `files` list of dicts, NOT top-level
    `dataset_id`/`file_path`:

        peek_multiple(files=[
            {"dataset_id": "census-2021", "file_path": "files/rows.txt"},
            {"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/x/files/y.txt"},
        ])

    Args:
        files:    NON-EMPTY list of dicts. Each dict needs 'dataset_id' and
                  'file_path'. The key 'path' is accepted as an alias for
                  'file_path'. A per-entry `s3_uri` is also accepted.
        entries:  Alias for `files`.
        max_rows: Maximum preview rows per file (default 20).

    Returns:
        Dict with `results` list and `count`. Each result has the same shape as
        peek_file and may include a `profile` field with selected cached
        metadata such as family, schema_status, schema_error, columns as
        name/type pairs, llm_description, snippet, row_count, size_bytes,
        and top_2_rows.

        On error: {error: ...}
    """
    if files is None and entries is not None:
        files = entries
    if isinstance(files, dict):
        files = [files]
    if not isinstance(files, list) or not files:
        return {
            "error": (
                "peek_multiple requires a non-empty `files` list of "
                "{dataset_id, file_path} dicts. Use peek_multiple for 2+ files "
                "when you already know the exact files, or peek_file(dataset_id, file_path) for one "
                "file. Example: "
                'peek_multiple(files=[{"dataset_id": "census", "file_path": "files/rows.txt"}], max_rows=5)'
            )
        }

    results = []
    for spec in files:
        if isinstance(spec, str):
            results.append(peek_file._tool_func(s3_uri=spec, max_rows=max_rows))
            continue
        if not isinstance(spec, dict):
            results.append({"error": "each entry must be a dict with dataset_id/file_path or s3_uri"})
            continue
        ds = spec.get("dataset_id", "")
        fp = spec.get("file_path") or spec.get("path") or ""
        uri = spec.get("s3_uri") or spec.get("uri") or ""
        results.append(
            peek_file._tool_func(
                dataset_id=ds,
                file_path=fp,
                max_rows=max_rows,
                s3_uri=uri,
            )
        )

    return {"results": results, "count": len(results)}


__all__ = ["peek_file", "peek_multiple"]
