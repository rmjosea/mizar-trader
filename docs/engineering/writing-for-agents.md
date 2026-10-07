# Writing files that agents read

How to write the Markdown an agent may load: `AGENTS.md`, docs, specs, skills
and plans. Less text, placed where it is needed, works better: long or
generic instruction files raise cost without raising success, and buried
rules get ignored.

## Rules

- **Only what the agent cannot infer.** Write project-specific rules,
  commands and non-standard practices. Never describe what the code or the
  file tree already shows, or general practice the model knows. Test each
  line: would removing it cause a mistake? If not, delete it.
- **Prefer a check to a sentence.** A rule that a linter, type checker, test
  or `scripts/check_harness.py` can enforce belongs there, not in prose.
- **Right place.** Rules for every task go in `AGENTS.md`; repeatable
  procedures in a skill; knowledge for some tasks in a `docs/` file listed in
  `docs/README.md`; what one block must deliver in its spec; how and progress
  in `.work/`.
- **Summary first.** Line 1 is the title, then one to three sentences on what
  the file is for. Most important rules first.
- **One home per fact.** Link instead of copying; two copies drift apart.
- **Self-contained sections.** Name the subject; link to a file and heading
  instead of writing "see above".
- **Exact words.** Use the glossary in `docs/contracts/00-domain-model.md`,
  imperative rules, absolute ISO dates, and runnable commands. Volatile facts
  (vendor status, versions, terms) carry "checked on YYYY-MM-DD" and live in
  `docs/research/01-external-code-and-sources.md` or
  `docs/product/open-decisions.md`.
- **Budgets.** `AGENTS.md` at most 200 lines; `SKILL.md` at most 500;
  other files about 300, split by purpose before that.
- **Maintain.** Update docs in the same change as the behavior; delete stale
  text (git keeps history). If agents keep ignoring a rule, the file is too
  long or the rule is buried.

## References

- Anthropic: [Claude Code best practices](https://code.claude.com/docs/en/best-practices),
  [Building effective agents](https://www.anthropic.com/research/building-effective-agents),
  [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- Gloaguen et al., [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988)
  (2026): context files help mainly for non-standard practices.
- Böckeler, [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
  (2026): guides versus sensors; deterministic checks run on every change.
