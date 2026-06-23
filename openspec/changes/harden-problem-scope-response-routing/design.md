# Design: harden-problem-scope-response-routing

## Context

The current `goal-spec` documentation already defines the Problem & Scope Confirmation Flow:

1. Stage 1 Project Modeling gathers source evidence.
2. Stage 1.5 Problem & Scope Framing runs in framing-only mode.
3. Stage 1.6 Scope Closure Gate checks structural closure.
4. Stage 1.7 Problem-Scope User Confirmation Gate accepts only `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`.
5. Stage 2 Proposal Meaning Analysis is blocked until Stage 1.7 passes with `confirm_scope_for_analysis`.

The deterministic helper already validates several artifact-level rules, including scope closure, invalid Stage 1.7 decisions, stale digests, and missing canonical prerequisites. The gap is earlier: a natural-language first response can still skip or blur these gates before an artifact is written. Black-box tests found responses that performed value challenge while scope was uncertain, recommended no-build or smaller-scope before confirmation, treated a selected scope as final confirmation, accepted `approve_openspec_authoring` at Stage 1.7, or claimed a gate/artifact was recorded without persistence.

## Spec Kernel

- Why: Make the first response obey the same Problem & Scope Confirmation Flow as the deterministic artifacts.
- Value gate outcome: `proceed_to_spec`
- Capabilities:
  - Route Stage 1.5–1.7 first responses from explicit state conditions.
  - Keep framing-only output neutral until the user confirms scope for analysis.
  - Require bounded clarification questions and exact confirmation decisions.
  - Reject gate-mismatched decisions before they can advance the workflow.
  - Lint and regression-test response text for premature value judgment, spec-kernel creation, artifact claims, and freshness acceptance.
- Constraints:
  - Preserve the critical-collaborator value challenge after the scope confirmation gate.
  - Preserve deterministic artifact gates as the source of machine-checkable state.
  - Do not introduce runtime/DAG behavior or concrete model IDs.
  - Do not claim artifacts or gate records exist unless written and validated.
- Non-goals:
  - No change to downstream Goal DAG planning.
  - No replacement of OpenSpec markdown/spec files as authoritative sources.
  - No removal of no-build/smaller-scope recommendations after the proper value-analysis stage.
- Success signal: The ten black-box flow tests and response-lint checks pass.

## Goals

- Make Stage 1.5 framing-only behavior unambiguous and testable.
- Separate neutral scope candidates from value recommendations.
- Prevent scope selection from skipping the user confirmation gate.
- Prevent Stage 5 approval language from being accepted at Stage 1.7.
- Preserve artifact freshness enforcement for all downstream semantic artifacts.
- Stop agents from overstating unpersisted workflow state.

## Non-Goals

- Do not turn `goal-spec` into a runtime conversation middleware outside the skill/helper package.
- Do not make the deterministic scripts author semantic artifacts.
- Do not weaken value assessment, no-build, or smaller-scope analysis once the flow reaches the proper stages.

## Concern Scan

| Concern | Relevance | Design response |
| --- | --- | --- |
| Prompt-only rules are soft | The failures happened in natural-language first responses. | Add a router matrix, fixed templates, response-lint checks, and black-box regression tests in addition to prompt text. |
| Critical collaborator may be suppressed too much | The skill must still challenge low-value or over-scoped work. | The ban applies only before `confirm_scope_for_analysis`; value challenge remains required after scope confirmation and Proposal Meaning Analysis. |
| Scope options can become recommendations | Stage 1.5 may need to present options without judging them. | Define neutral `scopeCandidates`; disallow ranking, “recommended path”, value scores, no-build, or smaller-scope recommendation language. |
| Resumed conversations can hallucinate state | Users may say “continuing” without persisted artifacts. | Require artifact-backed state before claiming current stage, gate pass, or recorded decisions; otherwise restart from framing or ask for artifacts/change name. |
| Response lint can be brittle | Phrase detection can over-block legitimate explanations. | Keep lint focused on stage-specific forbidden claims and required routing phrases; allow prohibited terms only when framed as “not doing yet” or invalid choices. |

