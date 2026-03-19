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
    run_id: Optional[str],
    model: Optional[str],
    batch: Optional[str],
) -> str:
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_part = _slugify(model)
    batch_part = _slugify(batch)
    parts = ["agent"]
    if model_part:
        parts.append(model_part)
    if batch_part:
        parts.append(batch_part)
    parts.append(run_id or timestamp)
    parts.append(f"pid{os.getpid()}")
    filename = "_".join(parts) + ".log"
    return os.path.join(log_dir, filename)


def configure_logging(
    log_dir: str = "logs",
    run_id: Optional[str] = None,
    model: Optional[str] = None,
    batch: Optional[str] = None,
    level: int = logging.DEBUG,
) -> None:
    """Configure file + console handlers on the strands and strands_evaluation root loggers.

    Call once per process before creating any Agent. Worker processes call this inside
    _run_task_worker before constructing DataLakeAgent.
    """
    log_file = _build_log_file(log_dir, run_id, model, batch)

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
