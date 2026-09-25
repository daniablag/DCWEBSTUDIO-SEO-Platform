# Architecture

## Goal

Create an auditable pipeline that turns permitted external observations and the
site's own performance data into reviewed SEO decisions and WordPress drafts.
The platform must distinguish facts, measurements, derived decisions and
generated copy.

The execution model is a directed acyclic graph of independently invocable
stages, not a conveyor that must always start at SERP discovery. Every stage has
a versioned input schema, output schema, precondition validator and idempotency
contract. Provider-produced and owner-supplied artifacts enter through the same
validation boundary.

## Proposed component map

```text
SERP provider ─┐
Competitor URLs ├─> collectors ─> parser/normalizer ─> PostgreSQL
Google Ads API ┤                                      │
Search Console ┘                                      v
                                           clusters/opportunities
                                                     │
                                    approved brief + company facts
                                                     │
                                          Codex content worker
                                                     │
                                           deterministic QA gate
                                                     │
                                       WordPress adapter -> draft
                                                     │
                                           human review/publish
                                                     │
Search Console feedback
```

Any box in the diagram is a valid entry point when its required input artifact
already exists. For example, an owner-supplied competitor URL list enters at
the fetch/parse stage, while a keyword spreadsheet can enter at normalization,
metrics enrichment, clustering or mapping depending on its columns and the
requested outcome.

## Composable stage contract

Each stage declares:

- stable stage name and contract version;
- accepted artifact types and required fields;
- optional enrichment fields;
- preconditions such as market, language or target page;
- deterministic validation and import report;
- output artifact types;
- idempotency key/content hash behavior;
- allowed downstream stages;
- side effects and approval requirements;
- retry, stop and resume behavior.

The default is `resolve_missing_upstream = false`. Missing input causes a clear
validation result; it does not authorize a SERP search, Google Ads request,
content generation or WordPress mutation. An operator may explicitly request
additional stages.

## Run planner and import gateway

The run planner converts an operator request into a stage plan before work is
queued. A plan records:

- supplied artifact IDs/files and provenance;
- chosen start and stop stages;
- stages to execute;
- stages intentionally skipped and the reason;
- validation/enrichment steps;
- estimated external providers and mutating side effects;
- required approvals.

The import gateway accepts versioned JSON, CSV/XLSX exports after column
mapping, newline URL lists and platform artifact IDs. Original input is hashed
and retained according to policy; parsed rows and validation errors are stored
separately. Reimporting the same artifact is idempotent unless the operator
creates an explicit new version.

## Runtime components

### API and CLI

One Python application exposes the same service layer through a private API and
a `seo` CLI. The CLI is the first operator interface; a web UI is not required
for the MVP. Suggested implementation: Python, Typer, FastAPI, SQLAlchemy and
Alembic. Framework choices remain provisional until the vertical slice is
specified.

Both interfaces expose the same `plan -> validate -> run -> inspect -> resume`
operations. Natural-language agents are clients of this interface, not an
alternative execution engine.

### Minimal implementation boundary

The platform uses a project-owned thin core for artifact contracts, provenance,
run planning, durable jobs, approval gates, locale/market identities and the
WordPress projection boundary. These guarantees must not be delegated to an
upstream SEO application's schema or lifecycle.

Small MIT-licensed components may be adapted behind project interfaces after
license, commit, security and test review. The platform does not call
SEOctopus, CrawlSEO or OpenGSC as hosted runtime dependencies. The reviewed
donors, intake procedure and external-provider cost rules are defined in
`REUSE-AND-COST.md`.

The required MVP path accepts owner URL lists and keyword tables and works
without paid SERP or AI requests. Provider enrichment is additive and may be
disabled without breaking imports, crawling, normalization or audit history.

### Worker

A separate process executes durable jobs. The initial queue should live in
PostgreSQL, using row locking/advisory locks and explicit retry state. Redis is
not justified for the first workload. Collection and AI concurrency start at 1.

### Scheduler

A small scheduler enqueues refresh jobs and uses a PostgreSQL lock so only one
scheduler is authoritative. It does not execute heavy work itself.

