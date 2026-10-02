---
name: review
description: Reviews a change against its source intent, the AGENTS.md rules and the engineering standards, using the diff and checks it runs itself, and returns findings by severity with a verdict. Use for code review, acceptance or pre-merge review, or an independent review of high-risk work. Read-only unless the user asks for fixes.
---

# Review a change

Judge the actual diff and observed behavior. Never treat the author's summary
as evidence.

State the independence: `independent` only when the reviewer did not write the
change (a fresh session, the `independent-reviewer` agent, or a human);
otherwise `self-review`. High-risk work with only a self-review gets `blocked`.

## 1. Establish scope

1. Record the base and head (or working-tree scope) and capture the diff.
2. Find the source intent: spec, backlog row, plan, or confirmed request. Do
   not invent missing intent.
3. List the checks that can prove each acceptance criterion.

## 2. Check intent

- Every acceptance criterion is met, with evidence.
- Nothing required is missing; nothing unrequested was added.
- Failure behavior and edge cases from the spec are handled.

## 3. Check engineering

- Correctness and regressions.
- Simplicity: would a senior engineer call it overcomplicated?
- Scope: every changed line traces to the task.
- **Integrity: no test, fixture, threshold, lint rule, metric or experiment
  criterion was weakened to pass.** Compare test changes with code changes.
- Data integrity, compatibility, error handling and observability.
- Docstrings and comments follow `docs/engineering/code-documentation.md`.
- Changed Markdown follows `docs/engineering/writing-for-agents.md`.

Read [references/trading-invariants.md](references/trading-invariants.md)
whenever the change touches market data, features, strategies, models, risk,
execution, accounting, scheduling, backtesting or evaluation.

Read [references/security.md](references/security.md) only when the change
touches authentication, untrusted input, secrets, external actions or another
trust boundary.

## 4. Validate

Run the relevant checks yourself when safe. Label each conclusion as
**observed**, **inferred from source**, or **unverified**. Passing tests alone
never justify approval.

## 5. Report

Use [assets/review.template.md](assets/review.template.md). Order findings
`critical`, `high`, `medium`, `low`; breaking an `AGENTS.md` section 3 rule is
`critical`. Each finding has evidence, location, impact and the smallest fix.
Report only findings that affect correctness, the rules or the stated
requirements; mark style preferences as optional.

Verdict:

- `approved`: no finding requires a change, and all risk-required evidence
  exists.
- `changes-required`: at least one finding must be fixed.
- `blocked`: evidence, access, scope or required independence is missing.

An approving review supports moving the spec to `verified`.
