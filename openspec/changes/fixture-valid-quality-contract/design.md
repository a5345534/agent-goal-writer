# Design: fixture-valid-quality-contract

## Context

This is a test fixture for validating Execution Quality Contract detection
in the goal-spec bundled helpers. It is not a real implementation change.

## Spec Kernel

- Why: Provide a test fixture with explicit quality profiles for validation.
- Capabilities:
  - Quality profile validation can detect explicit profiles from a source-grounded Execution Quality Contract.
- Constraints:
  - Must follow OpenSpec package conventions in proposal.md, design.md, tasks.md, and spec.md.
- Non-goals:
  - No production code change.
- Success signal: `validate-quality-profile` returns ok with at least four explicit profiles.

## Goals

- Serve as a positive test fixture for quality contract validation.

## Non-Goals

- No implementation, deployment, or migration.

## Concern Scan

| Concern | Relevance | Design response |
| --- | --- | --- |
| API boundary keywords | This fixture uses api-boundary-review as an explicit profile; API/endpoint/contract keywords are not a false positive concern for fixture validation. | N/A — fixture only. |

## Decisions

### D1. Quality profiles selection

**Choice**
Include `incremental-implementation`, `test-driven-change`, `code-review-required`, and `api-boundary-review` as explicit profiles.

**Rationale**
A mix of discipline profiles and one conditional profile exercises the profile validation adequately.

**Alternatives considered**
- Using only one profile: would not test multi-profile detection.

## Detailed Design

### Data / Contract Changes

None (test fixture).

### Execution Flow

The fixture is read-only by validation scripts. No execution.

### Module Boundaries

None.

### Migration / Rollout

None.

## Engineering Quality

This section records source-grounded engineering quality decisions that supplement
the Execution Quality Contract from proposal.md.

- Quality profiles reiterated: `incremental-implementation`, `test-driven-change`, `code-review-required`, `api-boundary-review`
- Verification tooling: `scripts/goal-spec-openspec.py validate-quality-profile`
- Performance/SLA targets: N/A
- Observability requirements: N/A

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Fixture drifts from contract schema | Low | Explicit profiles match `VALID_QUALITY_PROFILES` in `goal-spec-openspec.py`. |

## Verification Plan

- Run `scripts/goal-spec-openspec.py validate-quality-profile fixture-valid-quality-contract --project-root . --json` and confirm status=ok and explicitProfiles includes all four profiles.

## Load-Bearing Preservation Notes

- Source claim: "Quality profiles must be explicitly stated" → proposal.md Execution Quality Contract.
