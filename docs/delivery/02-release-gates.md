# Release gates

A gate closes when every listed block is `done` and the evidence below is linked
from the gate record (a PR or `docs/delivery/gates/` entry), with test
commands, owner approval and documented unresolved risks.

| Gate | Name | Blocks | Evidence required |
|---|---|---|---|
| 0 | Foundation | F01, F02 | local ARM64 boot, CI green without secrets, typed contracts, replay test |
| 1 | Point-in-time market data | D01 | real historical observations in both markets, gap/latency report, reproducible snapshot |
| 2 | Honest backtest | S01, E01, B01 | fees and next-event fills, no look-ahead tests, ledger invariants, baseline reports |
| 3 | Forward virtual trading | P01, U01 | fresh real feeds, kill switch, restart reconciliation, restore drill, unattended run in both markets |
| 4 | Research comparisons | I01, A01, X01 | external signals with provenance, preregistered baselines, ablations with uncertainty |
| 5 | Broker paper account (optional) | none yet | jurisdiction and entitlement verified ([OD-04](../product/open-decisions.md)); new ADR |

There is **no live-money gate**. Gates may overlap in time but close in order.
