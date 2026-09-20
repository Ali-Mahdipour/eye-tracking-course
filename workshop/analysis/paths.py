"""Repository path helpers so notebooks work from workshop/sessions/."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def data_path(*parts: str) -> Path:
    return REPO_ROOT / "Data" / Path(*parts)


def stimuli_path(*parts: str) -> Path:
    return REPO_ROOT / "Stimuli" / Path(*parts)
