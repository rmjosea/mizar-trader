# Features and snapshots

Produce reproducible, point-in-time feature and signal snapshots that are the
only inputs strategies see.

## Rules

- Features: trailing returns, realized volatility, momentum, moving averages,
  volume anomalies, session-aware liquidity metrics.
- Use only closed, eligible bars. Reject incomplete history; do not leak future
  bars or revised fundamentals.
- Each feature definition declares window, adjustment policy, `min_history`,
  code version and a deterministic hash.
- Signal snapshots include evidence references and expiry.
- A snapshot is immutable and addressed by its hash.

## Required tests

Hand-calculated fixtures, warm-up period, missing bars, split adjustment,
crypto 24/7, time-travel query (snapshot at `as_of` ignores later data).

## Acceptance

Reproducible feature snapshot for equities and crypto at a fixed `as_of`.

## Backlog

D05, S01.
