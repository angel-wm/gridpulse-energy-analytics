# Phase 3 analytics runbook

Calculate the March pilot indicators directly in BigQuery, then use the same
data to verify the dbt staging view and Power BI Desktop import. The
[validation record](validation/phase-3-analytics.md) lists the checks that ran.

## Establish the native BigQuery reference

Verify that billing is unlinked and the March pilot table is available. Use
the operator and CLI configuration from the
[ingestion runbook](phase-2-ingestion.md#verify-the-project-and-operator).
From the repository root, substitute the verified project ID, estimate
the scan, and run the bounded query.

    $gridSql = (Get-Content -Raw docs/validation/check_erco_pilot_kpis.sql).Replace('PROJECT_ID', $gridProject)
    $gridSql | & $gridBq @gridArgs query --dry_run=true --use_legacy_sql=false --maximum_bytes_billed=10485760
    $gridSql | & $gridBq @gridArgs query --use_legacy_sql=false --maximum_bytes_billed=10485760 --use_cache=false

Peak demand is the maximum observed hourly demand. Mean absolute error
averages the magnitude of forecast minus demand over paired hours. Bias
averages the signed difference over the same hours. A positive bias means
the day-ahead forecast was higher than observed demand on average.

## Parse the dbt project locally

The [staging model](../dbt/models/staging/stg_eia930__erco_202503.sql) reads
the raw table through dbt's `source()` reference, which declares where the
data comes from. The view exposes the pilot fields without storing another
copy of the rows. The tests check a non-null unique UTC key and the ERCO code.

From the repository root, install the Phase 3 runtime in an isolated Python
3.12 environment and use a placeholder project for parsing. The GitHub
workflow uses the same profile without Google credentials.

    python -m venv .venv\dbt-core-compat
    .\.venv\dbt-core-compat\Scripts\python.exe -m pip install -r requirements-dbt-core.txt
    $gridDbt = '.\.venv\dbt-core-compat\Scripts\dbt.exe'
    $env:GRIDPULSE_PROJECT_ID = 'gridpulse-offline'
    $env:DBT_SEND_ANONYMOUS_USAGE_STATS = 'false'
    & $gridDbt parse --project-dir dbt --profiles-dir dbt

[D-028](../DECISIONS.md#d-028--use-dbt-core-v1-for-the-unbilled-bigquery-pilot)
records why the pilot uses the Python adapter.

## Prepare local OAuth for dbt

The `bq` commands use Google Cloud CLI credentials. The dbt profile uses
Application Default Credentials (ADC), which applications look up independently.
The pilot uses the existing human login to obtain temporary credentials for
the operator. Keep the local credential file outside the repository.

Use the isolated `$env:CLOUDSDK_CONFIG` from the
[foundation runbook](phase-1-foundation.md#google-cloud-cli-on-windows).
Set `$gridProject` to the verified unbilled project before running the
following setup. Sign in to Google with the project owner's existing account.

    $gridOperator = "gridpulse-bq-operator@$gridProject.iam.gserviceaccount.com"
    & $gridGcloud auth application-default login "--impersonate-service-account=$gridOperator" --disable-quota-project
    $env:GOOGLE_APPLICATION_CREDENTIALS = Join-Path $env:CLOUDSDK_CONFIG 'application_default_credentials.json'
    $env:GRIDPULSE_PROJECT_ID = $gridProject

The staging destination is `gridpulse_models_pilot` in `US`. Grant any new
write access only on that dataset and preserve the operator's project job role.
Verify the connection before running the model.

    & $gridDbt debug --project-dir dbt --profiles-dir dbt
    & $gridDbt build --project-dir dbt --profiles-dir dbt --select stg_eia930__erco_202503

## Validate the local CSV import

When the staging view is available, run the
[bounded CSV query](validation/export_erco_pilot.sql) using `bq` with the
verified project ID and the operator identity. Estimate the bytes before
execution and use the same scan limit as the native check. Save the CSV
outside Git with the name `erco_pilot.csv`.

In a blank Power BI Desktop file, use **Get data → Text/CSV**, select the
local file, and choose **Load**. Ensure that the table name is `erco_pilot`
and the measurement and error columns are numeric. From DAX Query View,
run the [import reconciliation query](validation/check_erco_pilot_import.dax).
Compare its row count, unique hours, paired hours, peak, MAE, and bias with
the native results. This import is a delivery check for the March pilot.
[Text/CSV connector](https://learn.microsoft.com/power-query/connectors/text-csv) ·
[DAX Query View](https://learn.microsoft.com/power-bi/transform-model/dax-query-view)
