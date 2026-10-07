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

Development follows an agentic workflow. Any coding agent (Claude Code, Codex
and others) implements one plan task of a backlog block at a time under the single contract in
[`AGENTS.md`](AGENTS.md), using portable skills in
[`.agents/skills/`](.agents/skills/):

```text
spec -> plan -> implement -> review
```

Critical changes (ledger, risk, execution, point-in-time data, secrets, new
dependencies) require an independent review by an agent that did not write the change, or by
a human. Commits are authored by the human operator only.

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
AGENTS.md            the only always-loaded agent contract
.agents/skills/      portable Agent Skills (source of truth)
.claude/             Claude Code settings, subagents, and links to the skills
docs/                binding contracts and ADRs, plus the baseline design
specs/               approved specifications, one per backlog block
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
