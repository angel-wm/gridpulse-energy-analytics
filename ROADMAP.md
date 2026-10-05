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
5. affected authoritative documents are updated;
6. CURRENT_STATE is updated;
7. required repository changes are committed;
8. publication requirements for that phase are satisfied.

A local commit alone does not prove publication.

Do not automatically start the next phase after closing one.

Material scope/architecture changes must be recorded in DECISIONS.md before
the affected implementation proceeds.

## Plan

| Phase | Name | Primary scope | Dependency |
| --- | --- | --- | --- |
| 0 | Formal Project Design | Select dataset/source, business problem, stakeholders, KPIs, requirements, architecture, cost constraints, modeling strategy, Terraform/CI goals, and phase acceptance criteria | None |
| 1 | Repository and Cloud Foundation | Finalize implementation repository structure; establish GCP project strategy, BigQuery foundation, authentication, environment conventions, Terraform foundation for approved resources, and reproducible local setup | Phase 0 closed |
| 2 | Source Acquisition, Ingestion and Raw Layer | Acquire data reproducibly; implement ingestion; load BigQuery raw/source-aligned data; preserve traceability; profile schema/volume; validate source-to-load reconciliation | Phase 1 closed |
| 3 | BigQuery Native Analytics and dbt Foundation | Exercise native BigQuery querying/modeling concepts; configure dbt; declare sources; establish staging conventions and initial tests without hiding warehouse fundamentals | Phase 2 closed |
| 4 | Analytical Modeling | Build staging/intermediate/marts as approved; dimensional or equivalent analytical model; facts/dimensions; reusable metric logic; appropriate materializations | Phase 3 closed |
| 5 | Data Quality, Documentation and Performance | Expand dbt tests, business-rule tests, reconciliation, dbt docs/lineage, partitioning/clustering, query optimization, incremental processing if justified, and cost analysis | Phase 4 closed |
| 6 | Power BI Analytics | Build final semantic/reporting layer, DAX where appropriate, dashboard/report pages, interactions, KPI presentation, and documented business insights | Phase 5 closed |
| 7 | CI/CD and Infrastructure Hardening | Complete/expand Terraform for justified resources; implement safe GitHub Actions workflows for dbt, Terraform and other applicable checks; document environment/security approach | Phase 6 closed |
| 8 | Final Validation and Portfolio Release | Reproduce end-to-end workflow, audit documentation and decisions, validate architecture, finalize README/screenshots, record limitations/costs, and produce release-quality handoff | Phase 7 closed |

## Phase 0 — Formal Project Design

### Goals

- choose and justify the dataset/source;
- define the business scenario;
- establish primary stakeholders/personas;
- define analytical questions and KPIs;
- inspect source characteristics;
- establish source and analytical grain;
- decide ingestion approach;
- determine GCP/free-tier constraints;
- design logical and physical BigQuery layer responsibilities;
- define which BigQuery concepts must be learned natively;
- design dbt layer responsibilities;
- propose the final analytical/dimensional model;
- define Power BI analytical requirements;
- confirm cost controls;
- identify Terraform scope;
- define safe CI/CD goals;
- define data-quality/reconciliation strategy;
- define acceptance criteria for later phases.

### Phase 0 expected outputs

At minimum:

- approved PROJECT_SPEC;
- approved intended ARCHITECTURE;
- dataset/source selection;
- business questions and KPI definitions;
- initial data model decision;
- major tooling decisions recorded;
- reviewed roadmap;
- explicit cost/security constraints;
- validation criteria for Phase 0;
- Phase 0 validation record;
- Phase 0 handoff;
- CURRENT_STATE update.

### Exit criteria

Phase 0 cannot close until:

- PROJECT_SPEC reflects approved scope;
- ARCHITECTURE contains an approved intended design;
- dataset/source and business problem are confirmed;
- key architecture/tool decisions are recorded;
- later roadmap phases are reviewed and corrected if required;
- Phase 0 validation record exists and supports closure;
- Phase 0 handoff exists;
- CURRENT_STATE identifies Phase 0 as closed;
- the phase's coherent documentation state is published as required.

## Phase evolution

The roadmap is intentionally high-level before Phase 0.

Phase 0 is expected to refine later phase names, boundaries, deliverables, and
exit criteria.

Changing future phases is allowed when justified and recorded.

Removing a technology because it is not justified is preferable to keeping it
only for portfolio breadth.
