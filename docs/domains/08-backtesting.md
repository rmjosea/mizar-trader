# Historical backtesting

Replay real historical observations event by event with point-in-time
availability, producing reproducible runs.

## Rules

- Event-driven replay over an immutable, versioned dataset; real historical
  observations, never generated prices.
- Fees, spread, slippage and conservative fills from the shared fill model
  ([07](07-virtual-execution-and-accounting.md)); equity sessions, corporate
  actions and continuous crypto sessions.
- No same-close fill when the signal uses the close.
- Benchmark against the same universe, calendar and capital, plus passive and
  cash baselines.
- Store a run manifest and decision traces.
- Historical LLM evaluations may be contaminated by training exposure; label
  them separately from prospective evidence.
- A vectorized engine (vectorbt) may cross-check results; discrepancies are
  reported and explained, never forced to equality.

## Required tests

Future news blocked, next-bar fill, unfilled limit, missing quote, fee
accounting, delisting and corporate actions, deterministic replay.

## Acceptance

The toy ledger reconciles and the run is reproducible from pinned artifacts.

## Backlog

B01.
