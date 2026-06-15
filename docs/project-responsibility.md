# Project Responsibility

Status: authoritative project-boundary document for `goal-spec`.

This document defines what this repository owns, what it must not own, and how it hands work to the next repository in the three-stage goal execution pipeline.

## Pipeline position

```text
Stage 1: goal-spec   user goal -> OpenSpec change package
Stage 2: goal-dag    OpenSpec/PRD/design/ticket -> validated Goal DAG JSON + optional trace
Stage 3: goal-runner Goal DAG JSON -> runtime execution
```

`goal-spec` is Stage 1 only. Its job is to turn a user goal, feature request, bug direction, product idea, or architecture decision into governed OpenSpec source material.

## Owns

`goal-spec` owns:

- value challenge before writing a spec;
- discovery, assumptions, alternatives, non-goals, risks, and success signals;
- OpenSpec change package authoring;
- OpenSpec proposal/design/tasks/spec-delta structure;
- `source-manifest.json` creation and validation;
- optional `change-explainer.html` generation and validation when the target project requires it;
- Stage 1 operational workflow artifacts under `.goal-spec/`;
- Execution Handoff Notes as source-grounded evidence for downstream planning.

## Does not own

`goal-spec` must not own or perform:

- `GoalDagSpec` creation;
- `.dag.json` or `.trace.json` generation;
- `/goal` invocation;
- subagent planning or scheduling;
- model routing;
- worktree allocation;
- runtime validation policy;
- execution, implementation, merge, or cleanup behavior;
- goal completion, blocked-state decisions, or lifecycle ledger behavior.

## Inputs

Valid Stage 1 inputs include:

- user goal;
- feature request;
- bugfix direction;
- product idea;
- architecture decision;
- existing OpenSpec change for update/review/archive-preflight modes.

## Outputs

The primary output is:

```text
openspec/changes/<change-name>/
├── .openspec.yaml
├── proposal.md
├── design.md
├── tasks.md
├── source-manifest.json
├── change-explainer.html        # optional / non-authoritative
└── specs/<capability>/spec.md
```

Authoritative downstream sources are:

- `proposal.md`;
- `design.md`;
- `tasks.md`;
- `specs/**/spec.md`.

The handoff index is:

- `source-manifest.json`.

Non-authoritative downstream sources are:

- `change-explainer.html`;
- `.goal-spec/` workflow state;
- scratch notes;
- extracted-claim reports;
- reflection reports;
- recovery reports;
- temporary context files.

Non-authoritative files may help humans review context, but downstream planning must not treat them as source-of-truth requirements unless the same claim is preserved in an authoritative OpenSpec source.

## Handoff to `goal-dag`

When `goal-spec` hands work to `goal-dag`, it must provide a complete OpenSpec change package and a current `source-manifest.json`.

`goal-spec` may add `Execution Handoff Notes` inside `design.md` to help downstream planning. Those notes may describe:

- candidate execution slices;
- source-grounded ordering or dependency evidence;
- validation commands or observable acceptance signals;
- execution-affecting open questions;
- execution non-goals.

`Execution Handoff Notes` must not contain runtime DAG fields or ready-to-execute DAG definitions. In particular, do not write:

- `after` edges as DAG JSON;
- `modelScenario`;
- `modelRouting`;
- `workspaceStrategy`;
- `completionGates`;
- node definitions;
- `.dag.json` output;
- `/goal --dag` commands.

## Drift prevention rules

A change to this repository is suspicious and requires boundary review if it:

- adds a dependency on `goal-dag` or `goal-runner` runtime APIs;
- creates or validates `.dag.json` files;
- invokes `/goal`;
- creates worktrees or subagent sessions;
- executes validators as runtime controller policy;
- decides model routing;
- treats `change-explainer.html` as source of truth;
- treats `.goal-spec/` state as OpenSpec source of truth;
- moves implementation execution into the Stage 1 workflow.

## Reviewer checklist

Before merging a change to `goal-spec`, verify:

- the output is still an OpenSpec change package, not a runtime plan;
- authoritative sources remain `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md`;
- `source-manifest.json` remains the handoff index;
- no `.dag.json` or `.trace.json` generation was introduced;
- no `/goal` invocation was introduced;
- `change-explainer.html` remains non-authoritative;
- execution handoff content is evidence for `goal-dag`, not a substitute for `goal-dag`.
