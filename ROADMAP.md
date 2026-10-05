# GridPulse Roadmap

## Phase rules

The native Work Unit for GridPulse is a **phase**.

Allowed phase states:

- `planned`
- `current`
- `closed`

A phase may start only after:

1. explicit user authorization;
2. all required predecessor phases are closed;
3. required predecessor handoff information is available.

A roadmap entry does NOT authorize execution.

A phase closes only when:

1. its required scope is completed;
2. exit checks have been performed;
3. results are recorded in a phase validation record;
4. a phase handoff/closeout has been written;
5. CURRENT_STATE is updated;
6. required repository changes are committed;
7. publication requirements for that phase are satisfied.

A local commit alone does not prove publication.

Do not automatically start the next phase after closing one.

Material scope changes must be recorded in DECISIONS.md before the affected
implementation proceeds.

## Plan

| Phase | Name | Primary scope | Dependency |
| --- | --- | --- | --- |
| 0 | Formal Project Design | Select dataset, business problem, KPIs, requirements, architecture, cost constraints, model strategy, and acceptance criteria | None |
| 1 | Repository and Cloud Foundation | Establish implementation repository structure, development conventions, GCP/BigQuery foundation, credentials strategy, and reproducible setup | Phase 0 closed |
| 2 | Ingestion and Raw BigQuery Layer | Acquire source data reproducibly, load raw data, preserve source traceability, profile volume/schema, and validate ingestion | Phase 1 closed |
| 3 | dbt Foundation and Staging | Configure dbt, declare sources, create staging models, standardize fields/types, and establish first dbt tests | Phase 2 closed |
| 4 | Analytical Modeling | Build intermediate transformations, dimensional/analytical model, facts/dimensions or equivalent marts, and business metrics | Phase 3 closed |
| 5 | Data Quality and Performance | Expand tests, reconciliation, documentation, lineage, partitioning/clustering, query optimization, and cost analysis | Phase 4 closed |
| 6 | Power BI Analytics | Build final semantic/reporting layer, DAX measures, dashboard pages, interactions, and business insights | Phase 5 closed |
| 7 | Infrastructure and Delivery Automation | Codify justified infrastructure with Terraform and implement appropriate GitHub Actions CI/CD/validation workflows | Phase 6 closed |
| 8 | Final Validation and Portfolio Release | End-to-end reproduction, documentation review, architecture review, screenshots, README finalization, limitations, and release-quality handoff | Phase 7 closed |

## Phase 0 — Formal Project Design

### Goals

- choose and justify the dataset;
- define the business scenario;
- establish primary stakeholders;
- define business questions and KPIs;
- inspect data characteristics;
- establish data grain;
- decide ingestion approach;
- design logical BigQuery layers;
- design dbt layer responsibilities;
- propose final analytical model;
- define Power BI analytical requirements;
- confirm cost controls;
- identify Terraform scope;
- define CI/CD goals;
- establish acceptance criteria for later phases.

### Exit criteria

Phase 0 cannot close until:

- PROJECT_SPEC reflects approved scope;
- ARCHITECTURE contains an approved intended design;
- key design decisions are recorded;
- dataset and business problem are confirmed;
- later roadmap phases are reviewed and updated if necessary;
- Phase 0 validation record exists;
- Phase 0 handoff exists;
- CURRENT_STATE identifies Phase 0 as closed.

## Phase evolution

The roadmap is expected to become more precise during Phase 0.

Changing future phase details is allowed when justified and recorded.

Removing a technology because it is not justified is preferable to keeping it
only for portfolio breadth.
