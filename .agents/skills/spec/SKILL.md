---
name: spec
description: Turns an idea or backlog block into an approved specification of what must be true, by interviewing the user one selectable question at a time and then writing specs/<BLOCK-ID>-<slug>/spec.md with testable acceptance criteria. Use when the what is new, vague or unclear, or the user asks to shape, write, update or approve a spec. Not for implementation design, which belongs to the plan skill.
---

# Write a specification

Agree with the user on **what** to build and **why**, then record it as a
short, testable spec. No implementation choices unless they are confirmed
constraints.

## Steps

1. Restate the idea in two or three sentences in the user's language.
2. Read the backlog row and only the baseline docs and contracts it links to.
   Note where the idea extends or changes them.
3. Ask the single most important open question as a selectable list
   (`AGENTS.md` section 1). Offer the simpler alternative when one exists.
   Repeat until the remaining uncertainty would not change scope, behavior,
   risk or research validity; record the rest as assumptions.
4. Check the result against two or three concrete scenarios, one of them a
   failure (for example: "the data feed is down at the daily close").
5. Write `specs/<BLOCK-ID>-<slug>/spec.md` from
   [assets/spec.template.md](assets/spec.template.md) and add its row to
   `specs/README.md`. If the work has no backlog block, propose the row and
   get it confirmed first.
6. Update every baseline doc the spec changes, in the same change.
7. Run `python3 scripts/check_harness.py`, show the spec, and ask for
   approval. Only an explicit "yes" sets `status: approved`.

## Writing rules

- One to two pages. Split a spec that holds two independent outcomes, never by
  technical layer.
- Acceptance criteria are observable and numbered (`AC-001`); never renumber
  one that a plan or test already uses. Prefer this form:

  ```text
  AC-001: IF the latest quote is older than the policy limit,
          THEN the risk gate SHALL reject the intent with reason STALE_QUOTE.
  ```

- Always fill `Out of scope` and the failure cases (outage, stale data,
  duplicates, restart).
- Use the terms of `docs/contracts/00-domain-model.md`.
- Spec states: `draft` -> `approved` -> `done` (all acceptance criteria have
  merged evidence). If behavior changes later, update the spec first.
