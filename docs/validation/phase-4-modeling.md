# Phase 4 historical modeling validation

## Identification

- Phase: **4 — Analytical Modeling**
- Baseline: published Phase 3 closure `2da94a4`
- Validation date: 2026-11-26

## Sources and environment

Canonical `main` returned `2da94a4`, and the owner authorized Phase 4.
The six source hashes matched the [source manifest](phase-0-eia930.md#reproduce-the-local-check).
The historical projection contained 26,304 rows and 2,488,421 CSV bytes.
Its SHA-256 was `3e7100ebb785ac817864a30286a52cc999bc686113ab2b6f11d19bf3b8a56760`.
The March-only projection retained the Phase 2 CSV hash.

The project was unbilled at preflight. The owner prepared `gridpulse_raw`
and `gridpulse_models` in `US`. Each dataset had a 60-day default table
expiration and a dataset-level Data Editor grant for the existing operator.

## BigQuery raw load

The dedicated operator ran job `gridpulse_phase4_load_c44d7d4c` and wrote
26,304 rows to `gridpulse_raw.eia930_erco_hourly`. The input was 2,488,421
CSV bytes. The resulting unpartitioned table reported 2,287,296 logical
bytes. The column names, order, types and modes matched the generated
schema. The table has Sandbox expiration metadata.

## dbt and KPI checks

dbt Core 1.12.7 and BigQuery adapter 1.12.4 returned seven passes on the
`history` target. BigQuery metadata confirmed both relations as logical
views in `US`. The raw-to-mart test returned zero discrepancies across
source fields, coverage, and forecast errors. The clock test checked the
six 23- or 25-hour reporting dates, including the repeated 01:00 hour and
the skipped 02:00 hour.

| Model or test | BigQuery job ID | Bytes processed |
| --- | --- | ---: |
| Create staging view | `c4000d87-80cd-4033-b7d0-f0aa8012fe54` | 0 |
| ERCO accepted value | `6d904958-5e04-4387-b9bb-8ebf2758961b` | 157,824 |
| Non-null UTC key | `d95e3469-718e-4684-bd4e-df61fefbd3a8` | 210,432 |
| Unique UTC key | `d202cefb-ae54-448e-8621-e4225d017cd8` | 210,432 |
| Create hourly fact view | `c891f002-8b2f-4b21-9071-92fa2af408a0` | 0 |
| Raw-to-mart reconciliation | `36ec1851-8f4b-447b-ad01-719b1956f650` | 2,287,296 |
| Reporting clock | `d8e82482-ba2f-47ee-8cfe-b9c3834cbe08` | 631,296 |

The [historical reconciliation query](check_erco_history.sql) estimated
1,919,040 bytes and processed that amount in job
`gridpulse_phase4_reconcile_9502efd2`. The job ran without cached results
and within the 10 MiB per-query limit. The final billing check returned
`billingEnabled: false` with no linked account.

| Check | Observed value |
| --- | ---: |
| Rows and distinct consecutive UTC keys | 26,304 each |
| Reporting dates and source files | 1,096 and 6 |
| UTC range | `2023-01-01T07:00:00Z` to `2026-01-01T06:00:00Z` |
| Paired hours | 26,232 |
| Missing demand only, forecast only, or both | 24 each |
| Missing net generation | 48 |
| Errors populated on unpaired hours | 0 |
| MAE and bias for unpaired-only selection | `NULL` each |
| Peak demand | 85,544 MW |
| Mean absolute day-ahead forecast error | 1,268.017726 MW |
| Mean forecast minus demand | +374.605558 MW |

## Closure

**PASS.** The warehouse results match the source baseline. The historical
target keeps one persisted raw table and two logical views. Local dbt
parse passed without credentials for both targets. The pilot had one active
model and three tests. History had two active models and five tests. The
[Phase 5 handoff](../handoffs/phase-4-to-5.md) records the pending quality,
documentation, performance, and expiry recovery work.
