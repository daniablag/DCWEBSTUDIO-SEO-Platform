# Infrastructure and Capacity

## Host snapshot

Measured 2026-09-24 before any project runtime was created:

- Ubuntu 24.04.4 LTS;
- Docker Engine 29.8.0 and Compose 5.5.1;
- 2 vCPU;
- 3.8 GiB RAM, about 2.1 GiB available;
- 2.0 GiB swap, about 161 MiB used;
- 78 GiB root disk, 44 GiB free;
- three unrelated Poehali containers, about 90 MiB actual combined usage and
  1 GiB combined memory limits;
- no failed systemd units; shared health check `OK`;
- Docker build cache 18.19 GiB, of which 13.76 GiB was reported reclaimable.

No cache pruning was performed. Reclaimable space is not authorization for a
destructive Docker prune.

## Proposed Compose project

The initial stack should use a unique project name and private network:

```text
dcwebstudio-seo-postgres
dcwebstudio-seo-api
dcwebstudio-seo-worker
dcwebstudio-seo-scheduler
```

No container publishes PostgreSQL. The API has no public port; if needed for
local administration it binds to `127.0.0.1` only. The WordPress integration is
normally outbound from the platform to the existing HTTPS site.

A future `telegram` command may run from the same application image as a small
separate process after the core CLI/API contracts are stable. It uses the
PostgreSQL notification outbox and application service layer; it adds no Redis,
database, public listener or second application framework.

## Initial resource envelope

Planning limits, to be validated under load:

| Service | Memory limit | CPU intent |
|---|---:|---:|
| PostgreSQL | 256 MiB | 0.35 CPU |
| API/CLI service | 192 MiB | 0.25 CPU |
| Worker | 384 MiB | 0.75 CPU |
| Scheduler | 96 MiB | 0.10 CPU |
| Total | 928 MiB | burst-limited |

If the later Telegram notifier/bridge is enabled, start it at no more than
96 MiB and 0.10 CPU, then remeasure total idle and peak usage. It is not part of
the initial R1 runtime.

Use worker concurrency 1 initially. Plain HTTP crawling may use a very small
per-domain-aware concurrency inside one job; AI and browser jobs remain serial.
PostgreSQL should start with low connection counts and conservative buffers.

## Explicit exclusions for this VPS tier

- no local LLM or embedding model;
- no Elasticsearch/OpenSearch;
- no separate Redis until queue measurements justify it;
- no always-running Playwright/browser pool;
- no concurrent Codex worker sessions;
- no unbounded crawl or raw-HTML archive;
- no public administration panel in the MVP.

The same restraint applies to application dependencies: an upstream SEO
project may donate a bounded algorithm or adapter, but it does not bring its
framework, database, queue or frontend into the stack. `REUSE-AND-COST.md`
defines the intake boundary.

## External-cost envelope

The default MVP variable-provider budget is zero. Owner URL/keyword imports,
the bounded project crawler and local deterministic processing remain usable in
that mode. Search Console and PageSpeed are optional quota-limited enrichments.

DataForSEO, AI and any future usage-priced adapter are disabled until a reviewed
configuration supplies provider, price-source version, per-job maximum, daily
cap and monthly cap. The planner estimates the upper bound before enqueueing;
unknown price or exhausted budget stops before the network call. Cache hits and
idempotent replay must not consume a new paid request.

## Capacity conclusion

The current VPS is likely sufficient for an operator-triggered MVP and modest
scheduled refreshes because inference occurs through external APIs and the
database volume is initially small. This conclusion depends on strict limits,
serial heavy jobs and measured retention.

Upgrade or separate the worker when any of these becomes normal:

- multiple simultaneous Codex/browser jobs;
- sustained crawl concurrency above a few requests;
- available memory repeatedly below 800 MiB or material swap churn;
- persistent CPU or I/O full pressure;
- PostgreSQL data/temporary work outgrows the low-memory tuning;
- a public multi-user UI or near-real-time processing is required.

A practical next tier would be at least 4 vCPU and 8 GiB RAM, or an external
worker while keeping the database/API private. Do not resize before measuring
the vertical slice.

## Deployment rules

- Build one application image and run different commands for API, worker,
  scheduler and CLI.
- Pin image/dependency versions and use health checks.
- Run application processes as a non-root UID.
- Use a project-owned volume and separate backup path.
- Define restart policy, log rotation, memory limits and graceful shutdown.
- Emit structured redacted logs with correlation IDs and bounded retention;
  Telegram carries selected alerts, not the full log stream.
- Add a project health check before any scheduled production work.
- Do not add `daniablag` to the Docker group; use the server's narrow sudo
  pattern for reviewed Docker operations.

## Backup requirement

Before live data matters, define automated `pg_dump`, retention, restore test
and off-server copy. A local Docker volume or local dump alone is not a backup
against VPS loss.
