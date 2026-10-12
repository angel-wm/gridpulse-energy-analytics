# GridPulse Architecture

## Status

Architecture status: **INTENDED / NOT IMPLEMENTED**

This document explains the current architectural direction. It does not prove that infrastructure, datasets, tables, pipelines, dbt models, Terraform resources, CI workflows, or dashboards exist.

Phase 0 must refine and approve this architecture before implementation.

## Architecture at a glance

GridPulse is intended to move energy data from source systems into a cloud analytical warehouse, transform it through dbt, and expose curated models to Power BI as the required core BI deliverable. A small Looker Studio report is a separately authorized optional post-release experiment.

    Energy source data
            ↓
    acquisition / ingestion
            ↓
       BigQuery raw
            ↓
       dbt staging
            ↓
    dbt intermediate
            ↓
        dbt marts
            ↓
    Power BI (core, Phase 6)
            ↓
    Core portfolio release (Phase 8)

    Optional, after Phase 8 and separate approval:
    dbt curated marts -> bounded CSV export
                     -> Looker Studio dashboard (Phase 9)

Cross-cutting concerns:

| Concern | Role |
| --- | --- |
| Data quality | Tests, reconciliation, and business-rule validation |
| Terraform | Reproducible approved cloud infrastructure |
| GitHub Actions | Safe automated validation and CI/CD |
| Git / GitHub | Version control, review, publication, and handoff |
| Cost / security | Strict zero-billing/no-charge constraints and least-privilege identity shape every implementation decision |

## Core design principle

GridPulse is an Analytics Engineering project, but it must still expose the warehouse concepts being learned.

The intended learning progression is:

    source data
        ↓
    load and query with native BigQuery concepts
        ↓
    introduce dbt abstractions
        ↓
    build maintainable analytical models
        ↓
    expose curated data to Power BI

dbt should improve maintainability without making BigQuery behavior opaque.

## Data flow responsibilities

### Source

The source layer represents the original energy-domain data and any approved contextual sources.

Phase 0 must resolve:

- exact source;
- acquisition method;
- licensing or usage constraints;
- source grain;
- update cadence;
- expected volume;
- supplementary sources.

Source data must remain reproducible or reacquirable.

### Acquisition and ingestion

This layer moves source data into the analytical platform while preserving traceability.

Possible implementations include:

- BigQuery-native loading;
- Python;
- Cloud Storage as a landing layer;
- API or file acquisition.

The selected source should determine the ingestion design. Do not force Python or additional GCP services without a reason.

Important concerns include reproducibility, idempotency where useful, source/load counts, failure visibility, and load metadata when valuable.

### BigQuery raw

The raw layer should:

- retain source-aligned data;
- provide stable transformation inputs;
- preserve traceability;
- support source-to-load reconciliation;
- expose native BigQuery behavior before dbt abstracts downstream work.

Raw data should not silently discard analytically unusual but technically valid records.

Phase 0 or early implementation must define dataset/table naming, loading strategy, schema approach, ingestion metadata, and cost controls.

### Native BigQuery learning

This is a conceptual responsibility, not necessarily a permanent physical dataset.

Before dbt hides an important behavior, the user should understand relevant native BigQuery capabilities such as:

- GoogleSQL execution;
- datasets and tables;
- data types;
- query plans and bytes scanned;
- partitioning;
- clustering;
- native loading;
- views and tables.

Temporary learning objects should not become permanent architecture without a reason.

### dbt staging

Staging should:

- declare sources;
- rename and standardize fields;
- normalize data types;
- establish consistent null/value handling;
- perform light source-level cleaning;
- expose stable building blocks;
- add foundational source/model tests.

Staging should avoid high-level business aggregations.

### dbt intermediate

Intermediate models should centralize reusable joins and transformations that reduce duplication or clarify responsibility.

Do not create intermediate models merely to add another layer.

### dbt marts

Marts should:

- expose business-ready analytical models;
- implement approved reusable metric logic;
- support Power BI efficiently;
- provide stable analytical contracts.

The final model may use a star schema or another justified analytical pattern.