## Decisions

### D1. Introduce a first-response state router for Stage 1.5–1.7

**Choice**
Add a routing contract that every response must apply before producing user-visible content:

| Condition | Allowed response |
| --- | --- |
| Scope uncertain or `scopeUncertainty=true` | Stage 1.5 Problem & Scope Framing only; if not closed, Stage 1.6-1 bounded clarification request. |
| User selected a scope but did not provide `confirm_scope_for_analysis` | Summarize selected scope and request exactly `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`. |
| User provides `confirm_scope_for_analysis` | Stage 2 Proposal Meaning Analysis may proceed, subject to artifact/input availability. |
| User provides `revise_scope` | Return to Stage 1.5 framing. |
| User provides `abandon_proposal` | Terminate the proposal; do not label it no-build. |
| User provides Stage 5 approval before Stage 5 | Reject as invalid for Stage 1.7 and show the three valid Stage 1.7 decisions. |
| User chooses `continue_discussion` while scope is uncertain | Return to Stage 1.5 framing/clarification, not Value & Logic Closure Assessment. |
| Required `inputDigests` are missing | Block freshness; do not accept the artifact. |

**Rationale**
The flow already has machine-checkable states, but the first response needs the same decision table so it cannot drift into value analysis or writing before the gate.

**Alternatives considered**
- Prompt reminder only: rejected because black-box tests showed reminders are insufficient.
- Runtime interceptor outside this package: deferred; this change can harden the skill/helper first.

### D2. Define framing-only output templates

**Choice**
Stage 1.5 and Stage 1.6-1 responses must use constrained sections:

```text
Problem & Scope Framing
- Intended outcome:
- Improvement intent:
- Scope uncertainty:
- Current baseline / source context:

Neutral scope candidates:
A. <scope> — included/excluded/success signal/trade-off
B. <scope> — included/excluded/success signal/trade-off

Blocking clarification:
1. <bounded question mapped to blocking field>
   Options: A / B / C
2. <bounded question mapped to blocking field>
   Options: A / B / C

Not doing yet:
- no value judgment
- no no-build recommendation
- no smaller-scope recommendation
- no Proposal Meaning Analysis
- no Spec Kernel or OpenSpec writing
```

After a user chooses a scope, the response must use:

```text
Selected scope: <scope summary>
Before Proposal Meaning Analysis, choose exactly one:
- confirm_scope_for_analysis
- revise_scope
- abandon_proposal
```

**Rationale**
Templates reduce ambiguity and give response-lint clear required/forbidden markers.

**Alternatives considered**
- Let each agent phrase the flow freely: rejected because phrasing drift caused premature recommendations.

### D3. Separate neutral scope candidates from recommendations

**Choice**
Before `confirm_scope_for_analysis`, the agent may list scope candidates with included changes, excluded changes, success signal, and trade-off. It must not:

- call one option “recommended”;
- label a candidate “best” or “highest value”;
- rank options by value or complexity as a decision recommendation;
- propose no-build or measure-first as a recommended path;
- use existing functionality to cancel improvement intent.

Existing functionality may only be used as baseline context and scope boundary evidence during framing.

**Rationale**
The core rule is scope closure before value judgment. Candidates help users decide scope; recommendations evaluate value and therefore belong later.

**Alternatives considered**
- Allow smaller-scope recommendation during framing: rejected because it bypasses Stage 1.7 and produced failing black-box results.

### D4. Require persisted-state honesty in resumed conversations

**Choice**
If a user says “continuing” but the agent has no matching `.goal-spec/changes/<change-name>/workflow-state.json` and relevant gate artifacts, the agent must not claim a stage, gate pass, or recorded decision. It may say:

- “I do not see persisted workflow state for this change.”
- “Based on your message, I would route this to <stage>.”
- “Please provide the change name/artifacts, or I will restart from Problem & Scope Framing.”

