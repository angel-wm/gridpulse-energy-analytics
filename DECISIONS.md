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

Status: **SUPERSEDED** by D-016

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

## D-016 — Return to Power BI only; remove Looker Studio from GridPulse

Status: **SUPERSEDED** by D-018

Supersedes: **D-012**

### Context

The previously accepted companion Looker Studio deliverable introduced an extra BI integration and a potential billing-account requirement for direct BigQuery connectivity. Looker Studio itself can be used free of charge, but its native BigQuery connector requires a Google Cloud billing account. The user explicitly prefers removing the second BI deliverable rather than complicating GridPulse's strict zero-billing constraint.

### Decision

Keep **Power BI as the sole planned BI reporting deliverable**. Remove Looker Studio / Looker from active architecture, phase scope, functional requirements, and success criteria. Do not replace it with another tool merely to demonstrate tool breadth. This is not a claim that Looker Studio itself requires a paid subscription.

Power BI Desktop, an Import-first approach when appropriate, and evaluation of text-based PBIP versioning remain planned. During Phase 0, verify an end-to-end Power BI data delivery path that works without linking a GCP billing account; a reproducible bounded export/import may be preferable to a live connector.

### Rationale

The portfolio should demonstrate deep, reproducible work with BigQuery, dbt, and Power BI, without imposing an unnecessary billing or integration risk.

### Consequences

ROADMAP Phase 6 returns to Power BI analytics only. PROJECT_SPEC, ARCHITECTURE, README, CURRENT_STATE and AGENTS align. D-012 is retained as historical context but is no longer authoritative for current BI scope.

---

## D-017 — Size the complete warehouse footprint before choosing materializations

Status: **ACCEPTED**

### Context

BigQuery Sandbox has a non-replenishing lifetime storage quota; raw, staging and marts may materialize data repeatedly. A dataset smaller than 10 GiB can therefore still produce an excessive total or cumulative storage footprint.

### Decision

During Phase 0, once the actual source/dataset is chosen, estimate raw inputs, projected models, intermediate artifacts, repeated loads, and headroom under Sandbox's **lifetime** storage budget. Do not preselect a materialization strategy now. Evaluate production-relevant techniques where technically justified: views rather than unnecessary persisted copies; dbt ephemeral models for limited reusable SQL; selective, compact, business-ready mart tables; only justified intermediate layers; column pruning; partitioning/clustering based on measured query patterns; and carefully bounded test datasets.

Account for tradeoffs: views and ephemeral models reduce persisted copies but can increase repeated query processing; rebuilds and replacement data may consume the non-refundable Sandbox storage allocation; incremental models requiring unsupported Sandbox DML cannot be assumed executable. Choose using expected storage, query scans, performance, correctness, and reproducibility, not simply smallest bytes on disk.

### Rationale

This makes storage optimization a real engineering design exercise while preserving the USD 0 constraint and avoiding premature choices before data characteristics are known.

### Consequences

PROJECT_SPEC, ARCHITECTURE, and ROADMAP require a documented capacity estimate and materialization rationale in Phase 0, then validation against actual measurements in later phases. Dataset selection is still pending and no infrastructure is authorized.

---

## D-018 — Retain free Looker Studio as a companion without cloud billing

Status: **SUPERSEDED** by D-020 (scope/timing only)

Supersedes: **D-016**

### Context

The user wants to learn Looker Studio in addition to Power BI, but explicitly prioritizes no monetary charges. A direct Looker Studio (now also called Data Studio) -> BigQuery connector requires an eligible Google Cloud billing account, while standard Looker Studio supports free CSV file uploads and other sources.

### Decision

Power BI remains the complete primary BI report and Looker Studio returns as a **small, complementary** report using a no-billing data path. The preferred candidate is a reproducible, bounded **CSV export of curated business results -> free Looker Studio CSV file upload**. Google Sheets may be evaluated as an alternative if it is clearly available and free for the intended workload.

