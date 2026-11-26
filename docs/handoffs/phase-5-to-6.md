# Phase 5 handoff to Phase 6

## Identification

- Phase: **5 — Data Quality, Documentation and Performance**
- Status: **Quality and recovery validated in the closure snapshot**
- Baseline: canonical `main` commit containing this handoff
- Date: 2026-11-26

## Scope completed

The historical warehouse passed six dbt data tests, including coverage for
each of the six files. The generated dbt catalog confirmed source → staging →
hourly fact lineage. Scan measurements supported keeping the single
unpartitioned raw table and logical views. The isolated March recovery
restored the raw table and staging view and reconciled the 743 pilot hours
and metrics. Billing remained unlinked.

## Deliverables and validation

- [Quality and recovery runbook](../phase-5-quality.md).
- [Source coverage test](../../dbt/tests/erco_history_source_coverage.sql)
  and [KPI benchmark](../validation/benchmark_erco_kpis.sql).
- [Validation evidence](../validation/phase-5-quality.md) records the
  warehouse tests, catalog, scan measurements, and recovery jobs.

## Known limitations

The recovery exercise simulated absent objects with a separate empty
dataset. The raw table and views remain subject to Sandbox expiration.
For a historical rebuild, use the pinned files and the
[historical runbook](../phase-4-modeling.md).

## Handoff to Phase 6

Start after explicit authorization. Recheck unlinked billing and availability
of `gridpulse_models.fct_erco_hourly`. Export the curated hourly rows with a
bounded, verified query and compare against 26,304 UTC keys, 26,232 paired
hours, and the [historical validation](../validation/phase-4-modeling.md).
If the export route caps results, export separate nonoverlapping reporting
years and reconcile each part before combining them.

Use Power BI Desktop Import and the report structure in the
[design baseline](../phase-0-design-baseline.md#power-bi-delivery). Validate
the calendar relationship, report filters, observed peak, forecast MAE,
signed bias, and paired-hour coverage. Reopen and refresh the verified
artifact. The [roadmap](../../ROADMAP.md#phase-18-acceptance-criteria)
defines the Phase 6 checks.

## Repository state and closure

Verify this handoff on [canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main).
Jira tracks the closeout in [GRID-6](https://angel231995.atlassian.net/browse/GRID-6).
