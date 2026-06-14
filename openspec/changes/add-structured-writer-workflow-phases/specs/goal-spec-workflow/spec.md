# goal-spec-workflow Specification

## Purpose

This capability defines the pre-OpenSpec authoring workflow for `goal-spec`. It ensures workspace-local workflow state can track value challenge phases, structured claims, recovery recommendations, loop guards, and load-bearing preservation before the writer creates governed OpenSpec artifacts.

## Requirements

### Requirement: Phase-aware workflow state

The workflow SHALL maintain a phase-aware state file at `.writer-workflow/changes/<change-name>/workflow-state.json` for each active change. The state SHALL include active phase, phase status, phase steps, loop guard counters, and update timestamp.

#### Scenario: Initialization creates phase-aware state

- **GIVEN** a change name and capability name
- **WHEN** `scripts/goal-spec-workflow init <change-name> --capability <capability>` runs
- **THEN** the workflow SHALL create `.writer-workflow/changes/<change-name>/workflow-state.json`
- **AND** the state SHALL include phases for intake, value challenge, clarification, spec kernel, pre-spec gate, OpenSpec write, and validation
- **AND** the state SHALL include loop guard defaults.

#### Scenario: Existing value-gate workflows remain compatible

- **GIVEN** `.writer-workflow/changes/<change-name>/value-gate.json` exists but `workflow-state.json` is missing
- **WHEN** `scripts/goal-spec-workflow check <change-name>` runs
- **THEN** the workflow SHALL either synthesize compatible default phase state or report a migration warning
- **AND** it SHALL NOT discard existing `value-gate.json` decisions.

### Requirement: Extract reflect recover pipeline

The workflow SHALL provide a deterministic extract/reflect/recover pipeline for pre-spec user/source input. The pipeline SHALL write structured outputs under `.writer-workflow/changes/<change-name>/` and SHALL remain advisory unless the pre-spec gate marks a blocker.

#### Scenario: Extraction records value-frame claims

- **GIVEN** user/source input is available for the change
- **WHEN** extraction runs
- **THEN** `extracted-claims.json` SHALL record available problem/opportunity, beneficiary, desired outcome, proposed solution, constraints, success signal, assumptions, open questions, no-build candidate, and smaller-scope candidate
- **AND** missing values SHALL remain explicit rather than invented.

#### Scenario: Reflection identifies gaps

- **GIVEN** extracted claims contain missing or weak value, scope, risk, or verification information
- **WHEN** reflection runs
- **THEN** `reflection-report.json` SHALL identify the gaps
- **AND** it SHALL classify each gap as blocker, warning, or informational.

#### Scenario: Recovery recommends one next action

- **GIVEN** a reflection report exists
- **WHEN** recovery runs
- **THEN** `recovery-actions.json` SHALL recommend exactly one next action
- **AND** the next action SHALL be one of ask-one-question, no-build, smaller-scope, proceed-with-assumptions, block-high-stakes, or proceed-to-gate.

### Requirement: Claim graph preservation

The workflow SHALL track load-bearing source claims in `.writer-workflow/changes/<change-name>/claim-graph.json`. The claim graph SHALL map each load-bearing claim to its preservation status and OpenSpec destination before closeout.

#### Scenario: Load-bearing claim blocks pre-spec completion when unpreserved

- **GIVEN** `claim-graph.json` contains a load-bearing claim with status `unpreserved`
- **WHEN** `scripts/goal-spec-workflow gate <change-name> --pre-spec` runs
- **THEN** the gate SHALL report a blocker unless the claim is explicitly deferred, marked non-load-bearing, or acknowledged as an assumption/open question.

#### Scenario: Preserved claim names OpenSpec destination

- **GIVEN** a load-bearing claim is preserved
- **WHEN** the claim graph is checked
- **THEN** the claim SHALL name at least one destination in `proposal.md`, `design.md`, `tasks.md`, or `specs/**/spec.md`.

### Requirement: Loop guard controls

The workflow SHALL track clarification and value-challenge loop guards to prevent repeated prompts and unbounded debate. Loop guards SHALL count clarification turns, challenge turns, and normalized repeated question/challenge hashes.

#### Scenario: Repeated question is blocked

- **GIVEN** the same normalized clarification question has already reached the configured repeat limit
- **WHEN** the writer attempts to record or emit the same question again
- **THEN** the workflow SHALL block the repeat
- **AND** it SHALL recommend a fallback path.

#### Scenario: Challenge limit recommends a decision path

- **GIVEN** the writer has challenged value for the configured maximum number of turns
- **WHEN** value remains unresolved
- **THEN** the workflow SHALL recommend no-build, smaller-scope, `proceed_with_assumptions`, ask-user-to-choose, or block-high-stakes based on the recorded risk and assumptions.

### Requirement: Registry-style workflow organization

The workflow helper SHOULD organize phase templates, gate checks, extractors, reflectors, recovery strategies, and preservation rules as registry-style data structures. It SHALL NOT load arbitrary external plugin code as part of this change.

#### Scenario: Independent changes do not leak workflow state

- **GIVEN** two different change names have workflow directories under `.writer-workflow/changes/`
- **WHEN** checks, gates, or write-spec operations run for one change
- **THEN** they SHALL use only that change's workflow state unless an explicit artifact directory override is provided.

### Requirement: OpenSpec remains authoritative

Workflow state files SHALL remain workspace-local operational artifacts. OpenSpec markdown/spec files SHALL remain the governed source of truth, and load-bearing workflow conclusions SHALL be copied or summarized into OpenSpec sources when writing proceeds.

#### Scenario: Workflow state does not replace OpenSpec sources

- **GIVEN** `workflow-state.json`, `reflection-report.json`, or `claim-graph.json` contains a decision relevant to implementation or verification
- **WHEN** `write-spec <change-name>` creates or updates OpenSpec files
- **THEN** the decision SHALL be preserved in `proposal.md`, `design.md`, `tasks.md`, `specs/**/spec.md`, assumptions, open questions, or preservation notes
- **AND** the generated `change-explainer.html` SHALL remain a companion view rather than the authoritative source.
