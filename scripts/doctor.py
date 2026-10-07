"""Check that this host can develop and run Mizar Trader.

Standard library only and Python 3.9+, so it runs before uv exists. It prints
one line per check (OK, WARN or FAIL) and exits 1 if any check fails. It reads
variable names from .env, never their values.
"""

from __future__ import annotations

import http.client
import platform
import shutil
import socket
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

# Decimal gigabytes, the unit the limits are written in.
GB = 10**9
# Provisional limits; adjust them here when measurements say so.
MIN_FREE_DISK_BYTES = 20 * GB
MIN_DOCKER_MEMORY_BYTES = 8 * GB
MAX_CLOCK_OFFSET_SECONDS = 2.0
SUPPORTED_MACHINES = {"arm64", "aarch64", "x86_64", "amd64"}
NTP_SERVER = "time.cloudflare.com"
NTP_EPOCH_OFFSET = 2208988800
REQUIRED_HOSTS = {
    "pypi.org": "https://pypi.org/simple/",
    "registry-1.docker.io": "https://registry-1.docker.io/v2/",
}


@dataclass(frozen=True)
class Result:
    """Outcome of one check.

    Attributes:
        status: ``OK``, ``WARN`` or ``FAIL``.
        name: Short check name shown to the operator.
        detail: What was found; never a secret value.
    """

    status: str
    name: str
    detail: str


@dataclass(frozen=True)
class Probes:
    """Functions that observe the host; tests replace them with fakes.

    Attributes:
        machine: Returns the CPU architecture name.
        docker_memory: Returns memory available to Docker in bytes, or None
            when the engine is not reachable.
        uv_status: Returns (uv found, Python 3.14 available through uv).
        free_disk: Returns free bytes on the repository's file system.
        clock_offset: Returns host clock minus NTP time in seconds, or None.
        unreachable: Returns the names of required hosts that did not answer.
    """

    machine: Callable[[], str]
    docker_memory: Callable[[], int | None]
    uv_status: Callable[[], tuple[bool, bool]]
    free_disk: Callable[[], int]
    clock_offset: Callable[[], float | None]
    unreachable: Callable[[], list[str]]


def run_quietly(command: list[str]) -> str | None:
    """Run a command without a shell; return its stdout, or None on failure."""
    if shutil.which(command[0]) is None:
        return None
    try:
        result = subprocess.run(  # noqa: S603
            command, capture_output=True, text=True, timeout=20, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def docker_memory() -> int | None:
    """Return the memory the Docker engine reports, or None if unreachable."""
    output = run_quietly(["docker", "info", "--format", "{{.MemTotal}}"])
    return int(output.strip()) if output and output.strip().isdigit() else None


def uv_status() -> tuple[bool, bool]:
    """Report whether uv exists and can provide Python 3.14."""
    if shutil.which("uv") is None:
        return False, False
    return True, run_quietly(["uv", "python", "find", "3.14"]) is not None


def clock_offset() -> float | None:
    """Measure the host clock against one SNTP answer; None if impossible."""
    request = b"\x1b" + 47 * b"\0"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)
            sent = time.time()
            sock.sendto(request, (NTP_SERVER, 123))
            answer = sock.recv(48)
            received = time.time()
    except OSError:
        return None
    if len(answer) < 48:
        return None
    seconds, fraction = struct.unpack("!II", answer[40:48])
    server_time = seconds - NTP_EPOCH_OFFSET + fraction / 2**32
    return (sent + received) / 2 - server_time


def unreachable_hosts() -> list[str]:
    """Return the required hosts that give no HTTP answer within 5 seconds."""
    missing: list[str] = []
    for name, url in REQUIRED_HOSTS.items():
        try:
            urllib.request.urlopen(url, timeout=5).close()  # noqa: S310
        except urllib.error.HTTPError:
            continue  # Any HTTP status, even 401, proves the host answers.
        except (OSError, ValueError, http.client.HTTPException):
            missing.append(name)
    return missing


def real_probes(root: Path) -> Probes:
    """Build the probes that observe this host."""
    return Probes(
        machine=platform.machine,
        docker_memory=docker_memory,
        uv_status=uv_status,
        free_disk=lambda: shutil.disk_usage(root).free,
        clock_offset=clock_offset,
        unreachable=unreachable_hosts,
    )


