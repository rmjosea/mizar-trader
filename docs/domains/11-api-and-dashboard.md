# API and dashboard

## Purpose

Let the operator inspect every decision end to end and stop virtual execution.

## API

Read-only by default:
`GET /health`, `/instruments`, `/feeds/status`, `/experiments`,
`/experiments/{id}`, `/portfolios`, `/portfolios/{id}/orders`,
`/decisions/{id}`, `/signals`, `/risk/incidents`.

Authenticated, audited operator actions: `POST /paper/start`, `/paper/stop`,
`/kill-switch`.

## Dashboard

Market and feed timestamps and tier with stale badges, strategy comparison,
equity curves, risk and exposure, fees, model spend, source evidence,
decision-to-fill trace and errors. Local virtual P&L is visibly distinct from
broker-confirmed paper P&L.

## Required tests

Authorization, pagination, no secret leakage, timezone display, stale badge,
portfolio isolation.

## Acceptance

The operator can inspect any decision through to its fills and can stop
virtual execution.

## Backlog

U01.
