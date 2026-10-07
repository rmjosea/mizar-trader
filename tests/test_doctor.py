"""Tests for the host diagnostic in scripts/doctor.py."""

import ast
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

from tests.conftest import SENTINEL_PASSWORD

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("doctor", REPO / "scripts" / "doctor.py")
if _spec is None or _spec.loader is None:
    raise ImportError("cannot load scripts/doctor.py")
doctor = importlib.util.module_from_spec(_spec)
# dataclasses resolve the module through sys.modules while it executes.
sys.modules["doctor"] = doctor
_spec.loader.exec_module(doctor)

GB = 10**9
# doctor is loaded from a file path, so Pyright cannot see its types; the
# helpers below use Any for its objects.


def healthy_probes(**overrides: object) -> Any:
    """Return probes for a host where every check passes, with overrides."""
    values: dict[str, object] = {
        "machine": lambda: "arm64",
        "docker_memory": lambda: 16 * GB,
        "uv_status": lambda: (True, True),
        "free_disk": lambda: 100 * GB,
        "clock_offset": lambda: 0.1,
        "unreachable": list,
    }
    values.update(overrides)
    return doctor.Probes(**values)


def write_env_files(root: Path, env: str | None) -> None:
    """Create .env.example with two variables and, optionally, a .env."""
    (root / ".env.example").write_text(
        "# comment\nA=placeholder\nPOSTGRES_PASSWORD=x\n"
    )
    if env is not None:
        (root / ".env").write_text(env)


def statuses(results: list[Any]) -> dict[str, str]:
    """Map each check name to its status."""
    return {r.name: r.status for r in results}


def test_healthy_host_passes(tmp_path: Path) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")

    results = doctor.collect(tmp_path, healthy_probes())

    assert set(statuses(results).values()) == {"OK"}
    assert doctor.exit_code(results) == 0


def test_missing_env_variable_is_named_and_fails(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_env_files(tmp_path, f"POSTGRES_PASSWORD={SENTINEL_PASSWORD}\n")

    code = doctor.main(tmp_path, healthy_probes())

    output = capsys.readouterr().out
    assert code == 1
    assert "FAIL .env: missing A" in output
    assert SENTINEL_PASSWORD not in output


def test_missing_env_file_fails(tmp_path: Path) -> None:
    write_env_files(tmp_path, None)

    results = doctor.collect(tmp_path, healthy_probes())

    assert statuses(results)[".env"] == "FAIL"


@pytest.mark.parametrize(
    ("override", "check"),
    [
        ({"machine": lambda: "riscv64"}, "Architecture"),
        ({"docker_memory": lambda: None}, "Docker"),
        ({"free_disk": lambda: 19 * GB}, "Disk"),
        ({"uv_status": lambda: (False, False)}, "uv and Python"),
        ({"uv_status": lambda: (True, False)}, "uv and Python"),
    ],
)
def test_blocking_problems_fail(
    tmp_path: Path, override: dict[str, object], check: str
) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")

    results = doctor.collect(tmp_path, healthy_probes(**override))

    assert statuses(results)[check] == "FAIL"
    assert doctor.exit_code(results) == 1


def test_low_docker_memory_only_warns(tmp_path: Path) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")

    results = doctor.collect(tmp_path, healthy_probes(docker_memory=lambda: 4 * GB))

    assert statuses(results)["Docker"] == "WARN"
    assert doctor.exit_code(results) == 0


def test_offline_host_warns_but_passes(tmp_path: Path) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")
    offline = healthy_probes(
        clock_offset=lambda: None,
        unreachable=lambda: ["pypi.org", "registry-1.docker.io"],
    )

    results = doctor.collect(tmp_path, offline)

    assert statuses(results)["Clock"] == "WARN"
    assert statuses(results)["Connectivity"] == "WARN"
    assert doctor.exit_code(results) == 0


def test_large_clock_offset_warns(tmp_path: Path) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")

    results = doctor.collect(tmp_path, healthy_probes(clock_offset=lambda: -3.5))

    assert statuses(results)["Clock"] == "WARN"


def test_env_names_never_include_values(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        f"# POSTGRES_PASSWORD={SENTINEL_PASSWORD}\nexport A=1\n"
        f"POSTGRES_PASSWORD={SENTINEL_PASSWORD}\n\n"
    )

    names = doctor.variable_names(tmp_path / ".env")

    assert names == ["A", "POSTGRES_PASSWORD"]


def test_doctor_source_is_valid_python_3_9_syntax() -> None:
    source = (REPO / "scripts" / "doctor.py").read_text(encoding="utf-8")

    ast.parse(source, feature_version=(3, 9))


def test_non_utf8_env_fails_cleanly_without_leaking(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_env_files(tmp_path, None)
    secret = b"caf\xe9-" + SENTINEL_PASSWORD.encode()
    (tmp_path / ".env").write_bytes(b"POSTGRES_PASSWORD=" + secret + b"\n")

    code = doctor.main(tmp_path, healthy_probes())

    output = capsys.readouterr().out
    assert code == 1
    assert "FAIL .env: missing A" in output
    assert SENTINEL_PASSWORD not in output
    assert "0xe9" not in output


def test_docker_memory_uses_decimal_gigabytes(tmp_path: Path) -> None:
    write_env_files(tmp_path, "A=1\nPOSTGRES_PASSWORD=y\n")

    results = doctor.collect(
        tmp_path, healthy_probes(docker_memory=lambda: 8_232_894_464)
    )

    assert statuses(results)["Docker"] == "OK"
