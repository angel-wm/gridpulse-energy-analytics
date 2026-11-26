# Phase 1 foundation runbook

Use this runbook to reproduce the local environment and verify the dedicated
BigQuery Sandbox project before the ingestion phase. The
[validation record](validation/phase-1-foundation.md) distinguishes the checks
that ran from those that still need a target project.

## Local environment

Install Python 3.12 and Git. From the repository root in PowerShell, create an
isolated environment and install the pinned dbt runtime and dependencies:

    python --version
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements-dbt.txt
    .\.venv\Scripts\python.exe -m pip check
    .\.venv\Scripts\dbt.exe --version
    .\.venv\Scripts\python.exe scripts/check_local.py

Expected dbt version: `2.0.13`. The virtual environment isolates the tools
from other projects. The static checks need only the Python standard library
and can also run as `python scripts/check_local.py` before installing dbt.

The GitHub Actions workflow runs that same static command on a standard
runner for pull requests and pushes to `main`. It uses read-only repository
permissions and does not authenticate to GCP, install dbt, or download
source data. Standard runners on the current public repository are covered
by the [GitHub Actions free usage policy](https://docs.github.com/en/actions/concepts/billing-and-usage).
Recheck runner eligibility if visibility or runner configuration changes.
Use the local command if hosted execution cannot be kept free.

## Verify an unbilled Sandbox target

A **project** is the boundary for access, quotas, and the billing account.
Inside the project, a **dataset** groups tables and views. Phase 1 identifies
and verifies the project. The March pilot dataset and table belong to later
authorized work.

The dedicated project is **GridPulse Sandbox**, created with the account
selected by the owner. The [validation record](validation/phase-1-foundation.md)
records its verified Sandbox and billing state. To recreate the project
in another authorized environment, use the
[BigQuery Sandbox project flow](https://docs.cloud.google.com/bigquery/docs/sandbox).
Stop and record a blocker if the account or organization requires billing
or a trial.

For the intended project, check Google Cloud Billing for the absence of a
linked billing account, and check that BigQuery shows it as Sandbox. For
repeatable verification once the [Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk)
and local OAuth are available:

    $gridProject = '<verified-gridpulse-project-id>'
    gcloud billing projects describe $gridProject --format='json(billingEnabled,billingAccountName)'

Require a successful command with `billingEnabled` equal to `false` and
`billingAccountName` empty or absent. A permission error or unreadable project
does not establish billing status. Record the check and outcome without tokens,
account identifiers, or credentials. [Google Cloud billing status documentation](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled)

For the later pilot, distinguish setup permissions from day-to-day execution.
The job identity needs BigQuery Job User for the project and only the
necessary read and write access on its datasets. Use user OAuth and keep
Application Default Credentials outside Git. Verify actual access on the
designated project before any load. Keep Terraform and cloud CI deferred
until there is a verified unbilled environment and a justified resource
or automation scope. [Phase 0 identity and infrastructure design](phase-0-design-baseline.md#identity-infrastructure-and-ci)
