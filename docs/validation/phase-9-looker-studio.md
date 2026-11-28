# Phase 9 Looker Studio validation

Started November 27, 2026. The experiment uses the historical ERCO
snapshot and free CSV upload. The [Phase 8 handoff](../handoffs/phase-8-release.md)
records the predecessor closure. Track progress in
[GRID-10](https://angel231995.atlassian.net/browse/GRID-10).

## Local input verified

Use the [bounded curated export](phase-6-power-bi.md#reproduce-the-local-export)
and run `python docs/validation/check_erco_history_export.py <csv-path>`.
The existing export passed on November 27. Its SHA-256
`f60458ea7e18273df28baaca2cbc3d8ef41b6aa1984761f374fa88dce4477d9f`
matches the [Phase 8 baseline](phase-8-release.md). It is 2,746,594 bytes
and contains 26,304 unique UTC hours and 26,232 hours with paired observations.
The reporting dates span 2023-01-01 through 2025-12-31. No warehouse job was
needed for this check.

## Results in Data Studio

On November 27, Data Studio accepted one file and detected all 12 columns.
The initial record-count card returned 26,304 rows. The report's date-prefix
and local-hour filters updated the cards and both hourly bar tables. The
tables displayed all 24 hours in the unfiltered view. Standard column charts
were blank in the browser used for validation, so the report uses native
tables with bars, which displayed the hour and metric values.

View-mode results agree at displayed precision with the
[Power BI validation scenarios](phase-6-power-bi.md#local-report-project).

| Selection | Peak demand (MW) | MAE (MW) | Signed bias (MW) | Paired coverage |
| --- | ---: | ---: | ---: | ---: |
| Full history | 85,544 | 1,268.02 | +374.61 | 99.73% |
| March 2025 | 62,827 | 1,034.65 | +505.58 | 100% |
| Local start hour 17 | 85,544 | 1,512.80 | +579.34 | 99.73% |
| December 4–6, 2025 | 51,172 | No data | No data | 0% |

Use `2025-03` with **Starts with**, choose **Only** for hour `17`, and use
`^2025-12-0[456]$` with **Regex** for the date range containing all 72 unpaired
hours. Reset between checks. The report identifies the 2023–2025 reporting
period and November 25, 2026 source verification date. Data Studio's update
time reflects query execution. The report source is the fixed historical file.

## Refresh and duplicate validation

Use a separate dataset for each replacement snapshot. The live test used a
separate QA report and two test datasets. Two 10-row files overlapped on five
UTC keys. A single replacement file contained the same 15 unique hours.

| Test dataset | Successful files | Rows in Data Studio | Distinct UTC keys in Data Studio |
| --- | ---: | ---: | ---: |
| Overlapping append | 2 | 20 | 15 |
| Clean replacement | 1 | 15 | 15 |

Locally, byte-identical inputs produced the same SHA-256. The historical
validator rejected a combined file with a repeated UTC key at its second data
row. Skip an upload when its checksum matches the active file. For a changed
full snapshot, validate UTC uniqueness locally, upload to a new dataset,
compare row counts with distinct UTC counts, then switch the report source.
Recheck the four report results after the switch.

Data Studio lists a 100 MB per-dataset limit for free uploads. The historical
file fits within it. The phase used the free CSV connector and required no
new BigQuery jobs, linked billing, or paid subscription. See the
[CSV connector documentation](https://docs.cloud.google.com/data-studio/upload-csv-files).
