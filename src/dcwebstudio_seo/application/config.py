"""Typed, fail-closed application configuration."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PREFIX = "DCWS_SEO_"
DEFAULT_ENV_FILE = Path(".env")


class RuntimeEnvironment(StrEnum):
    """Supported runtime modes."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Allowed application log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogDestination(StrEnum):
    """Supported structured-log sinks."""

    STDERR = "stderr"
    STDOUT = "stdout"
    FILE = "file"


class ConfigurationError(ValueError):
    """A sanitized configuration or startup validation failure."""


class AppSettings(BaseSettings):
    """Non-secret application settings loaded from environment or `.env`."""

    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
        validate_default=True,
    )

    environment: RuntimeEnvironment = RuntimeEnvironment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    log_destination: LogDestination = LogDestination.STDERR
    log_file: Path | None = None
    log_max_bytes: int = Field(default=10_485_760, ge=65_536, le=104_857_600)
    log_backup_count: int = Field(default=5, ge=1, le=10)

    @model_validator(mode="after")
    def validate_logging_combination(self) -> Self:
        """Reject ambiguous or unsafe logging combinations."""

        if self.log_destination is LogDestination.FILE and self.log_file is None:
            raise ValueError("log_file is required when log_destination=file")
        if self.log_destination is not LogDestination.FILE and self.log_file is not None:
            raise ValueError("log_file is allowed only when log_destination=file")
        if self.environment is RuntimeEnvironment.PRODUCTION and self.log_level is LogLevel.DEBUG:
            raise ValueError("DEBUG logging is not allowed in production")
        return self


@dataclass(frozen=True, slots=True)
class StartupValidation:
    """Sanitized startup validation result safe to expose in status output."""

    environment: RuntimeEnvironment
    log_destination: LogDestination
    rotation_owner: str
    log_max_bytes: int
    log_backup_count: int


def allowed_environment_names() -> frozenset[str]:
    """Return the complete set of accepted project-prefixed environment names."""

    return frozenset(f"{ENV_PREFIX}{name.upper()}" for name in AppSettings.model_fields)


def validate_environment_keys(environ: Mapping[str, str]) -> None:
    """Fail on unknown project-prefixed variables without exposing their values."""

    allowed = allowed_environment_names()
    unknown = sorted(
        name
        for name in environ
        if name.upper().startswith(ENV_PREFIX) and name.upper() not in allowed
    )
    if unknown:
        raise ConfigurationError(f"unknown {ENV_PREFIX}settings: {', '.join(unknown)}")


def _sanitized_validation_detail(error: ValidationError) -> str:
    issues: list[str] = []
    for issue in error.errors(include_url=False, include_input=False):
        location = ".".join(str(part) for part in issue["loc"]) or "settings"
        issues.append(f"{location}:{issue['type']}")
    return ", ".join(issues)


def load_settings(*, env_file: str | Path | None = DEFAULT_ENV_FILE) -> AppSettings:
    """Load settings and return sanitized errors suitable for startup output."""

    validate_environment_keys(os.environ)
    try:
        # `_env_file` is a documented BaseSettings runtime keyword omitted from
        # the generated subclass signature seen by mypy.
        return AppSettings(_env_file=env_file)  # type: ignore[call-arg]
    except ValidationError as error:
        detail = _sanitized_validation_detail(error)
        raise ConfigurationError(f"invalid application settings ({detail})") from None


def validate_startup(settings: AppSettings) -> StartupValidation:
    """Validate environment-dependent preconditions without creating resources."""

    rotation_owner = "runtime"
    if settings.log_destination is LogDestination.FILE:
        assert settings.log_file is not None
        log_file = settings.log_file
        if not log_file.is_absolute():
            raise ConfigurationError("log_file must be an absolute path")
        parent = log_file.parent
        if not parent.exists():
            raise ConfigurationError("log_file parent directory does not exist")
        if not parent.is_dir():
            raise ConfigurationError("log_file parent path is not a directory")
        if not os.access(parent, os.W_OK):
            raise ConfigurationError("log_file parent directory is not writable")
        rotation_owner = "application"

    return StartupValidation(
        environment=settings.environment,
        log_destination=settings.log_destination,
        rotation_owner=rotation_owner,
        log_max_bytes=settings.log_max_bytes,
        log_backup_count=settings.log_backup_count,
    )
