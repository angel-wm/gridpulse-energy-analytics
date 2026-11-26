# Phase 5 quality, lineage, and performance validation

## Identification

- Phase: **5 — Data Quality, Documentation and Performance**
- Baseline: published Phase 4 closure `9edb3f1`
- Validation date: 2026-11-26

The owner authorized Phase 5. Canonical `main` returned `9edb3f1`, and
the Google Cloud CLI confirmed no linked billing account before the work.
The [quality runbook](../phase-5-quality.md) records the comparison and
recovery procedures.

## Historical quality

The `history` target returned six passing data tests. The new source coverage
test checked the exact days and row counts of each of the six semiannual
sources against the fact view. It processed 1,078,464 bytes in job
`f1e4e057-7d9c-4a40-8e2b-f6a31fda31c9`.

| Check | BigQuery job ID |
| --- | --- |
| ERCO authority | `b13dad86-6c2b-4db1-8b45-d9b0c7b0ac13` |
| Raw-to-fact reconciliation | `55f9262c-e643-4c92-9fb5-98ea3fcc7ba4` |
| Reporting clock | `845d781b-4adc-40da-8bc0-d422e0b1d9e0` |
| Six half-year sources | `f1e4e057-7d9c-4a40-8e2b-f6a31fda31c9` |
| Non-null UTC key | `842da536-9710-4aa0-8633-778cfdd4a4d8` |
| Unique UTC key | `00fc936f-c649-436c-8b23-4d32c92622ef` |

## dbt catalog and lineage

`dbt docs generate` produced `index.html`, `manifest.json`, and
`catalog.json` for the historical target. The manifest confirmed the
source → staging → fact chain. The live catalog returned a table followed
by two views containing 8, 8, and 12 columns, respectively.

The first catalog generation hit the 10 MiB cap in jobs
`b5fc3232-f90f-4140-b06f-f6d1d9a8b904` and
`b8dc04ad-ef16-4b5a-b843-45518c33e4a7`. BigQuery required at least
52,428,800 bytes. The retry succeeded with the documented 50 MiB catalog
flag in its own process. The adapter warned that `table_owner` was absent
from catalog results. The generated catalog still contained all three
relations and their expected columns, with no catalog errors.

## Query scans and storage

The [benchmark query](benchmark_erco_kpis.sql) used the same KPI expression
on raw, staging, and fact. All full-range results matched the Phase 4
baseline. The March run returned 743 paired hours with the pilot's peak,
MAE, and bias. Cache was disabled. The dry runs matched the observed
processed bytes in each scenario.

| Scenario | BigQuery job ID | Estimated and processed bytes |
| --- | --- | ---: |
| Full historical raw | `gridpulse_phase5_bench_raw_eda5d2f7` | 420,096 |
| Full historical staging | `gridpulse_phase5_bench_staging_eda5d2f7` | 420,096 |
| Full historical fact | `gridpulse_phase5_bench_fact_eda5d2f7` | 420,096 |
| March 2025 slice of historical fact | `gridpulse_phase5_bench_march_eda5d2f7` | 630,528 |

BigQuery reported 10,485,760 `totalBytesBilled` in each query's job metadata.
The raw table metadata reported 2,287,296 logical bytes. The staging and
fact views each reported zero stored bytes. The March predicate reads
the reporting date column across the unpartitioned table, which accounts
for the extra 210,432 processed bytes.

Keep the unpartitioned table and logical views for this batch. The three
layers show identical scan estimates for the same projection, and the
date-filtered query stays below 1 MiB. The evidence supports leaving
partitioning, clustering, and persisted marts for a larger workload.

## Recovery rehearsal

The six source snapshots matched the pinned hashes. The regenerated
743-row March CSV matched the Phase 2 hash. The operator confirmed an
empty `gridpulse_recovery` dataset in `US` with a 60-day table default.
The recovery build recreated one raw table and one staging view. It
passed the three staging tests. The pilot and historical datasets were
outside the rehearsal target.

| Recovery check | BigQuery job ID | Observed result |
| --- | --- | --- |
| Batch load | `gridpulse_phase5_recover_dec23510` | 743 rows and 64,641 output bytes |
| Create staging view | `16dac504-15bc-4ed8-a201-db1ca4d000c9` | Logical view in `US` |
| March KPIs | `gridpulse_phase5_recovery_kpis_dec23510` | 743 unique UTC and paired hours, 62,827 MW peak, 1,034.649 MW MAE, +505.580 MW bias |

This was a bounded simulation of absent objects. It started with an empty
dataset and preserved the existing historical and pilot relations.

## Closure

**PASS.** The warehouse layers reconciled, the local catalog and lineage
were verified, the four uncached benchmarks matched the expected results,
and the bounded recovery restored the pilot. The final CLI check confirmed
that billing was disabled and no billing account was linked. Local dbt
parse verified the pilot, history, and recovery targets without warehouse
credentials. See the [Phase 6 handoff](../handoffs/phase-5-to-6.md).
