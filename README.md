# GridPulse — Cloud Energy Analytics Platform

GridPulse is a planned **Analytics Engineering + Business Intelligence** portfolio project for energy data.

It is designed to turn source energy data into tested, documented, business-ready analytical models using **BigQuery, dbt, SQL, Power BI, Terraform, and CI/CD** where those technologies are justified.

> **Current status:** PRE-PROJECT.  
> No dataset, cloud resources, dbt project, data model, infrastructure, CI workflow, or Power BI report is implemented yet.

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

Supporting concerns such as Terraform, GitHub Actions, security, cost control, and data quality apply across the flow.

The exact design remains subject to Phase 0 approval.

## Planned technology roles

| Technology | Intended role |
| --- | --- |
| BigQuery | Primary cloud analytical warehouse |
| SQL / GoogleSQL | Core transformation and analytical language |
| dbt | Modular transformations, tests, documentation, lineage, and marts |
| Python | Ingestion or utilities when SQL/dbt are not the natural tool |
| Power BI / DAX | Business-facing semantic and reporting layer |
| Terraform | Reproducible cloud infrastructure where justified |
| GitHub Actions | Safe CI/CD and automated validation where justified |
| Git / GitHub | Version control, review, publication, and project handoff |

Spark, Databricks, Snowflake, Kafka, Airflow, Hadoop, and Kubernetes are not part of the planned core architecture unless a future approved decision establishes a real need.

## Current state

| Item | State |
| --- | --- |
| Project | PRE-PROJECT |
| Current phase | None |
| Next planned phase | Phase 0 — Formal Project Design |
| Dataset | Not selected |
| Architecture | Intended only; not approved for implementation |
| BigQuery resources | Not implemented |
| dbt project | Not implemented |
| Terraform / CI/CD | Not implemented |
| Power BI | Not implemented |

Implementation must not begin until Phase 0 is explicitly authorized.

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

Phase handoffs and validation evidence live under:

    docs/
    ├── handoffs/
    └── validation/

Repository documentation presentation follows the locally installed Repository Documentation Readability skill under:

    .agents/
    └── skills/
        └── repository-documentation-readability/

That guidance affects presentation only. GridPulse's own project semantics, authority rules, architecture, and lifecycle always take precedence.
