---
name: implement
description: Implements one bounded change (one task from an approved plan, or one small change the user confirmed) in short edit-and-verify loops, with tests and docstrings, ending with one validated commit and evidence. Use when the user asks to build, code, fix or continue accepted work. Does not expand scope or start a task whose dependencies are not done.
---

# Implement one task

Finish one outcome and leave the repository green and reviewable.

## Steps

1. **Pick one input:** a `todo` task in `.work/<BLOCK-ID>-<slug>/plan.md`
   whose dependencies are `done`, or a small change the user confirmed
   (`AGENTS.md` section 4). Work on the spec's branch (`AGENTS.md`
   section 6) and set the task to `in-progress`.
2. **Read** the affected code and tests. Write the goal as checks. Stop and
   ask on a material ambiguity; never invent a product or architecture
   choice.
3. **Loop:** for rules and bugs, write the failing test first and confirm it
   fails for the expected reason; make the smallest change that passes; run
   the narrowest useful check. Write docstrings as you go
   ([code-documentation](../../../docs/engineering/code-documentation.md)).
4. **Verify:** run `make check`
   and compare the behavior with each acceptance criterion of the task.
5. **Close:** for a `critical` task, get the independent review on the
   task's diff and fix what it requires. Then make one commit for the task
   (subject starts with the task ID), push the branch, set the task to
   `done`, and report commands and results. Open a pull request only when
   the human asks. If you stop early, write
   what is done, what is next and the exact state into the plan's task row.

## Project test rules

- Property tests (Hypothesis) for invariants: cash and position
  conservation, no negative cash or holdings, idempotent replay, exclusion of
  inputs with `available_at` after the decision time.
- Every time rule is tested at the boundary: data available exactly at the
  decision time (allowed) and one tick later (rejected).
- No network or wall clock: inject the clock and providers; adapters are
  tested against recorded fixtures labeled as fixtures.
- Assert exact `Decimal` equality; never approximate.
- Models run through the mock or replay adapter; live calls are opt-in tests.

Never weaken, skip or delete a failing test, fixture or threshold to get a
green result (`AGENTS.md` section 3, rule 9). If a check seems wrong, stop and
report it with evidence.
