# Phase 9 Looker Studio handoff

The optional experiment closed on November 27, 2026. The
[Phase 8 handoff](phase-8-release.md) remains the record for the core Power BI
release. The experiment used the same verified ERCO export under the
USD 0 cost constraint. Track closure in [GRID-10](https://angel231995.atlassian.net/browse/GRID-10).

## Delivery

The owner account holds **GridPulse | ERCO demand and forecast accuracy**
in Google Data Studio. The report contains four KPI cards, two 24-hour tables
with bars, and controls for reporting date and local start hour. The
[validation record](../validation/phase-9-looker-studio.md) contains the measured
Power BI parity and the isolated append and replacement results.

## Rebuild and refresh

1. Obtain the verified CSV through the
   [curated export instructions](../validation/phase-6-power-bi.md#reproduce-the-local-export).
   Run the historical validator and compare the SHA-256 with the release evidence.
2. Create a new dataset in the free **CSV File Upload** connector with one
   verified full file. Keep the existing dataset available for rollback. Use
   `Record Count` and `COUNT_DISTINCT(hour_ending_utc)` to confirm the same
   expected count before attaching the new source.
3. Recreate or rebind the report from that source and compare the four report
   selections against the [validation record](../validation/phase-9-looker-studio.md#results-in-data-studio).
   Use the text `reporting_date` for the date-prefix filter and numeric
   `local_start_hour` for the hour selection and both table dimensions.

| Report field | Calculation |
| --- | --- |
| Peak demand (MW) | `MAX(CAST(demand_mw AS NUMBER))` |
| Mean absolute error (MW) | `AVG(CASE WHEN paired_hour = 1 THEN CAST(absolute_error_mw AS NUMBER) END)` |
| Signed forecast bias (MW) | `AVG(CASE WHEN paired_hour = 1 THEN CAST(forecast_error_mw AS NUMBER) END)` |
| Paired coverage (%) | `100 * AVG(paired_hour)` |
| Mean observed demand by hour (MW) | `AVG(CASE WHEN demand_mw != "" THEN CAST(demand_mw AS NUMBER) END)` grouped by `local_start_hour` |
| Forecast MAE by hour (MW) | Mean absolute error grouped by `local_start_hour` |

Both hourly tables sort `local_start_hour` ascending. The report displays the
historical period and source snapshot date. Replacing the source requires an
explicit import. The CSV and account-owned report assets stay outside Git.
