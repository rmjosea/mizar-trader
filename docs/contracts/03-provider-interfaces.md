# Provider interfaces (v1)

All external integrations are ports with replaceable adapters. Every adapter
has an offline mode and contract tests against recorded, labeled fixtures.

| Port | Operations | Must preserve or return |
|---|---|---|
| `MarketDataProvider` | `fetch_bars(instrument, start, end, timeframe)`, `stream_quotes(instrument)`, `health()`, `capabilities()` | exchange timezone plus UTC, feed type (SIP/IEX/venue), delay and entitlement, corporate-action policy |
| `NewsProvider` | `fetch_events(since)` | source URL/ID, `published_at`, `first_seen_at`, `received_at`, instruments, license, dedup hash |
| `ModelProvider` | `infer(snapshot, schema, timeout, budget)` | validated output, provider, model and version, cost, latency, raw response reference |
| `ExecutionAdapter` | `submit_virtual_order`, `cancel_virtual_order`, `get_virtual_fills`, `reconcile` | the paper adapter never forwards real orders |
| `Clock` | `now()` | historical event clock in backtests, UTC wall clock in forward runs; always injected |
| `ObjectStore` | `put`, `get`, `exists` by content hash | immutability; implementation per [OD-06](../product/open-decisions.md) |

## Errors

Adapters raise typed errors: `RateLimited`, `Stale`, `Unavailable`,
`Malformed`, `EntitlementMissing`, `BudgetExceeded`, `Timeout`. Callers map
them to fail-closed behavior; no adapter retries non-idempotent operations.
