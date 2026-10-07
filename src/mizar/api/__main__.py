"""Entry point of the api process: ``python -m mizar.api``."""

import logging
import sys

import uvicorn

from mizar import log
from mizar.api.app import create_app
from mizar.config import ConfigurationError, load_settings

logger = logging.getLogger("mizar.api")


def main() -> int:
    """Load the configuration and serve the api until stopped.

    Returns:
        0 after a clean shutdown; 1 if the configuration is missing or invalid.
    """
    try:
        settings = load_settings()
    except ConfigurationError as err:
        log.configure("INFO")
        logger.error("refusing to start: %s", err)
        return 1
    log.configure(settings.log_level)
    uvicorn.run(
        create_app(settings),
        host=settings.api_host,
        port=settings.api_port,
        log_config=None,
        server_header=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
