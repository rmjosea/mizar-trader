---
name: create-skill
description: Create, revise, or evaluate an Agent Skill that follows the open Agent Skills specification, Anthropic-style quality practices, progressive disclosure, and repository portability. Use when the user asks to add, design, improve, validate, benchmark, or review a SKILL.md workflow or its scripts, references, assets, triggers, and evaluation cases.
---

# Create a High-Quality Agent Skill

Create the smallest reusable procedure that reliably changes agent behavior.

## Select the mode

- `create` or `revise`: change files only after responsibility and boundaries
  are confirmed; report files changed and validation results.
- `evaluate`: do not mutate by default; report evidence-backed findings by
  severity, non-findings worth preserving, and `approved`,
  `changes-required`, or `blocked`.
- `benchmark`: define positive and adjacent-negative prompts, quality rubrics,
  fresh-session procedure, baseline without the skill, and comparable results.

## Understand with examples

1. Gather two or more realistic requests that should use the skill.
2. Gather requests that look similar but should not use it.
3. Identify the repeated procedure, non-obvious knowledge, and failure modes.
4. Ask one material question at a time using `AGENTS.md`.
5. Confirm the skill's responsibility and boundaries before creating files.

Do not create a skill for one-off context, generic intelligence the model
already has, or durable repository rules that belong in `AGENTS.md`.

## Design progressive disclosure

Use three levels:

1. `name` and `description` for discovery;
2. concise `SKILL.md` instructions for activation;
3. `references/`, `scripts/`, and `assets/` loaded or executed only as needed.

Keep `SKILL.md` preferably under 200 lines and always under 500 lines. Keep
references one level deep. State the exact condition for reading each resource.
Do not duplicate information between files.

## Choose resources

- `scripts/`: deterministic or repeatedly rewritten operations; execute tests.
- `references/`: focused knowledge needed only in specific conditions.
- `assets/`: templates or output resources not intended as instructions.

Create no directory or file without a concrete use. Do not add auxiliary
README, changelog, installation guide, or process diary inside a skill.

## Write metadata

Use YAML frontmatter containing at least:

```yaml
---
name: verb-led-name
description: What the skill does. Use when ... Include concrete triggers.
---
```

Use lowercase letters, digits, and hyphens. Make the description discriminate
both intended use and adjacent non-use through precise triggers.

## Write instructions

- Use imperative language.
- Put the reusable workflow before background explanation.
- Match freedom to risk: guidance for judgment, scripts for fragile operations.
- Define preconditions, stopping conditions, output contract, and quality gate.
- Preserve user control for irreversible, risky, or materially ambiguous work.
- Avoid provider-specific features in a portable skill.

## Evaluate

Validate:

- structure and metadata;
- intended activation on positive examples;
- non-activation on adjacent negative examples;
- output and workflow quality on realistic tasks;
- scripts by executing representative cases;
- reference links and context size;
- permissions, external input, and supply-chain risks.

Run `python3 scripts/check_harness.py` from this repository when available. Iterate
from observed failures rather than adding speculative instructions.

## Attribution

Review the license of any adapted source. Prefer original wording. Preserve
required notices and identify substantial borrowed material.
