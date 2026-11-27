# Current State

## State

Project state: **POWER BI AND OFFLINE CI VALIDATED**

Current phase: **None**

Last closed phase: **Phase 7 — CI/CD and Infrastructure Hardening** (`closed`)

Next planned phase:
**Phase 8 — Final Validation and Portfolio Release** (`planned`,
authorized to start after Phase 7 closure)

Implementation status:
**Historical reports verified in Desktop and the CI command verified locally**

Published implementation:
Local bootstrap, GitHub Actions checks, pilot and historical ingestion,
dbt models and tests, query benchmarks, the recovery runbook, and the
historical Power BI projects.

Repository context status:
The [Phase 7 handoff](docs/handoffs/phase-7-to-8.md) identifies the closure
snapshot on canonical `main` and the evidence needed for Phase 8.

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

## Phase 3 outcome

The native query verified 743 paired hours, a 62,827 MW peak, 1,034.649 MW
mean absolute error, and +505.580 MW mean signed forecast error. The
[Phase 3 validation record](docs/validation/phase-3-analytics.md) records
the jobs, bytes scanned, and results.
The dbt Core staging view and its three data tests passed in the unbilled
Sandbox. The exported CSV and the Power BI Desktop import both reconciled
to the native results. The [analytics runbook](docs/phase-3-analytics.md)
documents how to reproduce the checks.

## Phase 4 outcome

The historical raw table and hourly fact contain 26,304 distinct UTC hours
with 26,232 paired measurements. The five dbt data tests passed. Peak
demand, forecast error, bias, clock changes, and missingness matched the
baseline. The [modeling runbook](docs/phase-4-modeling.md) and
[validation record](docs/validation/phase-4-modeling.md) document the results.

## Phase 5 outcome

Six history tests passed. The local dbt catalog confirmed the warehouse
lineage. The historical raw table stores 2,287,296 logical bytes. The three
equivalent full-range KPI queries each processed 420,096 bytes. The isolated
recovery dataset restored the March pilot with 743 hours and the same KPIs.
Billing remained unlinked. See the [quality runbook](docs/phase-5-quality.md)
and [validation evidence](docs/validation/phase-5-quality.md).

## Phase 6 outcome

The curated CSV matched the 26,304 historical UTC hours, 26,232 paired
hours, peak demand, MAE, and bias. See the
[export validation](docs/validation/phase-6-power-bi.md). The
[approved report specification](_brief/report-spec.md) is implemented in
the local [Power BI project](powerbi/GridPulse.pbip). A separate
[color variant](powerbi/GridPulse%20Color.pbip) shares its semantic model.
Both Desktop models returned all four expected DAX scenarios. The
color variant's two pages rendered successfully after layout cleanup.
The original reopened from its PBIP, refreshed the local CSV, and rendered
both pages with the same metric results.

## Phase 7 outcome

The shared offline CI command passed from a clean clone with the candidate
changes. A broken local link caused a nonzero exit before dbt. The live
access audit confirmed the dedicated operator's scope and absence of
user-managed keys. See the [validation record](docs/validation/phase-7-ci-hardening.md).

## Current authorization

The user explicitly authorized Phase 6 on 2026-11-26. The scope covers the
historical CSV and the local Power BI report. The owner approved the
two-page specification. The owner authorized Phases 7 and 8 in sequence,
with GitHub visibility private until separately authorized.
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

Start with the [Phase 7 handoff to Phase 8](docs/handoffs/phase-7-to-8.md).
