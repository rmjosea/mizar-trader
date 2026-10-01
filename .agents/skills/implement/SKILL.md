---
name: implement
description: Implements one bounded change (one ready step from a task graph, one outcome from an approved spec or plan, or one confirmed direct-path request) in short verify loops, with tests, docstrings and recoverable state. Use when the user asks to build, code, fix or continue accepted work. Does not expand scope or start blocked work.
---

# Implement one bounded change

Finish one outcome and leave the repository in a verifiable state.

## 1. Select and bound

Pick exactly one input:

- a `ready` step from `.work/<TASK-ID>-<slug>/tasks.md`: confirm every
  dependency is `done`, then set it to `in-progress`;
- one decision-complete outcome from an approved spec or plan;
- a direct-path request: confirm it meets the direct-path row in `AGENTS.md`
  section 4 and state `Intent`, `Change` and `Verification` before editing.

Read the affected code and tests first. Write the goal as steps with checks
(`AGENTS.md` section 2, rule 4). Stop on a material ambiguity; never invent a
product or architecture choice.

## 2. Execute

- Make the smallest coherent change; follow existing patterns; leave unrelated
  code untouched.
- Work in short loops: edit, run the narrowest useful check, read the result.
- For reproducible bugs, business rules and contracts, write the failing test
  first and confirm it fails for the expected reason.
- Write docstrings and comments as you go, following
  [`docs/engineering/code-documentation.md`](../../../docs/engineering/code-documentation.md).
- Treat external input, secrets and side effects as trust boundaries.

Read [references/testing.md](references/testing.md) when choosing or writing
tests. Read [references/debugging.md](references/debugging.md) only when a
failure is not explained by your change.

If the **how** changes, update the plan; mark affected steps `stale` and rerun
`decompose-tasks` when boundaries move. If the **what** changes, stop and ask.

## 3. Verify

Run all outcome-relevant checks and `python3 scripts/check_harness.py` before
you call anything done. Compare the observed behavior with each acceptance
criterion.

Never weaken, skip or delete a failing check, test, fixture or threshold to get
a green result. If a check seems wrong, stop and report it with evidence.

## 4. Close

- Record the exact commands and results in the step's `Result` (task graph) or
  in the final report. A failing or unrun required check never supports
  `done`.
- After a step is `done`, move dependent steps to `ready` only when all their
  dependencies are `done` and no decision or external blocker remains.
- If you stop early or someone else will continue, write
  `.work/<TASK-ID>-<slug>/handoff.md` from
  [assets/handoff.template.md](assets/handoff.template.md).
- Self-check the diff: every changed line traces to the task.
- Report: files changed, behavior delivered, checks and results, risks, next
  ready step. When all work for a spec is done, say it may move to
  `implemented`.
