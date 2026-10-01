# Local runtime (Apple Silicon)

Target: MacBook Pro M1 Pro, ~32 GB unified memory, macOS ARM64. Verify actual
RAM and free disk before setup.

## Rules

- Use native ARM64 images; no mandatory x86 emulation.
- Start with a Docker memory budget of 8–12 GB and adjust from measurements;
  leave headroom for macOS, IDE and browser.
- Bound data batches, queues, model concurrency and retention.
- Run baselines and backtests on CPU; use PyTorch MPS only for supported small
  experiments. Hosted LLM/Jev are reached through adapters with rate and cost
  caps. No local 30B+ model requirement.
- Keep raw data partitioned by provider/instrument/date; do not keep full tick
  history in the MVP.
- `make doctor` (backlog F01) verifies architecture, RAM, disk, Docker, env
  file presence, time sync and connectivity without printing secrets.

## Continuity limits

A sleeping or disconnected laptop invalidates continuous forward tests. Record
feed gaps and pause affected strategies; never synthesize missed decisions. Do
not infer 24/7 reliability from laptop runs; use the cloud runtime
([OD-09](../product/open-decisions.md)) for multi-week studies.
