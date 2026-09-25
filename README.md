# DCWEBSTUDIO SEO Platform

Status: architecture and documentation foundation only. No application,
database, container, scheduled job or WordPress integration has been deployed.

Current source/runtime root:

`/opt/apps/dcwebstudio-seo`

Current documentation entry point:

`/opt/docs/dcwebstudio-seo/README.md`

The intended product is a private SEO research and controlled content pipeline
for `dcwebstudio.com`. It will collect permitted search/competitor observations,
enrich keyword candidates with provider metrics, maintain a semantic/content
map, create constrained briefs and drafts, and send approved drafts to
WordPress through a narrow adapter.

The implementation baseline is a project-owned thin Python core, one application
image and a separate PostgreSQL database. The useful MVP path starts from an
owner URL list or keyword table and does not require a paid SERP provider or AI.
Paid adapters are disabled until their provider, price source and budget are
explicitly approved.

Open-source SEO applications are reviewed source donors, not runtime services.
Only bounded, licensed components may be adapted behind project-owned contracts
with commit provenance, tests and required attribution.

The canonical future repository tree is defined in
`/opt/docs/dcwebstudio-seo/PHASE-0-BASELINE.md`. Reuse and provider rules are in
`/opt/docs/dcwebstudio-seo/REUSE-AND-COST.md`. Directories should be created only
with the first reviewed implementation slice; empty scaffolding is not a
deployed system.
