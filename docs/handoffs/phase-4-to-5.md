# Phase 4 handoff to Phase 5

## Identification

- Phase: **4 — Analytical Modeling**
- Status: **Historical model closed in the closure snapshot**
- Baseline: canonical `main` commit containing this handoff
- Date: 2026-11-26

## Scope completed

The six EIA-930 snapshots produced one 26,304-row raw table for ERCO's
2023–2025 reporting dates. BigQuery verified the table schema and
reconciliation. The history target builds staging and hourly fact views.
The fact adds local clock hour, paired coverage, and the forecast errors.

## Deliverables and validation

- [Historical runbook](../phase-4-modeling.md) and
  [source preparation](../validation/check_eia930_source.py).
- [Historical fact](../../dbt/models/history/marts/fct_erco_hourly.sql),
  [raw-to-mart test](../../dbt/tests/erco_history_matches_raw.sql), and
  [clock test](../../dbt/tests/erco_history_reporting_clock.sql).
- [Reconciliation SQL](../validation/check_erco_history.sql) and
  [validation evidence](../validation/phase-4-modeling.md).

**PASS.** The five dbt data tests passed. The hourly model has 26,304
unique UTC keys, 26,232 paired hours, and all three documented missingness
cases. The final billing check confirmed that billing was unlinked.

## Architecture and limitations

The unpartitioned raw table stores 2,287,296 logical bytes. Staging and the
hourly mart are logical views. The design uses one source without joins,
so there is no separate intermediate relation. Table expiration and the
Sandbox lifetime storage allowance apply to rebuilds. The date dimension and
historical Power BI report belong to the Power BI phase.

## Handoff to Phase 5

Start after explicit authorization. Reconcile the warehouse layers, document
dbt lineage, and use measured scan and storage results to evaluate any
partitioning, clustering, or additional persistence. Rehearse recovery from
expiration with bounded input and record the results. Use the existing
historical baseline and follow the
[roadmap criteria](../../ROADMAP.md#phase-18-acceptance-criteria).

## Repository state and closure

Verify this handoff on [canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main).
Jira tracks the closeout in [GRID-5](https://angel231995.atlassian.net/browse/GRID-5).
