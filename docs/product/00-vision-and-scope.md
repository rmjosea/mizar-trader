# Vision and scope

What Mizar Trader is for, what the MVP includes, and what it will never do.

## Goal

Answer one research question with auditable evidence: **does an AI-derived
signal improve risk-adjusted net results versus preregistered quantitative
baselines under equal information, capital and execution assumptions?**

To do that, Mizar Trader continuously ingests genuine market-provider data,
derives contextual signals from timestamped public sources, runs quantitative,
Jev, reasoning-LLM and hybrid strategies in independent virtual portfolios,
and displays reproducible results.

## Operating principle

Real observed market data, virtual cash, virtual fills. No live order
submission ([ADR-0002](../decisions/0002-real-data-virtual-money.md)).

## Initial universe

| Sleeve | Instruments | Timeframes |
|---|---|---|
| US equities and ETFs | AAPL, MSFT, NVDA, SPY, QQQ | 1D |
| Spot crypto | BTC, ETH, SOL (quote currency per venue) | 4h, 1D |

Instruments are configuration with venue, currency, tick, lot and calendar
metadata. The two sleeves are reported separately; 24/7 crypto and
exchange-hours equity returns are never naively compared.

## In scope (MVP)

- At least one equity and one crypto market-data source with provenance.
- Point-in-time snapshots, event-driven backtest and quantitative baselines.
- Deterministic risk gate, virtual execution, double-entry ledger.
- Prospective (forward) virtual trading in both markets with restart recovery.
- External signals (news, macro, filings) with provenance.
- AI strategies behind a provider-neutral, replayable adapter.
- Experiment registry, metrics and a read-only dashboard with a kill switch.

## Non-goals

- Real money, live broker orders, live credentials.
- Margin, leverage, short selling, options, perpetuals or other derivatives.
- High-frequency trading or full tick-history retention.
- Profitability guarantees or performance claims without evidence.
- Autonomous self-modification of strategies or risk policy.
- Training large models locally; JEPA, RL and ML are optional isolated plugins,
  never on the critical path.
- Dependence on paid social-data feeds or scraping against terms of service.

A live adapter would require a new ADR, a separate security review, approval
and staged rollout; it is not planned.

## Success criteria

The MVP is complete when every release gate in
[`delivery/02-release-gates.md`](../delivery/02-release-gates.md) up to Gate 4
passes with linked evidence. Unresolved business choices are tracked in
[`open-decisions.md`](open-decisions.md).
