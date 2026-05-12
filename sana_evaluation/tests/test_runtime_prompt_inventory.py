"""Tests for checked-in runtime prompt inventory snapshots."""

from __future__ import annotations

from pathlib import Path


def test_runtime_inventory_uses_schema_knowledge_rule() -> None:
    inventory_dir = Path(__file__).resolve().parents[1] / "runtime_prompt_inventory"
    expected = "NEVER call `query_file` on a file you do not know the schema of."
    old = "NEVER call `query_file` on a file you have not first inspected with `peek_file`."

    for path in sorted(inventory_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        assert old not in text, path.name
        if "- query_file" in text:
            assert expected in text, path.name
