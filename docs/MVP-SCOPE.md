# MVP Research Scope

## Status

Roadmap step: R0.1, completed 2026-09-25.

Owner-confirmed on 2026-09-25:

- site: `dcwebstudio.com`;
- business/search geography: Ukraine;
- content languages: Russian and Ukrainian;
- each service may have one Russian and one Ukrainian WordPress page connected
  as translations through Polylang;
- SEO research is performed independently in each language for Ukraine;
- each language page receives its own queries, clusters, metadata, brief, draft
  and performance observations;
- Google is the first search engine for Ukraine;
- both desktop and mobile evidence may be collected, while each language page
  receives one combined recommendation and material device differences are
  shown separately;
- the project owner is the initial approver for imports and keyword/page maps;
- successful crawls keep normalized observations and hashes, not raw HTML;
  bounded diagnostic raw payloads expire after at most seven days.

This is a research-scope decision only. It does not authorize Polylang
activation, page duplication, content changes or publication.

## Content and WordPress model

Polylang-linked pages represent the same business concept, but they are not one
shared SEO document:

```text
content_unit: website-development service
  ├─ Russian content_target
  │    ├─ Russian queries used in Ukraine
  │    ├─ Russian SEO title/description/brief/draft
  │    └─ Russian WordPress page mapping
  └─ Ukrainian content_target
       ├─ Ukrainian queries used in Ukraine
       ├─ Ukrainian SEO title/description/brief/draft
       └─ Ukrainian WordPress page mapping

Polylang translation set: Russian page <-> Ukrainian page
```

The system must discover how users actually phrase the service in each
language. It must not create the Ukrainian keyword set by mechanically
translating Russian keywords, or the Russian set by translating Ukrainian
keywords. Cross-language comparison may link equivalent intent, but keyword
membership and SEO decisions remain locale-specific.

## Locale and geography identities

The platform research identities are:

| Dimension | Russian target | Ukrainian target |
|---|---|---|
| Platform BCP 47 locale | `ru-UA` | `uk-UA` |
| Language | Russian (`ru`) | Ukrainian (`uk`) |
| Search country | Ukraine (`UA`) | Ukraine (`UA`) |
| Polylang slug | proposed `ru` | proposed `uk` |
| WordPress locale | current site uses `ru_RU`; final mapping belongs to WP0 | final mapping belongs to WP0 |

The platform locale describes the intended content audience. WordPress UI/
translation-package locale is adapter configuration and may differ; it must not
change the platform identity or search geography. Whether Russian remains the
default unprefixed URL and Ukrainian uses `/uk/` is a separate WP0 decision.

## Google and device meaning

`Google` identifies the search engine whose query demand and results we intend
to study. It does not create another website version. Google is the confirmed
first engine for Ukraine; live SERP access remains optional and disabled until
its provider and budget are approved.

`desktop` and `mobile` are observation segments, not business markets and not
page variants. Google results and Search Console metrics can differ by device,
so the platform preserves the source device when it is known.

The presentation rule is:

- one Russian page and one Ukrainian page for a service;
- one combined SEO recommendation per language page;
- desktop/mobile evidence shown separately only when it materially changes the
  recommendation;
- no desktop-specific or mobile-specific WordPress page;
- device-agnostic manual evidence remains explicitly `unspecified`, never
  guessed.

Internally, the data model may use separate normalized observation records for
desktop and mobile so measurements are not collapsed. Owner-facing reports
must call them device segments, not separate geographies or business markets.

## Required no-paid-provider path

Initial accepted inputs:

- owner-supplied Russian or Ukrainian URL lists;
- owner-supplied Russian or Ukrainian keyword CSV files;
- explicit locale and Ukraine search context on every import.

Initial outputs:

- page observations;
- normalized keywords per locale;
- proposed locale-specific keyword groups;
- mapping to the matching Russian/Ukrainian existing page or proposed target;
- validation and provenance report.

The R1–R4 path keeps the external-provider budget at zero. Live SERP, Google
Ads and AI enrichment remain optional later stages.

## R0.1 completion

All R0.1 scope choices are confirmed. The longer-term normalized-observation
retention period remains a later R3 operations choice; it does not reopen the
seven-day maximum for bounded diagnostic raw payloads.
