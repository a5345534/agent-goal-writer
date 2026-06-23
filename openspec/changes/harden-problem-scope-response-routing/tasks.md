# Tasks: harden-problem-scope-response-routing

## 1. Spec and Contract

- [x] 1.1 Update the `goal-spec-workflow` spec delta with first-response routing, framing-only constraints, scope confirmation behavior, invalid decision rejection, artifact-state honesty, user-facing response template requirements, hardened PMA unlock conditions, and response-lint expectations (acceptance: all ten black-box cases have corresponding spec scenarios).
- [x] 1.2 Update `SKILL.md` so the first-response router and Stage 1.5–1.7 templates appear before the general critical-collaborator value challenge guidance.
- [x] 1.3 Update `docs/problem-scope-confirmation-flow.md` with the routing matrix and the distinction between neutral scope candidates and recommendations.
- [x] 1.4 Update `prompts/ideation/problem-scope-framing.md` and `problem-scope-clarification-request.md` with bounded-output templates and forbidden pre-confirmation content.
- [x] 1.5 Confirm affected data contracts for `problem-scope-framing.json`, `problem-scope-clarification-request.json`, `problem-scope-user-gate.json`, and any response-lint report.

## 2. Workflow Helper / Lint Implementation

- [x] 2.1 Add or update deterministic `next-step` routing so selected scope without `confirm_scope_for_analysis` routes only to Stage 1.7 confirmation.
- [x] 2.2 Reject Stage 5 approval decisions such as `approve_openspec_authoring` when the active gate is Stage 1.7.
- [x] 2.3 Ensure `continue_discussion` with unresolved scope uncertainty routes to Problem & Scope Framing rather than value-logic closure assessment.
- [x] 2.4 Implement a deterministic response-lint command (or fixture callable from the bash test runner) that accepts a response string + stage context, emits JSON with `status`/`pass`/`fail`/forbidden phrases/missing decisions, and returns exit code 0 for pass only.
- [x] 2.5 Ensure missing required `inputDigests` remains a blocking freshness failure.
- [x] 2.6 Add persisted-state honesty checks or guidance so agents do not claim artifacts/gates were recorded unless files exist and validate.

## 3. Regression Tests

- [x] 3.1 Add a fixture for improvement intent + scope uncertainty: no no-build/smaller-scope recommendation, no Proposal Meaning Analysis, bounded clarification required.
- [x] 3.2 Add a fixture proving existing functionality cannot cancel improvement intent before scope confirmation.
- [x] 3.3 Add a fixture for bounded clarification request shape: max 1–2 questions, each with bounded options and blocking-field mapping.
- [x] 3.4 Add a fixture where the user selects scope and the response must request `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`.
- [x] 3.5 Add a fixture where `approve_openspec_authoring` at Stage 1.7 is rejected.
- [x] 3.6 Add a fixture where `confirm_scope_for_analysis` unlocks Proposal Meaning Analysis only after the gate decision.
- [x] 3.7 Add fixtures for `revise_scope`, `abandon_proposal`, and `continue_discussion` routing.
- [x] 3.8 Add a fixture where missing `inputDigests` fails freshness validation.
- [x] 3.9 Add a response-lint fixture that validates a known-bad pre-confirmation response (containing no-build/smaller-scope recommendations) fails with exit code non-zero and lists the forbidden phrases.

## 4. Documentation / Closeout

- [x] 4.1 Run `scripts/test-workflow`.
- [x] 4.2 Run the black-box Problem & Scope Confirmation Flow tests against the installed skill path.
- [x] 4.3 Refresh `source-manifest.json`.
- [x] 4.4 Validate `source-manifest.json` with the bundled helper.
- [x] 4.5 Generate and validate `change-explainer.html` if required for review.
- [x] 4.6 Confirm Stage 1 produced only OpenSpec package sources and did not generate downstream execution-plan artifacts.

## Backlog / Follow-ups

- [ ] [BACKLOG] Consider adding a Pi-level response middleware only if prompt/template/lint/test hardening remains insufficient.
- [ ] [BACKLOG] Add multilingual response-lint phrase sets after the English/decision-token structural checks stabilize.
