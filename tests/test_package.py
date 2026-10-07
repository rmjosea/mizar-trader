"""Tests for the installed mizar distribution."""

import importlib.metadata
import sys

import mizar


def test_installed_package_runs_on_the_pinned_python() -> None:
    metadata = importlib.metadata.metadata("mizar-trader")

    assert mizar.__doc__
    assert metadata["Requires-Python"].replace(" ", "") == ">=3.14,<3.15"
    assert sys.version_info[:2] == (3, 14)
