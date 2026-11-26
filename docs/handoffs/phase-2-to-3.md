# Phase 2 handoff to Phase 3

## Identification

- Phase: **2 — Source Acquisition, Ingestion and Raw Layer**
- Status: **Ingestion pilot closed in the closure snapshot**
- Baseline: the canonical `main` commit containing this handoff and the
  matching [current state](../../CURRENT_STATE.md)
- Date: 2026-11-26

## Scope completed

The ingestion pilot builds the March 2025 ERCO CSV from the six verified
EIA-930 Balance snapshots. The raw table is
`gridpulse_raw_pilot.eia930_erco_202503` in `US`. It preserves one row per
UTC hour, the reporting date and hour, the three measurements, and source
provenance. The operator has Data Editor on the pilot dataset through the
existing keyless impersonation path.

## Deliverables and validation

- [Ingestion runbook](../phase-2-ingestion.md) and
  [source file hashes](../validation/phase-0-eia930.md#reproduce-the-local-check).
- [Reconciliation SQL](../validation/check_erco_pilot.sql) and
  [validation record](../validation/phase-2-ingestion.md).

**PASS for the bounded pilot.** Initial load and replacement both returned
743 rows and 743 distinct consecutive UTC hours, with equal schema, coverage,
and null counts. Billing remained unlinked.

## Known limitations

Sandbox tables expire automatically. Check the table metadata before using
it and rebuild from the pinned source snapshots if it has expired. The full
2023–2025 load is scheduled for Phase 4.

## Handoff to Phase 3

Phase 3 requires explicit authorization. Recheck unlinked billing and
confirm the pilot table is available. Start by running bounded native
GoogleSQL and recording the results and bytes scanned. Compare peak demand,
MAE, and bias with the local values in the
[pilot tooling guide](../phase-0-pilot-tooling.md#where-sql-ends-and-dbt-begins).

Then verify the pinned dbt runtime with impersonated Application Default
Credentials. Scope any new write grant to the model dataset. Build and test
a source and staging view using the verified Sandbox path. Reconcile a
bounded CSV export and Power BI Desktop Import with the native SQL results.
See the [roadmap criteria](../../ROADMAP.md#phase-18-acceptance-criteria).

## Repository state and closure

Verify the commit containing this handoff on
[canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main)
before relying on it as published. Jira tracks the phase in
[GRID-3](https://angel231995.atlassian.net/browse/GRID-3).
