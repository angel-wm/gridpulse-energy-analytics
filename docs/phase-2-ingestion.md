# Phase 2 ingestion runbook

Rebuild the March 2025 ERCO raw table from the public EIA-930 Balance files.
The raw table preserves the EIA reporting date and hour, the UTC key,
nullable measurements, and the source filename.

## Prepare the source

Download the six Balance CSVs, compare their SHA-256 hashes, and generate
the March CSV and schema using the
[source validation and preparation commands](validation/phase-0-eia930.md#reproduce-the-local-check).
The expected CSV has 743 rows and SHA-256
`44cfa2c4a03c79fd6afda34fb27ff24035adf71905ad58a597aa9883bd4324c2`.
Keep the source files and generated output outside Git.

## Verify the project and operator

Set the CLI paths and use the isolated configuration from the
[foundation runbook](phase-1-foundation.md#google-cloud-cli-on-windows).
Verify unlinked billing before provisioning or submitting jobs. Continue only
if the CLI returns `billingEnabled: false` with no billing account name. The
existing project owner creates `gridpulse_raw_pilot` in `US` and grants BigQuery
Data Editor on that dataset to the operator. The operator uses its existing
project-level BigQuery Job User role to submit jobs. Check the dataset access
entry before continuing. [BigQuery dataset access documentation](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam)

In a dedicated PowerShell session with `$gridProject` set to the verified
project ID, set the impersonation property for that process. Use the
session identity query to confirm the result matches `$gridOperator`.

    $gridOperator = "gridpulse-bq-operator@$gridProject.iam.gserviceaccount.com"
    $env:CLOUDSDK_AUTH_IMPERSONATE_SERVICE_ACCOUNT = $gridOperator
    $gridArgs = @("--project_id=$gridProject", '--location=US', '--format=json')
    & $gridBq @gridArgs query --use_legacy_sql=false --maximum_bytes_billed=10485760 'SELECT SESSION_USER() AS principal'
    & $gridBq @gridArgs show "$($gridProject):gridpulse_raw_pilot"

## Load and reconcile the pilot

Set `$gridPilotOutput` to the folder containing the generated March files.
Use a unique job ID for each intentional submission, and use `bq show`
to inspect a submitted job before retrying after a client interruption.

    $gridCsv = Join-Path $gridPilotOutput 'erco-2025-03.csv'
    $gridSchema = Join-Path $gridPilotOutput 'eia930-erco-schema.json'
    $gridTarget = "$($gridProject):gridpulse_raw_pilot.eia930_erco_202503"
    $gridJob = 'gridpulse_phase2_load_' + [guid]::NewGuid().ToString('N')
    & $gridBq @gridArgs "--job_id=$gridJob" load --source_format=CSV --skip_leading_rows=1 --max_bad_records=0 --replace=true $gridTarget $gridCsv $gridSchema
    & $gridBq @gridArgs show --job=true $gridJob
    & $gridBq @gridArgs show $gridTarget

The load job replaces only the designated pilot table. Confirm the job
completed successfully with 743 output rows and compare the table's columns,
types, and modes with the generated schema. Confirm the table has expiration
metadata. To check the contents from the repository root, estimate the query
scan first, then run the same query with the bytes limit and cache disabled.

    $gridSql = (Get-Content -Raw docs/validation/check_erco_pilot.sql).Replace('PROJECT_ID', $gridProject)
    $gridSql | & $gridBq @gridArgs query --dry_run=true --use_legacy_sql=false --maximum_bytes_billed=10485760
    $gridSql | & $gridBq @gridArgs query --use_legacy_sql=false --maximum_bytes_billed=10485760 --use_cache=false

Compare the results with the [validation record](validation/phase-2-ingestion.md).
Repeat the load and checks to verify replacement. Clear the process-local
impersonation property and recheck billing when finished.

    Remove-Item Env:CLOUDSDK_AUTH_IMPERSONATE_SERVICE_ACCOUNT
    & $gridGcloud billing projects describe $gridProject --format='json(billingEnabled,billingAccountName)'
