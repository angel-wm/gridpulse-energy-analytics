# Phase 3 analytics validation

## Identification

- Phase: **3 — BigQuery Native Analytics and dbt Foundation**
- Baseline: published Phase 2 closure `b8150c6`
- Validation date: 2026-11-26

## Native BigQuery reference

The CLI confirmed that the project had no linked billing account and that
the March raw table contained 743 rows. The operator ran the
[native GoogleSQL check](check_erco_pilot_kpis.sql) in `US` with a 10 MiB
maximum-bytes setting and the query cache disabled. The dry run and the live
job both reported 28,234 bytes processed. Job ID
`gridpulse_phase3_native_002866da` used the approved operator identity.

| Check | BigQuery result |
| --- | ---: |
| Rows, unique UTC keys, and paired measurements | 743 each |
| Peak demand | 62,827 MW |
| Mean absolute day-ahead forecast error | 1,034.649 MW |
| Mean forecast minus demand | +505.580 MW |

The values match the [local pilot baseline](../phase-0-pilot-tooling.md#where-sql-ends-and-dbt-begins).

## dbt staging

Local `dbt parse` passed with dbt v2.0.13 and a placeholder project. Its
live connection check failed because it requires project-level BigQuery
Read Session User to use the Storage Read API. Google OAuth created the
isolated impersonated ADC file, and `dbt debug` passed with dbt Core 1.12.7
and BigQuery adapter 1.12.4 on Python 3.12.10. See
[D-028](../../DECISIONS.md#d-028--use-dbt-core-v1-for-the-unbilled-bigquery-pilot)
and the [analytics runbook](../phase-3-analytics.md).

`gridpulse_models_pilot` was created in `US`. The operator's new Data
Editor grant applies to that dataset. BigQuery returned `VIEW` for
`gridpulse_models_pilot.stg_eia930__erco_202503`. `dbt build` reported one
successful model and three passing tests. BigQuery job metadata confirmed
that the approved operator issued `CREATE_VIEW` in `US`.

| Check | BigQuery job ID | Bytes processed |
| --- | --- | ---: |
| Create staging view | `308dd263-16bb-4d83-b270-efe1dfa87069` | 0 |
| ERCO accepted value | `baaf773f-0aa7-4ae5-8644-54f2da08ef74` | 4,458 |
| Non-null UTC key | `4ed60def-2f6a-417d-b70f-9d35bacf4983` | 5,944 |
| Unique UTC key | `39f32293-de54-40dc-8d2c-06314f898075` | 5,944 |

## CSV handoff and Desktop import

The [export query](export_erco_pilot.sql) processed 64,641 bytes in job
`gridpulse_phase3_export_fd8bfc8c`. The generated `erco_pilot.csv` contained
743 rows and 743 distinct UTC keys. The peak, MAE, and bias matched the
native query. The local CSV SHA-256 was
`4f97d4c0cca986c6dbbffe141aad0d31640fd22691b5675b43dd3e703a947f52`.
Billing remained unlinked after the jobs.

Power BI Desktop imported the verified CSV into `erco_pilot` using a
Power Query `Csv.Document(File.Contents(...))` partition in Import mode.
The local Power BI Authoring MCP created and refreshed the table in a blank
Desktop document. A separate DAX execution against the Desktop instance
confirmed the loaded data.

| [DAX reconciliation](check_erco_pilot_import.dax) | Power BI Desktop |
| --- | ---: |
| Rows, distinct UTC hours, and paired hours | 743 each |
| Peak demand | 62,827 MW |
| Mean absolute day-ahead forecast error | 1,034.649 MW |
| Mean forecast minus demand | +505.580 MW |

## Closure

**PASS.** The native query, staging view, export and Desktop import agree.
The published checkpoint `fb4e7db` passed static checks and dbt parsing
without warehouse credentials. [GitHub Actions run](https://github.com/angel-wm/gridpulse-energy-analytics/actions/runs/45876603411)

The Desktop session was a local import check. The versioned evidence is
the query, procedure, and observed results. The
[Phase 4 handoff](../handoffs/phase-3-to-4.md) records the remaining work.
