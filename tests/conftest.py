"""Shared fixtures: a complete, valid environment with a sentinel password."""

import pytest

# A fake value that tests search for in every output to prove it never leaks.
SENTINEL_PASSWORD = "sentinel-secret-7f3a9c"  # noqa: S105

VALID_ENVIRONMENT = {
    "API_HOST": "127.0.0.1",
    "API_PORT": "8000",
    "POSTGRES_HOST": "127.0.0.1",
    "POSTGRES_PORT": "5432",
    "POSTGRES_USER": "mizar",
    "POSTGRES_PASSWORD": SENTINEL_PASSWORD,
    "POSTGRES_DB": "mizar",
    "HEALTH_TIMEOUT_SECONDS": "2",
    "LOG_LEVEL": "INFO",
}


@pytest.fixture
def valid_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Set every required variable to a valid value and return the mapping."""
    for name, value in VALID_ENVIRONMENT.items():
        monkeypatch.setenv(name, value)
    return dict(VALID_ENVIRONMENT)
