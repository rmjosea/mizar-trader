# Testing strategy

Select tests by risk and observable behavior.

- Use test-first development for reproduced bugs, business rules, contracts,
  transformations, and other deterministic behavior.
- Add regression evidence before fixing a bug when practical.
- Prefer tests through stable public seams over private implementation details.
- Use integration tests at boundaries that unit tests cannot represent.
- Use end-to-end tests only for critical cross-component journeys.
- For visual work, verify rendered behavior with the available browser or
  screenshot tooling instead of relying only on source inspection.
- Use property-based tests (Hypothesis) for invariants: cash and position
  conservation, no negative cash or holdings, idempotent replay, and exclusion
  of data whose `available_at` is after the decision time.
- Inject the clock and providers; tests never touch the network, wall clock,
  or paid APIs. Adapters are tested against recorded, labeled fixtures.
- Assert money with exact `Decimal` equality, never approximate floats.
- For every time-dependent rule, include a boundary case where data becomes
  available exactly at, and one tick after, the decision time.
- Avoid tests that merely repeat type checks, framework behavior, or mocks.
- Keep each test focused on one meaningful behavior and failure message.

Use red-green-refactor when it improves feedback:

1. Create a focused failing test.
2. Run it and confirm it fails for the expected reason.
3. Implement the smallest passing change.
4. Run relevant neighboring tests.
5. Refactor only while all tests stay green.

