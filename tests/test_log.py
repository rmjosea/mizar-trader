"""Tests for the JSON log formatter."""

import json
import logging
import sys

from mizar.log import JsonFormatter


def test_exception_is_rendered_inside_one_json_line() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord(
            "mizar.test",
            logging.ERROR,
            __file__,
            1,
            "failed %s",
            ("step",),
            sys.exc_info(),
        )

    line = JsonFormatter().format(record)
    payload = json.loads(line)

    assert "\n" not in line
    assert payload["message"] == "failed step"
    assert payload["level"] == "ERROR"
    assert "ValueError: boom" in payload["exception"]
