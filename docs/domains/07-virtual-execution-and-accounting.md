# Virtual execution and accounting

Simulate fills conservatively against observed market data and keep an exact,
reconcilable double-entry ledger.

## Fill model

- Virtual fills are modeled, never claims of exchange execution.
- A signal at bar close fills no earlier than the next tradable event; never at
  the same close unless explicitly justified by market order data.
- With quotes: buy at ask, sell at bid, plus configurable adverse slippage and
  fees.
- With OHLCV only: conservative next-bar execution; limit orders only with
  explicit path assumptions; no invented liquidity.
- Support partial fills, rejects, cancellations, minimum notional, precision
  and session or venue rules.

## Ledger invariants

- Cash never goes negative; holdings never go negative.
- Sum of fill quantities equals the position delta.
- Fees are debited exactly once.
- A duplicate `client_order_id` cannot create a duplicate fill.
- Timestamped FX marks; stale FX blocks cross-currency actions.
- After restart, reconcile cash, holdings and orders before new activity.

## Required tests

Property tests for conservation and non-negativity; next-event fill; unfilled
limit; partial fill; fee accounting; duplicate order; restart mid-order; stale
FX.

## Acceptance

A toy ledger reconciles exactly and every fill is traceable to its decision.

## Backlog

E01.
