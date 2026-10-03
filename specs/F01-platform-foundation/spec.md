---
id: SPEC-F01
title: Platform foundation
status: draft
depends_on: []
---

# Platform foundation

Makes Mizar Trader a runnable, checkable project on any machine with Docker:
one command validates the host, one starts the API with an empty PostgreSQL,
and one runs every check that CI also runs. Every later block builds on it.

## Contents

- Context
- Outcome
- Scope
- Requirements (REQ-001 to REQ-009)
- Acceptance criteria (AC-001 to AC-012)
- Failure behavior and edge cases
- Changes to the baseline docs
- Open questions

## Context

Backlog block F01 ([backlog](../../docs/delivery/01-backlog.md), Gate 0) is
the first block; nothing executable exists yet. Constraints come from
[01-system](../../docs/architecture/01-system.md) (process shape, stack),
[03-local-runtime](../../docs/architecture/03-local-runtime.md) (runtime and
`make doctor`), [python.md](../../docs/engineering/python.md) §2 (toolchain),
[03-test-strategy](../../docs/delivery/03-test-strategy.md) (CI without keys
or network) and [04-security](../../docs/architecture/04-security-and-live-boundary.md)
(secrets, execution boundary). Python 3.14 is fixed by
[OD-07](../../docs/product/open-decisions.md).

## Outcome

On a fresh clone, on Linux or macOS and on arm64 or amd64, an operator or agent
can validate the host, start a healthy `api` and empty `postgres`, and run the
full check suite; CI runs the same suite on every pull request without secrets.

## Scope

### In scope

- Python project: Python 3.14, locked dependencies, `src/` layout, the
  toolchain of [python.md](../../docs/engineering/python.md) §2.
- One local check command, equal to what CI runs, including the harness checks.
- CI workflow for pull requests and pushes to `main`.
- Container stack with two services: `api` and an empty `postgres`.
- Health endpoint `/health` used as the `api` container healthcheck.
- Environment-based configuration and `.env.example`.
- Host diagnostic `make doctor`.
- Updates to `AGENTS.md` §8 and `03-local-runtime.md`.

### Out of scope

- Domain schemas, migrations, event journal (block F02).
- Object store ([OD-06](../../docs/product/open-decisions.md) is open).
- Worker process, web dashboard, API authentication.
- Data providers and any provider or broker key.
- Cloud deployment ([OD-09](../../docs/product/open-decisions.md)).
- Native Windows; Windows is supported only through WSL2.

## Requirements

### REQ-001: Reproducible Python project

The interpreter is pinned to Python 3.14 in one place that CI also reads, all
dependencies are locked in a committed lock file, and the toolchain follows
[python.md](../../docs/engineering/python.md) §2 (format, lint, strict types,
tests with branch coverage, import boundaries, vulnerability scan).

### REQ-002: One check command equal to CI

A single local command runs every check CI runs, in the same configuration, and
exits non-zero if any check fails. It includes `scripts/check_harness.py` and
the harness tests. Tests never use the network or the wall clock; only the
vulnerability scan may reach the network.

### REQ-003: CI without secrets

CI runs REQ-002 on every pull request and every push to `main`, with the
Python version from REQ-001 and no repository secrets. CI also starts the
container stack (REQ-004) and verifies REQ-005 on amd64.

### REQ-004: Portable container stack

One command starts `api` and an empty `postgres` with native images for both
arm64 and amd64 (no mandatory emulation). PostgreSQL listens only on the
loopback interface of the host by default. `api` waits for `postgres` to be
healthy before it reports itself healthy.

### REQ-005: Health reflects the database

`GET /health` answers 200 with the database reported as `ok` when PostgreSQL
accepts a query, and 503 with the reason `database unavailable` otherwise,
within the configured health timeout. The response contains no connection
string, credential, host name or dependency version. The `api` recovers on its
own when PostgreSQL returns.

### REQ-006: Explicit configuration

Every setting comes from the environment. `.env.example` lists every variable
with a placeholder value and contains no real secret and no provider, broker or
live-trading variable. If a required variable is missing or invalid, `api`
refuses to start and names the variable; it never falls back to a silent
default.

### REQ-007: Host diagnostic

