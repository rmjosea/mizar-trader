---
name: review
description: Reviews a change against its spec or plan task and the AGENTS.md rules, using the diff and checks it runs itself, and returns findings by severity with a verdict. Use for pre-merge review and for the independent review that critical work needs. Read-only unless the user asks for fixes.
---

# Review a change

Judge the actual diff and the observed behavior. Never treat the author's
summary as evidence.

State the independence: `independent` only when the reviewer did not write the
change (a fresh session, the `independent-reviewer` agent, or a human);
otherwise `self-review`. Critical work with only a self-review is `blocked`.

## Steps

1. Capture base, head and the diff. Find the source intent (spec acceptance
   criteria, plan task, or confirmed request); never invent it.
2. Check intent: every acceptance criterion is met with evidence; nothing
   required is missing; nothing unrequested was added.
3. Check engineering: correctness, simplicity, every changed line traces to
   the task, docstrings follow
   [code-documentation](../../../docs/engineering/code-documentation.md).
4. Check integrity: **no test, fixture, threshold, lint rule, metric or
   experiment criterion was weakened to pass.** Compare test changes with code
   changes.
5. Read [references/trading-invariants.md](references/trading-invariants.md)
   whenever the change touches market data, features, strategies, models,
   risk, execution, accounting, scheduling, backtesting or evaluation.
6. Run the relevant checks yourself. Label each conclusion **observed** or
   **unverified**.
7. Report with [assets/review.template.md](assets/review.template.md).

## Findings and verdict

Severity: `critical` (breaks an `AGENTS.md` section 3 rule), `high`, `medium`,
`low`. Each finding has evidence, location, impact and the smallest fix.
Report only what affects correctness, the rules or the acceptance criteria;
mark style preferences as optional.

- `approved`: nothing must change and the required evidence exists.
- `changes-required`: at least one finding must be fixed.
- `blocked`: evidence, access, scope or required independence is missing.
