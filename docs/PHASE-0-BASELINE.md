# Phase 0 Design Baseline

## Purpose and status

This document converts the multilingual, persistence and source-control work
into an implementable owner decision packet. It remains a design baseline for
runtime and WordPress work. Source control and the canonical documentation
migration were separately authorized and completed on 2026-09-25; Polylang
activation, WordPress code/content changes, containers and package installation
remain outside the authorized work.

Verified on 2026-09-24:

- WordPress locale: `ru_RU`;
- active theme: `dcwebstudio` 0.1.79;
- Polylang Pro: 3.7.8, inactive;
- published pages: 7, all currently Russian and without language assignment;
- permalink structure: `/%postname%/`;
- Polylang `language` taxonomy: absent;
- ACF inventory: 33 groups and 318 fields including layout fields;
- explicit ACF `translations` settings: 0;
- application root: only `AGENTS.md` and `README.md`, no Git repository;
- SEO documentation root: no Git repository.

## Decisions required from the owner

The owner should approve one row per item before the dependent release begins.

| Decision | Recommended baseline | Required owner input | Blocks |
|---|---|---|---|
| Default WordPress locale/URL | current Russian pages remain the default candidate | confirm no-prefix Russian URL policy | Polylang |
| Research locales | `ru-UA` and `uk-UA` | owner confirmed Russian/Ukrainian for Ukraine; confirm WP locale mappings in WP0 | content/Polylang |
| Search geography | Ukraine (`UA`) | Google plus combined desktop/mobile recommendation confirmed | provider research |
| Default URL | current URLs, no `/ru/` | approve or request prefixed migration | Polylang |
| Added-language URL | lowercase language directory, localized slug | approve directory/slug policy | Polylang |
| Browser redirect | disabled | confirm | Polylang |
| Missing translation | no public fallback copy | confirm | publication |
| Media | media translation off initially; ACF images Copy Once | approve or request translated attachments | WordPress release |
| ACF policy | matrix below | approve exceptions | WordPress release |
| Forms and menus | separate per public locale | confirm ownership and approver | Polylang |
| Git remote | public GitHub repository for the current stage; secret controls do not depend on visibility | confirmed and completed | first code |
| Docs migration | repository `docs/` plus routed symlink | confirmed and completed | docs move |
| Approval roles | project owner initially approves imports and keyword/page maps | name later delegates for briefs, drafts, delivery, publication | governed workflow |
| Telegram operations | logs/outbox first; project-owned notifier and command adapter later | bot/destination supplied only when R8 begins | operations |
| Reuse policy | project-owned thin core plus bounded reviewed MIT components | approve or name an exception | source intake |
| MVP provider spend | zero-variable-cost path; paid SERP/AI disabled | set explicit caps only when enabling | paid stages only |

Google Ads, Search Console, SERP-provider, retention and business-priority
questions remain in `OPEN-QUESTIONS.md` and are resolved before the phase that
uses them.

## Recommended URL and indexing contract

1. Treat current Russian content as the default locale only after owner
   confirmation.
2. Preserve all seven current canonical paths with no default-language prefix.
3. Put the added Ukrainian locale below one directory, proposed as `/uk/`.
4. Use a localized slug inside that directory. Do not force transliterated
   Russian slugs onto translations.
5. Keep browser-language detection and automatic redirection off.
6. Each published translation has a self-referencing canonical. Alternate
   language links come only from the approved Polylang translation set.
7. Do not publish a locale route until its page, menus, form, metadata and
   internal links pass review. An absent translation returns normal not-found
   behavior; it does not display another language under the requested locale.
8. Preserve trailing-slash behavior and avoid query-string language selection.
9. Any future change to prefix the default language is a separate SEO migration
   with a complete old-to-new redirect map, sitemap/canonical update and
   Search Console monitoring.

Language and market remain independent. `/uk/` identifies Ukrainian content;
the approved search geography is separately stored as Ukraine. Russian content
can also be researched for Ukraine even though the current WordPress software
locale is `ru_RU`.

## ACF translation policy

The theme's code-registered fields must receive explicit `translations`
values before a translation is created. Relying on Polylang defaults is unsafe
because all 318 current fields omit the setting and default behavior can also
depend on the global custom-field synchronization option.

### Translate

Translate every reader-visible or locale-routing value:

- `*_eyebrow`, `*_title`, `*_intro`, `*_text`, `*_label`, `*_excerpt`,
  `*_challenge`, `*_timeline`, `*_result`, `industry`, `footer_text` and
  `header_cta_label`;
- all popup headings, body copy and CTA labels;
- all service, capability, case, process, project and portfolio copy;
- internal relative URLs and anchors, including service-card URLs, homepage
  examples CTA URL and popup CTA URLs;
- localized page SEO title, description, canonical proposal and schema copy
  when those fields are added later.

