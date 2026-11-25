# Phase 0 design closeout validation

## Identification

- Phase: **0 — Formal Project Design**
- Baseline: the design files in the same commit as this record, and the six
  EIA snapshots identified in the [source validation](phase-0-eia930.md).
- Validation date: 2026-11-25

## Validation scope

Review the design and its reproducible local evidence against the
[Phase 0 exit criteria](../../ROADMAP.md#exit-criteria). Cloud jobs, dbt
warehouse execution, and Power BI report behavior require evidence in the
implementation phases.

## Checks

| ID | Exit check | Result | Status | Evidence |
| --- | --- | --- | --- | --- |
| V-101 | Scope, audience, KPIs, and source | EIA-930 for ERCO 2023–2025, historical demand and forecast performance, and documented measurement rules | PASS | [Spec](../../PROJECT_SPEC.md#initial-kpi-definitions), [source comparison](../phase-0-design-baseline.md#source-selection), D-022 to D-024 |
| V-102 | Intended architecture and model | Verified input baseline, UTC-keyed hourly design, local-date dimension, controlled CSV handoff | PASS | [Architecture](../../ARCHITECTURE.md), [model and BI contract](../phase-0-design-baseline.md#warehouse-and-report-model) |
| V-103 | USD 0 feasibility and limitations | Assessed the documented Sandbox route. Deferred live load, adapter, export and import checks with a responsible phase and pass condition | PASS | [Feasibility](../phase-0-design-baseline.md#zero-charge-feasibility-and-recovery), [handoff](../handoffs/phase-0-to-1.md#handoff-to-phase-1) |
| V-104 | Lifetime capacity and no-DML strategy | 26,304 raw rows. Estimated about 3.2 MiB for one raw copy and allowed for pilot and rebuilds. Historical snapshot uses batch replacement and views | PASS | [Feasibility](../phase-0-design-baseline.md#zero-charge-feasibility-and-recovery) |
| V-105 | Reproducibility, identity, CI, Terraform | Source manifest and replay steps defined. OAuth and scoped grants are specified. Cloud CI and Terraform applies are gated | PASS | [Identity and rebuild plan](../phase-0-design-baseline.md#identity-infrastructure-and-ci), [pilot tooling](../phase-0-pilot-tooling.md) |
| V-106 | Tooling decisions and later phases | Free local dbt v2.0.13 starts on Windows. Native SQL, model, and cost requirements mapped to implementation gates | PASS | [D-025](../../DECISIONS.md#d-025--adopt-the-erco-design-baseline-with-runtime-gates), [roadmap](../../ROADMAP.md#phase-18-acceptance-criteria) |
| V-107 | Reference metrics and null handling | Reproduced 26,304 unique hours, 26,232 pairs, 72 excluded error rows, and the 743-row March fixture. SQL returned null metrics when no pair existed | PASS | [Source validation](phase-0-eia930.md) |
| V-108 | Live warehouse-to-report pilot | Requires an eligible project, a verified identity, and specific execution authorization | NOT RUN | [Deferred gates](../handoffs/phase-0-to-1.md#handoff-to-phase-1) |
| V-109 | Handoff and repository state | Handoff and CURRENT_STATE are in the same closure snapshot. Publication must be verified against the canonical main branch | PASS | [Handoff](../handoffs/phase-0-to-1.md), [state](../../CURRENT_STATE.md) |

## Reconciliation

The [source validation](phase-0-eia930.md#reconciliation) records expected
counts and metric values. The data profile used the six listed hashes and
wrote a matching pilot CSV on rerun. The new local SQL check used actual
missing rows from the source, with no imputation.

## Limitations

This is a design review and local validation. Storage remains an estimate.
The prior working specification called for runtime demonstration in
Phase 0. The authoritative Roadmap exit criterion allows an explicitly
documented blocker or deferral. D-025 resolves the sequencing and assigns
live tests before the workflow is used for the full dataset.

## Overall result

**PASS for design closeout.** Live Sandbox and Power BI feasibility are
still unverified. This review was performed in the local checkout against
the recorded user choices and source evidence. It is not an independent
external review.

## Closure recommendation

Close Phase 0 when this snapshot is published and independently read back
from the canonical repository. Phase 1 needs new explicit authorization.
