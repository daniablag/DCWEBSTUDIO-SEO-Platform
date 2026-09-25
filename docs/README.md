# DCWEBSTUDIO SEO Platform Documentation

This directory is the source of truth for the planned SEO research, semantic
planning and controlled content-generation platform for `dcwebstudio.com`.

## Status

Planning and source-control foundation only. Canonical documentation is tracked
in the project repository, but there is no runtime, Compose stack, database,
WordPress plugin, runtime credential set or scheduler.

## Read order

1. `HANDOFF.md` — current state and next action.
2. `MVP-SCOPE.md` — active R0.1 language, geography, device and first-output
   baseline.
3. `ARCHITECTURE.md` — component boundaries and integration direction.
4. `REUSE-AND-COST.md` — thin-core boundary, open-source intake, provider cost
   policy and zero-paid-API MVP path.
5. `DATA-MODEL.md` — durable entities, provenance and lifecycle states.
6. `WORKFLOWS.md` — collection, clustering, briefing, drafting and publishing.
7. `OPERATOR-INTERFACE.md` — natural-language/CLI entry at any workflow stage.
8. `INFRASTRUCTURE.md` — proposed Compose topology and VPS capacity envelope.
9. `SECURITY-AND-COMPLIANCE.md` — credentials, crawling, prompt injection and
   publication controls.
10. `PHASE-0-BASELINE.md` — owner decision packet, multilingual/Polylang
   contract, persistence baseline and final repository layout.
11. `DECISIONS.md` — accepted and proposed architectural decisions.
12. `ROADMAP.md` — numbered execution steps, acceptance gates and current
    active milestone.
13. `OPEN-QUESTIONS.md` — choices that still require evidence or owner input.
14. `CHANGELOG.md` — dated implementation history.

## Project boundaries

- Application/repository root: `/opt/apps/dcwebstudio-seo`
- Stable documentation route: `/opt/docs/dcwebstudio-seo`
- Canonical documentation directory: `/opt/apps/dcwebstudio-seo/docs`
- Production WordPress: `/var/www/dcwebstudio.com/public_html`
- Future WordPress adapter: project-owned plugin, reviewed under the WordPress
  workflow before it is added or activated.

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
