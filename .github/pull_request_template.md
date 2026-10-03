## Task

- Plan task: <!-- e.g. F02-T03 -->
- Spec / plan: <!-- SPEC-F02, .work/F02-... or "direct path" -->
- Risk: <!-- low | medium | high -->

## Change

<!-- What changed and why, in a few lines. -->

## Verification

<!-- Commands run and their actual results. -->

## Invariants checked

- [ ] No live execution path, endpoint or credential
- [ ] Point-in-time: no input with `available_at` after decision time
- [ ] `Decimal` money; missing values not coerced to zero
- [ ] Idempotent effects and replay
- [ ] Untrusted text never reaches commands or execution
- [ ] No test, fixture, threshold, metric or experiment criterion weakened to pass
- [ ] Docstrings and comments follow docs/engineering/code-documentation.md
- [ ] Not applicable (documentation or tooling only)
- [ ] Backlog status and affected docs updated

## Review

- Independence: <!-- independent | self-review (high risk requires independent) -->

## Remaining risks and follow-up
