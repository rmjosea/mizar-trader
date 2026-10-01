---
name: shape-idea
description: Turns a vague or early idea into a confirmed shared understanding through a one-question-at-a-time conversation, before any spec or code exists. Use when the request is exploratory, ambiguous, missing scope or success criteria, or the user asks to brainstorm, refine, challenge or validate what to build. Writes no files.
---

# Shape an idea

Reach an approved shared understanding of **what** to build and **why**. Stay
conversational. Create or edit no files.

## Steps

1. Restate the idea in one short paragraph, in the user's language.
2. Read the baseline docs that constrain it (start at `docs/README.md`); read
   code only when existing behavior matters.
3. Pick the single highest-impact open question.
4. Ask it using the format in `AGENTS.md` section 1: options, consequences, one
   **Recommended** option with its reason. Wait for the answer.
5. Update the working understanding and repeat from step 3.
6. Stop asking when the remaining uncertainty would not change scope,
   behavior, risk or research validity. Record it as an assumption.
7. Test the result against two or three concrete scenarios, including one
   failure case (for example: "the data feed is down at the daily close").
8. Present the output below and ask for explicit confirmation.

Choose each question from the evidence, the previous answers and the open
risks; never run a fixed questionnaire. Offer a simpler alternative whenever
one meets the goal.

## Output

```markdown
## Shared understanding

### Problem
### Desired outcome
### Users and scenarios
### In scope
### Out of scope
### Constraints (including AGENTS.md section 3 rules that apply)
### Acceptance signals (observable)
### Confirmed decisions
### Assumptions
### Remaining questions
```

Omit empty sections except `Remaining questions`; it must say `None` before
asking for approval.

## Boundaries

- Do not design the implementation unless it is an explicit constraint.
- Do not start `write-spec` on your own; silence is not approval.
