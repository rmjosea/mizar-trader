---
name: decompose-tasks
description: Splits an approved plan into an ordered, traceable graph of small implementation steps with dependencies, risk, conflicts and safe parallelism, written to .work/. Use after every approved plan, or when the user asks to break work down or schedule it. Does not redesign the solution or write code.
---

# Decompose an approved plan

Produce the smallest useful graph of executable steps. Do not reopen settled
decisions or change production code.

## Preconditions

- The plan has `status: approved` and no material open question.
- If decomposition reveals a missing design, return to `plan`. If it reveals a
  change to **what**, return to the user and the spec.

## Build the graph

1. Map each requirement and plan obligation to one or more observable steps.
2. Make each step a vertical slice with one verifiable result. Never split by
   layer ("backend", "database").
3. Derive dependencies from contracts, data flow, migrations and validation
   order, not from habit.
4. Mark conflicts where two steps change the same files or state.
5. Split a step that has several outcomes or does not fit one focused session;
   keep together changes that must land atomically.

## Write

Use [assets/tasks.template.md](assets/tasks.template.md) and write
`.work/<BLOCK-ID>-<slug>/tasks.md`. Step IDs are `<BLOCK-ID>-T01`, `-T02`, and so
on. Each step is one task: one branch and one pull request (`AGENTS.md`
section 9).

- States: `blocked`, `ready`, `in-progress`, `done`, `stale`.
- Only dependency-free, decision-complete steps start as `ready`.
- Execution: `parallel-safe` (may run alongside others once dependencies are
  done and no conflict is active) or `exclusive`. When unsure, choose
  `exclusive` and say why.
- A human or orchestrator assigns steps before agents run in parallel; agents
  never self-claim `ready` steps concurrently.

## Quality gate

- Every requirement is covered; the coverage table is complete.
- The graph has no cycles and at least one `ready` step.
- Each step can be understood and verified on its own.
- No step hides a product or architecture decision.
