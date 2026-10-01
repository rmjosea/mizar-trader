# External code, data and sources

Use the `assess-external-code` skill before adopting, vendoring, benchmarking
or depending on anything listed here.

## Adoption policy

- Pin the commit or version; verify the actual license and terms (including
  data, model-output and benchmark-publication restrictions).
- Check dependencies and security; run a minimal example in an isolated
  sandbox with no live credentials.
- Inspect data leakage and fill assumptions; reproduce claimed metrics.
- Preserve attribution; never copy code wholesale before an approved verdict.
- Published performance figures are unverified until reproduced. A repository
  is never "profitable" because it has code or an equity curve.

## Evidence ladder

1. Historical backtest.
2. Leakage-controlled out-of-sample test.
3. Prospective paper (virtual) results.
4. Audited live fills (out of scope for this project).

For each candidate record: URL, authors, paper DOI/arXiv, license, commit SHA,
last release, markets and dates, data vendor, benchmark, costs, split method,
point-in-time treatment, number of runs, uncertainty, compute needs, and
reported versus reproduced metrics. Reject promotion if an advantage disappears
under plausible fees, delayed signals or alternate windows. Log negative
results.

## Candidates

| Candidate | Intended use | Notes |
|---|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | reference, isolated benchmark | multi-agent research scaffold; no fixed reproducible returns |
| [FinRL](https://github.com/AI4Finance-Foundation/FinRL) / [FinRL-Trading](https://github.com/AI4Finance-Foundation/FinRL-Trading) | later RL benchmark | upstream points production work to newer branches; review each independently |
| [Freqtrade](https://github.com/freqtrade/freqtrade) and [FreqAI](https://www.freqtrade.io/en/stable/freqai/) | architecture reference | do not mix its fills with ours without calibration |
| [vectorbt](https://github.com/polakowo/vectorbt) | optional cross-check (B02) | not the authoritative event or ledger engine |
| [Fin-JEPA](https://github.com/cedricwyh/fin-jepa) | optional representation research | no live alpha evidence |
| Jev by TypeSafe ([announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev)) | capability-gated adapter (A03) | announced 2026-09-15, early access; vendor claims unverified; third-party "Jev trading" repositories need provenance checks |

## Data and broker sources

| Source | Notes |
|---|---|
| [Alpaca market data](https://docs.alpaca.markets/docs/about-market-data-api) | coverage depends on entitlement; the basic feed is IEX-only |
| [Alpaca paper trading](https://docs.alpaca.markets/docs/paper-trading) | simulated execution differs from live; Gate 5 only |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | filings |
| [FRED API](https://fred.stlouisfed.org/docs/api/fred/) | macro data; track revisions |
| [Reddit developer terms](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Reddit-Developer-Platform) | use only if permitted |

Links were checked on 2026-09-25; Jev status on 2026-10-01. Verify current
terms, licenses, entitlements and jurisdiction before each integration.
