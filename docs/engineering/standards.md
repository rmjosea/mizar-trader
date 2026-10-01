# Engineering standards

Normative for all code. Tooling commands are set by backlog task F01; until
then these rules guide its design.

## Python

- Python 3.12+ ([OD-07](../product/open-decisions.md)), managed with `uv`;
  dependencies pinned through `uv.lock`.
- `ruff` for lint and format; strict static typing on all modules; `pytest`
  with Hypothesis for property tests.
- Pydantic v2 models at boundaries; immutable value objects for snapshots and
  decisions.
- `Decimal` for money, prices and quantities; never `float` on the accounting
  path, including JSON and database columns.
- Timezone-aware UTC `datetime` only; naive datetimes are rejected at
  boundaries.
- Inject clocks, providers and randomness (seeded); no hidden global state.
- Typed exceptions per port ([contracts/03](../contracts/03-provider-interfaces.md));
  never swallow an error on the decision, risk or execution path.

## Documentation in code

- Public modules, classes and functions have Google-style docstrings with an
  imperative one-line summary; document `Args`, `Returns` and `Raises` when they
  add information.
- Comments explain why (invariants, rationale, constraints), never what the
  code already says. No banners, history notes, issue numbers or agent
  attribution.

## Logging and observability

- Structured JSON logs through the standard `logging` module.
- Every flow entry point (HTTP request, scheduled job, decision cycle, model
  call, order lifecycle) logs received, stage durations and outcome with its
  correlation IDs (`run_id`, `snapshot_id`, `decision_id`, `order_id`,
  `fill_id`).
- Never log secrets, credentials, licensed raw content or full raw model
  responses; log hashes and references instead.
- Logging failures never change behavior.

## Frontend

React with Vite and TypeScript in strict mode. The dashboard is read-only
except audited operator actions; it never holds credentials.

## Dependencies

Each new dependency states its purpose, license and maintenance status in the
PR; runtime dependencies on external research code require an approved
`assess-external-code` verdict.
