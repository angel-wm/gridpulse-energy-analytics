# Phase 0 validation — EIA-930 source baseline

## Identification

- Phase: **0 — Formal Project Design**
- Baseline: EIA-930 Balance CSV snapshots listed below
- Validation date: 2026-11-25

## Validation scope

The local check profiles reported ERCO rows and computes reference values
for the proposed indicators. It uses the original EIA files and Python's
standard library. These results are a baseline for later load and report
reconciliation.

## Checks

| ID | Check | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| V-001 | Required source columns and types | Common fields present and measures parse as finite numbers | All six files have the fields. All 78,768 populated measure cells contain whole numbers | PASS | Source check |
| V-002 | ERCO hourly keys and volume | 26,304 distinct, consecutive UTC hour endings | 26,304 rows, zero duplicate keys, zero non-hourly steps | PASS | Source check |
| V-003 | Paired forecast coverage | Count only rows with demand and forecast available | 26,232 paired hours. In 2025, 48 values are missing in each measure, with both missing together in 24 hours | PASS | Reconciliation below |
| V-004 | March 2025 pilot baseline | Capture a complete reporting month including the March clock change | 743 paired rows. March 9 has 23 rows and all timestamps are consecutive in UTC | PASS | Source check |
| V-005 | Unbilled Sandbox load, dbt, and Power BI CSV handoff | Reproduce the March counts and KPIs | Pilot is specified in ARCHITECTURE.md | NOT RUN | Proposed pilot |
| V-006 | Local pilot fixture and schema | Preserve 743 rows, keys, schema order, and baseline KPIs | CSV read-back and independent SQLite aggregate matched | PASS | [Pilot tooling evidence](../phase-0-pilot-tooling.md#evidence-and-remaining-checks) |
| V-007 | Local dbt CLI startup | dbt v2.0.13 starts in an isolated Python 3.12 environment | Installed and returned `dbt 2.0.13` | PASS | [Pilot tooling evidence](../phase-0-pilot-tooling.md#evidence-and-remaining-checks) |
| V-008 | Local SQL with real missing measurements | Preserve all hours, calculate errors only for pairs, and return null on a selection without pairs | 24 rows each with only demand missing, only forecast missing, and both missing. All 72 have null errors. Empty-pair selections return null metrics. The SQL aggregates match the baseline | PASS | Source check, `hourly model SQL` result |

## Reconciliation

Demand peaks use observed hours. MAE and bias use paired hours. Positive
bias indicates overforecasting on average. MAE and bias are rounded below
to three decimal places.

| Reporting period | Hours | Paired hours | Peak demand (MW) | MAE (MW) | Bias (MW) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023 | 8,760 | 8,760 | 85,432 | 1,299.369 | +265.518 |
| 2024 | 8,784 | 8,784 | 85,544 | 1,139.508 | +199.227 |
| 2025 | 8,760 | 8,688 | 83,597 | 1,366.337 | +661.913 |
| 2023–2025 | 26,304 | 26,232 | 85,544 | 1,268.018 | +374.606 |
| March 2025 pilot | 743 | 743 | 62,827 | 1,034.649 | +505.580 |

The full series runs from 2023-01-01 07:00 UTC to 2026-01-01 06:00 UTC.
The pilot spans 2025-03-01 07:00 UTC to 2025-04-01 05:00 UTC. Both windows
are selected by EIA reporting date.

## Reproduce the local check

Download these files into a local folder. The SHA-256 values identify the
snapshots used for this record. A different hash calls for reviewing any
source revisions before comparing against this baseline.

| EIA Balance file | ERCO rows | SHA-256 |
| --- | ---: | --- |
| [2023 Jan–Jun](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2023_Jan_Jun.csv) | 4,343 | `a0e14e9c07ab4cc1de3e384c7be890b0c61d9de3fe04ad3ae5ec739f1f35ec1b` |
| [2023 Jul–Dec](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2023_Jul_Dec.csv) | 4,417 | `c719fc1b513eec8982ce209b6e3173fc64b2d0d243f83d3bf0d8d1adf6222de2` |
| [2024 Jan–Jun](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2024_Jan_Jun.csv) | 4,367 | `26768c495c3ba987e29d79df2e40d4e741f9dbcff086f53c12ff774465756a10` |
| [2024 Jul–Dec](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2024_Jul_Dec.csv) | 4,417 | `a602a8e577cfdd2fa3083413eaa4dd8ba7f0d2b26a2986f8f6d22917465ea49f` |
| [2025 Jan–Jun](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2025_Jan_Jun.csv) | 4,343 | `fac4bb991dfa1dab3b4b35300ccab54ac99be13a40ce91954db8ddafb2816242` |
| [2025 Jul–Dec](https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2025_Jul_Dec.csv) | 4,417 | `1146158b972439db7c7f4cc7d0491e07644ddbf244d03b8ecb44cb2c833d10f1` |

From the repository root, set the path to that folder and run the
[source check](check_eia930_source.py) with Python 3.12:

    $eiaFolder = 'C:\path\to\eia-downloads'
    $eiaFiles = @(Get-ChildItem -LiteralPath $eiaFolder -File |
        Where-Object Name -Match '^EIA930_BALANCE_202[3-5]_(Jan_Jun|Jul_Dec)\.csv$' |
        Sort-Object Name | Select-Object -ExpandProperty FullName)
    python docs/validation/check_eia930_source.py @eiaFiles

To also generate the validated March CSV and BigQuery schema locally, see
the [pilot preparation command](../phase-0-pilot-tooling.md#prepare-and-load-the-pilot).
The reference pilot CSV has 743 rows, 70,431 bytes, and SHA-256
`44cfa2c4a03c79fd6afda34fb27ff24035adf71905ad58a597aa9883bd4324c2`.

Source: U.S. Energy Information Administration, Form EIA-930 Balance files
for reporting periods 2023–2025, as retrieved for this validation. See the
[source definitions](https://www.eia.gov/electricity/930-content/about.html)
and [reuse policy](https://www.eia.gov/about/copyrights_reuse.php).

## Limitations

The profile uses reported values and preserves missing measurements. It
does not independently measure the grid or prove warehouse, dbt, or Power
BI behavior. The provisional full-history storage estimate is not a measured
Sandbox charge or quota usage.

## Overall result

**PARTIAL.** The source and local KPI baseline are verified. Warehouse and
report feasibility remain to be verified for the planned route.

## Closure recommendation

Use the verified local results as input to the
[design closeout](phase-0-closeout.md). The live pilot has its own gates in the
[handoff](../handoffs/phase-0-to-1.md).
