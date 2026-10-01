# Security review

Review only controls relevant to the changed trust boundaries:

- authentication and session lifecycle;
- authorization at every protected action and object boundary;
- validation and canonicalization of untrusted input;
- injection into queries, commands, templates, paths, or prompts;
- secret handling and accidental logging;
- personal or regulated data collection, retention, and exposure;
- destructive or external side effects, idempotency, and confirmation;
- dependency and supply-chain changes;
- secure failure behavior and rate or resource limits.

Prefer concrete exploit paths and evidence over generic checklist warnings.

