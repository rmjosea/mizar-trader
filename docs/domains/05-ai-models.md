# AI models and strategies

Let reasoning LLMs, Jev and optional ML models propose decisions through a
provider-neutral, replayable, budget-bounded adapter, without ever executing.

## Adapter rules

- Provider-agnostic interface with structured (Pydantic) output and a mock and
  replay adapter.
- Input is a bounded point-in-time snapshot, never unrestricted browsing.
- Retries only on safe, read-only inference; bounded latency, concurrency and
  cost; daily spend cap. Failures yield `ABSTAIN`.
- Record model ID, version and date, provider, prompt template hash, schema
  version, tool versions, temperature, input and output hashes, allowed
  evidence IDs, token usage and cost, latency, raw response reference, refusal
  or error.
- Never interpret model confidence as a calibrated probability without a
  calibration experiment.

## Strategy arms

- **Reasoning LLM**: analysis of structured context and evidence producing a
  structured proposal, never trading commands.
- **Jev** (TypeSafe "System One" model, early access since 2026-09-15): behind a
  capability flag; bounded typed questions over shared state. Vendor claims are
  unverified; confirm API, terms and benchmark-publication rules before
  integration ([OD-08](../product/open-decisions.md)).
- **Hybrid**: combines frozen signal scores with a versioned rule.
- **Optional, isolated**: LightGBM/XGBoost baseline, JEPA encoder plus head,
  RL. Never on the critical path.

## Required tests

Invalid schema, hallucinated symbol, inconsistent target, timeout, provider
outage, rate limit, malformed response, missing provider, prompt injection in
news, repeated replay, model drift.

## Acceptance

The mock adapter and at least one configured live API adapter yield a validated
proposal or a safe abstention, without any order execution.

## Backlog

A01, A02, A03, A04, X02.
