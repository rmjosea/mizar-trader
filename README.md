# Mizar Trader

Research-first, dual-market trading laboratory for US equities/ETFs and spot
crypto. **Real observed market data, virtual cash and virtual fills; no live
order submission.**

It answers one question with auditable evidence: does an AI-derived signal
(reasoning LLMs, Jev, hybrids) improve risk-adjusted net results over
preregistered quantitative baselines under identical information, capital and
execution assumptions?

> Status: specification and agentic-delivery harness only; no application code
> yet. The first task is [F01](docs/delivery/01-backlog.md).

## How this repository is built

Development follows an agentic SDLC: AI agents implement one backlog task at a
time under the contract in [`AGENTS.md`](AGENTS.md), using the skills in
[`.claude/skills/`](.claude/skills/):

```text
shape-idea -> write-spec -> plan -> decompose-tasks -> implement -> review
```

High-risk changes (contracts, ledger, risk, execution, scheduling, security)
require an independent review by a fresh agent
([`.claude/agents/independent-reviewer.md`](.claude/agents/independent-reviewer.md))
or a human. Commits are authored by the human operator only.

## Where to start

| You want to | Read |
|---|---|
| Understand the product | [Vision and scope](docs/product/00-vision-and-scope.md) |
| Navigate all documentation | [Documentation map](docs/README.md) |
| Pick the next piece of work | [Backlog](docs/delivery/01-backlog.md) |
| See unresolved choices | [Open decisions](docs/product/open-decisions.md) |
| Work as an agent | [AGENTS.md](AGENTS.md) |

## Repository layout

```text
AGENTS.md            agent contract (CLAUDE.md imports it)
.claude/             skills, subagents and settings for Claude Code
docs/                product, architecture, contracts, domains, delivery, research
specs/               approved product specifications per backlog task
examples/            reference contracts (fixtures, not results)
scripts/             repository checks
tests/harness/       tests for the repository checks
```

## Checks

```sh
python3 scripts/check_harness.py
python3 -m unittest discover -s tests/harness
```

## Disclaimer

Nothing here is investment advice. Risk limits are provisional engineering
defaults. No result in this repository is a claim of real-money performance.
