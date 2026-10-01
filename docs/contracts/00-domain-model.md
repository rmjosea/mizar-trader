# Domain model contract (v1)

Canonical entities shared by every module. Changing this file requires explicit
human approval and updating all dependents in the same change (`AGENTS.md`).

## Global rules

- All timestamps are timezone-aware UTC. `available_at` is the earliest moment
  a value may influence a decision ([01-events](01-events.md)).
- Money, prices and quantities are `Decimal` with explicit currency and
  instrument precision; never `float` on the accounting path.
- Missing values are explicit (`null` plus a quality flag); no schema may
  reinterpret a missing value as zero.
- Every persisted record carries `schema_version`.

## Identifiers

- `instrument_id = {venue}:{asset_class}:{symbol}:{quote_currency}` with
  `asset_class` in lowercase, for example `NASDAQ:equity:AAPL:USD` or
  `COINBASE:crypto_spot:BTC:USD`. Provider symbols map to it through a stable
  mapping that survives symbol changes and corporate actions.
- Entity IDs (`decision_id`, `order_id`, `fill_id`, `run_id`, `snapshot_id`)
  are UUIDs unless stated otherwise.

## Entities

### Instrument

`instrument_id`, `asset_class` (`EQUITY` — includes ETFs — or `CRYPTO_SPOT`),
`venue`, `symbol`, `base_currency`, `quote_currency`, `timezone`, `tick_size`,
`lot_size`, `min_notional`, `session_calendar`, `active_from`, `active_to`.

### MarketObservation

`observation_id`, `instrument_id`, `kind` (`BAR` | `TRADE` | `QUOTE`),
`event_time`, `received_at`, `available_at`, `provider`, `feed` (for example
SIP, IEX, venue), `feed_tier`, `quality_flags`, `raw_ref`.

- `BAR`: `open`, `high`, `low`, `close`, `volume`, `interval_start`,
  `interval_end`, `closed` flag, `adjustment_policy`, `completeness` flag.
- `QUOTE`: `bid`, `ask`, `bid_size`, `ask_size`, `venue`.

### SourceDocument

`source_id`, `uri`, `provider_id`, `source_type`, `published_at`,
`first_seen_at`, `received_at`, `available_at`, `content_hash`,
`dedup_cluster_id`, `language`, `license_policy`, `instrument_ids`, `raw_ref`.

### Signal

`signal_id`, `instrument_id`, `source_refs` (event/document IDs),
`evidence_refs`, `category`, `direction`, `strength`, `horizon`, `confidence`
(nullable), `expires_at`, `model_id`, `model_version`, `prompt_version`.
`confidence` is not a calibrated probability unless a calibration experiment
validates it.

### Decision

| Field | Rule |
|---|---|
| `decision_id`, `run_id`, `strategy_id`, `strategy_version`, `portfolio_id`, `instrument_id` | required |
| `snapshot_id`, `snapshot_hash` | required; the exact inputs used |
| `action` | `TARGET` \| `HOLD` \| `ABSTAIN` |
| `target_weight` | `Decimal` in `[0, 1]`; **required for `TARGET`, `null` otherwise** |
| `reason_code` | required, machine-readable |
| `created_at`, `valid_until` | required; expired decisions are never executed |
| `confidence` | optional, uncalibrated |
| `rationale` | optional free text; untrusted, never executed |
| `model_id`, `model_version`, `prompt_version` | required when a model contributed |
| `error_code` | set when the strategy failed and abstained |

- `TARGET` sets a new target weight; `target_weight = 0` means exit the
  position.
- `HOLD` preserves the current target.
- `ABSTAIN` means no executable proposal (uncertainty, missing or stale data,
  error); the risk gate treats it as no action.
- The sum of `TARGET` weights in a portfolio is `<= 1`; the risk gate may
  reject or reduce.

### OrderIntent and Order

`intent_id`, `decision_id`, `portfolio_id`, `instrument_id`, `side` (`BUY` |
`SELL`), `quantity`, `order_type` (`MARKET` | `LIMIT`), `limit_price`
(required only for `LIMIT`), `time_in_force`, `client_order_id` (idempotency
key), `status`. The status lifecycle is defined by backlog task F02.

### Fill

`fill_id`, `order_id`, `instrument_id`, `quantity`, `price`, `fee`,
`fee_currency`, `slippage`, `fill_model_version`, `event_time`. Fills are
modeled, never claims of exchange execution.

### Ledger and valuation

Double-entry journal of cash, positions and fees with exact `Decimal`
arithmetic; timestamped mark-to-market valuations with the FX marks used.
