# Phase 6 Power BI validation

## Identification

- Phase: **6 — Power BI Analytics**
- Baseline: published Phase 5 closure `060ab57`
- Validation date: 2026-11-26
- Status: **PASS — historical CSV, local refresh, and both report designs verified**

## Curated CSV

Canonical `main` returned `060ab57`. BigQuery returned the expected 12-column
historical fact view in `US`. The impersonated operator ran the
[bounded export query](export_erco_history.sql), with no cached result and
a 10 MiB cap. The dry run and query both reported 2,287,296 processed bytes.
The export job was `gridpulse_phase6_export_95a12015`. The preflight and
final CLI checks showed no linked billing account.

The CSV was produced from the query rows in one pass and reconciled with the
[local CSV checker](check_erco_history_export.py).

| Check | Observed value |
| --- | ---: |
| Hours and distinct consecutive UTC keys | 26,304 each |
| Reporting dates | 1,096 |
| Hours in 2023, 2024, and 2025 | 8,760, 8,784, and 8,760 |
| Hours with both measurements | 26,232 |
| Peak demand | 85,544 MW |
| Mean absolute day-ahead forecast error | 1,268.017726 MW |
| Mean forecast minus demand | +374.605558 MW |
| CSV size | 2,746,594 bytes |

The checker verified the header order, UTC and reporting calendars, the
source names, missing-measure counts, and row-level error fields. The
validated CSV SHA-256 was
`f60458ea7e18273df28baaca2cbc3d8ef41b6aa1984761f374fa88dce4477d9f`.

## Reproduce the local export

Use the [unbilled project and operator setup](../phase-2-ingestion.md#verify-the-project-and-operator).
From the repository root, use the verified project ID and write the CSV
outside Git. Compare the output with the results above.

    $gridFolder = Join-Path $env:TEMP ('gridpulse-phase6-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $gridFolder | Out-Null
    $gridCsv = Join-Path $gridFolder 'erco_hourly_2023_2025.csv'
    $gridSql = (Get-Content -Raw docs/validation/export_erco_history.sql).Replace('PROJECT_ID', $gridProject)
    $gridSql | & $gridBq @gridArgs query --dry_run=true --use_legacy_sql=false --maximum_bytes_billed=10485760
    $gridCsvArgs = @("--project_id=$gridProject", '--location=US', '--format=csv')
    $gridSql | & $gridBq @gridCsvArgs query --use_legacy_sql=false --use_cache=false --maximum_bytes_billed=10485760 --max_rows=26305 | Set-Content -LiteralPath $gridCsv -Encoding utf8
    .\.venv\Scripts\python.exe docs/validation/check_erco_history_export.py $gridCsv

## Local report project

The [approved specification](../../_brief/report-spec.md) defines the two
report pages. The [GridPulse PBIP](../../powerbi/GridPulse.pbip) binds to a
local TMDL model. Power BI Modeling MCP opened the TMDL definition and
reported two tables, ten measures, and one relationship. The Desktop results below verify the loaded model separately from
that file-level result.

For Desktop refresh, place the verified CSV at the path in the model's
`CsvPath` parameter. The default is
`C:\Users\Public\Documents\GridPulse\erco_hourly_2023_2025.csv`.
If the CSV is stored elsewhere, update the parameter in Power Query and
apply the change before refresh. Open `GridPulse.pbip` in Desktop. After
refresh, use the [DAX validation query](../../powerbi/GridPulse.SemanticModel/DAXQueries/Validate%20GridPulse.dax)
to compare the full, date-filtered, local-hour-filtered, and unpaired results.

| Selection | Reporting hours | Paired hours | Peak MW | Peak date | MAE MW | Bias MW |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| Full history | 26,304 | 26,232 | 85,544 | 2024-08-20 | 1,268.017726 | +374.605558 |
| March 2025 | 743 | 743 | 62,827 | 2025-03-25 | 1,034.648721 | +505.580081 |
| Local start hour 17 | 1,096 | 1,093 | 85,544 | 2024-08-20 | 1,512.795974 | +579.339433 |
| Unpaired hours | 72 | 0 | 51,172 | 2025-12-06 | Blank | Blank |

These expected values were computed independently from the verified CSV.

## Two local report designs

- [GridPulse original](../../powerbi/GridPulse.pbip) preserves the initial
  light design. The Desktop instance returned all four expected DAX rows
  for the full, March, local-hour, and unpaired selections.
- [GridPulse Color](../../powerbi/GridPulse%20Color.pbip) is a separate PBIP
  over the same semantic model and CSV. The
  [color design contract](../../_brief/report-color-spec.md) documents its
  palette, typography, and visual sizes.

The original PBIP, report, and model files were checked byte for byte
while creating the copy. Both pages kept the original 21 visual
bindings, filters, and interactions. The color layout passed the
rectangle check for visual overlaps.

On November 26, 2026, both color pages rendered with the verified
2023–2025 data in Power BI Desktop. The first captures showed overlapping
monthly point labels and automatic subtitles that repeated chart titles.
The corrected copy hides those labels and subtitles. Monthly values
remain available when hovering over the charts.

After the correction, the Microsoft report authoring CLI reported zero
errors and zero warnings for the color variant. Both new Desktop captures
showed the charts and KPI values, with the monthly series clear of label
overlaps. The color variant's live DAX query returned all four expected
rows from the table above, including blank error metrics for unpaired
hours. The original's current CLI check reported zero errors and two
warnings because it could not retrieve the report and visual schemas used
by some of its files.

## Filter and navigation review

Both GridPulse Color pages were reloaded and captured in Desktop.
The date controls show both range endpoints and the teal slider.
The local-hour controls retain their dropdowns. The page navigator
shows two distinct buttons without a shared frame, and the active
page is highlighted on both captures.

The final CLI check reported zero errors and two warnings because it
could not retrieve the newer report and visual schemas used by some
files.

## Original report reopen and refresh

Power BI Desktop 2.160.1151.0 reopened the original project on
November 26, 2026. The CSV SHA-256 matched the verified export.
The local Desktop model fully refreshed its Calendar and Hourly
partitions from that file. The post-refresh DAX query returned the
four expected rows above, including 99.726277% coverage across the
full period and blank MAE and bias for the unpaired-only case.

Desktop captured both original pages with populated charts, KPIs,
date and hour controls, and the correct active navigation states.
Dense labels in the original monthly charts remain part of its
preserved design. GridPulse Color incorporates the readability fixes
described above. Local use was verified without paid service sharing.

The current authoring CLI reported zero errors and two inaccessible
schema versions. These warnings limit schema coverage. The refresh,
DAX reconciliation, and visual review ran directly on Desktop.
PBIP tracks editable definitions while the import cache and CSV are
local runtime inputs. This evidence supports Phase 6 closure.
