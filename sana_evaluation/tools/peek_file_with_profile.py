"""SANA's profile-enriched peek_file.

Wraps the baseline `peek_file` tool from `strands_evaluation` and merges in a
`profile` field populated from the precomputed profile cache. When the
`results` SANA flag is on, this tool replaces the baseline `peek_file`
in the agent's tool list.

Baseline strands_evaluation has zero awareness of profiles — all enrichment
plumbing lives here in SANA.
"""

from __future__ import annotations

from typing import Any, Dict

from strands import tool
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

        May also include a `profile` field with cached metadata for the dataset:
        `schema_columns`, `table_kind`, `llm_description`, `snippet`. Some
        profiles also include `row_count`, `size_bytes`, `top_2_rows`, and
        per-column `null_rate`, `distinct_count`, `min`, `max`, `mean`. When
        present, prefer reading the profile fields before issuing query_file —
        they're cheaper than running a query.

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
            if profile is not None:
                result["profile"] = profile
    return result


__all__ = ["peek_file"]
