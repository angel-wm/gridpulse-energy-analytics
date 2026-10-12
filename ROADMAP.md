# GridPulse Roadmap

## Phase rules

The native Work Unit for GridPulse is a **phase**.

Allowed phase states:

- `planned`
- `current`
- `closed`

A roadmap entry records planned work. It does **not** authorize execution.

### Start a phase

A phase may start only when:

1. the user explicitly authorizes it;
2. all required predecessor phases are closed;
3. required predecessor handoff information is available.

### Close a phase

A phase closes only when:

1. required scope is complete;
2. exit checks have been performed;
3. results are recorded in a phase validation record;
4. a phase handoff/closeout exists;
5. affected authoritative documents are updated;
6. CURRENT_STATE is updated;
7. required repository changes are committed;
8. publication requirements are satisfied.

A local commit alone does not prove publication.

Do not automatically start the next phase after closing one.

Material scope or architecture changes must be recorded in DECISIONS.md before the affected implementation proceeds.

**Strict cost gate:** Documentation changes are not authorization to begin a phase, enable cloud billing, start paid trials/subscriptions, provision potentially billable resources, or execute cloud workloads. The target is USD 0 actual charges, not merely low cost. If a feature is incompatible with an unbilled environment, propose a free workaround, defer it, or seek separate explicit approval for a revised constraint; never enable billing by assumption. Check PROJECT_SPEC cost and authentication gates before any future cloud work.

## Phase overview

| Phase | Name | Main outcome | Dependency |
| --- | --- | --- | --- |
| 0 | Formal Project Design | Approved source, business problem, architecture, model strategy, strict zero-billing feasibility, and acceptance criteria | None |
| 1 | Repository and Cloud Foundation | Reproducible local foundation, assessed BigQuery Sandbox, authentication design, basic no-cloud-cost CI checks, and Terraform scope where justified | Phase 0 closed |
| 2 | Source Acquisition, Ingestion and Raw Layer | Reproducible acquisition and source-aligned raw data with ingestion checks and source/load reconciliation | Phase 1 closed |
| 3 | BigQuery Native Analytics and dbt Foundation | Native BigQuery practice, verified free local dbt distribution, sources/staging, initial tests, and safe dbt CI checks | Phase 2 closed |
| 4 | Analytical Modeling | Justified staging/intermediate/marts, dimension or equivalent models, tested metrics, and ongoing CI validation | Phase 3 closed |
| 5 | Data Quality, Documentation and Performance | Deeper tests, reconciliation, dbt docs/lineage, cost review, and evidence-based optimization | Phase 4 closed |
| 6 | Business Intelligence: Power BI + Looker Studio | Full primary Power BI report, compact complementary Looker Studio report, aligned KPIs, and documented insights without new charges | Phase 5 closed |
| 7 | CI/CD and Infrastructure Hardening | Harden existing safe automation, Terraform scope, least-privilege identity, and environment/security practices | Phase 6 closed |
| 8 | Final Validation and Portfolio Release | Reproducible end-to-end release with complete portfolio documentation, evidence, and verified zero spend | Phase 7 closed |

## Phase 0 — Formal Project Design

Phase 0 defines what GridPulse will actually build. It is a design phase, not an implementation shortcut.

### Goals

- choose and justify the dataset/source;
- define the business scenario and stakeholders;
- define analytical questions and KPIs;
- establish source and analytical grain;
- decide the ingestion approach;
- establish a no-billing, USD 0 cost plan; verify BigQuery Sandbox lifetime storage, monthly query allowance, automatic expiry, and feature limitations;
- identify free alternatives or deferrals for features that require a billing account (including direct Looker Studio-to-BigQuery connection);
- design BigQuery layer responsibilities;
- define which BigQuery concepts must be learned natively;
- define dbt layer responsibilities;
- propose the analytical/dimensional model;
- define Power BI as the primary BI deliverable and a smaller complementary Looker Studio deliverable, with validated no-charge data access for both;
- assess Power BI Desktop/Import and text-based PBIP versioning, without assuming paid sharing features;
- establish cost controls;
- identify Terraform scope;
- define safe CI/CD goals, including early static/local checks and cloud-free PR validation;
- select a free local dbt distribution only after confirming BigQuery adapter compatibility and required features;
- design least-privilege authentication and assess GitHub OIDC/Workload Identity Federation feasibility;
- define data-quality and reconciliation strategy;
- define acceptance criteria for later phases.

### Expected outputs

Phase 0 should produce, at minimum:

- approved PROJECT_SPEC;
- approved intended ARCHITECTURE;
- selected dataset/source;
- business questions and KPI definitions;
- initial data-model decision;
- recorded major tooling decisions;
- reviewed roadmap;
- explicit no-billing / zero-spend feasibility decision, alternatives for unsupported features, and least-privilege security constraints;
- Phase 0 validation criteria and record;
- Phase 0 handoff;
- updated CURRENT_STATE.

### Exit criteria

Phase 0 cannot close until:

- PROJECT_SPEC reflects approved scope;
- ARCHITECTURE reflects an approved intended design;
- dataset/source and business problem are confirmed;
- USD 0 operating plan is feasible without enabling billing, or blockers and deferred capabilities are explicitly documented;
- key architecture/tool decisions are recorded;
- later roadmap phases have been reviewed and corrected where required;
- Phase 0 validation supports closure;
- a Phase 0 handoff exists;
- CURRENT_STATE identifies Phase 0 as closed;
- the coherent Phase 0 documentation state is published as required.

## How the roadmap may evolve

This roadmap is intentionally high-level before Phase 0.

Phase 0 may refine later phase names, boundaries, deliverables, and exit criteria.

Removing a technology because it is not justified is preferable to keeping it only for portfolio breadth.
