# Execution Roadmap

## Purpose

This is the step-by-step delivery order for the DCWEBSTUDIO SEO platform. It is
an execution plan, not a feature wish list. Work advances one numbered step at
a time and crosses a milestone only after its acceptance gate passes.

No date estimate overrides a gate. A later phase may be refined as evidence
appears, but it must not silently expand the active step.

## Status model

- `active` — the only step currently being resolved or implemented;
- `ready` — prerequisites are complete and the step may be started;
- `planned` — ordered but not yet ready;
- `blocked` — a named external decision or dependency prevents progress;
- `done` — deliverables and acceptance checks are recorded as passed.

Current step: **R0.2 — establish private source control (`blocked`)**.

R0.1 is complete. No implementation step is active while R0.2 waits for the
owner-provided empty private remote and authentication method.

No application code, repository, database, container, credential or WordPress
integration exists yet.

## Dependency map

```text
R0 readiness
  -> R1 repository and runtime foundation
  -> R2 durable workflow kernel
  -> R3 safe crawl and page observations
  -> R4 keyword intelligence and page mapping       = research MVP
  -> R5 optional provider enrichment
  -> R6 briefs and governed AI                      = content MVP
  -> R7 WordPress draft delivery                    = delivery MVP
  -> R8 feedback and operations

WP0 multilingual WordPress readiness ---------------> required before R7 only
```

The platform track may progress through R6 without activating Polylang or
changing production WordPress. Paid providers are not required through R4.

## Milestone overview

| Milestone | Status | Outcome |
|---|---|---|
| R0 — implementation readiness | blocked at R0.2 | exact first scope, private repository and accepted contracts |
| R1 — foundation | planned | reproducible private application skeleton and isolated PostgreSQL |
| R2 — durable kernel | planned | artifacts, runs, stages, jobs, provenance and dry-run planning |
| R3 — safe collection | planned | bounded URL import, crawl, parse and page-observation artifacts |
| R4 — research MVP | planned | keyword import, normalization, clustering proposal and URL mapping |
| R5 — provider enrichment | planned/optional | quota-limited Google data and approved live SERP observations |
| R6 — content MVP | planned | approved brief and reviewed draft artifacts with optional AI |
| WP0 — WordPress readiness | planned/separate | reviewed multilingual production contract and canary |
| R7 — delivery MVP | planned | idempotent WordPress draft-only projection |
| R8 — feedback and operations | planned | refresh schedules, Search Console feedback, backup and retention |

## Completion contract for every step

A step is `done` only when all applicable items are true:

1. Its bounded deliverable exists and no unrelated feature was bundled into it.
2. Unit, contract, integration or migration checks appropriate to its risk pass.
3. Failure, retry and rollback behavior is documented and tested where state
   can change.
4. Secrets are absent from Git, Markdown, fixtures and logs.
5. Ownership remains `daniablag:daniablag`; runtime and resource limits remain
   inside the project envelope.
6. The current handoff, roadmap status and changelog are updated once.
7. No unresolved high-risk finding is carried into the next step silently.

## R0 — Implementation readiness

Goal: remove only the decisions that would otherwise make the first code
ambiguous. WordPress publication decisions that are irrelevant to the research
slice remain in the separate WP0 track.

### R0.1 — Freeze the first research scope

Status: `done`, 2026-09-25. The approved values are in `MVP-SCOPE.md`.

Record one exact initial configuration:

- project/site: `dcwebstudio.com` — confirmed;
- first locales: Russian `ru-UA` and Ukrainian `uk-UA` — confirmed product
  direction for Ukraine-first research;
- first search country: Ukraine (`UA`) — confirmed;
- first search engine: Google — confirmed;
- device policy: preserve desktop/mobile measurement segments but produce one
  recommendation per language page — confirmed;
- first accepted inputs: URL list and keyword CSV;
- first outputs: page observations, normalized keywords, proposed groups and
  mapping to an existing or proposed page;
