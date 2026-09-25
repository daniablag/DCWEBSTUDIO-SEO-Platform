"""Tests for typed settings and startup validation."""

import os
from pathlib import Path

import pytest

from dcwebstudio_seo.application.config import (
    AppSettings,
    ConfigurationError,
    LogDestination,
    LogLevel,
    RuntimeEnvironment,
    load_settings,
    validate_environment_keys,
    validate_startup,
)

PREFIX = "DCWS_SEO_"
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def clear_project_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in tuple(os.environ):
        if name.startswith(PREFIX):
            monkeypatch.delenv(name, raising=False)


def test_default_settings_are_non_secret_and_stream_to_stderr() -> None:
    settings = load_settings(env_file=None)

    assert settings.environment is RuntimeEnvironment.DEVELOPMENT
    assert settings.log_level is LogLevel.INFO
    assert settings.log_destination is LogDestination.STDERR
    assert settings.log_file is None
    assert set(AppSettings.model_fields) == {
        "environment",
        "log_level",
        "log_destination",
        "log_file",
        "log_max_bytes",
        "log_backup_count",
    }


def test_tracked_env_example_is_valid_and_contains_no_secret_setting() -> None:
    settings = load_settings(env_file=ROOT / ".env.example")

    assert settings == AppSettings()
    assert not any(
        fragment in name
        for name in AppSettings.model_fields
        for fragment in ("password", "secret", "token", "credential")
    )


def test_environment_values_are_typed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DCWS_SEO_ENVIRONMENT", "test")
    monkeypatch.setenv("DCWS_SEO_LOG_LEVEL", "WARNING")
    monkeypatch.setenv("DCWS_SEO_LOG_MAX_BYTES", "65536")
    monkeypatch.setenv("DCWS_SEO_LOG_BACKUP_COUNT", "2")

    settings = load_settings(env_file=None)

    assert settings.environment is RuntimeEnvironment.TEST
    assert settings.log_level is LogLevel.WARNING
    assert settings.log_max_bytes == 65_536
    assert settings.log_backup_count == 2


def test_unknown_project_setting_fails_without_exposing_value() -> None:
    secret_value = "must-not-appear"

    with pytest.raises(ConfigurationError) as captured:
        validate_environment_keys({"DCWS_SEO_UNKNOWN_TOKEN": secret_value})

    assert "DCWS_SEO_UNKNOWN_TOKEN" in str(captured.value)
    assert secret_value not in str(captured.value)


def test_validation_error_does_not_expose_invalid_value(monkeypatch: pytest.MonkeyPatch) -> None:
    invalid_value = "secret-shaped-invalid-value"
    monkeypatch.setenv("DCWS_SEO_LOG_MAX_BYTES", invalid_value)

    with pytest.raises(ConfigurationError) as captured:
        load_settings(env_file=None)

    assert invalid_value not in str(captured.value)
    assert "log_max_bytes" in str(captured.value)


def test_dotenv_error_does_not_expose_unknown_value(tmp_path: Path) -> None:
    invalid_value = "dotenv-secret-shaped-value"
    env_file = tmp_path / ".env"
    env_file.write_text(f"DCWS_SEO_UNKNOWN_TOKEN={invalid_value}\n", encoding="utf-8")

    with pytest.raises(ConfigurationError) as captured:
        load_settings(env_file=env_file)

    assert invalid_value not in str(captured.value)
    assert "dcws_seo_unknown_token" in str(captured.value).lower()


def test_production_debug_is_rejected() -> None:
    with pytest.raises(ValueError, match="DEBUG logging is not allowed"):
        AppSettings(environment="production", log_level="DEBUG")


def test_file_logging_requires_an_existing_absolute_parent(tmp_path: Path) -> None:
    relative = AppSettings(log_destination="file", log_file=Path("application.jsonl"))
    with pytest.raises(ConfigurationError, match="absolute"):
        validate_startup(relative)

    missing_parent = AppSettings(
        log_destination="file",
        log_file=tmp_path / "missing" / "application.jsonl",
    )
    with pytest.raises(ConfigurationError, match="does not exist"):
        validate_startup(missing_parent)


def test_startup_report_assigns_rotation_owner(tmp_path: Path) -> None:
    file_settings = AppSettings(
        log_destination="file",
        log_file=tmp_path / "application.jsonl",
        log_max_bytes=65_536,
        log_backup_count=2,
    )

    file_report = validate_startup(file_settings)
    stream_report = validate_startup(AppSettings())

    assert file_report.rotation_owner == "application"
    assert file_report.log_max_bytes == 65_536
    assert file_report.log_backup_count == 2
    assert stream_report.rotation_owner == "runtime"
