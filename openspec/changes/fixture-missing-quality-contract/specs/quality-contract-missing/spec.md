# quality-contract-missing Specification

## Purpose

This capability owns the test-fixture behavior for missing Execution Quality
Contract detection. It is not a production capability; it exists solely as
an OpenSpec sample fixture for quality profile validation testing.

## Requirements

### Requirement: Keyword-inferred quality profile detection

The OpenSpec bundled helpers SHALL detect quality profiles from keyword
analysis when a non-trivial change omits the Execution Quality Contract
section, and SHALL emit a warning about the missing explicit contract.

#### Scenario: Missing contract fixture triggers keyword inference

- **GIVEN** a change package at `openspec/changes/fixture-missing-quality-contract/`
  with a proposal.md that does NOT contain an Execution Quality Contract
  section but contains API boundary, performance, and production keywords
- **WHEN** `scripts/goal-spec-openspec.py validate-quality-profile
  fixture-missing-quality-contract --project-root . --json` is executed
- **THEN** the command returns exit code 0 (keyword-inferred profiles exist)
  or exit code 1 with no_quality_profiles_detected in errors
- **AND** the JSON output has hasQualityContract=false
- **AND** if status=ok, warnings indicate no explicit quality contract found
