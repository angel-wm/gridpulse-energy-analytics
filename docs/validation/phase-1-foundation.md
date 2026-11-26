# Phase 1 foundation validation

## Identification

- Phase: **1 — Repository and Cloud Foundation**
- Baseline: local Phase 1 work on the published Phase 0 commit `f6691c4`
- Local validation: 2026-11-25
- Sandbox verification: 2026-11-26

## Validation scope

Verify the start gate, local tool bootstrap, and static checks. Record the
remaining checks for the project's actual unbilled Sandbox and identity.

## Checks

| ID | Check | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| V-201 | Phase 0 closure and Phase 1 authorization | Published closure with handoff and explicit authorization | Canonical `main` returned `f6691c4`, with the Phase 0 handoff available locally. The owner authorized Phase 1 | PASS |
| V-202 | Bootstrap Python and dbt | Python 3.12, dependency check passes, dbt CLI reports 2.0.13 | Fresh repository virtual environment on Python 3.12.10. Locked dependencies installed, `pip check` found no broken requirements, and the CLI returned `dbt 2.0.13` | PASS |
| V-203 | Static checks | Same command is runnable locally and wired into the GitHub workflow | `scripts/check_local.py` passed for 108 documentation links and two Python files. The local workflow invokes that command | PASS |
| V-204 | Hosted GitHub Actions | Workflow run succeeds after publication | Local checks passed on canonical `main` for commit `6bea0ff`, without GCP credentials or jobs. [Run 45834831415](https://github.com/angel-wm/gridpulse-energy-analytics/actions/runs/45834831415) | PASS |
| V-205 | Dedicated unbilled Sandbox project | Project exists, BigQuery shows Sandbox, and Billing shows no linked account | Created **GridPulse Sandbox** with the owner-selected account. BigQuery displayed the Sandbox indicator and Billing reported that the selected project had no linked billing account | PASS |
| V-206 | Scoped identity and local CLI authentication | Verify a limited operating identity for the designated project | IAM lists the creator as legacy Owner. A limited operating identity and its OAuth access are pending | PARTIAL |
| V-207 | Terraform scope | Resolve infrastructure scope for the verified environment | D-026 records manual setup for the single Sandbox. Terraform is deferred until a justified, unbilled use case exists | PASS |
| V-208 | Google Cloud CLI bootstrap | Official Windows archive matches its published SHA-256 and both executables start | Checksum matched. `gcloud version` returned 594.0.1 and `bq version` returned 2.1.42. The bundled `bq` emitted a dependency warning and exited successfully | PASS |

## Limitations and closure

**PARTIAL.** Phase 1 is current. The Sandbox mode and unlinked billing were
verified in the console. Scoped identity and local CLI authentication
remain open. The [foundation runbook](../phase-1-foundation.md)
describes how to recheck project metadata before execution. The pilot data
load is assigned to Phase 2 after Phase 1 closes.
