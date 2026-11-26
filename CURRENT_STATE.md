# Current State

## State

Project state: **INGESTION PILOT COMPLETE**

Current phase: **None**

Last closed phase: **Phase 2 — Source Acquisition, Ingestion and Raw Layer** (`closed`)

Next planned phase:
**Phase 3 — BigQuery Native Analytics and dbt Foundation** (`planned`,
requires explicit authorization)

Implementation status:
**March 2025 ERCO ingestion pilot verified in BigQuery Sandbox**

Published implementation:
Local bootstrap, static checks, GitHub Actions workflow, ingestion procedure,
and pilot reconciliation SQL.

Repository context status:
The [Phase 2 handoff](docs/handoffs/phase-2-to-3.md) identifies the closure
snapshot on canonical `main` and the evidence needed for Phase 3.

## What is confirmed

The following project direction has been approved at a conceptual level:

- project name: GridPulse;
- orientation: Analytics Engineering + cloud BI;
- domain: energy analytics;
- primary data source: EIA-930 ([D-022](DECISIONS.md#d-022--use-eia-930-as-the-primary-energy-data-source));
- initial scope: ERCO (Texas), reporting years 2023–2025, focused on demand
  peaks and day-ahead forecast accuracy;
- ingestion design: prepare a bounded ERCO batch from the six EIA-930 CSVs
  locally and load one source-aligned BigQuery raw table
  ([D-024](DECISIONS.md#d-024--prepare-a-bounded-eia-930-batch-locally-for-bigquery));
- validation approach: one-month Sandbox pilot without billing before a full
  load, with reproducible source checks for Phase 0 closeout
  ([D-023](DECISIONS.md#d-023--analyze-erco-demand-and-forecast-accuracy-for-20232025));
- primary warehouse: BigQuery;
- primary transformation framework: dbt;
- SQL is the primary transformation language;
- Python may support ingestion or utilities when justified;
- **core BI layer**: Power BI (Desktop/Import-first where appropriate, with PBIP considered for reproducibility); a small free-CSV Looker Studio dashboard is an **optional separately authorized Phase 9 after the Phase 8 core release**, not a core deliverable;
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

## Phase 0 outcome

The [design baseline](docs/phase-0-design-baseline.md) defines the hourly
model, CSV export, recovery plan, and zero-charge design. The
[closeout validation](docs/validation/phase-0-closeout.md) records evidence
and limitations. Local checks verified 26,304 distinct hours, 26,232
paired hours, the 743-row March pilot fixture, and dbt CLI startup.

## Phase 1 outcome

Use the [foundation runbook](docs/phase-1-foundation.md) and
[validation record](docs/validation/phase-1-foundation.md) for the local
setup, static checks, and project eligibility gate. The pinned dbt CLI,
Google Cloud CLI, and BigQuery CLI start locally. The static workflow passed
on GitHub Actions. The dedicated project showed BigQuery Sandbox in the
console, and both the console and CLI confirmed that billing was unlinked.
Local OAuth and short-lived impersonation passed the project-level permission
check for the BigQuery operator service account (D-027). The project creator
retains Owner for administration. Terraform is deferred for the single
Sandbox (D-026).

## Phase 2 outcome

The March 2025 raw pilot in `US` contains 743 ERCO rows. The initial load and
bounded replacement matched the generated schema and source checks. Billing
remained unlinked. See the [ingestion runbook](docs/phase-2-ingestion.md)
and [validation record](docs/validation/phase-2-ingestion.md).

## Runtime verification still required

Verify native analytics, dbt execution, and Power BI Desktop CSV import in
Phase 3 before loading the full three years. The
[Phase 2 handoff](docs/handoffs/phase-2-to-3.md#handoff-to-phase-3) records the
next checks. Terraform applies and cloud CI remain deferred.

## Current authorization

The user explicitly authorized Phase 2 on 2026-11-26, with documentation,
commit, and push. The scope is the March 2025 ERCO pilot in the dedicated,
unbilled Sandbox, using the dataset-scoped operator in the Phase 1 handoff.
The full historical load and Phase 3 require their own authorization.
GridPulse requires USD 0 actual charges and an unlinked Cloud Billing
account for the Sandbox route.

## Resume instructions

When resuming GridPulse:

1. read REPO_CONTEXT.md;
2. read this state;
3. identify whether the task is state, planning, education/debugging,
   architecture, implementation, review, or history;
4. read the selected phase rules and scope in ROADMAP;
5. read PROJECT_SPEC and only the additional sources required by the task;
6. perform only explicitly authorized work.

## Next handoff

Start with the [Phase 2 handoff to Phase 3](docs/handoffs/phase-2-to-3.md).
