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

import base64
import datetime
import decimal
import json
import os
import re
import traceback
import uuid
import xml.etree.ElementTree as ET
from collections import Counter, deque
from typing import Any, Dict, List, Optional

import duckdb
from dotenv import load_dotenv
from strands import tool
from strands.types.tools import ToolContext

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
    s3_access_mode,
    BUCKET,
    REGION,
    SANDBOX_BASE_DIR,
    _resolve_file_reference,
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
_QUERY_MAX_FILE_BYTES = 500 * 1024 * 1024  # 500 MB — above this, download first
_TOOL_RESULT_CHAR_CAP = 6_000              # ~1.5k tokens — keeps single tool results from dominating context


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
    region = os.getenv("AWS_DEFAULT_REGION", REGION)
    conn.execute(f"SET s3_region='{region}'")
    if s3_access_mode() == "unsigned":
        # Keep DuckDB S3 access anonymous for public buckets.
        conn.execute("SET s3_access_key_id=''")
        conn.execute("SET s3_secret_access_key=''")
        conn.execute("SET s3_session_token=''")
    else:
        aws_key = os.getenv("AWS_ACCESS_KEY_ID", "")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY", "")
        aws_session = os.getenv("AWS_SESSION_TOKEN", "")
        if aws_key:
            conn.execute(f"SET s3_access_key_id='{aws_key}'")
        if aws_secret:
            conn.execute(f"SET s3_secret_access_key='{aws_secret}'")
        if aws_session:
            conn.execute(f"SET s3_session_token='{aws_session}'")
    return conn


