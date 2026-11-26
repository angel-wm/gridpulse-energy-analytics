# Phase 1 foundation validation

## Identification

- Phase: **1 — Repository and Cloud Foundation**
- Baseline: local Phase 1 work on the published Phase 0 commit `f6691c4`
- Local validation: 2026-11-25 and 2026-11-26
- Sandbox and effective IAM verification: 2026-11-26

## Validation scope

Verify the start gate, local tool bootstrap, static checks, Sandbox eligibility,
and project-level permissions for the operator.

## Checks

| ID | Check | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| V-201 | Phase 0 closure and Phase 1 authorization | Published closure with handoff and explicit authorization | Canonical `main` returned `f6691c4`, with the Phase 0 handoff available locally. The owner authorized Phase 1 | PASS |
| V-202 | Bootstrap Python and dbt | Python 3.12, dependency check passes, dbt CLI reports 2.0.13 | Fresh repository virtual environment on Python 3.12.10. Locked dependencies installed, `pip check` found no broken requirements, and the CLI returned `dbt 2.0.13` | PASS |
| V-203 | Static checks | Same command is runnable locally and wired into the GitHub workflow | `scripts/check_local.py` passed for 108 documentation links and two Python files. The local workflow invokes that command | PASS |
| V-204 | Hosted GitHub Actions | Workflow run succeeds after publication | Static checks passed on canonical `main` for commit `a86073c`, without GCP credentials or jobs. [Run 45835639432](https://github.com/angel-wm/gridpulse-energy-analytics/actions/runs/45835639432) | PASS |
| V-205 | Dedicated unbilled Sandbox project | Project exists, BigQuery shows Sandbox, and Billing shows no linked account | BigQuery displayed the Sandbox indicator for the dedicated project. The console showed no linked account. `gcloud billing projects describe` returned `billingEnabled: false` with no billing account name before and after the IAM check | PASS |
| V-206 | Scoped identity and local CLI authentication | Verify temporary credentials and limited effective permissions for the designated project | Local OAuth succeeded for the owner-selected login. Google issued a temporary credential via impersonation. The metadata API returned only the two expected permissions from the requested set. See the checks below | PASS |
| V-207 | Terraform scope | Resolve infrastructure scope for the verified environment | D-026 records manual setup for the single Sandbox. Terraform is deferred until a justified, unbilled use case exists | PASS |
| V-208 | Google Cloud CLI bootstrap | Official Windows archive matches its published SHA-256 and both executables start | Checksum matched. `gcloud version` returned 594.0.1 and `bq version` returned 2.1.42. The bundled `bq` emitted a dependency warning and exited successfully | PASS |

## Effective permission checks

The console showed BigQuery Job User on the project for the dedicated
service account, Service Account Token Creator for the existing owner at the
service account scope, and no user-managed keys. The IAM Service Account
Credentials and Cloud Resource Manager APIs were enabled to obtain a
temporary credential and run the read-only permission check.

The Cloud Resource Manager `projects.testIamPermissions` request used the
impersonated credential and checked these permissions on the project:

| Permission | Result |
| --- | --- |
| `bigquery.jobs.create` | Granted |
| `resourcemanager.projects.get` | Granted |
| `resourcemanager.projects.setIamPolicy` | Absent |
| `bigquery.datasets.create` | Absent |
| `bigquery.tables.create` | Absent |

## Limitations and closure

**PASS for Phase 1.** The BigQuery pilot dataset was not created and no
BigQuery jobs were submitted. The permission check covers the tested
permissions at project scope. Phase 2 requires its own dataset-level access
verification and load reconciliation. dbt connectivity and Power BI Desktop
import are Phase 3 checks. The
[Phase 1 handoff](../handoffs/phase-1-to-2.md) records the remaining gates.