When the user asks not to write files, the agent must not say “recorded”, “created”, “gate passes”, or “artifact produced” unless those artifacts already exist and were validated. It must use “would record” or “next artifact would be”.

**Rationale**
This prevents false audit trails and stage hallucination in black-box or fresh-session tests.

**Alternatives considered**
- Trust user-provided continuation claims as state: rejected because it allowed Stage 5 approval to be accepted at Stage 1.7.

### D5. Add response lint and regression coverage

**Choice**
Add tests that assert first-response behavior for the ten black-box cases:

1. improvement intent + scope uncertainty;
2. existing functionality cannot cancel improvement intent;
3. bounded clarification request;
4. selected scope requires user confirmation;
5. approval-type decision rejected at Stage 1.7;
6. `confirm_scope_for_analysis` unlocks Proposal Meaning Analysis;
7. `revise_scope` returns to framing;
8. `abandon_proposal` is terminal but not no-build;
9. `continue_discussion` with scope uncertainty returns to framing;
10. missing required `inputDigests` fails.

Response lint should inspect stage-specific forbidden and required features:

- forbidden before confirmation: no-build recommendation, smaller-scope recommendation, Value Challenge heading, recommended path, Proposal Meaning Analysis output, Spec Kernel, OpenSpec writing/scaffolding;
- required after scope selection: exact `confirm_scope_for_analysis`, `revise_scope`, `abandon_proposal` choices;
- required for invalid Stage 1.7 approval: rejection plus valid Stage 1.7 choices;
- required for missing digests: blocking freshness failure.

**Rationale**
The failure mode is observable at the response level, so it needs response-level tests, not only artifact tests.

**Alternatives considered**
- Only expand unit tests for helper commands: insufficient because the observed failures happened before helper commands were invoked.

### D6. Response-lint minimum implementation contract

**Choice**
Response lint shall be delivered as a deterministic helper command (or fixture) that is invoked by `scripts/test-workflow`. The minimum contract is:

- Accept a plain-text response string and a stage context (pre-confirmation, scope-selected, etc.).
- Emit JSON with `status` (`pass` / `fail`), detected stage, forbidden phrases found, and missing required decisions.
- Return exit code 0 for `pass`, non-zero for `fail`.
- Be callable from the existing bash test runner.

A companion black-box test runner may invoke the installed skill end-to-end, but the deterministic response-lint command is the floor — an implementation that delivers only prompt/docs changes without a testable lint contract is incomplete.

**Rationale**
Leaving the implementation locus as an open question would allow a docs-only or test-harness-only change to claim completion. A minimum testable contract prevents that.

**Alternatives considered**
- Test-harness-only fixture without a standalone command: rejected because black-box fixture coverage depends on model availability; the deterministic lint can run offline.

## Detailed Design

### Data / Contract Changes

Potential new or updated helper outputs:

| Contract | Change |
| --- | --- |
| `problem-scope-framing.json.boundaryAssertions` | Ensure it includes no value judgment, no no-build recommendation, no OpenSpec writing, no runtime planning, and no concrete model ID. |
| `problem-scope-clarification-request.json.questionsForUser` | Enforce max 1–2 bounded questions, each mapped to a blocking field. |
| `problem-scope-user-gate.json.decision` | Continue allowing only `confirm_scope_for_analysis`, `revise_scope`, and `abandon_proposal`. |
| response-lint report | New test/helper output that records `pass`/`fail`, forbidden phrases, missing required decisions, and detected stage. Must be invocable as a deterministic command from `scripts/test-workflow`. |

No public API, event, or runtime contract changes are required.

### Execution Flow

1. Agent receives a goal-spec request or continuation.
2. Agent resolves persisted state if available; otherwise it treats user-provided state as unverified context.
3. Agent applies the first-response state router.
4. If scope is uncertain, agent emits only framing/clarification template content.
5. If a scope was selected, agent asks for the exact Stage 1.7 decision set.
6. If `confirm_scope_for_analysis` is provided and required artifacts are available or can be created, agent proceeds to Proposal Meaning Analysis.
7. If invalid approval language appears before Stage 5, agent rejects it and restates valid Stage 1.7 choices.
8. Response-lint tests verify that the response contains required markers and omits stage-forbidden content.
9. Deterministic artifact gates continue enforcing structural closure, freshness, and boundary rules.

