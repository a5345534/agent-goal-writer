# Problem & Scope Confirmation Flow

The Problem & Scope Confirmation Flow (stages 1.5–1.7) sits between Project
Modeling (Stage 1) and Proposal Meaning Analysis (Stage 2). Its core principle
is **Scope closure before value judgment**.

## Stages

### 1.5 Problem & Scope Framing

The **judge** (`value-judge`) operates in **framing-only mode** to clarify the
user's problem, intended scope, and improvement intent. Output:
`problem-scope-framing.json`.

The judge MUST NOT recommend no-build, evaluate value, classify as duplicate,
or write OpenSpec during this stage. If the user expresses improvement intent
("make it more complete"), `improvementIntent` must be true. If the user is
unsure about scope, `scopeUncertainty` must be true.

### 1.6 Scope Closure Gate

A **deterministic gate** that verifies `problem-scope-framing.json` is
structurally complete. It does NOT evaluate value, duplicates, or whether
OpenSpec should be written.

- **closed** → routes to Problem-Scope User Confirmation Gate (1.7)
- **not_closed** → routes to Problem Scope Clarification Request (1.6-1)

### 1.6-1 Problem Scope Clarification Request

The **judge** produces bounded questions (max 1–2) when scope is not closed.
Output: `problem-scope-clarification-request.json`.

### 1.6-2 Problem Scope Clarification Response

A **deterministic step** capturing the decision maker's answers.
Output: `problem-scope-clarification-response.json`. After response,
workflow loops back to Stage 1.5 for reframing with clarified scope.

### 1.7 Problem-Scope User Confirmation Gate

The user confirms the defined scope may proceed to Proposal Meaning Analysis.
Output: `problem-scope-user-gate.json`.

Allowed decisions:
- `confirm_scope_for_analysis` → proceed to Stage 2
- `revise_scope` → return to Stage 1.5
- `abandon_proposal` → terminal (NOT treated as no-build)

## Key Rules

- **Scope closure before value judgment**: Proposal Meaning Analysis SHALL NOT
  run until problem-scope-user-gate.json exists with `confirm_scope_for_analysis`
- **No no-build before scope confirmation**: When improvement intent is true,
  existing functionality must not be used to recommend no-build before Stage 1.7
- **Two-gate design**: Scope Closure Gate proves scope is well-formed;
  User Confirmation Gate proves the user accepts it for analysis
