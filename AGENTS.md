# Repository Guidance for AI Assistants and Coding Agents

Before substantial work, read [REPO_CONTEXT.md](REPO_CONTEXT.md) and follow its
task-specific loading rules.

## Authority

Chat history, assistant memory, and previous explanations are not the durable
source of truth for GridPulse.

Use repository sources according to the authority declared in
REPO_CONTEXT.md.

If chat context conflicts with an authoritative repository source, identify
the conflict instead of silently choosing one.

## Work authorization

GridPulse uses phases.

A planned phase is not authorization to execute it.

Do not begin a new phase unless the user explicitly authorizes it and its
required predecessors are closed according to ROADMAP.md.

## Claims

Never claim that:

- code ran successfully;
- infrastructure exists;
- a query passed;
- a test passed;
- a dashboard works;
- a deployment was published;

without evidence supporting the claim.

Distinguish intended, implemented, validated, committed, and published state.

## Changes

Material architectural or scope changes require a recorded decision.

Routine status belongs in CURRENT_STATE.md.

Do not turn REPO_CONTEXT.md into a status journal.

## Handoff

When a phase closes:

- record validation evidence;
- create the phase handoff;
- update CURRENT_STATE;
- update authoritative design/decision documents if required;
- commit the coherent phase state;
- establish publication separately from local completion.