Maintain consistent KPI definitions across reports, show the data freshness/export process, and avoid duplicate rows when updating a Looker Studio CSV dataset because additional uploads append rather than replace data. Confirm connector availability and applicable upload quotas before implementation. Do not introduce Looker (enterprise), Looker Studio Pro, new cloud hosting, or a mandatory direct BigQuery connector.

### Rationale

The second report demonstrates useful versatility without the risk and additional complexity of cloud-billed direct BI access.

### Consequences

Update ROADMAP, PROJECT_SPEC, ARCHITECTURE, README, CURRENT_STATE and AGENTS. BigQuery Sandbox-first, USD 0 and phase authorization rules remain unchanged. The new decision is a **documentation scope approval only**, not authorization to start Phase 0.

---

## D-019 — Defer any billing-enabled BI experiment and research layered cost safeguards

Status: **ACCEPTED**

### Context

After completing the primary GridPulse project, the user might wish to evaluate a direct Looker Studio -> BigQuery integration by linking a billing account, but only if the risk can be understood and reduced substantially. The user has **not authorized** any billing activation or actual experiment.

### Decision

Record the direct integration as an **optional post-release research/experiment candidate**, not a delivery requirement. It requires a separate, explicit, future authorization to enable billing and to accept any residual risk of charges. If the user retains a non-negotiable USD 0 charge guarantee, **do not conduct** a billing-enabled experiment.

Before making any such recommendation, recheck current Google Cloud features, costs and service eligibility. Evaluate in this priority order:

1. Use a distinct disposable project, least privilege, very small bounded data/queries, and disable unrelated services/automated schedules.
2. Evaluate query dry runs, maximum bytes billed per query, and **conservative daily project/user custom query quotas**. These apply to on-demand query processing and are approximate; they do not cap all Cloud charges or precisely guarantee stopping under the free monthly allowance.
3. Add Cloud Billing budgets/alerts as monitoring only; alert-only budgets are not hard spending caps. Google documents delays in reported costs and notifications.
4. Examine the official Cloud Billing -> Pub/Sub -> Cloud Run function -> Cloud Billing API disconnection pattern. It is **reactive, not guaranteed** to prevent a charge, may itself require billable services, and disabling billing may shut down services and affect data.
5. Check the eligibility of native **spend-cap budgets**, which are service-specific and, according to Google's October 2026 eligible list, **do not include BigQuery**. Do not present these as a BigQuery hard cap. Even eligible caps can have non-instant enforcement and overages.

Do **not** assume that an alert/function set at '90% of the free tier' acts on free-tier *consumption*; billing-based alerts may respond only once monetary costs are recorded. Resource-usage monitoring and quota controls are separate from monetary budget alerts.

### Rationale

Preserves the user's option to learn native BI connectivity while explicitly rejecting a false '$0 guarantee' from delayed reactive cost shutdown.

### Consequences

No billing account, budget, function, Pub/Sub topic, or cloud infrastructure is created by this decision. Keep the optional evaluation after Phase 8 or in a separately authorized experiment; don't move the main project off Sandbox by default.

---

## D-020 — Complete the Sandbox project first; make Looker Studio an optional final experiment

Status: **ACCEPTED**

Supersedes: **D-018** for timing and core-release scope; preserves its no-billing free-CSV approach.

### Context

The user wants GridPulse's core project completed first, including BigQuery Sandbox, dbt, engineering quality and Power BI. Looker Studio is useful additional experience but should not delay or block the project's main release.

### Decision

Define the **core deliverable** as Phases 0–8 ending with the tested Power BI report, documentation, reproducibility and portfolio release. Move the small Looker Studio dashboard to **optional Phase 9 — Post-release Looker Studio Experiment**, startable only after Phase 8 is closed and the user separately authorizes Phase 9. The project is complete at Phase 8 even if Phase 9 never starts. Phase 9 is not implicitly authorized on release.

Within Phase 9, prefer the free, bounded CSV export/upload flow derived from dbt marts. Validate KPIs, freshness, append/deduplication and portability. The potential **direct** BigQuery connector on a billing-enabled project is a *separate optional experiment* discussed in D-019; it is not a prerequisite or automatically included in Phase 9.

