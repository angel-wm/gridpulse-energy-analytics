# Phase 5 quality, lineage, and recovery runbook

Use the `history` target to examine the published warehouse model. Use the
`recovery` target for the isolated March rehearsal. Before running BigQuery
jobs, confirm unlinked billing and set the operator and ADC as described in
the [analytics runbook](phase-3-analytics.md#prepare-local-oauth-for-dbt).

## Inspect the historical model

    & $gridDbt test --project-dir dbt --profiles-dir dbt --target history --target-path target/phase5-history

BigQuery requires a 50 MiB cap for the adapter's catalog queries. Set the
catalog flag only for documentation generation after rechecking unlinked billing.

    $env:GRIDPULSE_DBT_CATALOG = '1'
    try {
        & $gridDbt docs generate --project-dir dbt --profiles-dir dbt --target history --target-path target/phase5-history
    } finally {
        Remove-Item Env:GRIDPULSE_DBT_CATALOG
    }

The test suite checks UTC uniqueness, authority, reporting-clock behavior,
raw-to-fact reconciliation, and coverage for every source file. The
source-coverage test expects exactly six semiannual files and compares
each filename, date range, day count, and hourly count with the pinned batch.

The `manifest.json` dependency map traces these relations in order:

| Object | How it enters the chain |
| --- | --- |
| `gridpulse_raw.eia930_erco_hourly` | The [source declaration](../dbt/models/history/staging/eia930_history.yml) maps the six-file projection to the persisted table. |
| `gridpulse_models.stg_eia930_erco_hourly` | The [staging view](../dbt/models/history/staging/stg_eia930_erco_hourly.sql) calls `source()` and preserves the source fields. |
| `gridpulse_models.fct_erco_hourly` | The [fact view](../dbt/models/history/marts/fct_erco_hourly.sql) calls `ref()` and derives the local hour, covered pairs, and forecast errors. |

The generated docs site uses that manifest and `catalog.json`, which records
the BigQuery column and relation metadata. To explore the graph locally,
serve the site on the loopback interface:

    & $gridDbt docs serve --project-dir dbt --profiles-dir dbt --target history --target-path target/phase5-history --host 127.0.0.1 --no-browser

Generated docs, catalogs, and metadata stay under the ignored dbt `target`
directory. The source, models, tests, and evidence are versioned.

## Compare query scans

Run the same [KPI query](validation/benchmark_erco_kpis.sql) with
`RELATION_ID` set to each of the three relations above and `DATE_FILTER`
set to `TRUE`. Then run it over the fact view with this narrower predicate:

    reporting_date >= DATE '2025-03-01' AND reporting_date < DATE '2025-04-01'

Use the `bq` impersonation setup from the
[ingestion runbook](phase-2-ingestion.md#verify-the-project-and-operator).
Run a dry run first. Use `--use_cache=false` and
`--maximum_bytes_billed=10485760` for the measured query. Record the job ID,
bytes processed, and returned KPIs. Use BigQuery relation metadata to record
persisted bytes. The [validation record](validation/phase-5-quality.md) reports
the observed values and the resulting storage decision.

## Rehearse a rebuild from missing objects

1. Use the [pinned sources and pilot preparation](phase-4-modeling.md#prepare-the-historical-batch)
   with `--pilot-output` in place of `--history-output`. Verify the resulting
   `erco-2025-03.csv` against the [pilot hash](phase-2-ingestion.md#prepare-the-source).
2. Use an authorized, empty `gridpulse_recovery` dataset in `US` with
   dataset-scoped Data Editor for the operator. Confirm it is empty with
   `bq ls` before beginning an absence rehearsal.
3. Load the verified CSV and explicit schema into
   `gridpulse_recovery.eia930_erco_202503` using the
   [batch-load pattern](phase-2-ingestion.md#load-and-reconcile-the-pilot).
   Use a unique job ID and confirm 743 output rows.
4. Run the command below to restore the view and its three tests in the
   recovery dataset. Then run the
   [pilot KPI query](validation/check_erco_pilot_kpis.sql) against
   `gridpulse_recovery.stg_eia930__erco_202503` and compare to the Phase 3
   baseline.

    & $gridDbt build --project-dir dbt --profiles-dir dbt --target recovery

This exercise simulates the absence of expired objects by starting with an
empty dataset. For a full rebuild, apply the
[historical runbook](phase-4-modeling.md) to the missing relations and
reconcile the historical row counts, clocks, and KPIs before reuse.
