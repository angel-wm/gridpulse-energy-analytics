# GridPulse — Cloud Energy Analytics Platform

GridPulse is a planned **Analytics Engineering + Business Intelligence** portfolio project for energy data.

It is designed to turn source energy data into tested, documented, business-ready analytical models using **BigQuery, dbt, SQL, Power BI, Terraform, and CI/CD; with an optional later Looker Studio experiment** where justified and feasible at **USD 0 actual charges**.

> **Current status:** Phase 1 — Repository and Cloud Foundation.
>
> The design uses EIA-930 for ERCO (Texas), 2023–2025. The project requires **USD 0 actual charges**.

For authoritative project context and task-specific reading guidance, start with [REPO_CONTEXT.md](REPO_CONTEXT.md).

## Why this project exists

GridPulse is the portfolio project focused on learning how a modern cloud analytics platform is designed and operated.

The project should demonstrate that the user can:

- work directly with BigQuery rather than treating it as an invisible dbt backend;
- build maintainable analytical models with dbt;
- define and validate business metrics;
- manage cost and data quality deliberately;
- expose curated models through Power BI;
- automate infrastructure and validation only where they add real value.

The final repository should be understandable by another engineer and defensible in a technical interview.

## Intended data flow

The current conceptual direction is:

    Energy source data
            ↓
    acquisition / ingestion
            ↓
       BigQuery raw
            ↓
       dbt staging
            ↓
    dbt intermediate
            ↓
        dbt marts
            ↓
         Power BI
            ↓
     Core release (Phase 8)

    Optional post-release (Phase 9):
    curated mart -> free CSV -> Looker Studio

Supporting concerns such as Terraform, GitHub Actions, security, cost control, and data quality apply across the flow.

See the [Phase 0 design baseline](docs/phase-0-design-baseline.md) for
the initial model and release scope.

## Planned technology roles

| Technology | Intended role |
| --- | --- |
| BigQuery | Primary cloud analytical warehouse |
| SQL / GoogleSQL | Core transformation and analytical language |
| dbt | Modular transformations, tests, documentation, lineage, and marts; select a compatible free local distribution before implementation |
| Python | Ingestion or utilities when SQL/dbt are not the natural tool |
| Power BI / DAX | Primary business-facing semantic and reporting layer; prefer Desktop/Import and assess PBIP versioning |
| Looker Studio (Data Studio) | **Optional Phase 9 after core release**, small dashboard via free bounded CSV export; requires separate authorization |
| Terraform | Reproducible cloud infrastructure where justified |
| GitHub Actions | Safe CI/CD and automated validation where justified |
| Git / GitHub | Version control, review, publication, and project handoff |

Docker is optional and has not been selected; see the [reproducibility tradeoff](PROJECT_SPEC.md#explicit-non-goals).

Spark, Databricks, Snowflake, Kafka, Airflow, Hadoop, and Kubernetes are not part of the planned core architecture unless a future approved decision establishes a real need.

## Current state

| Item | State |
| --- | --- |
| Project | Foundation in progress |
| Current phase | Phase 1 — Repository and Cloud Foundation |
| Last closed phase | Phase 0 — Formal Project Design |
| Next planned phase | Phase 2 — Source Acquisition, Ingestion and Raw Layer |
| Data source | [EIA-930](PROJECT_SPEC.md#business-domain), ERCO (Texas), 2023–2025 |
| Architecture | Design baseline with runtime verification gates |
| BigQuery resources | Not implemented |
| dbt project | Not implemented |
| Terraform / CI/CD | Not implemented; safe CI checks are planned early |
| Billing / charges | Zero billing authorized; USD 0 actual-charge requirement |
| Power BI | Not implemented |
| Looker Studio | Optional Phase 9, not begun; not required for core completion |

The [Phase 1 foundation runbook](docs/phase-1-foundation.md) covers the local
setup and the unbilled Sandbox gate. The [Phase 0 handoff](docs/handoffs/phase-0-to-1.md) records the local
validation and the remaining runtime checks for BigQuery Sandbox, dbt,
and Power BI. See the
[strict zero-billing gate](PROJECT_SPEC.md#cost-constraint--strict-zero-billing-gate)
and [phase rules](ROADMAP.md#phase-rules).

For the authoritative state, read [CURRENT_STATE.md](CURRENT_STATE.md).

## Where to read next

Use the document that matches your question:

| If you want to know... | Read |
| --- | --- |
| What is true right now? | [CURRENT_STATE.md](CURRENT_STATE.md) |
| What is this project supposed to become? | [PROJECT_SPEC.md](PROJECT_SPEC.md) |
| How is the system intended to work? | [ARCHITECTURE.md](ARCHITECTURE.md) |
| What phases are planned? | [ROADMAP.md](ROADMAP.md) |
| Why was a technical choice made? | [DECISIONS.md](DECISIONS.md) |
| How should an AI assistant work in this repo? | [AGENTS.md](AGENTS.md) |
| What should be loaded for a specific task? | [REPO_CONTEXT.md](REPO_CONTEXT.md) |

## Project documentation model

GridPulse uses the [AI Repository Context](REPO_CONTEXT.md) convention for cross-chat and cross-tool continuity.

The repository, not chat memory, is the durable source of truth.

The [GridPulse Jira project](https://angel231995.atlassian.net/browse/GRID)
tracks planned phase epics and tasks. The repository remains authoritative for
scope, decisions, phase state, authorization, and evidence. A Jira issue or
status does not start or close a phase; follow the [roadmap rules](ROADMAP.md#phase-rules).

Phase handoffs and validation evidence live under:

    docs/
    ├── handoffs/
    └── validation/

Repository documentation presentation follows the locally installed Repository Documentation Readability skill under:

    .agents/
    └── skills/
        └── repository-documentation-readability/

That guidance affects presentation only. GridPulse's own project semantics, authority rules, architecture, and lifecycle always take precedence.

## License

GridPulse's original code and documentation are available under the [MIT License](LICENSE).
Third-party datasets and materials remain subject to their own licenses and terms.