- one owner/approver for imported data and cluster/page mapping — project owner,
  confirmed;
- initial raw-response/extract retention rule — seven-day diagnostic raw
  payload maximum, confirmed;
- external-provider budget: zero for the required R1-R4 path.

Acceptance gate: the values are written as an approved MVP scope with no
ambiguous language, geography, device treatment or implicit paid-provider
fallback. Device segments must not create separate content targets.

### R0.2 — Establish private source control

Status: `blocked`; this is the current step and waits until the owner supplies
an empty private remote and authentication method without exposing credentials
in chat or documentation.

Work:

- create a recovery set;
- initialize the documented monorepo at `/opt/apps/dcwebstudio-seo`;
- add the deny-by-default `.gitignore` before any other project files;
- create `THIRD_PARTY.md` and the source-intake ledger template;
- move canonical project docs into repository `docs/` through the approved
  checksum-and-symlink procedure;
- push the documentation-only initial commit and verify the remote copy.

Acceptance gate: one clean private repository, one canonical documentation
copy, no secret/runtime files tracked and the routed docs still resolve.

### R0.3 — Freeze contracts and acceptance fixtures

Status: `planned`.

Define version 1 schemas for:

- URL batch and keyword-table import;
- artifact envelope, source, hash and validation report;
- run plan, stage result, skipped stage and approval requirement;
- page observation and normalized keyword;
- project, locale, market, content unit and content target identity;
- provider cost class and upper-bound estimate;
- notification event/delivery envelope and normalized Telegram command,
  confirmation and outcome envelope.

Create only synthetic or explicitly permitted fixtures: a small URL list, a
keyword CSV, an offline SERP response and expected normalized outputs.

Acceptance gate: the manual URL and keyword paths can be explained completely
from schemas and fixtures without choosing a framework-specific representation.

### R0 exit gate

- R0.1–R0.3 are `done`;
- the private remote is verified;
- first-slice inputs, outputs and stop boundaries are explicit;
- paid SERP, AI and WordPress are confirmed unnecessary for R1–R4.

## R1 — Repository and runtime foundation

Goal: create the smallest reproducible application shell without business
features.

### Ordered steps

1. **R1.1 Repository skeleton** — create the accepted `src/`, migrations,
   contracts, tests, instructions and deploy layout; add pinned Python tooling
   and license/notice files.
2. **R1.2 Configuration and logging boundary** — typed settings,
   `.env.example` placeholders, structured redacted logs, correlation IDs, log
   rotation and startup validation; no real credential.
3. **R1.3 Isolated PostgreSQL** — one private Compose database, migration tool,
   health check, resource limits and project-owned volume; no published port.
4. **R1.4 Application commands** — one image/package with `api`, `cli`, `worker`
   and `scheduler` entry points; only `seo project status` needs real behavior.
5. **R1.5 Measured smoke test** — record idle memory/CPU, clean startup,
   graceful shutdown and ownership.

Exit gate: a fresh checkout can start the isolated database and application
shell, apply/revert an empty baseline migration and report health without a
public listener or extra stateful service.

Explicitly excluded: crawler, providers, AI, WordPress, Redis and public UI.

## R2 — Durable workflow kernel

Goal: prove the project-owned guarantees before importing donor functionality.

### Ordered steps

1. **R2.1 Persistence core** — projects, locales, markets, artifacts, artifact
   versions, runs, stages, jobs, approvals, audit events and a durable
   notification outbox.
2. **R2.2 Artifact gateway** — schema validation, canonical hashing, source and
   lineage, duplicate detection and row-level import errors.
3. **R2.3 PostgreSQL jobs** — claim/lock, heartbeat, retry, timeout, cancellation
   and restart recovery with worker concurrency 1.
4. **R2.4 Run planner** — explicit start/stop stages, skipped-stage reasons,
   side effects, provider cost class and dry-run output.
