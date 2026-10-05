# GridPulse Decision Log

## Rules

This file records material project decisions.

Each decision should include:

- ID;
- status;
- context;
- decision;
- rationale;
- consequences;
- supersession reference when applicable.

Decision statuses:

- `PROPOSED`
- `ACCEPTED`
- `SUPERSEDED`
- `REJECTED`

Do not silently overwrite historical decisions.

When an accepted decision materially changes, create a new decision and mark
the old one `SUPERSEDED`.

## D-001 — Use a phase-based work model

Status: **ACCEPTED**

### Context

GridPulse is expected to span multiple technical domains and multiple AI/chat
sessions.

### Decision

Use `phase` as the project's Work Unit.

State, plans, handoffs, and validation are organized around explicit phases.

### Rationale

This provides bounded work, clearer handoff, controlled context loading, and
prevents a long conversation from becoming the only source of project state.

### Consequences

ROADMAP defines phase rules and order.

CURRENT_STATE identifies active and completed phases.

Closed phases receive handoff and validation records.

---

## D-002 — Use BigQuery as the primary analytical warehouse

Status: **ACCEPTED**

### Context

GridPulse is intended to develop cloud Analytics Engineering skills while
leveraging existing SQL knowledge.

### Decision

BigQuery is the primary analytical warehouse for GridPulse.

### Rationale

It provides a natural transition from relational SQL into cloud analytics and
supports the intended project focus without introducing an unnecessary second
warehouse.

### Consequences

Snowflake is not part of the core GridPulse architecture.

BigQuery-native concepts must be learned and demonstrated.

---

## D-003 — Use dbt as the primary analytical transformation framework

Status: **ACCEPTED**

### Context

GridPulse is intended to specifically develop Analytics Engineering practices.

### Decision

dbt will be central to transformations after source/raw data reaches BigQuery.

### Rationale

The project should demonstrate modular SQL transformations, dependencies,
testing, documentation, lineage, and maintainable analytical modeling.

### Consequences

dbt should not be used merely as a thin wrapper around a few queries.

Its abstractions must not prevent learning the underlying BigQuery behavior.

---

## D-004 — Use Power BI as the final business-consumption layer

Status: **ACCEPTED**

### Context

The project requires a stakeholder-facing analytical outcome.

### Decision

Power BI will consume curated analytical models and provide the final
interactive reporting experience.

### Rationale

Power BI complements the upstream Analytics Engineering workflow and fits the
broader portfolio.

### Consequences

Reusable transformation logic should remain upstream when appropriate instead
of being duplicated unnecessarily in DAX.

---

## D-005 — Avoid redundant data platforms in GridPulse

Status: **ACCEPTED**

### Context

Other portfolio projects are intended to cover Databricks, Snowflake, Spark,
Kafka, Airflow, and related technologies.

### Decision

Do not add Snowflake, Databricks, Spark, Kafka, Airflow, Hadoop, Kubernetes, or
similar platforms to GridPulse without a newly approved architectural need.

### Rationale

Portfolio breadth should come from justified architectures across projects,
not unnecessary complexity inside one project.

### Consequences

GridPulse remains focused on BigQuery + dbt + Power BI and supporting
engineering practices.

---

## D-006 — Include Terraform and GitHub Actions when justified

Status: **ACCEPTED**

### Context

Reproducibility and professional delivery practices are project goals.

### Decision

Terraform and GitHub Actions are planned components, but their exact scope must
follow actual implementation requirements.

### Rationale

Infrastructure as Code and CI/CD add professional and educational value but
should not be decorative.

### Consequences

Phase 0 defines intended roles.

Terraform may begin in the foundation phase for approved resources.

Later phases harden infrastructure and CI/CD practices.

Cost and security constraints must be considered before cloud automation.

---

## D-007 — Use AI Repository Context convention 0.1

Status: **ACCEPTED**

### Context

The project will be worked across multiple chats, tools, and potentially long
periods of time.

### Decision

Adopt root-level REPO_CONTEXT.md following AI Repository Context convention
version 0.1.

### Rationale

The repository should remain the durable context source rather than relying
only on AI memory or chat history.

### Consequences

README exposes REPO_CONTEXT.

REPO_CONTEXT maps authority and task-specific loading rules.

Routine state remains in its authoritative source rather than being copied into
the context map.

---

## D-008 — Learn native BigQuery concepts before relying on dbt abstractions

Status: **ACCEPTED**

### Context

dbt can make warehouse transformation workflows easier to manage, but an
Analytics Engineering portfolio project should also demonstrate understanding
of the underlying warehouse.

### Decision

When GridPulse introduces a BigQuery concept that dbt later abstracts, the user
should first or concurrently understand and practice the relevant native
BigQuery behavior.

### Rationale

The goal is not merely to produce a dbt project. The user should be able to
reason about data storage, SQL execution, partitioning, clustering, query cost,
loading, and materialization independently of dbt.

### Consequences

The roadmap includes native BigQuery work before/alongside the dbt foundation.

dbt remains central but does not replace warehouse understanding.

---

## D-009 — Use a learning-first implementation approach

Status: **ACCEPTED**

### Context

GridPulse is both a professional portfolio project and a structured learning
project.

### Decision

Implementation should progress incrementally, with important concepts explained
and validated rather than maximizing delivery speed.

### Rationale

The finished portfolio has limited value if the user cannot explain or defend
the architecture and implementation.

### Consequences

Important new concepts should include purpose, context, alternatives, and
tradeoffs.

Large unexplained code/configuration dumps should be avoided where incremental
work is practical.

Validation evidence is required before implementation is described as working.

---

## D-010 — Keep repository sources authoritative across chats

Status: **ACCEPTED**

### Context

GridPulse may use separate chats for planning, implementation phases,
education, debugging, and review.

### Decision

Repository documentation mapped by REPO_CONTEXT is the durable project source
of truth. Chat history and Project memory are secondary context.

### Rationale

This prevents loss of continuity and conflicting project state across long or
separate conversations.

### Consequences

A new stateful chat should reconstruct context from REPO_CONTEXT and
CURRENT_STATE.

Educational/debugging discussions do not automatically update official state.

Material approved changes must be written back to the appropriate repository
source.
