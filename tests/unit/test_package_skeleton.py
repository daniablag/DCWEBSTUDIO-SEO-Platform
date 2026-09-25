"""Acceptance checks for the R1.1 package and repository skeleton."""

from pathlib import Path

import dcwebstudio_seo

ROOT = Path(__file__).resolve().parents[2]


def test_package_exposes_version() -> None:
    assert dcwebstudio_seo.__version__ == "0.1.0"


def test_accepted_repository_boundaries_exist() -> None:
    expected = (
        "migrations",
        "contracts",
        "instructions/brief/v1",
        "instructions/draft/v1",
        "instructions/review/v1",
        "tests/unit",
        "tests/contract",
        "tests/integration",
        "tests/fixtures",
        "deploy/healthcheck",
        "deploy/backup",
    )

    missing = [path for path in expected if not (ROOT / path).is_dir()]
    assert not missing, f"missing repository boundaries: {missing}"


def test_accepted_python_boundaries_are_importable() -> None:
    from dcwebstudio_seo import (
        api,
        application,
        cli,
        contracts,
        domain,
        persistence,
        scheduler,
        worker,
    )
    from dcwebstudio_seo.adapters import ai, crawling, google_ads, search_console, serp, wordpress

    modules = (
        api,
        application,
        cli,
        contracts,
        domain,
        persistence,
        scheduler,
        worker,
        ai,
        crawling,
        google_ads,
        search_console,
        serp,
        wordpress,
    )
    assert all(module.__package__ for module in modules)
