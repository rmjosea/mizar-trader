"""Tests that configuration stays on the virtual-money side of the boundary."""

import re
from pathlib import Path

from mizar.config import Settings

REPO = Path(__file__).resolve().parents[1]
FORBIDDEN_NAME = re.compile(r"LIVE|BROKER|ALPACA|API_KEY|SECRET_KEY|TOKEN|ACCOUNT")


def example_variables() -> list[str]:
    """Return the variable names declared in .env.example."""
    lines = (REPO / ".env.example").read_text(encoding="utf-8").splitlines()
    return [
        line.split("=", 1)[0] for line in lines if line and not line.startswith("#")
    ]


def test_env_example_declares_exactly_the_settings() -> None:
    expected = sorted(name.upper() for name in Settings.model_fields)

    assert sorted(example_variables()) == expected


def test_no_live_provider_or_broker_variable_exists() -> None:
    names = example_variables() + [name.upper() for name in Settings.model_fields]

    assert [name for name in names if FORBIDDEN_NAME.search(name)] == []
