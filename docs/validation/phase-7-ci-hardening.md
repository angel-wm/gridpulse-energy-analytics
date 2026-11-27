# Phase 7 CI and infrastructure validation

Baseline is the Phase 6 closure `6bbc965`. Validated November 26, 2026.

| Check | Result |
| --- | --- |
| Clean clone with the candidate workflow and runner | Exit 0. Documentation and Python checks passed, followed by full dbt parses for pilot, history and recovery. |
| Broken link in the isolated clone | Exit 1. The script named the missing target and stopped before invoking dbt. |
| Project and dataset IAM | The operator has only BigQuery Job User directly at project level and a dataset Writer entry on the inspected raw, models and recovery datasets in US. |
| Credential exposure | The operator has zero user-managed keys. GitHub reports zero repository Actions secrets. |
| Billing | BigQuery project billing was disabled with no linked account. The CI proof ran locally and used no hosted runner minutes. |

The [workflow](../../.github/workflows/local-checks.yml) and
[local entrypoint](../../scripts/check_ci.py) now share one command.
The workflow keeps read-only contents permission, pinned actions and a
checkout without persisted Git credentials. The runner uses a placeholder
project, disables partial parse and telemetry, and passes only the
process variables needed to start dbt. It runs `parse`, which verifies
project configuration and SQL/Jinja structure without running warehouse
queries or tests.

## Reproduce

From a clean checkout, use Python 3.12 and install the
[pinned dbt runtime](../../requirements-dbt-core.txt) into a virtual
environment. Activate it and run:

    python scripts/check_ci.py

For the failure case, add a Markdown link to a nonexistent local file
under `docs/` in a disposable checkout. The same command exits 1 before
printing the first parse target. Remove the probe when done.

## Boundaries

Terraform stays deferred under [D-026](../../DECISIONS.md#d-026--use-a-manual-bootstrap-for-the-single-sandbox).
The repository tracks no Terraform resources or state. Local cloud
operations use the existing OAuth and short-lived impersonation flow.
Cloud CI and GitHub OIDC federation remain deferred. The revised
workflow was exercised through its shared command in a clean local clone.
Hosted execution of this revision was skipped for the private delivery.
