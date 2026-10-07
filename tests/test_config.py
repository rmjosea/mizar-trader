"""Tests for environment-only configuration."""

import pytest

from mizar.config import ConfigurationError, load_settings
from tests.conftest import SENTINEL_PASSWORD, VALID_ENVIRONMENT


def test_complete_environment_loads(valid_env: dict[str, str]) -> None:
    settings = load_settings()

    assert settings.postgres_port == 5432
    assert settings.health_timeout_seconds == 2.0
    assert settings.postgres_password.get_secret_value() == SENTINEL_PASSWORD


@pytest.mark.parametrize("name", sorted(VALID_ENVIRONMENT))
def test_every_missing_variable_is_named_without_values(
    name: str, valid_env: dict[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(name)

    with pytest.raises(ConfigurationError) as raised:
        load_settings()

    assert raised.value.variables == [name]
    assert name in str(raised.value)
    assert SENTINEL_PASSWORD not in str(raised.value)
    assert raised.value.__cause__ is None
    assert raised.value.__suppress_context__


def test_empty_password_is_invalid(
    valid_env: dict[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("POSTGRES_PASSWORD", "")

    with pytest.raises(ConfigurationError) as raised:
        load_settings()

    assert raised.value.variables == ["POSTGRES_PASSWORD"]


def test_invalid_value_is_named(
    valid_env: dict[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("POSTGRES_PORT", "not-a-port")
    monkeypatch.setenv("HEALTH_TIMEOUT_SECONDS", "0")

    with pytest.raises(ConfigurationError) as raised:
        load_settings()

    assert raised.value.variables == ["HEALTH_TIMEOUT_SECONDS", "POSTGRES_PORT"]
    assert "not-a-port" not in str(raised.value)


def test_secret_is_masked_in_repr(valid_env: dict[str, str]) -> None:
    settings = load_settings()

    assert SENTINEL_PASSWORD not in repr(settings)
    assert SENTINEL_PASSWORD not in str(settings.model_dump())
