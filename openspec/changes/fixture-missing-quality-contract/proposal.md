# fixture-missing-quality-contract

## Why

A non-trivial change that touches API boundaries, is performance-sensitive,
and is production-visible, but deliberately omits the Execution Quality
Contract section from proposal.md. This fixture exercises the validation
path where quality profiles must be inferred from keyword analysis, and
validates that the system warns about the missing explicit contract.

## What Changes

- Simulate a change that modifies an API endpoint with performance
  implications and a production rollout plan, without an explicit
  Execution Quality Contract section.
- This is a test fixture intended to trigger the "no explicit quality
  contract" warning path in `validate-quality-profile`.

## Impact

- Affected specs: `quality-contract-missing`
- Affected modules/repos: `goal-spec` test fixtures only
- Affected APIs/events/data: Simulated API endpoint change (test fixture, no production API surface)
- Migration/deployment impact: N/A
- User-visible impact: None (developer-facing test fixture)

## Non-Goals

- Do not include a production code change; this is a fixture package only.
- Do not rely on validators passing this fixture; it is intentionally
  incomplete regarding quality posture.

## Success Signal

The `validate-quality-profile` subcommand resolves quality profiles from
keyword analysis, returns status=ok (or fail with warning), and detects
that no explicit Execution Quality Contract section exists. The test
runner verifies the warning or fail outcome.

## Assumptions

- `[ASSUMPTION]` The validate-quality-profile subcommand fallback to
  keyword detection will detect api-boundary, performance-sensitive,
  and production-visible signals from the keywords in this file.

## Open Questions

- None
