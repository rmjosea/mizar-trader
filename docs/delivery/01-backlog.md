# Backlog

The ordered list of delivery work. It starts from the baseline design and grows
as specs add or split tasks. One task ID per branch and pull request
(`AGENTS.md`). A task may start only when all its dependencies are `done`.

- **New tasks** get the next free ID in their area letter (for example `D06`),
  are confirmed by the operator, and are added here in the change that needs
  them.

- **Status**: `todo`, `in-progress`, `done`. Update it in the PR that changes
  it.
- **Risk** follows the table in `AGENTS.md`; a plan may raise it, never lower it
  without a recorded reason.
- **Gate**: the release gate the task contributes evidence to
  ([02-release-gates](02-release-gates.md)).

## Tasks

| ID | Outcome | Depends | Gate | Risk | Domain | Acceptance | Status |
|---|---|---|---|---|---|---|---|
| F01 | uv project, lint/type/test tooling, CI, ARM64 Compose, health endpoint, `make doctor` | — | 0 | medium | [arch/03](../architecture/03-local-runtime.md) | clean local boot on ARM64; CI green without secrets; no live keys; `AGENTS.md` commands updated | todo |
| F02 | Canonical schemas with UTC and `Decimal` validation | F01 | 0 | high | [contracts/00](../contracts/00-domain-model.md) | schema fixtures and negative tests; missing ≠ zero | todo |
| F03 | Event journal, migrations, outbox and idempotency | F02 | 0 | high | [contracts/01](../contracts/01-events.md) | restart and replay reach the same state | todo |
| D01 | Instrument registry and trading calendars | F02 | 1 | medium | [01](../domains/01-market-data.md) | equity holiday and crypto 24/7 tests | todo |
| D02 | Historical US equity bars adapter | D01 | 1 | medium | [01](../domains/01-market-data.md) | feed, entitlement and adjustment metadata retained | todo |
| D03 | Historical crypto bars and quotes adapter | D01 | 1 | medium | [01](../domains/01-market-data.md) | venue and base/quote currency preserved | todo |
| D04 | Live feed adapter and freshness monitor | D02, D03 | 3 | medium | [01](../domains/01-market-data.md) | outage raises the stale flag | todo |
| D05 | Parquet archive and point-in-time snapshot builder | D02, D03, F03 | 1 | medium | [03](../domains/03-features.md) | snapshot at fixed `as_of` is reproducible | todo |
| S01 | Momentum and volatility features | D05 | 2 | medium | [03](../domains/03-features.md) | hand-calculated fixtures; no future bars | todo |
| S02 | Baselines: cash, buy-and-hold, equal weight, momentum | S01 | 2 | medium | [04](../domains/04-quant-baselines.md) | deterministic decisions on fixtures | todo |
| S03 | Control baselines: mean reversion, random | S02 | 2 | medium | [04](../domains/04-quant-baselines.md) | seeded, deterministic runs | todo |
| E01 | Virtual ledger and valuation | F03, D01 | 2 | high | [07](../domains/07-virtual-execution-and-accounting.md) | property tests for cash and position invariants | todo |
| E02 | Fill simulator and cost schedule | E01, D05 | 2 | high | [07](../domains/07-virtual-execution-and-accounting.md) | next-event fills and fees tested | todo |
| R01 | Deterministic risk gate and persistent kill switch | E01, F02 | 2 | high | [06](../domains/06-portfolio-and-risk.md) | stale data, exposure, stop and kill-switch tests | todo |
| B01 | Event-driven backtester | S02, E02, R01 | 2 | medium | [08](../domains/08-backtesting.md) | deterministic replay; no look-ahead | todo |
| B02 | vectorbt cross-check | B01 | 2 | high | [08](../domains/08-backtesting.md) | discrepancy report, not forced equality; adoption assessment approved | todo |
| V01 | Metrics and experiment registry | B01 | 2 | medium | [10](../domains/10-evaluation.md) | report reproduces from manifest | todo |
| P01 | Forward virtual scheduler | D04, B01 | 3 | high | [09](../domains/09-forward-paper-trading.md) | no retroactive trades; restart idempotent | todo |
| P02 | Independent paper portfolios | P01 | 3 | high | [06](../domains/06-portfolio-and-risk.md) | no shared cash or fills | todo |
| U01 | API and dashboard with audited operator actions | P02, V01 | 3 | high | [11](../domains/11-api-and-dashboard.md) | decision-to-fill trace; operator can stop execution | todo |
| O01 | Telemetry, alerts, backup and restore drill | P02 | 3 | medium | [arch/02](../architecture/02-storage-and-operations.md) | gaps, kill switch and restore tested | todo |
| I01 | News and event archive with dedup | D05 | 4 | medium | [02](../domains/02-external-intelligence.md) | `published_at` and `first_seen_at` tracked | todo |
| I02 | Social adapter behind permissions | I01 | 4 | medium | [02](../domains/02-external-intelligence.md) | disabled gracefully without access | todo |
| I03 | Structured signal extraction | I01, A01 | 4 | high | [02](../domains/02-external-intelligence.md) | prompt-injection and provenance tests | todo |
| A01 | Model provider abstraction with mock and replay | F02, D05 | 4 | medium | [05](../domains/05-ai-models.md) | timeout, cost cap and invalid-JSON tests | todo |
| A02 | Reasoning LLM strategy | A01, I03, S02, B01 | 4 | medium | [05](../domains/05-ai-models.md) | proposals only, never orders | todo |
| A03 | Jev capability-gated strategy | A01, S02, B01 | 4 | high | [05](../domains/05-ai-models.md) | disabled if unavailable; schema tests; vendor assessment approved | todo |
| A04 | Hybrid strategy and ablation | A02, A03 | 4 | medium | [05](../domains/05-ai-models.md) | same snapshots, independent portfolios | todo |
| X01 | Prospective protocol and experiment freeze | U01, O01, V01 | 4 | high | [research/00](../research/00-research-protocol.md) | frozen manifests registered before the run | todo |
| X02 | Isolated JEPA/ML/RL experiment plugin | X01 | — | high | [05](../domains/05-ai-models.md) | no core changes; out-of-sample evidence | todo |

## Sequencing notes

- External intelligence (I01) and model work (A01) may proceed in parallel with
  Gate 2 once their dependencies are done; forward trading (P01) never waits
  for AI tasks.
- Every task's definition of done is in `AGENTS.md`; tasks that adopt external
  code or vendors also need an approved `assess-external-code` verdict.
