# GridPulse Architecture

## Status

Architecture status: **INTENDED / NOT IMPLEMENTED**

This document describes the current architectural direction.

It does not prove that any infrastructure, dataset, table, pipeline, dbt model,
Terraform resource, CI workflow, or dashboard exists.

Phase 0 must refine and approve the architecture before implementation.

## Current conceptual architecture

    Energy data source(s)
            |
            v
    Acquisition / Ingestion
            |
            v
      BigQuery Raw
            |
            v
      dbt Staging
            |
            v
    dbt Intermediate
            |
            v
       dbt Marts
            |
            v
        Power BI

Cross-cutting concerns:

    Terraform
        -> reproducible approved cloud infrastructure

    GitHub Actions
        -> safe validation / CI/CD

    Data Quality
        -> tests, reconciliation, business rules

    Git / GitHub
        -> version control, review, publication, handoff

## Design principle

GridPulse is an Analytics Engineering project, but the architecture must expose
the warehouse concepts being learned.

The intended learning progression is:

    source data
        ->
    understand/load/query in native BigQuery
        ->
    introduce dbt abstractions
        ->
    build maintainable analytical models
        ->
    expose curated data to Power BI

dbt should improve maintainability and engineering practice without making
BigQuery behavior opaque.

## Layer responsibilities

### Source

Original energy-domain data and any approved contextual sources.

Unresolved until Phase 0:

- exact source;
- acquisition method;
- licensing/usage constraints;
- source grain;
- update cadence;
- volume;
- supplementary sources.

Source data must be preserved or reproducibly reacquirable.

### Acquisition / ingestion

Responsible for moving source data into the analytical platform while
preserving traceability.

Possible implementations may include:

- BigQuery-native loading;
- Python;
- Cloud Storage as a landing layer;
- API/file acquisition mechanisms.

The final design must follow the selected source rather than forcing Python or
additional GCP services unnecessarily.

Expected concerns:

- reproducibility;
- idempotency where useful;
- source/load counts;
- failure visibility;
- metadata such as load time/source file when valuable.

### BigQuery raw layer

Purpose:

- retain source-aligned data;
- provide stable transformation inputs;
- preserve traceability;
- enable source-to-load reconciliation;
- provide direct exposure to native BigQuery concepts before dbt abstracts
  downstream work.

Raw data should not silently discard analytically unusual but technically valid
records.

Phase 0/early implementation must define:

- dataset naming;
- table naming;
- load strategy;
- schema approach;
- whether ingestion-time metadata is needed;
- cost controls.

### Native BigQuery learning layer

This is a conceptual responsibility, not necessarily a permanent physical
dataset.

Before important behavior is hidden behind dbt, the user should understand and
practice relevant native BigQuery capabilities such as:

- GoogleSQL execution;
- table/dataset behavior;
- data types;
- query plans/cost awareness;
- bytes scanned;
- partitioning;
- clustering;
- native loading;
- views/tables where relevant.

Temporary exploration objects should not become permanent architecture without
a reason.

### dbt staging

Purpose:

- declare sources;
- rename and standardize fields;
- normalize data types;
- establish consistent null/value handling;
- perform light source-level cleaning;
- expose stable building blocks;
- add foundational source/model tests.

Staging should avoid high-level business aggregations.

### dbt intermediate

Purpose:

- combine/enrich staging models;
- centralize reusable transformations;
- resolve reusable business logic;
- prepare data for marts.

Intermediate models should exist only when they reduce duplication or clarify
responsibilities.

### dbt marts

Purpose:

- expose business-ready analytical models;
- implement approved reusable metric logic;
- support Power BI efficiently;
- provide stable analytical contracts.

The final design may use a star schema or another justified analytical pattern.

Phase 0 must define:

- fact grain;
- dimensions;
- keys;
- slowly changing behavior if relevant;
- metric ownership;
- expected Power BI consumption pattern.

### Power BI

Purpose:

- consume curated analytical models;
- provide stakeholder-facing KPIs and analysis;
- implement semantic/presentation logic that belongs in BI.

Reusable data transformation/business logic should not be duplicated in DAX
without a clear reason.

Power BI design remains unresolved until business questions and marts are
approved.

## Cross-cutting architecture

### Data quality

Expected controls include:

- source/load reconciliation;
- schema expectations;
- not-null checks;
- uniqueness checks;
- relationship/referential checks;
- accepted values when meaningful;
- temporal sanity checks;
- metric reconciliation;
- business-rule tests.

Tests should be chosen because they protect a real assumption, not because dbt
supports them.

### Cost and performance

BigQuery architecture should consider:

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

Terraform should manage approved cloud resources where doing so improves
reproducibility and learning.

Terraform may begin during the foundation phase once resource requirements are
known.

Potential targets include:

- BigQuery datasets;
- Cloud Storage if selected;
- service accounts/IAM where safe and justified;
- supporting GCP resources required by the final design.

Do not commit secrets or service-account key material.

Not every resource must be managed by Terraform if doing so adds complexity
without learning or reproducibility value.

### CI/CD

Potential GitHub Actions checks include:

- dbt dependency/install validation;
- dbt parse/compile;
- dbt tests/build in a safe environment;
- SQL or Python quality checks when applicable;
- Terraform fmt;
- Terraform validate;
- Terraform plan when safe and appropriate;
- documentation/repository checks.

CI must be designed to avoid uncontrolled cloud cost and accidental production
changes.

### Security and credentials

Credentials must remain outside version control.

The final design should prefer short-lived or environment-managed credentials
over committed key files wherever practical.

Exact authentication strategy is a Phase 0/Phase 1 decision.

## Environment concept

Expected environments are at least conceptual:

- local development;
- CI validation;
- cloud analytical resources.

Whether separate BigQuery datasets/projects are needed for dev/CI/final use
must be justified against cost and complexity.

## Intended future repository areas

Implementation folders should be created only when their phase begins.

Likely future areas:

    ingestion/
    dbt/
    infra/
    powerbi/
    tests/
    docs/

Potential additional areas may be added only when the implemented architecture
requires them.

## Architecture principles

- Give every technology a clear responsibility.
- Learn important native BigQuery behavior before hiding it behind abstractions.
- Prefer simple architecture until requirements justify complexity.
- Preserve source-to-metric traceability.
- Keep reusable transformation logic upstream of visualization when practical.
- Make important assumptions explicit.
- Validate important transformations and reconciliations.
- Optimize from evidence, not from portfolio decoration.
- Control cloud cost deliberately.
- Distinguish intended architecture from implemented architecture.
- Distinguish implementation from validated runtime behavior.
- Do not infer success solely from documentation or code presence.
