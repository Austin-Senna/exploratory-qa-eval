#!/usr/bin/env python3
"""Build datagov_tables_profiles.jsonl from schema and metadata caches."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import decimal
import json
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import duckdb
from dotenv import load_dotenv
try:
    from tqdm.auto import tqdm
except Exception:  # pragma: no cover
    def tqdm(iterable=None, **_kwargs):
        return iterable if iterable is not None else _NullTqdm()

from strands_evaluation.tools.agent_tools import BUCKET, REGION, _build_s3_client
from strands_evaluation.tools.helper.detect import detect_family

load_dotenv()


class _NullTqdm:
    def update(self, _n: int = 1) -> None:
        return None

    def set_postfix(self, *args, **kwargs) -> None:
        return None

    def close(self) -> None:
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

_DESC_PATH = Path("table_descriptions.jsonl")
_SNIPPET_PATH = Path("snippet.jsonl")
_SNIFF_BYTES = 8 * 1024
_SNIPPET_FALLBACK_BYTES = 2 * 1024
_MAX_CELL_CHARS = 80

_TABULAR_KIND_TO_FAMILY = {
    "delimited_text": "csv",
    "csv": "csv",
    "tsv": "csv",
    "parquet": "parquet",
    "json": "json",
    "geojson": "json",
}


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="datagov_tables_schemas_full.jsonl")
    parser.add_argument("--input-kind", choices=("auto", "schemas", "manifest"), default="auto")
    parser.add_argument("--output", default="datagov_tables_profiles.jsonl")
    parser.add_argument("--descriptions", default=str(_DESC_PATH))
    parser.add_argument("--snippets", default=str(_SNIPPET_PATH))
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--bucket", default=BUCKET)
    return parser.parse_args(argv)


def _jsonl_rows(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                yield obj


def _peek_first_row(path: Path) -> Optional[Dict[str, Any]]:
    for obj in _jsonl_rows(path):
        return obj
    return None


def _load_description_cache(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for obj in _jsonl_rows(path):
        uri = str(obj.get("dataset_uri") or obj.get("uri") or "").strip()
        desc = str(obj.get("description") or "").strip()
        if uri and desc and uri not in out:
            out[uri] = desc
    return out


def _load_snippet_cache(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for obj in _jsonl_rows(path):
        uri = str(obj.get("dataset_uri") or obj.get("uri") or "").strip()
        snippet = str(obj.get("dataset_snippet") or obj.get("snippet") or obj.get("content") or "").strip()
        if uri and snippet and uri not in out:
            out[uri] = snippet
    return out


def _profile_identity(row: Dict[str, Any]) -> Optional[str]:
    s3_uri = str(row.get("s3_uri") or "").strip()
    if s3_uri:
        return f"uri:{s3_uri}"
    slug = str(row.get("slug") or "").strip()
    filename = str(row.get("filename") or "").strip()
    if slug and filename:
        return f"slug:{slug}::{filename}"
    return None


def _load_existing_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys: set[str] = set()
    for obj in _jsonl_rows(path):
        identity = _profile_identity(obj)
        if identity:
            keys.add(identity)
    return keys


def _sql_quote_string(value: str) -> str:
    return "'" + str(value).replace("\\", "\\\\").replace("'", "''") + "'"


def _sql_quote_ident(value: str) -> str:
    return '"' + str(value).replace('"', '""') + '"'


def _is_s3_ref(source_ref: str) -> bool:
    return str(source_ref).startswith("s3://")


def _parse_s3_uri(uri: str) -> Tuple[str, str]:
    raw = str(uri)
    if not raw.startswith("s3://"):
        raise ValueError(f"Expected s3:// URI, got: {uri}")
    bucket_and_key = raw[5:]
    if "/" not in bucket_and_key:
        raise ValueError(f"Malformed s3:// URI, missing key: {uri}")
    bucket, key = bucket_and_key.split("/", 1)
    return bucket, key


def _build_s3_client_for_runtime():
    requested = (os.getenv("S3_ACCESS_MODE", "auto") or "auto").strip().lower()
    if requested in {"unsigned", "public", "anonymous", "anon", "no-sign-request"}:
        return _build_s3_client(unsigned=True)
    try:
        return _build_s3_client(unsigned=False)
    except Exception:
        return _build_s3_client(unsigned=True)


def _head_size_bytes(source_ref: str) -> int:
    if _is_s3_ref(source_ref):
        bucket, key = _parse_s3_uri(source_ref)
        s3 = _build_s3_client_for_runtime()
        meta = s3.head_object(Bucket=bucket, Key=key)
        return int(meta.get("ContentLength") or 0)
    return int(Path(source_ref).stat().st_size)


def _read_prefix_bytes(source_ref: str, num_bytes: int) -> bytes:
    if _is_s3_ref(source_ref):
        bucket, key = _parse_s3_uri(source_ref)
        s3 = _build_s3_client_for_runtime()
        end = max(num_bytes - 1, 0)
        resp = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes=0-{end}")
        return resp["Body"].read()
    with Path(source_ref).open("rb") as f:
        return f.read(num_bytes)


def _expected_family(table_kind: str) -> Optional[str]:
    return _TABULAR_KIND_TO_FAMILY.get((table_kind or "").strip().lower())


def _resolve_family(table: Dict[str, Any], source_ref: str) -> str:
    expected = _expected_family(str(table.get("table_kind") or ""))
    if expected == "parquet":
        return "parquet"

    try:
        sniff_text = _read_prefix_bytes(source_ref, _SNIFF_BYTES).decode("utf-8", errors="replace")
    except Exception:
        return expected or "text"

    sniffed = detect_family(sniff_text)
    if expected and sniffed == "text":
        return expected
    return expected or sniffed


def _source_ref_for_table(table: Dict[str, Any], bucket: str) -> str:
    direct_uri = str(table.get("source_uri") or table.get("s3_uri") or "").strip()
    if direct_uri:
        return direct_uri

    local_path = str(table.get("local_path") or "").strip()
    if local_path:
        return local_path

    s3_key = str(table.get("s3_key") or "").strip()
    if not s3_key:
        raise ValueError("Schema table is missing both source_uri/local_path and s3_key")
    return f"s3://{bucket}/{s3_key}"


def _filename_stem(table: Dict[str, Any], source_ref: str) -> str:
    rel = str(table.get("relative_path") or "").strip()
    name = rel.rsplit("/", 1)[-1] if rel else Path(source_ref).name
    return name.rsplit(".", 1)[0] if "." in name else name


def _stem_from_path(path_like: str) -> str:
    name = str(path_like).rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[0] if "." in name else name


def _iter_schema_entries(input_path: Path, bucket: str) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for obj in _jsonl_rows(input_path):
        slug = str(obj.get("dataset_slug") or "").strip()
        if not slug:
            continue
        tables = obj.get("tables") or []
        if not isinstance(tables, list):
            continue
        for table in tables:
            if not isinstance(table, dict):
                continue
            source_ref = _source_ref_for_table(table, bucket)
            entries.append(
                {
                    "slug": slug,
                    "filename": _filename_stem(table, source_ref),
                    "source_ref": source_ref,
                    "s3_uri": source_ref if _is_s3_ref(source_ref) else None,
                    "table": table,
                }
            )
    return entries


def _iter_manifest_entries(input_path: Path) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for obj in _jsonl_rows(input_path):
        source_ref = str(obj.get("source_ref") or obj.get("local_path") or obj.get("s3_uri") or "").strip()
        if not source_ref:
            continue
        dataset_id = str(obj.get("dataset_id") or "").strip()
        file_path = str(obj.get("file_path") or obj.get("path") or "").strip()
        slug = dataset_id or _stem_from_path(source_ref)
        filename = _stem_from_path(file_path or source_ref)
        table = {
            "delimiter": obj.get("delimiter"),
            "table_kind": obj.get("table_kind"),
        }
        entry = {
            "slug": slug,
            "filename": filename,
            "source_ref": source_ref,
            "s3_uri": str(obj.get("s3_uri") or "").strip() or None,
            "dataset_id": dataset_id or None,
            "file_path": file_path or None,
            "size_bytes": obj.get("size_bytes") or obj.get("size"),
            "table": table,
        }
        entries.append(entry)
    return entries


def _detect_input_kind(input_path: Path) -> str:
    first_row = _peek_first_row(input_path)
    if first_row is None:
        return "manifest"
    if isinstance(first_row.get("tables"), list):
        return "schemas"
    return "manifest"


def _iter_input_entries(input_path: Path, *, input_kind: str, bucket: str) -> List[Dict[str, Any]]:
    resolved = _detect_input_kind(input_path) if input_kind == "auto" else input_kind
    if resolved == "schemas":
        return _iter_schema_entries(input_path, bucket)
    return _iter_manifest_entries(input_path)


def _duckdb_connection(*, needs_httpfs: bool) -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect(":memory:")
    if needs_httpfs:
        conn.execute("INSTALL httpfs")
        conn.execute("LOAD httpfs")
        conn.execute(f"SET s3_region='{REGION}'")

        requested = (os.getenv("S3_ACCESS_MODE", "auto") or "auto").strip().lower()
        if requested in {"unsigned", "public", "anonymous", "anon", "no-sign-request"}:
            conn.execute("SET s3_access_key_id=''")
            conn.execute("SET s3_secret_access_key=''")
            conn.execute("SET s3_session_token=''")
        else:
            access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
            secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
            session_token = os.getenv("AWS_SESSION_TOKEN", "")
            if access_key:
                conn.execute(f"SET s3_access_key_id='{access_key}'")
            if secret_key:
                conn.execute(f"SET s3_secret_access_key='{secret_key}'")
            if session_token:
                conn.execute(f"SET s3_session_token='{session_token}'")
    return conn


def _scan_sql(source_ref: str, family: str, table: Dict[str, Any]) -> str:
    ref = _sql_quote_string(source_ref)
    if family == "parquet":
        return f"read_parquet({ref})"
    if family == "json":
        return f"read_json_auto({ref})"

    delimiter = table.get("delimiter")
    options = ["sample_size=-1"]
    if delimiter:
        options.append(f"delim={_sql_quote_string(str(delimiter))}")
    return f"read_csv_auto({ref}, {', '.join(options)})"


def _type_category(raw_type: str) -> Tuple[str, Optional[str]]:
    upper = (raw_type or "").upper()
    if upper.startswith(("TINYINT", "SMALLINT", "INTEGER", "BIGINT", "UTINYINT", "USMALLINT", "UINTEGER", "UBIGINT")):
        return "integer", "numeric"
    if upper.startswith(("DECIMAL", "DOUBLE", "FLOAT", "REAL", "HUGEINT")):
        return "number", "numeric"
    if upper.startswith("DATE"):
        return "date", "temporal"
    if upper.startswith(("TIMESTAMP", "TIME")):
        return "datetime", "temporal"
    if upper.startswith("BOOLEAN"):
        return "boolean", None
    return "string", None


def _json_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return None if not math.isfinite(value) else value
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, dt.datetime):
        if value.tzinfo is not None:
            return value.isoformat()
        return value.replace(tzinfo=dt.timezone.utc).isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, dt.time):
        return value.isoformat()
    return value


def _truncate_cell(value: Any) -> Any:
    value = _json_value(value)
    if isinstance(value, str) and len(value) > _MAX_CELL_CHARS:
        return value[:_MAX_CELL_CHARS] + "…"
    return value


def _top_rows(conn: duckdb.DuckDBPyConnection, scan_sql: str) -> List[Dict[str, Any]]:
    cursor = conn.execute(f"SELECT * FROM {scan_sql} LIMIT 2")
    colnames = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    out: List[Dict[str, Any]] = []
    for row in rows:
        out.append({name: _truncate_cell(value) for name, value in zip(colnames, row)})
    return out


def _mean_from_epoch(value: Any, kind: str) -> Optional[str]:
    value = _json_value(value)
    if value is None:
        return None
    stamp = dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc)
    if kind == "date":
        return stamp.date().isoformat()
    return stamp.isoformat()


def _column_profiles(conn: duckdb.DuckDBPyConnection, scan_sql: str) -> Tuple[int, List[Dict[str, Any]]]:
    describe_rows = conn.execute(f"DESCRIBE SELECT * FROM {scan_sql}").fetchall()
    columns: List[Tuple[str, str, Optional[str]]] = []
    for row in describe_rows:
        name = str(row[0])
        raw_type = str(row[1])
        output_type, aggregate_kind = _type_category(raw_type)
        columns.append((name, output_type, aggregate_kind))

    select_exprs = ["COUNT(*) AS row_count"]
    for idx, (name, output_type, aggregate_kind) in enumerate(columns):
        quoted = _sql_quote_ident(name)
        select_exprs.append(f"SUM(CASE WHEN {quoted} IS NULL THEN 1 ELSE 0 END) AS null_count_{idx}")
        select_exprs.append(f"COUNT(DISTINCT CAST({quoted} AS VARCHAR)) AS distinct_count_{idx}")
        if aggregate_kind in {"numeric", "temporal"}:
            select_exprs.append(f"MIN({quoted}) AS min_{idx}")
            select_exprs.append(f"MAX({quoted}) AS max_{idx}")
        else:
            select_exprs.append(f"NULL AS min_{idx}")
            select_exprs.append(f"NULL AS max_{idx}")
        if aggregate_kind == "numeric":
            select_exprs.append(f"AVG({quoted}) AS mean_{idx}")
        elif aggregate_kind == "temporal":
            select_exprs.append(f"AVG(epoch(CAST({quoted} AS TIMESTAMP))) AS mean_{idx}")
        else:
            select_exprs.append(f"NULL AS mean_{idx}")

    aggregate_row = conn.execute(f"SELECT {', '.join(select_exprs)} FROM {scan_sql}").fetchone()
    row_count = int(aggregate_row[0] or 0)
    profiles: List[Dict[str, Any]] = []
    offset = 1
    for idx, (name, output_type, aggregate_kind) in enumerate(columns):
        null_count = int(aggregate_row[offset] or 0)
        distinct_count = int(aggregate_row[offset + 1] or 0)
        min_value = aggregate_row[offset + 2]
        max_value = aggregate_row[offset + 3]
        mean_value = aggregate_row[offset + 4]
        if aggregate_kind == "temporal":
            mean_value = _mean_from_epoch(mean_value, output_type)
        else:
            mean_value = _json_value(mean_value)
        profiles.append(
            {
                "name": name,
                "type": output_type,
                "null_rate": round((null_count / row_count), 2) if row_count else 0.0,
                "distinct_count": distinct_count,
                "min": _json_value(min_value) if aggregate_kind in {"numeric", "temporal"} else None,
                "max": _json_value(max_value) if aggregate_kind in {"numeric", "temporal"} else None,
                "mean": mean_value if aggregate_kind in {"numeric", "temporal"} else None,
            }
        )
        offset += 5
    return row_count, profiles


def _snippet_fallback(source_ref: str) -> str:
    raw = _read_prefix_bytes(source_ref, _SNIPPET_FALLBACK_BYTES)
    return raw.decode("utf-8", errors="replace").strip()


def _build_tabular_profile(
    *,
    slug: str,
    filename: str,
    source_ref: str,
    s3_uri: Optional[str],
    dataset_id: Optional[str],
    file_path: Optional[str],
    family: str,
    table: Dict[str, Any],
    size_bytes: int,
    description: Optional[str],
) -> Dict[str, Any]:
    conn = _duckdb_connection(needs_httpfs=_is_s3_ref(source_ref))
    try:
        scan_sql = _scan_sql(source_ref, family, table)
        row_count, columns = _column_profiles(conn, scan_sql)
        top_2_rows = _top_rows(conn, scan_sql)
    finally:
        conn.close()

    profile: Dict[str, Any] = {
        "slug": slug,
        "filename": filename,
        "family": family,
        "size_bytes": size_bytes,
        "row_count": row_count,
        "top_2_rows": top_2_rows,
        "columns": columns,
    }
    if s3_uri:
        profile["s3_uri"] = s3_uri
    if dataset_id:
        profile["dataset_id"] = dataset_id
    if file_path:
        profile["file_path"] = file_path
    if description:
        profile["llm_description"] = description
    return profile


def _build_non_tabular_profile(
    *,
    slug: str,
    filename: str,
    source_ref: str,
    s3_uri: Optional[str],
    dataset_id: Optional[str],
    file_path: Optional[str],
    family: str,
    size_bytes: int,
    description: Optional[str],
    snippet_cache: Dict[str, str],
) -> Dict[str, Any]:
    profile: Dict[str, Any] = {
        "slug": slug,
        "filename": filename,
        "family": family,
        "size_bytes": size_bytes,
        "snippet": snippet_cache.get(source_ref) or _snippet_fallback(source_ref),
    }
    if s3_uri:
        profile["s3_uri"] = s3_uri
    if dataset_id:
        profile["dataset_id"] = dataset_id
    if file_path:
        profile["file_path"] = file_path
    if description:
        profile["llm_description"] = description
    return profile


def _process_entry(entry: Dict[str, Any], description_cache: Dict[str, str], snippet_cache: Dict[str, str]) -> Tuple[Tuple[str, str], Optional[Dict[str, Any]], Optional[str]]:
    slug = str(entry["slug"])
    filename = str(entry["filename"])
    source_ref = str(entry["source_ref"])
    s3_uri = str(entry.get("s3_uri") or "").strip() or None
    dataset_id = entry.get("dataset_id")
    file_path = entry.get("file_path")
    table = entry["table"]
    key = (slug, filename)
    try:
        size_bytes = int(entry.get("size_bytes") or 0) or _head_size_bytes(source_ref)
        cache_key = s3_uri or source_ref
        description = description_cache.get(cache_key)
        family = _resolve_family(table, source_ref)
        if family in {"csv", "json", "parquet"}:
            profile = _build_tabular_profile(
                slug=slug,
                filename=filename,
                source_ref=source_ref,
                s3_uri=s3_uri,
                dataset_id=dataset_id,
                file_path=file_path,
                family=family,
                table=table,
                size_bytes=size_bytes,
                description=description,
            )
        else:
            profile = _build_non_tabular_profile(
                slug=slug,
                filename=filename,
                source_ref=source_ref,
                s3_uri=s3_uri,
                dataset_id=dataset_id,
                file_path=file_path,
                family=family,
                size_bytes=size_bytes,
                description=description,
                snippet_cache=snippet_cache,
            )
        return key, profile, None
    except Exception as exc:
        return key, None, f"{type(exc).__name__}: {exc}"


def build_profiles(
    *,
    input_path: Path,
    output_path: Path,
    input_kind: str = "auto",
    descriptions_path: Path = _DESC_PATH,
    snippets_path: Path = _SNIPPET_PATH,
    parallel: int = 4,
    resume: bool = False,
    bucket: str = BUCKET,
) -> Dict[str, int]:
    description_cache = _load_description_cache(descriptions_path)
    snippet_cache = _load_snippet_cache(snippets_path)
    entries = _iter_input_entries(input_path, input_kind=input_kind, bucket=bucket)
    existing_keys = _load_existing_keys(output_path) if resume else set()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if resume else "w"
    written = 0
    skipped = 0
    errors = 0

    with output_path.open(mode) as out:
        if parallel <= 1:
            for entry in tqdm(
                entries,
                total=len(entries),
                desc="Profiling files",
                unit="file",
            ):
                identity = _profile_identity(entry)
                key = (entry["slug"], entry["filename"])
                if identity is not None and identity in existing_keys:
                    skipped += 1
                    continue
                _, profile, error = _process_entry(entry, description_cache, snippet_cache)
                if error is not None or profile is None:
                    errors += 1
                    print(f"SKIP {key[0]}/{key[1]}: {error}", file=sys.stderr)
                    continue
                out.write(json.dumps(profile, default=_json_value))
                out.write("\n")
                out.flush()
                written += 1
            return {"written": written, "skipped": skipped, "errors": errors}

        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
            futures: Dict[concurrent.futures.Future, Tuple[str, str]] = {}
            for entry in entries:
                identity = _profile_identity(entry)
                key = (entry["slug"], entry["filename"])
                if identity is not None and identity in existing_keys:
                    skipped += 1
                    continue
                future = executor.submit(_process_entry, entry, description_cache, snippet_cache)
                futures[future] = key

            with tqdm(total=len(futures), desc="Profiling files", unit="file") as pbar:
                for future in concurrent.futures.as_completed(futures):
                    _, profile, error = future.result()
                    if error is not None or profile is None:
                        errors += 1
                        key = futures[future]
                        print(f"SKIP {key[0]}/{key[1]}: {error}", file=sys.stderr)
                        pbar.update(1)
                        continue
                    out.write(json.dumps(profile, default=_json_value))
                    out.write("\n")
                    out.flush()
                    written += 1
                    pbar.update(1)

    return {"written": written, "skipped": skipped, "errors": errors}


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
    summary = build_profiles(
        input_path=Path(args.input),
        output_path=Path(args.output),
        input_kind=args.input_kind,
        descriptions_path=Path(args.descriptions),
        snippets_path=Path(args.snippets),
        parallel=args.parallel,
        resume=args.resume,
        bucket=args.bucket,
    )
    print(
        f"Wrote {summary['written']} profiles to {args.output} "
        f"(skipped={summary['skipped']}, errors={summary['errors']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
