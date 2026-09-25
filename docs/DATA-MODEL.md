# Data Model

## Principles

- PostgreSQL is authoritative; WordPress is the publication projection.
- Keep observations, metrics, derived decisions and generated artifacts apart.
- Every mutable business artifact has a lifecycle state and audit trail.
- Every provider result has market, language, location, device, observation
  time and source/run provenance.
- Natural keys and content hashes make collection jobs idempotent.
- Never overwrite historical keyword metrics with the newest value.
- Do not encode one mandatory pipeline position into a business artifact. A
  valid imported artifact may begin a new run at any compatible stage.

## Core entities

### Project and market

- `projects`: site identity and canonical origin.
- `locales`: stable language/locale identity with BCP 47 tag, ISO language,
  optional script/region, WordPress locale, Polylang slug, default flag and
  lifecycle state. Locale does not imply a country or search market.
- `markets`: technical search-observation context with locale reference, ISO
  country, optional provider location ID or region, device, search
  engine/network, timezone, currency and lifecycle state. Multiple normalized
  records may represent device/language segments of one owner-facing business
  geography; they must not be described as separate countries or page versions.
- `project_locales`: which locales a project supports and whether each is
  planned, preparing, active or retired.
- `provider_accounts`: non-secret provider configuration references. Secret
  values live outside the database.

Use UUID primary keys. Enforce uniqueness for a project's BCP 47 locale and for
the normalized market tuple `(project, locale, country, region, device,
search_engine, network)`. Provider-specific geography IDs are mappings, not the
identity of a market.

### Artifacts and execution

- `artifacts`: immutable logical input/output objects with type, schema version,
  content hash, provenance class, owner/source and retention policy.
- `artifact_versions`: original file/object reference, parser/import version,
  row counts and validation summary.
- `workflow_runs`: operator intent, requested start/stop boundary, status and
  approval context.
- `stage_runs`: stage name/version, inputs, outputs, attempt, status, timing and
  error classification.
- `stage_dependencies`: executed or intentionally skipped relationship with a
  machine-readable reason.
- `import_batches`: uploaded URL/keyword/brief/draft material, original hash,
  column mapping, market/target context and row-level validation results.

An artifact can belong to many runs without being copied. A new version never
silently replaces the artifact used by an earlier run.

### Discovery and crawling

- `queries`: normalized search query, market, source and state.
- `serp_runs`: provider request, collection time, status and payload hash.
- `serp_results`: rank, URL, displayed title/snippet, domain and result type.
- `domains`: competitor/owned-domain classification and crawl policy.
- `source_pages`: canonical URL and current known page identity.
- `crawl_snapshots`: HTTP metadata, robots decision, content hash, parser
  version and retention deadline.
- `page_observations`: title, description, canonical, headings, language,
  schema types and bounded extracted signals.

Raw HTML is not retained indefinitely by default. A short-lived artifact may be
stored for parser debugging, then removed according to the retention policy.

### Keywords and metrics

- `keywords`: normalized phrase plus locale/language; equivalent intent in
  another language is a relationship, not the same keyword record.
- `keyword_aliases`: raw spelling and normalization relationship.
- `keyword_sources`: relationship to seed query, SERP page or provider idea.
- `keyword_metric_snapshots`: provider, market, date range, volume,
  competition and bid fields without overwriting older snapshots.
- `keyword_relationships`: parent/variant/related edges with method and score.
- `clusters`: approved semantic/search-intent group.
- `cluster_members`: keyword membership, confidence and review state.

### Content planning

- `content_units`: language-neutral conceptual identity used to group related
  translations without sharing their SEO fields. It stores a stable UUID,
  project, content kind and lifecycle state, but no title, slug or SEO copy.
- `content_targets`: one locale-specific existing canonical URL or proposed
  content item with content-unit reference, locale, path/canonical URL, primary
  cluster, intent, type, funnel stage and state. There is at most one active
  target per `(content_unit, locale)`.
- `content_target_markets`: many-to-many target/market scope with one optional
  primary market, priority and status. This avoids cloning the same locale page
  merely because it is measured in more than one country.
- `content_translation_members`: auditable membership of a locale-specific
  target in a content unit, including source, review state and validity dates.
  This is the platform's translation relation.
- `wordpress_sites`: publication endpoint identity and non-secret adapter
  configuration reference.
