# Rebuild and inspect GridPulse

Start with the screenshots and findings in the [README](../README.md).
Use the steps below to reproduce the historical report on Windows.
Plan for Python 3.12, the [pinned dbt dependencies](../requirements-dbt-core.txt),
the [pinned Google Cloud CLI](phase-1-foundation.md#google-cloud-cli-on-windows),
and Power BI Desktop. The final Desktop test used version 2.160.1151.0.

## Reproduce the report

1. **Prepare the inputs.** Download the six Balance CSV files from the
   [EIA source manifest](validation/phase-0-eia930.md#reproduce-the-local-check).
   Check their hashes and generate the raw projection and explicit
   schema using the [historical ingestion runbook](phase-4-modeling.md#prepare-the-historical-batch).
2. **Build the warehouse model and export.** Use an authorized Sandbox
   with billing unlinked and the
   [keyless operator setup](phase-2-ingestion.md#verify-the-project-and-operator).
   Follow the [historical rebuild](phase-4-modeling.md#load-the-raw-table)
   and then run the [bounded curated export](validation/phase-6-power-bi.md#reproduce-the-local-export).
   The dry run must pass before the 10 MiB-capped query. Check the curated CSV
   for 26,304 rows and the hash in the [release validation](validation/phase-8-release.md).
3. **Refresh Power BI.** Open
   [GridPulse Color](../powerbi/GridPulse%20Color.pbip) or the
   [light design](../powerbi/GridPulse.pbip). Set `CsvPath` in
   Power Query to the verified local CSV, apply the change, then refresh.
   The default points to
   `C:\Users\Public\Documents\GridPulse\erco_hourly_2023_2025.csv`.
   Compare results with the
   [four DAX scenarios](validation/phase-6-power-bi.md#local-report-project).
   In Desktop, use Ctrl + click on a report navigation button.

For checks that do not access the warehouse, activate the pinned dbt
environment and run `python scripts/check_ci.py`. It checks links and Python
syntax and parses all three dbt targets. See the
[CI evidence](validation/phase-7-ci-hardening.md).

## Data attribution

Source is the **U.S. Energy Information Administration, Form EIA-930
Balance files**, six semiannual snapshots for reporting years 2023–2025.
The manifest records their exact fingerprints. The dashboard screenshots
use EIA's ERCO data and original GridPulse analysis of the snapshot
verified on November 25, 2026. [EIA source manifest](validation/phase-0-eia930.md#reproduce-the-local-check)
· [EIA reuse policy](https://www.eia.gov/about/copyrights_reuse.php)

The [MIT License](../LICENSE) applies to GridPulse's original code and
documentation. EIA data and Microsoft-generated Power BI resources
retain their respective terms. Raw files, curated CSVs, imported caches,
and local credentials stay outside Git.

## Operating limits

- This is a historical ERCO analysis using EIA reporting dates. It is
  designed for local Power BI Desktop Import and was exercised without
  paid sharing.
- The single persisted raw table and logical views are subject to
  Sandbox expiry. Recover from the verified source files and the
  [recovery instructions](phase-5-quality.md#rehearse-a-rebuild-from-missing-objects).
  Reloads count against Sandbox lifetime storage limits. The final test
  reused the verified persisted raw table and rebuilt the views.
- Forecast error metrics use hours with both demand and forecast.
  Full-period coverage was 99.73%. Error metrics return blank for a
  selection without paired hours.
- Public visibility is an owner-controlled release action. The
  [handoff](handoffs/phase-8-release.md) records the delivery boundary.
