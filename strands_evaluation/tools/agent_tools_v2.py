"""
Data Lake Access Tools v2 for LLM Agent

Improvements over v1 (agent_tools.py):
  - peek_file: range-GET + family detection + column headers (replaces inspect_file)
  - query_file: query S3 directly via DuckDB httpfs — no download needed
  - download_smart: budget-aware range-GET per content family, skips metadata/binary files
  - execute_code, search, search_keyword, list_files, get_sandbox_info, cleanup_sandbox: unchanged

Bucket: lakeqa-yc4103-datalake
Folders: wikipedia/, datagov/
"""

import os
import json
import re
import traceback
from typing import Any, Dict, List

import duckdb
from dotenv import load_dotenv
from strands import tool

from .agent_tools import (  # noqa: F401 — re-exported
    search,
    search_keyword,
    list_files,
    execute_code,
    download,
    get_sandbox_info,
    cleanup_sandbox,
    set_sandbox_dir,
    _get_s3_client,
    _get_sandbox_dir,
    _resolve_dataset_folder,
    BUCKET,
    REGION,
    SANDBOX_BASE_DIR,
)
from .helper.detect import detect_family, should_skip

load_dotenv()

# ---------------------------------------------------------------------------
# Budget constants (mirrored from streams.py S3Config defaults)
# ---------------------------------------------------------------------------
_PEEK_BYTES = 65_536          # 64 KB for initial range-GET / peek
_READ_BYTES = 1_048_576       # 1 MB budget for read_file / search_in_file
_MAX_CSV_ROWS = 500
_CSV_BYTES_PER_ROW = 512
_MAX_JSON_ITEMS = 200
_JSON_BYTES_PER_ITEM = 2_048
_MAX_TEXT_CHARS = 50_000
_QUERY_ROW_CAP = 200
_SEARCH_MAX_MATCHES = 20
_SEARCH_CONTEXT_LINES = 2


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _s3_range_get(s3, key: str, start: int, end: int) -> bytes:
    """Sync range-GET from the configured bucket."""
    resp = s3.get_object(Bucket=BUCKET, Key=key, Range=f"bytes={start}-{end}")
    return resp["Body"].read()


def _s3_head(s3, key: str) -> int:
    """Return file size in bytes via HeadObject."""
    meta = s3.head_object(Bucket=BUCKET, Key=key)
    return meta.get("ContentLength", 0)


def _duckdb_connection() -> duckdb.DuckDBPyConnection:
    """Create a fresh in-memory DuckDB connection with httpfs and AWS credentials."""
    conn = duckdb.connect(":memory:")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    aws_key = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    region = os.getenv("AWS_DEFAULT_REGION", REGION)
    conn.execute(f"SET s3_region='{region}'")
    if aws_key:
        conn.execute(f"SET s3_access_key_id='{aws_key}'")
    if aws_secret:
        conn.execute(f"SET s3_secret_access_key='{aws_secret}'")
    return conn


# ---------------------------------------------------------------------------
# Tool 1: peek_file
# ---------------------------------------------------------------------------

