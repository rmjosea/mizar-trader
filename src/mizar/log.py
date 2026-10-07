"""Structured JSON logging on standard error."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import override


class JsonFormatter(logging.Formatter):
    """Render each log record as one JSON object on a single line."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        """Return the record as JSON with time, level, logger and message."""
        payload = {
            "time": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure(level: str) -> None:
    """Send every log record, including the server's, to stderr as JSON.

    Args:
        level: Minimum level name, for example ``INFO``.
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
