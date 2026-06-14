# Tasks: add-structured-writer-workflow-phases

## 1. Spec and Skill Contract

- [x] 1.1 Update `SKILL.md` to describe phase-aware workflow state, extract/reflect/recover, claim graph preservation, and loop guard behavior.
- [x] 1.2 Clarify that `.writer-workflow/changes/<change-name>/` remains workspace-local operational state and OpenSpec markdown/spec files remain authoritative.
- [x] 1.3 Document when loop guards should recommend no-build, smaller-scope, blocking question, or `proceed_with_assumptions`.
- [x] 1.4 Update `README.md` with the new workflow-state artifacts and command behavior.

## 2. Workflow State Schema

- [x] 2.1 Extend `scripts/goal-spec-workflow init <change-name>` to create `workflow-state.json` with default phases and loop guards.
- [x] 2.2 Add or update helpers for reading/writing phase status and active phase.
- [x] 2.3 Preserve compatibility with existing `value-gate.json` workflows.
- [x] 2.4 Add migration or warning behavior when existing workflow directories lack `workflow-state.json`.

## 3. Extract / Reflect / Recover Pipeline

- [x] 3.1 Add deterministic extraction into `extracted-claims.json` for goal, beneficiary, problem/opportunity, success signal, constraints, assumptions, open questions, no-build candidate, and smaller-scope candidate.
- [x] 3.2 Add deterministic reflection into `reflection-report.json` for value clarity, scope discipline, risk/boundary gaps, verification gaps, and assumption posture.
- [x] 3.3 Add recovery strategy output into `recovery-actions.json` with exactly one recommended next action.
- [x] 3.4 Ensure recovery actions include no-build, smaller-scope, ask-one-question, proceed-with-assumptions, block-high-stakes, and proceed-to-gate.

## 4. Claim Graph and Preservation Checks

- [x] 4.1 Add `claim-graph.json` with claims, relations, load-bearing status, preservation status, and OpenSpec destinations.
- [x] 4.2 Update `gate <change-name> --pre-spec` to block on unpreserved load-bearing claims unless explicitly acknowledged/deferred.
- [x] 4.3 Ensure `write-spec <change-name>` preserves claim-graph outputs in `proposal.md`, `design.md`, `tasks.md`, or `specs/**/spec.md`.
- [x] 4.4 Add preservation notes to generated `design.md` when claims are deferred or intentionally omitted.

## 5. Loop Guards

- [x] 5.1 Track clarification turn count, challenge turn count, and normalized repeated question/challenge hashes.
- [x] 5.2 Block repeated identical clarification/challenge prompts after the configured limit.
- [x] 5.3 Emit a fallback recommendation when loop limits are reached.
- [x] 5.4 Add configurable defaults for `maxClarificationTurns` and `maxChallengeTurns`.

## 6. Registry-Style Organization

- [x] 6.1 Introduce internal registry-style data structures for phase templates, gate checks, extractors, reflectors, recovery strategies, and preservation rules.
- [x] 6.2 Keep registry behavior static and standard-library only; do not add dynamic plugin loading.
- [x] 6.3 Add tests proving independent change workflow directories do not leak state into each other.

## 7. Tests and Validation

- [x] 7.1 Add fixture coverage for `init <change-name>` creating the new workflow-state artifacts.
- [x] 7.2 Add coverage for phase status transitions and active-phase reporting.
- [x] 7.3 Add coverage for extract/reflect/recover outputs.
- [x] 7.4 Add coverage for claim-graph preservation blockers.
- [x] 7.5 Add coverage for loop guard limits and fallback recommendations.
- [x] 7.6 Run `scripts/test-workflow`.
- [x] 7.7 Refresh `source-manifest.json`.
- [x] 7.8 Validate `change-explainer.html` with the bundled strict decision-review helper.

## Backlog / Follow-ups

- [ ] [BACKLOG] Add optional LLM-assisted reflection once deterministic extraction/reflection is stable.
- [ ] [BACKLOG] Consider project-local policy configuration for registry entries after the static registry shape proves useful.
