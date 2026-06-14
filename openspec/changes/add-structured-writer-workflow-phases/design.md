# Design: add-structured-writer-workflow-phases

## Context

The current writer workflow has established the right boundary: `.writer-workflow/changes/<change-name>/` is workspace-local operational state, while `openspec/changes/<change-name>/` remains the governed source package. The next limitation is the shape of that operational state.

A single value-gate artifact can answer “is this complete enough to write a spec?”, but it cannot fully answer:

- Which clarification/value-challenge phase is active?
- Which stage was skipped, completed, or blocked?
- Which user/source claims are load-bearing?
- Which claims landed in proposal/design/tasks/spec?
- Which repeated questions or challenges should stop and fall back to a decision path?
- Which recovery question should be asked next?

Omnigent demonstrates useful production patterns for this class of problem: phase-based planning, structured memory, extract/reflect/recover post-processing, reasoning graphs, and loop/circuit breakers. This change borrows those patterns at the workflow-script level without adopting Omnigent code, dependencies, or a full autonomous ReAct loop.

## Spec Kernel

- Why: Make value-gated OpenSpec authoring resumable, inspectable, non-repetitive, and better at preserving load-bearing claims.
- Capabilities:
  - Track writer workflow phases and step status per change.
  - Extract structured claims and value-frame fields from user/source input.
  - Reflect on value/scope/risk gaps and recommend the next recovery action.
  - Track load-bearing claims through a claim graph into OpenSpec artifacts.
  - Detect repeated clarification/challenge loops and force a decision path.
  - Allow registry-style configuration of phase templates and deterministic checks.
- Constraints:
  - `.writer-workflow/changes/<change-name>/` remains workspace-local operational state.
  - OpenSpec markdown/spec files remain the authoritative governed source.
  - No Omnigent runtime dependency or copied implementation code.
  - Existing `init/check/gate/write-spec` commands remain compatible.
  - The helper continues to use Python standard library automation.
- Non-goals:
  - No full autonomous ReAct loop.
  - No internal multi-provider LLM router.
  - No plugin loading or checksum system in this change.
- Success signal: The helper can resume and report phase progress, extracted claims, reflection/recovery advice, loop guard state, and claim preservation status before allowing OpenSpec writing.

## Goals

- Add phase-aware workflow state without breaking existing value-gate usage.
- Make clarification and value challenge progress explicit and resumable.
- Improve source-to-spec preservation with a claim graph.
- Add bounded dialogue guardrails so the writer challenges constructively without looping forever.
- Keep the implementation small, deterministic, and package-friendly.

## Non-Goals

- Rewriting `agent-goal-writer` as a general autonomous agent framework.
- Copying Omnigent code or relying on Omnigent as a dependency.
- Replacing `openspec-build-source-manifest`, explainer validation, or archive preflight helpers.
- Treating workflow-state files as OpenSpec archive targets.

## Concern Scan

| Concern | Relevance | Design response |
| --- | --- | --- |
| Compatibility | Existing value-gated workflow already works and has tests. | Add `workflow-state.json` as additive state; continue reading/writing `value-gate.json` during transition. |
| Over-formalization | Writer should not become a heavy autonomous framework. | Borrow phase/state concepts only; no ReAct loop, router, or plugin system. |
| Source-of-truth boundary | Operational state could be mistaken for governed spec. | Mark workflow files as workspace-local; require load-bearing outputs to land in OpenSpec sources. |
| Repeated questioning | Critical collaborator behavior can become friction. | Add loop counters and fallback paths after repeated clarification/challenge turns. |
| False confidence | Deterministic extraction cannot understand all value nuance. | Reflection/recovery outputs are advisory unless the gate check marks a blocker; assumptions remain explicit. |
| Package constraints | This skill should remain self-contained. | Use only Python standard library and bundled scripts. |

## Decisions

### D1. Add `workflow-state.json` as the phase-aware state root

**Choice**
Add a new workspace-local state file:

```text
.writer-workflow/changes/<change-name>/workflow-state.json
```

Initial shape:

```json
{
  "schemaVersion": "1.1",
  "changeName": "add-structured-writer-workflow-phases",
  "capability": "agent-goal-writer-workflow",
  "activePhase": "value_challenge",
  "phases": [
    {
      "id": "intake",
      "status": "complete",
      "steps": [
        {"id": "raw_goal", "status": "complete", "summary": "Raw goal captured"},
        {"id": "stakes", "status": "complete", "summary": "Internal workflow/tooling"}
      ],
      "skipCondition": ""
    },
    {
      "id": "value_challenge",
      "status": "active",
      "steps": [
        {"id": "no_build", "status": "pending", "summary": ""},
        {"id": "smaller_scope", "status": "pending", "summary": ""}
      ],
      "skipCondition": "low_stakes_and_value_confirmed"
    }
  ],
  "loopGuards": {
    "clarificationTurns": 0,
    "challengeTurns": 0,
    "repeatedQuestionHashes": [],
    "maxClarificationTurns": 3,
    "maxChallengeTurns": 2
  },
  "updatedAt": "2026-06-13T00:00:00Z"
}
```

