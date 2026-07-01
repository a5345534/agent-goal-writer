# Problem & Scope Confirmation Flow

The Problem & Scope Confirmation Flow (stages 1.5–1.7) sits between Project
Modeling (Stage 1) and Proposal Meaning Analysis (Stage 2). Its core principle
is **Scope closure before value judgment**.

## First-Response State Router

Before producing any user-visible analysis, recommendation, or OpenSpec
content, the agent MUST apply this routing contract:

| Condition | Allowed response |
| --- | --- |
| Scope uncertain or `scopeUncertainty=true` | Stage 1.5 Problem & Scope Grilling only; if not closed, Stage 1.6-1 single bounded clarification request. |
| User selected a scope but did not provide `confirm_scope_for_analysis` | Summarize selected scope and request exactly `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`. |
| User provides `confirm_scope_for_analysis` | Stage 2 Proposal Meaning Analysis may proceed, subject to artifact/input availability. |
| User provides `revise_scope` | Return to Stage 1.5 grilling. |
| User provides `abandon_proposal` | Terminate the proposal; do NOT label it no-build. |
| User provides Stage 5 approval (e.g., `approve_openspec_authoring`) before Stage 5 | Reject as INVALID for Stage 1.7 and show the three valid Stage 1.7 decisions. |
| User chooses `continue_discussion` while scope is uncertain | Return to Stage 1.5 grilling/clarification, NOT Value & Logic Closure Assessment. |
| Required `inputDigests` are missing | Block freshness; do NOT accept the artifact. |

## Problem & Scope Grilling Rules

Before `confirm_scope_for_analysis`, the agent operates in grilling mode.
Exactly one active blocking question may be asked at a time. Recommendations are
allowed only as the agent's suggested answer to that blocking question; value
judgment, no-build, and smaller-scope recommendations still belong after scope
confirmation.

Allowed:
- Ask exactly one blocking question that maps to one blocking field and one
  design-tree branch.
- Include why the question matters, the agent's recommended answer, and bounded
  options when possible.
- Use the user's natural language/script for visible prose and labels; preserve
  only canonical SSOT identifiers such as file names, paths, schema fields,
  commands, function names, and decision tokens.
- Use existing functionality as baseline context and scope boundary evidence.

Forbidden:
- Ask multiple unrelated questions in one response.
- Copy English template labels into non-English responses (for example,
  `Intended outcome` in a Traditional Chinese response).
- Expose internal reasoning, scratchpad, or response-planning notes.
- Label any whole scope candidate as "best", "highest value", "no-build", or
  "smaller-scope recommendation".
- Rank or score scope candidates by value or complexity.
- Use existing functionality to cancel `improvementIntent` or justify no-build.
- Proceed to PMA, Spec Kernel, or OpenSpec writing before scope closure and user
  confirmation.

## Persisted-State Honesty

- Without persisted artifacts, do NOT claim a stage, gate pass, or recorded decision.
- When asked not to write files, use "would record" / "next artifact would be".
- Do NOT say "recorded", "created", "gate passes" unless the artifact exists and is validated.

## Stages

### 1.5 Problem & Scope Grilling

The **judge** (`value-judge`) operates in **grilling mode** to clarify the
user's problem, intended scope, and improvement intent. Output:
`problem-scope-framing.json` plus durable design-tree state.

The judge MUST NOT recommend no-build, evaluate value, classify as duplicate,
or write OpenSpec during this stage. If the user expresses improvement intent
("make it more complete"), `improvementIntent` must be true. If the user is
unsure about scope, `scopeUncertainty` must be true.

**Response template**: The Stage 1.5 Problem & Scope Grilling Output Template
(see SKILL.md) MUST be used with localized visible labels — include intended
outcome, improvement intent, scope uncertainty, design tree status, exactly one
blocking question, why it matters, the agent's recommended answer, bounded
options, and a localized "Not doing yet" section.

### 1.6 Scope Closure Gate

A **deterministic gate** that verifies `problem-scope-framing.json` is
structurally complete. It does NOT evaluate value, duplicates, or whether
OpenSpec should be written.

