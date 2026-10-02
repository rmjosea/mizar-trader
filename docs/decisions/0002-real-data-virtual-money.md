# ADR-0002: Real data, virtual money

Use real observed market data with virtual cash and modeled fills; never
place real orders.

- Status: accepted
- Date: 2026-09-25

## Context

The lab must produce credible evidence about strategies without risking
capital. Synthetic prices hide real feed problems; real orders create
financial and security risk that the project does not need.

## Considered options

- **Real data, virtual money** (chosen): real feed problems, no capital or
  credential risk.
- **Synthetic data**: easy and reproducible, but hides real feed gaps,
  delays and entitlements.
- **Live trading with small capital**: real fills, but financial and security
  risk the research question does not need.

## Decision

- Market observations originate from actual providers with provenance.
- Execution is virtual: explicit, conservative fill approximations against
  observed data. The only execution modes are `BACKTEST` and `PAPER`.
- No live order code path, live endpoint or live trading credential exists.
- No fabricated prices, fills or future data.
- Prospective records cannot be rewritten by backfills; corrections create new
  versions.

## Consequences

- Results are labeled as virtual fills, never as exchange executions.
- An optional broker paper account (Gate 5) uses separate keys and is
  reconciled separately.
- Any live capability requires a new ADR, security review, explicit approval
  and staged rollout.
