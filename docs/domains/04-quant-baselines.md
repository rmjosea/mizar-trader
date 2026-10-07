# Quantitative baselines

Provide preregistered reference strategies every AI arm must beat net of costs.

## Baselines

| Baseline | Block |
|---|---|
| Cash only | S01 |
| Buy and hold | S01 |
| Equal weight with periodic rebalance | S01 |
| Momentum rule with volatility cap (preregistered parameters) | S01 |
| Mean reversion | S01 |
| Random control | S01 |

## Rules

- Signals are generated at bar close and are executable no earlier than the
  next eligible quote or bar under the declared fill model.
- Each baseline runs in its own portfolio with its own initial capital.
- No parameter optimization on the test split.

## Required tests

Flat, rising and falling series; fee drag; rebalance; equity market closure;
crypto weekend.

## Acceptance

Independent deterministic run IDs and equity curves that match expected toy
fixtures.

## Backlog

S01.
