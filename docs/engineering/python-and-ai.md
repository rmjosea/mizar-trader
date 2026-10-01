# Python and AI engineering standard

Normative for all application code. Docstrings and comments are covered by
[`code-documentation.md`](code-documentation.md). Tool commands are fixed by
backlog task F01; until then, these rules guide its design.

## Contents

1. Simplicity
2. Types and validation
3. Module boundaries
4. Money, time and determinism
5. AI and model code
6. Testing
7. Observability
8. Dependencies and security

## 1. Simplicity

- The simplest solution that fully meets the accepted need wins. Prefer a
  plain function or a deterministic rule over an agent loop when the steps are
  known ([Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).
- Prefer a maintainable heuristic over a model call when it is sufficient
  ([Google — Rules of ML, rule 3](https://developers.google.com/machine-learning/guides/rules-of-ml)).
- Every abstraction, parameter and configuration flag must serve a current,
  accepted requirement. Delete what no longer does.
- Keep `try` blocks minimal; avoid mutable global state and clever language
  tricks ([Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)).

## 2. Types and validation

- Python 3.12+ managed with `uv`, dependencies locked in `uv.lock`; `ruff` for
  lint and format; strict static type checking; `pytest` with Hypothesis.
- Every signature has real type hints. `Any` and `# type: ignore` need a
  comment explaining why no real fix exists.
- Every value crossing a boundary (API, provider, model, database, event) is a
  typed Pydantic v2 model or frozen dataclass, never a raw `dict`.
- Parse, don't validate: convert input into a precise type once, at the edge.
- Each validation rule lives in exactly one place; domain invariants are pure,
  unit-tested functions.

## 3. Module boundaries

The modules and their ownership are defined in
[`architecture/01-system.md`](../architecture/01-system.md).

- Dependencies point inward: domain code never imports adapters; application
  code depends on ports, and concrete adapters are injected at the edge.
- A new external integration is a new adapter behind a port, never a direct
  call from domain or application code.
- Domain code does not know that language models exist.

## 4. Money, time and determinism

- `Decimal` for money, prices and quantities everywhere on the accounting path,
  including JSON and database columns; build `Decimal` from strings, never from
  floats.
- Timezone-aware UTC `datetime` only; naive datetimes are rejected at the
  boundary.
- Inject the clock, providers and random seeds; nothing reads the wall clock
  or global randomness directly.
- Typed exceptions per port ([contracts/03](../contracts/03-provider-interfaces.md));
  never swallow an error on the decision, risk or execution path.

## 5. AI and model code

- **No rule is enforced only by a model.** Every constraint a prompt mentions
  (allowed instruments, weight range, expiry) is also enforced by
  deterministic code ([ADR-0003](../decisions/0003-ai-cannot-authorize-execution.md)).
- **Model output is untrusted input**: validate it against a schema before it
  reaches anything else
  ([OWASP Top 10 for LLM applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)).
- **Separate data from instructions.** Put news, filings and posts in clearly
  delimited data sections of a prompt, never inside the instruction text.
- **Own the prompts and the control flow.** Prompts are versioned files in the
  repository, reviewed like code and covered by tests. Application code
  decides when a model is called and what happens to its output
  ([12-Factor Agents](https://github.com/humanlayer/12-factor-agents)).
- **Minimal, structured context.** Give the model the smallest point-in-time
  snapshot that answers the question, in labeled sections, plus a few
  canonical examples instead of long lists of exceptions
  ([Anthropic — Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **Pin determinism settings in the adapter**: model version, temperature,
  seed, timeout, retries and budget are adapter configuration, recorded with
  every call.
- **Provider-neutral by construction**: a provider quirk lives in that
  provider's adapter only.

## 6. Testing

Keep "does it work" separate from "is it good":

1. **Deterministic unit and property tests** run on every change with no
   network. Code that calls a model uses the fake or replay adapter.
2. **Contract tests** run adapters against recorded, labeled fixtures.
3. **Replay tests** feed recorded model responses through the full decision
   path and assert the exact decisions.
4. **Live-model and live-provider checks** are opt-in, marked tests, run before
   merging a change that touches prompts, schemas or adapters; record the
   result in the pull request.
5. **Research evaluation** (strategy quality) follows
   [research/00](../research/00-research-protocol.md) and never decides
   correctness.

More detail per level: [delivery/03-test-strategy.md](../delivery/03-test-strategy.md).

## 7. Observability

- Structured JSON logs through the standard `logging` module, one event per
  record, with correlation IDs (`run_id`, `snapshot_id`, `decision_id`,
  `order_id`, `fill_id`).
- Every flow entry point (HTTP request, scheduled job, decision cycle, model
  call, order lifecycle) logs received, stage durations and outcome.
- Model calls use the OpenTelemetry GenAI attribute names where one fits
  (`gen_ai.request.model`, `gen_ai.usage.input_tokens`)
  ([OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)).
- **Never log**: secrets or API keys, licensed raw content, full model
  prompts or responses, or full serialized portfolios. Log IDs, hashes, counts,
  durations, reason codes and closed enum values.
- The level comes from `LOG_LEVEL`. Logging never changes behavior, and a
  logging failure never fails the flow.

## 8. Dependencies and security

- Add a dependency only when the standard library and current stack cannot do
  the job. The pull request states its purpose, license and maintenance status.
- Runtime dependencies on external research code require an approved
  `assess-external-code` verdict.
- Scan dependencies in CI; secrets reach the process only through the
  environment.
- Frontend: React, Vite and TypeScript in strict mode; the dashboard never
  holds credentials.
