# Phase 8 release validation

Baseline is the Phase 7 closure `4d95e47`. Validated November 26, 2026.

| Stage | Observed evidence |
| --- | --- |
| Source | Six EIA snapshots matched the manifest. The local generator reproduced 26,304 raw rows with SHA-256 `3e7100ebb785ac817864a30286a52cc999bc686113ab2b6f11d19bf3b8a56760`. |
| Warehouse | dbt Core 1.12.7 and BigQuery adapter 1.12.4 built two views and passed all six historical tests. Staging job `6b2b1073-0a2e-4000-9192-e8eaa37bd61e` and fact job `222b8dce-fe7b-4a09-acbe-898424850649` each processed zero data bytes to define the views. |
| Curated export | Dry run and job `gridpulse_phase8_export_9dd0a2aee62e4588a098dff01da0f32f` each processed 2,287,296 bytes under a 10 MiB cap. The export validator passed. |
| Reconciliation | Each of the 26,304 rows matched its regenerated EIA source row across all eight original data fields. The curated CSV matched the Phase 6 SHA-256 byte for byte. |
| Power BI | A clean clone had no import cache. Only its local `CsvPath` was changed to point to the new export. Power BI Desktop opened GridPulse Color and fully refreshed Calendar and Hourly. All four DAX scenarios returned the expected values. |
| Cost | The dedicated project had billing disabled and no attached billing account before and after the jobs. Desktop ran locally. The revised CI command ran locally and these private pushes skipped hosted Actions execution. These activities incurred USD 0 in project charges. |

The 2,746,594-byte curated CSV has SHA-256
`f60458ea7e18273df28baaca2cbc3d8ef41b6aa1984761f374fa88dce4477d9f`.
It contains 26,232 paired hours across 26,304 UTC keys. The full-history
Desktop results were peak 85,544 MW on August 20, 2024, MAE 1,268.017726 MW,
signed bias +374.605558 MW, and coverage 99.726277%. March, local hour 17,
and the unpaired-only case matched the
[Phase 6 DAX evidence](phase-6-power-bi.md#local-report-project).

## Scope and limitations

The release rehearsal regenerated the raw projection locally and
reconciled it row by row with the warehouse output. It reused the
persisted raw table to avoid another batch load. The
[Phase 4 load evidence](phase-4-modeling.md) covers table creation and the
[Phase 5 recovery](phase-5-quality.md) covers a bounded missing-object rebuild.
A BigQuery job's bytes-billed statistic is a metering field. The cost gate
for this run was the verified unlinked billing state.

The [release guide](../phase-8-release.md) links inputs, commands, reports,
attribution and operating limits. The README includes both real-data
screenshots from the Phase 6 visual review. This evidence covers the
private release package. Public access remains subject to owner approval.
