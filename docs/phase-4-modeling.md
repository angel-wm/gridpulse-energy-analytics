# Phase 4 historical modeling runbook

Rebuild the historical ERCO table and the two analytical views for reporting
years 2023–2025. The March pilot uses a separate dbt target and datasets.

## Prepare the historical batch

Download the six snapshots listed in the
[source manifest](validation/phase-0-eia930.md#reproduce-the-local-check).
Set `$eiaFiles` using the manifest's PowerShell instructions. From the
repository root, generate the historical CSV and explicit BigQuery schema.

    $gridHistory = Join-Path $env:TEMP ('gridpulse-history-' + [guid]::NewGuid().ToString('N'))
    .\.venv\Scripts\python.exe docs/validation/check_eia930_source.py @eiaFiles --history-output $gridHistory

The command rejects a snapshot whose name and SHA-256 do not match the
recorded batch. It verifies the source grain, continuity, and null patterns
before writing 26,304 rows to `erco-2023-2025.csv`. Keep the source and
generated files outside Git.

## Load the raw table

Follow the [unbilled project and operator checks](phase-2-ingestion.md#verify-the-project-and-operator).
Use only the authorized Sandbox. The project owner provisions
`gridpulse_raw` and `gridpulse_models` in `US` and grants the operator
Data Editor on those two datasets. The same service account uses its
existing project-level BigQuery Job User role.

With verified impersonation active in `$gridArgs`, load the designated raw
table. Use replacement for intentional rebuilds of the same historical
batch. Inspect an existing target and record the load job before replacing
data. Use `bq show` to check a submitted job before retrying after a client
interruption.

    $gridCsv = Join-Path $gridHistory 'erco-2023-2025.csv'
    $gridSchema = Join-Path $gridHistory 'eia930-erco-schema.json'
    $gridTarget = "$($gridProject):gridpulse_raw.eia930_erco_hourly"
    $gridJob = 'gridpulse_history_load_' + [guid]::NewGuid().ToString('N')
    & $gridBq @gridArgs "--job_id=$gridJob" load --source_format=CSV --skip_leading_rows=1 --max_bad_records=0 --replace=true $gridTarget $gridCsv $gridSchema
    & $gridBq @gridArgs show --job=true $gridJob
    & $gridBq @gridArgs show $gridTarget

## Build and check the models

Use the [pinned dbt Core environment and local ADC](phase-3-analytics.md#prepare-local-oauth-for-dbt).
The `history` target builds the two views in `gridpulse_models`.

    & $gridDbt debug --project-dir dbt --profiles-dir dbt --target history
    & $gridDbt build --project-dir dbt --profiles-dir dbt --target history

Staging exposes the original fields. The hourly mart derives the local
interval-start hour, pair flag, and errors in one view over staging. A
separate intermediate layer would add a model without a reusable join or
transformation. Calendar filtering uses EIA's `reporting_date`. The date
dimension is a Power BI deliverable.

Both models use logical views. They reuse the single persisted raw table
and evaluate SQL at query time. The raw table starts unpartitioned because
the batch is small. Phase 5 measures scan costs before changing how data
is stored or partitioned.

Run the [historical reconciliation query](validation/check_erco_history.sql)
after dbt builds the views. Estimate bytes first and limit each execution
to 10 MiB. Compare against the [validation record](validation/phase-4-modeling.md).

    $gridSql = (Get-Content -Raw docs/validation/check_erco_history.sql).Replace('PROJECT_ID', $gridProject)
    $gridSql | & $gridBq @gridArgs query --dry_run=true --use_legacy_sql=false --maximum_bytes_billed=10485760
    $gridSql | & $gridBq @gridArgs query --use_legacy_sql=false --maximum_bytes_billed=10485760 --use_cache=false

The raw schema preserves nulls in the three measurements. A pair contributes
to MAE or bias only when demand and forecast both exist. For a selection
with no paired hours, both aggregates return null. The two repeated fall
hours share the same local bucket and have distinct UTC keys.
