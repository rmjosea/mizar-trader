# Open decisions

Business and technical choices that are not yet made. Adapters stay replaceable
so none of these blocks the offline foundation. Resolve each one through the
human decision protocol in `AGENTS.md`, then record the outcome here (and as an
ADR when it is architectural) before code depends on it.

| ID | Decision | Blocks | Options and notes | Status |
|---|---|---|---|---|
| OD-01 | Primary US equity data provider and subscription tier | D01, P01 | Must declare feed (IEX-only vs consolidated SIP), delay and redistribution rights. IEX-only and consolidated data are never treated as equivalent. | open |
| OD-02 | Crypto venue(s) for market data | D01, P01 | Venue determines quote currency (USD vs USDT/USDC), pairs and API limits. | open |
| OD-03 | Base reporting currency | E01, B01 | EUR (operator's home currency) vs USD (instrument currency). Affects FX feed requirements and stale-FX rules. | open |
| OD-04 | Broker paper account availability in Spain | Gate 5 | Gate 5 is optional and post-MVP; verify jurisdiction, terms and data entitlements first. | open |
| OD-05 | Monthly budget for data and model inference | D01, A01 | Sets daily spend caps and provider choice. | open |
| OD-06 | Object storage implementation | F01, D01 | MinIO Community Edition is archived (no maintained images since late 2025; archived April 2026). Candidates: local content-addressed filesystem behind an object-store port (simplest for MVP), Garage, SeaweedFS, RustFS. | open |
| OD-07 | Exact Python version pin | F01 | **Python 3.14**, approved by the operator on 2026-10-04. It is the only release in bugfix support (3.12 and 3.13 are security-only; 3.15 is a prerelease). PyPI check on 2026-10-04: every candidate library in the architecture and Python standard ships cp314 wheels for macOS ARM64 and Linux x86_64/aarch64, or is pure Python. Upgrade constraint: vectorbt 1.1.1 requires `<3.15`; DuckDB, PyArrow, torch and asyncpg had no cp315 wheels yet. | resolved |
| OD-08 | Reasoning LLM provider(s) and Jev access | A01 | Jev (TypeSafe) was announced 2026-09-15 in early access; verify API, terms and benchmark-publication rules before integration. | open |
| OD-09 | Always-on runtime for multi-week forward tests | U01, Gate 3 | A laptop that sleeps invalidates continuous runs; choose a cloud host compatible with ARM64/amd64 images. | open |