@tool
def peek_file(
    dataset_id: str,
    file_path: str,
    max_rows: int = 20,
) -> Dict[str, Any]:
    """
    Inspect a file with a budget range-GET: detects content family (csv/json/text),
    returns column headers and a preview without downloading the full file.

    Args:
        dataset_id: Dataset identifier (e.g. "Barack_Obama")
        file_path:  Relative path within the dataset (e.g. "table_0.csv")
        max_rows:   Maximum preview rows to include (default 20)

    Returns:
        Dict with keys: family, preview_text, header_columns, row_count_estimate,
        size_bytes, dataset_id, file_path. On error: {error: ...}
    """
    if not dataset_id:
        return {"error": "dataset_id is required"}
    if not file_path:
        return {"error": "file_path is required"}

    filename = file_path.rsplit("/", 1)[-1]
    if should_skip(filename):
        return {"error": f"File skipped (metadata/binary): {file_path}"}

    folder = _resolve_dataset_folder(dataset_id)
    if folder is None:
        return {"error": f"Dataset not found or ambiguous: {dataset_id}"}

    s3 = _get_s3_client()
    key = f"{folder}/{dataset_id}/{file_path.lstrip('/')}"

    try:
        size_bytes = _s3_head(s3, key)
    except Exception as e:
        return {"error": f"HeadObject failed: {e}"}

    end = min(_PEEK_BYTES - 1, size_bytes - 1)
    try:
        raw = _s3_range_get(s3, key, 0, end)
    except Exception as e:
        return {"error": f"Range-GET failed: {e}"}

    text = raw.decode("utf-8", errors="replace")
    family = detect_family(text)

    lines = [ln for ln in text.splitlines() if ln.strip()]
    preview_lines = lines[: max_rows + 1]  # +1 to include header for csv
    preview_text = "\n".join(preview_lines[:max_rows])

    result: Dict[str, Any] = {
        "dataset_id": dataset_id,
        "file_path": file_path,
        "size_bytes": size_bytes,
        "family": family,
        "preview_text": preview_text,
    }

    # Estimate row count from sampled bytes
    if size_bytes > 0 and end > 0:
        lines_in_sample = len(lines)
        bytes_per_line = (end + 1) / max(lines_in_sample, 1)
        result["row_count_estimate"] = int(size_bytes / bytes_per_line) if bytes_per_line > 0 else None
    else:
        result["row_count_estimate"] = len(lines)

    # CSV: extract header columns
    if family == "csv" and lines:
        header = lines[0]
        for delim in (",", "\t", "|", ";"):
            if delim in header:
                result["header_columns"] = [c.strip() for c in header.split(delim)]
                break

    # JSON: extract keys from first object
    if family == "json":
        try:
            first_obj = json.loads(lines[0]) if lines else None
            if isinstance(first_obj, dict):
                result["json_keys"] = sorted(first_obj.keys())
            elif isinstance(first_obj, list) and first_obj and isinstance(first_obj[0], dict):
                result["json_keys"] = sorted(first_obj[0].keys())
        except Exception:
            pass

    return result


# ---------------------------------------------------------------------------
# Tool 1b: peek_files (batch wrapper)
# ---------------------------------------------------------------------------

@tool
def peek_files(
    files: List[Dict[str, str]],
    max_rows: int = 20,
) -> Dict[str, Any]:
    """
    Inspect multiple files at once. Calls peek_file for each entry.

    Args:
        files:    List of dicts, each with 'dataset_id' and 'file_path'.
                  Example: [{"dataset_id": "census", "file_path": "files/data.txt"}]
        max_rows: Maximum preview rows per file (default 20)

    Returns:
        Dict with 'results' list (one entry per file, same shape as peek_file),
        and 'count'.
    """
    if not isinstance(files, list) or not files:
        return {"error": "files must be a non-empty list of {dataset_id, file_path} dicts"}

    results = []
    for spec in files:
        if not isinstance(spec, dict):
            results.append({"error": "each entry must be a dict with dataset_id and file_path"})
            continue
        ds = spec.get("dataset_id", "")
        fp = spec.get("file_path", "")
        results.append(peek_file(ds, fp, max_rows))

    return {"results": results, "count": len(results)}


# ---------------------------------------------------------------------------
# Tool 2: read_file
# ---------------------------------------------------------------------------

def _s3_fetch_text(dataset_id: str, file_path: str, max_bytes: int):
    """Fetch up to max_bytes of a file from S3 and return (text, size_bytes, truncated).

    Returns a tuple (text, size_bytes, truncated) or raises on error.
    """
    folder = _resolve_dataset_folder(dataset_id)
    if folder is None:
        raise ValueError(f"Dataset not found or ambiguous: {dataset_id}")
    s3 = _get_s3_client()
    key = f"{folder}/{dataset_id}/{file_path.lstrip('/')}"
    size_bytes = _s3_head(s3, key)
    end = min(max_bytes - 1, size_bytes - 1)
    raw = _s3_range_get(s3, key, 0, end)
    text = raw.decode("utf-8", errors="replace")
    truncated = size_bytes > max_bytes
    return text, size_bytes, truncated


