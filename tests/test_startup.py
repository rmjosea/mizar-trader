"""Tests for the api process entry point and its logs."""

import json

import pytest

from mizar.api.__main__ import main
from tests.conftest import SENTINEL_PASSWORD


def test_missing_variable_refuses_start_and_names_it(
    valid_env: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("POSTGRES_HOST")

    exit_code = main()

    stderr = capsys.readouterr().err
    record = json.loads(stderr.strip().splitlines()[-1])
    assert exit_code == 1
    assert record["level"] == "ERROR"
    assert "POSTGRES_HOST" in record["message"]
    assert SENTINEL_PASSWORD not in stderr
