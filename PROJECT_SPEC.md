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
8. consumed through a single business-facing Power BI deliverable;
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

The local **free dbt distribution** remains to be chosen in Phase 0 / Phase 3
after checking current adapter support and compatibility. As of September 2026,
dbt Labs distinguishes free local `dbt` (formerly Fusion) from the fully
open-source `dbt OSS` (formerly Core v2); older Core v1 terminology must not
silently dictate the choice. No paid dbt subscription or add-on is required.

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
- primary and sole Power BI report/dashboard, reproducible without paid sharing or a required Google Cloud billing account;
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
The current authorization covers documentation decisions only; it does not
authorize cloud implementation, account upgrades, billing activation, trials,
subscriptions, chargeable resources, or chargeable workloads.

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

Phase 0 must demonstrate that the chosen dataset, raw/staging/marts footprint,
refresh/rebuild approach, dbt materializations, CI execution, the sole Power BI
report, and any proposed Terraform/IAM resources can work with no billing
account. Do not assume a live BigQuery-to-Power BI connector works without
billing; evaluate a documented, reproducible bounded export/Import workflow
if required.
If a desired function requires billing, do not enable it: use a valid free
alternative, reduce scope, or explicitly record the blocker/deferred capability.

Where supported, additionally use dry runs/query estimates, conservative
maximum-bytes-billed settings, bounded test inputs, partition-pruned queries
and query quotas. These are **defense-in-depth controls**, not permission to
activate billing. Alerts and budgets do not by themselves prove a USD 0 cap.
Any change to this strict constraint requires a separate explicit user
decision; simply authorizing project work is insufficient.

Primary references:
https://docs.cloud.google.com/bigquery/docs/sandbox
https://cloud.google.com/bigquery/pricing
https://docs.cloud.google.com/bigquery/docs/best-practices-costs

## Dataset-dependent storage optimization

**No materialization optimization is chosen yet.** When Phase 0 selects
the dataset, estimate the total *and cumulative* Sandbox storage cost of
raw source-aligned data, staging, intermediate artifacts, marts, experiments,
replacement/reloads and headroom. The 10 GiB Sandbox limit is **lifetime** and
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

Phase 0 should document a capacity estimate and rationale; later phases
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
- Power BI delivery has an evidenced free data path, or a blocker is explicitly documented without enabling billing;
- actual cloud/service charges for the project remain USD 0;
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
- What cumulative Sandbox storage will source loads, model materializations and planned rebuilds consume?
- Which layers should be views, ephemeral models or persisted tables after dataset sizing, and what does each choice do to query scans?
- What dimensional or analytical model is appropriate?
- What should be learned natively in BigQuery before dbt abstracts it?
- Which dbt materializations are likely appropriate?
- Which resources should Terraform manage?
- What GitHub Actions workflows are safe and useful?
- How will Power BI connect to the curated layer and how will PBIP/Import be validated without paid licensing?
- Can Power BI consume BigQuery outputs without a GCP billing account, potentially via a reproducible bounded export and Power BI Desktop Import?
- Which local free dbt distribution and version work with the adapter and Sandbox constraints?
- How will Sandbox 60-day expiry and non-DML restrictions be handled and documented?
- Can OIDC/Workload Identity Federation be configured in the zero-billing environment, or must cloud CI be deferred?
- What validation and closure criteria apply to every later phase?
