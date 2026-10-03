# Local runtime

Where Mizar Trader runs locally and the resource rules it follows. The system
is containerized so it runs on any host with Docker, not only on the current
development machine.

Target: any host with Docker on Linux or macOS, arm64 or amd64; Windows only
through WSL2. Reference development machine: MacBook Pro M1 Pro, ~32 GB
unified memory, macOS arm64. Verify actual RAM and free disk before setup.

## Rules

- Use images that run natively on both arm64 and amd64; no mandatory
  emulation.
- Start with a Docker memory budget of 8–12 GB and adjust from measurements;
  leave headroom for the host's other work (IDE, browser).
- Bound data batches, queues, model concurrency and retention.
- Run baselines and backtests on CPU; use PyTorch MPS only for supported small
  experiments on Apple Silicon. Hosted LLM/Jev are reached through adapters
  with rate and cost caps. No local 30B+ model requirement.
- Keep raw data partitioned by provider/instrument/date; do not keep full tick
  history in the MVP.
- `make doctor` (backlog F01) checks architecture, RAM, disk, Docker, env file
  presence, time sync and connectivity without printing secrets; its exact
  checks and exit codes are in
  [SPEC-F01](../../specs/F01-platform-foundation/spec.md).

## Continuity limits

A sleeping or disconnected laptop invalidates continuous forward tests. Record
feed gaps and pause affected strategies; never synthesize missed decisions. Do
not infer 24/7 reliability from laptop runs; use the cloud runtime
([OD-09](../product/open-decisions.md)) for multi-week studies.
