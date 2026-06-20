# quality-contract-valid Specification

## Purpose

This capability owns the test-fixture behavior for valid Execution Quality
Contract detection. It is not a production capability; it exists solely
as an OpenSpec sample fixture for quality profile validation testing.

## Requirements

### Requirement: Explicit quality profile detection

The OpenSpec bundled helpers SHALL detect explicit quality profiles,
required evidence, review posture, and ship posture from a proposal.md
that contains a complete Execution Quality Contract section.

#### Scenario: Valid fixture is parsed

- **GIVEN** a change package at `openspec/changes/fixture-valid-quality-contract/`
  with a proposal.md containing an Execution Quality Contract section that
  lists `Quality profiles: incremental-implementation, test-driven-change,
  code-review-required, api-boundary-review`
- **WHEN** `scripts/goal-spec-openspec.py validate-quality-profile
  fixture-valid-quality-contract --project-root . --json` is executed
- **THEN** the command returns exit code 0
- **AND** the JSON output has status=ok
- **AND** explicitProfiles contains at least four profiles
- **AND** hasQualityContract is true