def variable_names(path: Path) -> list[str]:
    """Return the variable names assigned in an env file, dropping values.

    The parser is line-based: a quoted value spanning lines may hide a name.
    Bytes that are not UTF-8 are replaced, so decoding never raises with a
    piece of a secret in its message.
    """
    names: list[str] = []
    text = path.read_bytes().decode("utf-8", errors="replace")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name = stripped.split("=", 1)[0].strip()
        names.append(
            name[len("export ") :].strip() if name.startswith("export ") else name
        )
    return names


def check_env(root: Path) -> Result:
    """Check that .env sets every variable named in .env.example."""
    env_path = root / ".env"
    if not env_path.is_file():
        return Result("FAIL", ".env", "file missing; copy .env.example")
    try:
        present = set(variable_names(env_path))
        expected = variable_names(root / ".env.example")
    except OSError as err:
        return Result("FAIL", ".env", f"cannot read: {type(err).__name__}")
    missing = [name for name in expected if name not in present]
    if missing:
        return Result("FAIL", ".env", "missing " + ", ".join(missing))
    return Result("OK", ".env", "every variable of .env.example is set")


def collect(root: Path, probes: Probes) -> list[Result]:
    """Run every check and return the results in display order."""
    results: list[Result] = []

    machine = probes.machine()
    results.append(
        Result(
            "OK" if machine in SUPPORTED_MACHINES else "FAIL", "Architecture", machine
        )
    )

    memory = probes.docker_memory()
    if memory is None:
        results.append(Result("FAIL", "Docker", "engine not reachable"))
    elif memory < MIN_DOCKER_MEMORY_BYTES:
        results.append(
            Result(
                "WARN",
                "Docker",
                f"{memory / GB:.1f} GB memory, below {MIN_DOCKER_MEMORY_BYTES // GB} GB",
            )
        )
    else:
        results.append(Result("OK", "Docker", f"{memory / GB:.1f} GB memory"))

    has_uv, has_python = probes.uv_status()
    if not has_uv:
        results.append(Result("FAIL", "uv and Python", "uv not found"))
    elif not has_python:
        results.append(
            Result(
                "FAIL",
                "uv and Python",
                "Python 3.14 not installed; run `uv python install 3.14`",
            )
        )
    else:
        results.append(Result("OK", "uv and Python", "uv provides Python 3.14"))

    results.append(check_env(root))

    free = probes.free_disk()
    disk_status = "OK" if free >= MIN_FREE_DISK_BYTES else "FAIL"
    results.append(
        Result(
            disk_status,
            "Disk",
            f"{free / GB:.0f} GB free, minimum {MIN_FREE_DISK_BYTES // GB} GB",
        )
    )

    offset = probes.clock_offset()
    if offset is None:
        results.append(Result("WARN", "Clock", "offset could not be measured"))
    elif abs(offset) > MAX_CLOCK_OFFSET_SECONDS:
        results.append(
            Result(
                "WARN",
                "Clock",
                f"offset {offset:+.2f} s, limit {MAX_CLOCK_OFFSET_SECONDS} s",
            )
        )
    else:
        results.append(Result("OK", "Clock", f"offset {offset:+.2f} s"))

    unreachable = probes.unreachable()
    if unreachable:
        results.append(
            Result("WARN", "Connectivity", "unreachable: " + ", ".join(unreachable))
        )
    else:
        results.append(
            Result(
                "OK", "Connectivity", "package index and container registry reachable"
            )
        )
    return results


def exit_code(results: list[Result]) -> int:
    """Return 1 if any check failed, otherwise 0."""
    return 1 if any(r.status == "FAIL" for r in results) else 0


def main(root: Path, probes: Probes) -> int:
    """Print every check result and return the process exit code."""
    results = collect(root, probes)
    for result in results:
        print(f"{result.status:<4} {result.name}: {result.detail}")
    return exit_code(results)


if __name__ == "__main__":
    repository = Path(__file__).resolve().parent.parent
    sys.exit(main(repository, real_probes(repository)))
