# Architecture Decisions

## D-001 — Separate project and database

Status: accepted, 2026-09-24.

The SEO platform lives under `/opt/apps/dcwebstudio-seo` with its own future
Compose project, PostgreSQL, volume, network and secrets. It does not reuse
WordPress MariaDB or another project's containers.

## D-002 — WordPress is a projection target

Status: accepted, 2026-09-24.

Research, metrics, clustering, briefs, jobs and audit history live in the SEO
platform. WordPress receives only approved metadata/content projections through
a narrow adapter. Direct database writes are prohibited.

## D-003 — PostgreSQL-backed jobs before Redis

Status: accepted for MVP, 2026-09-24.

The workload is low-volume and the VPS is memory-constrained. Durable job rows,
locking and retries in PostgreSQL avoid a second stateful dependency. Revisit
only after queue/load measurements.

## D-004 — Provider-based SERP acquisition

Status: accepted in principle; provider open, 2026-09-24.

Production must not depend on scraping ordinary Google Search HTML. A provider
adapter keeps Google Programmable Search, a licensed SERP provider or another
reviewed source replaceable.

## D-005 — AI proposes; deterministic code governs

Status: accepted, 2026-09-24.

AI can label, brief, draft and review. It cannot own collection permissions,
state transitions, credentials, category creation or publication. Outputs are
versioned proposals until approved.

## D-006 — Draft-only WordPress integration first

Status: accepted, 2026-09-24.

The first adapter may create/update drafts and registered SEO metadata only.
Human publication remains mandatory.

## D-007 — Current Codex SDK, isolated thread per job

Status: accepted as the current planning baseline, 2026-09-24.

If Codex is the content worker, use the current programmatic SDK/app-server
contract, not the removed Codex MCP-server command. Start a fresh thread for
each article/brief and a separate reviewer thread; retain only explicit job
lineage and versioned input/output artifacts.

## D-008 — Any-stage entry through typed artifacts

Status: accepted, 2026-09-24.

The workflow is a directed graph of independently invocable stages. The owner
or an authorized agent can begin with supplied URLs, keyword tables, clusters,
briefs, drafts or platform artifact IDs and can define the requested stop
boundary. The run planner validates the artifact, records skipped upstream
stages and never launches missing upstream work implicitly.

Natural-language agents use the reviewed CLI/API and do not manipulate the
database directly. This preserves operator control without creating separate
untracked scripts for every partial workflow.

## D-009 — Multilingual contract precedes SEO publication integration

Status: languages/geography accepted; WordPress URL/mapping policy open,
2026-09-25.

Polylang Pro is the planned WordPress translation-relation layer. Its production
activation is a separate WordPress migration. Russian and Ukrainian research
for Ukraine is approved; activation still waits for the owner-approved default
language, URL, redirect, media, menu/form and WordPress locale-mapping contract.
The SEO platform does not treat language as a synonym for market:
locale/language, country or region, device and search network are separate
dimensions.

Each WordPress translation is a distinct SEO target with its own keyword
mapping, title, description, brief, draft and performance history. A stable
translation-group reference links these targets to the same conceptual content
unit. The platform must not invent missing translations or silently publish one
language's metadata into another language.

## D-010 — Preserve default-language URLs

Status: recommended; owner approval required before Polylang activation,
2026-09-24.

Use the current Russian content as the default locale after owner confirmation,
keep its existing URLs without `/ru/`, and place each additional locale under
one lowercase language directory, proposed as `/uk/`. Keep browser-language
redirection disabled. A translated page uses its own localized slug, self
canonical and only the approved Polylang translation set for alternate links.
Untranslated pages do not receive a copied public fallback.

This minimizes migration risk for the seven indexed URLs while leaving locale
and search market as separate decisions. Choosing prefixes for every language
instead would require an explicit redirect/canonical migration plan.

## D-011 — One monorepo with visibility-independent secret controls

Status: accepted and implemented, 2026-09-25.

Use one repository rooted at `/opt/apps/dcwebstudio-seo` for the Python
application, CLI, Compose definition, migrations, versioned contracts, tests,
AI instruction bundles and canonical project documentation. Runtime state,
secrets, `.env` files, OAuth material, dumps, volumes, logs, provider payloads
and collected competitor data are excluded from Git.

The owner selected the public GitHub repository
`daniablag/DCWEBSTUDIO-SEO-Platform` for the current stage. It may be made
private later, but neither visibility permits secrets or operational data in
Git. Server write access uses a dedicated deploy key whose private half is not
stored in the repository or documentation.

## D-012 — Stable multilingual identities

Status: accepted design baseline, 2026-09-24.

