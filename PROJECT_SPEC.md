# GridPulse Project Specification

## Status

Specification status: **PHASE 0 DESIGN BASELINE**

This document defines the currently intended project.

Implementation follows this design baseline, the [phase rules](ROADMAP.md#phase-rules),
and the [runtime verification gates](docs/handoffs/phase-0-to-1.md).

## Project purpose

GridPulse will be a professional Analytics Engineering and Business
Intelligence portfolio project centered on energy data.

The project should demonstrate how raw analytical data can be:

1. acquired or generated reproducibly;
2. ingested into a cloud analytical platform;
3. organized into reliable warehouse layers;
4. transformed and modeled with dbt;
5. validated through automated data-quality checks;
6. optimized for analytical workloads and cost;
7. exposed through business-ready marts;
8. consumed through Power BI as the required BI deliverable; optionally, after core release, demonstrated through a small Looker Studio experiment using a free data path;
9. supported by reproducible infrastructure and CI/CD where justified.

The project must resemble a realistic professional data platform, not a
collection of disconnected technology demonstrations.

## Portfolio role

GridPulse is the portfolio project primarily responsible for developing and
demonstrating:

- BigQuery;
- dbt;
- Analytics Engineering;
- cloud analytical warehousing;
- dimensional / analytical modeling;
- data quality;
- Power BI consumption of curated warehouse models; optionally, a small post-release Looker Studio experiment on the same KPIs;
- Terraform and CI/CD where they naturally support the platform.

Other portfolio projects are intended to cover Spark/Databricks, Snowflake,
Airflow, Kafka, streaming, and related architectures. GridPulse must not absorb
those technologies without a real architectural requirement.

## Business domain

The domain is energy analytics.

The selected source is [EIA-930](https://www.eia.gov/electricity/930-content/about.html),
which publishes hourly demand, day-ahead demand forecasts, and net generation
for U.S. electricity balancing authorities. The initial scope is ERCO (Texas)
for reporting years 2023–2025, focused on demand peaks and day-ahead forecast
accuracy. The sections below define the audience, metrics, and missing-data
rules. See [D-023](DECISIONS.md#d-023--analyze-erco-demand-and-forecast-accuracy-for-20232025).

The final data should ideally support several of the following:

- energy consumption over time;
- meters, facilities, sites, regions, or customers;
- peak-demand analysis;
- consumption trends and seasonality;
- cost or tariff analysis;
- operational efficiency;
- anomaly or unusual-consumption analysis;
- comparisons across locations or periods;
- optional contextual enrichment such as weather when analytically justified.

Supplementary datasets may be introduced only when they improve the business
analysis or modeling challenge rather than merely increasing project scope.

## Intended users

### Initial report audience and questions

The initial audience is a grid operations analyst reviewing historical
demand and forecast performance. The report should show when ERCO demand
peaked, which months and reporting hours had the largest forecast errors,
and whether the forecast tended to be above or below observed demand.

### Initial KPI definitions

Use EIA's reporting date and hour for report filters and UTC hour ending for
row identity. EIA publishes time-weighted hourly average power. The demand
peak is therefore the highest observed hourly average in MW.

| Measure | Calculation within the selected period |
| --- | --- |
| Observed peak demand (MW) | Maximum reported demand across the hours with demand available |
| Mean absolute error (MW) | Average of the absolute difference between forecast and reported demand over paired hours |
| Forecast bias (MW) | Average of forecast minus reported demand over paired hours. A positive value indicates overforecasting on average |
| Paired-hour coverage | Hours with both values divided by all expected reporting hours in the selection |

Missing measurements remain null. If a selection has no paired hours, show
error and bias as unavailable. If it has no observed demand, show the peak as
unavailable. Roll up error metrics from hourly pairs or from summed error and
pair counts. Averaging monthly averages would give unequal weights to hours.
The project uses the source's day-ahead forecast and evaluates it historically.

The [Phase 0 source validation](docs/validation/phase-0-eia930.md) supplies
reference values for these calculations.

Potential analytical consumers include:

- operations managers;
- energy managers;
- finance/business stakeholders;
- analysts;
- executives.

Exact personas will be confirmed during Phase 0.

## Core technology roles

### BigQuery

Primary cloud analytical warehouse.

Expected responsibilities:

- raw and transformed analytical storage;
- scalable GoogleSQL execution;
- datasets and tables;
- partitioning and clustering when justified;
- query-cost and performance analysis;
- native loading and warehouse behavior that should be learned explicitly.

GridPulse should teach BigQuery itself, not only BigQuery as an invisible
backend for dbt.

### dbt

Primary Analytics Engineering transformation layer.

Expected responsibilities:

- source declarations;
- staging models;
- intermediate models;
- marts;
- dependency management through `ref()`;
- tests;
- documentation;
- lineage;
- reusable Jinja/macros when justified;
- snapshots or incremental models when justified;
- model materialization decisions.

dbt is central to GridPulse, but it must not hide native BigQuery concepts that
the user should understand first.

The pilot uses the free local dbt Core distribution with the Python BigQuery
adapter selected during Phase 3. See
[D-028](DECISIONS.md#d-028--use-dbt-core-v1-for-the-unbilled-bigquery-pilot)
for the pinned versions and compatibility rationale.

### SQL

Primary transformation and analytical language.

The project should exercise professional SQL patterns such as:

- CTEs;
- joins;
- aggregations;
- window functions;
- conditional logic;
- date/time analysis;
- dimensional-model transformations;
- reconciliation queries;
- data-quality investigation.

### Python

Python may support:

- ingestion;
- API/file acquisition;
- source generation when a realistic source is unavailable;
- automation or utilities.

Python should not replace SQL or dbt where those are the natural tools.

### Power BI

Final business-consumption and visualization layer.

Expected responsibilities:

- semantic/reporting model;
- DAX measures where necessary;
- interactive analysis;
- business KPIs;
- stakeholder-facing report/dashboard.

Business logic should live upstream in dbt/BigQuery when it is reusable data
logic. DAX should handle semantic/presentation calculations that belong in the
BI layer.

Prefer Power BI Desktop and Import initially where compatible with dataset size
and refresh needs. Assess text-based Power BI Project (PBIP) for version control.
Do not make Pro/PPU paid sharing a project completion requirement.

### Looker Studio (Data Studio) — optional post-release experiment

Looker Studio is a **secondary, optional post-release report (Phase 9)**, not another enterprise BI
platform. The default no-charge data path is a **bounded reproducible CSV
export** of curated BigQuery/dbt results and the documented free Looker Studio
CSV-file upload connector. Google Sheets may be assessed if equally free and
appropriate for this dataset. The direct BigQuery connector requires a Google
Cloud billing account and is **out of scope for initial implementation**.

Verify Looker Studio CSV feature access, quota/size restrictions, and the
append-on-upload behavior (avoid double-counting when refreshing). Reuse
approved KPIs and document dataset freshness. No paid Looker/Looker Studio Pro
subscription or BigQuery billing activation is necessary for this deliverable.

The entire Phase 9 experiment is separately authorized and is not part of
core-project success. An optional **direct** BigQuery integration is recorded
in D-019 for research only; it requires **another** explicit approval and
acceptance of residual billing risk.

### Terraform

Infrastructure as Code for reproducible cloud infrastructure where technically
and economically practical.

Terraform should be introduced when actual resources and dependencies are
understood. It should not be postponed solely to make it look like an optional
portfolio add-on, nor used decoratively.

Potential scope may include:

- BigQuery datasets;
- IAM/service accounts when safe and justified;
- storage or other GCP resources if the final ingestion architecture needs
  them.

### GitHub Actions

CI/CD and automated validation where meaningful.

Potential responsibilities:

- dbt compile/test/build;
- SQL/project checks;
- Python quality/tests if Python exists;
- Terraform fmt/validate/plan where safe;
- documentation or repository checks.

CI/CD design must account for secrets, cloud cost, environment separation, and
the danger of triggering paid cloud work unnecessarily.

Start with repository/static/no-cloud-cost checks. Add tests when ingestion
and dbt models appear, not only in the final CI/CD hardening phase. If cloud
jobs are authorized later, prefer OIDC + Workload Identity Federation,
restricted repository/ref claims, and least-privilege access when feasible.
Do not store long-lived service-account keys or activate billing for CI.

## Explicit non-goals

Unless an approved decision changes the architecture, GridPulse will not use:

- Snowflake;
- Databricks;
- Apache Spark;
- Kafka;
- Airflow;
- Kubernetes;
- Hadoop.

Docker is not automatically required. Add it only if the chosen local workflow
or reproducibility problem clearly benefits from it.
For example, it could isolate conflicting local dependencies or make a complex
toolchain repeatable across machines. A documented local environment with pinned
dependencies may be sufficient and simpler. Compare setup effort, maintenance,
platform compatibility and any licensing or cost constraints before proposing
Docker; containers do not by themselves reproduce cloud data or credentials.
No container workflow has been selected or validated.

## Functional requirements

The completed project should provide:

- reproducible source acquisition/ingestion;
- clearly separated raw and transformed data;
- dbt staging layer;
- reusable business transformation layer;
- analytical marts;
- explicit model grain;
- documented dimensional or analytical model;
- automated data-quality checks;
- reconciliation between important layers;
- documented KPIs and metric definitions;
- primary Power BI report/dashboard, reproducible without paid sharing or a required Google Cloud billing account;
- optional, after core release only: compact Looker Studio report from a validated free CSV or equivalent data source, aligned with approved metrics; it must not block Phase 8 closure;
- reproducible setup instructions;
- technical documentation;
- phase-based validation evidence.

## Non-functional requirements

The project should prioritize:

- reproducibility;
- maintainability;
- modularity;
- traceability;
- testability;
- understandable naming;
- cloud cost control;
- documentation;
- version control;
- least unnecessary complexity;
- security of credentials and secrets.

## Cost constraint — strict zero-billing gate

**The requirement is USD 0 in actual charges, not an expectation of low cost.**
Cloud execution and provisioning require specific authorization under the
phase and cost gates.

**Preferred route:** a BigQuery Sandbox project with **no linked billing
account or payment method for this project**. Google's published limits
(verify again before use) include:

- **10 GiB of Sandbox storage across its lifetime**, not a renewable monthly
  10 GiB allowance; deleting stored data does not refund the allocation;
- **1 TiB of query data processed per month** within the free allowance;
- **60-day automatic expiration** of Sandbox tables, views, and partitions;
- no DML statements or streaming ingestion, which may block some incremental
  model patterns and automated refresh approaches.

BigQuery's **billing-enabled** free usage tier has different conditions: the
first 10 GiB of storage per month and 1 TiB of on-demand query processing per
month are free, but exceeding them or using other services/features can
generate charges. Staying below these two limits alone does **not** guarantee
zero billing across Google Cloud.

The [Phase 0 assessment](docs/phase-0-design-baseline.md#zero-charge-feasibility-and-recovery)
reviews the footprint, rebuild approach, dbt materializations, CI, Power BI,
and infrastructure against the unbilled route. The
[handoff](docs/handoffs/phase-0-to-1.md) records the deferred runtime checks
under the Roadmap exit criteria. Verify each capability before relying on it.
Power BI uses a bounded CSV export and Desktop Import.
If a desired function requires billing, do not enable it: use a valid free
alternative, reduce scope, or explicitly record the blocker/deferred capability.

Where supported, additionally use dry runs/query estimates, conservative
maximum-bytes-billed settings, bounded test inputs, partition-pruned queries
and query quotas. These are **defense-in-depth controls**, not permission to
activate billing. Alerts and budgets do not by themselves prove a USD 0 cap.
Any change to this strict constraint requires a separate explicit user
decision; simply authorizing project work is insufficient.

**Future option only:** A post-release direct Looker Studio-to-BigQuery
connection might require billing. The user has not approved enabling it. Cloud
Billing budgets/alerts and the official Pub/Sub + Cloud Run function billing
shutoff example are delayed, reactive safeguards and do NOT guarantee zero
charges. Query dry runs, maximum bytes billed and approximate custom daily
on-demand query quotas are useful proactive safeguards but do not cover all
costs. Native spend-cap budgets currently list specific services, not BigQuery.
A separate risk assessment and explicit authorization would be prerequisites.
See D-019.

Primary references:
https://docs.cloud.google.com/bigquery/docs/sandbox
https://cloud.google.com/bigquery/pricing
https://docs.cloud.google.com/bigquery/docs/best-practices-costs

## Sandbox-compatible batch workflow and future portability

Prepare a historical batch locally from the six EIA-930 Balance CSV files.
Keep ERCO rows and the common fields needed for the report. Load one
source-aligned BigQuery raw table keyed by balancing authority and UTC hour
ending. The input contract and [rebuild plan](docs/phase-0-design-baseline.md#rebuild-package)
define the schema and handling of source revisions. See
[D-024](DECISIONS.md#d-024--prepare-a-bounded-eia-930-batch-locally-for-bigquery).

### Input contract

Use a UTF-8 CSV with a header and an explicit load schema. Normalize the date
and timestamp syntax while preserving the original reporting calendar and
measurements. Empty measurement cells represent nulls.

| Column | BigQuery type | Source or meaning |
| --- | --- | --- |
| `balancing_authority` | STRING | EIA Balancing Authority, fixed to `ERCO` in the initial scope |
| `reporting_date` | DATE | EIA Data Date, used for year and month selection |
| `reporting_hour_number` | INT64 | EIA Hour Number within the reporting date |
| `hour_ending_utc` | TIMESTAMP | EIA UTC Time at End of Hour, normalized with a UTC offset |
| `demand_mw` | INT64, nullable | EIA Demand (MW) |
| `forecast_mw` | INT64, nullable | EIA Demand Forecast (MW) |
| `net_generation_mw` | INT64, nullable | EIA Net Generation (MW), retained as context |
| `source_file` | STRING | Original EIA filename, matched to the URL and checksum in the source manifest |

The input key is `balancing_authority` plus `hour_ending_utc`. The source uses
23-hour and 25-hour reporting dates around daylight saving changes. Keep all
expected UTC hours, including those with missing measures. Validate column
presence, required values, integer measures, uniqueness, continuity, counts,
and the original file identity before treating the input as a valid batch.
If a later source revision changes the contract or counts, review the
differences before replacing the baseline.

Sandbox does **not** support DML `INSERT`, `UPDATE`, `DELETE` or `MERGE`,
but ordinary SELECT queries, views and relevant table creation (DDL /
CREATE TABLE AS SELECT) can support many useful dbt workflows. dbt `view`,
`ephemeral`, and tested `table` materializations may suffice for the main
pipeline. **Do not assume** every dbt command or materialization works in
Sandbox until the chosen adapter/version and permissions are exercised;
incremental `merge` / `insert_overwrite` workflows commonly emit DML and
are not part of the default executable scope. A full rebuild is not the same
as a row-level `UPDATE`.

For an eventual new environment, require a documented **portability bundle**:
- legal, reproducible source acquisition and checksum/schema/grain notes;
- configuration templates without credentials, required versions/adapters
  and environment-specific BigQuery dataset/project settings;
- versioned SQL, dbt sources/models/macros/tests and approved KPI definitions;
- bounded and reproducible ingestion/rebuild commands plus measured validation;
- known Sandbox limitations (60-day expiry and non-refundable lifetime storage);
- reproducible curated export contract, Power BI project/report artifacts,
  and safe CSV handling for optional Looker Studio;
- a migration/rebuild playbook that marks what was actually tested versus
  merely planned.

Never make activating billing or migrating required for completing Phases
0–8. A later billed environment must be separately approved (D-019).

## Dataset-dependent storage optimization

Start with one raw table and logical staging and fact views. The
[capacity assessment](docs/phase-0-design-baseline.md#zero-charge-feasibility-and-recovery)
includes experiments, repeated loads, and headroom. The 10 GiB Sandbox limit is **lifetime** and
deleted bytes are not credited back.

Evaluate professional patterns *against actual data and query needs*:

- prefer views when a persistent duplicate is unnecessary and repeated query
  scans are acceptable;
- consider dbt ephemeral models for simple intermediate reusable SQL, while
  observing the generated SQL and potential repeat computation;
- persist only selected business-ready marts where performance or semantic
  contracts justify it;
- avoid unnecessary intermediate datasets and wide duplicated tables;
- project only required columns and consider selective dimensional reductions;
- consider partitioning/clustering when supported and demonstrably valuable,
  while accounting for configuration and query-performance tradeoffs;
- keep bounded source samples and model rebuilds reproducible;
- do not assume DML-based incremental strategies work in Sandbox.

The design baseline covers capacity and rationale. Later phases
should compare estimates with real storage/query measurements without breaking
the zero-charge boundary. Storage saved by views may be offset by more bytes
processed in queries: optimize the complete workload, not one isolated metric.

## Learning objectives

GridPulse should provide meaningful, hands-on practice with:

- BigQuery and GoogleSQL;
- BigQuery native loading and storage concepts;
- partitioning;
- clustering;
- query optimization and bytes scanned;
- cloud analytical architecture;
- dbt project structure;
- dbt sources and refs;
- staging/intermediate/marts;
- Jinja;
- dbt tests;
- dbt documentation and lineage;
- materializations and incremental processing;
- dimensional modeling;
- data quality and reconciliation;
- Power BI;
- optional post-release Looker Studio reporting through a free import-based data source;
- DAX;
- Terraform;
- GitHub Actions / CI/CD.

The user should be able to explain what each technology does, why it is used,
what alternatives exist, and what tradeoffs were accepted.

## Learning-first implementation rule

The assistant should not optimize only for finishing quickly.

When a new important concept appears, explain:

- what it is;
- what problem it solves;
- why GridPulse needs it;
- when it is normally used;
- reasonable alternatives;
- relevant limitations or tradeoffs.

Implementation should proceed incrementally so the user can inspect and
validate each layer.

Large blocks of unexplained code, SQL, Terraform, or dbt configuration should
be avoided.

## Portfolio requirements

The final repository should communicate:

- business problem;
- source data and acquisition;
- architecture;
- data grain;
- engineering decisions;
- warehouse organization;
- data model;
- transformations;
- tests and reconciliation;
- infrastructure;
- CI/CD;
- analytical results;
- dashboard;
- known limitations;
- cost considerations;
- reproducibility instructions.

A reviewer should be able to understand why each major technology exists.

## Definition of success

GridPulse is successful when:

- the analytical flow can be reproduced from documented inputs;
- important transformations are tested;
- important row counts/metrics reconcile across layers;
- architecture and decisions are documented;
- BigQuery/dbt behavior is demonstrably understood rather than hidden;
- Power BI answers the approved business questions;
- Looker Studio remains an explicitly optional post-release experiment, not a core success condition;
- Power BI delivery has an evidenced free data path, or a blocker is explicitly documented without enabling billing;
- actual cloud/service charges for the project remain USD 0;
- infrastructure and automation are reproducible where included;
- the repository provides sufficient evidence for technical portfolio review;
- the user can explain and defend the system without relying on memorized
  assistant-generated descriptions.

## Runtime checks after design

Use the [design baseline](docs/phase-0-design-baseline.md) for the selected
source, report, operating plan and rebuild package. Before committing to
the full warehouse load, prove the unbilled environment, the pilot load,
dbt view and tests, and the Power BI Desktop import from a bounded export.
See the [handoff](docs/handoffs/phase-0-to-1.md#handoff-to-phase-1) and
[phase acceptance criteria](ROADMAP.md#phase-18-acceptance-criteria).
