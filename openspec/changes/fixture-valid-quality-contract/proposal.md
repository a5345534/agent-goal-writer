# fixture-valid-quality-contract

## Why

The goal-spec open-source skill needs deterministic validation that its
Execution Quality Contract sections are correctly detected and acknowledged
by the quality profile mapper and the validation controller. Without this
fixture, quality contract detection can regress without test coverage.

## What Changes

- Add a sample OpenSpec change package that includes a complete Execution
  Quality Contract section in proposal.md.
- Demonstrate explicit quality profiles, required evidence, review posture,
  and ship posture fields as defined by the goal-contract schema.
- Serve as a fixture for `validate-quality-profile` and
  `validate-source-manifest` test coverage.

## Impact

- Affected specs: `quality-contract-valid`
- Affected modules/repos: `goal-spec` test fixtures only
- Affected APIs/events/data: None (test fixture, no production API surface)
- Migration/deployment impact: None
- User-visible impact: None (developer-facing test fixture)

## Non-Goals

- Do not include a production code change; this is a fixture package only.
- Do not produce downstream planning artifacts.

## Execution Quality Contract

This section defines the quality posture and required evidence for this change.
It is consumed by goal-dag's quality profile mapper and goal-runner's validation
controller.

- Quality profiles: `incremental-implementation`, `test-driven-change`, `code-review-required`, `api-boundary-review`
- Required evidence: `validators-ran`, `locked-artifacts-unchanged`, `implementation-diff-present`
- Review posture: elevated
- Ship posture: standard

## Success Signal

The `validate-quality-profile` subcommand detects explicit quality profiles,
required evidence, review posture, and ship posture from this fixture and
returns status=ok with explicitProfiles containing at least four profiles.

## Assumptions

- [ASSUMPTION] The quality profile enum values in goal-contract remain stable
  for the profiles used in this fixture.
- [ASSUMPTION] The `validate-quality-profile` subcommand reads proposal.md
  from the standard openspec/changes/<name> path.

## Open Questions

- None
