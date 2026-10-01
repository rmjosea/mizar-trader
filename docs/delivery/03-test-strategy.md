# Test strategy

| Level | Covers | Notes |
|---|---|---|
| Unit | schemas, indicators, risk rules, `Decimal` ledger, event ordering | fast, no I/O |
| Property | cash and asset conservation, no negative cash or holdings, idempotent replay, future-data exclusion | Hypothesis |
| Contract | provider adapters against recorded fixtures, inference schemas, API auth | offline by default |
| Integration | PostgreSQL and object store, equity and crypto ingestion, virtual fill and valuation, worker restart | Docker Compose |
| End-to-end | one forward day with no fabricated events; simulated outages | |
| Research | leakage audit, split integrity, fee sensitivity, ablations, repeated runs | per experiment |

## Rules

- CI never requires paid API keys or network access; live-provider tests are
  opt-in, marked, and use isolated secrets.
- Fixtures are recorded from real providers when licensing allows, labeled as
  fixtures, and never presented as results.
- Time is injected; tests never depend on the wall clock.
- Each domain document lists its required test cases; a task is not done until
  the ones it touches exist and pass.
