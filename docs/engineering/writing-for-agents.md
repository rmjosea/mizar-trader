# Writing files that agents read

How to write every Markdown file an agent may load: `AGENTS.md`, docs, specs,
skills, plans and handoffs. The goal is the smallest set of clear, high-signal
text that lets an agent act correctly, loaded only when it is needed.

## Contents

1. Why this matters
2. Progressive disclosure
3. Where content belongs
4. File shape and budgets
5. One purpose per file, one home per fact
6. Self-contained sections
7. Precise language
8. Formatting
9. Time-sensitive facts
10. Maintenance
11. What the harness checks
12. References

## 1. Why this matters

An agent's context window is a limited budget. Every model tested gets less
accurate as its input grows; facts in the middle of a long input are recalled
worst; and plausible but irrelevant text distracts more than random text. So:
load less, put the important part first, and keep unrelated material out.

## 2. Progressive disclosure

Information is layered. Each layer is small and tells the agent exactly when
to open the next one.

| Level | Loaded | In this repository |
|---|---|---|
| 0. Always | at session start | `AGENTS.md` |
| 1. Signposts | at start, or when browsing | skill `name` and `description`; `docs/README.md` and `specs/README.md` indexes; file names; headings |
| 2. Body | when the signpost matches the task | one document, one spec, or one `SKILL.md` |
| 3. Detail | only under a stated condition | skill `references/`, `assets/`, `scripts/`; `.work/` files |

Rules:

- Put in level 0 only what every task needs. Everything else gets a level 1
  signpost.
- Every link to deeper content states **when** to read it.

  ```markdown
  Good: Read [references/trading-invariants.md](references/trading-invariants.md)
        whenever the change touches risk, execution or accounting.
  Bad:  See also references/trading-invariants.md.
  ```

- Keep detail **one level deep** from its entry point: an index links to
  documents, and a `SKILL.md` links to its references. A reference never sends
  the agent on to another reference.
- Split content that is used in different situations into separate files, so
  one task never loads text for another.
- Give the agent a way to search instead of reading: descriptive file names,
  headings and stable terms let `grep` find the one section needed.

## 3. Where content belongs

| Content | Home |
|---|---|
| A rule that applies to every task | `AGENTS.md` |
| A repeatable multi-step procedure | a skill in `.agents/skills/` |
| Knowledge needed for some tasks | a document in `docs/`, listed in `docs/README.md` |
| A binding schema, event or interface | `docs/contracts/` |
| A decision and its reasons | `docs/decisions/` (ADR) |
| What one task must deliver | `specs/<TASK-ID>-<slug>/spec.md` |
| How and in what order, progress, handoff | `.work/<TASK-ID>-<slug>/` |
| Anything the agent can derive from the code | nowhere; do not write it |

## 4. File shape and budgets

- Line 1 is the title (`# …`). Then one to three sentences that say what the
  file is for, before the first `##` heading. An agent must be able to decide
  from those lines whether to keep reading.
- Put the most important rules first, not in the middle.
- Files over 100 lines start with a `## Contents` list.
- Names are lowercase kebab-case; prefix `NN-` when reading order matters
  (`01-system.md`). Headings name their subject (`## Risk policy`, not
  `## Details`).

| File | Budget |
|---|---|
| `AGENTS.md` | 200 lines |
| `SKILL.md` | 200 lines preferred, 500 maximum |
| Any other document or spec | 300 lines; split by purpose before that |

Test every line: would removing it cause an agent to make a mistake? If not,
remove it.

## 5. One purpose per file, one home per fact

- Each document has one type: **rule** (`AGENTS.md`, standards), **procedure**
  (skills), **reference** (contracts, domain baselines, indexes) or
  **explanation** (ADRs, research). Do not mix procedures into references or
  long rationale into rules.
- Each fact lives in exactly one file. Other files link to it; they never copy
  it. Two copies drift apart, and an agent may follow either one.
- When two files disagree, the authority order in `docs/README.md` decides;
  fix the lower one in the same change.

## 6. Self-contained sections

Agents often read one section, found by search, without what comes before it.

- Name the subject in each section. Write "the risk gate rejects…", not "it
  rejects…".
- Never write "see above", "see below" or "as mentioned earlier"; link to the
  file and heading.
- Keep a constraint next to the thing it constrains.

```markdown
Good: The scheduler is idempotent on (strategy_id, instrument_id, bar_end).
Bad:  As noted above, this must also be idempotent.
```

## 7. Precise language

- Use the glossary terms from `docs/contracts/00-domain-model.md`; one term per
  concept, everywhere.
- Write rules in the imperative. Reserve "never" and "always" for real hard
  rules so they keep their weight.
- Be specific enough to verify: "run `python3 scripts/check_harness.py`", not
  "check your work".
- Prefer one or two canonical examples over a long list of exceptions.
- Give a default, not a menu: name the recommended option and the condition
  for the alternative.

## 8. Formatting

- Plain Markdown only: headings, short lists, tables for mappings, fenced code
  blocks with a language tag. No HTML; no essential information only inside an
  image.
- Relative links with paths that resolve from the file's own folder.
- Front matter only where a tool reads it (skills, specs, plans).

## 9. Time-sensitive facts

- Use absolute ISO dates (`2026-10-02`), never "recently", "new" or
  "currently".
- Volatile facts (vendor status, prices, API terms, versions) carry
  "checked on YYYY-MM-DD" and live in one place:
  `docs/research/01-external-code-and-sources.md` or
  `docs/product/open-decisions.md`.

## 10. Maintenance

- Update the affected documents in the same change as the behavior.
- Delete stale content; do not keep it "for history" (git keeps history).
- If an agent keeps ignoring a rule, the file is probably too long or the rule
  is buried: shorten the file or move the rule up a level. If agents keep
  asking something a file answers, its wording is ambiguous.
- In long tasks, keep progress and decisions in `.work/<TASK-ID>-<slug>/`
  files, not only in the conversation; they survive context resets.
- A subagent returns a short, structured summary, not its raw findings.

## 11. What the harness checks

`python3 scripts/check_harness.py` enforces the mechanical part of this
standard:

- title on line 1 and a summary before the first `##` in `docs/` and specs;
- `## Contents` in files over 100 lines;
- line budgets for `AGENTS.md`, `SKILL.md`, documents and specs;
- every document in `docs/` is listed in `docs/README.md`;
- every file inside a skill is linked from its `SKILL.md`, and references do
  not link to further references;
- no "see above" or "see below";
- every relative link resolves.

## 12. References

- Anthropic: [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
  [Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills),
  [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- Chroma: [Context rot](https://www.trychroma.com/research/context-rot); Liu et
  al.: [Lost in the middle](https://arxiv.org/abs/2307.03172).
- [Diátaxis](https://diataxis.fr/) (one purpose per document);
  [llms.txt](https://llmstxt.org/) (concise, link-based indexes);
  [kapa.ai: writing documentation for AI](https://docs.kapa.ai/improving/writing-best-practices)
  (self-contained sections).
