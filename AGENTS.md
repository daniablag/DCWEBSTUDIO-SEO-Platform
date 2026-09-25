# Instructions for the DCWEBSTUDIO SEO platform

These instructions apply to `/opt/apps/dcwebstudio-seo`.

## Mandatory read order

1. `/opt/docs/README.md`
2. `/opt/docs/HANDOFF.md`
3. `/opt/docs/dcwebstudio-seo/README.md`
4. `/opt/docs/dcwebstudio-seo/HANDOFF.md`
5. the project documents routed by that README

Read the WordPress project instructions only when a task explicitly changes
the site plugin, site content or WordPress integration. Do not read or modify
either Poehali project as part of SEO-platform work.

## Boundaries

- Project source/runtime root: `/opt/apps/dcwebstudio-seo`
- Project documentation: `/opt/docs/dcwebstudio-seo`
- Future WordPress adapter: a separately reviewed plugin under the production
  WordPress tree; it does not exist yet.
- The platform must have its own Compose project, PostgreSQL container, volume,
  private network, credentials and lifecycle.
- Never reuse another project's PostgreSQL, Redis, Docker network, Codex state,
  secret files or application user.
- Never connect directly to the WordPress MariaDB. Use an authenticated,
  least-privilege WordPress API or an explicitly reviewed WP-CLI import.

## Data and automation rules

- Treat the product as a composable stage graph, not a mandatory end-to-end
  pipeline. The owner may start from any stage by supplying URLs, a keyword
  table, an approved cluster, a brief, a draft or another valid artifact.
- Before execution, identify the supplied artifact, requested start stage,
  requested result and stop boundary. Produce a dry-run plan when the command
  can mutate data or when the requested boundary is ambiguous.
- Do not run an upstream stage merely because it normally precedes the requested
  work. Owner-supplied competitor URLs skip SERP discovery; an owner-supplied
  keyword table skips discovery/crawling unless enrichment was explicitly
  requested.
- Validate every manual input through the same typed contract as provider data,
  store its source and hash, and record which stages were skipped and why.
- Never repair missing required context by silently launching another stage.
  Report the missing market, target URL, language, column mapping or approval.
- Agents operate the platform through reviewed CLI/API commands. They do not
  edit PostgreSQL rows directly or invent one-off import scripts when a stage
  contract exists.
- Preserve provenance for every fetched, measured, derived and AI-generated
  value. Observed data must never be silently replaced by generated text.
- Respect robots.txt, source terms, rate limits and retention rules. Do not
  scrape Google Search HTML directly as the production SERP source.
- Competitor text is research input, not copy. Store only what is necessary and
  never instruct an agent to paraphrase a competitor article section by section.
- Collection, parsing, normalization and publication-state transitions are
  deterministic application code. AI may propose briefs, drafts, labels and
  reviews only through versioned instructions and structured contracts.
- Initial WordPress delivery is draft-only. Publishing always requires an
  explicit human approval gate.
- A content-generation job receives only the approved brief, approved company
  facts and bounded source extracts. It does not receive infrastructure secrets
  or unrestricted production access.

## Operations

- Do not create a public listener by default. Bind any future admin/API service
  to loopback or a private Docker network until public routing is approved.
- Set explicit CPU, memory, process and concurrency limits before starting a
  runtime on this VPS.
- Back up every changed production configuration and every live data set before
  migration. Keep source and docs owned by `daniablag:daniablag`.
- Store no keys, OAuth tokens, passwords or customer identifiers in Markdown,
  Git, images or logs. Use project-owned secret files or another reviewed secret
  mechanism with restrictive permissions.
- Do not deploy containers, install host packages, create systemd units or alter
  firewall/vhost configuration during planning unless the owner explicitly asks.
