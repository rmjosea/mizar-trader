# Trading invariants review

Check only the areas the change touches. Cite the file and line, or the test,
that proves or disproves each item.

## Time and information

- Every input to a decision carries `available_at`, and the code path filters
  `available_at <= decision_time`, not `event_time` or `published_at`.
- Rolling windows, normalization, scalers and labels are computed only from
  past data; no `shift(-n)`, full-series statistics, or fit-before-split.
- The universe is point-in-time (instruments active on that date), not today's
  list.
- Revised data (macro revisions, late corrections) creates a new version; prior
  decision inputs are never mutated.
- Signals generated on a bar close fill no earlier than the next eligible
  tradable event under the declared fill model.

## Money and accounting

- `Decimal` end to end for price, quantity, cash and fees; no `float` on the
  accounting path, including serialization and database columns.
- Currency is explicit; rounding follows instrument tick and lot size.
- Ledger stays double-entry: cash and holdings non-negative, fill quantities
  sum to the position delta, fees debited exactly once.
- Missing values are rejected or flagged, never coerced to zero.

## Boundaries and failure

- Strategies and models return proposals only; nothing outside `risk` approves
  an order intent; nothing outside `execution` changes balances.
- No live endpoint, live credential, or `LIVE` execution mode appears.
- Stale feed, missing FX, schema error, timeout or provider failure yields
  `ABSTAIN` or a risk rejection with a machine-readable reason.
- Effects are idempotent on their declared key; restart and replay do not
  duplicate orders, fills or decisions.
- Kill switch persists and blocks new orders while allowing reconciliation.

## Models and external text

- External documents are passed as quoted data; they cannot trigger tool
  calls, change policy, or reach commands.
- Model output is schema-validated; unknown symbols, prices or weights outside
  `[0, 1]` are rejected.
- Model ID, version, prompt hash, inputs hash, cost and latency are recorded;
  replay uses recorded responses.
- Self-reported confidence is never treated as a calibrated probability.

## Research validity

- Experiment criteria, splits, baselines and prompts match the preregistered
  manifest; changes after seeing results are a new version, not an edit.
- Historical LLM results are labeled as potentially contaminated.
- Reported metrics include costs, sample size and uncertainty; no alpha claim
  from a single favorable run.
