# Strategy plugin contract (v1)

The binding interface every strategy implements, what it may receive, and
what it must never do.

## Interface

```python
from typing import Protocol

class Strategy(Protocol):
    metadata: StrategyMetadata

    async def initialize(self, config: StrategyConfig, tools: StrategyTools) -> None: ...
    async def decide(self, context: DecisionContext) -> list[Decision]: ...
    async def shutdown(self) -> None: ...
```

`Decision` is defined in [00-domain-model](00-domain-model.md). Strategies
emit proposals, never orders.

## Metadata

Every plugin declares: `strategy_id`, `strategy_version`, type (rule-based,
ML, LLM, Jev, JEPA encoder + head, RL, hybrid), compatible markets and
timeframes, required feeds and features, lookback, maximum latency, cost
ceiling, model or weights hash, and deterministic seed where applicable.

## DecisionContext

Immutable, point-in-time: `as_of` (UTC), portfolio snapshot, eligible feature
snapshot, eligible signal snapshot, instrument metadata, inference budget and
strategy configuration. Nothing in it has `available_at > as_of`.

## Tools

`StrategyTools` is the only side channel: an injected inference port (model
calls are recorded for replay) and a logger. There is no other I/O.

## Rules

- No network, broker, database, filesystem or wall-clock access; no reading of
  credentials; no mutation of risk policy; no rewriting of its own code.
- Determinism: the same context, configuration and recorded model response
  yield the same decisions.
- Missing capability, stale or unavailable features, or a schema error yield
  `ABSTAIN` with a reason code and an alert, never a hidden fallback.
- Prices come only from the context; model-proposed prices or symbols outside
  the allowlist are rejected.
- Jev uses bounded classification or score questions; reasoning LLMs return a
  structured, evidence-linked proposal; hybrids combine frozen scores with a
  versioned rule, not open-ended agent debate.
- Run plugins with timeouts and, where feasible, process and resource
  isolation.

## Ablation

Arms under comparison receive the same snapshot, the same cost assumptions, an
independent portfolio and an independent audit log.
