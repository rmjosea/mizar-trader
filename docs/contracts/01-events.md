# Events and temporal semantics (v1)

The binding event envelope, the timestamps that decide when data may be
used, and the replay invariants.

## Envelope

| Field | Meaning |
|---|---|
| `event_id` | UUID, unique |
| `type`, `schema_version` | event name and payload version |
| `source` | producing module or provider |
| `occurred_at` | when it happened according to the source (provider event time) |
| `received_at` | when this system received it |
| `available_at` | earliest time it may influence a decision |
| `correlation_id`, `causation_id` | flow trace and direct parent event |
| `run_id` | backtest or forward run, when applicable |
| `payload`, `payload_hash` | content and its hash |

Keep original provider timestamps and local reception timestamps.

## Availability

```text
available_at = max(published_at, received_at, embargo_or_entitlement_time)
```

Reject any input whose `available_at` is later than the decision time.

For data that was not captured live (historical backfill), `received_at` is not
the download time. Instead:

- **Market observations**: `available_at = interval_end + declared provider
  publication lag` (bars) or the provider event time (trades, quotes), and the
  record carries a `backfilled` quality flag.
- **Source documents**: only an archived `first_seen_at` from a point-in-time
  archive establishes availability. Documents without one are ineligible for
  backtests; current retrieval never backfills historical availability.
- **Revised series** (for example macro data): use the vintage that was
  published at the decision time, never the latest revision.

## Event types

`MarketObservationAccepted`, `SourceDocumentAccepted`,
`FeatureSnapshotCreated`, `SignalCreated`, `DecisionProposed`, `RiskApproved`,
`RiskRejected`, `VirtualOrderAccepted`, `VirtualFillRecorded`,
`PortfolioValued`, `FeedStale`, `KillSwitchChanged`.

## Invariants

- At-least-once delivery is allowed; effects happen exactly once through unique
  IDs.
- Deterministic ordering: `available_at`, then `event_id`.
- Replay with pinned data, configuration and recorded AI outputs produces
  identical state.
- Late or corrected data creates a new version; previous decision inputs are
  never mutated.
