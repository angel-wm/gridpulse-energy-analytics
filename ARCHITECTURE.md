# GridPulse Architecture

## Status

Architecture status: **INTENDED / NOT IMPLEMENTED**

This document explains the current architectural direction. It does not prove that infrastructure, datasets, tables, pipelines, dbt models, Terraform resources, CI workflows, or dashboards exist.

Phase 0 must refine and approve this architecture before implementation.

## Architecture at a glance

GridPulse is intended to move energy data from source systems into a cloud analytical warehouse, transform it through dbt, and expose curated models to Power BI.

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
         Power BI

Cross-cutting concerns:

| Concern | Role |
| --- | --- |
| Data quality | Tests, reconciliation, and business-rule validation |
| Terraform | Reproducible approved cloud infrastructure |
| GitHub Actions | Safe automated validation and CI/CD |
| Git / GitHub | Version control, review, publication, and handoff |
| Cost / security | Constraints that shape every implementation decision |

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

### Cost and performance

BigQuery decisions should consider:

- bytes scanned;
- table size and query patterns;
- partitioning;
- clustering;
- materialization strategy;
- incremental processing;
- unnecessary rebuilds;
- development versus full-data execution.

Optimization should be evidence-based.

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

Potential GitHub Actions checks include:

- dbt dependency/install validation;
- dbt parse/compile;
- dbt tests/build in a safe environment;
- SQL or Python quality checks when applicable;
- Terraform fmt/validate/plan where safe;
- repository/documentation checks.

CI must avoid uncontrolled cloud cost and accidental production changes.

### Security and credentials

Credentials must remain outside version control.

Prefer short-lived or environment-managed credentials over committed key files where practical.

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
- Make important assumptions explicit.
- Validate important transformations and reconciliations.
- Optimize from evidence, not portfolio decoration.
- Control cloud cost deliberately.
- Distinguish intended architecture from implemented architecture.
- Distinguish implementation from validated runtime behavior.
- Do not infer success from documentation or code presence alone.
