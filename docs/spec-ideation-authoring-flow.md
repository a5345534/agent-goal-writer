# Spec Ideation Authoring Flow

The `goal-spec` skill follows the Spec Ideation Authoring Flow — a canonical,
machine-checkable 15-step workflow that moves from a raw proposal through logic
closure, approval, and OpenSpec writing.

## Stages 0–11

| Stage | Step | Kind | Role / ModelClass |
|-------|------|------|-------------------|
| 0 | Proposal Intake | deterministic | — |
| 1 | Project Modeling | role | collector / evidence-collector |
| 2 | Proposal Meaning Analysis | role | judge / value-judge |
| 3 | Value & Logic Closure Assessment | role | judge / value-judge |
| 4 | Logic Closure Gate | gate | deterministic script |
| 4-1 | Logic Gap Completion | role | judge / value-judge |
| 4-2 | Change Value Assessment Report | role | judge / value-judge |
| 5 | OpenSpec Authoring Approval Gate | gate | deterministic + approver input |
| 6 | Spec Kernel | role | writer / spec-writer |
| 7 | Pre-Spec Gate | gate | deterministic script |
| 8 | OpenSpec Writing | role | writer / spec-writer |
| 9 | Explainer | role | explainer / explainer-writer |
| 10 | Package Review | role | reviewer / strict-reviewer |
| 11 | Handoff Ready Gate | gate | deterministic script |

## Logic Closure Gate

The Logic Closure Gate evaluates whether the proposal has sufficient project
understanding, meaning clarity, and resolved logic gaps to proceed.

- **not_closed** → Logic Gap Completion → clarification → loop back to assessment
- **closed** → Change Value Assessment Report

## Approval Gate

The OpenSpec Authoring Approval Gate records an explicit approval decision.

Allowed decisions:
- `continue_discussion` — loop back
- `abandon_proposal` — terminal, no package
- `accept_no_build_recommendation` — terminal, no package
- `approve_smaller_scope_openspec_authoring` — Writer, limited scope
- `approve_openspec_authoring` — Writer, full scope

## Artifact Freshness

Every downstream artifact records SHA-256 digests of its load-bearing inputs.
Gates fail closed on stale digests. JSON artifacts use canonical JSON hashing
(sorted keys, UTF-8, trailing newline ignored). Markdown files hash exact UTF-8.

## Role-Run Audit

Every semantic artifact is traceable to a role-run record or deterministic
command record. Role-run records include boundary assertions enforcing
collector/judge/writer/reviewer separation.

## Boundary Validators

Stage 1 artifacts must not contain runtime-owned outputs (DAG, trace, worktree,
runtime model binding, concrete model IDs). Allowed references are abstract
`modelClass` values only.

## Scripts

The `scripts/goal-spec-workflow` helper provides deterministic commands for
intake, validation, gate evaluation, freshness checks, and boundary checks.

The deterministic scripts validate and transition only; they do not author
semantic artifacts.
