# Operator Interface

## Purpose

Allow the owner, Codex or another authorized AI to start work from any valid
artifact without executing the whole SEO workflow. Natural language is an
operator convenience; stage contracts remain the system authority.

## Starting a Codex project chat

Start Codex with `/opt/apps/dcwebstudio-seo` as the working directory so its
`AGENTS.md` is loaded. Official Codex documentation confirms that project
instructions are discovered from `AGENTS.md` at the project/current directory
and its parents. The project file then routes the agent to this documentation.

Until the CLI exists, requests are planning-only. An agent must not improvise
database writes, containers or production changes to simulate missing commands.

## Natural-language request contract

The operator request may include:

- input: file path, pasted table, URL list or existing artifact/run ID;
- target: page URL, proposed page, site section or blog category;
- market: language, location and device when relevant;
- start: explicit stage, or inferable from the artifact type;
- stop: exact requested output;
- enrichment: providers that may be called;
- mutation: whether a WordPress draft may be created;
- budget/deadline constraints.

Only input and desired result are essential when the remaining context is
unambiguous. The agent should infer the smallest safe plan and show assumptions.

## Required planning response

Before a mutating or multi-stage run, the agent produces a plan equivalent to:

```text
Input: owner-supplied URL list, 5 rows
Start: crawl/parse
Run: validate URLs -> robots/policy -> fetch -> parse -> compare
Skip: SERP discovery (owner supplied the result set)
Stop: competitor comparison
External calls: 5 domains; no Google Ads
Mutations: project database only; no WordPress write
```

For a keyword file:

```text
Input: keywords.xlsx, sheet ERP, target /avtomatizacziya-erp-proczessov/
Start: keyword import/normalization
Run: map columns -> validate locale -> normalize -> deduplicate -> map to page
Skip: SERP discovery and competitor crawling
Stop: SEO title/description and coverage proposal
External calls: none unless Google Ads enrichment is explicitly approved
Mutations: project database only; WordPress unchanged
```

## Artifact types

Initial public operator types:

- `url_batch`;
- `keyword_batch`;
- `serp_snapshot`;
- `page_observation_batch`;
- `metric_snapshot_batch`;
- `cluster_version`;
- `content_target`;
- `content_brief`;
- `content_draft`;
- `review_report`;
- `wordpress_payload`.

Each artifact has an ID, schema version, source/actor, creation time, market and
target context where applicable, content hash, validation result and lineage.

## Partial-run rules

- Upstream is never automatic.
- Downstream is limited by the requested stop boundary.
- `--resolve-missing-upstream` is off by default.
- Missing required context produces a validation report, not guessed data.
- Manual and provider inputs use the same schema after import validation.
- Reusing an artifact does not mutate its previous version.
- Every skipped stage has a reason such as `owner_supplied`, `not_requested` or
  `existing_approved_artifact`.
- A partial run can later be resumed from any produced artifact.

## WordPress boundary

Creating a recommendation, SEO metadata proposal or article draft inside the
platform is not a WordPress mutation. A WordPress write requires an explicit
request, an approved payload and the adapter's draft-only permission. An agent
must state this side effect in the plan before execution.

## Logging and error notification boundary

Every run, stage and job receives a correlation ID used consistently in
structured logs, audit events and notifications. Application code records the
final state and writes a sanitized notification event to the PostgreSQL outbox
before any channel delivery is attempted.

The R1.2 application boundary uses canonical UUID correlation IDs and emits one
bounded JSON object per line with timestamp, level, logger, stable event name,
message and correlation ID. Structured fields are recursively bounded and keys
for credentials, authorization, cookies, raw HTML, provider payloads, prompts
and source excerpts are redacted. Common bearer, assignment, URL-userinfo and
private-key forms are also removed from free text. Invalid inbound correlation
IDs fail rather than reaching a log record.

Telegram receives concise actionable events, not the general log stream. The
default notification set is:

- job/stage failure after retries are exhausted;
- stuck job, timeout or repeated crash;
- provider authentication, quota or approved-budget block;
- database migration, backup or restore failure;
- WordPress draft-delivery failure when that adapter exists.

Transient retries remain in logs and job history without Telegram spam. A
notification contains severity, stable error code, time, run/job/stage ID and a
short redacted explanation. It contains no secret, authorization header, raw
HTML, full provider payload, prompt/source excerpt or stack trace. Telegram
delivery failure is logged and retried without changing the original job result
or generating recursive alerts.

## Future Telegram command bridge

The SEO Telegram bridge is a thin project-owned adapter over the same
application service layer as CLI/API. It is not a shell, database console or a
second workflow engine.

Initial read-only commands may expose:

```text
/seo_status
/seo_jobs
/seo_run <run-id>
/seo_errors
/seo_plan_status <plan-id>
```

Later mutating commands follow the ordinary planner contract:

```text
Telegram request -> validate -> dry-run plan -> expiring confirmation token
-> owner confirms -> enqueue reviewed command -> return artifact/run IDs
```

The bridge never accepts arbitrary shell text or SQL. It cannot publish,
delete, bypass budgets, read secrets or broaden a requested stage boundary.
Natural-language Telegram messages may be converted into a proposed plan, but
the plan remains authoritative and all mutations are audited and idempotent.

The existing private owner-facing multi-project Telegram/Codex bridge is a
separate administrative project. It can route development sessions to isolated
site and SEO threads, but it is not the runtime adapter described here. The SEO
adapter does not reuse its service, Codex state, database, secrets or lifecycle.
Using the same visible bot identity later would require a deliberate cross-
project routing and permission review; the safe default is a separate project-
owned bot credential and allowlist.

## Future CLI examples

These commands document the intended interface and are not implemented yet:

```text
seo run plan --input urls.txt --from crawl --to compare
seo run plan --input keywords.xlsx --target <url> --from normalize --to seo-meta
seo import urls --file urls.txt --market <market>
seo import keywords --file keywords.xlsx --mapping mapping.json --target <url>
seo stage crawl --url-batch <artifact-id>
seo stage normalize --keyword-batch <artifact-id>
seo stage map --keyword-batch <artifact-id> --target <url>
seo stage brief --cluster <artifact-id>
seo stage draft --brief <artifact-id>
seo stage review --draft <artifact-id>
seo wordpress push --draft <artifact-id>
```
