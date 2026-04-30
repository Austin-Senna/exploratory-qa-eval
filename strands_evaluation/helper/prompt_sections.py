"""Helpers for persistent agent-authored system-prompt sections."""

from __future__ import annotations

import re
from typing import Dict, Iterable, Tuple


_KNOWN_HEADINGS = ("CURRENT PLAN", "CURRENT SPRINT")
_SECTION_RE = re.compile(r"(?P<prefix>\A|\n\n)## (?P<heading>CURRENT PLAN|CURRENT SPRINT)\n")


def split_prompt_sections(prompt: str) -> Tuple[str, Dict[str, str]]:
    """Split a prompt into base text and known persistent sections."""
    text = prompt or ""
    matches = list(_SECTION_RE.finditer(text))
    if not matches:
        return text, {}

    base = text[: matches[0].start()]
    sections: Dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[match.group("heading")] = text[start:end].strip()
    return base, sections


def upsert_prompt_section(
    prompt: str,
    heading: str,
    body: str,
    *,
    ordered_headings: Iterable[str] = _KNOWN_HEADINGS,
) -> str:
    """Insert or replace a known prompt section, preserving section order."""
    normalized_heading = heading.strip().upper()
    if normalized_heading not in _KNOWN_HEADINGS:
        raise ValueError(f"Unknown prompt section heading: {heading!r}")

    base, sections = split_prompt_sections(prompt)
    sections[normalized_heading] = (body or "").strip()

    out = base.rstrip()
    for section_heading in ordered_headings:
        if section_heading in sections:
            out += f"\n\n## {section_heading}\n{sections[section_heading]}"
    return out


__all__ = ["split_prompt_sections", "upsert_prompt_section"]
