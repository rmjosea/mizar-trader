# External intelligence (news, macro, filings, social)

Turn timestamped public information into point-in-time, provenance-linked
signals that strategies may use as research features.

## Sources (v0)

| Source | Status |
|---|---|
| Licensed financial news or headlines | MVP |
| FRED macro data and release calendar | MVP |
| SEC EDGAR filings | MVP |
| Reddit | only if API access and terms permit; disabled otherwise |
| X, on-chain data | optional later adapters, disabled by default |

Use official APIs and licensed access only; no scraping against terms or
behind access controls. Respect rate limits and privacy.

## Pipeline

```text
ingest -> normalize -> deduplicate -> entity link -> event extraction and sentiment
  -> source-quality tags -> expiry -> snapshot
```

## Rules

- Each record keeps original URL or provider ID, author or publisher when
  allowed, `published_at`, `first_seen_at`, `received_at`, instrument mapping,
  language, license and retention policy, content hash and dedup cluster.
- Distinguish publication from revisions (macro) and filing effective
  availability.
- The LLM extractor outputs typed category, sentiment, relevance, horizon and
  evidence, and labels fact, opinion or rumor. No trading on unverified rumors
  by default.
- Documents are untrusted quoted data: they cannot request tool calls,
  secrets or policy changes.
- Social signals are noisy and manipulable: research features only.
- Backtests use only archived point-in-time data with a known first-seen time;
  current retrieval never backfills historical decisions.
- Evaluate with ablations: price-only, +news, +social, full, with cost
  attribution.

## Required tests

Syndicated story, edited article, false ticker match, deleted post, revised
macro series, late arrival, embedded malicious instruction, API rate limit.

## Acceptance

At least one real news event and one real macro, filing or social event
persisted with provenance, or an explicit unavailable-source status, without
fabricated signals.

## Backlog

I01, I02, I03.
