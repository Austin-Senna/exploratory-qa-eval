#!/usr/bin/env python3
"""Stage and upload sanitized HotpotQA context paragraphs to S3."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urlparse


REPO = Path(__file__).resolve().parents[1]
DEFAULT_RAW_PATH = REPO / "other-benchmarks" / "raw" / "hotpotqa" / "hotpot_dev_distractor_v1.json"
DEFAULT_TASKS_DIR = REPO / "tasks-hotpotqa-mini"
DEFAULT_STAGING_DIR = REPO / "other-benchmarks" / "data-imports" / "hotpotqa" / "_s3_context_staging"
DEFAULT_MANIFEST_PATH = REPO / "manifests" / "hotpotqa_context_manifest.jsonl"
DEFAULT_BUCKET_URI = "s3://sana-hotpotqa-2"


@dataclass(frozen=True)
class UploadItem:
    local_path: Path
    bucket: str
    key: str
    source_id: str
    title: str

    @property
    def s3_uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"


def parse_bucket_uri(bucket_uri: str) -> tuple[str, str]:
    parsed = urlparse(bucket_uri)
    if parsed.scheme != "s3" or not parsed.netloc:
        raise ValueError(f"expected an S3 URI like s3://bucket[/prefix], got {bucket_uri!r}")
    return parsed.netloc, parsed.path.strip("/")


def _join_key(prefix: str, key: str) -> str:
    return f"{prefix}/{key}" if prefix else key


def _title_slug(title: str) -> str:
    normalized = re.sub(r"\s+", "_", title.strip())
    return quote(normalized, safe="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-()")


def _paragraph_filename(title: str, used: set[str]) -> str:
    base = f"{_title_slug(title)}.txt"
    if base not in used:
        used.add(base)
        return base
    stem = base[:-4]
    index = 2
    while True:
        candidate = f"{stem}_{index}.txt"
        if candidate not in used:
            used.add(candidate)
            return candidate
        index += 1


def _context_text(source_id: str, title: str, sentences: list[str]) -> str:
    lines = [
        f"Title: {title}",
        f"HotpotQA Source ID: {source_id}",
        "",
    ]
    lines.extend(f"[{index}] {sentence.strip()}" for index, sentence in enumerate(sentences))
    return "\n".join(lines).rstrip() + "\n"


def _load_raw_examples(raw_path: Path) -> list[dict]:
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)
    with raw_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"expected HotpotQA raw file to contain a list, got {type(payload).__name__}")
    return payload


def _source_ids_from_tasks_dir(tasks_dir: Path) -> set[str]:
    root = tasks_dir if tasks_dir.is_absolute() else REPO / tasks_dir
    if not root.exists():
        raise FileNotFoundError(root)

    source_ids: set[str] = set()
    for task_path in sorted(root.glob("**/task_*.json")):
        data = json.loads(task_path.read_text(encoding="utf-8"))
        provenance = data.get("_provenance") or {}
        source_id = str(provenance.get("source_id") or "").strip()
        if source_id:
            source_ids.add(source_id)
            continue

        for source in data.get("datasets_used") or []:
            match = re.search(r"#([0-9a-f]{24}):", str(source))
            if match:
                source_ids.add(match.group(1))
    return source_ids


def _selected_examples(
    examples: list[dict],
    *,
    source_ids: set[str] | None,
    limit: int | None,
) -> Iterable[dict]:
    yielded = 0
    for example in examples:
        source_id = str(example.get("_id") or "")
        if source_ids is not None and source_id not in source_ids:
            continue
        yield example
        yielded += 1
        if limit is not None and yielded >= limit:
            break


def materialize_uploads(
    bucket_uri: str,
    staging_dir: Path = DEFAULT_STAGING_DIR,
    raw_path: Path = DEFAULT_RAW_PATH,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    source_ids: set[str] | None = None,
    limit: int | None = None,
) -> list[UploadItem]:
    bucket, prefix = parse_bucket_uri(bucket_uri)
    examples = _load_raw_examples(raw_path)
    items: list[UploadItem] = []
    manifest_rows: list[dict[str, str]] = []

    for example in _selected_examples(examples, source_ids=source_ids, limit=limit):
        source_id = str(example.get("_id") or "")
        if not source_id:
            continue
        used_filenames: set[str] = set()
        context = example.get("context") or []
        for entry in context:
            if not isinstance(entry, list) or len(entry) != 2:
                continue
            title, sentences = entry
            title = str(title)
            if not isinstance(sentences, list):
                continue

            relative_key = (
                f"wikipedia/hotpotqa__{source_id}/files/"
                f"{_paragraph_filename(title, used_filenames)}"
            )
            key = _join_key(prefix, relative_key)
            local_path = staging_dir / relative_key
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_text(_context_text(source_id, title, sentences), encoding="utf-8")

            item = UploadItem(
                local_path=local_path,
                bucket=bucket,
                key=key,
                source_id=source_id,
                title=title,
            )
            items.append(item)
            manifest_rows.append(
                {
                    "s3_uri": item.s3_uri,
                    "dataset_id": f"hotpotqa__{source_id}",
                    "source_id": source_id,
                    "title": title,
                }
            )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as handle:
        for row in manifest_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    return items


def _upload_with_boto3(items: list[UploadItem]) -> list[UploadItem]:
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("boto3 is required for --uploader boto3") from exc

    s3_client = boto3.client("s3")
    for item in items:
        s3_client.upload_file(str(item.local_path), item.bucket, item.key)
    return items


def _upload_with_aws_cli(items: list[UploadItem], run_command=None) -> list[UploadItem]:
    if run_command is None:
        run_command = lambda command: subprocess.run(command, check=True)

    for item in items:
        run_command(["aws", "s3", "cp", str(item.local_path), item.s3_uri])
    return items


def upload_materialized_files(
    items: list[UploadItem],
    s3_client=None,
    uploader: str = "auto",
    run_command=None,
) -> list[UploadItem]:
    if s3_client is not None:
        for item in items:
            s3_client.upload_file(str(item.local_path), item.bucket, item.key)
        return items

    if uploader == "aws-cli":
        return _upload_with_aws_cli(items, run_command=run_command)
    if uploader == "boto3":
        return _upload_with_boto3(items)
    if uploader != "auto":
        raise ValueError(f"unknown uploader {uploader!r}; expected auto, boto3, or aws-cli")

    try:
        return _upload_with_boto3(items)
    except RuntimeError:
        return _upload_with_aws_cli(items, run_command=run_command)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stage and upload label-safe HotpotQA context paragraphs to S3.",
    )
    parser.add_argument(
        "--bucket-uri",
        default=DEFAULT_BUCKET_URI,
        help=(
            "Target S3 URI, optionally with prefix. For the existing agent_tools "
            "backend, use the bucket root with no prefix, e.g. s3://sana-hotpotqa-2, "
            "so uploaded keys start with wikipedia/."
        ),
    )
    parser.add_argument(
        "--raw-path",
        type=Path,
        default=DEFAULT_RAW_PATH,
        help="Path to hotpot_dev_distractor_v1.json",
    )
    parser.add_argument(
        "--tasks-dir",
        type=Path,
        default=DEFAULT_TASKS_DIR,
        help="Restrict upload to source IDs referenced by task_*.json files under this directory.",
    )
    parser.add_argument(
        "--all-raw",
        action="store_true",
        help="Upload every raw HotpotQA example instead of only source IDs from --tasks-dir/--source-id.",
    )
    parser.add_argument(
        "--staging-dir",
        type=Path,
        default=DEFAULT_STAGING_DIR,
        help="Directory for upload-ready context text files",
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help="JSONL manifest path for hybrid-search indexing",
    )
    parser.add_argument(
        "--source-id",
        action="append",
        default=None,
        help="Restrict upload to a HotpotQA source id. Repeat for multiple ids.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of examples materialized after source-id filtering",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Materialize files and print the upload plan without calling S3",
    )
    parser.add_argument(
        "--uploader",
        choices=("auto", "boto3", "aws-cli"),
        default="auto",
        help="Upload backend. auto uses boto3 when available, otherwise AWS CLI.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be >= 0")

    source_ids = set(args.source_id) if args.source_id else None
    if not args.all_raw and source_ids is None:
        source_ids = _source_ids_from_tasks_dir(args.tasks_dir)

    items = materialize_uploads(
        bucket_uri=args.bucket_uri,
        staging_dir=args.staging_dir,
        raw_path=args.raw_path,
        manifest_path=args.manifest_path,
        source_ids=source_ids,
        limit=args.limit,
    )

    for item in items:
        print(f"{item.local_path} -> {item.s3_uri}")
    print(f"manifest: {args.manifest_path} ({len(items)} rows)")

    if args.dry_run:
        return 0

    upload_materialized_files(items, uploader=args.uploader)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
