# GridPulse Project Specification

## Status

Specification status: **PROPOSED / PRE-PROJECT**

This document defines the currently intended project.

Requirements become implementation commitments only after Phase 0 review and
approval.

## Project purpose

GridPulse will be a professional Analytics Engineering and Business
Intelligence portfolio project centered on energy data.

The project should demonstrate how raw analytical data can be:

1. ingested into a cloud analytical platform;
2. organized into reliable layers;
3. transformed and modeled with dbt;
4. validated using automated data-quality tests;
5. optimized for analytical workloads;
6. exposed through business-ready marts;
7. consumed through Power BI;
8. supported by reproducible infrastructure and automated validation.

The project must resemble a realistic professional data platform rather than a
collection of disconnected technology demonstrations.

## Business domain

The domain is energy analytics.

The exact dataset and business scenario are intentionally **not yet selected**.

The final dataset should preferably support several of the following:

- energy consumption over time;
- meters, facilities, sites, regions, or customers;
- peak-demand analysis;
- consumption trends;
- cost or tariff analysis;
- operational efficiency;
- anomaly or unusual-consumption analysis;
- comparisons across locations or periods.

Weather, tariff, geographic, or other supplementary datasets may be introduced
only if they add meaningful analytical value.

## Intended users

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
- scalable SQL execution;
- analytical datasets;
- partitioning and clustering when justified;
- query-cost and performance analysis.

### dbt

Primary transformation and Analytics Engineering layer.

Expected responsibilities:

- sources;
- staging models;
- intermediate models;
- marts;
- dependency management with `ref()`;
- tests;
- documentation;
- lineage;
- reusable Jinja/macros when justified;
- incremental models where appropriate.

dbt should be a central technology in GridPulse rather than a superficial
addition.

### SQL

Primary analytical transformation language.

The project should exercise professional SQL patterns such as:

- CTEs;
- joins;
- aggregations;
- window functions;
- conditional logic;
- dimensional modeling queries;
- validation and reconciliation queries.

### Python

Python may support ingestion, source preparation, automation, or utilities when
a task is better solved outside SQL.

Python should not replace SQL or dbt where they are the natural tools.

### Power BI

Final business-consumption and visualization layer.

Expected responsibilities:

- semantic/reporting model;
- DAX measures where necessary;
- interactive analysis;
- business KPIs;
- final stakeholder-facing dashboard/report.

### Terraform

Infrastructure as Code for reproducible infrastructure where technically and
economically practical.

Terraform must not be included only to increase the technology count.

### GitHub Actions

CI/CD and automated validation where meaningful.

Potential responsibilities:

- SQL/dbt validation;
- dbt compile/test workflows;
- Python checks if Python is introduced;
- Terraform formatting/validation;
- repository quality checks.

## Explicit non-goals

The core project should NOT introduce technologies simply for portfolio breadth.

Unless an approved decision changes the architecture, the project will not use:

- Snowflake;
- Databricks;
- Apache Spark;
- Kafka;
- Kubernetes;
- Hadoop.

Those technologies belong to other portfolio projects where their use is
architecturally justified.

## Functional requirements

The completed project should provide:

- reproducible source ingestion;
- clearly separated raw and transformed data;
- dbt staging layer;
- business transformation layer;
- analytical marts;
- explicit data grain;
- documented dimensional or analytical model;
- automated data-quality checks;
- reconciliation between important layers;
- documented KPIs;
- Power BI report/dashboard;
- reproducible setup instructions;
- technical documentation;
- evidence of validation.

## Non-functional requirements

The project should prioritize:

- reproducibility;
- maintainability;
- modularity;
- traceability;
- testability;
- understandable naming;
- controlled cloud cost;
- documentation;
- version control;
- least unnecessary complexity.

## Cost constraint

The project should target zero or very low cost.

Before enabling any resource that may create charges:

1. identify the charging model;
2. explain the risk;
3. determine applicable free-tier or sandbox limits;
4. choose appropriate safeguards.

Cost-awareness is part of the learning objective.

## Learning objectives

GridPulse should provide meaningful practice with:

- BigQuery;
- GoogleSQL;
- partitioning;
- clustering;
- query optimization;
- cloud analytical architecture;
- dbt projects;
- dbt sources and refs;
- staging/intermediate/marts;
- Jinja;
- tests;
- documentation and lineage;
- incremental processing;
- dimensional modeling;
- data quality;
- Power BI;
- DAX;
- Terraform;
- CI/CD.

## Portfolio requirements

The final repository should communicate:

- the business problem;
- architecture;
- dataset;
- engineering decisions;
- data model;
- transformations;
- tests;
- infrastructure;
- CI/CD;
- analytical results;
- dashboard;
- limitations;
- reproducibility instructions.

A reviewer should be able to understand why each major technology exists.

## Definition of success

GridPulse is successful when:

- the complete analytical flow can be reproduced;
- important transformations are tested;
- final metrics reconcile with their upstream sources;
- architecture and decisions are documented;
- the Power BI output answers defined business questions;
- the repository provides sufficient technical evidence for portfolio review;
- the user can explain the architecture and implementation without relying on
  memorized descriptions generated by an assistant.

## Open questions for Phase 0

Phase 0 must resolve at least:

- Which energy dataset will be used?
- What is the dataset grain?
- What business scenario will the project represent?
- What KPIs and analytical questions matter?
- Is supplementary data justified?
- Which GCP project/account model will be used?
- Can the desired setup operate within free/sandbox constraints?
- How will ingestion occur?
- What BigQuery datasets/layers are required?
- What dimensional model is appropriate?
- Which infrastructure should be managed by Terraform?
- How will Power BI connect to the final analytical layer?
- What checks are required to close each implementation phase?
