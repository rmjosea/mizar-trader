"""Start the Compose stack and verify health, recovery, ports and secret hygiene.

Runs on the host with the standard library only. It never reads .env; it asks
Docker for published ports and reads the one non-secret timeout it needs from
the api container. Set STACK_CHECK_SENTINEL to the password value used in .env
to also prove that the container logs never contain it.
"""

from __future__ import annotations

import json
import os
import platform
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import Any

# Fixed arguments, run without a shell: the S603 and S607 noqa below are safe.
COMPOSE = ["docker", "compose"]
RECOVERY_LIMIT_SECONDS = 60.0


def compose(*args: str) -> str:
    """Run a docker compose command and return its standard output."""
    result = subprocess.run(  # noqa: S603
        [*COMPOSE, *args], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit(f"FAIL docker compose {' '.join(args)}:\n{result.stderr.strip()}")
    return result.stdout


def published(service: str) -> list[tuple[str, int]]:
    """Return the (host address, port) pairs a service publishes."""
    raw = compose("ps", "--format", "json", service).strip()
    # Compose prints untyped JSON (an array in old versions, one object per
    # line in new ones); each value is converted to str or int right below.
    rows: list[dict[str, Any]] = (
        json.loads(raw)
        if raw.startswith("[")
        else [json.loads(line) for line in raw.splitlines()]
    )
    pairs: list[tuple[str, int]] = []
    for row in rows:
        publishers: list[dict[str, Any]] = row.get("Publishers") or []
        pairs += [
            (str(p["URL"]), int(p["PublishedPort"]))
            for p in publishers
            if p.get("PublishedPort")
        ]
    return pairs


def health(port: int) -> tuple[int, str, float]:
    """Call GET /health and return status code, body and elapsed seconds."""
    started = time.monotonic()
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/health", timeout=30
        ) as reply:
            return reply.status, reply.read().decode(), time.monotonic() - started
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode(), time.monotonic() - started


def started_at(service: str) -> str:
    """Return the start time Docker recorded for a service's container."""
    container = compose("ps", "-q", service).strip()
    result = subprocess.run(  # noqa: S603
        ["docker", "inspect", "--format", "{{.State.StartedAt}}", container],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def non_loopback_address() -> str | None:
    """Return this host's outbound interface address, or None when offline."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        try:
            # A UDP connect only selects a route; it sends no packet.
            probe.connect(("192.0.2.1", 9))
        except OSError:
            return None
        address = str(probe.getsockname()[0])
    return None if address.startswith("127.") else address


def accepts_connections(address: str, port: int) -> bool:
    """Report whether a TCP connection to address:port succeeds."""
    try:
        with socket.create_connection((address, port), timeout=2):
            return True
    except OSError:
        return False


def main() -> int:
    """Run every stack check and return a process exit code."""
    failures: list[str] = []

    def check(passed: bool, label: str) -> None:
        print(f"{'OK  ' if passed else 'FAIL'} {label}")
        if not passed:
            failures.append(label)

    print(f"INFO host architecture: {platform.machine()}")
    compose("up", "-d", "--build", "--wait")
    check(True, "stack started and reported healthy")

    ports = {service: published(service) for service in ("api", "postgres")}
    addresses = {address for pairs in ports.values() for address, _ in pairs}
    check(
        addresses == {"127.0.0.1"},
        f"ports published on loopback only: {sorted(addresses)}",
    )
    api_port = ports["api"][0][1]
    postgres_port = ports["postgres"][0][1]

    outside = non_loopback_address()
    if outside is None:
        print("SKIP postgres unreachable from a non-loopback address (no such address)")
    else:
        check(
            not accepts_connections(outside, postgres_port),
            "postgres refuses a non-loopback address",
        )

    status, body, _ = health(api_port)
    check(
        status == 200 and json.loads(body) == {"status": "ok", "database": "ok"},
        f"/health with database up: {status} {body}",
    )

    api_started = started_at("api")
    timeout = float(
        compose("exec", "-T", "api", "printenv", "HEALTH_TIMEOUT_SECONDS").strip()
    )

    def expect_unavailable(situation: str) -> None:
        status, body, elapsed = health(api_port)
        check(
            status == 503
            and json.loads(body)["database"] == "database unavailable"
            and elapsed <= timeout + 1,
            f"/health with database {situation}: {status} {body} in {elapsed:.2f}s (timeout {timeout}s)",
        )

    def expect_recovery(situation: str) -> None:
        deadline = time.monotonic() + RECOVERY_LIMIT_SECONDS
        status = 0
        while time.monotonic() < deadline:
            status, _, _ = health(api_port)
            if status == 200:
                break
            time.sleep(1)
        check(status == 200, f"/health recovers after database {situation}: {status}")

    # A paused container keeps its socket open but never answers: a hang.
    compose("pause", "postgres")
    expect_unavailable("hanging")
    compose("unpause", "postgres")
    expect_recovery("hang")

    compose("stop", "postgres")
    expect_unavailable("stopped")
    compose("start", "postgres")
    expect_recovery("restart")
    check(started_at("api") == api_started, "api was not restarted")

    sentinel = os.environ.get("STACK_CHECK_SENTINEL")
    if sentinel:
        logs = compose("logs", "--no-color")
        check(
            sentinel not in logs,
            f"secret absent from {len(logs.splitlines())} container log lines",
        )
    else:
        print("SKIP secret check (STACK_CHECK_SENTINEL not set)")

    print(f"stack_check: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
