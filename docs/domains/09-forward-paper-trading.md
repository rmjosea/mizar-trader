# Forward (prospective) paper trading

Run all strategies prospectively on real, current market data with virtual
money, producing the untouched test that historical results cannot provide.

## Rules

- Schedule equities at the session-aware daily close and crypto at closed 4h
  and 1D candles.
- For each decision point: freeze one snapshot, run every strategy on the same
  snapshot, risk-check, simulate the fill against a subsequent observed quote or
  event, journal the result and update the dashboard.
- Independent virtual portfolios with identical cost schedules.
- The scheduler is idempotent on `(strategy_id, instrument_id, bar_end,
  strategy_version)`; no retrospective decision insertion.
- Log provider latency and whether a quote is IEX-only, consolidated or
  venue-specific.
- On data gaps or host sleep: log the gap, suspend affected strategies, never
  synthesize missed decisions.
- Restart requires reconnect, idempotent execution and reconciliation.
- An optional broker paper adapter (Gate 5) is a separate, second-stage
  reconciliation; its results are labeled separately from local virtual fills.

## Required tests

Feed outage leads to no trade; delayed signal; duplicate tick; restart
mid-order; market closure; partial fill; stale valuation.

## Acceptance

An unattended prospective run in both markets, with evidence and fills
inspectable by decision ID.

## Backlog

P01, U01 (operations).
