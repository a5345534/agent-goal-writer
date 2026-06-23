# goal-spec-workflow Specification

## Purpose

This capability defines the pre-OpenSpec authoring workflow for `goal-spec`, including the Problem & Scope Confirmation Flow that must close and confirm problem/scope before Proposal Meaning Analysis, value judgment, Spec Kernel creation, or OpenSpec writing.

## Requirements

### Requirement: First-response router before value judgment

The workflow SHALL apply a Stage 1.5–1.7 first-response router before producing user-visible analysis or recommendations. The router SHALL determine whether the response is framing-only, scope-confirmation, Proposal Meaning Analysis, revision, abandonment, or invalid-decision rejection.

#### Scenario: Scope uncertainty routes to framing only

- **GIVEN** the user expresses improvement intent and scope uncertainty
- **WHEN** the agent produces the first goal-spec response
- **THEN** the response SHALL be limited to Problem & Scope Framing or Problem Scope Clarification Request content
- **AND** it SHALL NOT recommend no-build
- **AND** it SHALL NOT recommend smaller-scope
- **AND** it SHALL NOT perform Proposal Meaning Analysis
- **AND** it SHALL NOT produce a Spec Kernel or OpenSpec source content.

#### Scenario: Project modeling does not skip scope confirmation

- **GIVEN** Project Modeling has completed
- **AND** `problem-scope-user-gate.json` does not exist with decision `confirm_scope_for_analysis`
- **WHEN** the workflow determines the next step
- **THEN** it SHALL route to Problem & Scope Framing, Scope Closure Gate, Problem Scope Clarification Request, or Problem-Scope User Confirmation Gate
- **AND** it SHALL NOT route directly to Proposal Meaning Analysis.

### Requirement: Framing-only responses use neutral scope candidates

Problem & Scope Framing responses SHALL clarify the intended outcome, problem statement, improvement intent, target surface, scope uncertainty, and candidate scopes without making a value recommendation.

#### Scenario: Scope candidates are not recommendations

- **GIVEN** the user is unsure whether scope should include multiple candidate capabilities
- **WHEN** the agent lists scope candidates before `confirm_scope_for_analysis`
- **THEN** each candidate MAY include included changes, excluded changes, success signal, and trade-off
- **AND** the response SHALL NOT label any candidate as the recommended path, best value, no-build path, or smaller-scope recommendation
- **AND** any trade-off description SHALL be descriptive (e.g., “smallest change, defers bulk actions”) rather than ranking, scoring, or recommendation.

#### Scenario: Existing functionality remains framing context

- **GIVEN** existing functionality already satisfies part of the user's current workflow
- **AND** the user expresses intent to improve, complete, refine, or extend the workflow
- **WHEN** the agent frames the problem and scope
- **THEN** existing functionality MAY be cited as baseline context or scope boundary evidence
- **AND** it SHALL NOT be used to cancel `improvementIntent`
- **AND** it SHALL NOT justify a no-build recommendation before scope closure and user confirmation.

### Requirement: Bounded clarification request shape

When Scope Closure Gate is `not_closed`, the Problem Scope Clarification Request SHALL ask at most one or two bounded questions. Every question SHALL map to a blocking field and provide concrete bounded options.

#### Scenario: Clarification questions are bounded

- **GIVEN** `problem-scope-framing.json` has unresolved blocking fields
- **WHEN** the agent produces `problem-scope-clarification-request.json` or an equivalent user-facing clarification
- **THEN** it SHALL include no more than two questions
- **AND** each question SHALL identify or map to a blocking field
- **AND** each question SHALL provide bounded options or concrete answer directions
- **AND** it SHALL NOT ask broad open-ended questions such as “please provide more detail” without options.

### Requirement: Selected scope requires explicit user confirmation

Selecting a scope candidate SHALL NOT itself authorize Proposal Meaning Analysis. After scope selection, the workflow SHALL request the Problem-Scope User Confirmation Gate decision.

#### Scenario: User selects a scope

- **GIVEN** the user selects a scope candidate
- **AND** the user has not provided `confirm_scope_for_analysis`
- **WHEN** the agent responds
- **THEN** it SHALL summarize the selected scope
- **AND** it SHALL ask the user to choose exactly one of `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`
- **AND** it SHALL NOT perform Proposal Meaning Analysis
- **AND** it SHALL NOT produce a Spec Kernel.

#### Scenario: Scope confirmation unlocks Proposal Meaning Analysis

- **GIVEN** `scope-closure-gate.json` status is `closed`
- **AND** `problem-scope-user-gate.json` exists with decision `confirm_scope_for_analysis`
- **WHEN** Proposal Meaning Analysis runs
- **THEN** it SHALL NOT produce `proposal-meaning-analysis.json` unless both upstream gate artifacts are available and fresh
- **AND** the resulting artifact SHALL record the digests of `project-model.json`, `problem-scope-framing.json`, and `problem-scope-user-gate.json` in `inputDigests`.

### Requirement: Stage 1.7 rejects approval-type decisions

The Problem-Scope User Confirmation Gate SHALL accept only `confirm_scope_for_analysis`, `revise_scope`, or `abandon_proposal`. Approval-type OpenSpec authoring decisions SHALL be rejected until Stage 5.

