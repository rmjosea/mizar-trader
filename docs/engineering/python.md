# Python engineering standard

How Python code in Mizar Trader is written, typed, tested and secured. It is
normative for all application code; docstrings follow
[`code-documentation.md`](code-documentation.md) and model-calling code also
follows [`ai-model-code.md`](ai-model-code.md).

## Contents

1. Principles
2. Toolchain and project layout
3. Types and data models
4. Errors
5. Money
6. Time
7. Concurrency
8. Module boundaries
9. Persistence and API
10. Testing
11. Logging
12. Security and dependencies
13. References

## 1. Principles

- The simplest solution that fully meets the accepted need wins. Every
  abstraction, parameter and configuration flag serves a current requirement;
  delete what no longer does.
- Readability over cleverness: explicit code, small functions, no mutable
  global state, no metaprogramming unless a contract requires it.
- Keep `try` blocks as small as the operation that can fail.
- Profile before optimizing; use vectorized Parquet/DuckDB reads for analytics
  instead of Python loops over rows.

## 2. Toolchain and project layout

Backlog block F01 creates this setup; the commands then go in `AGENTS.md`
section 8.

| Concern | Tool and rule |
|---|---|
| Interpreter | Python 3.14 ([OD-07](../product/open-decisions.md), resolved); pinned in `.python-version` and `requires-python`; CI reads `.python-version` |
| Environments and dependencies | `uv`; `uv.lock` is committed; CI runs `uv sync --locked` |
| Development tools | `[dependency-groups]` (PEP 735), not optional extras |
| Lint and format | Ruff: `ruff format` and `ruff check`, version pinned |
| Types | Pyright in `strict` mode is the blocking gate: it follows the typing specification most closely and checks unannotated code too |
| Tests | pytest, Hypothesis, coverage with branch measurement |
| Module boundaries | import-linter contracts (section 8) |
| Vulnerabilities | `pip-audit`; switch to `uv audit` when it is stable |

- One `pyproject.toml` (PEP 621) holds all tool configuration; the `src/`
  layout keeps tests from importing uninstalled code.
- Ruff: keep Ruff's default rules and add to them with `extend-select`
  (`select` replaces the defaults). Add at least `D` with
  `pydocstyle.convention = "google"` plus `D401` (imperative summary, which
  the convention turns off), `S` (security), `DTZ` (naive datetimes), `BLE`
  (blind `except`), `T20` (`print`), `ERA` (commented-out code), `TD`/`FIX`
  (TODO markers) and `PT` (pytest style). In `tests/**`, ignore `D101`–`D107`
  so test functions need no docstring. Upgrade Ruff deliberately: a new
  version can enable new rules.
- One local command (for example `make check`) runs exactly what CI runs.
- Re-evaluate `ty` as the type checker when it is stable. The current status
  of `ty` and `uv audit` is tracked in
  [research/01](../research/01-external-code-and-sources.md).

## 3. Types and data models

- Every function signature is fully typed. `Any`, `cast` and
  `# pyright: ignore[ruleName]` need a comment explaining why no real fix
  exists.
- Use modern syntax: `X | None`, built-in generics (`list[int]`), PEP 695 type
  parameters, `typing.Self`, `@override`.
- Every value that crosses a boundary (API, provider, model, database, event)
  is a typed model, never a raw `dict`.
- Pydantic v2 models use `ConfigDict(frozen=True, extra="forbid")`; internal
  models also use `strict=True`. Parse lenient external payloads in a
  dedicated adapter model, then convert to the strict domain model.
- Plain domain values are `@dataclass(frozen=True, slots=True, kw_only=True)`.
- Closed sets are `enum.StrEnum`; exhaustiveness is checked with `match` and
  `typing.assert_never`.
- Parse, don't validate: convert input into a precise type once, at the edge,
  and let the type carry the guarantee inward.
- Each validation rule lives in one place; domain invariants are pure,
  unit-tested functions.

## 4. Errors

- Each module defines a small exception hierarchy rooted in one base class;
  ports raise the typed errors in
  [contracts/03](../contracts/03-provider-interfaces.md).
- Chain causes with `raise DomainError(...) from err`.
- Never use bare `except:` or `except Exception:` to continue silently. On the
  decision, risk and execution path, an unexpected error stops the flow and
  fails closed (`AGENTS.md` section 3, rule 7).
- Handle `ExceptionGroup` from task groups with `except*`.
- Error messages state what failed and the identifier involved, never secret
  values.

## 5. Money

- `Decimal` for every price, quantity, cash amount and fee, including JSON
  (serialize as strings) and database columns (`numeric(p, s)`).
- Build `Decimal` from strings or integers, never from `float`.
- At process start, trap `decimal.FloatOperation` in both
  `decimal.DefaultContext` (copied by every new thread) and the current
  `decimal.getcontext()` (inherited by asyncio tasks), so constructing a
  `Decimal` from a `float`, or ordering a `Decimal` against a `float`, raises
  instead of passing silently. Equality comparisons with a
  `float` stay silent, so reviews still look for them.