Phase 0 must define fact grain, dimensions, keys, slowly changing behavior if relevant, metric ownership, and expected Power BI consumption.

### Power BI

Power BI should consume curated analytical models and provide stakeholder-facing KPIs and analysis.

Reusable transformation logic should remain upstream when practical instead of being duplicated in DAX.

The report design remains unresolved until business questions and marts are approved.

### Business Intelligence delivery and portability

Power BI is the **primary BI report** and should deliver the semantic/DAX
and interactive reporting layer. Prefer Power BI Desktop with Import when
appropriate and assess text-based PBIP for source control. Do not depend
on paid Power BI sharing or an unverified billing-dependent direct BigQuery
connection. During Phase 0, validate a genuinely no-billing connection or a
small, reproducible export/import workflow from curated results.

Looker Studio (Data Studio) is a **small optional Phase 9 experiment after the
core project is released**, reporting on the same
approved KPI definitions, through a repeatable bounded CSV export and the
free CSV upload source, subject to access and size validation. Since uploads
append rather than replace records, document a deduplicated refresh path.
Direct Looker Studio-to-BigQuery is *not* part of the core architecture or
required Phase 9 execution; it is only a candidate for another separately
authorized post-release experiment. Phase 8 is complete with Power BI.

## Cross-cutting engineering concerns

### Data quality

Expected controls include:

- source/load reconciliation;
- schema expectations;
- not-null checks;
- uniqueness checks;
- relationship/referential checks;
- accepted values where meaningful;
- temporal sanity checks;
- metric reconciliation;
- business-rule tests.

Use tests because they protect real assumptions, not because dbt supports them.

### Zero billing, Sandbox feasibility, and performance

**USD 0 charges are a mandatory architecture gate.** Prefer an unbilled
BigQuery Sandbox project; do not link a billing account or enable paid
resources without a new, separate, explicit user decision.

Google's published Sandbox conditions include a non-replenishing 10 GiB
lifetime storage allocation, a 1 TiB/month query processing allowance,
automatic 60-day table/view/partition expiry, and no DML or streaming.
This means dbt incremental models that use `MERGE` or other DML must not
be presumed available. Favor SQL views/tables and demonstrably supported
materializations; unsupported advanced patterns may be designed and
explained without executing them. Create a reproducible reload/rebuild
plan for object expiration.

Limits differ when billing is enabled, and staying within two BigQuery
free-tier figures is **not** a universal guarantee against charges. Do
not use a budget alert as the project's primary spending protection.

BigQuery decisions should consider:

- bytes scanned;
- table size and query patterns;
- partitioning;
- clustering;
- materialization strategy;
- incremental processing;
- unnecessary rebuilds;
- development versus full-data execution;
- safe query estimates/dry runs and maximum bytes billed where applicable;
- bounded dataset sizes, expected cumulative Sandbox storage, and restart/reload cost;
- explicitly documented fallback when feature/billing prerequisites conflict with USD 0.

Optimization should be evidence-based.

#### Dataset-dependent materialization and storage strategy

Do not lock materializations until the Phase 0 dataset, grain, data volume,
and BI query patterns are known. Estimate the **lifetime** Sandbox allocation
consumed by raw loads, persisted staging/intermediate/marts, experiments and
rebuilds, including reasonable headroom. Consider views and dbt ephemeral
models to avoid unnecessary persisted duplicates, but evaluate their repeated
query scans. Persist compact marts only where justified, avoid ornamental
intermediate tables, and consider partitioning/clustering on the measured
workload. Incremental strategies requiring DML may be unavailable in Sandbox.
Document the chosen rationale and validate it later against real metrics.

#### Optional post-release cost-control study — not an implementation requirement

Do not enable billing during core GridPulse work. If direct BigQuery-to-Looker
Studio is revisited after the release, first document separate approval,
uncapped-charge risks, and available safety layers: conservative BigQuery
custom daily query usage quotas; query-by-query `maximum_bytes_billed` and
dry runs; billing alerts; and Google's programmatic Pub/Sub -> Cloud Run
function -> billing deactivation pattern. Monetary notifications can be
delayed, custom query quotas are approximate and apply only to on-demand
queries, and even automatic billing shutdown cannot guarantee USD 0 costs.
Spend-cap budgets currently do not list BigQuery among eligible services.
Do not deploy any of these billed-project components without specific approval.

