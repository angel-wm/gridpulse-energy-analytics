# Phase 0 handoff to Phase 1

## Identification

- Phase: **0 — Formal Project Design**
- Status: **Design closed in the closure snapshot**
- Baseline: the canonical `main` commit containing this handoff and the
  matching [current state](../../CURRENT_STATE.md)
- Date: 2026-11-25

## Scope completed

The initial release covers ERCO, reporting years 2023–2025, using EIA-930
Balance files. The report evaluates demand peaks, day-ahead forecast error,
bias, and observed coverage. The baseline defines fields and time grain,
batch ingestion, warehouse models, CSV delivery to Power BI, and the
design assessment for operating without linked billing.

## Deliverables and decisions

- [Specification](../../PROJECT_SPEC.md), [architecture](../../ARCHITECTURE.md),
  and [Phase 1–8 acceptance criteria](../../ROADMAP.md#phase-18-acceptance-criteria).
- [Design baseline](../phase-0-design-baseline.md) and [pilot tooling](../phase-0-pilot-tooling.md).
- [Local data and KPI evidence](../validation/phase-0-eia930.md) and
  [design validation](../validation/phase-0-closeout.md).
- D-022 selects EIA-930, D-023 sets the ERCO scope, D-024 selects local
  projection with a batch load, and D-025 records model and runtime gates.

## Validation summary

**PASS for design.** The six snapshots, 26,304 hour keys, KPI rules,
743-row pilot, and dbt CLI startup were verified locally. The warehouse
and Power BI pilot are **NOT RUN**. The [design validation](../validation/phase-0-closeout.md)
separates those results.

## Handoff to Phase 1

Phase 1 is planned. Obtain explicit authorization and the intended GCP
account/project before any cloud activity. Use the locally verified fixture
and documented command, and prove the target is an eligible Sandbox with
no linked billing. If there is no such environment, stop the cloud path
and report the blocker before requesting a change in scope.

| Gate | Required evidence before proceeding |
| --- | --- |
| Phase 1 foundation | Verify the account/project, no linked billing, local tools, scoped identity, and cloud-free CI design. Leave Terraform applies and OIDC/WIF deferred until justified and separately authorized. |
| Phase 2 pilot load | Use the 743-row March fixture. Record the job, expected UTC boundaries and reporting dates, schema, row count, and a duplicate-free bounded reload. |
| Phase 3 pilot transform and delivery | Practice native GoogleSQL, verify dbt against Sandbox, and reconcile a bounded view export and Power BI Desktop Import with the March KPIs. This is a delivery smoke check. |
| Phase 4 full batch | Load the full snapshot only after the one-month workflow passes. Reconcile its 26,304 hours, 26,232 pairs, and KPI values. |
| Phase 6 report | Build, reopen, and refresh the final report from versioned artifacts and a bounded CSV. |

## Repository state and closure

The closure baseline is the commit that carries this document. Verify
that commit on [canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main)
before relying on this handoff as a published closure. Jira tracks the
work in [GRID-1](https://angel231995.atlassian.net/browse/GRID-1).