Supported phase statuses:

- `pending`
- `active`
- `complete`
- `skipped`
- `blocked`

Default phases:

1. `intake`
2. `value_challenge`
3. `clarification`
4. `spec_kernel`
5. `pre_spec_gate`
6. `openspec_write`
7. `validation`

**Rationale**
This borrows Omnigent's phase planner shape while keeping the workflow helper deterministic and lightweight.

**Alternatives considered**
- Keep only `value-gate.json`: rejected because it cannot represent phase progress, loop limits, or claim preservation.
- Replace `value-gate.json` immediately: deferred to avoid breaking current scripts/tests.
- Use DAG runtime state: rejected because this is authoring workflow state, not execution planning.

### D2. Add an extract/reflect/recover pipeline for pre-spec input processing

**Choice**
Add deterministic pipeline outputs under the workflow state directory:

```text
extracted-claims.json
reflection-report.json
recovery-actions.json
```

Pipeline responsibilities:

1. **Extract**: parse user/source text into structured items:
   - problem/opportunity;
   - beneficiary;
   - desired outcome;
   - proposed solution;
   - constraints;
   - success signal;
   - assumptions;
   - open questions;
   - no-build and smaller-scope candidates.
2. **Reflect**: evaluate extracted items for value, scope, risk, evidence, and verification gaps.
3. **Recover**: recommend one next action:
   - ask one focused question;
   - recommend no-build;
   - recommend smaller-scope;
   - proceed with assumptions;
   - block until a high-stakes decision is made;
   - proceed to pre-spec gate.

**Rationale**
Omnigent's extractor/reflector/recovery split maps cleanly to writer authoring. It makes the writer's critique visible and testable without requiring a new autonomous loop.

**Alternatives considered**
- Put all critique in the prompt only: rejected because it is hard to test or resume.
- Use LLM reflection immediately: deferred; deterministic first keeps the helper self-contained.

### D3. Add a claim graph for load-bearing preservation

**Choice**
Add:

```text
claim-graph.json
```

Initial shape:

```json
{
  "schemaVersion": "1.0",
  "claims": [
    {
      "id": "claim-001",
      "text": "The writer should challenge whether a goal is worth doing.",
      "kind": "value_constraint",
      "source": "user",
      "loadBearing": true,
      "status": "preserved",
      "destinations": [
        {"file": "proposal.md", "section": "Why"},
        {"file": "design.md", "section": "Decisions"},
        {"file": "specs/agent-goal-writer-workflow/spec.md", "section": "Value Challenge Gate"}
      ]
    }
  ],
  "edges": [
    {"from": "claim-001", "to": "requirement-value-challenge", "relation": "justifies"}
  ]
}
```

The helper should report blockers when a load-bearing claim remains unpreserved before validation/closeout.

**Rationale**
This adapts Omnigent's reasoning graph idea from “confirmed finding activates next path” into “source claim must land in governed OpenSpec artifacts”.

**Alternatives considered**
- Keep preservation notes only in `design.md`: useful but insufficient for deterministic checks.
- Make HTML explainer the preservation map: rejected because explainer is not authoritative.

### D4. Add bounded clarification/challenge loop guards

**Choice**
Track repeated clarification and challenge turns with hashes of normalized question/challenge text. Defaults:

- `maxClarificationTurns`: 3
- `maxChallengeTurns`: 2
- repeated identical question/challenge blocks the next repeat and requires a fallback recommendation.

Fallback recommendations:

- `ask_user_to_choose`: when multiple viable paths remain;
- `proceed_with_assumptions`: when uncertainty is acceptable and acknowledged;
- `smaller_scope`: when the request is too broad;
- `no_build`: when value is not established;
- `block_high_stakes`: when unresolved risk is irreversible or high stakes.

**Rationale**
This preserves the critical-collaborator stance without letting the writer become argumentative or stuck.

**Alternatives considered**
- Unlimited coaching path: rejected because it can waste user time.
- Always fast-path after one question: rejected because high-stakes changes need deeper challenge.

### D5. Add registry-style extension points without plugin loading

**Choice**
Introduce internal registry-style data structures in the helper module:

```python
WORKFLOW_PHASE_TEMPLATES = {...}
GATE_CHECKS = {...}
EXTRACTORS = {...}
REFLECTORS = {...}
RECOVERY_STRATEGIES = {...}
PRESERVATION_RULES = {...}
```

