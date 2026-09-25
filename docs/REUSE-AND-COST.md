# Reuse, Providers and Cost Baseline

## Purpose and status

This document is the implementation boundary for keeping the SEO platform
small, understandable and inexpensive. It records what the project owns, what
may be adapted from open source and when an external paid API is allowed.

Status: accepted planning baseline, 2026-09-24. It does not authorize source
imports, package installation, provider signup, credential creation, runtime
deployment or paid requests.

## Product rule

The platform is a project-owned application, not a hosted wrapper around
another SEO product. It never depends on SEOctopus, CrawlSEO, OpenGSC or another
reviewed project remaining online. Suitable open-source implementations may be
adapted behind our contracts; the upstream applications are not runtime APIs.

The MVP must remain useful with no paid provider and no AI runtime. Its required
zero-variable-cost path is:

```text
owner URL list or keyword CSV
  -> validated import
  -> HTTP crawl/parse or keyword normalization
  -> PostgreSQL artifacts and audit trail
  -> reviewed export
```

Search Console and PageSpeed may enrich that path within their quotas after
credentials are configured. Live SERP collection and AI generation are
optional capabilities, not preconditions for the core workflow.

## What the project owns

These parts encode DCWEBSTUDIO-specific guarantees and must remain small,
explicit and covered by project tests:

- typed artifact and stage contracts;
- hashes, provenance, lineage and retention metadata;
- run planning, skipped-stage records and stop boundaries;
- durable PostgreSQL jobs, retries, locks and deterministic state transitions;
- project, locale, market, content-unit and content-target identities;
- approval gates and paid-action authorization;
- bounded provider ports and normalized observations;
- the WordPress draft-only adapter contract.

Do not replace these boundaries with an upstream application's database schema,
background-task model or implicit workflow.

## Reviewed open-source candidates

| Project | License at review | Decision | Potentially reusable scope |
|---|---|---|---|
| [SEOctopus](https://github.com/itsjwill/seoctopus) | MIT | reference only | CLI/MCP command naming and report presentation |
| [CrawlSEO](https://github.com/crawlseo/crawlseo) | MIT | preferred technical donor | robots handling, redirect/SSRF safety, response limits, GSC and PageSpeed adapter tests |
| [OpenGSC](https://github.com/fenjo26/opengsc) | MIT | selective donor | safe fetching, provider logging/redaction, paid-action confirmation and content preflight patterns |
| [SEO Command Center](https://github.com/testedmedia/seo-command-center) | MIT | reference only | DataForSEO request, caching and cost-control patterns |
| [StackSEO](https://github.com/maximally0/stack-seo) | no usable license found at review | reject for code reuse | architecture may be studied, but code must not be copied |

The review snapshot is dated 2026-09-24. Repository activity and licensing must
be rechecked at the exact commit before any code is imported.

### Intake rule

For every imported or closely adapted implementation:

1. Record upstream repository, immutable commit, source paths, license and the
   project files that derive from it.
2. Copy only the smallest coherent component; never vendor a complete upstream
   application merely to obtain one feature.
3. Place the component behind a project-owned adapter or domain interface.
4. Add contract, security and failure-path tests before enabling it.
5. Preserve required copyright and license text in `THIRD_PARTY.md` and the
   repository's license-notice area.
6. Remove upstream telemetry, hosted-service assumptions, secret storage,
   direct Google HTML scraping and background work tied to a web request.

Architecture ideas may be reimplemented without copying source. Direct or
closely derived code receives attribution even when it has been translated to
another language.

## External provider baseline

| Capability | MVP default | Cost posture | Enablement rule |
|---|---|---|---|
| Owner CSV/JSON/URL import | enabled | no external fee | always available |
| Project HTTP crawler | enabled, bounded | VPS resources only | robots, rate, size, redirect and SSRF controls required |
| Search Console API | optional | no API charge; quota limited | enable after least-privilege OAuth review |
| PageSpeed Insights API | optional | quota limited; no planned per-call budget | cache results and avoid full-site repeated runs |
| WordPress REST/WP-CLI adapter | later, draft-only | no external per-call fee | separate reviewed WordPress release |
| DataForSEO SERP | disabled | paid, usage based | explicit provider approval and non-zero budget required |
| Google Ads keyword planning | disabled | access/quota dependent | enable only if account/token and terms are approved |
| AI/Codex API worker | disabled | paid, usage based | separate per-job and monthly budget required |

Pricing is never hard-coded as business truth. The planner reads versioned
provider price configuration, records the price version used for an estimate
and treats an unknown price as a reason not to enqueue a paid job.

Official references:

- Search Console pricing and quotas:
  https://developers.google.com/webmaster-tools/pricing
- PageSpeed Insights API:
  https://developers.google.com/speed/docs/insights/v5/get-started
- DataForSEO SERP pricing:
  https://dataforseo.com/apis/serp-api
- OpenAI API pricing:
  https://developers.openai.com/api/docs/pricing

## Paid-action contract

Every adapter declares `cost_class` as `local`, `quota`, `paid` or `unknown`.
A plan containing `paid` or `unknown` work must show:

- provider and operation;
- unit and estimated count;
- price-source version and maximum estimated charge;
- cache/idempotency effect;
- project, daily and monthly remaining budgets;
- the approval required before enqueueing.

Paid adapters default to disabled. Absence of a credential, current price or
budget never triggers a fallback scrape or another paid provider. The stage is
skipped or stopped with an auditable reason. Retries must not create duplicate
billable requests when the provider supports idempotency or result polling.

## Simplicity and load guardrails

- One Python package and one application image; API, CLI, worker and scheduler
  are commands over the same application layer.
- PostgreSQL is the only stateful service in the MVP.
- CLI first; no public UI or second backend framework.
- Worker concurrency starts at 1; browser and AI work are serial.
- HTTP is the default crawler. A short-lived browser fallback is a later,
  measured capability, never a permanent browser pool.
- No Redis, local LLM, Elasticsearch/OpenSearch, vector store, event bus or
  plugin marketplace without measured need and a recorded decision.
- No dependency is added merely because it exists upstream. Prefer the Python
  standard library or an already approved dependency when the result remains
  clear and testable.
- Raw responses are bounded and retained only when required by the approved
  provenance/retention policy.

## First-slice acceptance

Before adding a paid provider or AI worker, the vertical slice must prove that:

1. A URL list reaches crawl/parse and durable artifacts without SERP access.
2. A keyword CSV reaches normalization/mapping without crawl or AI.
3. Restarting the worker cannot silently lose a queued job.
4. Reimporting identical input is idempotent.
5. Resource limits and retention keep the current VPS inside the documented
   capacity envelope.
6. A paid stage with no approved budget performs no network request and records
   a clear stopped/skipped result.
