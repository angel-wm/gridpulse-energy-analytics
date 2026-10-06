# Repository Guidance for AI Assistants and Coding Agents

Before substantial work, read [REPO_CONTEXT.md](REPO_CONTEXT.md) and follow its
task-specific loading rules.

For repository documentation work, use the locally installed
`.agents/skills/repository-documentation-readability/SKILL.md`. Load its
references progressively according to that skill. GridPulse's native semantics,
authority rules, lifecycle, and required structures always take precedence over
presentation guidance.

## Authority

Chat history, assistant memory, Project memory, and previous explanations are
helpful context but are not the durable source of truth for GridPulse.

Use repository sources according to the authority declared in
REPO_CONTEXT.md.

If chat context conflicts with an authoritative repository source:

1. identify the conflict;
2. do not silently choose one;
3. prefer the repository authority unless the user explicitly approves a
   change;
4. record material approved changes in the correct project source.

## Work authorization

GridPulse uses phases.

A planned phase is not authorization to execute it.

Do not begin a new phase unless:

- the user explicitly authorizes it;
- required predecessor phases are closed according to ROADMAP.md;
- required handoff context exists.

Do not automatically begin the next phase after a closeout.

## State and claims

Never claim that:

- code ran successfully;
- infrastructure exists;
- a dataset was loaded;
- a query passed;
- a dbt model/test succeeded;
- Terraform applied successfully;
- CI/CD passed;
- a Power BI report works;
- a deployment or commit is published;

without evidence supporting that exact claim.

Distinguish:

- proposed;
- approved/intended;
- implemented;
- locally validated;
- committed;
- pushed/published;
- deployed.

## Learning-first behavior

This is a portfolio and learning project.

The user should understand and be able to explain the implementation.

For important new concepts, explain:

- what the concept is;
- what problem it solves;
- why it is used here;
- when it is normally used;
- relevant alternatives;
- tradeoffs or limitations.

Do not hide BigQuery learning behind dbt. Teach the relevant native warehouse
concept before or alongside the dbt abstraction.

Do not provide large unexplained code/configuration dumps when incremental
learning is practical.

## Implementation behavior

Work incrementally.

For meaningful implementation changes:

1. identify the current authorized phase;
2. state the component being changed;
3. explain the objective;
4. provide or apply the smallest coherent implementation step;
5. explain how to validate it;
6. use actual validation evidence before calling it successful;
7. update authoritative state only when warranted.

Debugging or educational chats do not automatically change official project
state.

## Architecture and tooling

Do not introduce technologies merely for portfolio breadth.

If a proposed technology is not part of the approved architecture:

1. explain the need;
2. compare reasonable alternatives;
3. request/obtain explicit approval for material architecture changes;
4. record the approved decision in DECISIONS.md.

Prefer a simpler design when it satisfies the approved requirements.

## Changes and decisions

Material changes to architecture, scope, major tooling, project lifecycle, or
phase structure require a recorded decision.

Do not silently rewrite an accepted decision.

If an accepted decision changes, create a superseding decision and preserve
history.

Routine state belongs in CURRENT_STATE.md.

REPO_CONTEXT.md is a map, not a status journal.

## Validation and phase closure

When closing a phase:

- validate against the phase exit criteria;
- record evidence under `docs/validation/`;
- create the phase handoff under `docs/handoffs/`;
- update authoritative documents affected by the work;
- update CURRENT_STATE;
- commit the coherent phase state;
- distinguish local commit from confirmed publication.

A phase is not closed merely because implementation appears finished.

## Repository hygiene

Never commit:

- credentials;
- service-account keys;
- access tokens;
- secrets;
- private configuration containing secrets.

Use examples/templates for secret-bearing configuration.

Keep generated, transient, or large raw artifacts out of Git unless the
project explicitly requires versioning them.

## Multi-chat continuity

Different chats may be used for:

- project control;
- architecture/planning;
- individual phases;
- concept learning;
- debugging;
- documentation;
- final review.

Before continuing stateful work in a new chat, reconstruct context from the
repository rather than assuming previous chat history is complete.

The primary state sources are REPO_CONTEXT.md and CURRENT_STATE.md.

## Output formatting rule

When the user requests:

- "todo en un solo bloque";
- "un solo cuadro";
- "para copiar y pegar";
- "sin ejecutar";
- a complete Markdown document containing code;

return everything inside one outer block.

Use exactly four backticks for the outer opening and closing fence.

Inside that block:

- do not use triple- or quadruple-backtick fences;
- represent internal code blocks with four-space indentation;
- use single backticks for inline snippets;
- close the outer block only at the very end;
- do not place explanatory text outside when the user requested only the block.

Verify the formatting before responding.