5. **R2.5 CLI contract** — `plan`, `validate`, `run`, `inspect`, `resume` and
   `jobs` commands use the same application service layer.
6. **R2.6 Notification contract** — sanitized severity/code/summary, run/job/
   stage correlation, deduplication, delivery attempts and retry state; business
   code emits events and never calls Telegram directly.

Exit gate: identical input is idempotent, a killed worker does not lose a job,
and an unbudgeted paid stage makes no provider request.

## R3 — Safe collection and page observations

Goal: complete the first useful URL-list vertical slice.

### Ordered steps

1. **R3.1 Donor intake** — recheck CrawlSEO/OpenGSC licenses and commits; record
   exact borrowed/derived paths before adapting any implementation.
2. **R3.2 Safe HTTP fetcher** — DNS/IP and redirect-hop SSRF protection,
   robots.txt, user agent, per-domain throttle, timeout, content-type and body
   limits, compression limits and response hash.
3. **R3.3 Parser** — title, description, canonical, language, headings,
   structured data, main-text signals and internal/external link observations.
4. **R3.4 Crawl artifacts** — bounded snapshots, error taxonomy, retention and
   reproducible page-observation output.
5. **R3.5 URL-list acceptance run** — a small permitted fixture reaches durable
   observations through plan, job, retry and inspection paths.

Exit gate: security/failure tests pass, robots decisions are auditable, no
unbounded HTML archive is created and measured load stays inside the VPS limit.

## R4 — Keyword intelligence and page mapping

Goal: deliver the first research MVP without paid APIs or AI.

### Ordered steps

1. **R4.1 Keyword import** — mapped CSV columns, locale/market validation,
   original-file hash and row-level errors.
2. **R4.2 Normalization** — Unicode-aware case/space/punctuation handling,
   locale-sensitive rules, deduplication and preserved source variants.
3. **R4.3 Metrics snapshots** — accept optional owner-supplied metrics without
   treating missing volume/CPC as zero.
4. **R4.4 Group proposals** — begin with explainable deterministic similarity;
   store proposals and reasons, never silently approve clusters.
5. **R4.5 Content map** — connect each approved group to an existing URL or a
   proposed locale-specific content target; detect competing mappings.
6. **R4.6 Research export** — inspect/export observations, groups, unmapped
   opportunities and validation errors without requiring a web UI.

Exit gate — **research MVP**: owner URL and keyword inputs produce repeatable,
reviewable page/keyword artifacts and a content map with full provenance.

## R5 — Optional provider enrichment

Goal: add external observations one adapter at a time without changing the core
contracts or making another adapter mandatory.

### Ordered independent steps

1. **R5.1 Search Console** — least-privilege OAuth, query/page/device/country
   snapshots, paging, quota handling and normalized dates.
2. **R5.2 PageSpeed** — bounded URL selection, mobile/desktop snapshots, caching
   and quota-aware refresh.
3. **R5.3 Live SERP** — only after provider terms and per-job/daily/monthly
   budgets are approved; DataForSEO is the first candidate, not a hard-coded
   dependency.
4. **R5.4 Google Ads keyword planning** — only if account, developer token,
   intended use and caching policy are approved.

Each adapter has contract fixtures, request redaction, timeout/retry rules,
payload hashing and a kill switch. Failure or absence of one provider never
launches another automatically.

Exit gate: every enabled adapter can be disabled without breaking the R4
research MVP; paid estimates reconcile with recorded usage.

## R6 — Briefs and governed content generation

Goal: turn an approved content target into reviewable artifacts while keeping
AI optional and bounded.

### Ordered steps

1. **R6.1 Approved facts** — version company/service facts, prohibited claims,
   style rules and source ownership.
2. **R6.2 Brief contract** — deterministic inputs, target/market, intent,
   headings, required facts, source references and acceptance checklist.
3. **R6.3 Manual brief path** — import, validate, approve and revise a brief
   without AI.
