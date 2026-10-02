# AI model code standard

How code that calls language models or other AI models (LLM, Jev, ML) is
built, tested and observed. It adds to [`python.md`](python.md); the
architectural rule behind it is
[ADR-0003](../decisions/0003-ai-cannot-authorize-execution.md).

## Contents

1. Control and trust
2. Prompts and context
3. Adapters
4. Testing
5. Observability
6. References

## 1. Control and trust

- **No rule is enforced only by a model.** Every constraint a prompt mentions
  (allowed instruments, weight range, expiry) is also enforced by
  deterministic code.
- **Model output is untrusted input.** Validate it against a Pydantic schema
  before anything else reads it; unknown symbols, prices not present in the
  snapshot and weights outside `[0, 1]` are rejected.
- **Application code owns the control flow.** It decides when a model is
  called and what happens to the output; no framework loop decides for it.
- **Prefer a deterministic rule or heuristic** over a model call when it is
  sufficient and maintainable.

## 2. Prompts and context

- Prompts are versioned files in the repository, reviewed like code, and
  identified by a content hash recorded with every call.
- Put news, filings and posts in clearly delimited data sections, never inside
  the instruction text. Assume they contain injection attempts.
- Give the model the smallest point-in-time snapshot that answers the
  question, in labeled sections, plus one or two canonical examples instead of
  long lists of exceptions.
- Add a prompt instruction only for an observed failure, ideally captured by a
  test; remove instructions that no longer match a live failure.
- Ask for structured output (typed fields, closed enums), never free text that
  code must interpret.

## 3. Adapters

- Each provider is one adapter behind the `ModelProvider` port
  ([contracts/03](../contracts/03-provider-interfaces.md)); a provider quirk
  never leaks out of its adapter.
- The adapter pins and records the determinism settings: model ID and version,
  temperature, seed when supported, timeout, retry policy and budget.
- Retry only idempotent, read-only inference, with a bounded number of
  attempts and backoff; a timeout, refusal or budget breach becomes
  `ABSTAIN`, never a fallback decision.
- A mock adapter and a replay adapter (recorded responses) exist for every
  model-backed strategy.

## 4. Testing

Keep "does it work" separate from "is it good":

1. **Deterministic tests** use the mock or replay adapter, never the network,
   and run on every change.
2. **Replay tests** run recorded responses through the full decision path and
   assert the exact decisions.
3. **Adversarial tests** feed malformed output, invalid schemas, hallucinated
   symbols and prompt-injection text, and assert a safe `ABSTAIN` or
   rejection.
4. **Live-model checks** are opt-in, marked tests, run before merging a change
   to a prompt, schema or adapter; the pull request records the result.
5. **Strategy quality** is a research question answered by the protocol in
   [research/00](../research/00-research-protocol.md), never by unit tests,
   and never by a model grading itself.

## 5. Observability

- Record per call: provider, model and version, prompt hash, schema version,
  input and output hashes, token usage, cost, latency, outcome, and a
  reference to the stored raw response.
- Use the OpenTelemetry GenAI attribute names where one fits
  (`gen_ai.request.model`, `gen_ai.usage.input_tokens`).
- Never log full prompts, raw responses or API keys; log hashes and
  references.
- Enforce a daily spend cap per provider and alert before it is reached.

## 6. References

- Anthropic: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents),
  [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents).
- [OWASP Top 10 for LLM applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).
- Google: [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml).
