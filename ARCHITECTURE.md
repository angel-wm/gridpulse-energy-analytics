# GridPulse Architecture

## Status

Architecture status: **INTENDED / NOT IMPLEMENTED**

This document describes the current architectural direction.

It does not prove that any infrastructure, table, pipeline, dbt model, or
dashboard exists.

Phase 0 must refine and approve the architecture before implementation.

## Current conceptual architecture

    Source energy data
            |
            v
        Ingestion
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

Supporting concerns:

    Terraform
        -> reproducible justified infrastructure

    GitHub Actions
        -> validation and CI/CD

    Git / GitHub
        -> version control and publication

## Layer responsibilities

### Source

Original energy-domain data.

The final source and its acquisition method are unresolved.

Source data should be preserved or reproducibly reacquirable.

### Ingestion

Responsible for moving data into the analytical platform while preserving
traceability.

Potential implementations include Python or native loading mechanisms.

The final mechanism must be chosen based on the selected source.

### BigQuery raw layer

Purpose:

- retain source-aligned data;
- provide a stable transformation input;
- preserve traceability;
- enable source-versus-loaded reconciliation.

Raw data should not silently discard analytically unusual but technically
valid records.

### dbt staging

Purpose:

- rename and standardize fields;
- normalize data types;
- establish consistent null/value handling;
- perform lightweight source-level cleaning;
- expose stable building blocks.

Staging should avoid embedding high-level business aggregations.

### dbt intermediate

Purpose:

- combine or enrich staging models;
- centralize reusable transformation logic;
- prepare data for business-facing models.

Intermediate models should exist only when they reduce duplication or clarify
transformation responsibilities.

### dbt marts

Purpose:

- expose business-ready analytical models;
- implement approved metric logic;
- support Power BI efficiently;
- provide stable consumption contracts.

The final fact/dimension or alternative analytical design will be chosen in
Phase 0.

### Power BI

Purpose:

- consume curated analytical models;
- implement only presentation/semantic logic that belongs in BI;
- provide stakeholder-facing KPIs and analysis.

Business logic should not be duplicated unnecessarily between dbt and DAX.

## Cross-cutting architecture

### Data quality

Expected controls include:

- source/load reconciliation;
- schema expectations;
- null tests;
- uniqueness tests;
- relationship tests;
- accepted values where relevant;
- metric reconciliation;
- business-rule tests.

### Cost and performance

BigQuery architecture should consider:

- bytes scanned;
- query patterns;
- partitioning;
- clustering;
- model materialization;
- incremental processing;
- unnecessary table rebuilds.

Optimization must be evidence-based rather than decorative.

### Infrastructure as Code

Terraform scope should be decided after the required resources are understood.

Possible targets include:

- BigQuery datasets;
- tables or supporting configuration where appropriate;
- service accounts/permissions when safe and justified.

Sensitive secrets must never be committed.

### CI/CD

Potential GitHub Actions checks include:

- dbt compile;
- dbt tests against an appropriate environment;
- SQL/project validation;
- Python checks if Python exists;
- Terraform format and validation.

The final workflow must account for secrets, cost, and safe execution.

## Intended future repository areas

Implementation folders should be created only when the relevant phase begins.

Likely future areas include:

    ingestion/
    dbt/
    infra/
    powerbi/
    tests/
    docs/

This list is provisional and not an instruction to create implementation
structure before Phase 0 approval.

## Architecture principles

- Use each technology for a clear responsibility.
- Prefer simple architecture until scale or requirements justify complexity.
- Preserve traceability from source to final metric.
- Keep reusable business logic upstream of visualization when practical.
- Make important assumptions explicit.
- Test important transformations.
- Distinguish intended architecture from implemented architecture.
- Never infer runtime success solely from design documentation.