The SEO database uses a language-neutral `content_unit` UUID and one
locale-specific `content_target` per translation. Markets link to targets
through a separate join table. WordPress numeric IDs and Polylang relationship
maps are versioned adapter observations; neither slugs nor Polylang internal
taxonomy identifiers are used as cross-system primary keys.

## D-013 — Canonical docs move into Git through a routed symlink

Status: accepted and completed, 2026-09-25.

After the repository exists, move the complete project documentation package
to `docs/` in the repository, verify checksums and replace
`/opt/docs/dcwebstudio-seo` with a symlink to that directory. The global
`/opt/docs/README.md` route remains unchanged. Keep the former directory in a
timestamped recovery set until the repository, remote push and documentation
route have all been verified.

The migration completed through recovery set
`seo-repository-migration-20260925-133957`; the routed path now resolves to the
repository copy. Retain the recovery set through at least the next verified
documentation update and push.

## D-014 — Project-owned thin core with selective reuse

Status: accepted, 2026-09-24.

Own the contracts, provenance, planner, durable jobs, approval state,
locale/market model and WordPress boundary. Reuse only bounded, reviewed
components from suitably licensed projects behind these interfaces. Upstream
SEO applications are source donors or references, not hosted dependencies and
not replacements for the core data model.

The candidate matrix and source-intake requirements live in
`REUSE-AND-COST.md`. Every direct or closely derived code import records an
immutable upstream commit and preserves its required license notices.

## D-015 — Zero-paid-API MVP path

Status: accepted, 2026-09-24.

The first useful workflow must run from owner-supplied URL lists and keyword
tables without paid SERP access or AI. Search Console and PageSpeed are optional
quota-limited enrichment. DataForSEO, AI and any other usage-priced provider
start disabled and require an explicit non-zero budget before a job is queued.

Unknown price, missing approval or exhausted budget fails closed. It must not
fall back to direct Google HTML scraping or another paid provider.

## D-016 — One-service-shape MVP

Status: accepted, 2026-09-24.

Use one Python package and one image with separate API, CLI, worker and
scheduler commands. PostgreSQL is the only stateful MVP dependency. Do not add
Redis, a public UI, a second backend, a permanent browser pool, local models,
search infrastructure or vector storage until measurements demonstrate a need
and a new decision records the tradeoff.

## D-017 — Ukraine-first bilingual SEO targets

Status: accepted product direction, 2026-09-25.

The first geography is Ukraine and the first content languages are Russian and
Ukrainian. Model them as separate locale-specific content targets under one
language-neutral content unit. The initial platform research identities are
`ru-UA` and `uk-UA`; exact WordPress locale-package mappings remain an adapter/
WP0 concern.

Keyword discovery, clustering, metadata, briefs, drafts and measurements run
independently per language. Translation links may express equivalent business
intent, but one language's keywords are never generated solely by translating
the other language's list.

Desktop and mobile are measurement segments, not page variants. Preserve their
source dimension when available, produce one recommendation per language page
and surface device differences only when they materially affect that decision.

## D-018 — Durable observability with a thin Telegram adapter

Status: accepted direction, 2026-09-25.

Structured local logs and PostgreSQL job/audit state are authoritative. Business
code records a sanitized durable notification event; a later notifier delivers
selected actionable final failures to Telegram with correlation IDs, retry,
deduplication and rate limiting. Telegram is not the only error record and a
delivery failure cannot change the original job result.

The future SEO Telegram command bridge uses the reviewed application service
layer behind CLI/API. It starts read-only; mutations require `plan -> confirm`,
an expiring token, authorization and the ordinary budget/approval gates. It
offers no arbitrary shell, SQL, secret access or publication command.

Keep it inside the SEO project boundary as a small command from the same image.
Do not reuse the owner-facing Telegram Codex bridge's secrets, Codex state,
database, service or lifecycle.

The separately reviewed `/opt/apps/codex-telegram` service may route the owner
to isolated site and SEO development threads. That administrative convenience
does not implement this decision's application notifier or command adapter and
does not permit the SEO runtime to reuse its bot identity, state or privileges.

## D-019 — Transport-neutral v1 contracts before framework code

Status: accepted and implemented, 2026-09-25.

Freeze boundary objects as strict JSON Schema Draft 2020-12 documents before
choosing the application framework, ORM or queue representation. Version 1
covers identities, manual imports, immutable artifacts, observations, provider
costs, run/stage state, notifications and Telegram operator envelopes.

Keep synthetic `.test` fixtures and deterministic offline checks beside the
contracts. Incompatible changes require a new version; application and database
implementations may add internal fields only behind adapters and must continue
to emit valid public contract objects. Raw HTML, real provider dumps, secrets
and original Telegram text remain outside these fixtures and Git.