For the ACF Options page, `footer_text` and `header_cta_label` require an
explicit locale-aware implementation such as registered Polylang strings;
ordinary shared `option` reads must not be assumed to translate automatically.

### Copy Once

Copy these values when a translation is first created, then allow the locale
editor to diverge without future source-language overwrites:

- `home_hero_visual` and all content `image` / `icon_image` ACF fields except
  the shared company logo;
- content repeater row structure and order. Visible child text still
  translates and synchronized technical child fields still synchronize;
- the existing `company_popup_form` only as a temporary migration fallback.
  It must be retired from runtime selection after the locale-to-form map is
  available.

With media translation disabled initially, a copied attachment may be replaced
by a locale-specific attachment whenever the visual or alt text needs
localization. Images containing source-language text must never remain shared
on a public translation.

### Synchronize

Synchronize values that express shared identity, presentation or technical
behavior rather than language copy:

- `automation_level`, `uses_ai`, `tone`, `full_width`, built-in icon choices
  and service icon selectors;
- section enable/disable flags unless the owner explicitly authorizes
  market-specific visibility;
- external portfolio destination URLs;
- `company_logo`, phone, email, WhatsApp, Viber, Telegram and social URLs;
- the future complete locale-to-CF7-form mapping, because it is one global
  routing table whose selected member depends on the current locale;
- stable taxonomy/content-type identifiers and future adapter IDs.

### Explicit URL and form exceptions

- Internal URLs: Translate so they point to the matching locale route.
- External portfolio URLs: Synchronize unless a project has an approved
  locale-specific destination.
- CF7: create a separate form per public locale. Replace the single
  `company_popup_form` option with a synchronized mapping of Polylang locale
  slug to form ID, retain the old field only as the Russian rollback fallback,
  and have runtime selection fail closed when the active locale has no form.
- Menus: create separate Header, Footer 1 and Footer 2 assignments per public
  locale. Do not synchronize menu item titles or destination IDs blindly.

Before implementation, generate a machine-reviewable manifest from the live
ACF registry with columns `group_key`, `field_key`, `field_name`, `type`,
`policy`, `reason` and `exception`. Validation must fail if any non-layout field
has no explicit policy. Layout fields derive behavior from their children.

## Safe Polylang release sequence

This is a separate WordPress-scoped release and requires explicit owner
approval.

1. Freeze the owner decision table and exact locale/market matrix.
2. Inventory current pages, page templates, menus, options, CF7 forms, ACF
   values, canonical URLs, sitemap URLs and redirect behavior.
3. Create a timestamped database dump and file/config recovery set; verify that
   the dump is readable and record ownership.
4. Prepare a reviewed theme release that adds explicit ACF translation settings,
   locale-aware option strings, locale-to-CF7 mapping and fail-closed form
   selection. Back up changed files, bump the theme version and validate PHP.
5. Prepare reviewed source copies/specifications for translated CF7 forms and
   language-specific menus, but do not create language assignments before
   Polylang supplies the approved locales.
6. Activate Polylang Pro in a controlled maintenance window. Create only the
   approved default locale first, select the no-prefix default-language mode
   and leave browser-language redirect disabled.
7. Assign exactly the seven known published pages and the current Header,
   Footer 1 and Footer 2 menus to the default locale. Do not bulk-assign
   unrelated post types or attachments.
8. Purge LiteSpeed and verify every existing URL, page ID marker, canonical,
   sitemap, menu, form, REST behavior and database integrity. A changed public
   path is a release failure.
9. Add secondary locale definitions, their separate menus and their separate
   CF7 forms without publishing translated pages.
10. Create one Contact page translation as a draft canary. It exercises page
    text, a repeater, shared contact options, the locale-specific CF7 mapping
    and language-specific menus without publishing a route.
11. Prove edit isolation: Translate and Copy Once values can diverge; changing
    one locale does not overwrite another; Synchronize values propagate exactly
    where the approved manifest says they should.
12. Inspect the adapter-visible locale-to-post map and confirm that WordPress
    IDs are stored only as external mappings.
13. Publish no translation until its copy, form, menu, metadata, internal links
    and indexing state receive explicit owner approval.

Rollback before translations become public is database restoration plus the
backed-up theme/config set and Polylang deactivation. Do not attempt to repair a
failed language assignment by deleting taxonomy rows directly. Once translated
URLs are public, rollback also requires an explicit redirect/indexing plan.

## Multilingual persistence baseline

Use UUIDs for platform identities and integers only for observed external
WordPress IDs.

```text
projects
  -> project_locales -> locales
  -> markets -----------^ (locale is one dimension of a market)
  -> content_units
       -> content_targets (one active target per locale)
            -> content_target_markets -> markets
            -> keywords/clusters/briefs/drafts/metadata by target + market
            -> wordpress_objects (nullable projection mapping)
       -> content_translation_members
       -> wordpress_translation_sets -> wordpress_translation_members
```

