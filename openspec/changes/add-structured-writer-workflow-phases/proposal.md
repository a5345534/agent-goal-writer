# add-structured-writer-workflow-phases

## Why

The current value-gated writer workflow gives `goal-spec` a useful pre-spec checkpoint, but the state model is still mostly a single gate artifact. That is enough to block obviously incomplete goals, but it is not enough to make a long clarification/value-debate session reliably resumable, inspectable, or self-correcting.

The Omnigent review surfaced several reusable architecture patterns that fit this repo without turning the writer into a full autonomous ReAct framework:

- phase-based planning state for explicit progress and skip conditions;
- extract → reflect → recover processing after user/source input;
- structured claim/reasoning graph for load-bearing preservation;
- loop/circuit-breaker controls to avoid endless clarification or repeated challenges;
- registry-style extension points for workflow checks, prompts, and project policy adapters.

This change specifies how to evolve the writer workflow from a flat value gate into a structured, phase-aware workspace capability while keeping OpenSpec markdown/spec files as the governed source of truth.

## What Changes

- Extend workspace-local `.writer-workflow/changes/<change-name>/` state with a phase-aware workflow model.
- Add an extract/reflect/recover pipeline for goal intake and source material before OpenSpec writing.
- Add a claim graph that links user/source claims to proposal/design/tasks/spec destinations.
- Add clarification-loop and challenge-loop guardrails with deterministic limits and fallback recommendations.
- Add a registry-style configuration surface for phase templates, gate checks, extractors, reflectors, recovery strategies, and preservation rules.
- Keep Omnigent as inspiration only; no runtime dependency or code copy is introduced by this change.

## Impact

- Affected specs: `goal-spec-workflow`
- Affected modules/repos: `goal-spec` skill instructions, `scripts/goal-spec-workflow`, tests, README, and OpenSpec closeout artifacts
- Affected APIs/events/data: workspace-local workflow JSON schema under `.writer-workflow/changes/<change-name>/`; no public API or event contract
- Migration/deployment impact: Existing `value-gate.json` workflows remain readable; new fields are additive and should default safely.
- User-visible impact: Users get more stable clarification sessions, fewer repeated questions, clearer value-challenge rationale, and better preservation of decisions into OpenSpec.

## Non-Goals

- Do not adopt Omnigent as a dependency.
- Do not implement a full autonomous ReAct loop or tool-calling agent inside `goal-spec`.
- Do not replace Pi/goal-planner model routing with an internal LLM router.
- Do not make `.writer-workflow/` authoritative over OpenSpec markdown/spec files.
- Do not introduce plugin loading or checksum enforcement in this change; registry-style extension points are enough.

## Success Signal

A non-trivial, ambiguous writer request can be resumed from `.writer-workflow/changes/<change-name>/workflow-state.json`; the helper can show active phase, completed steps, repeated-question/challenge counts, extracted claims, reflection/recovery recommendations, and claim preservation status. `write-spec` remains blocked until the pre-spec gate passes or acknowledged assumptions are recorded, and resulting OpenSpec files include the load-bearing value debate and claim graph outputs.

## Assumptions

- [ASSUMPTION] The existing `value-gate.json` can remain as a compatibility input while `workflow-state.json` becomes the richer phase-aware state.
- [ASSUMPTION] The first implementation can use deterministic extractors/checks and templated reflection/recovery rules; LLM-assisted reflection can be deferred.
- [ASSUMPTION] Registry-style extension can start as Python data structures in the bundled helper rather than a plugin system.

## Open Questions

- [ ] Should `workflow-state.json` replace `value-gate.json` as the primary state file immediately, or should both be written for one release cycle?
