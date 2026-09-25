"""Tests for structured logging, redaction, and bounded rotation."""

import json
import logging
from pathlib import Path

import pytest

from dcwebstudio_seo.application.config import AppSettings
from dcwebstudio_seo.application.correlation import correlation_context
from dcwebstudio_seo.application.logging import configure_logging, log_event


def _close_root_handlers() -> None:
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
        handler.close()


def test_json_log_contains_correlation_id_and_redacts_fields(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging(AppSettings(log_destination="stderr"))
    logger = logging.getLogger("dcwebstudio_seo.test")
    correlation_id = "4abf3aa9-54fc-4304-a25e-277957d4265a"
    secret = "provider-secret-value"

    try:
        with correlation_context(correlation_id):
            log_event(
                logger,
                logging.INFO,
                "test.redaction",
                f"request Authorization: Bearer {secret}",
                fields={
                    "provider": "synthetic",
                    "access_token": secret,
                    "nested": {"password": secret, "attempt": 1},
                    "raw_html": f"<html>{secret}</html>",
                    "url": f"https://example.test/?token={secret}&page=1",
                    "items": list(range(60)),
                },
            )
    finally:
        _close_root_handlers()

    captured = capsys.readouterr()
    assert secret not in captured.err
    payload = json.loads(captured.err)
    assert payload["correlation_id"] == correlation_id
    assert payload["event"] == "test.redaction"
    assert payload["fields"]["access_token"] == "[REDACTED]"
    assert payload["fields"]["nested"]["password"] == "[REDACTED]"
    assert payload["fields"]["raw_html"] == "[REDACTED]"
    assert "token=[REDACTED]" in payload["fields"]["url"]
    assert payload["fields"]["items"][-1] == "[TRUNCATED]"
    assert len(payload["fields"]["items"]) == 51


def test_file_handler_rotates_with_configured_bounds(tmp_path: Path) -> None:
    log_file = tmp_path / "application.jsonl"
    settings = AppSettings(
        log_destination="file",
        log_file=log_file,
        log_max_bytes=65_536,
        log_backup_count=2,
    )
    configure_logging(settings)
    logger = logging.getLogger("dcwebstudio_seo.rotation")

    try:
        for sequence in range(400):
            log_event(
                logger,
                logging.INFO,
                "test.rotation",
                "bounded rotation record",
                fields={"sequence": sequence, "padding": "x" * 120},
            )
    finally:
        _close_root_handlers()

    rotated = sorted(tmp_path.glob("application.jsonl*"))
    assert log_file in rotated
    assert tmp_path / "application.jsonl.1" in rotated
    assert len(rotated) <= settings.log_backup_count + 1


def test_invalid_event_name_is_rejected() -> None:
    logger = logging.getLogger("dcwebstudio_seo.invalid-event")

    try:
        log_event(logger, logging.INFO, "forged\nevent", "message")
    except ValueError as error:
        assert "event must match" in str(error)
    else:
        raise AssertionError("invalid event name was accepted")
