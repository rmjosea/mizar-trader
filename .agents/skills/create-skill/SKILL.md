---
name: create-skill
description: Creates, revises or evaluates an Agent Skill for this repository following the open Agent Skills specification, progressive disclosure and evaluation-first practice. Use when the user asks to add, improve, validate or benchmark a SKILL.md workflow or its references, assets or scripts. Not for repository-wide rules, which belong in AGENTS.md.
---

# Create or improve a skill

Build the smallest reusable procedure that measurably changes agent behavior.

## When a skill is the right tool

- Yes: a repeated multi-step procedure, or project knowledge needed only for
  some tasks.
- No: a one-off task, general knowledge the model already has, or a rule that
  applies to every task (put that in `AGENTS.md`).

## Steps

1. Collect two or more real requests that should trigger the skill and two
   similar requests that should not.
2. Run those requests without the skill and write down the actual failures.
   Write instructions only for observed failures.
3. Confirm the skill's responsibility and boundaries with the user (one
   question at a time).
4. Create `.agents/skills/<name>/SKILL.md`, then link it for Claude Code:
   `ln -s ../../.agents/skills/<name> .claude/skills/<name>`.
5. Rerun the requests with the skill; compare with step 2 and iterate.
6. Run `python3 scripts/check_harness.py`.

## Rules

- Follow [`docs/engineering/writing-for-agents.md`](../../../docs/engineering/writing-for-agents.md);
  this skill only adds what is specific to skills.
- Frontmatter only uses portable keys: `name`, `description`, and optionally
  `license`, `compatibility`, `metadata`, `allowed-tools`.
- `name`: lowercase letters, digits and hyphens; at most 64 characters; equal
  to the directory name.
- `description`: third person, at most 1024 characters, key use case first,
  then "Use when …" triggers and what it is not for.
- `SKILL.md` under 200 lines when possible, never over 500. Put detail in
  `references/` (read under a stated condition), templates in `assets/`, and
  fragile deterministic steps in `scripts/`. Keep references one level deep.
- Imperative instructions; one term per concept; concrete examples instead of
  long exception lists; no time-sensitive statements.
- Give a default, not a menu: name one recommended approach and an escape
  hatch.
- No README, changelog or diary inside a skill.