Minimum fields and constraints:

- `locales`: UUID, BCP 47 tag, language, optional script/region, WordPress
  locale, Polylang slug, default flag, status; unique by project and BCP 47.
- `markets`: UUID, locale UUID, country, optional region/provider geo ID,
  device, engine/network, timezone, currency, status; unique normalized tuple.
- `content_units`: UUID, project UUID, stable key, content kind and state; no
  locale-specific copy.
- `content_targets`: UUID, content-unit UUID, locale UUID, path/canonical URL,
  intent, content type and state; one active row per unit/locale.
- `content_target_markets`: target UUID, market UUID, primary flag, priority
  and status; no assumption that locale equals country.
- `wordpress_objects`: target UUID, site UUID, post type, numeric object ID,
  remote status, permalink, remote version and observed time; unique external
  object tuple.
- `wordpress_translation_sets`: content-unit UUID, adapter contract version,
  relationship hash and observed time.
- `wordpress_translation_members`: set UUID, locale UUID and WordPress-object
  UUID; unique locale within each set.

The WordPress adapter returns a versioned relationship payload such as
`{content_unit_id, members:[{locale, post_type, wp_id, status, permalink}]}`.
The platform validates it against known targets, hashes it and stores a new
observation only when membership changes. It never queries WordPress MariaDB or
reads Polylang's internal taxonomy tables.

## Final repository layout

The project uses one Python monorepo. It is public for the current stage by
owner decision, while operational data and secrets remain excluded:

```text
/opt/apps/dcwebstudio-seo/
  .gitignore
  .env.example
  AGENTS.md
  README.md
  THIRD_PARTY.md
  pyproject.toml
  uv.lock
  compose.yaml
  Dockerfile
  docs/
    README.md
    HANDOFF.md
    MVP-SCOPE.md
    ARCHITECTURE.md
    DATA-MODEL.md
    WORKFLOWS.md
    OPERATOR-INTERFACE.md
    INFRASTRUCTURE.md
    SECURITY-AND-COMPLIANCE.md
    PHASE-0-BASELINE.md
    DECISIONS.md
    ROADMAP.md
    OPEN-QUESTIONS.md
    CHANGELOG.md
  src/dcwebstudio_seo/
    domain/
    application/
    contracts/
    persistence/
    api/
    cli/
    worker/
    scheduler/
    adapters/
      serp/
      crawling/
      google_ads/
      search_console/
      wordpress/
      ai/
  migrations/
  contracts/
    artifacts/v1/
    stages/v1/
    wordpress/v1/
  instructions/
    brief/v1/
    draft/v1/
    review/v1/
  tests/
    unit/
    contract/
    integration/
    fixtures/
  deploy/
    healthcheck/
    backup/
```

One image runs API, worker, scheduler and CLI with different commands. Domain
and application code do not import provider SDKs directly; adapters implement
the versioned ports. Migrations and JSON contracts are reviewed artifacts.
Test fixtures contain only synthetic or explicitly permitted bounded samples.

The `.gitignore` must reject at minimum `.env*` except `.env.example`, secret
files, OAuth/token material, private keys, dumps, database/volume directories,
runtime workspaces, logs, caches, provider raw payloads, crawled HTML and
competitor collections. CI additionally scans tracked paths and fails on these
classes. Secret examples contain names and placeholders only.

## Canonical documentation migration

This procedure was completed on 2026-09-25 after the owner provisioned and
approved the empty remote:

1. Create a recovery set of `/opt/apps/dcwebstudio-seo` and
   `/opt/docs/dcwebstudio-seo`.
2. Initialize the repository at `/opt/apps/dcwebstudio-seo`, add the approved
   ignore rules first and configure the remote without storing a token in
   repository configuration or documentation.
3. Copy the complete documentation package into repository `docs/`, preserving
   ownership and modes. Commit and push the initial documentation-only state.
4. Compare per-file checksums between the repository copy and the routed docs.
5. Immediately recheck for parallel edits. If any checksum changed, stop and
   merge deliberately before switching the route.
6. Move the old `/opt/docs/dcwebstudio-seo` directory intact into the recovery
   set, then create `/opt/docs/dcwebstudio-seo` as a symlink to
   `/opt/apps/dcwebstudio-seo/docs`.
7. Resolve the route through `/opt/docs/README.md`, read both README and HANDOFF
   through the symlink, verify Git status and confirm the remote commit exists.
8. Keep the recovery copy until at least one subsequent documentation update
   and remote push have been verified.

This preserves the global documentation router while making Git the only
canonical editable copy. Shared server documents remain outside this repository
unless a later cross-project infrastructure change explicitly requires them.

Execution record: initial documentation commit `f744630`; recovery set
`/opt/docs/config-backups-user/seo-repository-migration-20260925-133957`.
