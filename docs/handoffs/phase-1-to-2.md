# Phase 1 handoff to Phase 2

## Identification

- Phase: **1 — Repository and Cloud Foundation**
- Status: **Foundation closed in the closure snapshot**
- Baseline: the canonical `main` commit containing this handoff and the
  matching [current state](../../CURRENT_STATE.md)
- Date: 2026-11-26

## Scope completed

The local foundation includes Python 3.12, the pinned dbt CLI, Google Cloud
CLI with `bq`, and the static checks that run locally and on GitHub Actions.
The dedicated project showed BigQuery Sandbox with no linked billing account.
The existing Google login can obtain short-lived credentials for a dedicated
BigQuery operator with a project-scoped job role.

## Deliverables and decisions

- [Foundation runbook](../phase-1-foundation.md), [pinned dbt runtime](../../requirements-dbt.txt),
  [local checks](../../scripts/check_local.py), and [static CI workflow](../../.github/workflows/local-checks.yml).
- [D-026](../../DECISIONS.md#d-026--use-a-manual-bootstrap-for-the-single-sandbox)
  records manual setup for the single Sandbox.
  [D-027](../../DECISIONS.md#d-027--use-one-human-login-with-keyless-service-account-impersonation)
  records keyless service account impersonation.

## Validation summary

**PASS for foundation.** The [validation record](../validation/phase-1-foundation.md)
contains the CLI bootstrap, hosted static CI, billing checks, and live
project-level permission test. The operator can submit jobs, and the test
found no project-level grant to create datasets, create tables, or change
project IAM. No BigQuery jobs were submitted during this validation.

## Known limitations

The pilot dataset and its access grants are pending. dbt connectivity with
impersonated credentials and the Power BI Desktop CSV import are Phase 3
checks. Terraform and cloud-connected CI are deferred.

## Handoff to Phase 2

Phase 2 requires explicit authorization and is limited to the March 2025 ERCO
pilot. The source and load procedure is in the
[pilot tooling guide](../phase-0-pilot-tooling.md#prepare-and-load-the-pilot).

1. Verify the six EIA-930 source hashes and regenerate the 743-row pilot CSV
   and explicit schema locally.
2. Recheck project billing and the scoped operator. Create the dedicated
   `gridpulse_raw_pilot` dataset in `US` through the authorized setup path.
   Grant the operator Data Editor only on that dataset. Verify explicit
   impersonation in the ingestion client before submitting the load.
3. Load the March CSV. Record the job and reconcile the schema, 743 unique
   UTC keys, reporting dates, March 9's 23 hours, and measurement null counts.
4. Repeat the bounded replacement and verify the row count and keys again.
   Preserve the rebuild procedure and record the validation results.

## Repository state and closure

Verify the commit containing this handoff on
[canonical main](https://github.com/angel-wm/gridpulse-energy-analytics/tree/main)
before relying on it as the published closure. The Phase 1 checks satisfy the
[roadmap acceptance criteria](../../ROADMAP.md#phase-18-acceptance-criteria).
Jira tracks the closeout in [GRID-2](https://angel231995.atlassian.net/browse/GRID-2).
