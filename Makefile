# Local entry points. `make check` runs exactly what CI runs.

RUN := uv run --frozen

.PHONY: check

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
