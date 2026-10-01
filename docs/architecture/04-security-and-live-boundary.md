# Security and live-execution boundary

## Execution boundary

- The execution-mode enum contains only `BACKTEST` and `PAPER`.
- No live adapter, live endpoint or live credential exists in the codebase.
- Live trading would require a new ADR, implementation, credentials, approval
  and staged rollout; it is out of scope
  ([ADR-0002](../decisions/0002-real-data-virtual-money.md)).

## Secrets

- Separate API keys for market data and for broker paper accounts.
- Inject secrets through environment or a local secret manager; commit only
  `.env.example`. Never log secrets or expose them to the frontend.

## Untrusted input

- Model output: strict schema, instrument allowlist, size limits, TTL, source
  provenance; no free text reaches commands or execution parameters.
- External documents: quoted data only; isolated from tools so embedded
  instructions cannot trigger actions (prompt-injection resistance).
- Broker and webhook events: idempotent, and signature-verified when the
  provider supports it.

## Risk independence

The risk service is independent of any model and denies by default on stale
feed, missing FX, unknown holdings, provider outage, inconsistent balances or
duplicate order IDs. The kill switch persists across restarts and blocks new
orders while allowing reconciliation. Every decision and risk verdict is
audited.

## API

Authentication is required whenever the API is reachable beyond localhost;
CSRF and CORS are restricted. Operator actions are audited.

## External code

Adoption requires a pinned commit, license review, dependency scanning and
isolation; follow the `assess-external-code` skill.
