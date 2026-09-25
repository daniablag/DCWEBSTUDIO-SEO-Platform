"""Tests for correlation context isolation and validation."""

from uuid import UUID

import pytest

from dcwebstudio_seo.application.correlation import (
    InvalidCorrelationId,
    correlation_context,
    get_correlation_id,
    normalize_correlation_id,
)


def test_generated_correlation_id_is_a_uuid() -> None:
    value = normalize_correlation_id()

    assert str(UUID(value)) == value


def test_context_restores_previous_correlation_id() -> None:
    outer = get_correlation_id()
    requested = "d5e349bb-08da-45af-9941-f846ad47b0c7"

    with correlation_context(requested) as current:
        assert current == requested
        assert get_correlation_id() == requested

    assert get_correlation_id() == outer


@pytest.mark.parametrize(
    "value",
    [
        "not-a-uuid",
        "d5e349bb-08da-45af-9941-f846ad47b0c7\nforged",
        "{d5e349bb-08da-45af-9941-f846ad47b0c7}",
    ],
)
def test_noncanonical_correlation_id_is_rejected(value: str) -> None:
    with pytest.raises(InvalidCorrelationId):
        normalize_correlation_id(value)
