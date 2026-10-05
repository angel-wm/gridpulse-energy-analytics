# GridPulse Decision Log

## Rules

This file records material project decisions.

Each decision must have:

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

When a decision changes, create a new decision and mark the old one
`SUPERSEDED`.

## D-001 — Use a phase-based work model

Status: **ACCEPTED**

### Context

GridPulse is expected to span multiple technical domains and multiple AI/chat
sessions.

### Decision

Use `phase` as the project's Work Unit.

State, plans, handoffs, and validation should be organized around explicit
phases.

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

---

## D-003 — Use dbt as the primary analytical transformation framework

Status: **ACCEPTED**

### Context

GridPulse is intended to specifically develop Analytics Engineering practices.

### Decision

dbt will be central to transformations after raw data reaches BigQuery.

### Rationale

The project should demonstrate modular SQL transformations, dependencies,
testing, documentation, lineage, and maintainable analytical modeling.

### Consequences

dbt should not be used merely as a thin wrapper around a few queries.

---

## D-004 — Use Power BI as the final business-consumption layer

Status: **ACCEPTED**

### Context

The project requires a stakeholder-facing analytical outcome.

### Decision

Power BI will consume curated analytical models and provide the final
interactive reporting experience.

### Rationale

Power BI complements the upstream Analytics Engineering workflow and is already
relevant to the broader portfolio.

### Consequences

Core transformation logic should remain upstream when appropriate instead of
being duplicated unnecessarily in DAX.

---

## D-005 — Avoid redundant data platforms in GridPulse

Status: **ACCEPTED**

### Context

Other portfolio projects are intended to cover Databricks, Snowflake, Spark,
Kafka, and related technologies.

### Decision

Do not add Snowflake, Databricks, Spark, Kafka, Hadoop, or Kubernetes to
GridPulse without a newly approved architectural need.

### Rationale

Portfolio breadth should come from justified architectures across projects,
not unnecessary complexity inside one project.

---

## D-006 — Include Terraform and GitHub Actions when justified

Status: **ACCEPTED**

### Context

Reproducibility and professional delivery practices are project goals.

### Decision

Terraform and GitHub Actions are planned components, but their exact scope must
be established after implementation requirements are understood.

### Rationale

Infrastructure as Code and CI/CD add professional value, but should not be
decorative.

### Consequences

Phase 0 must define intended roles.

Later phases must validate that cost and security constraints permit them.

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

Routine state must remain in its authoritative source rather than being copied
into the context map.
