"""
Load skills.md content and append it to a system prompt.

Usage:
    from strands_evaluation.tools.skills.load_skills import load_skills, append_skills

    # Get raw skills text
    text = load_skills()

    # Append to an existing prompt
    full_prompt = append_skills(system_prompt)
"""
from pathlib import Path

_SKILLS_PATH = Path(__file__).parent / "skills.md"


def load_skills() -> str:
    """Return the contents of skills.md."""
    return _SKILLS_PATH.read_text(encoding="utf-8")


def append_skills(system_prompt: str) -> str:
    """Append skills reference to a system prompt."""
    return system_prompt + "\n\n## SKILLS REFERENCE\n" + load_skills()
