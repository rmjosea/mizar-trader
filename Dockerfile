# Image of the api process. Both stages use the same base so the virtual
# environment's interpreter path stays valid.

FROM ghcr.io/astral-sh/uv:0.12.5 AS uv

FROM python:3.14.8-slim AS build
COPY --from=uv /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project
COPY src ./src
RUN uv sync --locked --no-dev --no-editable

FROM python:3.14.8-slim
RUN useradd --system --no-create-home --uid 10001 mizar
COPY --from=build /app/.venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH PYTHONUNBUFFERED=1
USER mizar
CMD ["python", "-m", "mizar.api"]
