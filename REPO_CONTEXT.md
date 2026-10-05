# Repository context

## Project

- Project: GridPulse — Cloud Energy Analytics Platform.
- Convention version: **0.1**.
- Description: [README](README.md).
- Work Unit: **phase**.
- Work Model: [roadmap rules](ROADMAP.md#phase-rules).

## Published state

Publication/handoff source:
[Current State](CURRENT_STATE.md#state) and the relevant phase handoff selected
from that state.

Canonical repository:
`https://github.com/angel-wm/gridpulse-energy-analytics`

Default handoff branch: `main`.

Until the first push to the canonical repository is confirmed, publication
status remains **Unknown**.

Remote readers describe only the published snapshot they can retrieve.
Unseen local work is **Unknown**.

Local readers must distinguish:

- working-tree changes;
- local commits;
- pushed commits;
- published handoff state.

A clean working tree or local commit alone does not prove publication.

Do not maintain a copied "latest commit" value in this file.

## Source map

| Topic / purpose | Source | Authority | Read when |
| --- | --- | --- | --- |
| State / Current Work | [CURRENT_STATE.md](CURRENT_STATE.md); select the phase explicitly marked current | Authoritative for recorded project and phase state | Understanding current state, resuming work, or selecting work to review |
| Last Completed Work | [CURRENT_STATE.md](CURRENT_STATE.md), then the handoff explicitly named there under `docs/handoffs/` | State selects the last closed phase; its handoff records closure and transfer context | Latest completion, continuation, or predecessor context matters |
| Planned Work | [ROADMAP.md](ROADMAP.md) | Authoritative for recorded phase order, scope, dependencies, and phase rules; planning is not authorization | Planning next work or evaluating dependencies |
| Project Scope / Requirements | [PROJECT_SPEC.md](PROJECT_SPEC.md) | Authoritative for approved project purpose, constraints, requirements, learning goals, and success criteria | Scope, requirements, technology-role, or acceptance questions |
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) | Authoritative for intended architecture; implementation must be verified separately | Architecture questions or work affecting system structure |
| Decisions | [DECISIONS.md](DECISIONS.md); select the relevant decision ID | Authoritative for recorded decisions and supersession | Rationale, historical choice, or proposed architectural change matters |
| Validation / Evidence | Phase-specific record under `docs/validation/`, selected using the phase and baseline from CURRENT_STATE or its handoff | Authoritative only for checks actually recorded at the named baseline | Reviewing work, closing a phase, or auditing evidence |

Use:

- **None** when the project explicitly records that no item exists.
- **Not documented** when no maintained source exists.
- **Unknown** when available information cannot establish the answer.

Missing documentation is not proof that something does not exist.

## Loading rules

- Start with applicable repository guidance, this map, and sources required by
  the task.
- Do not load every document automatically.
- State/resume task: read CURRENT_STATE first.
- Planning task: read CURRENT_STATE, ROADMAP phase rules, and the selected
  phase scope. Read predecessor handoff when required.
- Implementation task: identify the current authorized phase, then read its
  scope, PROJECT_SPEC constraints, relevant ARCHITECTURE sections, applicable
  decisions, and current validation requirements.
- Architecture question: read the relevant ARCHITECTURE section first; expand
  to PROJECT_SPEC and DECISIONS only when required.
- Historical decision: select the relevant decision ID in DECISIONS and follow
  any recorded supersession chain.
- Review or phase closure: read the phase scope, relevant validation record,
  and implementation evidence. Do not infer passing checks from code alone.
- Resolve links relative to this file.
- A directory or filename pattern is a location rule, never an instruction to
  read every file.
- Apply declared topic authority when sources disagree.
- Report unresolved conflicts, inaccessible evidence, and unknowns rather than
  silently inventing or substituting context.
- Stop reading when the sources support the task or identify a specific gap.
- Update this map only when source locations, authority, or loading rules
  change. Routine project state belongs in CURRENT_STATE.
