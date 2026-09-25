# DCWEBSTUDIO SEO Platform Changelog

## 2026-09-25 — R1.2 configuration and logging boundary

- Added a strict Pydantic Settings 2.15.0 model for non-secret `DCWS_SEO_`
  configuration and a tracked `.env.example` containing only safe defaults.
- Added fail-closed startup validation for unknown/invalid settings, production
  `DEBUG`, log destination/path conflicts and file-log directory requirements;
  error summaries omit rejected values.
- Added canonical UUID correlation contexts and bounded JSONL logging with
  stable event names, recursive structured-field sanitization and free-text
  redaction for common credential forms.
- Added tested file size/count rotation and documented that the future runtime
  owns rotation for the default `stderr`/`stdout` sink.
- Passed lock validation, format/lint, strict source type checking, 31 tests
  plus 14 subtests and the fresh-checkout package build. No credential,
  database, container, listener, provider call or WordPress change was made.
- Completed R1.2 and advanced the active roadmap step to R1.3 only after the
  acceptance checks passed.

Recovery set:

`/opt/docs/config-backups-user/seo-r12-config-logging-20260925-210217`

## 2026-09-25 — R1.1 repository skeleton

- Added the accepted importable `src/dcwebstudio_seo/` package boundaries plus
  migration, versioned instruction, integration-test, health-check and backup
  placeholders without creating runtime behavior or a service.
- Added Python 3.12 package metadata, enforced uv 0.12.19, generated a fully
  resolved `uv.lock`, and pinned Hatchling 1.32.4, jsonschema 4.26.0, pytest
  9.1.1, Ruff 0.16.9 and mypy 2.3.1.
- Added conservative proprietary `LICENSE` and `NOTICE` files. No third-party
  source was copied or adapted, so the `THIRD_PARTY.md` register remains empty.
- Replaced deprecated `jsonschema.RefResolver` usage in the contract acceptance
  test with `referencing.Registry`; all schemas and fixture content remain
  unchanged.
- Passed frozen-lock validation, formatting, lint, strict source type checking,
  14 tests plus 14 subtests, wheel build/content inspection and Git exclusion
  checks. No database, container, listener, credential, provider request or
  WordPress change was created.
- Completed R1.1 and advanced the active roadmap step to R1.2 only after its
  acceptance checks passed.

Recovery set:

`/opt/docs/config-backups-user/seo-r11-skeleton-20260925-204942`

## 2026-09-25 — R0.3 versioned contracts and acceptance fixtures

- Added 16 strict JSON Schema Draft 2020-12 contracts for identity, imports,
  artifacts, observations, normalized keywords, stage planning/results,
  provider cost/SERP evidence, notifications and Telegram operator envelopes.
- Added checksum-pinned synthetic `.test` fixtures for manual URL input,
  separate `ru-UA`/`uk-UA` keyword tables, deterministic normalized outputs and
  an offline SERP response; no live provider or production payload is present.
- Added 11 offline contract tests covering schema/reference validity, hashes,
  CSV boundaries, locale/device identity, skipped stages, seven-day diagnostic
  retention behavior, fail-closed unknown cost and Telegram sanitization.
- Recorded D-019, passed the R0 exit gate and advanced the active roadmap step
  to R1.1. No application runtime, package, database, container, provider
  request or WordPress change was created.

Recovery set:

`/opt/docs/config-backups-user/seo-r03-contracts-20260925-192649`

## 2026-09-25 — Isolated SEO access through the owner Codex bridge

- Added an explicit SEO profile to the existing private owner-to-Codex Telegram
  bridge with workspace `/opt/apps/dcwebstudio-seo`, the project-only bootstrap
  route and its own persistent thread slot.
- Preserved the former bridge thread as the independent `site` session; no SEO
  thread exists until the owner explicitly selects and starts it.
- Clarified that this development-session router is not the future D-018 SEO
  runtime notifier/command adapter. The application adapter still requires
  separate secrets, service, state, permissions and durable outbox behavior.
- No SEO runtime code, database, container, provider request or WordPress
  product behavior changed.

Recovery set:

`/opt/docs/config-backups-user/project-routing-telegram-20260925-141532`

## 2026-09-25 — Project-scoped documentation routing

- Removed shared-server and WordPress documentation from the normal mandatory
  SEO-platform read path.
- Converted the project README into a task router so a session loads only the
  current handoff and documents relevant to its requested work.
- Added `WORDPRESS-INTEGRATION.md` as the single explicit cross-project entry
  point with ownership, persistence and publication boundaries.
- Updated the WordPress instructions and site documentation router with the
  reciprocal isolation rule.