- Round only with `quantize()` and an explicit rounding mode, chosen per use
  and documented next to the call: quantities round **down** to the lot size;
  fees and slippage round **against** the portfolio.
- Money always travels with its currency; arithmetic across currencies goes
  through a timestamped FX rate.

## 6. Time

- Only timezone-aware datetimes in UTC: `datetime.now(UTC)` through the
  injected clock, never `datetime.now()` or `utcnow()`.
- Pydantic fields use `AwareDatetime`; naive datetimes are rejected at the
  boundary.
- Exchange-local times (sessions, holidays) use `zoneinfo` and are converted
  to UTC at the edge.
- Inject the clock and random seeds; nothing reads the wall clock or global
  randomness directly.

## 7. Concurrency

- Use `asyncio.TaskGroup` for concurrent work and `asyncio.timeout()` for
  every network or model call; no orphan fire-and-forget tasks.
- Never block the event loop: run blocking libraries through
  `asyncio.to_thread()`.
- Bound concurrency with a semaphore per provider, matching its rate limit.
- Cancellation is cooperative: clean up, then re-raise `CancelledError`;
  never swallow it.

## 8. Module boundaries

Modules and their ownership are defined in
[`architecture/01-system.md`](../architecture/01-system.md).

- Dependencies point inward: domain code imports no adapter; application code
  depends on ports; concrete adapters are injected at the edge.
- A new external integration is a new adapter behind a port.
- import-linter contracts in `pyproject.toml` enforce the rules in CI. For
  example, `strategies` must not import `execution`, `risk` must not import
  any model adapter, and only `execution` may import the ledger writer.

## 9. Persistence and API

- PostgreSQL: money in `numeric(p, s)`, times in `timestamptz`; never `float`
  columns for money, the `money` type, or `timestamp` without time zone.
- Idempotency is a database guarantee: unique constraints on provider event
  IDs and `client_order_id`, not only checks in code.
- SQLAlchemy 2.0 typed models (`Mapped[...]`); Alembic migrations are
  reviewed by hand, never applied unread from autogenerate.
- FastAPI: typed request and response models, dependency injection for
  services and auth, a `lifespan` handler for startup and shutdown, and
  configuration through `pydantic-settings`.

## 10. Testing

- pytest configuration: `--strict-markers`, `--strict-config`,
  `xfail_strict = true` and `filterwarnings = ["error"]`.
- Unit and property tests (Hypothesis) run on every change with no network
  and no wall clock. Required property tests are listed in
  [`delivery/03-test-strategy.md`](../delivery/03-test-strategy.md).
- Measure branch coverage and read the report; do not chase a number. Every
  rule in risk, ledger and execution has a test that fails when the rule is
  removed; mutation testing (for example `mutmut`) can verify this for
  high-risk modules.
- Integration tests use real PostgreSQL in Docker, not mocks of it.

## 11. Logging

- Structured JSON logs through the standard `logging` module, one event per
  record, with correlation IDs (`run_id`, `snapshot_id`, `decision_id`,
  `order_id`, `fill_id`).
- Every flow entry point (HTTP request, scheduled job, decision cycle, order
  lifecycle) logs received, stage durations and outcome.
- Never log secrets, credentials, licensed raw content or full serialized
  portfolios. Log IDs, hashes, counts, durations, reason codes and enum
  values.
- The level comes from `LOG_LEVEL`. Logging never changes behavior, and a
  logging failure never fails the flow.

## 12. Security and dependencies

- Add a dependency only when the standard library and current stack cannot do
  the job; the pull request states its purpose, license and maintenance
  status. Runtime use of external research code needs an approved
  `assess-external-code` verdict.
- Secrets come from the environment through `pydantic-settings` as
  `SecretStr`; never from code or committed files.
- Never `pickle` or `eval` untrusted data; load YAML with `yaml.safe_load`;
  run subprocesses without `shell=True`; use parameterized SQL only.
- CI runs the vulnerability scan on every pull request.

## 13. References

- [PEP 8](https://peps.python.org/pep-0008/),
  [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html),
  [PEP 735 dependency groups](https://peps.python.org/pep-0735/).
- [Python version status](https://devguide.python.org/versions/),
  [`decimal`](https://docs.python.org/3/library/decimal.html),
  [`asyncio` task groups and timeouts](https://docs.python.org/3/library/asyncio-task.html).
- [uv](https://docs.astral.sh/uv/), [Ruff rules](https://docs.astral.sh/ruff/rules/),
  [ty](https://github.com/astral-sh/ty), [Pyright configuration](https://microsoft.github.io/pyright/#/configuration),
  [import-linter](https://import-linter.readthedocs.io/),
  [uv audit announcement](https://astral.sh/blog/uv-audit).
- [Pydantic types and configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/types/),
  [pytest configuration](https://docs.pytest.org/en/stable/reference/customize.html),
  [Hypothesis](https://hypothesis.readthedocs.io/).
- [PostgreSQL wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This),
  [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/).
