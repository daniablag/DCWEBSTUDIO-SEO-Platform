# WordPress ↔ SEO Integration Boundary

## Purpose

This is the only cross-project entry point between the DCWEBSTUDIO WordPress
site and the SEO platform. Read it only when a task changes the contract or
behavior across that boundary. A shared owner, hostname or Telegram bot does
not make ordinary work cross-project.

## Scope routing

| Requested work | Primary scope | Additional documents |
|---|---|---|
| Keyword research, clustering, briefs or platform runtime | SEO platform only | SEO `AGENTS.md`, `README.md`, `HANDOFF.md` and the routed task document |
| Theme, ACF, content, frontend or unrelated WordPress plugin work | WordPress only | WordPress `AGENTS.md`, site `README.md`, `HANDOFF.md` and the routed task document |
| Define or change the draft-delivery payload | SEO platform first | relevant versioned contract plus site `CONTENT-MODEL.md` |
| Implement or change the WordPress adapter | WordPress first | site `WORKFLOW.md`, `CONTENT-MODEL.md` and the exact SEO contract |
| Activate/configure Polylang or migrate language assignments | WordPress first | site workflow and a separately approved multilingual release plan |
| End-to-end delivery test | both, declared explicitly | this file plus the minimum contract/workflow files from each scope |

## Ownership boundary

The SEO platform owns research artifacts, locale/market identities, content
targets, briefs, drafts, approvals, delivery intent and the versioned adapter
payload. WordPress owns posts/pages, ACF storage, Polylang relations, media,
menus, forms, rendering and publication state.

The SEO platform must never read or write WordPress MariaDB directly. Delivery
uses a reviewed least-privilege WordPress API or an explicitly reviewed WP-CLI
import. WordPress must not depend on the SEO PostgreSQL schema or runtime files.

## Current contract status

- No WordPress adapter or delivery endpoint exists yet.
- Polylang Pro is installed but inactive and unconfigured.
- Initial automated delivery will be draft-only.
- Human approval is mandatory before publication.
- Russian and Ukrainian content targets are researched independently and later
  linked as translations; one language's keywords are not mechanical
  translations of the other.
- Versioned delivery schemas will live under repository
  `contracts/wordpress/v1/` when R0.3 defines them.

## Change procedure

1. Name the primary project and whether the task changes only the contract or
   also a live WordPress implementation.
2. Read the primary project's instructions and only the secondary documents
   named in the routing table above.
3. Back up and validate each affected project independently.
4. Update both handoffs/changelogs only when both projects actually changed.
5. A contract change does not authorize deployment, Polylang activation,
   content publication or a production database mutation.