- No application code, container, database, provider request, WordPress
  runtime, content or frontend behavior changed.

Recovery set:

`/opt/docs/config-backups-user/project-routing-telegram-20260925-141532`

## 2026-09-25 — R0.2 repository and canonical documentation migration

- Initialized the monorepo at `/opt/apps/dcwebstudio-seo` and connected the
  owner-approved public GitHub repository
  `daniablag/DCWEBSTUDIO-SEO-Platform` through a dedicated deploy key.
- Added deny-by-default `.gitignore` rules for secrets, credentials, databases,
  runtime state, logs, provider payloads, raw HTML and collected competitor
  data; a credential-shape scan passed before staging.
- Added `THIRD_PARTY.md`; no third-party source code has been imported.
- Pushed documentation-only initial commit `f744630` and verified the remote.
- Compared per-file checksums, found no parallel documentation change, moved
  the former docs directory intact into the recovery set and routed
  `/opt/docs/dcwebstudio-seo` to repository `docs/` by symlink.
- Recorded public visibility as the owner's current-stage choice; secret and
  operational-data exclusions remain mandatory regardless of visibility.
- Completed R0.2 and advanced the roadmap to active R0.3. No application code,
  database, container, package, provider request or WordPress change was made.

Recovery set:

`/opt/docs/config-backups-user/seo-repository-migration-20260925-133957`

## 2026-09-25 — R0.1 completion and Telegram operations baseline

- Completed R0.1 after the owner confirmed the initial approval role and a
  seven-day maximum for bounded diagnostic raw HTML; successful crawls retain
  normalized observations and hashes rather than raw HTML.
- Moved the current roadmap step to blocked R0.2, pending the empty private Git
  remote and authentication method.
- Required structured redacted logs with correlation IDs plus a durable
  PostgreSQL notification outbox as the authoritative error path.
- Added a later Telegram notifier for deduplicated actionable final errors and
  a project-owned command bridge over the same reviewed CLI/API service layer.
- Defined read-only-first commands and expiring `plan -> confirm` authorization
  for later mutations; prohibited shell, SQL, secret access and publication.
- Kept the SEO bridge separate from the existing WordPress Telegram bridge's
  service, secrets, database, Codex state and lifecycle.
- No bot, token, service, public listener, repository, code, database,
  container, package or WordPress change was created.

Recovery set:

`/opt/docs/config-backups-user/seo-telegram-observability-20260925-130952`

## 2026-09-25 — Ukraine bilingual MVP scope

- Recorded Ukraine as the first search geography and Russian/Ukrainian as the
  first content languages, with initial research identities `ru-UA` and
  `uk-UA`.
- Defined one language-neutral content unit with separate Russian and Ukrainian
  content targets linked later through an observed Polylang translation set.
- Required independent real-query research, clusters, metadata, briefs and
  measurements per language instead of mechanical keyword translation.
- Clarified that desktop/mobile are observation segments, not page variants or
  additional business geographies; each language receives one combined page
  recommendation unless evidence shows a material device difference.
- Recorded the owner's confirmation of Google as the first engine and of the
  combined page recommendation with preserved desktop/mobile evidence.
- Added `MVP-SCOPE.md`, marked R0.1 partially resolved and reduced its remaining
  confirmations to the initial approver and diagnostic raw-payload retention.
- No Polylang activation, page copy, WordPress change, provider request,
  repository, code, database, package or container was created.

Recovery set:

`/opt/docs/config-backups-user/seo-ukraine-bilingual-scope-20260925-125551`

## 2026-09-25 — Gated execution roadmap

- Replaced the broad phase list with numbered R0–R8 execution milestones and a
  separate WP0 WordPress-readiness track.
- Made R0.1 (freeze the first research scope) the only active step; no
  implementation or production step has started.
- Added per-step deliverables, ordered work and acceptance gates for repository
  setup, durable workflow kernel, safe crawl, keyword intelligence, optional
  providers, governed content, WordPress draft delivery and operations.
- Defined the research MVP at R4, content MVP at R6 and delivery MVP at R7.
- Kept the R1–R4 path independent of paid APIs/AI and kept WordPress/Polylang
  work from blocking the research platform through R6.
- Preserved deferred heavy services and required measured evidence plus a new
  architecture decision before adding them.
- No repository, source code, package, database, container, credential,
  provider request or WordPress change was created.

Recovery set:

`/opt/docs/config-backups-user/seo-execution-roadmap-20260925-121100`

## 2026-09-24 — Thin-core, reuse and provider-cost baseline

