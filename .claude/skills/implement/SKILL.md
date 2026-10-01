---
name: implement
description: Implement one bounded change from an approved source artifact, one ready task from a task graph, or one confirmed direct-path request using small feedback loops, minimal changes, appropriate tests, and durable recovery state. Use when the user asks to execute, build, code, fix, or continue accepted work. Do not silently expand scope or implement unresolved blocked tasks.
---

# Implement a Bounded Change

Complete one bounded outcome at a time and leave the repository in a verifiable
state.

## Select and bound

1. Read `AGENTS.md`, the selected source artifacts, and only required contracts.
2. Select exactly one valid input:
   - a `ready` task from `tasks.md`: re-read task state, confirm every
     dependency is `done`, then transition it to `in-progress`;
   - one bounded, decision-complete outcome from an approved spec or plan that
     does not require a task graph: state the selected outcome and artifact
     evidence;
   - a direct-path change: confirm every direct-path condition in `AGENTS.md`
     and state `Intent`, `Change`, and `Verification` inline.
3. Inspect the affected code and tests before editing.
4. State the outcome, intended change surface, and validation.
5. Stop for a material ambiguity; do not invent product or architecture choices.

If execution changes **how**, update the durable plan or inline approach. When
a design change affects task boundaries, dependencies, validation, or change
surfaces, mark affected tasks `stale` and run `decompose-tasks` again before
continuing. If execution changes **what**, stop and reconfirm the accepted
intent; amend a spec when one exists or the expanded scope requires one. Mark
affected durable work stale.

## Execute

- Make the smallest coherent change that satisfies the task.
- Follow existing repository conventions before introducing new patterns.
- Avoid unrelated cleanup and speculative abstraction.
- Work in short edit-run-observe loops.
- Preserve compatibility unless the approved plan says otherwise.
- Treat external input, secrets, permissions, and destructive effects as trust
  boundaries.

Read [references/testing.md](references/testing.md) when selecting or writing
tests. Read [references/debugging.md](references/debugging.md) only when a
failure is not explained by the current change.

## Verify

Run the narrowest useful checks during iteration, then all outcome-relevant checks
before completion. Compare observed behavior with authoritative intent and the
applicable artifact or inline evidence.

Do not weaken, skip, or delete a failing check merely to obtain a green result.
Report checks that cannot run and why.

## Close

- When a task graph exists, update task state only when completion evidence
  exists, persist exact validation outcomes in task `Result` before marking it
  `done`, and never use a failing or unrun required check to support `done`.
- Without a task graph, record exact observed results in the final report or
  required handoff. Failing or unrun required validation cannot support
  completion.
- After completion, when a task graph exists, move newly unblocked tasks to
  `ready` only when every dependency is `done`, the blocker contains no
  decision, safety, or external reason, and no material decision remains.
- If a graph-backed task is interrupted, return it to `ready` only when retry
  is safe **and** no dependency, decision, safety, external, or validation
  blocker remains. Otherwise mark it `blocked` and record the reason. A retry
  being non-destructive does not make a task ready while its environment is
  still unavailable.
- Record deviations from the plan and their rationale.
- For direct-path work, self-check the final diff for scope, correctness, and
  unintended changes. Run standalone `review` only when requested, required by
  repository policy, or warranted by risk.
- Write or update `.work/<TASK-ID>-<slug>/handoff.md` whenever work stops unfinished
  or another session or agent may continue. Treat `tasks.md` as task-state
  truth and the handoff as a recovery snapshot.
- When all work scoped to a source spec is complete with evidence, report that
  it supports `implemented` and update the spec only when artifact maintenance
  is authorized.
- Summarize files changed, behavior delivered, checks run, results, risks, and
  the next ready task.

Use [assets/handoff.template.md](assets/handoff.template.md) for durable handoff.
