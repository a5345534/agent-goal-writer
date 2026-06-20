# Design: fixture-missing-quality-contract

## Context

This is a negative test fixture for Execution Quality Contract detection.
It simulates a non-trivial API endpoint change with performance and
production deployment considerations, but deliberately omits the
Execution Quality Contract and Engineering Quality sections.

## Spec Kernel

- Why: Test that quality profiles can be keyword-inferred even when the
  explicit Execution Quality Contract is missing.
- Capabilities:
  - Keyword-based quality signal detection for api boundary, performance,
    and production keywords.
- Constraints:
  - Must follow OpenSpec file conventions.
- Non-goals:
  - No production code change.
- Success signal: Quality profile detection returns status=ok or warn
  with keyword-inferred profiles.

## Goals

- Serve as a negative test fixture for quality contract validation.

## Non-Goals

- No implementation, deployment, or migration.

## Concern Scan

| Concern | Relevance | Design response |
| --- | --- | --- |
| API boundary | This change simulates an API endpoint modification. | Test fixture; no design response needed. |
| Performance | The change mentions performance implications. | Test fixture; no design response needed. |
| Production visible | The change mentions a production rollout. | Test fixture; no design response needed. |

## Decisions

### D1. Deliberate omission of Execution Quality Contract

**Choice**
Omit the Execution Quality Contract section entirely from proposal.md and
the Engineering Quality section from design.md.

**Rationale**
This exercises the keyword-based fallback detection path in
`detect_quality_signals()`.

**Alternatives considered**
- Including a partial contract: would not test the fully-missing path.

## Detailed Design

### Data / Contract Changes

This fixture simulates an API endpoint change that modifies the request
contract and response payload. Keywords: endpoint, contract, schema change,
compatibility, API.

### Execution Flow

The simulated execution flow involves a new endpoint handler with auth
middleware, input validation, and a database query that must be optimized
for throughput. Keywords: auth, authentication, authorization, token,
input validation, data access, performance, latency, throughput, SLA,
benchmark, cache, optimize, concurrency.

### Module Boundaries

The simulated change crosses a module boundary between the API gateway
and the core service. Keywords: module boundary, public contract.

### Migration / Rollout

The simulated rollout uses a feature flag and canary deployment before
full production traffic migration. Keywords: production, deploy, release,
launch, rollout, monitor, alert, feature flag, toggle, rollback, canary,
go-live.

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Quality contract missing may cause downstream mapper failure | Medium | Keyword inference provides fallback; explicit contract recommended. |

## Verification Plan

- Run `scripts/goal-spec-openspec.py validate-quality-profile fixture-missing-quality-contract --project-root . --json` and verify that keyword-inferred profiles are populated and a warning about the missing explicit contract is emitted.

## Load-Bearing Preservation Notes

- This design.md is keyword-heavy to exercise keyword-based quality signal detection.
