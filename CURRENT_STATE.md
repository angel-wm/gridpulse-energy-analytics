# Current State

## State

Project state: **PRE-PROJECT**

Current phase: **None**

Last closed phase: **None**

Next planned phase:
**Phase 0 — Formal Project Design**

Implementation status:
**Not started**

Published implementation:
**None**

Repository context status:
**Bootstrap documentation is published on the canonical GitHub repository.**

The published documentation describes intended work only. No cloud resources,
datasets, pipelines, dbt project, Terraform-managed infrastructure, CI/CD
workflow, or Power BI report should be inferred from repository publication.

## What is confirmed

The following project direction has been approved at a conceptual level:

- project name: GridPulse;
- orientation: Analytics Engineering + cloud BI;
- domain: energy analytics;
- primary warehouse: BigQuery;
- primary transformation framework: dbt;
- SQL is the primary transformation language;
- Python may support ingestion or utilities when justified;
- sole BI reporting layer: Power BI (Desktop/Import-first where appropriate, with PBIP considered for reproducibility);
- Terraform and GitHub Actions should be used where technically justified;
- the GridPulse cost constraint is now strict USD 0 actual charges, with an unbilled BigQuery Sandbox-first design; no billing activation or paid cloud services are authorized;
- safe CI and data-quality controls should begin incrementally in early phases rather than be postponed to the hardening phase;
- if cloud-connected GitHub Actions later becomes necessary, prefer OIDC with Workload Identity Federation when feasible and compliant with zero billing;
- dbt must be central without hiding important native BigQuery concepts;
- the project should follow a phase-based work model;
- the repository should act as the durable source of truth between AI chats,
  tools, and project phases;
- implementation should be learning-first: the user must understand and be
  able to explain what is built.

These confirmations do not mean any implementation exists.

## What is not yet confirmed

Still unresolved:

- dataset and acquisition method;
- business scenario;
- stakeholder personas;
- analytical questions and KPIs;
- source and analytical grain;
- supplementary datasets, if any;
- ingestion mechanism;
- GCP project/account setup;
- BigQuery Sandbox/free-tier feasibility;
- physical BigQuery datasets and naming;
- dimensional or alternative analytical model;
- partition strategy;
- clustering strategy;
- selection and compatibility verification of a free local dbt distribution (current dbt v2 / dbt OSS terminology);
- materialization and incremental-model strategy;
- Power BI semantic model and report structure;
- whether the entire desired BigQuery/dbt design is compatible with Sandbox no-DML, cumulative lifetime storage, and 60-day expiry;
- reproducible Power BI delivery without paid service sharing or mandatory GCP billing;
- dataset-dependent capacity estimate for cumulative Sandbox storage, duplicated layers, model materializations and rebuilds;
- exact Terraform scope;
- exact GitHub Actions / CI/CD workflow;
- phase-specific acceptance criteria beyond the current high-level roadmap.

These must be resolved through Phase 0 or later authorized design decisions.

## Current authorization

No implementation phase is authorized.

The user explicitly authorized **documentation-level** updates to the roadmap, authentication requirements, strict zero-charge controls and BI scope. Decision D-016 supersedes D-012: Power BI is the only planned BI deliverable; Looker Studio is removed. Decision D-017 defers selection of storage/materialization optimizations until the dataset is chosen and sized. These approvals do **not** start Phase 0 and do **not** authorize enabling billing, subscribing to paid products, creating cloud infrastructure, or executing cloud work.

When the user explicitly chooses to begin GridPulse, the authorized next work
is **Phase 0 — Formal Project Design**.

Phase 0 is a design phase. It must not silently create production resources or
begin implementation merely because technologies appear in the roadmap.

Do not automatically start Phase 1 after Phase 0 closes.

## Resume instructions

When resuming GridPulse:

1. read REPO_CONTEXT.md;
2. read this state;
3. identify whether the task is state, planning, education/debugging,
   architecture, implementation, review, or history;
4. if planning to begin, read ROADMAP Phase 0 rules and scope;
5. read PROJECT_SPEC and only the additional sources required by the task;
6. perform only explicitly authorized work.

## Next handoff

No phase handoff exists because no phase has been completed.

The updated published planning documents are not phase completion evidence.