4. **R6.4 Optional AI brief/draft adapter** — isolated job workspace, versioned
   instruction, strict structured output, token/cost cap and no production
   credential.
5. **R6.5 Independent review** — deterministic checks plus a separate human or
   reviewer job; no writer-thread self-approval.

Exit gate — **content MVP**: an approved target produces an approved brief and
reviewed draft artifact, with facts, instructions, model/runtime and revisions
traceable. Nothing is published.

## WP0 — Separate WordPress multilingual readiness track

Goal: prepare production WordPress for later draft projection without blocking
R1–R6.

### Ordered steps

1. **WP0.1 Owner decisions** — retain the confirmed Russian/Ukrainian languages
   and Ukraine geography; decide default language, WordPress locale mappings,
   URL policy, redirects, media, menus/forms and approval roles.
2. **WP0.2 Backed-up theme release** — explicit ACF translation policy,
   locale-aware options, locale-to-CF7 map and fail-closed form selection.
3. **WP0.3 Controlled Polylang setup** — preserve current URLs, assign existing
   Russian content and keep browser redirects off.
4. **WP0.4 Draft canary** — one Contact translation validates isolation,
   relationships, menus, forms, metadata and rollback before broader use.

Exit gate: the WordPress adapter can rely on an approved locale-to-post
relationship contract. This track is a separate production change with its own
authorization, backups and validation.

## R7 — WordPress draft delivery

Goal: project reviewed content into WordPress without granting publication
authority to the platform.

Prerequisite: WP0 exit gate passed.

### Ordered steps

1. **R7.1 Adapter contract** — versioned payload, stable idempotency key,
   allowed fields/blocks, locale relationship and structured error response.
2. **R7.2 Project-owned WordPress plugin/importer** — narrow authentication,
   registered metadata/schema fields and no direct MariaDB access.
3. **R7.3 Draft-only state machine** — create/update drafts only; reject publish
   requests and unapproved payloads.
4. **R7.4 Canary delivery** — one approved draft, retry/idempotency test,
   WordPress ID/permalink observation and rollback.

Exit gate — **delivery MVP**: a reviewed platform artifact becomes the intended
WordPress draft exactly once; publication still requires a human in WordPress.

## R8 — Feedback and operations

Goal: make the useful system observable and recoverable before increasing
automation.

### Ordered steps

1. **R8.1 Search Console feedback** — compare stable query/page snapshots with
   content targets and retain measurement provenance.
2. **R8.2 Telegram error notifications** — send deduplicated actionable final
   failures from the durable outbox, with run/job IDs and no secret, raw HTML,
   provider payload or stack trace.
3. **R8.3 Telegram command bridge** — project-owned bot adapter over the same
   CLI/API service layer; start read-only and require expiring `plan -> confirm`
   tokens for approved mutations. No shell or direct database access.
4. **R8.4 Scheduler** — PostgreSQL-locked schedules for approved refresh jobs;
   no hidden in-process timers.
5. **R8.5 Backup/restore** — automated `pg_dump`, retention, verified restore and
   approved off-server destination.
6. **R8.6 Health and limits** — job backlog, failures, provider spend/quota,
   storage growth, memory/CPU and retention cleanup.
7. **R8.7 Interface review** — add a small private UI only if measured operator
   friction cannot be solved clearly through CLI/API output.

Exit gate: the platform can be operated, audited, restored and cost-controlled
without database edits or undocumented scripts.

## Deferred until evidence exists

- autonomous publication;
- multiple simultaneous AI or browser workers;
- permanent browser pool or browser farm;
- Redis or a separate queue service;
- local LLM or embedding server;
- `pgvector`, vector database, Elasticsearch or OpenSearch;
- public control panel;
- multi-site or customer-facing SaaS behavior;
- real-time rank tracking.

Any deferred item requires measured need, an architecture decision, a resource
and security review, and an updated roadmap before implementation.
