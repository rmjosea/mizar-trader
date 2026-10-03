# Backlog

The ordered list of functional blocks to deliver. Each row is one complete
capability with one spec; the spec's plan breaks it into implementation tasks.
It starts from the baseline design and grows as new capabilities are confirmed.

## How blocks become work

- **Block → spec.** Each block has exactly one spec,
  `specs/<BLOCK-ID>-<slug>/spec.md` (`SPEC-<BLOCK-ID>`).
- **Spec → plan → tasks.** The approved plan is decomposed into tasks
  `<BLOCK-ID>-T01`, `-T02`, … (`decompose-tasks`). Each task is one branch
  and one pull request.
- **Start rule.** A block may start (`shape-idea`) only when all its
  dependencies are `done`.
- **New blocks** get the next free ID in their area letter (for example `D02`),
  are confirmed by the operator, and are added here in the change that needs
  them.
- **Status**: `todo`, `in-progress` (spec work has started), `done` (spec is
  `verified`). Update it in the pull request that changes it.
- **Risk** follows the table in `AGENTS.md`: the highest-risk area in the block
  decides it. A plan may raise the risk of a block or a task, never lower it
  without a recorded reason.
- **Gate**: the release gate the block contributes evidence to
  ([02-release-gates](02-release-gates.md)).

## Blocks

| ID | Outcome | Depends | Gate | Risk | Domain | Acceptance | Status |
|---|---|---|---|---|---|---|---|
| F01 | Platform foundation: uv project, lint/type/test tooling, CI, ARM64 Compose, health endpoint, `make doctor` | — | 0 | medium | [arch/03](../architecture/03-local-runtime.md) | clean local boot on ARM64; CI green without secrets and on the `.python-version` interpreter; no live keys; `AGENTS.md` commands updated | todo |
| F02 | Domain core: canonical schemas with UTC and `Decimal` validation; event journal, migrations, outbox and idempotency | F01 | 0 | high | [contracts/00](../contracts/00-domain-model.md), [contracts/01](../contracts/01-events.md) | schema fixtures and negative tests; missing ≠ zero; restart and replay reach the same state | todo |
| D01 | Point-in-time market data: instrument registry and calendars; historical US equity bars; historical crypto bars and quotes; Parquet archive and snapshot builder | F02 | 1 | medium | [01](../domains/01-market-data.md), [03](../domains/03-features.md) | equity holiday and crypto 24/7 tests; feed, entitlement, adjustment, venue and base/quote currency retained; snapshot at fixed `as_of` is reproducible | todo |
| S01 | Baseline strategies: momentum and volatility features; cash, buy-and-hold, equal weight and momentum baselines; mean-reversion and random controls | D01 | 2 | medium | [03](../domains/03-features.md), [04](../domains/04-quant-baselines.md) | hand-calculated feature fixtures; no future bars; deterministic, seeded decisions on fixtures | todo |
| E01 | Virtual execution and risk: ledger and valuation; fill simulator and cost schedule; deterministic risk gate and persistent kill switch | F02, D01 | 2 | high | [07](../domains/07-virtual-execution-and-accounting.md), [06](../domains/06-portfolio-and-risk.md) | property tests for cash and position invariants; next-event fills and fees tested; stale data, exposure, stop and kill-switch tests | todo |
| B01 | Honest backtest and evaluation: event-driven backtester; vectorbt cross-check; metrics and experiment registry | S01, E01 | 2 | high | [08](../domains/08-backtesting.md), [10](../domains/10-evaluation.md) | deterministic replay; no look-ahead; discrepancy report, not forced equality; vectorbt adoption assessment approved; report reproduces from manifest | todo |
| P01 | Forward virtual trading: live feed adapter and freshness monitor; forward scheduler; independent paper portfolios | B01 | 3 | high | [09](../domains/09-forward-paper-trading.md), [01](../domains/01-market-data.md), [06](../domains/06-portfolio-and-risk.md) | outage raises the stale flag; no retroactive trades; restart idempotent; no shared cash or fills | todo |
| U01 | Operator surface and operations: API and dashboard with audited operator actions; telemetry, alerts, backup and restore drill | P01 | 3 | high | [11](../domains/11-api-and-dashboard.md), [arch/02](../architecture/02-storage-and-operations.md) | decision-to-fill trace; operator can stop execution; gaps, kill switch and restore tested | todo |
| I01 | External intelligence archive: news and event archive with dedup; social adapter behind permissions | D01 | 4 | medium | [02](../domains/02-external-intelligence.md) | `published_at` and `first_seen_at` tracked; social source disabled gracefully without access | todo |
| A01 | AI strategies: model provider abstraction with mock and replay; structured signal extraction; reasoning LLM strategy; Jev capability-gated strategy; hybrid strategy and ablation | I01, S01, B01 | 4 | high | [05](../domains/05-ai-models.md), [02](../domains/02-external-intelligence.md) | timeout, cost cap and invalid-JSON tests; prompt-injection and provenance tests; proposals only, never orders; Jev disabled if unavailable and vendor assessment approved; same snapshots, independent portfolios | todo |
| X01 | Prospective protocol and experiment freeze | U01 | 4 | high | [research/00](../research/00-research-protocol.md) | frozen manifests registered before the run | todo |
| X02 | Isolated JEPA/ML/RL experiment plugin | X01 | — | high | [05](../domains/05-ai-models.md) | no core changes; out-of-sample evidence | todo |

## Sequencing notes

- External intelligence (I01) and AI strategies (A01) may proceed in parallel
  with Gate 2 once their dependencies are done; forward trading (P01) never
  waits for AI blocks.
- Structured signal extraction belongs to A01, not I01, because it needs the
  model provider abstraction; this keeps the block graph free of cycles.
- Every task's definition of done is in `AGENTS.md`; blocks that adopt external
  code or vendors also need an approved `assess-external-code` verdict.
