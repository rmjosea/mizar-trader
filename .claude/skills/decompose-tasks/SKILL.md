---
name: decompose-tasks
description: Convert an approved technical plan into an atomic, traceable dependency graph of implementation tasks, classifying task purpose, risk, execution order, conflicts, and safe parallelism. Use when a confirmed plan must be broken down, scheduled, prepared for multiple agents, or made ready for incremental implementation. Do not redesign the approved solution or implement code.
---

# Decompose an Approved Plan

Turn a confirmed design into the smallest useful executable task graph. Do not
modify production code or reopen settled technical decisions.

## Preconditions

1. Read `AGENTS.md`, the approved plan, its source intent, and only the
   contracts needed to understand delivery boundaries.
2. Require the plan status to be `approved` with no material open technical
   decision.
3. Return to `plan` if decomposition exposes a missing or contradictory design.
4. Return to the source owner if it exposes a change to accepted behavior; use
   `write-spec` only when a durable product contract is required.

## Build the graph

1. Map each non-trivial source item to one or more observable delivery outcomes.
2. Create vertical tasks that each produce one coherent, verifiable result.
3. Add enabling work only when a delivery task cannot safely absorb it.
4. Identify dependencies from contracts, data flow, migrations, shared state,
   and required validation—not from an assumed coding order.
5. Identify change-surface conflicts before marking tasks parallel.
6. Confirm every source item is covered and every task supports one or an
   explicit plan obligation.

Avoid tasks named only after layers such as "backend", "frontend", or
"database". Split a task when it has multiple outcomes, independent failure
modes, unrelated change surfaces, or cannot fit one focused agent session.
Do not split work that must change atomically to remain correct.

## Classify each task

Choose one primary type:

- `feature`: delivers observable behavior;
- `bugfix`: restores accepted behavior by correcting a defect;
- `enabler`: unlocks later delivery without standalone product behavior;
- `migration`: changes persisted data, contracts, or compatibility state;
- `verification`: provides independent evidence not owned by another task;
- `operations`: changes build, deployment, observability, or runtime controls;
- `maintenance`: improves internals without changing accepted behavior;
- `documentation`: updates durable user or engineering guidance.

Assign risk as `low`, `medium`, or `high` using `AGENTS.md` and record one-line
rationale. Inherit the plan risk unless the task has a clear reason to differ.

Assign execution policy:

- `parallel-safe`: may run with other eligible tasks after every dependency is
  done, provided no active change surface or mutable resource conflicts;
- `exclusive`: must run alone because shared mutation or coordination makes
  concurrency unsafe.

Keep dependency order only in `Depends on`; do not duplicate it in execution
policy. Record task conflicts symmetrically. When uncertain, prefer `exclusive`
and state the reason.

Execution policy describes safe scheduling, not task ownership. Without an
external atomic coordinator, require a human or orchestrator to assign tasks
before parallel agents start.

## Write

Use [assets/tasks.template.md](assets/tasks.template.md) and write
`.work/<TASK-ID>-<slug>/tasks.md`. Each task must include:

- stable ID and outcome;
- plan and source-item links;
- type, risk, and state;
- dependencies, blocker reason, and execution policy;
- expected change surface and conflicts;
- prospective acceptance evidence and validation commands;
- actual result, initially `pending`.

Use only `blocked`, `ready`, `in-progress`, `done`, or `stale` as task states.
Only dependency-free, decision-complete tasks may start as `ready`; dependent
tasks start `blocked` with their dependency IDs as the blocker. A decision,
safety, or external blocker requires an explicit reason and resolution; it is
never cleared merely because dependencies finish.

## Quality gate

Verify:

- all source items and plan obligations are covered;
- the graph is acyclic and has at least one ready task;
- each task is independently understandable and verifiable;
- no task contains a hidden product or architecture decision;
- parallel claims account for dependencies and conflicts;
- the graph contains no speculative infrastructure or process work.