@tool
def read_file(
    dataset_id: str,
    file_path: str,
    start_line: int = 0,
    max_lines: int = 200,
) -> Dict[str, Any]:
    """
    Read lines from a file in the data lake without downloading it.
    Use this to read text, CSV, or JSON files directly. Supports pagination
    via start_line for large files.

    Args:
        dataset_id: Dataset identifier (e.g. "census")
        file_path:  Relative path within the dataset (e.g. "files/data.txt")
        start_line: Line index to start reading from, 0-based (default 0)
        max_lines:  Number of lines to return, capped at 500 (default 200)
    """
    if not dataset_id or not file_path:
        return {"error": "dataset_id and file_path are required"}
    if start_line < 0:
        return {"error": "start_line must be >= 0"}

    max_lines = min(max_lines, 500)
    filename = file_path.rsplit("/", 1)[-1]
    if should_skip(filename):
        return {"error": f"File skipped (metadata/binary): {file_path}"}

    folder = _resolve_dataset_folder(dataset_id)
    if folder is None:
        return {"error": f"Dataset not found or ambiguous: {dataset_id}"}

    s3 = _get_s3_client()
    key = f"{folder}/{dataset_id}/{file_path.lstrip('/')}"
    
    try:
        # Open a streaming connection to the file
        resp = s3.get_object(Bucket=BUCKET, Key=key)
        line_iter = resp["Body"].iter_lines()
        
        lines = []
        current_line = 0

        # Skip lines until we hit the requested start_line
        for _ in range(start_line):
            try:
                next(line_iter)
                current_line += 1
            except StopIteration:
                break

        # Read the requested chunk
        for _ in range(max_lines):
            try:
                raw_line = next(line_iter)
                lines.append(raw_line.decode("utf-8", errors="replace"))
                current_line += 1
            except StopIteration:
                break
                
        # Close the stream explicitly to free the connection
        resp["Body"].close()
        
    except Exception as e:
        return {"error": f"Failed to stream file: {e}"}

    return {
        "dataset_id": dataset_id,
        "file_path": file_path,
        "start_line": start_line,
        "returned_lines": len(lines),
        "lines": lines,
    }


# ---------------------------------------------------------------------------
# Tool 3: search_in_file
# ---------------------------------------------------------------------------

@tool
def search_in_file(
    dataset_id: str,
    file_path: str,
    regex_pattern: str,
    context_lines: int = 2,
) -> Dict[str, Any]:
    """Search for a regex pattern inside a file over an S3 stream."""
    # ... (validation and S3 setup remains the same) ...
    if not dataset_id or not file_path or not regex_pattern:
        return {"error": "dataset_id, file_path, and regex_pattern are required"}

    context_lines = min(context_lines, 5)
    # filename = file_path.rsplit("/", 1)[-1]
    # if should_skip(filename):
    #     return {"error": f"File skipped (metadata/binary): {file_path}"}

    try:
        pattern = re.compile(regex_pattern, re.IGNORECASE)
    except re.error as e:
        return {"error": f"Invalid regex pattern: {e}"}

    folder = _resolve_dataset_folder(dataset_id)
    if folder is None:
        return {"error": f"Dataset not found: {dataset_id}"}

    s3 = _get_s3_client()
    key = f"{folder}/{dataset_id}/{file_path.lstrip('/')}"

    try:
        resp = s3.get_object(Bucket=BUCKET, Key=key)
        line_iter = resp["Body"].iter_lines()
        
        matches = []
        pending_matches = []
        # deque automatically pushes old lines out when it hits maxlen!
        history = deque(maxlen=context_lines) 

        for i, raw_line in enumerate(line_iter):
            line = raw_line.decode("utf-8", errors="replace")

            # 1. Fill the "after" context for any matches we found previously
            for m in pending_matches:
                if len(m["context_after"]) < context_lines:
                    m["context_after"].append(line)

            # 2. Move fully-populated matches into our final list
            completed = [m for m in pending_matches if len(m["context_after"]) == context_lines]
            for m in completed:
                matches.append(m)
                pending_matches.remove(m)
                
            if len(matches) >= _SEARCH_MAX_MATCHES:
                break

            # 3. Evaluate the CURRENT line for a new match
            if pattern.search(line):
                new_match = {
                    "line_number": i,
                    "line": line,
                    "context_before": list(history),  # Snapshot the current history
                    "context_after": []
                }
                if context_lines == 0:
                    matches.append(new_match)
                    if len(matches) >= _SEARCH_MAX_MATCHES:
                        break
                else:
                    pending_matches.append(new_match)

            # 4. Add current line to history for future matches
            history.append(line)

        # Catch any pending matches if we hit the end of the file early
        for m in pending_matches:
            if m not in matches:
                matches.append(m)

        resp["Body"].close()

    except Exception as e:
        return {"error": f"Stream search failed: {e}", "traceback": traceback.format_exc()}

    return {
        "dataset_id": dataset_id,
        "file_path": file_path,
        "match_count": len(matches),
        "truncated_matches": len(matches) >= _SEARCH_MAX_MATCHES,
        "matches": matches,
    }

