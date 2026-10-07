# Local entry points. `make check` runs exactly what CI runs.

RUN := uv run --frozen

.PHONY: check up down stack-check doctor

check:
	uv sync --locked
	$(RUN) ruff format --check
	$(RUN) ruff check
	$(RUN) pyright
	$(RUN) lint-imports
	$(RUN) pytest
	$(RUN) pip-audit --skip-editable --progress-spinner off
	$(RUN) python scripts/check_harness.py
	$(RUN) python -m unittest discover -s tests/harness

# Build and start api and postgres; returns once both report healthy.
up:
	docker compose up -d --build --wait

# Stop the stack; the database volume is kept.
down:
	docker compose down

# Start the stack and verify health, recovery, loopback ports and log hygiene.
stack-check:
	python3 scripts/stack_check.py

# Check this host: architecture, Docker, uv, .env, disk, clock, connectivity.
doctor:
	python3 scripts/doctor.py
