# DCWEBSTUDIO SEO Platform

Status: R1.1 repository skeleton complete; R1.2 configuration and logging
boundary is active. Versioned contracts, synthetic acceptance fixtures and the
minimal Python package layout exist, but no database, container, listener,
scheduled job or WordPress integration has been deployed.

Current source/runtime root:

`/opt/apps/dcwebstudio-seo`

Current documentation entry point:

`/opt/docs/dcwebstudio-seo/README.md`

The canonical documentation is tracked in this repository under `docs/`; the
stable `/opt/docs/dcwebstudio-seo` entry point is a symlink to that directory.
The repository is public for the current stage by owner decision. Secrets,
runtime state, provider payloads and collected page data must never be committed.

The frozen v1 boundary schemas are under `contracts/`. Their synthetic R0.3
fixtures and offline acceptance checks are under `tests/`.

The development baseline is Python 3.12 and uv 0.12.19. All direct and
transitive packages are frozen in `uv.lock`:

```bash
uv sync --frozen
uv run --frozen ruff format --check src tests
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pytest
```

The intended product is a private SEO research and controlled content pipeline
for `dcwebstudio.com`. It will collect permitted search/competitor observations,
enrich keyword candidates with provider metrics, maintain a semantic/content
map, create constrained briefs and drafts, and send approved drafts to
WordPress through a narrow adapter.

The implementation baseline is a project-owned thin Python core, one application
image and a separate PostgreSQL database. The useful MVP path starts from an
owner URL list or keyword table and does not require a paid SERP provider or AI.
Paid adapters are disabled until their provider, price source and budget are
explicitly approved.

Open-source SEO applications are reviewed source donors, not runtime services.
Only bounded, licensed components may be adapted behind project-owned contracts
with commit provenance, tests and required attribution.

The canonical repository tree is defined in
`/opt/docs/dcwebstudio-seo/PHASE-0-BASELINE.md`. Reuse and provider rules are in
`/opt/docs/dcwebstudio-seo/REUSE-AND-COST.md`. Directories should be created only
with the first reviewed implementation slice; empty scaffolding is not a
deployed system.
