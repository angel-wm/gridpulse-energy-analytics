# Current State

## State

Project state: **DESIGN COMPLETE**

Current phase: **None**

Last closed phase: **Phase 0 — Formal Project Design** (`closed`)

Next planned phase:
**Phase 1 — Repository and Cloud Foundation** (requires explicit authorization)

Implementation status:
**Not started**

Published implementation:
**None**

Repository context status:
The closure baseline is the canonical `main` snapshot containing this
state and the [Phase 0 handoff](docs/handoffs/phase-0-to-1.md). Verify the
remote ref before treating a local copy as published.

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

These confirmations do not mean any implementation exists.

## Phase 0 outcome

The [design baseline](docs/phase-0-design-baseline.md) defines the hourly
model, CSV export, recovery plan, and zero-charge design. The
[closeout validation](docs/validation/phase-0-closeout.md) records evidence
and limitations. Local checks verified 26,304 distinct hours, 26,232
paired hours, the 743-row March pilot fixture, and dbt CLI startup.

## Runtime verification still required

Verify the unbilled project and identity first. Then reconcile the March
load, dbt execution, and Power BI Desktop CSV import before loading the
full three years. [The handoff](docs/handoffs/phase-0-to-1.md#handoff-to-phase-1)
assigns these gates to later phases. Terraform applies and cloud CI remain
deferred until the relevant capabilities and authorization exist.

## Current authorization

The user authorized completion and publication of the Phase 0 design.
Phase 1 requires new explicit authorization. Cloud execution requires
specific authorization under the phase and cost gates. The project must
operate with USD 0 in actual charges and keep Cloud Billing unlinked for
the Sandbox route.

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

Start with the [Phase 0 handoff to Phase 1](docs/handoffs/phase-0-to-1.md).
