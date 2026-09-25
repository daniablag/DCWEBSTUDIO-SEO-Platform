# Open Questions

These are decisions, not blockers to keeping the documentation current. Resolve
them before the phase that depends on them.

## Market and content

Confirmed research scope: Russian and Ukrainian language targets for Ukraine,
represented initially as `ru-UA` and `uk-UA`. Device is an observation segment,
not a page version. Google is the first engine; desktop/mobile evidence produces
one recommendation per language page. See `MVP-SCOPE.md`.

1. Approve or reject the recommendation to preserve current Russian URLs,
   hide the default-language prefix and use directories for additional
   locales. If rejected, approve a redirect/canonical migration budget.
2. Confirm `ru` and `uk` Polylang slugs and the exact WordPress locale-package
   mapping; these adapter values do not change `ru-UA`/`uk-UA` research scope.
3. Confirm that browser-language redirects remain disabled and untranslated
   pages remain unavailable rather than showing copied fallback content.
4. Decide whether media translation support is disabled initially, with ACF
   images copied once and replaceable per locale, or enabled with translated
   attachment records and a separate media QA plan.
5. Which services have commercial priority and which claims are approved?
6. What blog taxonomy should exist before article generation?
7. Name the approvers for clusters, briefs, drafts, WordPress draft delivery
   and final publication.

## Providers

1. Is an active Google Ads account and approved API developer token available?
2. Is `dcwebstudio.com` verified in Search Console with API-capable OAuth
   access?
3. When live SERP collection is enabled, approve DataForSEO or another source
   with acceptable terms, location/language fidelity and cost. Google
   Programmable Search must be evaluated for result fidelity; it is not assumed
   to equal the public organic top ten. This choice does not block the
   owner-supplied URL/keyword MVP path.
4. Which competitor domains are explicitly in scope and which are excluded?
5. What per-job, daily and monthly caps may be assigned to the selected paid
   SERP provider? The baseline remains disabled with a zero budget.

## Data and retention

1. How long may raw HTML/debug payloads be retained?
2. Are external-source excerpts stored at all, or only hashes and extracted
   signals?
3. What off-server backup destination will protect the PostgreSQL data?
4. How often should metrics and competitor observations refresh?

## AI and cost

1. Which model/runtime and per-job budget should writer and reviewer use?
2. Which instructions and company facts are the initial approved source set?
3. What conditions must cause a job to stop and request human input?
4. Which quality checks must be deterministic rather than AI-based?
5. What per-job and monthly AI budget may be enabled after the non-AI vertical
   slice passes? The baseline remains disabled with a zero budget.

## WordPress

1. Approve the ACF policy in `PHASE-0-BASELINE.md`: visible copy and internal
   URLs translate; media copy once; technical presentation values and shared
   contact details synchronize. Approve its listed exceptions.
2. Approve replacing the single shared `company_popup_form` option with a
   synchronized locale-to-CF7-form mapping while retaining the old field only
   as a temporary default-language fallback.
3. Confirm separate Header, Footer 1 and Footer 2 menus per public locale and
   separate CF7 forms per locale before that locale is published.
4. Should content use native posts/categories or a project-owned content type?
5. Which fields/blocks are allowed in the first import payload?
6. Should the WordPress plugin expose a REST endpoint or should an operator run
   a validated WP-CLI import locally?
7. Who owns media selection and localized alt text in the first release?

## Source control

1. Which private remote will back up the single repository: GitHub, GitLab, a
   private Forgejo/Gitea instance or another reviewed destination? Supply the
   empty private repository URL and authentication method without putting any
   credential in documentation or chat.
2. Approve or reject the recommended canonical-doc move into repository
   `docs/`, with `/opt/docs/dcwebstudio-seo` retained as a symlink entry point
   after checksum verification and a recovery set.

## Telegram operations

These choices are deferred until R8 because the bridge depends on stable
CLI/API and notification contracts:

1. Create a separate SEO bot identity or explicitly review shared visible-bot
   routing while keeping service, secrets, Codex state and permissions separate.
2. Confirm the private destination chat and allowlisted Telegram users without
   placing token or raw identifiers in documentation/chat.
3. Approve the initial read-only command list and which planned mutations may
   later use expiring `plan -> confirm` tokens.
4. Decide whether successful job summaries are wanted; actionable final errors
   are the default, while transient retries remain logs only.
