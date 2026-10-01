---
name: plan
description: Designs how an approved spec, backlog task or confirmed request will be implemented, resolving technical decisions with the user one question at a time, and writes a plan under .work/. Use for architecture, data models, interfaces, migrations, test strategy, or any medium or high risk change. Does not write production code or split work into tasks.
---

# Plan an implementation

Turn approved intent into a coherent technical design. Do not modify
production code.

## Steps

1. Read the source intent (spec or backlog row), the contracts it touches,
   [`docs/engineering/python-and-ai.md`](../../../docs/engineering/python-and-ai.md)
   and the relevant code and tests.
2. Separate four lists: repository facts, confirmed constraints, assumptions,
   open choices.
3. Resolve each material open choice with one question at a time
   (`AGENTS.md` section 1). Decide trivial, reversible choices yourself and
   record a one-line rationale.
4. Write `.work/<TASK-ID>-<slug>/plan.md` from
   [assets/plan.template.md](assets/plan.template.md). Keep `status: draft`
   until the user confirms the whole direction; then set `approved`.

## What the design covers

Only what the change needs: components and responsibilities, interfaces, data
and migrations, failure handling and recovery, observability, verification
strategy, and how each `AGENTS.md` section 3 rule the change touches is kept
and tested. Choose the simplest design that meets the spec; justify every new
abstraction, dependency or configuration flag against a current requirement.

Set the risk from the `AGENTS.md` risk table: the highest-risk area touched
decides it.

## Consistency check before approval

- Every requirement and acceptance criterion maps to a design response and a
  verification step (fill the coverage table).
- No design choice contradicts a contract, an ADR or an open decision; if one
  must change, stop and ask.
- No material decision is hidden inside the design.

When the plan fully covers a spec, report that the spec may move to `planned`.
Use `decompose-tasks` only when the work needs several sessions, agents or
handoffs.
