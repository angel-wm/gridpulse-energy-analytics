# Phase 0 design baseline

This baseline covers the ERCO 2023–2025 portfolio release. Read the
[source evidence](validation/phase-0-eia930.md) for observed results and the
[pilot plan](phase-0-pilot-tooling.md) for the first authorized cloud checks.

## Source selection

The project needs reproducible public data with hourly measures that match
the questions about demand peaks and day-ahead forecast accuracy.

| Candidate | Access, rights, grain, and fit | Decision |
| --- | --- | --- |
| [EIA-930 Balance](https://www.eia.gov/electricity/930-content/about.html) | Public semiannual CSVs, no API key required. Six files for 2023–2025 total about 270 MB before filtering. One record per authority and UTC hour ending. Core measures are common across files. The publisher asks for acknowledgment with the publication date. [Reuse policy](https://www.eia.gov/about/copyrights_reuse.php) | Selected in D-022 and scoped to ERCO in D-023. Check file hashes to detect upstream revisions. |
| [UCI household power](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption) | Single public 20.6 MB ZIP, about 133 MB uncompressed, with 2,075,259 one-minute measurements from one home. CC BY 4.0. About 1.25% of active power measurements are missing. No day-ahead forecast or comparable authorities. | Viable alternative for a household consumption scenario. |
| [Open Power System Data](https://data.open-power-system-data.org/time_series/2020-10-06/) | Versioned public 130 MB hourly CSV. 2019 German and French load/forecast series have 8,760 UTC hours. The published free-reuse list covers day-ahead forecasts. Reuse rights for the selected actual-demand series were not established. [ENTSO-E reuse terms](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions) | Reserve pending rights clearance for the required fields. |

EIA publishes operational observations and can revise historical files.
GridPulse uses a fixed historical snapshot. Source updates are reviewed by
period, checksum, schema, and metric differences before replacing the
approved batch. Store the original files outside Git and record their URLs,
publication or reporting period and retrieval date, and hashes.

## Warehouse and report model

The canonical key is `(balancing_authority, hour_ending_utc)`. For example,
`ERCO / 2025-04-01 05:00 UTC` belongs to EIA reporting date March 31.
One raw record and one analytical fact represent that same time interval.

| Layer | Proposed object | Responsibility |
| --- | --- | --- |
| Raw | `gridpulse_raw.eia930_erco_hourly` | Load the approved projection as a single table with source filename lineage. |
| Staging | `stg_eia930_erco_hourly` view | Keep one row per raw key. Validate types, coverage, and allowed authority. |
| Intermediate | None for the initial scope | The hourly fact needs one source and no reusable joins. |
| Mart | `fct_erco_hourly` view | Keep one row per key. Add `paired_hour`, `forecast_error_mw`, `absolute_error_mw`, and the local hour of the interval start. |
| Power BI | Imported hourly fact and date dimension | Filter from one date row to many observations using `reporting_date`. Build or import a calendar covering every date in scope. |

Use EIA's reporting date for month and year. Derive the hour-of-day bucket
by subtracting one hour from the UTC end timestamp and converting the
interval start to `America/Chicago`. The two intervals in the repeated
autumn hour share an hour-of-day bucket and retain distinct UTC keys.
Do not use the EIA ordinal hour as a uniform local clock across DST.
With only ERCO there is no separate authority dimension or history
tracking for changing dimension attributes. A single-direction Date → Fact
relationship keeps filters clear and avoids repeating demand through joins.

The three-year snapshot has 26,304 reporting hours across 1,096 reporting
dates. Start with an unpartitioned raw table and logical views. A date
partition is a later candidate if measured scan reductions justify it.
Clustering by the single authority would provide no useful separation.

## Power BI delivery

Use two report pages during the implementation phase:

- **Demand patterns** shows observed peak and date, a demand/forecast trend
  at an appropriate date resolution, and hour-of-day patterns for the
  selected period.
- **Forecast accuracy** shows mean absolute error, signed bias, paired-hour
  coverage, and error by month and local hour. Display the counts behind
  coverage and identify gaps before interpreting differences.

The export is a flat UTF-8 CSV with one row per UTC key. Keep the raw contract
fields for authority, reporting date, UTC hour, and the three MW measures.
Add `local_start_hour` (integer 0–23), `paired_hour` (0 or 1),
`forecast_error_mw`, and `absolute_error_mw` (nullable signed and absolute
integers). Use ISO dates, explicit UTC timestamps, invariant numeric formats,
and empty cells for nulls. Validate column order, row count, unique keys,
UTC types, missing counts, and KPIs before distributing an export. The
report should show the reporting window and EIA snapshot date.

Keep row-level rules upstream in SQL/dbt. In Power BI, compute the observed
peak as max demand and the period error and bias as error sums divided by
the count of paired hours. Return blank if that count is zero. Derive
coverage by dividing pair count by reporting-hour count in the same filter
context. Reconcile those measures after changing date and hour filters.

Use Desktop Import and a local CSV parameter. Confirm the documented
console export limits against the actual result. If one export cannot
hold the full dataset, export nonoverlapping reporting years, check each
row count, and combine them locally. Version the PBIP text definitions once
the installed Desktop version verifies save, reopen, and refresh. Exclude
local settings and data cache. Offer GitHub screenshots for readers and
local Desktop interaction for users running the report. Keep Looker Studio
outside the core release. [BigQuery local export](https://docs.cloud.google.com/bigquery/docs/export-file) ·
[Power Query CSV](https://learn.microsoft.com/en-us/power-query/connectors/text-csv) ·
[PBIP source control](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)

## Zero-charge feasibility and recovery

**Design assessment: feasible in principle with runtime gates.** The local
fixture and published service capabilities support an unbilled Sandbox-first
design. There is no verified Sandbox project or authenticated adapter session
for this phase. The live pilot is deferred as described in the handoff.

- Verify the actual job project is an eligible Sandbox with no linked billing
  before any workload. Stop on a billing or trial prompt. Preserve Google's
  60-day expiry. Use dry runs and a query byte limit where supported. A budget
  alert is not a spending limit.
- The fixed historical source needs no CDC, streaming, incremental upserts,
  or snapshots. Reconcile the local projection, then reload it using a batch
  replacement into the intended raw table. Recreate dbt views and re-export
  the mart. A revised source is a deliberate full rebuild with an updated
  manifest. Reconcile staged rows with the source before exposing results.
- Plan for about 3.2 MiB of logical raw size at 128 bytes per row. With 4 MiB
  each for raw and an optional persisted hourly copy, ten complete rebuilds
  and 1 MiB for the pilot allow about 81 MiB, under 0.8% of the 10 GiB lifetime
  allowance. Logical views and ephemeral SQL avoid additional stored copies
  but can rescan input. Test the first view query and track actual table
  sizes and bytes processed before persisting any additional model.
- If CLI upload fails, check the documented console upload path with the
  bounded file. Compare the documented local dbt runtimes if the adapter
  blocks the pilot. If there is no validated unbilled path, stop at local
  evidence and escalate the BigQuery dependency. A local SQL result is not
  a substitute for verifying the approved BigQuery architecture.

See the [Sandbox limitations](https://docs.cloud.google.com/bigquery/docs/sandbox)
and the [pilot checks](phase-0-pilot-tooling.md#evidence-and-remaining-checks).

## Identity, infrastructure, and CI

- A human uses local OAuth to run jobs on the designated project. Assign
  BigQuery Job User at project scope. Scope Data Editor to the authorized
  raw-load writer's raw dataset and the dbt writer's model dataset. The
  dbt writer also needs Data Viewer on raw. Provisioning permissions are
  handled separately from day-to-day reads and writes. Keep ADC, user
  settings, project credentials, and tokens outside Git.
- Start with a documented local bootstrap and pinned dependencies. The
  initial toolchain does not need Docker. Consider Terraform only for
  reproducible dataset metadata, location, allowed expiry, labels, and scoped
  grants once an unbilled workflow is demonstrated. Defer applying Terraform
  until that scope and access are verified. Billing, trial, persistent keys,
  remote state buckets, and unneeded services are outside the baseline.
- Early CI checks documentation links, validates local fixture outputs, and
  parses dbt configuration when verified to work offline. Use a standard
  runner only after verifying no-cost eligibility, with read-only repository
  access and no cloud credentials, privileged PR execution, or cloud jobs.
  Keep the same checks runnable locally if host usage cannot be assured free.
- Defer cloud CI and OIDC/WIF until a zero-charge route and permissions are
  proven. A future federation policy must trust only the intended repository
  (prefer immutable owner/repository IDs) and protected ref or environment,
  scope job and dataset grants to disposable test resources, and use
  short-lived identities. Fork PRs receive no cloud access.

[BigQuery IAM roles](https://docs.cloud.google.com/bigquery/docs/access-control) ·
[Deployment identity federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines) ·
[Terraform dataset resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset) ·
[GitHub Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage)

## Rebuild package

Keep the source URLs and attribution, hashes and contract, local prepare and
load commands, non-secret environment examples, pinned tool versions,
versioned SQL and dbt models/tests, export contract, PBIP definitions,
validation results, and an expiry recovery runbook. A fresh authorized
environment must rebuild from the original inputs and reconcile against the
same baseline. Record actual rehydration results in the later phase that
performs it. Future billing-enabled and cross-region migration are separate
design decisions.
