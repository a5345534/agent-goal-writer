# harden-problem-scope-response-routing

## Why

Black-box behavior testing of the `goal-spec` skill showed that the Problem & Scope Confirmation Flow is specified, but first-response behavior can still bypass it before deterministic gates are invoked. In particular, an agent can recommend no-build or smaller-scope while scope is still uncertain, treat a selected scope as confirmed without `confirm_scope_for_analysis`, accept Stage 5 approval decisions at the Stage 1.7 gate, or claim gates/artifacts were recorded when no files were written.

This change turns the current decision into a governed OpenSpec proposal: harden the Stage 1.5–1.7 response contract so first responses are stage-routed, template-constrained, and regression-tested before value judgment, proposal meaning analysis, spec kernel creation, or OpenSpec writing can occur.

## Value Gate

- Outcome: `proceed_to_spec`
- No-build considered: Rejected. The issue is not a product feature request whose value is uncertain; it is a workflow correctness gap demonstrated by black-box tests against an existing Stage 1 contract.
- Smaller-scope considered: The selected scope is limited to Problem & Scope Confirmation Flow response routing, wording constraints, templates, and tests. Later stages remain out of scope except where they must reject premature decisions.
- Assumption posture: Confirmed by the current review discussion; no unresolved value blocker remains.

## What Changes

- Add a first-response state router for Stage 1.5–1.7 conditions.
- Require framing-only responses to list neutral scope candidates and bounded clarification questions without value judgment, no-build, smaller-scope recommendations, proposal meaning analysis, spec kernel content, or OpenSpec writing.
- Require a selected scope to route to the Problem-Scope User Confirmation Gate and ask for exactly `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`.
- Reject approval-type decisions such as `approve_openspec_authoring` before Stage 5.
- Route `confirm_scope_for_analysis`, `revise_scope`, `abandon_proposal`, and `continue_discussion` according to the confirmed flow.
- Require persisted artifacts or explicit “would record” wording before claiming that a gate passed, a decision was recorded, or an artifact was produced.
- Add response-lint as a deterministic helper command or fixture invoked by `scripts/test-workflow`, plus black-box regression coverage for the ten Problem & Scope Confirmation Flow cases.

## Impact

- Affected specs: `goal-spec-workflow`
- Affected modules/repos: `goal-spec` skill instructions, `docs/problem-scope-confirmation-flow.md`, ideation prompts, `scripts/goal-spec-workflow` routing/validation helpers, and `scripts/test-workflow` regression coverage
- Affected APIs/events/data: Workspace-local Stage 1 artifacts and gate validation semantics; no public API or event contract
- Migration/deployment impact: Existing OpenSpec changes remain valid. Agents gain stricter first-response behavior for new or resumed Stage 1 conversations.
- User-visible impact: Users see bounded scope framing first, explicit scope-confirmation choices after selecting scope, and clear rejection of gate-mismatched approval decisions.

## Non-Goals

- Do not remove the critical-collaborator value challenge; it remains available after `confirm_scope_for_analysis` unlocks Proposal Meaning Analysis and downstream value assessment.
- Do not change Stage 5 approval decisions except to reject them when supplied before Stage 5.
- Do not implement `/goal`, Goal DAG output, runtime routing, model binding, or downstream execution planning.
- Do not make `.goal-spec/` workflow artifacts authoritative over OpenSpec markdown/spec sources.
- Do not require a full runtime interceptor outside this repository; the first implementation may combine prompt contract, helper routing, response lint, and regression tests.

## Pipeline Handoff Boundary

- Stage 1 output: governed OpenSpec sources only.
- Downstream consumer: `goal-dag` reads `source-manifest.json` plus the authoritative markdown/spec sources.
- No Goal DAG JSON or execution runtime plan is produced by this package.

## Success Signal

The ten black-box Problem & Scope Confirmation Flow cases pass as regression tests: no pre-confirmation no-build or smaller-scope recommendation, no direct jump from project modeling or selected scope to Proposal Meaning Analysis or Spec Kernel, invalid Stage 1.7 decisions are rejected, `confirm_scope_for_analysis` unlocks Proposal Meaning Analysis, `revise_scope` returns to framing, `abandon_proposal` is terminal but not no-build, `continue_discussion` with scope uncertainty returns to framing, and missing `inputDigests` blocks freshness.

## Assumptions

- None

## Open Questions

- None (response-lint implementation minimum is decided — see design D6).
