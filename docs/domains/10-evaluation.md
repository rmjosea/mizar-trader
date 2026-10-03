# Evaluation and experiment registry

Measure strategies honestly under the preregistered protocol in
[research/00](../research/00-research-protocol.md).

## Registry

Every experiment stores a frozen manifest: hypotheses, universe, splits, costs,
models, prompts, strategy versions, risk policy version, data snapshot hash,
seed and success criteria. See [`examples/experiment-manifest.yaml`](../../examples/experiment-manifest.yaml).

## Metrics

Net return and CAGR, volatility, max drawdown, Sharpe and Sortino (with
annualization and sample count), turnover, exposure, hit rate, costs, inference
spend, provider latency, data gaps and rejected orders, reported per sleeve.

## Rules

- Confidence intervals by block bootstrap where appropriate; correct for
  multiple comparisons (for example the deflated Sharpe ratio) and report the
  number of configurations tried.
- Calibration is assessed against realized outcomes, never self-reported
  confidence.
- Ablate every source and model.
- No alpha claim from a single favorable run; reports include limitations,
  costs and sample sizes.

## Required tests

Benchmark alignment, zero-trade metrics, FX, missing observations,
reproducible manifest.

## Acceptance

A report generated from a manifest reproduces the same metrics and lists
limitations, costs and sample sizes.

## Backlog

B01 (metrics and experiment registry), X01.
