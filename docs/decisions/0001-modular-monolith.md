# ADR-0001: Modular monolith

- Status: accepted
- Date: 2026-09-25

## Context

The system has many bounded areas (market data, intelligence, features,
strategies, portfolio, risk, execution, evaluation, API) but one operator and
one deployment target. Independent contracts matter; independent deployment
does not.

## Decision

Build a modular monolith: one Python codebase with enforced module boundaries,
an API process, a separate scheduler/worker process, a shared PostgreSQL
database and an immutable object store. Microservices and message brokers are
deferred until an operational need is measured.

## Consequences

- Module boundaries must be enforced by imports and tests, not by the network.
- Restart safety relies on transactional outbox/inbox patterns in PostgreSQL.
- Splitting a module out later requires only its contract, not a rewrite.
