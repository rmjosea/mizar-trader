# Market data and feed quality

Ingest real US equity and spot crypto observations with full provenance and
quality flags, historically and prospectively.

## Rules

- Deliver at least one US equity and one crypto spot adapter with historical
  fetch and streaming or polling.
- Each feed declares real-time vs delayed, venue coverage, subscription tier,
  timezone, latency and entitlement. IEX-only and consolidated equity data are
  never merged or treated as equivalent.
- Calendars: US equity regular sessions and holidays; crypto 24/7.
- Use closed bars only. Daily equity bars become available after the close plus
  the provider's publication lag; crypto 4h bars after the interval closes.
- Never fill missing candles with invented tradable prices; never forward-fill
  prices across closed sessions for execution. Backfills carry explicit
  provenance.
- Detect duplicates, out-of-order events, negative volume, crossed quotes,
  impossible jumps, stale quotes, splits, dividends and symbol changes.
- Corporate actions: keep explicit adjusted and unadjusted series; execution
  uses raw tradable prices; research features use adjusted history
  consistently.
- Crypto observations keep base and quote currency; FX conversion uses
  timestamped marks.
- Align multi-source data on `available_at <= decision_at`; quarantine late
  revisions.

## Required tests

Duplicate and out-of-order events, reconnect and backfill, timezone and DST,
market holiday, stock split, missing quote, stale stream, crossed bid/ask,
currency conversion, exchange outage.

## Acceptance

Persisted historical and new real observations for at least one symbol in each
market, with a gap and latency report.

## Backlog

D01, D02, D03, D04, D05. Contracts: [domain model](../contracts/00-domain-model.md),
[providers](../contracts/03-provider-interfaces.md).
