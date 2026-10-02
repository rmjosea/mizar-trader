# Documentation map

Contracts and decision records here are **binding**. Everything else is the
**baseline design**: the agreed starting point for writing specs, not the full
list of what Mizar Trader will build. Approved specs in
[`specs/`](../specs/README.md) define what is built; when a spec extends or
changes the baseline, the affected document is updated in the same change.

Load documents on demand. Start from the backlog task you are working on and
follow its links; do not read the whole tree.

## Authority order

When two sources disagree, the higher one wins. Never resolve a conflict
silently: fix the lower source in the same change, or stop and ask when the
higher source looks wrong.

1. Code, tests and executable checks (observed behavior).
2. [`AGENTS.md`](../AGENTS.md): rules and process.
3. [`decisions/`](decisions/): accepted architecture decisions (ADRs).
4. [`contracts/`](contracts/): canonical schemas, events and interfaces.
5. Approved specs in [`specs/`](../specs/README.md).
6. Baseline design: [`domains/`](domains/), [`architecture/`](architecture/),
   [`product/`](product/), [`delivery/`](delivery/) and
   [`research/`](research/).

A spec that needs to change a contract or an ADR must amend it first, with
explicit human approval.

## Index

| Area | Document | Read when |
|---|---|---|
| Product | [00-vision-and-scope](product/00-vision-and-scope.md) | scoping any feature |
| Product | [open-decisions](product/open-decisions.md) | a choice depends on an unresolved business decision |
| Architecture | [01-system](architecture/01-system.md) | placing code in a module or crossing a boundary |
| Architecture | [02-storage-and-operations](architecture/02-storage-and-operations.md) | persistence, recovery, observability |
| Architecture | [03-local-runtime](architecture/03-local-runtime.md) | Docker, resources, Apple Silicon, cloud runtime |
| Architecture | [04-security-and-live-boundary](architecture/04-security-and-live-boundary.md) | secrets, auth, external input, execution modes |
| Decisions | [0001-modular-monolith](decisions/0001-modular-monolith.md) | adding a module, process or service |
| Decisions | [0002-real-data-virtual-money](decisions/0002-real-data-virtual-money.md) | touching data sources or execution modes |
| Decisions | [0003-ai-cannot-authorize-execution](decisions/0003-ai-cannot-authorize-execution.md) | connecting model output to risk or execution |
| Decisions | [0000-template](decisions/0000-template.md) | writing a new decision record |
| Contracts | [00-domain-model](contracts/00-domain-model.md) | any domain entity or identifier |
| Contracts | [01-events](contracts/01-events.md) | events, timestamps, replay |
| Contracts | [02-strategy-plugin](contracts/02-strategy-plugin.md) | writing or calling a strategy |
| Contracts | [03-provider-interfaces](contracts/03-provider-interfaces.md) | market, news, model, execution or clock adapters |
| Domains | [01-market-data](domains/01-market-data.md) | ingestion, calendars, feed quality |
| Domains | [02-external-intelligence](domains/02-external-intelligence.md) | news, macro, filings, social |
| Domains | [03-features](domains/03-features.md) | features and snapshots |
| Domains | [04-quant-baselines](domains/04-quant-baselines.md) | baseline strategies |
| Domains | [05-ai-models](domains/05-ai-models.md) | LLM, Jev, ML adapters and strategies |
| Domains | [06-portfolio-and-risk](domains/06-portfolio-and-risk.md) | portfolios, risk gate, kill switch |
| Domains | [07-virtual-execution-and-accounting](domains/07-virtual-execution-and-accounting.md) | fills, ledger, reconciliation |
| Domains | [08-backtesting](domains/08-backtesting.md) | historical replay |
| Domains | [09-forward-paper-trading](domains/09-forward-paper-trading.md) | prospective runs and scheduler |
| Domains | [10-evaluation](domains/10-evaluation.md) | metrics and experiment registry |
| Domains | [11-api-and-dashboard](domains/11-api-and-dashboard.md) | API and UI |
| Delivery | [01-backlog](delivery/01-backlog.md) | choosing or scoping a task |
| Delivery | [02-release-gates](delivery/02-release-gates.md) | closing a milestone |
| Delivery | [03-test-strategy](delivery/03-test-strategy.md) | choosing test levels |
| Engineering | [python](engineering/python.md) | writing any Python code |
| Engineering | [ai-model-code](engineering/ai-model-code.md) | writing code that calls a language or ML model |
| Engineering | [code-documentation](engineering/code-documentation.md) | writing docstrings or comments |
| Engineering | [writing-for-agents](engineering/writing-for-agents.md) | writing any Markdown an agent will read |
| Research | [00-research-protocol](research/00-research-protocol.md) | designing or evaluating an experiment |
| Research | [01-external-code-and-sources](research/01-external-code-and-sources.md) | adopting external code, data or models |

## Conventions

- Dates are ISO 8601; times are UTC.
- "Provisional" values are engineering defaults, not investment advice; change
  them only through versioned configuration and evaluation.
- Every document states rules imperatively and links instead of copying.
