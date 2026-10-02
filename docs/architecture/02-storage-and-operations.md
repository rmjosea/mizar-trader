# Storage, operations and observability

Where data is persisted, how the system recovers after a restart, and what
it must observe and alert on.

## Persistence

- **PostgreSQL**: instruments, provider cursors, canonical observations,
  source-document metadata, snapshots, experiment configs, decisions,
  portfolios, orders, fills, ledger entries, valuations, risk incidents, job
  runs, outbox.
- **Object store**: raw provider payloads and immutable experiment artifacts.
- **Parquet**: time-series partitions by provider/instrument/date, with
  manifests and checksums.
- Unique keys on `(provider, provider_event_id)` and on the order idempotency
  key. Event and decision logs are append-only and replayable.

## Recovery

- On restart, replay persisted events and reconcile journal, cash and holdings
  before accepting new decisions; never create a duplicate virtual order.
- Daily backups; a restore drill must pass before any long-running forward
  test (Gate 3).

## Observability

Structured JSON logs with correlation IDs; OpenTelemetry is optional. Never log
secrets, credentials or licensed raw content.

| Scope | Signals |
|---|---|
| Feed | last observed/received timestamps, latency, gaps, duplicates, reconnects, quota, entitlement |
| Strategy | model/version, run, portfolio, snapshot hash, tokens, cost, latency, decision, risk verdict |
| Execution | order lifecycle, idempotency hits, cash/position invariant checks, reconciliation result |
| Runtime | CPU, RAM, disk, network, job duration, model spend |

Alert on feed outage, inconsistent balances, unresolved orders and excessive
model spend. Thresholds are configuration.

## Deployment path

Local Docker Compose first ([03-local-runtime](03-local-runtime.md)), then an
always-on cloud runtime with the same images and configuration
([OD-09](../product/open-decisions.md)). Validate architecture-specific images
(ARM64/amd64) before migrating.
