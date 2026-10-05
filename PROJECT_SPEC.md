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

1. acquired or generated reproducibly;
2. ingested into a cloud analytical platform;
3. organized into reliable warehouse layers;
4. transformed and modeled with dbt;
5. validated through automated data-quality checks;
6. optimized for analytical workloads and cost;
7. exposed through business-ready marts;
8. consumed through Power BI;
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
- Power BI consumption of curated warehouse models;
- Terraform and CI/CD where they naturally support the platform.

Other portfolio projects are intended to cover Spark/Databricks, Snowflake,
Airflow, Kafka, streaming, and related architectures. GridPulse must not absorb
those technologies without a real architectural requirement.

## Business domain

The domain is energy analytics.

The exact dataset and business scenario are intentionally **not yet selected**.

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
- Power BI report/dashboard;
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

## Cost constraint

The project should target zero or very low cost.

Before enabling a resource that may create charges:

1. identify the charging model;
2. explain the risk;
3. determine relevant free-tier/sandbox limits;
4. choose safeguards;
5. prefer bounded test data and query patterns while learning.

Cost-awareness is part of the engineering objective.

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
- infrastructure and automation are reproducible where included;
- the repository provides sufficient evidence for technical portfolio review;
- the user can explain and defend the system without relying on memorized
  assistant-generated descriptions.

## Open questions for Phase 0

Phase 0 must resolve at least:

- Which energy dataset/source will be used?
- What business story will GridPulse represent?
- What is the source grain?
- What is the analytical grain?
- Which users/personas matter?
- Which business questions and KPIs matter?
- Is supplementary data justified?
- Which GCP project/account approach will be used?
- What BigQuery free-tier/sandbox constraints apply?
- How will ingestion occur?
- Are Cloud Storage or other GCP resources needed?
- What BigQuery datasets/layers are required?
- What dimensional or analytical model is appropriate?
- What should be learned natively in BigQuery before dbt abstracts it?
- Which dbt materializations are likely appropriate?
- Which resources should Terraform manage?
- What GitHub Actions workflows are safe and useful?
- How will Power BI connect to the curated layer?
- What validation and closure criteria apply to every later phase?
