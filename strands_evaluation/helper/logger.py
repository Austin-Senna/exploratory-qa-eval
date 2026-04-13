"""
Logging helpers for the Strands evaluation runner.

Extracted from agent_runner.py.
"""

import logging
import os
import re
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)  # "strands_evaluation.helper.logger" — never configured here


def _slugify(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())


def _build_log_file(
    log_dir: str,
    condition: Optional[str],
    model: Optional[str],
    task_id: Optional[str],
) -> str:
    from pathlib import Path
    # Build: logs/{condition}/{model}/{task_dir}/{task_stem}.log
    # e.g.  logs/a/claude-haiku-4-5/k-2-d-1/task_1.log
    subdir = log_dir
    if condition:
        # Allow hierarchical condition labels like "naive_k5/baseline".
        for part in str(condition).replace("\\", "/").split("/"):
            if part:
                subdir = os.path.join(subdir, _slugify(part))
    if model:
        subdir = os.path.join(subdir, _slugify(model))
    if task_id:
        p = Path(task_id)
        subdir = os.path.join(subdir, p.parent.name)
        filename = p.stem + ".log"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"agent_{timestamp}_pid{os.getpid()}.log"
    os.makedirs(subdir, exist_ok=True)
    return os.path.join(subdir, filename)


def configure_logging(
    log_dir: str = "logs",
    run_id: Optional[str] = None,
    model: Optional[str] = None,
    batch: Optional[str] = None,
    condition: Optional[str] = None,
    task_id: Optional[str] = None,
    level: int = logging.DEBUG,
) -> None:
    """Configure file + console handlers on the strands and strands_evaluation root loggers.

    Call once per process before creating any Agent. Worker processes call this inside
    _run_task_worker before constructing DataLakeAgent.
    """
    log_file = _build_log_file(log_dir, condition, model, task_id)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))

    # Application logger — full verbosity to file + console
    app_root = logging.getLogger("strands_evaluation")
    app_root.setLevel(level)
    app_root.handlers = []
    app_root.addHandler(file_handler)
    app_root.addHandler(console_handler)
    app_root.propagate = False

    # SDK logger — WARNING only (suppresses tool registry, plugin discovery, request body dumps)
    sdk_root = logging.getLogger("strands")
    sdk_root.setLevel(logging.WARNING)
    sdk_root.handlers = []
    sdk_root.addHandler(file_handler)   # warnings/errors still go to file
    sdk_root.propagate = False

    # Re-enable retry INFO logs from SDK (throttle/retry events are useful)
    logging.getLogger("strands.event_loop._retry").setLevel(logging.INFO)

    logger.info(f"Logging to: {log_file}")


def configure_worker_logging(
    run_config,
    *,
    model: Optional[str] = None,
    condition: Optional[str] = None,
    task_id: Optional[str] = None,
    level: int = logging.DEBUG,
) -> None:
    """Configure per-task logging using the run-configured log root."""
    configure_logging(
        log_dir=getattr(run_config, "logs_output_dir", "logs") or "logs",
        model=model,
        condition=condition,
        task_id=task_id,
        level=level,
    )
