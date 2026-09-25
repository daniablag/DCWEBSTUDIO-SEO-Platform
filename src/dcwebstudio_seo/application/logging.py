"""Structured JSON logging with bounded fields and fail-closed redaction."""

from __future__ import annotations

import json
import logging
import math
import re
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Final
from uuid import UUID

from dcwebstudio_seo.application.config import (
    AppSettings,
    LogDestination,
    validate_startup,
)
from dcwebstudio_seo.application.correlation import get_correlation_id

REDACTED: Final = "[REDACTED]"
TRUNCATED: Final = "[TRUNCATED]"
MAX_STRING_LENGTH: Final = 4_096
MAX_COLLECTION_ITEMS: Final = 50
MAX_NESTING_DEPTH: Final = 5
_EVENT_PATTERN = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
_SENSITIVE_KEY_PARTS = frozenset(
    {
        "access_token",
        "api_key",
        "apikey",
        "authorization",
        "client_secret",
        "cookie",
        "credential",
        "oauth",
        "password",
        "private_key",
        "provider_payload",
        "raw_html",
        "refresh_token",
        "secret",
        "source_excerpt",
    }
)
_BEARER_PATTERN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*")
_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(password|secret|token|api[_-]?key|authorization)\s*([=:])\s*([^\s,;&]+)"
)
_URL_USERINFO_PATTERN = re.compile(r"(?<=://)[^/@\s:]+:[^/@\s]+@")
_PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?"
    r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    re.DOTALL,
)


def _is_sensitive_key(key: object) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")
    return any(part in normalized for part in _SENSITIVE_KEY_PARTS)


def redact_text(value: str) -> str:
    """Redact common credential forms and bound retained text length."""

    value = _PRIVATE_KEY_PATTERN.sub(REDACTED, value)
    value = _BEARER_PATTERN.sub(f"Bearer {REDACTED}", value)
    value = _URL_USERINFO_PATTERN.sub(f"{REDACTED}@", value)
    value = _ASSIGNMENT_PATTERN.sub(
        lambda match: f"{match.group(1)}{match.group(2)}{REDACTED}", value
    )
    if len(value) > MAX_STRING_LENGTH:
        return f"{value[:MAX_STRING_LENGTH]}{TRUNCATED}"
    return value


def sanitize_log_value(value: object, *, depth: int = 0) -> object:
    """Convert a value to bounded JSON-safe data while redacting sensitive keys."""

    if depth >= MAX_NESTING_DEPTH:
        return TRUNCATED
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, (Path, UUID, date, datetime)):
        return redact_text(str(value))
    if isinstance(value, Mapping):
        sanitized: dict[str, object] = {}
        for index, (key, item) in enumerate(value.items()):
            if index >= MAX_COLLECTION_ITEMS:
                sanitized[TRUNCATED] = TRUNCATED
                break
            key_text = redact_text(str(key))
            sanitized[key_text] = (
                REDACTED if _is_sensitive_key(key) else sanitize_log_value(item, depth=depth + 1)
            )
        return sanitized
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        sanitized_items = [
            sanitize_log_value(item, depth=depth + 1) for item in value[:MAX_COLLECTION_ITEMS]
        ]
        if len(value) > MAX_COLLECTION_ITEMS:
            sanitized_items.append(TRUNCATED)
        return sanitized_items
    return redact_text(str(value))


class RedactingJsonFormatter(logging.Formatter):
    """Emit one bounded JSON object per log record."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=UTC).isoformat(
            timespec="milliseconds"
        )
        payload: dict[str, object] = {
            "timestamp": timestamp.replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": redact_text(record.name),
            "event": redact_text(str(getattr(record, "event_name", "log.message"))),
            "message": redact_text(record.getMessage()),
            "correlation_id": get_correlation_id(),
        }
        fields = getattr(record, "structured_fields", None)
        if fields:
            payload["fields"] = sanitize_log_value(fields)
        if record.exc_info:
            payload["exception"] = redact_text(self.formatException(record.exc_info))
        return json.dumps(
            payload,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )


def configure_logging(settings: AppSettings) -> logging.Handler:
    """Configure the root logger and return its sole owned handler."""

    validate_startup(settings)
    formatter = RedactingJsonFormatter()
    if settings.log_destination is LogDestination.FILE:
        assert settings.log_file is not None
        handler: logging.Handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count,
            encoding="utf-8",
            delay=True,
        )
    else:
        stream = sys.stderr if settings.log_destination is LogDestination.STDERR else sys.stdout
        handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    for existing in root.handlers[:]:
        root.removeHandler(existing)
        existing.close()
    root.addHandler(handler)
    root.setLevel(settings.log_level.value)
    logging.captureWarnings(True)
    return handler


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    message: str,
    *,
    fields: Mapping[str, object] | None = None,
) -> None:
    """Write a named structured event without allowing LogRecord key collisions."""

    if not _EVENT_PATTERN.fullmatch(event):
        raise ValueError("event must match ^[a-z][a-z0-9_.-]{0,63}$")
    logger.log(
        level,
        message,
        extra={
            "event_name": event,
            "structured_fields": dict(fields or {}),
        },
    )