- Accepted a project-owned thin core for contracts, provenance, run planning,
  durable jobs, approvals, multilingual identities and WordPress projection.
- Recorded the reviewed open-source donor matrix: bounded CrawlSEO/OpenGSC
  reuse, SEOctopus/SEO Command Center as references and no StackSEO code reuse
  without a usable license.
- Added a source-intake contract requiring immutable commit provenance,
  smallest-component imports, adapter isolation, tests and license notices.
- Required an MVP path that works from owner URL lists and keyword tables with
  no paid SERP provider and no AI runtime.
- Classified paid providers as disabled by default and required price-version,
  per-job, daily and monthly caps before enqueueing any paid request.
- Reaffirmed the single Python package/image, PostgreSQL-only stateful MVP and
  exclusions for Redis, public UI, permanent browser pools, local models,
  search clusters and vector storage until measurements justify them.
- Aligned the application-root README with the canonical monorepo layout and
  removed its obsolete preliminary directory list.
- No source import, repository initialization, provider signup, credential,
  package, container, runtime or WordPress change was performed.

Recovery set:

`/opt/docs/config-backups-user/seo-reuse-cost-baseline-20260924-233615`

## 2026-09-24 — Phase 0 multilingual and repository baseline

- Reverified production without mutation: theme 0.1.79 active, Polylang Pro
  3.7.8 inactive, WordPress locale `ru_RU`, seven published pages and no
  Polylang language taxonomy.
- Confirmed the application and docs are not Git repositories and found no
  unexplained parallel documentation changes.
- Added a bounded owner decision packet, recommended default-language URL
  contract and backed-up canary-first Polylang migration sequence.
- Inventoried 33 ACF groups and 318 fields and defined deterministic Translate,
  Copy Once and Synchronize rules plus URL, company-options and CF7 exceptions.
- Expanded the persistence design for locale, market, content unit, locale
  target, WordPress object and adapter-observed translation sets.
- Fixed the recommended one-private-monorepo tree and a staged plan to move
  canonical docs into Git while keeping `/opt/docs/dcwebstudio-seo` as the
  routed entry point.
- No plugin activation, theme/content change, repository initialization,
  container, package installation or public-routing change was performed.

Recovery set:

`/opt/docs/config-backups-user/seo-phase0-design-20260924-231121`

## 2026-09-24 — Multilingual prerequisite and source-control handoff

- Recorded that Polylang Pro 3.7.8 is installed but inactive and unconfigured;
  no production activation was performed.
- Made the multilingual WordPress contract a prerequisite for the SEO adapter
  and automated content delivery.
- Separated locale/language from country or regional search market in the
  architecture and added locale-specific content targets linked by a conceptual
  content unit and Polylang translation relationship.
- Added the URL-policy, ACF translation behavior and controlled Polylang
  migration decisions to phase 0 and the handoff.
- Added the Git repository/remote layout as a decision required before the
  first application code is created.

Recovery set:

`/opt/docs/config-backups-user/seo-multilingual-context-20260924-212309`

## 2026-09-24 — Composable stages and manual entry points

- Replaced the implied mandatory linear pipeline with a directed graph of
  independently invocable stages.
- Made owner-supplied URL lists, keyword tables, clusters, briefs and drafts
  first-class versioned artifacts with validation and provenance.
- Added a run-planning contract that records start/stop boundaries, executed
  stages, skipped upstream stages, side effects and approvals.
- Required Codex/AI operators to use reviewed CLI/API commands rather than
  direct database access, and to avoid launching upstream work implicitly.
- Added acceptance requirements for URL-list and keyword-table entry paths.

Recovery set:

`/opt/docs/config-backups-user/seo-manual-entrypoints-20260924-195734`

## 2026-09-24 — Project documentation foundation

- Registered the planned SEO platform as an independent shared-VPS project.
- Created `/opt/apps/dcwebstudio-seo` and the documentation package under
  `/opt/docs/dcwebstudio-seo`.
- Defined separate Compose/PostgreSQL/secret boundaries and prohibited reuse of
  WordPress MariaDB or another project's runtime resources.
- Defined provider-based SERP acquisition, polite competitor fetching, Google
  Ads/Search Console adapters, provenance-first data modeling, governed AI
  drafting and draft-only WordPress delivery.
- Recorded the current VPS capacity snapshot and a constrained MVP resource
  envelope. No container, database, service, credential or WordPress change was
  made.
- Recorded current OpenAI guidance: new programmatic Codex automation should
  use the Codex SDK/app-server path rather than the removed MCP-server command.

Recovery set for modified shared routing documents:

`/opt/docs/config-backups-user/seo-platform-foundation-20260924-194500`