_MAX_OBJECT_SIZE_RE = re.compile(
    r'"maximum_object_size".*?bytes\s*exceeded.*?\(>(\d+)\s*bytes\)',
    re.DOTALL,
)
_XML_NAMESPACE_RE = re.compile(r'\bxmlns(?::([A-Za-z_][\w.-]*))?=["\']([^"\']+)["\']')
_XML_SIMPLE_FIELD_RE = re.compile(
    r'<(?:[\w.-]+:)?SimpleField\b[^>]*\bname=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_XML_SIMPLE_DATA_RE = re.compile(
    r'<(?:[\w.-]+:)?SimpleData\b[^>]*\bname=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_XML_OPEN_TAG_RE = re.compile(r"<(?![!?/])([A-Za-z_][\w:.-]*)\b")
_XML_LEADING_NOISE_RE = re.compile(
    r"^(?:<\?xml.*?\?>\s*)?(?:<!--.*?-->\s*)*(?:<!DOCTYPE.*?>\s*)*",
    re.DOTALL | re.IGNORECASE,
)


def _normalize_sql_backticks(sql: str) -> str:
    """
    Convert MySQL-style backtick identifiers to DuckDB's double-quoted form.

    Agents trained on MySQL/SQLite repeatedly write `` `column name` `` even
    though DuckDB only accepts `"column name"`. Observed ~17 times in eval
    logs as Parser Errors. Auto-fix at the source eliminates the round-trip.

    Carefully preserves backticks that fall INSIDE single-quoted string
    literals (e.g. `WHERE name = 'O\\`Brien'`) and inside already-double-
    quoted identifiers (e.g. `"weird\\`col"`). Handles escaped single quotes
    (`''`) inside literals.
    """
    out: List[str] = []
    in_single = False
    in_double = False
    i = 0
    n = len(sql)
    while i < n:
        ch = sql[i]
        if in_single:
            if ch == "'":
                # `''` is an escaped single quote inside a literal
                if i + 1 < n and sql[i + 1] == "'":
                    out.append("''")
                    i += 2
                    continue
                in_single = False
            out.append(ch)
        elif in_double:
            if ch == '"':
                # `""` is an escaped double quote inside an identifier
                if i + 1 < n and sql[i + 1] == '"':
                    out.append('""')
                    i += 2
                    continue
                in_double = False
            out.append(ch)
        else:
            if ch == "'":
                in_single = True
                out.append(ch)
            elif ch == '"':
                in_double = True
                out.append(ch)
            elif ch == "`":
                out.append('"')
            else:
                out.append(ch)
        i += 1
    return "".join(out)


def _rewrite_query_error(raw: str) -> str:
    """
    Rewrite low-level DuckDB error strings into actionable remediation hints
    so the agent stops thrashing on platform-side limits.

    The headline case: when DuckDB's read_json_auto rejects a JSON object
    larger than `maximum_object_size`, the stock hint says "Try increasing
    maximum_object_size" — which is misleading because the cap is hard-coded
    in this module and the agent cannot change it. Logs show the agent then
    retries the same query, malforms a download call, or pivots to peek_file
    which doesn't help. The right remediation is the same one used by the
    pre-check at line 483: download the file and process it with execute_code.
    """
    m = _MAX_OBJECT_SIZE_RE.search(raw)
    if m:
        observed = m.group(1)
        return (
            f"File contains a JSON object larger than the 100 MB query limit "
            f"({observed} bytes observed). query_file cannot stream it. "
            "Use download to fetch the file, then execute_code with a "
            "streaming JSON parser (e.g. ijson) or pandas.read_json with "
            "chunksize."
        )
    if "Timeout was reached" in raw and "HTTP GET" in raw:
        return (
            "S3 read timed out — file is likely too large to query directly "
            "over httpfs. Use download to fetch it locally, then execute_code "
            "to process it. Original: " + raw
        )
    if "Parser Error" in raw and "`" in raw:
        # Agent is using MySQL-style backtick identifiers; DuckDB requires
        # double quotes. Observed ~17 times in production logs.
        return (
            'DuckDB uses double quotes for identifiers, not backticks. '
            'Replace `column name` with "column name" in your SQL. '
            "Original: " + raw
        )
    return raw


def _rewrite_unqueryable_family_error(family: str) -> str:
    """
    Replace the bare "File family '<X>' is not queryable with SQL" message
    with a hint naming the right tool to use instead. The agent has no way
    to know that text files should go through grep/read/peek; spell it out.
    """
    if family == "xml":
        return (
            "XML/KML was detected. query_file does not support XML because "
            "there is no stable row model for arbitrary XML documents yet. "
            "Use peek_file to inspect tags and schema fields, grep_file to "
            "search for specific values, or download + execute_code with "
            "xml.etree.ElementTree for custom extraction."
        )
    if family == "text":
        return (
            "File contents are plain text — query_file only handles CSV and "
            "JSON. Use peek_file to inspect structure, grep_file to search "
            "for specific values, or read_file to load lines directly."
        )
    return (
        f"File family '{family}' is not queryable with SQL via query_file "
        "(only CSV and JSON are supported). Use peek_file to inspect what "
        "the file actually contains, then pick a tool that matches its "
        "format (read_file for text, download + execute_code for binary "
        "or unsupported formats)."
    )


def _to_json_safe(value: Any) -> Any:
    """
    Convert DuckDB row values into JSON-serializable primitives.

    DuckDB returns native Python types for SQL DATE / TIMESTAMP / TIME / INTERVAL /
    DECIMAL / UUID / BLOB columns, which json.dumps cannot serialize. Without
    this conversion, even `SELECT * FROM t LIMIT 1` against any table with a
    date column raises `Object of type date is not JSON serializable`.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, datetime.time):
        return value.isoformat()
    if isinstance(value, datetime.timedelta):
        return value.total_seconds()
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, (bytes, bytearray, memoryview)):
        return base64.b64encode(bytes(value)).decode("ascii")
    if isinstance(value, dict):
        return {str(k): _to_json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_to_json_safe(v) for v in value]
    # Fallback for unexpected types (e.g., numpy scalars). Stringify rather
    # than crash — surfaces the value while keeping the tool call alive.
    return str(value)


def _strip_folder_prefix(dataset_id: str) -> str:
    """
    Silently strip a hallucinated leading `wikipedia/` or `datagov/` prefix
    from a dataset_id.

    The agent frequently constructs dataset ids of the form `wikipedia/<page>`
    after seeing a Wikipedia mention (~38 read_file errors per eval, plus a
    handful in peek_file/grep_file). The actual dataset_id is the bare name
    (e.g. `Logan_Fontenelle`), which the agent already knows one turn later
    via search_prefix. Per tool_error_findings.md the recommended fix is to
    auto-strip the prefix and resolve.

    Strips a single optional leading slash, then a case-insensitive
    `wikipedia/` or `datagov/` segment. Idempotent. Returns the input
    unchanged for empty/None or strings that don't start with one of the
    known folder prefixes.
    """
    if not dataset_id or not isinstance(dataset_id, str):
        return dataset_id
    candidate = dataset_id.lstrip("/")
    lowered = candidate.lower()
    for folder in ("wikipedia/", "datagov/"):
        if lowered.startswith(folder):
            return candidate[len(folder):]
    return dataset_id


def _local_xml_name(tag: str | None) -> str | None:
    """Return an XML tag without namespace or prefix decoration."""
    if not tag:
        return tag
    if tag.startswith("{") and "}" in tag:
        tag = tag.split("}", 1)[1]
    if ":" in tag:
        tag = tag.split(":", 1)[1]
    return tag


def _unique_preserve_order(values: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _extract_xml_namespaces(text: str) -> Dict[str, str]:
    namespaces: Dict[str, str] = {}
    for prefix, uri in _XML_NAMESPACE_RE.findall(text):
        key = prefix or "default"
        namespaces[key] = uri
    return namespaces


def _strip_xml_leading_noise(text: str) -> str:
    return _XML_LEADING_NOISE_RE.sub("", text.lstrip(), count=1)


def _extract_xml_root_tag(text: str) -> str | None:
    stripped = _strip_xml_leading_noise(text)
    m = _XML_OPEN_TAG_RE.match(stripped)
    if not m:
        return None
    return _local_xml_name(m.group(1))


def _extract_xml_schema_fields(text: str) -> List[str]:
    names = _XML_SIMPLE_FIELD_RE.findall(text) + _XML_SIMPLE_DATA_RE.findall(text)
    return _unique_preserve_order([name.strip() for name in names if name.strip()])


def _extract_xml_record_tag_candidates(text: str, root_tag: str | None) -> List[str]:
    tags = [_local_xml_name(tag) for tag in _XML_OPEN_TAG_RE.findall(_strip_xml_leading_noise(text))]
    filtered = [tag for tag in tags if tag]
    counts = Counter(filtered)

    candidates: List[str] = []
    if counts.get("Placemark"):
        candidates.append("Placemark")

    for tag, count in counts.most_common():
        if tag in {root_tag, "SimpleField", "SimpleData"}:
            continue
        if count >= 2:
            candidates.append(tag)

    if not candidates:
        for tag, _count in counts.most_common():
            if tag in {root_tag, "SimpleField", "SimpleData"}:
                continue
            candidates.append(tag)
            if len(candidates) >= 5:
                break

    return _unique_preserve_order(candidates)[:5]


def _build_xml_preview_from_tree(root: ET.Element, text: str) -> Dict[str, Any]:
    root_tag = _local_xml_name(root.tag)
    tags = [_local_xml_name(elem.tag) for elem in root.iter() if isinstance(elem.tag, str)]
    counts = Counter(tag for tag in tags if tag)
    schema_fields = _unique_preserve_order(
        [
            elem.attrib["name"].strip()
            for elem in root.iter()
            if _local_xml_name(elem.tag) in {"SimpleField", "SimpleData"}
            and elem.attrib.get("name", "").strip()
        ]
    )

    record_candidates: List[str] = []
    if counts.get("Placemark"):
        record_candidates.append("Placemark")
    for tag, count in counts.most_common():
        if tag in {root_tag, "SimpleField", "SimpleData"}:
            continue
        if count >= 2:
            record_candidates.append(tag)
    if not record_candidates:
        for tag, _count in counts.most_common():
            if tag in {root_tag, "SimpleField", "SimpleData"}:
                continue
            record_candidates.append(tag)
            if len(record_candidates) >= 5:
                break

    return {
        "xml_root_tag": root_tag,
        "xml_namespaces": _extract_xml_namespaces(text),
        "xml_schema_fields": schema_fields,
        "xml_record_tag_candidates": _unique_preserve_order(record_candidates)[:5],
        "xml_preview_mode": "parsed",
    }


def _build_xml_preview(text: str, size_bytes: int) -> Dict[str, Any]:
    if size_bytes <= _PEEK_BYTES:
        try:
            root = ET.fromstring(text)
            return _build_xml_preview_from_tree(root, text)
        except ET.ParseError:
            pass

    root_tag = _extract_xml_root_tag(text)
    return {
        "xml_root_tag": root_tag,
        "xml_namespaces": _extract_xml_namespaces(text),
        "xml_schema_fields": _extract_xml_schema_fields(text),
        "xml_record_tag_candidates": _extract_xml_record_tag_candidates(text, root_tag),
        "xml_preview_mode": "heuristic",
    }


# ---------------------------------------------------------------------------
# Tool 1: peek_file
# ---------------------------------------------------------------------------

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
        xml_record_tag_candidates, xml_preview_mode. On error: {error: ...}
    """
    ref = _resolve_file_reference(dataset_id=dataset_id, file_path=file_path, s3_uri=s3_uri)
    if "error" in ref:
        return {"error": ref["error"]}

    dataset_id = _strip_folder_prefix(ref["dataset_id"])
    file_path = ref["file_path"]
    s3_uri = ref["s3_uri"]
    s3 = _get_s3_client()
    key = ref["key"]

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
        "s3_uri": s3_uri,
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

    if family == "xml":
        result.update(_build_xml_preview(text, size_bytes))

    return result


# ---------------------------------------------------------------------------
# Tool 1b: peek_multiple (batch wrapper around peek_file)
# ---------------------------------------------------------------------------

@tool
def peek_multiple(
    files: Optional[List[Dict[str, str]]] = None,
    entries: Optional[List[Dict[str, str]]] = None,
    max_rows: int = 20,
) -> Dict[str, Any]:
    """
    Inspect SEVERAL files in ONE call — a batch wrapper around peek_file.

    USE THIS when you already know which 2+ files you need
    (e.g. immediately after `list_files` returned several relevant paths).
    For a single file, use `peek_file` instead — its signature is simpler.

    REQUIRED ARGUMENT SHAPE: You MUST pass a `files` list of dicts, NOT
    `dataset_id`/`file_path` directly:

        CORRECT:
            peek_multiple(files=[
                {"dataset_id": "census-2021", "file_path": "files/rows.txt"},
            ])
        WRONG (these will all error):
            peek_multiple(max_rows=5)                             # missing files

    Args:
        files:    NON-EMPTY list of dicts. Each dict needs 'dataset_id' and
                  'file_path'. The key 'path' is also accepted as an alias for
                  'file_path' so raw list_files output can be passed directly.
                  A per-entry `s3_uri` is also accepted.
        entries:  Alias for `files`. Accepted to be forgiving when the agent
                  uses the older/wrong wrapper key.
        max_rows: Maximum preview rows per file (default 20).

    Returns:
        Dict with 'results' list (one entry per file, same shape as peek_file)
        and 'count'.
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
                "after list_files, or peek_file(dataset_id, file_path) for one "
                "file. Example: "
                'peek_multiple(files=[{"dataset_id": "census", "file_path": "files/rows.txt"}], max_rows=5)'
            )
        }

    results = []
    for spec in files:
        if isinstance(spec, str):
            results.append(peek_file(s3_uri=spec, max_rows=max_rows))
            continue
        if not isinstance(spec, dict):
            results.append({"error": "each entry must be a dict with dataset_id/file_path or s3_uri"})
            continue
        ds = spec.get("dataset_id", "")
        fp = spec.get("file_path") or spec.get("path") or ""
        uri = spec.get("s3_uri") or spec.get("uri") or ""
        results.append(peek_file(dataset_id=ds, file_path=fp, max_rows=max_rows, s3_uri=uri))

    return {"results": results, "count": len(results)}


# ---------------------------------------------------------------------------
# Tool 2: read_file
# ---------------------------------------------------------------------------


@tool
def read_file(
    dataset_id: str | None = None,
    file_path: str | None = None,
    start_line: int = 0,
    max_lines: int = 10000,
    s3_uri: str | None = None,
) -> Dict[str, Any]:
    """
    Read lines from a file in the data lake without downloading it.
    Use this to read text, CSV, or JSON files directly. Supports pagination
    via start_line for large files.

    Args:
        dataset_id: Dataset identifier (e.g. "census")
        file_path:  Relative path within the dataset (e.g. "files/data.txt")
        start_line: Line index to start reading from, 0-based (default 0)
        max_lines:  Number of lines to return, capped at 10000 (default 10000)
        s3_uri:     Optional full object URI instead of dataset_id/file_path
    """
    if start_line < 0:
        return {"error": "start_line must be >= 0"}

    max_lines = min(max_lines, 10_000)
    ref = _resolve_file_reference(dataset_id=dataset_id, file_path=file_path, s3_uri=s3_uri)
    if "error" in ref:
        return {"error": ref["error"]}

    dataset_id = _strip_folder_prefix(ref["dataset_id"])
    file_path = ref["file_path"]
    s3_uri = ref["s3_uri"]
    s3 = _get_s3_client()
    key = ref["key"]

    try:
        resp = s3.get_object(Bucket=BUCKET, Key=key)
        body = resp["Body"]
        lines = []
        current = 0
        for raw_line in body.iter_lines():
            if current < start_line:
                current += 1
                continue
            lines.append(raw_line.decode("utf-8", errors="replace"))
            current += 1
            if len(lines) >= max_lines:
                break
        body.close()
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    result = {
        "dataset_id": dataset_id,
        "file_path": file_path,
        "s3_uri": s3_uri,
        "start_line": start_line,
        "returned_lines": len(lines),
        "lines": lines,
    }
    result_json = json.dumps(result)
    if len(result_json) > _TOOL_RESULT_CHAR_CAP:
        # Write full content to sandbox, return truncated lines + pointer
        sandbox = _get_sandbox_dir()
        safe_name = file_path.lstrip("/").replace("/", "_")
        dump_path = sandbox / dataset_id / f"{safe_name}.read_result.json"
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        dump_path.write_text(result_json)
        budget = _TOOL_RESULT_CHAR_CAP - 600
        char_count, truncated_lines = 0, []
        for line in lines:
            if char_count + len(line) + 4 > budget:
                break
            truncated_lines.append(line)
            char_count += len(line) + 4
        return {
            "dataset_id": dataset_id,
            "file_path": file_path,
            "s3_uri": s3_uri,
            "start_line": start_line,
            "returned_lines": len(truncated_lines),
            "truncated": True,
            "local_result_path": str(dump_path),
            "truncation_note": (
                f"Output truncated to {len(truncated_lines)} of {len(lines)} fetched lines. "
                f"Full content written to: {dump_path} (use execute_code to read it). "
                f"Or use start_line={start_line + len(truncated_lines)} to page forward, "
                "or grep_file for specific values."
            ),
            "lines": truncated_lines,
        }
    return result


# ---------------------------------------------------------------------------
# Tool 3: grep_file
# ---------------------------------------------------------------------------

@tool
def grep_file(
    dataset_id: str | None = None,
    file_path: str | None = None,
    regex_pattern: str = "",
    context_lines: int = 2,
    s3_uri: str | None = None,
) -> Dict[str, Any]:
    """
    Search for a regex pattern inside a file without downloading it.
    Streams the file from S3 and returns matching lines with surrounding context.
    Use this to locate specific values, IDs, or keywords in large files.

    Args:
        dataset_id:    Dataset identifier (e.g. "public-school-locations-current-23297")
        file_path:     Relative path within the dataset (e.g. "files/data.txt")
        regex_pattern: Case-insensitive regex to search for (e.g. "King County")
        context_lines: Lines of context before/after each match (default 2, max 5)
        s3_uri:        Optional full object URI instead of dataset_id/file_path

    Returns:
        Dict with keys: match_count, matches (list of {line_number, line,
        context_before, context_after}), truncated. On error: {error: ...}
    """
    if not regex_pattern:
        return {"error": "regex_pattern is required"}

    context_lines = min(context_lines, 5)
    # filename = file_path.rsplit("/", 1)[-1]
    # if should_skip(filename):
    #     return {"error": f"File skipped (metadata/binary): {file_path}"}

    try:
        pattern = re.compile(regex_pattern, re.IGNORECASE)
    except re.error as e:
        return {"error": f"Invalid regex pattern: {e}"}

    ref = _resolve_file_reference(dataset_id=dataset_id, file_path=file_path, s3_uri=s3_uri)
    if "error" in ref:
        return {"error": ref["error"]}

    dataset_id = _strip_folder_prefix(ref["dataset_id"])
    file_path = ref["file_path"]
    s3_uri = ref["s3_uri"]
    s3 = _get_s3_client()
    key = ref["key"]

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

    result = {
        "dataset_id": dataset_id,
        "file_path": file_path,
        "s3_uri": s3_uri,
        "match_count": len(matches),
        "truncated_matches": len(matches) >= _SEARCH_MAX_MATCHES,
        "matches": matches,
    }
    result_json = json.dumps(result)
    if len(result_json) > _TOOL_RESULT_CHAR_CAP:
        sandbox = _get_sandbox_dir()
        safe_name = file_path.lstrip("/").replace("/", "_")
        dump_path = sandbox / dataset_id / f"{safe_name}.grep_result.json"
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        dump_path.write_text(result_json)
        budget = _TOOL_RESULT_CHAR_CAP - 600
        char_count, capped_matches = 0, []
        for match in matches:
            match_json = json.dumps(match)
            if char_count + len(match_json) + 2 > budget:
                break
            capped_matches.append(match)
            char_count += len(match_json) + 2
        return {
            "dataset_id": dataset_id,
            "file_path": file_path,
            "s3_uri": s3_uri,
            "match_count": len(matches),
            "returned_matches": len(capped_matches),
            "truncated_matches": True,
            "local_result_path": str(dump_path),
            "truncation_note": (
                f"Match output exceeded the {_TOOL_RESULT_CHAR_CAP} char limit. "
                f"Showing {len(capped_matches)} of {len(matches)} matches. "
                f"Full result written to: {dump_path}. "
                "Tighten the regex or reduce context_lines if you need a smaller in-context result."
            ),
            "matches": capped_matches,
        }
    return result

# ---------------------------------------------------------------------------
# Tool 4: query_file
# ---------------------------------------------------------------------------

@tool
def query_file(
    dataset_id: str | None = None,
    file_path: str | None = None,
    sql: str = "",
    s3_uri: str | None = None,
) -> Dict[str, Any]:
    """
    Run a SQL query directly against an S3 file using DuckDB httpfs.
    No download required. The file is referenced as table alias 't'.

    Supported file types: CSV (.csv), JSON (.json, .jsonl, .ndjson).
    XML/KML is detected but not queryable here; query_file returns a hint
    to use peek_file, grep_file, or download + execute_code instead.
    Results are capped at 200 rows.

    Args:
        dataset_id: Dataset identifier (e.g. "Barack_Obama")
        file_path:  Relative path within the dataset (e.g. "table_0.csv")
        sql:        SQL query. Use 't' as the table alias.
                    Example: "SELECT * FROM t LIMIT 10"
                    Example: "SELECT col1, COUNT(*) FROM t GROUP BY col1"
        s3_uri:     Optional full object URI instead of dataset_id/file_path

    Returns:
        Dict with keys: columns, rows, row_count, truncated. On error: {error: ...}
    """
    if not sql or not sql.strip():
        return {"error": "sql is required"}

    # Auto-fix MySQL-style backtick identifiers — DuckDB only accepts double
    # quotes. Preserves backticks inside string literals. Eliminates ~17
    # Parser Errors per eval at the source.
    sql = _normalize_sql_backticks(sql)

    ref = _resolve_file_reference(dataset_id=dataset_id, file_path=file_path, s3_uri=s3_uri)
    if "error" in ref:
        return {"error": ref["error"]}

    dataset_id = _strip_folder_prefix(ref["dataset_id"])
    file_path = ref["file_path"]
    s3_uri = ref["s3_uri"]

    # Determine reader function — peek first for all extensions
    try:
        s3 = _get_s3_client()
        key = ref["key"]
        size = _s3_head(s3, key)
        if size > _QUERY_MAX_FILE_BYTES:
            return {"error": f"File too large to query directly ({size // (1024*1024)} MB). Use download + execute_code instead."}
        end = min(_PEEK_BYTES - 1, size - 1)
        raw = _s3_range_get(s3, key, 0, end)
        text = raw.decode("utf-8", errors="replace")
        family = detect_family(text)
    except Exception as e:
        return {"error": f"Could not detect file family: {e}"}

    if family == "csv":
        reader = f"read_csv_auto('{s3_uri}')"
    elif family == "json":
        reader = f"read_json_auto('{s3_uri}', maximum_object_size=104857600)"
    else:
        return {"error": _rewrite_unqueryable_family_error(family)}

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
        # Convert rows to JSON-safe primitives up front so DATE / TIMESTAMP /
        # DECIMAL / UUID / BLOB columns don't crash json.dumps below.
        safe_rows = [[_to_json_safe(v) for v in r] for r in rows]
        result = {
            "dataset_id": dataset_id,
            "file_path": file_path,
            "s3_uri": s3_uri,
            "columns": columns,
            "rows": safe_rows,
            "row_count": len(safe_rows),
            "truncated": truncated,
        }
        result_json = json.dumps(result)
        if len(result_json) > _TOOL_RESULT_CHAR_CAP:
            # Write full result to sandbox so agent can read it via execute_code
            sandbox = _get_sandbox_dir()
            safe_name = file_path.lstrip("/").replace("/", "_")
            dump_path = sandbox / dataset_id / f"{safe_name}.query_result.json"
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(result_json)
            # Pack as many rows as fit within the budget
            budget = _TOOL_RESULT_CHAR_CAP - 600  # headroom for metadata fields
            char_count, capped_rows = 0, []
            for row in safe_rows:
                row_json = json.dumps(row)
                if char_count + len(row_json) + 2 > budget:
                    break
                capped_rows.append(row)
                char_count += len(row_json) + 2
            avg_row_bytes = len(result_json) // max(len(safe_rows), 1)
            return {
                "truncated": True,
                "truncation_note": (
                    f"Result too large for context ({size // 1024}KB source file, "
                    f"~{int(size / max(1, avg_row_bytes))} rows estimated). "
                    f"Showing {len(capped_rows)} of {len(safe_rows)} rows within the {_TOOL_RESULT_CHAR_CAP} char limit. "
                    f"Full result written to: {dump_path} (use execute_code to read it). "
                    "Prefer: query_file with SELECT specific columns + WHERE/GROUP BY/LIMIT "
                    "for aggregates, or grep_file for searching specific values."
                ),
                "local_result_path": str(dump_path),
                "dataset_id": dataset_id,
                "file_path": file_path,
                "s3_uri": s3_uri,
                "size_bytes": size,
                "columns": columns,
                "rows": capped_rows,
                "row_count_shown": len(capped_rows),
                "row_count_estimate": int(size / max(1, avg_row_bytes)),
            }
        return result
    except Exception as e:
        return {
            "error": f"Query failed: {_rewrite_query_error(str(e))}",
            "traceback": traceback.format_exc(),
        }


# ---------------------------------------------------------------------------
# Tool 5: summarize_context
# ---------------------------------------------------------------------------

@tool(context=True)
def summarize_context(
    summary: str,
    drop_messages: int,
    tool_context: ToolContext,
) -> dict:
    """
    Free up context space by dropping old messages and anchoring your key findings.

    Write everything important you've learned so far into `summary` — datasets found,
    values computed, hypotheses confirmed or rejected. That text is injected at the
    start of the remaining history as a permanent memory anchor that won't be
    truncated by the sliding window.

    Call this proactively when the conversation is getting long, before making a
    large tool call, or after receiving a truncation_note from another tool.

    Args:
        summary:       Your written summary of findings so far. Be thorough — this
                       replaces the dropped messages as your memory. Not truncated.
        drop_messages: Number of oldest messages to remove (must be >= 2 and even,
                       to preserve tool use/result pairs). Use 10–20 for moderate
                       cleanup, higher for aggressive cleanup.

    Returns:
        Dict with messages_before, messages_after, and confirmation.
    """
    try:
        agent = tool_context.agent
        messages = agent.messages
        before = len(messages)

        # Clamp and align drop_messages to an even number (preserve tool use/result pairs)
        n = max(2, int(drop_messages))
        n = min(n, max(0, before - 2))  # always keep at least 2 messages
        if n % 2 != 0:
            n -= 1  # round down to even

        # Find a safe trim index: can't start on a toolResult or orphaned toolUse
        trim = n
        while trim < before:
            content = messages[trim].get("content", [])
            is_tool_result = any("toolResult" in c for c in content)
            is_orphan_tool_use = (
                any("toolUse" in c for c in content)
                and trim + 1 < before
                and not any("toolResult" in c for c in messages[trim + 1].get("content", []))
            )
            if is_tool_result or is_orphan_tool_use:
                trim += 1
            else:
                break

        # Drop the oldest `trim` messages
        messages[:] = messages[trim:]

        # Prepend the agent's summary as a user message at position 0
        # User messages are never truncated by _truncate_tool_results
        memory_message = {
            "role": "user",
            "content": [{"text": f"[Context summary — key findings so far]\n{summary}"}],
        }
        messages.insert(0, memory_message)

        after = len(messages)
        return {
            "status": "ok",
            "messages_before": before,
            "messages_dropped": trim,
            "messages_after": after,
            "summary_anchored": True,
            "note": (
                f"Dropped {trim} oldest messages. Your summary is anchored at position 0 "
                "and will not be truncated. Continue your task."
            ),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # v2-new
    "peek_file",
    "peek_multiple",
    "read_file",
    "grep_file",
    "query_file",
    "summarize_context",
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
