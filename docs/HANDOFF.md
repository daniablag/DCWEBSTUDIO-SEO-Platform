# DCWEBSTUDIO SEO Platform Handoff

Snapshot: 2026-09-25 13:09 Europe/Berlin

## Current state

The project is in architecture and planning. `/opt/apps/dcwebstudio-seo` and
this documentation package exist. No code, database, container, service,
public route, credentials, scheduled jobs or WordPress plugin exist yet.

The production site currently has WordPress-native titles, canonical links,
virtual robots.txt and a working core sitemap. It does not have managed meta
descriptions, Open Graph, project-owned JSON-LD or a stable SEO automation
contract. Those site changes remain a later WordPress-scoped release.

Polylang Pro 3.7.8 is installed on production but inactive and unconfigured.
There are no Polylang language terms or post-language relationships; all seven
published pages are currently unassigned. No activation or production change
was made during the SEO planning work.

This state was rechecked on 2026-09-24: the active theme is still
`dcwebstudio` 0.1.79, WordPress locale is `ru_RU`, the permalink structure is
`/%postname%/`, and Polylang still reports no `language` taxonomy. The theme
currently registers 33 ACF groups and 318 fields including layout fields; none
has an explicit Polylang `translations` setting. This must be corrected in a
separately reviewed WordPress release before translations are created.

The application root still contains only `AGENTS.md` and `README.md`. It is not
a Git repository and no runtime resources exist. The current SEO documents
match the expected multilingual update relative to recovery set
`seo-multilingual-context-20260924-212309`; no unexplained parallel edit or
conflict was found during this review.

`ROADMAP.md` is the step-by-step execution source of truth. R0.1 is complete;
the current step is blocked R0.2 (establish private source control). All
implementation steps remain planned and unstarted.

The owner confirmed Ukraine as the first geography and Russian/Ukrainian as the
first content languages. `MVP-SCOPE.md` records the resulting `ru-UA` and
`uk-UA` research targets and explains that desktop/mobile are measurement
segments, not additional pages or business geographies. Google, the combined
desktop/mobile recommendation, project-owner approval role and seven-day
diagnostic raw-payload maximum are confirmed. R0.1 is complete.

The owner also requires structured logs, Telegram delivery of actionable final
errors and a later Telegram command bridge. D-018 defines a durable PostgreSQL
notification outbox and a thin project-owned Telegram adapter over the same
CLI/API service layer. It must remain separate from the existing WordPress
Telegram bridge and must not expose shell, SQL, secrets or publication.

## Agreed direction

- Build a private SEO data platform, not a collection of ad-hoc scripts.
- Use a separate Docker Compose project and separate PostgreSQL database.
- Keep data collection and normalization deterministic.
- Use a provider adapter for SERP acquisition; do not build production around
  scraping Google Search result HTML.
- Fetch competitor pages politely, respect robots.txt and retain provenance.
- Treat competitor title/description/page structure as observations, never as
  copy to reproduce.
- Use Google Ads Keyword Planning for ideas and historical metrics, and Search
  Console for the site's own performance data.
- Store raw observations, normalized keywords, metrics snapshots, clusters,
  content targets, briefs, drafts, instruction versions and audit events as
  distinct records.
- Model execution as a composable directed graph of stages. The owner or an
  authorized agent may start from any stage with a validated external artifact
  and may request an explicit stop boundary.
- Owner-supplied URLs, keyword tables, clusters, briefs and drafts are
  first-class inputs with provenance. They skip unnecessary upstream stages;
  the system records skipped stages instead of silently recreating their data.
- A Codex operator reads the project instructions, converts natural language
  into a dry-run stage plan, validates preconditions and invokes only reviewed
  CLI/API commands. It never edits the database directly.
- Map every keyword cluster either to an existing URL or to one proposed content
  target before generating text.
- Use versioned, bounded instructions for AI work. Collection, permissions and
  state transitions remain application code.
- Create WordPress drafts only in the first release. Human approval remains
  mandatory before publication.
- Establish the WordPress multilingual contract before the SEO adapter and
  automated content delivery. Polylang Pro is the planned translation-relation
  layer, but activation is a separate backed-up WordPress release after the
  owner confirms the remaining URL, redirect, media, menu/form and locale-map
  policy. Russian/Ukrainian research for Ukraine is already fixed.
- Model content language and search market separately. A translation is a
  distinct SEO target with its own queries, metadata, brief and performance
  observations, even when Polylang links it to the same conceptual page.
- For Ukraine, research Russian and Ukrainian queries independently. Link the
  two locale-specific service pages through Polylang, but never obtain one
  language's SEO plan by mechanically translating the other language's
  keywords. Device data may remain segmented while the page recommendation is
  unified per language.
- Use the current Codex SDK for programmatic local sessions if Codex is selected
  for a worker. Do not base new work on the removed `codex mcp-server` command.