### Rationale

Keeps the core deliverable focused and free while allowing additional BI experience later with independently bounded risk and effort.

### Consequences

ROADMAP adds explicitly optional Phase 9 outside the mandatory closure path. PROJECT_SPEC, ARCHITECTURE, CURRENT_STATE, README and AGENTS must not describe Looker Studio as a mandatory core report.

---

## D-021 — Prefer batch-first Sandbox-compatible transformations and document migration

Status: **ACCEPTED**

### Context

BigQuery Sandbox does not support DML (including INSERT, UPDATE, DELETE and MERGE), but GridPulse has not selected a dataset. dbt transformations do not inherently require per-row DML: views and suitably supported table builds using DDL/CTAS can support a historical batch dataset. Incremental models with MERGE/INSERT_OVERWRITE usually require forbidden statements.

### Decision

For Phase 0 evaluate a **reproducible batch/historical source** as the simplest likely fit for the no-billing constraint; do not prejudge dataset selection or rule out time-series business questions. Test the actual dbt adapter/commands in Sandbox before asserting compatibility. Prefer views, ephemeral models and appropriate bounded full-build tables where validated; do not implement untested DML-based incremental models, snapshots, hooks or ingestion techniques dependent on DML.

If an approved business requirement truly needs CDC, daily updates, late corrections, or incremental upsert, explicitly document that Sandbox does not provide the needed behavior. Evaluate a compliant alternative (for example, idempotent batch re-ingestion and a bounded full rebuild), a separate non-executed educational example, or deferral. Do not silently imply such workflows were tested.

For future portability, maintain reproducible source acquisition, dataset and metric definitions, SQL/dbt code, model and test configuration, environment-specific profiles via examples with **no secrets**, warehouse object naming, schema/grain/lineage, bounded export specification, Power BI artifacts, and verified runbooks. Explain how to rebuild in a new authorized environment and record limitations from Sandbox's 60-day object expiry and non-refundable lifetime storage quota. This documentation is not authorization to upgrade, migrate or enable billing.

### Rationale

Achieves real end-to-end Analytics Engineering using the free environment while clearly exposing what cannot be simulated. Retaining portable assets means later experimentation will not depend on remembering undocumented steps.

### Consequences

ROADMAP Phase 0 includes a DML-requirement decision and core-release handoff portability checklist; PROJECT_SPEC and ARCHITECTURE explain batch-first constraints. Future paid experimentation requires separate authorization per D-013 and D-019.

---

## Reference checks for Phase 0

These are **external documentation references, not a claim that services were deployed**. Provider limits and terminology must be rechecked before execution:

- BigQuery Sandbox: https://docs.cloud.google.com/bigquery/docs/sandbox
- BigQuery pricing: https://cloud.google.com/bigquery/pricing
- BigQuery cost controls: https://docs.cloud.google.com/bigquery/docs/best-practices-costs
- Looker Studio connector: https://cloud.google.com/looker/docs/studio/connect-to-google-bigquery
- GitHub OIDC: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform
- dbt distributions (September 2026): https://docs.getdbt.com/blog/comparing-dbt-and-dbt-oss
- dbt BigQuery incremental strategies: https://docs.getdbt.com/reference/resource-configs/bigquery-configs
- BigQuery SQL DDL for CTAS: https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language


Additional official references for the deferred experiment:

- Free Looker Studio CSV upload: https://docs.cloud.google.com/looker/docs/studio/upload-csv-files-to-looker-studio
- Direct BigQuery connector: https://docs.cloud.google.com/data-studio/connect-to-google-bigquery
- BigQuery daily custom quotas: https://docs.cloud.google.com/bigquery/docs/custom-quotas
- BigQuery cost controls: https://docs.cloud.google.com/bigquery/docs/best-practices-costs
- Billing budgets and limits: https://docs.cloud.google.com/billing/docs/how-to/budgets
- Programmatic billing shutdown (not guaranteed): https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications
- Spend cap budget service eligibility: https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps
