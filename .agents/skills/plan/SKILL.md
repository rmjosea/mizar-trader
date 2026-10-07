---
name: plan
description: Designs how an approved spec or confirmed request will be built and splits it into small tasks, resolving technical decisions with the user one selectable question at a time, and writes .work/<BLOCK-ID>-<slug>/plan.md. Use for architecture, interfaces, data, test strategy or any change that is not small. Does not write production code.
---

# Plan an implementation

Choose the simplest design that meets the spec and cut it into tasks that
each end in one validated, revertible commit. Do not modify production code.

## Steps

1. Read the spec, the contracts it touches,
   [`docs/engineering/python.md`](../../../docs/engineering/python.md) (plus
   [`ai-model-code.md`](../../../docs/engineering/ai-model-code.md) when models
   are involved) and the relevant code.
2. List the open technical choices. Ask each one that matters as a
   selectable list (`AGENTS.md` section 1); decide reversible details
   yourself and record a one-line reason.
3. Write `.work/<BLOCK-ID>-<slug>/plan.md` from
   [assets/plan.template.md](assets/plan.template.md). Justify every new
   dependency, abstraction or configuration flag against a current
   acceptance criterion.
4. Show the plan and ask for approval. Only an explicit "yes" sets
   `status: approved`.

## Tasks

- IDs are `<BLOCK-ID>-T01`, `-T02`, …; each is one commit with one
  verifiable result. Slice by outcome, never by layer.
- Each task names its acceptance criteria, its checks, the tasks it depends
  on, and its risk (`critical` or `normal`, `AGENTS.md` section 4).
- Every acceptance criterion maps to at least one task.

If implementation shows the **how** must change, update the plan. If the
**what** must change, stop and return to the spec.
