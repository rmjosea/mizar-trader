# Testing strategy

Choose tests by risk and observable behavior.

## Rules

- Test through stable public seams, not private details.
- One meaningful behavior per test, with a failure message that explains it.
- Integration tests only at boundaries unit tests cannot represent; end-to-end
  tests only for critical cross-module journeys.
- Do not write tests that only repeat type checks, framework behavior or
  mocks.

## Project-specific rules

- **Property tests (Hypothesis)** for invariants: cash and position
  conservation, no negative cash or holdings, idempotent replay, exclusion of
  inputs with `available_at` after the decision time.
- **Time boundaries**: for every time rule, test data available exactly at the
  decision time (allowed) and one tick later (rejected).
- **No network or wall clock**: inject the clock and providers; adapters are
  tested against recorded fixtures labeled as fixtures.
- **Exact money**: assert `Decimal` equality; never approximate floats.
- **Models**: use the fake or replay adapter; live calls are opt-in tests.

## Red, green, refactor

1. Write a focused failing test.
2. Run it; confirm it fails for the expected reason.
3. Make the smallest change that passes.
4. Run the neighboring tests.
5. Refactor only while everything stays green.