`make doctor` checks the host and prints one line per check with `OK`, `WARN`
or `FAIL`. It exits 1 if any check is `FAIL`, otherwise 0.

| Check | FAIL when | WARN when |
|---|---|---|
| Architecture | not arm64 or amd64 | — |
| Docker | engine not reachable | memory available to Docker below the minimum |
| uv and Python | uv missing, or uv cannot provide Python 3.14 | — |
| `.env` | file missing, or a variable of `.env.example` missing | — |
| Disk | free space below the minimum | — |
| Clock | — | offset above the limit, or offset cannot be measured |
| Connectivity | — | package index or container registry unreachable |

Minimums and limits are provisional configuration: disk 20 GB free, Docker
memory 8 GB, clock offset 2 s.

### REQ-008: No secret in any output

No output of `make doctor`, `/health`, application logs, the check command or
CI contains the value of a secret. `make doctor` names variables, never values.

### REQ-009: Documentation current

`AGENTS.md` §8 lists the real commands for checks, stack start and doctor, and
`03-local-runtime.md` describes the portable runtime (see "Changes to the
baseline docs").

## Acceptance criteria

- AC-001: WHEN the check command runs on a clean checkout,
  THE check command SHALL exit 0, and SHALL exit non-zero after a deliberate
  lint, type or test failure is introduced. (REQ-001, REQ-002)
- AC-002: WHEN a pull request is opened with no repository secrets configured,
  THE CI workflow SHALL run the same steps as the check command on the pinned
  Python and pass. (REQ-002, REQ-003)
- AC-003: WHEN the stack is started on arm64 (operator machine) and on amd64
  (CI), THE stack SHALL report both services healthy and `GET /health` SHALL
  return 200 with the database `ok`. (REQ-004, REQ-005)
- AC-004: IF PostgreSQL is stopped while `api` runs, THEN `GET /health` SHALL
  return 503 with reason `database unavailable` within the health timeout, and
  WHEN PostgreSQL is back, SHALL return 200 without restarting `api`. (REQ-005)
- AC-005: IF a required variable is missing from the environment, THEN `api`
  SHALL refuse to start and name the variable. (REQ-006)
- AC-006: IF `.env` lacks a variable declared in `.env.example`, THEN
  `make doctor` SHALL print `FAIL` naming that variable and exit 1. (REQ-007)
- AC-007: IF the architecture is neither arm64 nor amd64, or Docker is not
  reachable, or free disk is below the minimum, THEN `make doctor` SHALL exit 1.
  (REQ-007)
- AC-008: IF there is no network, THEN `make doctor` SHALL report the clock
  and connectivity checks as `WARN` and still exit 0 when nothing else fails.
  (REQ-007)
- AC-009: WHEN a sentinel secret value is placed in every secret variable and
  doctor, `/health`, startup logs and the failing-start path are exercised,
  THE captured output SHALL NOT contain the sentinel. (REQ-008)
- AC-010: WHEN the stack starts on the host, PostgreSQL SHALL NOT accept
  connections on a non-loopback interface by default. (REQ-004)
- AC-011: THE repository SHALL contain no live-trading variable, endpoint or
  credential, and `.env.example` SHALL contain no provider or broker key.
  (REQ-006)
- AC-012: WHEN the block is complete, `AGENTS.md` §8 SHALL list commands that
  run successfully as written. (REQ-009)

## Failure behavior and edge cases

- PostgreSQL hangs instead of refusing: `/health` still answers 503 within the
  timeout (AC-004).
- PostgreSQL starts slower than `api`: `api` is not reported healthy until the
  database answers; no crash loop is required to recover.
- Offline host: checks and tests still run; only the vulnerability scan, clock
  and connectivity checks need the network.
- Host without enough memory: doctor warns; it does not block development.

## Changes to the baseline docs

- `docs/architecture/03-local-runtime.md`: target becomes any host with Docker
  on Linux or macOS, arm64 or amd64 (Windows through WSL2); the MacBook
  M1 Pro is the reference development machine; images are native on both
  architectures; `make doctor` behavior links to this spec.
- `docs/README.md`: the 03-local-runtime index row stops naming only Apple
  Silicon.

## Open questions

None. The health timeout value is a plan choice; it is configuration, like
the provisional values in REQ-007.
