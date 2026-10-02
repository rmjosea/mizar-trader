# Quantitative baselines

Provide preregistered reference strategies every AI arm must beat net of costs.

## Baselines

| Baseline | Task |
|---|---|
| Cash only | S02 |
| Buy and hold | S02 |
| Equal weight with periodic rebalance | S02 |
| Momentum rule with volatility cap (preregistered parameters) | S02 |
| Mean reversion | S03 |
| Random control | S03 |

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

S02, S03.
