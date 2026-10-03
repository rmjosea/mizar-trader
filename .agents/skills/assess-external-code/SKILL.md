---
name: assess-external-code
description: Assesses an external repository, library, dataset, model API or published strategy before Mizar Trader adopts, copies, benchmarks or depends on it, covering license, provenance, security, data leakage, fill assumptions and reproduction of claimed results. Use when someone proposes a new dependency, copying code, integrating a vendor model such as Jev, or citing third-party performance. Not for version bumps of already-approved dependencies.
---

# Assess External Code or Claims

Produce an evidence-based adoption verdict. Never treat a README, paper, equity
curve, or vendor announcement as evidence of profitability.

## Preconditions

1. Read `AGENTS.md` and
   [`docs/research/01-external-code-and-sources.md`](../../../docs/research/01-external-code-and-sources.md).
2. Identify the intended use: `reference-only`, `isolated-benchmark`,
   `optional-plugin`, or `runtime-dependency`. Rigor increases in that order.
3. A new dependency or external code is `high` risk (`AGENTS.md` section 5);
   the verdict needs human approval.

## Assess

Record facts with their source and retrieval date:

- identity: URL, owner, pinned commit SHA or version, last release, activity;
- license and terms, including data, model-output and benchmark-publication
  restrictions; incompatible or unclear terms block adoption;
- supply chain: dependency tree, known vulnerabilities, install scripts,
  network calls, telemetry, credential handling;
- method: markets, period, data vendor, point-in-time treatment, splits,
  costs, fill model, number of runs, uncertainty;
- leakage: look-ahead, survivorship, full-series normalization, training
  contamination for LLMs;
- claims: reported metrics versus independently reproduced metrics.

Reproduce only inside an isolated sandbox with pinned dependencies, no live
credentials and no repository secrets. Label anything not reproduced as
`unverified`.

## Output

Use [assets/assessment.template.md](assets/assessment.template.md) and save it
to `.work/<TASK-ID>-<slug>/assessment.md`. Finish with one verdict:

- `adopt`: meets the bar for the stated intended use;
- `adopt-isolated`: usable only as reference or isolated benchmark;
- `reject`: license, security, leakage, or provenance blocks use;
- `blocked`: evidence or access is missing for a reliable verdict.

## Quality gate

- Every claim is labeled `verified`, `reproduced`, or `unverified`.
- The commit or version is pinned and the license is quoted, not guessed.
- No code is copied before an `adopt` verdict is approved by a human.
