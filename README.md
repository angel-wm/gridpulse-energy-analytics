# GridPulse — Cloud Energy Analytics Platform

GridPulse is a planned portfolio project focused on building a professional
cloud analytics platform for energy data.

The project is intended to demonstrate an end-to-end Analytics Engineering
workflow using BigQuery, dbt, SQL, Power BI, data quality practices,
Infrastructure as Code, and CI/CD.

The project is currently in **PRE-PROJECT** state. No implementation has
started and no dataset, architecture, data model, infrastructure, or dashboard
should be considered final yet.

For project context and task-specific reading guidance, see
[REPO_CONTEXT.md](REPO_CONTEXT.md).

## Intended direction

The current conceptual flow is:

    Energy data
        ↓
    ingestion
        ↓
    BigQuery raw layer
        ↓
    dbt staging
        ↓
    dbt intermediate
        ↓
    dbt analytical marts
        ↓
    Power BI

Terraform and GitHub Actions are intended to support reproducible
infrastructure and automated validation where technically justified.

The exact architecture will be finalized during Phase 0.

## Planned core stack

- Python
- SQL
- Google BigQuery
- dbt
- Jinja
- Power BI
- DAX
- Git
- GitHub
- GitHub Actions
- Terraform
- Data Quality
- Dimensional Modeling

Spark, Databricks, Snowflake, Kafka, and other technologies are not part of
the planned core architecture unless a future approved decision establishes
a concrete need for them.

## Project objective

The project should demonstrate the ability to turn raw cloud-hosted data into
reliable, tested, documented, business-ready analytical models and reporting.

The final project should be reproducible, understandable by another engineer,
and defensible during a technical interview.

## Status

Current state: **PRE-PROJECT**

Next planned work: **Phase 0 — Formal Project Design**

Implementation must not begin until Phase 0 is explicitly authorized.
