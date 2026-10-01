---
name: review
description: Review a completed or in-progress change against its authoritative intent and the repository's engineering standards, using diff evidence and executed checks. Use when the user asks for code review, implementation verification, acceptance review, pre-merge review, or an independent assessment of whether a change is correct and ready, with or without a formal specification.
---

# Review an Implementation

Review the actual diff and observed behavior. Do not rely on the implementer's
summary as evidence.

Review is non-mutating by default. Report findings without editing unless the
user explicitly asks for fixes.

State whether the review is independent or a self-review. Treat only a fresh
session or agent that did not implement the change as independent; for an
independent review from an implementing session, delegate to the
`independent-reviewer` agent in `.claude/agents/`. High-risk
work reviewed only by its implementer must receive `blocked`, not `approved`.

## Establish scope

1. Resolve and record the fixed base/head or equivalent working-tree scope.
2. Capture committed and uncommitted changes within that scope.
3. Locate the authoritative intent: spec, accepted request, issue, contract, or
   reproduced prior behavior; then locate any plan and repository guidance.
4. Identify checks that can verify the acceptance criteria.

If no spec exists, verify against the available authoritative intent. Do not
invent missing intent; mark product conformance not applicable only when no
reliable source exists.

## Axis 1: intent conformance

Check:

- required behavior and acceptance criteria;
- traceability from available source items to tasks and evidence;
- missing, partial, or extra behavior;
- business rules, failures, and edge cases;
- externally observable quality constraints;
- unexplained deviation from confirmed scope.

## Axis 2: engineering quality

Check:

- correctness and regression risk;
- simplicity and unnecessary abstraction;
- unrelated or overly broad changes;
- data integrity and compatibility;
- trust boundaries, authorization, secrets, and unsafe effects;
- error handling, recovery, and observability;
- tests, static checks, and documentation;
- maintainability within repository conventions.

Read [references/trading-invariants.md](references/trading-invariants.md)
whenever the change touches market data, features, strategies, models, risk,
execution, accounting, scheduling, backtesting, or evaluation.

Read [references/security.md](references/security.md) only when the change
handles authentication, authorization, untrusted input, secrets, personal data,
payments, external actions, or another trust boundary.

## Validate

Run relevant checks when safe and available. Distinguish:

- observed evidence;
- source-based inference;
- unverified claim.

Do not approve solely because tests pass; tests may not cover the spec.

## Report

Order findings by severity: `critical`, `high`, `medium`, `low`. Any violation
of a non-negotiable invariant in `AGENTS.md` is `critical`. Each finding
must include evidence, location, impact, and the smallest recommended action.
Do not invent findings to fill categories.

Finish with one verdict:

- `approved`: no unresolved finding requires an implementation change; advisory
  low findings may remain;
- `changes-required`: one or more findings must be corrected before approval;
- `blocked`: required evidence, access, scope, or high-risk independence is
  missing, so a reliable verdict is not possible.

`approved` also requires no unresolved acceptance failure and all risk-required
evidence. An approving review supports a source spec's `verified` transition;
update it only when artifact maintenance is authorized. Independence is
mandatory only for high-risk work.

Use [assets/review.template.md](assets/review.template.md).
