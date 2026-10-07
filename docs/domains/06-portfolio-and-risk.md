# Portfolio and deterministic risk

Keep independent virtual portfolios and make the only, deterministic decision
on whether an order intent may proceed.

## Portfolios

- One independent virtual account per strategy and sleeve, or an explicitly
  declared combined portfolio; no shared cash or fills.
- Track cash, holdings, realized and unrealized P&L, fees and FX valuation.
- Long-only, no leverage.

## Risk policy

Synchronous, deterministic and independent of any model. Configuration is
versioned per experiment and immutable to models.

Provisional defaults (engineering placeholders, not investment advice):

| Limit | Default |
|---|---|
| Max target weight per instrument | 5% |
| Max gross exposure | 50% |
| Max new order notional | 5% of equity |
| Daily stop | 2% from day-start equity |
| Max drawdown stop | 10% |

Also validate: minimum cash reserve, quote age, feed integrity, order count,
session status, liquidity, spread cap, FX availability, instrument allowlist,
sector and correlation exposure when available, stale positions and model
output schema.

## Rules

- On violation, reject or reduce with a machine-readable reason and the policy
  version.
- Stops halt new exposure; any liquidation behavior must be explicit and
  tested, never assumed.
- The kill switch persists across restarts, blocks new orders and still allows
  reconciliation.

## Required tests

Overspend, negative cash, fractional lot, stale quote, zero liquidity, repeated
intent, daily-loss breach, kill switch during a pending order, flash move, gap,
outage, missing quote, double signal, news prompt injection, restart.

## Acceptance

No accepted intent can violate configured constraints, and the accounting
identity holds.

## Backlog

E01 (risk gate and kill switch), P01 (independent paper portfolios).
