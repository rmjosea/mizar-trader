# Release gates

A gate closes when every listed task is `done` and the evidence below is linked
from the gate record (a PR or `docs/delivery/gates/` entry), with test
commands, owner approval and documented unresolved risks.

| Gate | Name | Tasks | Evidence required |
|---|---|---|---|
| 0 | Foundation | F01, F02, F03 | local ARM64 boot, CI green without secrets, typed contracts, replay test |
| 1 | Point-in-time market data | D01, D02, D03, D05 | real historical observations in both markets, gap/latency report, reproducible snapshot |
| 2 | Honest backtest | S01, S02, S03, E01, E02, R01, B01, B02, V01 | fees and next-event fills, no look-ahead tests, ledger invariants, baseline reports |
| 3 | Forward virtual trading | D04, P01, P02, U01, O01 | fresh real feeds, kill switch, restart reconciliation, restore drill, unattended run in both markets |
| 4 | Research comparisons | I01, I02, I03, A01, A02, A03, A04, X01 | external signals with provenance, preregistered baselines, ablations with uncertainty |
| 5 | Broker paper account (optional) | none yet | jurisdiction and entitlement verified ([OD-04](../product/open-decisions.md)); new ADR |

There is **no live-money gate**. Gates may overlap in time but close in order.