### PostgreSQL

PostgreSQL is the system of record because the product needs concurrent jobs,
metrics history, provenance, relationships, idempotent imports and audit logs.
It must be a project-owned container and volume. SQLite is acceptable only for
throwaway prototypes; WordPress MariaDB is never used for this data.

`pgvector` is deferred. Add it only if measured clustering/retrieval quality
requires embeddings at scale; do not introduce it merely because AI is present.

### SERP provider adapter

The application owns an interface such as `search(query, market, language,
device)`. Provider payloads are normalized but retained by hash/run metadata.
Google Programmable Search can be evaluated, but it is not assumed to reproduce
the exact public organic top ten. A commercial SERP provider may be more
appropriate; the provider decision remains open.

The system must not send automated production queries to ordinary Google Search
HTML. This avoids a brittle parser and an avoidable terms/compliance risk.

### Competitor fetcher and parser

Fetch only result URLs selected by policy. Use HTTP first; a browser fetch is an
explicit fallback for approved JavaScript-dependent pages. The fetcher uses a
clear user agent, per-domain throttling, timeouts, response-size limits,
redirect/SSRF protection, robots.txt evaluation and content hashes.

Extract title, meta description, canonical, language, headings, structured
data, main-text signals and link structure. Do not treat competitor statements
as verified facts about DCWEBSTUDIO.

### Google adapters

- Google Ads Keyword Planning provides keyword ideas and historical metrics
  using keyword, URL or site seeds plus language/location settings. Cache
  responses because these endpoints are rate-limited and historical metrics
  refresh slowly.
- Search Console provides the site's own query/page/device/country performance
  and sitemap operations. It does not provide competitor query data and may
  return top rows rather than every row.

### Content intelligence

Deterministic code performs normalization, deduplication, metric snapshots,
state changes and scoring formulas. Statistical/embedding methods may propose
clusters. AI may label a cluster, propose a brief or draft and explain a
recommendation, but its output is stored as a proposal with model and
instruction provenance.

### Codex worker

Each article/brief job starts a fresh isolated Codex thread unless an approved
revision explicitly resumes that job's thread. The worker receives a generated
workspace containing only:

- an immutable job manifest;
- the approved brief and keyword cluster;
- approved company/service facts;
- bounded source extracts with provenance;
- the applicable versioned instruction bundle;
- a strict output schema and acceptance checks.

The thread has no WordPress credential and cannot publish. A separate reviewer
job should not inherit the writer's conversation. Current OpenAI documentation
supports programmatic local threads through the Codex SDK; the previous Codex
MCP-server pattern is deprecated/removed for new integrations.

### WordPress adapter

A future `dcwebstudio-seo` WordPress plugin owns metadata fields, head output,
schema and a narrow authenticated import endpoint. The platform sends a
validated payload and receives a stable WordPress object ID plus sync status.
Initial writes are limited to drafts and registered SEO fields. There is no
direct MariaDB access and no remote theme-file editing.

## Candidate CLI surface

Names are provisional contracts, not implemented commands:

```text
seo project status
seo run plan --input ... --from ... --to ...
seo run start --plan ...
seo run inspect --run ...
seo import urls --file ... --market ...
seo import keywords --file ... --mapping ... --target ...
seo import brief --file ...
seo import draft --file ...
seo serp collect --query-id ...
seo crawl collect --serp-run ... | --url-batch ...
seo keywords normalize --batch ...
seo keywords enrich --provider google-ads --cluster ...
seo gsc sync --from ... --to ...
seo clusters build --market ...
seo opportunities score
seo brief create --target ...
seo brief approve --brief ...
seo draft generate --brief ...
seo draft review --draft ...
seo wordpress push --draft ...
seo jobs list
seo jobs retry --job ...
```

Commands enqueue or inspect durable jobs. They do not hide untracked background
processes or make publication decisions implicitly. Every stage command can be
used directly by an operator, while `seo run plan` is the safe natural-language
agent entry point for composing multiple stages.
