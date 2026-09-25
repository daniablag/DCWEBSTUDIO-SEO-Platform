# Security and Compliance

## Secrets

Expected secrets include Google OAuth credentials/refresh tokens, Google Ads
developer token and account references, SERP-provider credentials, OpenAI/Codex
credentials, a future Telegram bot credential and a least-privilege WordPress
credential.

- Never store values in Git, Markdown, database rows, prompts or general logs.
- Mount project-owned secret files read-only with restrictive host permissions.
- Refer to credentials by logical name in configuration and database records.
- Rotate one provider independently without rebuilding content data.
- Redact request headers, query credentials and OAuth responses from logs.

## Network

- PostgreSQL is private and has no host/public port.
- API/admin endpoints default to private network or loopback.
- Outbound fetches reject localhost, private/link-local ranges, metadata
  endpoints and unsafe redirects to prevent SSRF.
- HTTP clients enforce connect/read/total timeouts, response-size limits and
  allowed content types.

## Crawling policy

- Respect RFC 9309 robots.txt decisions and cache them for an appropriate time.
- Use an identifiable user agent and contact page/URL when available.
- Apply per-domain rate limits and bounded retries with backoff.
- Do not bypass authentication, paywalls, CAPTCHAs or access controls.
- Keep a domain denylist and operator override with a recorded reason.
- Do not scrape ordinary Google Search HTML in production. Use an approved API
  or licensed SERP provider whose terms cover the intended use.

Robots.txt is not legal authorization and not a security boundary. Provider
terms, copyright/database rights and applicable privacy law still require
review for the chosen markets and retention policy.

## Content and copyright

Competitor metadata and structure may be analyzed to understand search intent.
The system must not reproduce substantial source text, generate close
paraphrases or build articles by stitching competitor passages together.

Store the minimum source material required for analysis. Prefer extracted
signals and hashes over indefinite raw HTML. Every fact used in generated copy
must point to an approved first-party/company source or an explicitly accepted
external source.

## Prompt-injection boundary

Fetched pages are untrusted data. Their text can contain instructions intended
for an agent. Collection/parsing code must label source text as data, and the
writer receives bounded extracts inside a schema that explicitly forbids
following source instructions.

The agent has no secret-reading tool, no Docker socket, no production database
access and no WordPress publish permission. Use workspace-only filesystem
access for content jobs. Review output for unexpected links, instructions,
claims and data exfiltration patterns.

## WordPress permission model

- Dedicated integration user with the minimum capability set.
- HTTPS only.
- Idempotency key on every write.
- Plugin allowlists writable post types, statuses and meta fields.
- Initial endpoint permits `draft` only.
- Publication, deletion, taxonomy creation and media replacement are excluded.
- Audit both the platform request hash and WordPress result.

## Telegram permission and notification model

- Use a project-owned bot token/secret reference and explicit Telegram user and
  chat allowlists; store neither raw identifier nor token in Git or Markdown.
- Default to outbound long polling or another private design that does not
  require a new public listener. A webhook requires a separate routing/TLS/
  secret review.
- Start commands read-only. Mutations require an auditable dry-run plan, an
  expiring one-time confirmation and the same authorization/budget gates as
  CLI/API.
- Never expose arbitrary shell, SQL, secret reads, publication, deletion or
  permission-management commands.
- Redact secrets, query strings, raw HTML, provider payloads, source excerpts,
  prompts and stack traces from Telegram messages.
- Rate-limit and deduplicate notifications by stable event key. Notify final or
  actionable failure, not every transient retry.
- Record command actor, normalized command, plan/run IDs and outcome. Store the
  minimum Telegram message data needed for audit and retention.
- Do not reuse the owner-facing multi-project Telegram Codex bridge's secrets,
  Codex state, service or runtime lifecycle. Its isolated SEO development
  thread is not the application's notifier/command adapter.

## Retention baseline

The confirmed baseline separates:

- successful fetches retain normalized observations/hashes but not raw HTML;
- bounded diagnostic raw fetch payloads expire after at most seven days;
- longer-lived parsed observations and hashes;
- historical metrics needed for trends;
- immutable instruction/approval/publication audit records;
- removable provider debug payloads.

Retention must be implemented as explicit jobs with dry-run/reporting before
deletion.
