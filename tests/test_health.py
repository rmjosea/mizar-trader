"""Tests for the database health check and the /health endpoint."""

import asyncio
import logging
import socket
import time
from collections.abc import Awaitable, Callable

import pytest
from fastapi.testclient import TestClient

from mizar.api.app import create_app
from mizar.api.health import check_database
from mizar.config import Settings, load_settings
from tests.conftest import SENTINEL_PASSWORD


def free_port() -> int:
    """Return a loopback port with no listener."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def settings_for(
    monkeypatch: pytest.MonkeyPatch, port: int, timeout: str = "0.5"
) -> Settings:
    """Load settings that point the database at a local test port."""
    monkeypatch.setenv("POSTGRES_PORT", str(port))
    monkeypatch.setenv("HEALTH_TIMEOUT_SECONDS", timeout)
    return load_settings()


def fixed_probe(*results: bool) -> Callable[[], Awaitable[bool]]:
    """Build a probe that returns the given results in order."""
    remaining = list(results)

    async def probe() -> bool:
        return remaining.pop(0)

    return probe


def test_health_is_ok_when_database_answers(valid_env: dict[str, str]) -> None:
    client = TestClient(create_app(load_settings(), database_probe=fixed_probe(True)))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_recovers_without_restart(valid_env: dict[str, str]) -> None:
    probe = fixed_probe(False, True)
    client = TestClient(create_app(load_settings(), database_probe=probe))

    down = client.get("/health")
    up = client.get("/health")

    assert down.status_code == 503
    assert down.json() == {"status": "unavailable", "database": "database unavailable"}
    assert up.status_code == 200


def test_refused_connection_gives_503_without_secrets(
    valid_env: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    settings = settings_for(monkeypatch, free_port())
    client = TestClient(create_app(settings))

    with caplog.at_level(logging.DEBUG):
        response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["database"] == "database unavailable"
    assert SENTINEL_PASSWORD not in response.text
    assert SENTINEL_PASSWORD not in caplog.text
    assert "127.0.0.1" not in response.text


def test_hanging_database_is_reported_within_timeout(
    valid_env: dict[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    async def scenario() -> tuple[bool, float]:
        async def never_answer(
            reader: asyncio.StreamReader, writer: asyncio.StreamWriter
        ) -> None:
            await reader.read()
            writer.close()

        server = await asyncio.start_server(never_answer, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        settings = settings_for(monkeypatch, port, timeout="0.3")
        started = time.monotonic()
        healthy = await check_database(settings)
        elapsed = time.monotonic() - started
        server.close()
        await server.wait_closed()
        return healthy, elapsed

    healthy, elapsed = asyncio.run(scenario())

    assert healthy is False
    assert elapsed < 1.0
