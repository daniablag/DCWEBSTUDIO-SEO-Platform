# DCWEBSTUDIO SEO Platform Documentation

This directory is the source of truth for the planned SEO research, semantic
planning and controlled content-generation platform for `dcwebstudio.com`.

## Status

Implementation-readiness contracts and source-control foundation are complete.
Canonical documentation, version 1 schemas and synthetic acceptance fixtures
are tracked in the repository, but there is no runtime, Compose stack,
database, WordPress plugin, runtime credential set or scheduler.

## Session start

Read `HANDOFF.md`, identify the active roadmap step and then open only the
matching route below. Do not preload every architecture, infrastructure,
WordPress or history document. Search `CHANGELOG.md` selectively when a dated
implementation fact is required.

| Task | Read after `HANDOFF.md` |
|---|---|
| Current execution step | `ROADMAP.md`, then only the documents named by that step |
| MVP language, country, device or output scope | `MVP-SCOPE.md` |
| Core boundaries or component design | `ARCHITECTURE.md`, relevant entries in `DECISIONS.md` |
| Contracts, persistence or provenance | `DATA-MODEL.md`, `WORKFLOWS.md` |
| CLI, Codex or Telegram operator behavior | `OPERATOR-INTERFACE.md`, relevant security sections |
| Compose, resources or deployment | `INFRASTRUCTURE.md`, `SECURITY-AND-COMPLIANCE.md` |
| Open-source reuse or provider cost | `REUSE-AND-COST.md`, `THIRD_PARTY.md` at repository root |
| WordPress, Polylang or draft delivery boundary | `WORDPRESS-INTEGRATION.md`, then only the affected site workflow/contract |
| Unresolved owner decision | `OPEN-QUESTIONS.md`, relevant decision record |
| Historical evidence | targeted search in `CHANGELOG.md`; do not read it end to end |

## Project boundaries

- Application/repository root: `/opt/apps/dcwebstudio-seo`
- Stable documentation route: `/opt/docs/dcwebstudio-seo`
- Canonical documentation directory: `/opt/apps/dcwebstudio-seo/docs`
- Production WordPress: `/var/www/dcwebstudio.com/public_html`
- Future WordPress adapter: project-owned plugin, reviewed under the WordPress
  workflow before it is added or activated.

Normal SEO research and platform implementation do not require the WordPress
handoff. Normal WordPress work does not require this package. Read both scopes
only for an explicit integration task described in `WORDPRESS-INTEGRATION.md`.

This is a separate project on a shared VPS. It must not reuse the Poehali
database, network, Redis, Codex profile or source tree. WordPress remains the
publication target, not the SEO platform's primary database.

## External references

- Google Ads keyword ideas:
  https://developers.google.com/google-ads/api/docs/keyword-planning/generate-keyword-ideas
- Google Ads keyword-planning limits and caching guidance:
  https://developers.google.com/google-ads/api/docs/keyword-planning/overview
- Search Console API:
  https://developers.google.com/webmaster-tools
- Robots Exclusion Protocol:
  https://www.rfc-editor.org/rfc/rfc9309.html
- Current Codex SDK guidance:
  https://learn.chatgpt.com/docs/codex-sdk