- Use one private monorepo for application code, CLI, Compose, migrations,
  contracts, tests, versioned AI instructions and canonical project docs.
  Runtime data, secrets, provider payloads, logs, dumps and competitor
  collections remain outside Git.
- Treat the platform `content_unit` as the stable language-neutral identity and
  each locale-specific `content_target` as an independent SEO object. WordPress
  IDs and the Polylang locale-to-post map are adapter observations, not primary
  identities and not inferred from slugs.
- Keep a project-owned thin core for contracts, provenance, planning, durable
  jobs, approvals and the WordPress boundary. Adapt only bounded, reviewed
  open-source components; do not adopt an upstream SEO application or depend on
  it as a hosted runtime service.
- Require a useful zero-paid-API path from owner URL lists and keyword tables.
  Paid SERP and AI providers remain disabled until a versioned price source,
  explicit budget and approval are present.
- Keep the MVP to one Python package/image and PostgreSQL as its only stateful
  service. Do not add Redis, a public UI, permanent browser pool, local model,
  vector store or search cluster without measured need.

## Phase 0 design baseline

`PHASE-0-BASELINE.md` now records:

- the bounded owner decisions required before Polylang or implementation;
- the recommended no-prefix/default-language URL contract;
- the field-by-field ACF classification rules and exceptions;
- a backed-up, canary-first Polylang release sequence and rollback boundary;
- the concrete locale/market/content/WordPress persistence model;
- the final monorepo tree and a staged move of canonical docs into Git while
  keeping `/opt/docs/dcwebstudio-seo` as the stable routed entry point.

These are design recommendations, not authorization to activate Polylang,
initialize Git, create containers, install packages or modify WordPress.

## Reuse and cost baseline

`REUSE-AND-COST.md` records the reviewed donor matrix and the accepted boundary:
CrawlSEO is the preferred source for bounded crawler/GSC/PageSpeed behavior,
OpenGSC is a selective security and provider-control donor, and SEOctopus is a
CLI/report reference rather than a core. StackSEO code is excluded because no
usable license was found at review.

The required MVP works without paid APIs or AI. Search Console and PageSpeed
are optional quota-limited enrichment; DataForSEO and AI are opt-in paid
adapters. A paid or unknown-cost stage cannot enqueue without a current price
source, upper-bound estimate and remaining per-job/daily/monthly budget.

## Initial VPS finding

The host has 2 vCPU, 3.8 GiB RAM, 2.0 GiB swap and 44 GiB free disk. At the
planning snapshot about 2.1 GiB RAM was available. Existing Docker containers
used roughly 90 MiB in total but have combined limits of 1 GiB. CPU had no full
pressure, while normal contention and small I/O pressure were visible.

A constrained MVP should fit if it uses one small PostgreSQL container, one API
process, one worker with concurrency 1 and a tiny scheduler, with no local LLM,
Elasticsearch/OpenSearch, Redis or permanent browser pool. This is a planning
estimate, not deployment approval. `INFRASTRUCTURE.md` records the envelope and
upgrade triggers.

## Next action

Follow `ROADMAP.md` one gate at a time. Do not begin R1 while R0 is incomplete.

1. Complete current step R0.2 only after the owner supplies the empty private
   Git remote and authentication method; then perform the documented docs
   migration. R0.2 is blocked until then.
2. Complete R0.3 by freezing version 1 contracts and synthetic acceptance
   fixtures, including notification-event and Telegram-command envelopes.
3. Begin R1 only after the R0 exit gate passes.

The separate WP0 track may be scheduled independently, but it is required only
before R7 WordPress delivery. Do not activate Polylang or change WordPress as a
side effect of R0–R6 platform work.

Recovery sets:

- project registration/shared routing:
  `/opt/docs/config-backups-user/seo-platform-foundation-20260924-194500`;
- latest composable-workflow documentation update:
  `/opt/docs/config-backups-user/seo-manual-entrypoints-20260924-195734`.
- multilingual/Polylang planning update:
  `/opt/docs/config-backups-user/seo-multilingual-context-20260924-212309`.
- Phase 0 design baseline:
  `/opt/docs/config-backups-user/seo-phase0-design-20260924-231121`.
- thin-core/reuse/provider-cost baseline:
  `/opt/docs/config-backups-user/seo-reuse-cost-baseline-20260924-233615`.
- execution roadmap baseline:
  `/opt/docs/config-backups-user/seo-execution-roadmap-20260925-121100`.
- Ukraine bilingual R0.1 scope:
  `/opt/docs/config-backups-user/seo-ukraine-bilingual-scope-20260925-125551`.
- R0.1 Google/device confirmation:
  `/opt/docs/config-backups-user/seo-r01-google-device-20260925-130420`.
- R0.1 completion and Telegram observability baseline:
  `/opt/docs/config-backups-user/seo-telegram-observability-20260925-130952`.