- `wordpress_objects`: stable mapping from a content target to WordPress site,
  post type, numeric object ID, status, permalink, remote version and last
  observation time. `(site, post_type, object_id)` is unique.
- `wordpress_translation_sets`: adapter-observed hash/version of the Polylang
  locale-to-object map for one content unit.
- `wordpress_translation_members`: translation-set, locale and WordPress-object
  membership. Never use a Polylang internal taxonomy term or matching slug as
  the platform's durable translation identity.
- `wordpress_taxonomy_map`: deterministic mapping from content type/cluster to
  WordPress taxonomy and term IDs.
- `opportunity_scores`: versioned formula inputs and result; never a single
  unexplained AI score.
- `content_briefs`: target audience, user task, outline, required facts,
  prohibited claims, keyword usage guidance, internal links and approval state.
- `brief_sources`: exact source snapshot/claim relationship.

Keywords, clusters, briefs, drafts, SEO metadata and GSC/provider measurements
reference both `content_target_id` and the applicable `market_id` when the
value is market-specific. No uniqueness rule may collapse records merely
because two markets share a language.

## Multilingual invariants

1. `locale` answers which language/locale the content uses; `market` answers
   where, on which device and search surface it is evaluated.
2. A `content_unit` has no publishable copy. Every title, description, slug,
   brief and draft belongs to a locale-specific `content_target`.
3. A WordPress numeric ID is an external identifier. The platform remains
   stable if a draft is recreated and receives a new WordPress ID.
4. Polylang membership is accepted only from the reviewed adapter payload and
   stored with its observation time and hash. It is never inferred from path,
   title or slug equality.
5. A translation target may exist in the SEO platform before WordPress delivery;
   therefore WordPress mappings are nullable until an approved draft push.
6. Deleting or unlinking a WordPress translation creates a new observed
   relation version; it does not erase prior platform history.
7. For Ukraine-first research, one conceptual service may have one `ru-UA` and
   one `uk-UA` content target. Their keywords, metadata, briefs, drafts and
   performance observations remain separate even when Polylang links them.
8. `desktop` and `mobile` distinguish observations, not content targets. A
   device difference never creates another WordPress page; unknown device is
   stored explicitly rather than inferred.

### Instructions and generation

- `instruction_bundles`: immutable versioned writing/review rules.
- `generation_runs`: provider/runtime, model, thread ID, instruction version,
  input manifest hash, timestamps, usage and outcome.
- `drafts`: generated artifact, structured QA result and revision lineage.
- `review_findings`: rule, severity, evidence and resolution state.

### Publication and feedback

- `publication_jobs`: target, payload hash, approval actor and delivery state.
- `wordpress_objects`: local target to WordPress ID/URL/version mapping.
- `sync_events`: request/result hashes, timestamps and error details without
  secrets.
- `gsc_metric_snapshots`: page/query/date/device/country clicks, impressions,
  CTR and position.
- `audit_events`: actor, action, object, before/after references and timestamp.
- `notification_events`: durable outbox event with severity, stable error code,
  sanitized summary, run/job/stage correlation, deduplication key, occurrence
  count and delivery state.
- `notification_deliveries`: channel, attempt, timestamps, redacted provider
  reference and outcome; no bot token or raw chat secret.
- `operator_commands`: normalized channel command, allowlisted actor reference,
  proposed plan, confirmation state, resulting run/artifact IDs and audit
  outcome. Raw Telegram conversation is not the system of record.

## Required provenance classes

Every data point is classified as one of:

1. `observed` — directly fetched or returned by an API;
2. `normalized` — deterministic transformation of observed data;
3. `derived` — algorithmic score, relationship or cluster;
4. `suggested` — AI/human proposal not yet approved;
5. `approved` — explicitly accepted for downstream use;
6. `published` — confirmed WordPress projection.

Generated text must never be stored in an `observed` field.

## Initial lifecycle

```text
discovered -> researched -> clustered -> mapped
-> brief_ready -> brief_approved
-> draft_generated -> qa_failed | review_ready
-> approved -> delivered_as_draft
-> published -> monitored -> refresh_due
```

No transition from generated text directly to `published` exists in the MVP.
The lifecycle describes possible artifact states, not a mandatory execution
path. A manual import can create an artifact at `researched`, `clustered`,
`mapped`, `brief_ready` or `draft_generated` when its stage validator passes.
The run audit records absent predecessors as `skipped_owner_supplied`, not as
completed work.
