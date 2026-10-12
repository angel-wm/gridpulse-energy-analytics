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


---

## D-011 — Adopt repository documentation readability guidance

Status: **ACCEPTED**

### Context

GridPulse documentation is used by human readers, AI assistants, and coding
agents across long-running project phases. The repository already separates
state, architecture, roadmap, decisions, and evidence, but presentation quality
should remain consistent as those documents grow.

### Decision

Install and use the Repository Documentation Readability skill under
`.agents/skills/repository-documentation-readability/` for documentation work.

The guidance applies to presentation: reader intent, progressive disclosure,
representation choice, scanning, mobile readability, descriptive links, and
documentation-set coherence.

### Rationale

The goal is to reduce reader effort without weakening technical precision or
duplicating authoritative project information.

### Consequences

- README remains an entry point rather than the full documentation system.
- Project-native contracts and the authority defined in REPO_CONTEXT always
  take precedence.
- Documentation changes should use the simplest useful representation.
- Essential meaning must remain understandable in source-readable Markdown.
- Future documentation work should consult the installed skill and load deeper
  references only when needed.

---

## D-012 — Keep Power BI primary and add complementary Looker Studio

Status: **ACCEPTED**

### Context

The portfolio should show strong Power BI/DAX skills and some experience with the Google BI ecosystem without producing two redundant large dashboards or enabling paid services.

### Decision

Keep Power BI as the primary, complete business-facing BI deliverable. Add a smaller Looker Studio (also branded Data Studio) companion report on a deliberately aligned subset of approved KPIs. Compare tools in the final portfolio documentation.

Use a free, reproducible data-delivery path. Direct Looker Studio -> BigQuery connectivity is **not assumed feasible without a billing account** and must not be enabled if it requires billing. Never introduce Looker enterprise, paid Looker Studio Pro, or paid Power BI sharing as a hidden dependency.

### Rationale

Two purposefully scoped BI clients demonstrate versatility while keeping metric logic centralized upstream and preventing duplicate modeling work.

### Consequences

PROJECT_SPEC, ARCHITECTURE, ROADMAP, and BI success criteria include both reports. Phase 0 resolves the exact no-charge Looker Studio data source and verifies any Power BI license constraints. Prefer Power BI Desktop with Import for initial development and evaluate PBIP versioning.

---

## D-013 — Require zero billing, not just low expected usage

Status: **ACCEPTED**

### Context

The user explicitly requires avoiding any monetary charges from GridPulse and does not authorize enabling a cloud billing account or paid services for implementation.

### Decision

Target **USD 0 actual cost**, with a no-billing approach first. BigQuery Sandbox is the default feasibility candidate, subject to its constraints and the approved dataset. Storage and query allowances alone do not guarantee zero cost in a billing-enabled project.

Never activate or link billing, start a paid trial/subscription, create potentially billable resources, or run cloud workloads without separate explicit authorization for that action. If zero-charge feasibility fails, document the blocker and prefer a free workaround, reduced scope, or deferred feature rather than silently relaxing the requirement.

### Rationale

A cloud project can incur charges through services or operations outside BigQuery query/storage free quotas, and budgets/alerts are not a substitute for an unbilled environment.

### Consequences

Phase 0 must check current provider pricing, account prerequisites, Sandbox restrictions (including no DML/streaming and 60-day object expiry), ingestion and incremental dbt feasibility, BI connectivity, Terraform/IAM availability, and safe CI. Record operational safeguards such as query estimates/dry runs, explicit query byte limits where supported, small bounded test datasets, and repeatable rehydration after Sandbox expiry. Do not describe the Sandbox 10 GiB lifetime allocation as a renewable monthly quota.

---

## D-014 — Shift data quality and safe CI earlier

Status: **ACCEPTED**

### Context

Placing most data quality work in Phase 5 and CI/CD development in Phase 7 would delay feedback on foundational defects.

### Decision

Introduce no-cloud-cost repository/static checks in Phase 1; ingestion validation and reconciliation in Phase 2; dbt tests and safe CI checks starting in Phase 3; and business metric tests during analytical modeling. Phase 5 deepens quality and performance evidence, while Phase 7 hardens the already-existing automation.

### Rationale

Early tests reduce the cost of defects and provide a better learning progression.

### Consequences

Revise the ROADMAP outcome and Phase 0 acceptance design without interpreting this documentation decision as implementation authorization. Cloud-executing CI remains disabled unless separate feasibility, cost, and phase authorization are confirmed.

---

## D-015 — Prefer keyless, least-privilege GitHub-to-GCP authentication

Status: **ACCEPTED**

### Context

The intended Terraform/dbt CI architecture may eventually require GitHub Actions to access Google Cloud. Static service-account JSON keys create avoidable long-lived credential risk.

### Decision

Prefer GitHub Actions OIDC with Google Cloud Workload Identity Federation where supported, necessary, and compatible with the no-billing environment. Follow least privilege and restrict workload identity claims to the correct repository/ref/environment. Do not commit service-account keys or create a cloud workload just to demonstrate identity federation.

If federation is not feasible under a no-billing account, prefer local-only CI and document the limitation; do not bypass the USD 0 gate.

### Rationale

Short-lived identity federation limits credential exposure without making extra cloud infrastructure mandatory.

### Consequences

Phase 0 evaluates feasibility and Phase 1 defines the identity approach; later authorized phases implement and validate it only if needed.

---

## Reference checks for Phase 0

These are **external documentation references, not a claim that services were deployed**. Provider limits and terminology must be rechecked before execution:

- BigQuery Sandbox: https://docs.cloud.google.com/bigquery/docs/sandbox
- BigQuery pricing: https://cloud.google.com/bigquery/pricing
- BigQuery cost controls: https://docs.cloud.google.com/bigquery/docs/best-practices-costs
- Looker Studio connector: https://cloud.google.com/looker/docs/studio/connect-to-google-bigquery
- GitHub OIDC: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform
- dbt distributions (September 2026): https://docs.getdbt.com/blog/comparing-dbt-and-dbt-oss

