"""Load YAML demo scenarios from this package directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_SCENARIO_DIR = Path(__file__).resolve().parent


@dataclass
class Scenario:
    """A named, ordered list of user prompts for the automated demo."""

    name: str
    description: str
    turns: list[str]


def load_scenario(scenario_id: str = "telecom_support") -> Scenario:
    """Load a scenario YAML by id (filename without extension)."""
    path = _SCENARIO_DIR / f"{scenario_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Unknown scenario: {scenario_id}")
    data = yaml.safe_load(path.read_text())
    return Scenario(
        name=data["name"],
        description=data.get("description", ""),
        turns=list(data["turns"]),
    )
