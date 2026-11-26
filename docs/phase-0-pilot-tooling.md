# Phase 0 pilot tooling

Status: **Designed and verified locally**. Cloud execution is planned for
the phases listed in the [handoff](handoffs/phase-0-to-1.md). The March 2025
pilot requires specific execution authorization and an eligible BigQuery
Sandbox project with no linked billing.

## Tool choices

| Step | Tool | Why |
| --- | --- | --- |
| Prepare the input | Python 3.12 standard library | Select ERCO and the agreed columns from the original CSVs. Preserve EIA's reporting dates, missing values, and source filenames. |
| Load and inspect | Google Cloud CLI `bq` and GoogleSQL | Load the local CSV with explicit types, then observe table metadata, UTC keys, and query bytes directly in BigQuery. |
| Transform and test | Local dbt v2.0.13, package `dbt`, BigQuery adapter | Define a reusable source and views, make the test results inspectable, and provide the analytical input for the report. |
| Deliver pilot results | BigQuery console CSV download and Power BI Desktop Import | Verify the warehouse result reaches Power BI using a local file. |

dbt Labs documents local BigQuery support in dbt v2 and gcloud OAuth for
local authentication. The default `dbt` distribution is free for local use.
`dbt-oss` is the Apache 2.0 distribution and dbt v1 with `dbt-bigquery` is a
separate compatibility route if a specific requirement blocks the v2 pilot.
Check the cause before switching runtimes. Pin the tested version in the
implementation environment once warehouse compatibility is established.
See the [dbt versions](https://docs.getdbt.com/docs/dbt-versions),
[2.0.13 release](https://pypi.org/project/dbt/2.0.13/), and
[BigQuery adapter setup](https://docs.getdbt.com/docs/local/connect-data-platform/bigquery-setup?version=2).

## Prepare and load the pilot

Use the six files and PowerShell file list in the
[source validation record](validation/phase-0-eia930.md#reproduce-the-local-check).
Compare the file hashes before treating the output as the recorded baseline.
From the repository root, choose a new folder under an existing directory
outside the repository.

    $gridPilotOutput = Join-Path $env:TEMP 'gridpulse-erco-march-2025'
    python docs/validation/check_eia930_source.py @eiaFiles --pilot-output $gridPilotOutput

The check writes `erco-2025-03.csv` and `eia930-erco-schema.json` after
validating the source baseline. The candidate schema keeps key fields
required and allows nulls in the three measurements. The output is a local
validation fixture for the pilot.

For authorized execution, install Google Cloud CLI with `bq`, verify the
selected project has no billing linked, and use the matching project and
dataset location. The example assumes an existing `gridpulse_raw_pilot`
dataset in `US`. Substitute the actual unbilled project ID before use.

    $gridProject = '<verified-unbilled-project-id>'
    $gridTarget = "${gridProject}:gridpulse_raw_pilot.eia930_erco_202503"
    $gridPilotCsv = Join-Path $gridPilotOutput 'erco-2025-03.csv'
    $gridPilotSchema = Join-Path $gridPilotOutput 'eia930-erco-schema.json'
    bq "--project_id=$gridProject" --location=US load --source_format=CSV --skip_leading_rows=1 --max_bad_records=0 --replace=true $gridTarget $gridPilotCsv $gridPilotSchema

`--replace=true` replaces only this dedicated pilot table. It uses a batch
load job so that rerunning the same input does not append duplicate rows.
Confirm load-job support in the unbilled environment before adopting this as
the rebuild procedure. A local upload keeps Cloud Storage out of the pilot.
[BigQuery local batch loading](https://docs.cloud.google.com/bigquery/docs/batch-loading-data) ·
[bq load flags](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference#bq_load)

Before running the load example, configure and verify explicit impersonation
of the approved BigQuery operator described in the
[foundation runbook](phase-1-foundation.md#separate-project-setup-from-job-execution).
Grant write access only on the pilot dataset. The dbt identity needs read
access to the raw dataset and write access to the model dataset. Verify
impersonated Application Default Credentials for dbt in Phase 3. Version a
profile example with project, dataset, and location placeholders. Keep
credentials outside the repository.

## Where SQL ends and dbt begins

First inspect the loaded table in BigQuery. Verify its schema and row count.
Check that ERCO is the only authority, UTC timestamps are unique and
consecutive, and the reporting date of March 9 has 23 rows. Run a query
estimate before execution and record the bytes processed for the pilot.
Then reconcile the first aggregate in native GoogleSQL:

    SELECT
      COUNT(*) AS hours,
      COUNT(DISTINCT hour_ending_utc) AS distinct_utc_hours,
      COUNTIF(demand_mw IS NOT NULL AND forecast_mw IS NOT NULL) AS paired_hours,
      MAX(demand_mw) AS peak_demand_mw,
      ROUND(AVG(ABS(forecast_mw - demand_mw)), 3) AS mae_mw,
      ROUND(AVG(forecast_mw - demand_mw), 3) AS bias_mw
    FROM `YOUR_PROJECT_ID.gridpulse_raw_pilot.eia930_erco_202503`
    WHERE balancing_authority = 'ERCO';

The expected result is 743 hours, 743 distinct UTC hours, 743 paired hours,
a peak of 62,827 MW, mean absolute error of 1,034.649 MW, and bias of
+505.580 MW. A direct SQL check sets a reference before the model is built.

Use dbt to maintain those rules in versioned models and tests:

1. Declare the raw table as an EIA source. Use a staging view to expose
   stable column names, data types, and the UTC key.
2. Build a candidate hourly view with a paired-hour flag, signed error,
   and absolute error. Missing input measures produce null errors.
3. Test key uniqueness, required fields, and the presence of all expected
   hours. Reconcile the view against the same native SQL baseline.
4. Export the bounded hourly result through the BigQuery console and
   import it into Power BI Desktop. Aggregate the hourly measures with
   their eligible denominators when filtering the report.

The pilot has complete measurements. Include a separate bounded case with
an absent demand or forecast value when validating the null-handling rule.
Start with views because the workload is small. Compare query bytes and
storage before adding another persisted copy.

## Evidence and remaining checks

Python 3.12.10 on Windows generated the 743-row pilot fixture and schema.
Reading that CSV back confirmed the column order, UTC offsets, provenance,
and March 9 coverage. An independent SQLite query reproduced the KPI
baseline. The `dbt==2.0.13` package also installed and returned its version
in a temporary virtual environment.

The [Phase 1 validation](validation/phase-1-foundation.md) records the
cloud client, local OAuth, and project-level permission checks. The load job,
dbt adapter execution, view creation, and Power BI import remain pending.
If a step requests billing, record the blocker and evaluate a free
alternative or deferral.