# ---------------------------------------------------------------------------
# Tool 4: query_file
# ---------------------------------------------------------------------------

@tool
def query_file(
    dataset_id: str,
    file_path: str,
    sql: str,
) -> Dict[str, Any]:
    """
    Run a SQL query directly against an S3 file using DuckDB httpfs.
    No download required. The file is referenced as table alias 't'.

    Supported file types: CSV (.csv), JSON (.json, .jsonl, .ndjson).
    Results are capped at 200 rows.

    Args:
        dataset_id: Dataset identifier (e.g. "Barack_Obama")
        file_path:  Relative path within the dataset (e.g. "table_0.csv")
        sql:        SQL query. Use 't' as the table alias.
                    Example: "SELECT * FROM t LIMIT 10"
                    Example: "SELECT col1, COUNT(*) FROM t GROUP BY col1"

    Returns:
        Dict with keys: columns, rows, row_count, truncated. On error: {error: ...}
    """
    if not dataset_id:
        return {"error": "dataset_id is required"}
    if not file_path:
        return {"error": "file_path is required"}
    if not sql or not sql.strip():
        return {"error": "sql is required"}

    filename = file_path.rsplit("/", 1)[-1]
    if should_skip(filename):
        return {"error": f"File skipped (metadata/binary): {file_path}"}

    folder = _resolve_dataset_folder(dataset_id)
    if folder is None:
        return {"error": f"Dataset not found or ambiguous: {dataset_id}"}

    s3_uri = f"s3://{BUCKET}/{folder}/{dataset_id}/{file_path.lstrip('/')}"
    lower_path = file_path.lower()

    # Determine reader function
    if lower_path.endswith(".csv"):
        reader = f"read_csv_auto('{s3_uri}')"
    elif lower_path.endswith((".json", ".jsonl", ".ndjson")):
        reader = f"read_json_auto('{s3_uri}')"
    else:
        # Attempt to detect from a quick peek
        try:
            s3 = _get_s3_client()
            key = f"{folder}/{dataset_id}/{file_path.lstrip('/')}"
            size = _s3_head(s3, key)
            end = min(_PEEK_BYTES - 1, size - 1)
            raw = _s3_range_get(s3, key, 0, end)
            text = raw.decode("utf-8", errors="replace")
            family = detect_family(text)
        except Exception as e:
            return {"error": f"Could not detect file family: {e}"}

        if family == "csv":
            reader = f"read_csv_auto('{s3_uri}')"
        elif family == "json":
            reader = f"read_json_auto('{s3_uri}')"
        else:
            return {"error": f"File family '{family}' is not queryable with SQL"}

    try:
        conn = _duckdb_connection()
        # Create view aliased as 't'
        conn.execute(f"CREATE VIEW t AS SELECT * FROM {reader}")
        # Execute user SQL, cap rows
        rel = conn.execute(sql)
        rows = rel.fetchmany(_QUERY_ROW_CAP + 1)
        columns = [desc[0] for desc in rel.description]
        truncated = len(rows) > _QUERY_ROW_CAP
        if truncated:
            rows = rows[:_QUERY_ROW_CAP]
        return {
            "columns": columns,
            "rows": [list(r) for r in rows],
            "row_count": len(rows),
            "truncated": truncated,
        }
    except Exception as e:
        return {"error": f"Query failed: {e}", "traceback": traceback.format_exc()}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # v2-new
    "peek_file",
    "peek_files",
    "read_file",
    "search_in_file",
    "query_file",
    # re-exported from agent_tools
    "search",
    "search_keyword",
    "list_files",
    "execute_code",
    "get_sandbox_info",
    "cleanup_sandbox",
    "set_sandbox_dir",
    "download",
]
