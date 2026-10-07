"""FastAPI application factory and the health endpoint."""

from collections.abc import Awaitable, Callable
from functools import partial
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from mizar.api.health import check_database
from mizar.config import Settings

type DatabaseProbe = Callable[[], Awaitable[bool]]


class HealthReport(BaseModel):
    """Body of ``GET /health``; it never carries hosts, versions or secrets.

    Attributes:
        status: ``ok`` when every dependency is healthy.
        database: ``ok``, or the reason the database is unavailable.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    status: Literal["ok", "unavailable"]
    database: Literal["ok", "database unavailable"]


def create_app(
    settings: Settings, database_probe: DatabaseProbe | None = None
) -> FastAPI:
    """Build the api application.

    Args:
        settings: Validated process configuration.
        database_probe: Replaces the real database check; tests pass a fake.

    Returns:
        The configured FastAPI application.
    """
    probe = database_probe or partial(check_database, settings)
    app = FastAPI(
        title="Mizar Trader API", docs_url=None, redoc_url=None, openapi_url=None
    )

    # FastAPI registers the route through the decorator; Pyright cannot see
    # that use and reports the function as unused.
    @app.get("/health", response_model=HealthReport)
    async def health() -> JSONResponse:  # pyright: ignore[reportUnusedFunction]
        """Report 200 when PostgreSQL answers a query, otherwise 503."""
        if await probe():
            report = HealthReport(status="ok", database="ok")
            return JSONResponse(report.model_dump(), status_code=200)
        report = HealthReport(status="unavailable", database="database unavailable")
        return JSONResponse(report.model_dump(), status_code=503)

    return app
