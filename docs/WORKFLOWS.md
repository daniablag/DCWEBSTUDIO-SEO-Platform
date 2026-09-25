# Workflows

## Execution model

Workflows are compositions of independent stages. The full sequence below is a
useful default, not a requirement. An operator can provide an existing artifact
and start at the first compatible stage, then stop at any requested output.

Before execution the platform produces a plan containing inputs, validations,
executed stages, skipped stages, side effects and stop boundary. Upstream stages
are opt-in when their output was not supplied.

Examples:

| Owner request/input | Start stage | Skipped by default | Possible stop |
|---|---|---|---|
| Five competitor URLs | crawl/parse | SERP discovery | parsed comparison or keyword candidates |
| CSV/XLSX keyword table for a page | import/normalize | SERP and competitor crawl | SEO mapping or metadata proposal |
| Approved cluster | page mapping or brief | discovery and clustering | approved brief |
| Approved brief | draft generation | all research stages | reviewed draft |
| Existing draft | review | research and generation | QA report or WordPress draft |
| Existing page URL | page audit | content generation | recommendations only |

If required context is missing, the stage reports it. It does not silently
search the web or infer a target page. Manual inputs receive source
`owner_supplied` (or another explicit actor), original hash, import mapping and
validation report.

## Agent-operated runs

A Codex or another authorized AI operator may translate a natural-language
request into CLI/API calls. It must:

1. read project instructions and the operator interface;
2. identify supplied artifacts and desired output;
3. set start and stop stages explicitly;
4. produce/inspect a dry-run plan;
5. run only the approved plan;
6. report artifact IDs, validations, skipped stages and side effects.

The agent does not get permission to expand scope merely because a downstream
stage could benefit from more research. WordPress mutation still follows the
separate approval contract.

## 1. Research collection

1. Operator creates or imports seed queries for a market.
2. SERP adapter records a versioned result set.
3. Policy selects eligible competitor URLs.
4. Fetcher checks scheme, DNS/IP safety, robots.txt and per-domain limits.
5. Parser extracts metadata and structural signals.
6. Google Ads enrichment receives bounded keyword/URL/site seeds.
7. Raw provider responses are hashed; normalized values are stored separately.
8. Retries are idempotent and cannot duplicate a run's logical records.

Titles and descriptions are useful to understand intent, vocabulary and result
positioning. They are not templates to copy.

## 2. Semantic processing

1. Normalize Unicode, case, punctuation and locale-specific variants while
   preserving the original form.
2. Deduplicate exact and known equivalent phrases.
3. Attach current metrics snapshots by market.
4. Produce candidate clusters using lexical similarity, provider relations,
   SERP overlap and optionally embeddings.
5. Detect likely cannibalization against existing/proposed targets.
6. Review ambiguous cluster merges and assign search intent.
7. Freeze an approved cluster version before briefing.

The system must not select topics using volume alone. Opportunity scoring should
include business relevance, intent fit, current coverage, competition proxy,
evidence quality and expected maintenance cost.

## 3. Page mapping

### Bilingual Ukraine research rule

For one service, Russian and Ukrainian research run as separate locale-scoped
branches within the same Ukraine geography:

1. Collect or import Russian seed/query evidence for the Russian target.
2. Collect or import Ukrainian seed/query evidence for the Ukrainian target.
3. Normalize and cluster only within the applicable locale/search context.
4. Optionally record a reviewed cross-language intent-equivalence link, but do
   not merge keyword membership or metrics across languages.
5. Produce separate page mapping, metadata and brief decisions for each target.
6. Link the two WordPress objects through the approved Polylang relationship,
   not matching slugs, titles or translated keyword guesses.

Device-specific observations may support either branch. They are combined into
one page recommendation unless a material mobile/desktop difference is shown
explicitly; they never produce device-specific pages.

Every approved cluster receives exactly one initial disposition:

- improve an existing commercial page;
- create a new commercial/landing page;
- create an informational blog article;
- merge into another cluster;
- hold/reject with a reason.

Blog category assignment comes from an approved taxonomy map. AI may suggest a
category but cannot create arbitrary production categories.

## 4. Brief creation

A brief contains:

- target URL or proposed slug;
- search intent and concrete user task;
- primary and supporting keywords without density targets;
- unique angle and relationship to existing site pages;
- approved heading outline;
- required company facts and evidence references;
- prohibited claims and uncertainty notes;
- internal links and expected anchor purpose;
- SEO title/meta-description proposal;
- schema/content type;
- acceptance checks.

A human approves the brief before text generation.

## 5. Controlled AI drafting

The CLI creates an immutable job workspace and starts a fresh Codex SDK thread.
Instructions explicitly require the agent to:

- use only approved facts for claims about DCWEBSTUDIO;
- mark missing evidence instead of inventing it;
- treat competitor text as research, not reusable prose;
- follow the approved outline and output contract;
- avoid unsupported numbers, clients, results and guarantees;
- produce a draft plus a structured fact/source manifest.

The writer cannot access WordPress credentials. A separate review run checks
brief compliance, unsupported claims, internal-link targets, metadata and
structural requirements. Deterministic validators run before and after AI
review.

## 6. WordPress delivery

1. Human approves the reviewed draft.
2. Platform sends a versioned JSON payload to the WordPress adapter.
3. Plugin validates schema, permissions, idempotency key and allowed fields.
4. Plugin creates or updates a WordPress `draft`, never a published post in the
   initial release.
5. Plugin returns object ID, edit URL, canonical preview URL and payload hash.
6. Editor performs final WordPress review and publishes manually.
7. Platform records the resulting URL/version and begins monitoring only after
   confirmed publication.

## 7. Feedback loop

Scheduled Search Console imports compare query/page performance over stable
windows. Candidate actions include title/description review, content refresh,
internal-link improvement, consolidation or a new target. Metrics create tasks;
they do not trigger autonomous rewrites or publication.
