# Research protocol (v1)

## Question

Does an AI-derived signal improve risk-adjusted **net** results versus
preregistered quantitative baselines under equal information, capital and
execution assumptions?

## Arms

| Group | Arms |
|---|---|
| Baselines | cash, buy-and-hold, equal weight, momentum, mean reversion, random control |
| AI | Jev, reasoning LLM, quant+Jev, quant+LLM, hybrid |
| Later, isolated | JEPA, ML, RL |

All arms share decision timestamps, point-in-time data, initial virtual cash,
fill model, fees, risk policy and snapshot IDs. Equity and crypto sleeves are
reported separately.

## Splits

- Train 2021–2023, validate 2024, historical holdout 2025–2026, only where
  licensed point-in-time inputs exist.
- Rolling walk-forward with purging and embargo for overlapping labels.
- Historical tests of current LLMs are exploratory because of pretraining
  contamination.
- The prospective forward run is the untouched test: prompts and model
  configurations are frozen before it starts and evaluated only on unseen
  future observations.

## Preregistration and integrity

- Register hypotheses, metrics and success criteria in the experiment
  manifest before viewing holdout or prospective results.
- Pin seeds and prompts; persist every non-deterministic output.
- Record all trials, including failures and negative results, and report how
  many configurations were tried.
- Never tune repeatedly on the test split; a change after seeing results is a
  new registered version.
- Ablate news, social and macro sources separately.

## Reporting

Net CAGR and return, volatility, Sharpe, Sortino, drawdown, turnover, hit rate,
exposure, calibration, inference cost, provider latency and rejected orders,
with confidence intervals and per-sleeve breakdown. Account for multiple
testing (for example the deflated Sharpe ratio or the probability of backtest
overfitting).

## Promotion

A strategy is promoted only with prespecified minimum observations and regimes,
results that survive plausible fees, delayed signals and alternate windows, and
operational safety. There is no fixed duration ("30 days") that implies
profitability, and no promotion to real capital within this project.