#### Scenario: Approval decision at Stage 1.7 is rejected

- **GIVEN** the active gate is Problem-Scope User Confirmation Gate
- **WHEN** the user provides `approve_openspec_authoring`, `approve_smaller_scope_openspec_authoring`, `accept_no_build_recommendation`, or another Stage 5 approval decision
- **THEN** the workflow SHALL reject the decision as invalid for Stage 1.7
- **AND** it SHALL present the valid Stage 1.7 decisions: `confirm_scope_for_analysis`, `revise_scope`, and `abandon_proposal`
- **AND** it SHALL NOT record OpenSpec authoring approval.

### Requirement: Scope revision, abandonment, and discussion routing

The workflow SHALL route user decisions according to the gate where they are valid, and unresolved scope uncertainty SHALL return to framing rather than value assessment.

#### Scenario: Revise scope returns to framing

- **GIVEN** the user provides `revise_scope` at Stage 1.7
- **WHEN** the workflow determines the next step
- **THEN** it SHALL route back to Problem & Scope Framing
- **AND** it SHALL re-evaluate the revised scope candidates without value judgment.

#### Scenario: Abandon proposal is terminal but not no-build

- **GIVEN** the user provides `abandon_proposal` at Stage 1.7
- **WHEN** the workflow responds
- **THEN** it SHALL terminate the proposal without producing an OpenSpec package
- **AND** it SHALL NOT label the result as no-build
- **AND** it SHALL NOT preserve a no-build recommendation rationale unless a separate Stage 5 no-build decision exists.

#### Scenario: Continue discussion with unresolved scope returns to framing

- **GIVEN** the user chooses `continue_discussion`
- **AND** the current discussion still has unresolved scope uncertainty
- **WHEN** the workflow determines the next step
- **THEN** it SHALL route to Problem & Scope Framing or Problem Scope Clarification Request
- **AND** it SHALL NOT route directly to Value & Logic Closure Assessment.

### Requirement: Persisted-state honesty

The agent SHALL distinguish persisted workflow state from user-provided continuation context. It SHALL NOT claim that a gate passed, a decision was recorded, or an artifact was produced unless the corresponding artifact exists and has been validated or written in the current turn.

#### Scenario: Fresh session claims continuation without artifacts

- **GIVEN** the user says the discussion is continuing
- **AND** the agent cannot find matching workflow-state and gate artifacts
- **WHEN** the agent responds
- **THEN** it SHALL state that persisted workflow state is not available or not yet verified
- **AND** it MAY describe how the message would route
- **AND** it SHALL NOT claim the workflow is at Stage 5 or Stage 6 solely from the user's continuation wording.

#### Scenario: User requests no file writes

- **GIVEN** the user asks the agent not to write or modify files
- **WHEN** the agent describes workflow artifacts or gates
- **THEN** it SHALL use prospective wording such as “would record” or “next artifact would be”
- **AND** it SHALL NOT say “recorded”, “created”, “gate passes”, or “artifact produced” unless those artifacts already exist and were validated.

### Requirement: Response-level regression checks

The workflow SHALL include response-level regression coverage for the Problem & Scope Confirmation Flow. The checks SHALL cover premature value recommendations, missing bounded clarification, missing scope confirmation request, invalid gate decisions, discussion routing, and freshness failures.

#### Scenario: Pre-confirmation response lint blocks premature value content

- **GIVEN** a response is produced before `confirm_scope_for_analysis`
- **WHEN** response lint evaluates the response
- **THEN** it SHALL fail the response if it contains no-build recommendation, smaller-scope recommendation, Value Challenge output, Proposal Meaning Analysis output, Spec Kernel output, or OpenSpec writing claims outside an explicit “not doing yet” or invalid-action explanation.

#### Scenario: Missing input digest fails freshness

- **GIVEN** a downstream Stage 1 artifact references load-bearing inputs
- **AND** required `inputDigests` are missing or stale
- **WHEN** freshness validation runs
- **THEN** the workflow SHALL fail closed
- **AND** it SHALL NOT accept the artifact as ready for the next semantic stage.

### Requirement: Stage 1.5 and 1.7 user-facing responses follow required sections

User-facing agent responses during Stage 1.5 Problem & Scope Framing and Stage 1.7 Problem-Scope User Confirmation Gate SHALL include the mandatory sections and decision tokens defined by the workflow templates.

#### Scenario: Stage 1.5 framing response contains required sections

- **GIVEN** the agent produces a Problem & Scope Framing response
- **WHEN** the response is inspected
- **THEN** it SHALL include intended outcome, improvement intent, scope uncertainty, and neutral scope candidates
- **AND** it SHALL include a “Not doing yet” section listing at minimum no value judgment, no no-build recommendation, no Proposal Meaning Analysis, and no Spec Kernel or OpenSpec writing.

#### Scenario: Stage 1.7 scope-confirmation response contains required decision tokens

- **GIVEN** the user has selected a scope candidate
- **AND** `confirm_scope_for_analysis` has not yet been provided
- **WHEN** the agent responds
- **THEN** the response SHALL include the exact decision tokens `confirm_scope_for_analysis`, `revise_scope`, and `abandon_proposal` as the required choices
- **AND** it SHALL NOT include Stage 5 approval tokens such as `approve_openspec_authoring` as valid options.