Future project-local policy may be loaded from config, but this change should not add arbitrary Python plugin loading.

**Rationale**
Omnigent's `DomainRegistry` avoids global behavior leaks and centralizes customization. We can adopt the same organization pattern without the security and packaging overhead of plugins.

**Alternatives considered**
- Hard-code all checks inline: rejected because the helper is already growing.
- Full plugin system with checksums: deferred; not needed for the current skill.

## Detailed Design

### Data / Contract Changes

New workspace-local artifacts under `.writer-workflow/changes/<change-name>/`:

| File | Purpose | Authority |
| --- | --- | --- |
| `workflow-state.json` | phase/step progress, active phase, loop guards | operational only |
| `extracted-claims.json` | structured claims and value-frame extraction | operational only |
| `reflection-report.json` | deterministic critique of value/scope/risk gaps | operational only |
| `recovery-actions.json` | recommended next action after blockers/gaps | operational only |
| `claim-graph.json` | load-bearing claim preservation map | operational evidence; OpenSpec remains authoritative |

Existing files remain valid:

- `value-gate.json`
- `spec-kernel.md`
- `status.json`
- `pre-spec-gate.json`
- `write-spec-status.json`

### Execution Flow

1. `init <change-name>` creates the existing value-gate files and the new phase-aware files.
2. The agent records user/source input.
3. `extract` logic updates `extracted-claims.json` and relevant value-frame fields.
4. `reflect` logic writes `reflection-report.json` with gaps, risks, and warnings.
5. `recover` logic writes `recovery-actions.json` with one recommended next step.
6. The agent continues dialogue, updates phase/step status, and loop guards prevent repeated questions/challenges.
7. The agent updates `claim-graph.json` as claims are preserved or deferred.
8. `gate <change-name> --pre-spec` checks both value-gate completeness and phase/claim-graph blockers.
9. `write-spec <change-name>` writes starter OpenSpec files only after pass or acknowledged assumptions.
10. Source manifest, explainer validation, and archive preflight remain the final OpenSpec gates.

### Module Boundaries

- `SKILL.md` owns prompt-level behavior: when to challenge, when to proceed, and what must be preserved.
- `scripts/agent-goal-writer-workflow` owns deterministic workspace-state artifacts and gate checks.
- `scripts/openspec-*` helpers own manifest, explainer, and archive validation.
- `.writer-workflow/changes/<change-name>/` is workspace-local and should stay out of governed OpenSpec sources except as summarized in proposal/design/tasks/spec.

### Migration / Rollout

- Keep `value-gate.json` as the compatibility artifact.
- Add `workflow-state.json` and related files on new `init` runs.
- For existing workflow directories, `check` may synthesize default phase state from `value-gate.json` or report a warning with a migration suggestion.
- Existing OpenSpec change packages remain valid.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Workflow helper becomes too complex. | Medium | Keep Omnigent concepts as small data structures, not a full agent loop. |
| Deterministic extraction misses nuanced claims. | Medium | Treat extraction as advisory; allow agent edits and assumptions. |
| Claim graph adds maintenance burden. | Medium | Only require preservation checks for load-bearing claims. |
| Loop guards prematurely stop useful coaching. | Low | Defaults are configurable and fallback paths preserve progress. |
| Registry structure becomes pseudo-plugin system. | Low | No dynamic Python loading in this change. |

## Verification Plan

- Add unit/fixture checks that `init <change-name>` creates the new phase-aware files under `.writer-workflow/changes/<change-name>/`.
- Verify `check <change-name>` reports active phase and missing required phase/claim data.
- Verify repeated normalized clarification/challenge text increments loop guards and blocks repeated prompts after the limit.
- Verify recovery output recommends exactly one next action.
- Verify `gate <change-name> --pre-spec` blocks when a load-bearing claim is unpreserved.
- Verify `write-spec <change-name>` succeeds only after value gate and claim preservation blockers are cleared or acknowledged.
- Run `scripts/test-workflow`.
- Refresh and validate `source-manifest.json`.
- Validate `change-explainer.html` with the bundled strict decision-review validator.

## Load-Bearing Preservation Notes

- User asked whether Omnigent has useful ideas → preserved as explicit Omnigent-inspired but dependency-free design.
- Valuable Omnigent patterns identified: phase planner, registry pattern, extract/reflect/recover, reasoning graph, loop/circuit breaker, context/state preservation → mapped into workflow-state, registry-style structures, claim graph, and loop guards.
- User boundary from prior discussion: `.writer-workflow/` is workspace capability, not OpenSpec package content → preserved by keeping all new artifacts under `.writer-workflow/changes/<change-name>/` and marking them operational.
- Existing skill rule: OpenSpec markdown/spec files remain source of truth → preserved in authority and module boundary sections.
