---
name: write-spec
description: Writes or updates a product specification that defines what a backlog task must do, with observable, testable acceptance criteria, using the baseline docs as input. Use after an understanding is confirmed, or when the user asks to write, split, update or approve a spec. Not for implementation design, which belongs to the plan skill.
---

# Write a specification

A spec is the contract for **what** must be true and why. It contains no
implementation choices unless they are confirmed constraints.

## Preconditions

- An approved shared understanding, or an equally clear request. If a material
  question remains, return to `shape-idea`.
- A backlog task ID. If the work has none, propose a new backlog row (ID,
  outcome, dependencies, gate, risk) and get it confirmed first.

## Steps

1. Read the backlog row, the baseline documents it links to, and the contracts
   it touches. Cite them; do not copy them.
2. List any point where the spec extends or changes the baseline. Each one
   needs confirmation and an update to the affected document in the same
   change.
3. Write `specs/<TASK-ID>-<slug>/spec.md` from
   [assets/spec.template.md](assets/spec.template.md). Delete sections that add
   nothing.
4. Add or update the row in `specs/README.md`
   ([assets/spec-index.template.md](assets/spec-index.template.md)).
5. Run `python3 scripts/check_harness.py` and fix every error.
6. Show the spec to the user, ask for approval, then set `status: approved`.

## Writing rules

- Follow [`docs/engineering/writing-for-agents.md`](../../../docs/engineering/writing-for-agents.md):
  summary first, self-contained sections, link instead of copying.
- Keep a spec to one to three pages. Split it when it holds two independent
  outcomes, never by technical layer.
- Give every requirement a stable ID (`REQ-001`). Never renumber an ID that a
  plan, test or review already uses.
- Write acceptance criteria as observable outcomes, preferably in EARS form:

  ```text
  AC-001: WHEN a daily bar closes and the feed is fresh,
          THE scheduler SHALL create exactly one decision per strategy and instrument.
  AC-002: IF the latest quote is older than the policy limit,
          THEN THE risk gate SHALL reject the intent with reason STALE_QUOTE.
  ```

- Always fill `Out of scope`; it bounds the work.
- Cover failure behavior and edge cases explicitly (outage, stale data,
  duplicates, restart).
- Exclude frameworks, classes, tables and endpoints unless they are imposed
  constraints.

## Lifecycle

`draft -> approved -> [planned] -> implemented -> verified`. This skill owns
`draft -> approved`. When behavior changes later, update the spec first and the
code second.

## Quality gate

- Every requirement supports the outcome, and every criterion can be tested.
- Terms match the glossary in `docs/contracts/00-domain-model.md`.
- No implementation preference is disguised as a requirement.
- Open questions are listed and block planning when material.
- Frontmatter has `id: SPEC-<TASK-ID>`, a valid `status` and `depends_on`.
