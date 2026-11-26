# Phase 2 ingestion validation

## Identification

- Phase: **2 — Source Acquisition, Ingestion and Raw Layer**
- Baseline: published Phase 1 closure `dbefffc`
- Validation date: 2026-11-26
- Scope: March 2025 ERCO pilot in the unbilled BigQuery Sandbox

## Start and source checks

| Check | Result |
| --- | --- |
| Phase start | Canonical `main` returned `dbefffc`. The owner authorized Phase 2 |
| Source snapshots | All six SHA-256 values matched the [Phase 0 reference](phase-0-eia930.md#reproduce-the-local-check) |
| Local pilot | 743 rows, 70,431 bytes, and matching CSV SHA-256 `44cfa2c4a03c79fd6afda34fb27ff24035adf71905ad58a597aa9883bd4324c2` |
| Sandbox preflight | The CLI returned `billingEnabled: false` with no linked account |
| Dataset scope | `gridpulse_raw_pilot` was created in `US` with a 60-day table default. The dataset access entry grants the operator `WRITER` (BigQuery Data Editor) |
| Effective identity | `SESSION_USER()` matched the intended service account. The same session could read pilot dataset metadata |

## Load and reconciliation

Both jobs completed with `WRITE_TRUNCATE`, 70,431 input bytes, 743 output
rows, and 64,641 output bytes. The table metadata matched the generated
eight-column schema, including field order, types, and required or nullable
modes. BigQuery reported table expiration on 2027-01-25 at 14:34:56 UTC.

| Pass | Load job ID | Reconciliation query job ID |
| --- | --- | --- |
| Initial load | `gridpulse_phase2_load_6d0b8cc8_1` | `gridpulse_phase2_check_6d0b8cc8_1b` |
| Replacement | `gridpulse_phase2_load_6d0b8cc8_2` | `gridpulse_phase2_check_6d0b8cc8_2b` |

The [reconciliation query](check_erco_pilot.sql) returned the same results
after both loads.

| Check | Observed value |
| --- | --- |
| Row count and unique UTC keys | 743 each |
| First and last UTC hour endings | `2025-03-01T07:00:00Z` and `2025-04-01T05:00:00Z` |
| UTC hour gaps | 0 |
| Reporting dates | March 1–31, 31 distinct days |
| March 9 reporting hours | 23 |
| Rows from unexpected authorities or source files | 0 |
| Null demand, forecast, or generation values | 0 for each measure |

Each recorded dry run estimated 58,697 bytes. Each corresponding query
processed 58,697 bytes and reported 10,485,760 `totalBytesBilled` under
BigQuery's minimum query accounting. The project had no billing account
linked before and after the jobs. The Windows `bq` client emitted its
existing dependency warning and completed the load and validation commands.

## Closure

**PASS.** The raw table reconciled with the bounded source, and replacement
preserved its row count and unique keys. Reproduce these checks with the
[ingestion runbook](../phase-2-ingestion.md). See the
[Phase 3 handoff](../handoffs/phase-2-to-3.md) for the remaining analytics checks.
