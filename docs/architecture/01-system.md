# System architecture

How Mizar Trader is split into processes and modules, which module owns what,
and the rules that cross every module.

## Shape

Modular monolith ([ADR-0001](../decisions/0001-modular-monolith.md)):

- **api** process: FastAPI, read-only by default, authenticated operator
  actions.
- **worker** process: scheduler, ingestion, decisions, virtual execution.
- **PostgreSQL**: transactional state, event journal, ledger.
- **Object store**: immutable raw payloads and experiment artifacts
  (implementation pending [OD-06](../product/open-decisions.md)).
- **Parquet/DuckDB**: partitioned time series and analytical reads.
- **web**: React/Vite dashboard.

Stack: Python 3.12+, uv, FastAPI, Pydantic v2, PostgreSQL, Parquet/DuckDB,
React/Vite, Docker Compose (ARM64). PydanticAI is optional inside the AI
adapter only. No message broker or microservices until a measured need exists.

## Pipeline

```text
provider adapters -> immutable raw records -> canonical observations and documents
  -> point-in-time feature and signal snapshots -> strategy proposals
  -> portfolio target calculation -> deterministic risk validation
  -> virtual execution -> ledger and valuation -> evaluation and dashboard
```

## Modules and ownership

| Module | Owns | Must not |
|---|---|---|
| `market_data` | instruments, calendars, provider adapters, canonical bars/quotes, feed health | compute features or decide |
| `intelligence` | source documents, dedup, entity linking, signal extraction | trade on raw text |
| `features` | feature definitions and point-in-time snapshots | read data after `as_of` |
| `strategies` | strategy plugins producing `Decision` proposals | call brokers, databases, network or wall clock |
| `portfolio` | target-to-intent calculation, holdings view | approve intents or change balances |
| `risk` | policy evaluation, approvals and rejections, kill switch | depend on any model |
| `execution` | virtual orders, fills, ledger, reconciliation | accept intents not approved by `risk` |
| `evaluation` | metrics, experiment registry, reports | modify experiment criteria after results |
| `api` | HTTP surface and auth | contain domain logic |

Only `execution` changes balances; only `risk` approves an order intent. All
provider integrations are ports with adapters
([contracts/03](../contracts/03-provider-interfaces.md)). External text is
untrusted data.

## Cross-cutting rules

- All times are timezone-aware UTC; exchange timezones are preserved as
  metadata.
- Money, prices and quantities use `Decimal` with instrument-specific rounding.
- Schema changes go through database migrations.
- Correlation IDs: `run_id`, `snapshot_id`, `decision_id`, `order_id`,
  `fill_id`, carried on every log record and event of a flow.
- Restart safety through transactional outbox/inbox and idempotency keys.