### Module Boundaries

- `SKILL.md` owns user-visible routing rules and templates.
- `docs/problem-scope-confirmation-flow.md` owns concise reference documentation.
- `prompts/ideation/problem-scope-framing.md` and `problem-scope-clarification-request.md` own role-specific prompt constraints.
- `scripts/goal-spec-workflow` owns deterministic gate commands, next-step routing, freshness checks, and optional response-lint support.
- `scripts/test-workflow` owns regression coverage.
- OpenSpec sources remain the governed contract for this change.

### Migration / Rollout

- Update docs and prompts first so installed skill behavior is clearer.
- Add response-lint helpers and black-box fixtures without breaking existing command tests.
- Keep existing artifact schemas compatible; add fields only when optional or schema-backed.
- Re-run `scripts/test-workflow` and black-box tests before archive.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Lint blocks legitimate discussion that mentions “no-build” as a prohibited action. | Medium | Allow forbidden terms when explicitly under “Not doing yet” or invalid-decision explanation; block only recommendations or value judgments. |
| Agents still ignore templates in free-form environments. | Medium | Put templates near the top of skill workflow docs and test the installed skill black-box. |
| State-honesty rules add friction for real continuations. | Low | Allow users to provide change name/artifacts; use “would route” wording when state is not persisted. |
| Existing tests overfit English phrases. | Medium | Prefer structural markers, exact decision tokens, and section-level checks over prose-only matching. |

## Verification Plan

- Run `scripts/test-workflow`.
- Add response-lint fixtures for the ten black-box Problem & Scope Confirmation Flow cases.
- Re-run black-box tests against the installed skill path.
- Verify Stage 1.5 responses do not contain pre-confirmation no-build/smaller-scope recommendations or Spec Kernel content.
- Verify selected-scope responses include exactly the Stage 1.7 decision set.
- Verify missing `inputDigests` still blocks freshness.
- Refresh and validate `source-manifest.json`.
- Validate `change-explainer.html` if generated for review.

## Execution Handoff Notes

This section records execution-planning evidence for downstream tools. It is not a DAG and does not assign runtime scheduling.

### Candidate Execution Slices

- Skill/docs contract: update `SKILL.md`, `docs/problem-scope-confirmation-flow.md`, and ideation prompts with router and templates.
- Helper routing/lint: update `scripts/goal-spec-workflow` with response-lint or next-step checks for the routing matrix.
- Regression tests: add black-box/fixture coverage for the ten cases in `scripts/test-workflow` or a companion test runner.

### Ordering / Dependency Evidence

- Helper/lint tests depend on finalized router semantics because assertions must match the allowed-output matrix.
- Black-box installed-skill validation depends on docs/prompt updates because it tests natural-language behavior.

### Validation Signals

- `scripts/test-workflow`
- Black-box behavior table showing all ten cases pass
- `scripts/openspec-validate-source-manifest harden-problem-scope-response-routing --project-root .`

### Open Questions Affecting Execution

- None (response-lint implementation minimum is decided; see D6).

### Non-Goals for Execution

- Do not implement runtime DAG planning or model routing.
- Do not alter Stage 5 approval semantics except to reject those decisions before Stage 5.

## Load-Bearing Preservation Notes

- Black-box failures in tests 1, 3, 4, 5, and 9 → preserved as router, template, and lint requirements.
- Passing behavior in tests 6, 7, 8, and 10 → preserved as regression cases to prevent backsliding.
- Review conclusion that helper gates are already harder than first-response behavior → preserved by adding response-lint and templates rather than replacing deterministic gates.
- Decision that “scope candidates” are allowed but “recommendations” are not before confirmation → preserved in D3 and the spec delta.