### Batch-first execution and migration readiness

A no-DML solution is realistic **if** Phase 0 selects an analytically useful,
reproducible historical/batch source. dbt can build SQL views and appropriate
tables through supported DDL rather than per-row mutations; test adapter/version
behavior before claiming an executable pipeline. `UPDATE`, `INSERT`,
`DELETE`, `MERGE`, and common DML-based incremental strategies are
unavailable in Sandbox. Do not confuse a `SELECT` transformation or
`CREATE TABLE AS SELECT` rebuild with an `UPDATE` statement.

If the business problem requires continual ingestion, late corrections, CDC
or incremental upserts, evaluate a compliant bounded batch rebuild or record
the capability as deferred; do not pretend it was tested. Preserve
source-provenance notes, non-secret environment templates, dbt code/model
contracts/tests, observed quality results, reproducible load/rebuild commands,
BI data-export contracts and versioned Power BI artifacts. Document the
steps for recreating them in a future separately approved environment, without
presuming that Sandbox datasets survive 60-day expiration or upgrades.

### Infrastructure as Code

Terraform may manage approved cloud resources when doing so improves reproducibility and learning.

Potential targets include:

- BigQuery datasets;
- Cloud Storage if selected;
- service accounts or IAM when safe and justified;
- supporting GCP resources required by the final design.

Do not commit secrets or service-account key material.

Not every resource must be managed by Terraform.

### CI/CD

Introduce repository/static validation during the foundation phase, ingestion
checks during acquisition, and dbt/model checks as soon as models exist.
Phase 7 hardens rather than first introduces safe CI.

Potential GitHub Actions checks include:

- dbt dependency/install validation;
- dbt parse/compile;
- dbt tests/build in a safe environment;
- SQL or Python quality checks when applicable;
- Terraform fmt/validate/plan where safe;
- repository/documentation checks.

CI must avoid uncontrolled cloud cost and accidental production changes.
Default to local/CI checks that do not invoke GCP. Any cloud-connected CI
requires separately authorized feasibility and must preserve the zero-billing
constraint.

### Security and credentials

Credentials must remain outside version control.

Prefer short-lived or environment-managed credentials over committed key files where practical.
For GitHub-to-GCP workflows, prefer OIDC with Google Cloud Workload Identity
Federation when necessary and feasible; bind trust to approved repository/ref
claims and minimal IAM roles. Do not create service-account key files or a
billable cloud environment just to demonstrate federation. Local development
must use its own approved credential flow.

The exact authentication strategy is a Phase 0/Phase 1 decision.

## Environment concept

At minimum, the project should distinguish:

- local development;
- CI validation;
- cloud analytical resources.

Separate GCP projects or BigQuery datasets for development/CI/final use should be added only when justified by cost and complexity.

## Likely future repository structure

Implementation folders should be created only when the relevant phase begins.

    ingestion/
    dbt/
    infra/
    powerbi/
    tests/
    docs/

This tree is illustrative, not an instruction to create these folders now.

## Architecture principles

- Give every technology a clear responsibility.
- Learn native BigQuery behavior before hiding it behind abstractions.
- Prefer the simplest architecture that satisfies approved requirements.
- Preserve source-to-metric traceability.
- Keep reusable transformation logic upstream of visualization when practical.
- Treat dbt intermediate models as optional: add them only to centralize genuine reusable work, not as a mandatory hop.
- Preserve approved KPI definitions between BigQuery/dbt marts and Power BI; reuse them if the optional Looker Studio experiment later runs, without duplicating business rules.
- Make important assumptions explicit.
- Validate important transformations and reconciliations.
- Optimize from evidence, not portfolio decoration.
- Control cloud cost deliberately.
- Distinguish intended architecture from implemented architecture.
- Distinguish implementation from validated runtime behavior.
- Do not infer success from documentation or code presence alone.
