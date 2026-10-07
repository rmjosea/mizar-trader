"""Database reachability check used by the health endpoint."""

import asyncio
import logging

import psycopg

from mizar.config import Settings

logger = logging.getLogger(__name__)


async def check_database(settings: Settings) -> bool:
    """Report whether PostgreSQL accepts a query within the health timeout.

    Each call opens and closes its own connection, so the result recovers on
    its own when the database comes back.

    Args:
        settings: Connection parameters and the health timeout.

    Returns:
        True if ``SELECT 1`` succeeded in time, otherwise False.
    """
    try:
        async with asyncio.timeout(settings.health_timeout_seconds):
            connection = await psycopg.AsyncConnection.connect(
                host=settings.postgres_host,
                port=settings.postgres_port,
                user=settings.postgres_user,
                password=settings.postgres_password.get_secret_value(),
                dbname=settings.postgres_db,
            )
            async with connection:
                await connection.execute("SELECT 1")
    except (TimeoutError, OSError, psycopg.Error) as err:
        # Driver messages can name hosts or roles; log only the error type.
        logger.warning("database health check failed: %s", type(err).__name__)
        return False
    return True
