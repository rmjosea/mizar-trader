---
name: plan
description: Design how accepted product intent should be implemented in an existing or new codebase, resolving material technical decisions with the user one clear question at a time. Use when the user asks for architecture, technical design, an implementation plan, data model, API contract, migration plan, or test strategy, or when medium/high risk requires a durable plan. Accept a spec, issue, contract, or confirmed request as source intent. Do not decompose the design into executable tasks.
---

# Plan an Implementation

Convert approved product behavior into a technically coherent design.
Do not modify production code.

## Discover

1. Read only the authoritative source intent and relevant repository guidance.
2. Inspect the codebase, tests, dependencies, and established conventions.
3. Identify constraints, reusable components, trust boundaries, and unknowns.
4. Separate repository facts, confirmed constraints, assumptions, and choices.

## Resolve decisions conversationally

For every material uncertainty, apply the human decision protocol in
`AGENTS.md`:

- ask one clear, self-contained question at a time;
- offer distinct alternatives with consequences;
- mark and justify the recommended option;
- update the confirmed design after each answer.

Ask when a choice materially affects architecture, data, APIs, security, cost,
operability, compatibility, reversibility, or task structure. Decide trivial,
reversible, repository-standard details directly and record the rationale.

Do not write the final plan until material decisions are resolved and the user
has confirmed the proposed technical direction.

## Design

Cover only what the change needs:

- components and responsibilities;
- interfaces and integration points;
- data ownership, model, and migration;
- security and privacy boundaries;
- failure handling and recovery;
- compatibility and rollout;
- observability;
- verification strategy;
- how each non-negotiable invariant in `AGENTS.md` that the change touches
  (point-in-time availability, `Decimal` money, idempotency, fail-closed,
  proposal/risk/execution boundary, untrusted text) is preserved and tested.

Classify risk with the table in `AGENTS.md`; the highest-risk area touched
sets the plan risk.

Create a separate technical artifact only when several tasks share it, it needs
independent review, or moving it out materially reduces task context. Possible
artifacts include `architecture.md`, `data-model.md`, `api-contract.md`,
`migration.md`, and `test-strategy.md`.

Use [assets/plan.template.md](assets/plan.template.md) and write temporary
planning artifacts under `.work/<TASK-ID>-<slug>/`. Keep the plan `draft` while a
material decision or user confirmation is pending; set it to `approved` only
after the user confirms the complete technical direction.

## Quality gate

Verify that:

- the plan links to every authoritative source;
- requirements have a coherent implementation path;
- risk is classified as `low`, `medium`, or `high`;
- no unresolved material decision is hidden in the design;
- the plan introduces no unnecessary infrastructure or abstraction.

When an approved plan fully covers a source spec, report that it supports the
spec's `planned` transition and update it only when artifact maintenance is
authorized. Do not create executable tasks. Use `decompose-tasks` only when the
plan contains multiple independently executable tasks, requires cross-session
handoff, or benefits from parallel execution.
