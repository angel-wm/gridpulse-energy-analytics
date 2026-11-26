# Phase 3 handoff to Phase 4

## Identification

- Phase: **3 — BigQuery Native Analytics and dbt Foundation**
- Status: **Analytics foundation closed in the closure snapshot**
- Baseline: canonical `main` commit containing this handoff
- Date: 2026-11-26

## Scope completed

The native BigQuery query established peak demand, MAE, and signed forecast
bias for the 743-hour March ERCO pilot. dbt Core 1.12.7 with BigQuery adapter
1.12.4 used the keyless operator to build and test a staging view in `US`.
Power BI Desktop imported the bounded CSV and reproduced all three metrics
and the coverage counts with DAX.

## Deliverables and decisions

- [Analytics runbook](../phase-3-analytics.md),
  [dbt staging model](../../dbt/models/staging/stg_eia930__erco_202503.sql),
  and [staging tests](../../dbt/models/staging/eia930.yml).
- [Native KPI query](../validation/check_erco_pilot_kpis.sql),
  [CSV export query](../validation/export_erco_pilot.sql), and
  [Desktop reconciliation query](../validation/check_erco_pilot_import.dax).
- [D-028](../../DECISIONS.md#d-028--use-dbt-core-v1-for-the-unbilled-bigquery-pilot)
  records the compatible runtime and its project permission requirements.

## Validation summary

**PASS for the bounded pilot.** See the
[Phase 3 validation](../validation/phase-3-analytics.md) for BigQuery jobs,
dbt results, CI, and the Desktop import. BigQuery billing remained unlinked.

## Known limitations

Sandbox objects expire. The versioned SQL, dbt files, and runbooks support a
rebuild. The Desktop check used a temporary local model and one month of
source data. The analytical models for the full history and the portfolio
report remain later-phase deliverables.

## Handoff to Phase 4

Start after explicit authorization. Verify unlinked billing and use the
same six EIA-930 source snapshots. Load and reconcile 26,304 distinct ERCO
hours and 26,232 paired measurements for 2023–2025. Verify reporting clock
changes, missing-measure cases, and peak demand, MAE, and bias against the
[design baseline](../phase-0-design-baseline.md).

Build the approved staging, intermediate, and mart models at the hourly
grain. Justify the materialization of each layer under Sandbox lifetime
storage limits. Preserve the UTC key and reportable coverage through the
models. See the [roadmap criteria](../../ROADMAP.md#phase-18-acceptance-criteria).

## Repository state and closure

Verify this handoff on [canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main).
Jira tracks the closeout in [GRID-4](https://angel231995.atlassian.net/browse/GRID-4).
