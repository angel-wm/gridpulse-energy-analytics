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

## Google Cloud CLI on Windows

The Phase 1 verification uses the official versioned Windows x64 archive
for Google Cloud CLI **594.0.1**, which includes `bq` **2.1.42**. Check the
archive against the SHA-256 on the
[Google Cloud downloads page](https://docs.cloud.google.com/sdk/docs/downloads-versioned-archives)
before extracting it. The local GridPulse install uses a directory under
`LOCALAPPDATA`, with a separate CLI configuration outside the repository.
From PowerShell:

    $gridSdk = Join-Path $env:LOCALAPPDATA 'GridPulseTools/google-cloud-cli-594.0.1/google-cloud-sdk/bin'
    $env:CLOUDSDK_CONFIG = Join-Path $env:LOCALAPPDATA 'GridPulseTools/gcloud-config'
    $gridGcloud = Join-Path $gridSdk 'gcloud.cmd'
    $gridBq = Join-Path $gridSdk 'bq.cmd'
    & $gridGcloud version
    & $gridBq version

Adjust the SDK path if it was extracted elsewhere. Authenticate only once
the operating account has been selected and granted the scoped role. Sign
in through Google's browser flow using `& $gridGcloud auth login`. Keep
that account's credential store outside Git. The local CLI OAuth login
and the future dbt Application Default Credentials setup are distinct.

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
    & $gridGcloud billing projects describe $gridProject --format='json(billingEnabled,billingAccountName)'

Require a successful command with `billingEnabled` equal to `false` and
`billingAccountName` empty or absent. A permission error or unreadable project
does not establish billing status. Record the check and outcome without tokens,
account identifiers, or credentials. [Google Cloud billing status documentation](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled)

## Separate project setup from job execution

The project creator currently holds the general Owner role. Reserve that
account for setup. Confirm a separate user-controlled operating identity
before granting it BigQuery Job User on this project. In the ingestion
phase, grant Data Editor only on the pilot dataset to the raw-load writer.
Add read access on raw and write access on the model dataset for dbt only
when that phase requires them.

Use local user OAuth for CLI execution. When dbt needs Application Default
Credentials, keep them outside Git. Verify the operating principal's
project-level job permission without submitting a query. Then verify
dataset-level access when the authorized dataset exists. Use the
[BigQuery IAM roles](https://docs.cloud.google.com/bigquery/docs/access-control)
and [read-only permission test](https://docs.cloud.google.com/resource-manager/reference/rest/v3/projects/testIamPermissions)
as references.

## Terraform scope

The project uses the documented manual Sandbox creation path for its
single environment (D-026). Evaluate Terraform only when a subsequent
authorized phase has a concrete repeatable need for dataset metadata
or restricted IAM. Cloud CI remains deferred pending the required
identity and cost checks.
