"""Correlation ID lifecycle for CLI, API, worker, and scheduler contexts."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from uuid import UUID, uuid4

_correlation_id: ContextVar[str | None] = ContextVar("dcws_seo_correlation_id", default=None)


class InvalidCorrelationId(ValueError):
    """Raised when an inbound correlation ID is not a canonical UUID."""


def normalize_correlation_id(value: str | None = None) -> str:
    """Create a UUID4 ID or validate and canonicalize an inbound UUID."""

    if value is None:
        return str(uuid4())
    try:
        parsed = UUID(value)
    except (AttributeError, ValueError) as error:
        raise InvalidCorrelationId("correlation ID must be a canonical UUID") from error
    canonical = str(parsed)
    if value.lower() != canonical:
        raise InvalidCorrelationId("correlation ID must be a canonical UUID")
    return canonical


def get_correlation_id() -> str:
    """Return the bound ID, creating one for the current context when absent."""

    value = _correlation_id.get()
    if value is None:
        value = normalize_correlation_id()
        _correlation_id.set(value)
    return value


@contextmanager
def correlation_context(value: str | None = None) -> Iterator[str]:
    """Bind a correlation ID temporarily and restore the previous context."""

    correlation_id = normalize_correlation_id(value)
    token = _correlation_id.set(correlation_id)
    try:
        yield correlation_id
    finally:
        _correlation_id.reset(token)
