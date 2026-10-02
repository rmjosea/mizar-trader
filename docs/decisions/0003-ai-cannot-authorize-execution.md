# ADR-0003: AI cannot authorize execution

Models and strategies only propose; a deterministic risk engine approves
orders and only the execution module changes balances.

- Status: accepted
- Date: 2026-09-25

## Context

Model outputs are non-deterministic, can be manipulated through untrusted
documents (prompt injection) and are not calibrated. They must not control
capital, even virtual capital, without a deterministic check.

## Considered options

- **Deterministic risk gate** (chosen): auditable, testable, model-independent.
- **Model-authorized execution**: simpler pipeline, but non-deterministic,
  manipulable through prompt injection and uncalibrated.

## Decision

- Models and strategies only propose target weights or abstain.
- The deterministic risk engine is the only component that approves an order
  intent; the execution adapter is the only component that changes balances.
- Risk policy is configuration versioned per experiment and immutable to
  models.
- The system fails closed on stale or invalid input and inference errors.
- External documents are untrusted data, never instructions.

## Consequences

- Every decision, risk verdict and model call is audited with provenance.
- Model outages degrade to `ABSTAIN`, not to fallback trading.
- Hybrid strategies combine frozen, versioned scores, not unbounded agent
  debate.
