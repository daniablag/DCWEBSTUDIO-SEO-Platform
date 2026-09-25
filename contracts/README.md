# Versioned contracts

This directory freezes transport-neutral contracts before application or
database implementation. Version 1 uses JSON Schema Draft 2020-12 and UTF-8.
The schemas describe boundaries; they do not select a Python framework, ORM,
queue or storage representation.

## Rules

- Every schema has an immutable `$id` and semantic `schema_version`.
- Objects reject unknown properties unless a schema explicitly says otherwise.
- UUIDs are platform identities; provider IDs and WordPress IDs are external
  mappings, never primary identities.
- Timestamps are RFC 3339 `date-time` values with an explicit offset.
- Content hashes use lowercase `sha256:<64 hex characters>`.
- Locale, market and device remain separate dimensions.
- Human/provider input and derived output carry source, validation and lineage.
- Missing data is absent or explicit `null` only where the contract allows it;
  missing metrics are never converted to zero.
- Summaries and errors are sanitized. Schemas do not accept secrets, raw
  authorization material, raw Telegram messages, raw HTML or provider dumps.
- A new incompatible shape requires a new version directory. Existing v1
  fixtures stay valid for the lifetime of v1.

## v1 map

| Boundary | Schema |
|---|---|
| Common IDs, hashes, sources, validation and references | `common/v1/common.schema.json` |
| Project/locale/market/content identities | `identity/v1/identity-record.schema.json` |
| Immutable artifact envelope | `artifacts/v1/artifact-envelope.schema.json` |
| Owner URL input | `imports/v1/url-batch.schema.json` |
| Owner keyword CSV import | `imports/v1/keyword-table.schema.json` |
| Parsed page signals | `observations/v1/page-observation.schema.json` |
| Deterministically normalized keyword | `keywords/v1/normalized-keyword.schema.json` |
| Dry-run workflow plan | `stages/v1/run-plan.schema.json` |
| Executed/skipped/blocked stage result | `stages/v1/stage-result.schema.json` |
| Provider price class and upper-bound estimate | `providers/v1/cost-estimate.schema.json` |
| Normalized offline/provider SERP evidence | `providers/v1/serp-snapshot.schema.json` |
| Sanitized durable notification | `notifications/v1/notification-event.schema.json` |
| Channel delivery attempt | `notifications/v1/notification-delivery.schema.json` |
| Normalized Telegram command | `operator/v1/telegram-command.schema.json` |
| Expiring one-time confirmation | `operator/v1/telegram-confirmation.schema.json` |
| Audited operator outcome | `operator/v1/telegram-outcome.schema.json` |

`tests/fixtures/r0_3/` contains synthetic acceptance data. Run
`uv run --frozen python tests/contract/test_contracts.py -v` to validate schema
syntax, references, examples, CSV boundaries and the fixture checksum manifest.