- **closed** → routes to Problem-Scope User Confirmation Gate (1.7)
- **not_closed** → routes to Problem Scope Clarification Request (1.6-1)

### 1.6-1 Problem Scope Clarification Request

The **judge** produces a single bounded question when scope is not closed.
Output: `problem-scope-clarification-request.json`. The question must map to one
blocking field and one design-tree branch, provide bounded options when possible,
and include the agent's recommended answer.

### 1.6-2 Problem Scope Clarification Response

A **deterministic step** capturing the decision maker's answers.
Output: `problem-scope-clarification-response.json`. After response,
workflow loops back to Stage 1.5 for grilling/reframing with clarified scope.

### 1.7 Problem-Scope User Confirmation Gate

The user confirms the defined scope may proceed to Proposal Meaning Analysis.
Output: `problem-scope-user-gate.json`.

Allowed decisions:
- `confirm_scope_for_analysis` → proceed to Stage 2
- `revise_scope` → return to Stage 1.5
- `abandon_proposal` → terminal (NOT treated as no-build)

**Response template**: The Stage 1.7 Scope-Confirmation Response Template
(see SKILL.md) MUST be used — summarize selected scope and list exactly the
three valid choices.

## Grilling (Value Challenge / Critical Collaborator) Responses

After scope confirmation (`confirm_scope_for_analysis`), the agent enters the
critical collaborator / value challenge phase. Responses during this phase
MUST follow the one-question discipline enforced by the `grilling` lint stage:

- **Exactly one question** — a single focused question that resolves the
  highest-impact blocker. ASCII `?` and CJK `？` are both accepted; multiple
  questions are rejected by the linter.
- **My recommended answer or localized equivalent** — the agent provides a
  concrete recommendation or suggested approach.
- **Bounded options** — the question presents the user with specific, limited
  choices (e.g., "A / B" or numbered options).
- **Not doing yet section or localized equivalent** — explicitly lists what is
  NOT being addressed in this response (no PMA, no Spec Kernel, no OpenSpec
  writing).
- **Same-language visible labels** — non-English responses must localize
  template labels while preserving canonical SSOT identifiers.
- **No internal reasoning leakage** — scratchpad/planning text and meta headings
  must not be user-visible.
- **No premature content** — the response must not contain Proposal Meaning
  Analysis, Spec Kernel, OpenSpec writing, or OpenSpec scaffolding as
  substantive content. These terms are allowed only in negative "not doing yet"
  lines.

Use the `lint-response` command with `--stage grilling` to validate responses:

```bash
<script-dir>/scripts/goal-spec-workflow lint-response --stage grilling --response-text "<response>" --project-root <target>
```

The linter returns exit 0 (pass) or exit 20 (blocked) with a JSON report
identifying forbidden phrases or missing required sections.

## Key Rules

- **Scope closure before value judgment**: Proposal Meaning Analysis SHALL NOT
  run until `problem-scope-user-gate.json` exists with `confirm_scope_for_analysis`.
  PMA SHALL NOT be produced unless `scope-closure-gate.json` is closed AND
  `problem-scope-user-gate.json` decision is `confirm_scope_for_analysis`. PMA
  MUST record digests of `project-model.json`, `problem-scope-framing.json`,
  and `problem-scope-user-gate.json` in `inputDigests`.
- **No no-build before scope confirmation**: When improvement intent is true,
  existing functionality must not be used to recommend no-build before Stage 1.7.
- **Two-gate design**: Scope Closure Gate proves scope is well-formed;
  User Confirmation Gate proves the user accepts it for analysis.
- **Stage 1.7 rejects approval-type decisions**: `approve_openspec_authoring`,
  `approve_smaller_scope_openspec_authoring`, `accept_no_build_recommendation`
  are NOT valid until Stage 5. Providing these at Stage 1.7 must be rejected with
  the three valid Stage 1.7 choices.
- **Value challenge starts AFTER scope confirmation**: The critical-collaborator
  no-build, smaller-scope, and value challenge protocol applies only after
  `confirm_scope_for_analysis` has been recorded.
