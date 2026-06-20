# Tasks: fixture-missing-quality-contract

## 1. Spec and Contract

- [x] 1.1 Update `quality-contract-missing` spec delta.
- [x] 1.2 Confirm affected APIs/events/data contracts (simulated — test fixture).
- [ ] 1.3 Execution Quality Contract intentionally omitted from proposal.md (test fixture design).

## 2. Implementation

- [x] 2.1 Write proposal.md without Execution Quality Contract section.
- [x] 2.2 Write design.md without Engineering Quality section.
- [x] 2.3 Write tasks.md noting the intentional omission.

## 3. Verification

- [ ] 3.1 Run `scripts/goal-spec-openspec.py validate-quality-profile fixture-missing-quality-contract --project-root . --json`.
- [ ] 3.2 Confirm keyword-inferred profiles are populated and warning is emitted.

## 4. Documentation / Closeout

- [x] 4.1 No user-visible docs change needed (test fixture only).
- [ ] 4.2 Refresh `source-manifest.json` (keyword-inferred profiles only).
- [x] 4.3 Validate quality profiles with `scripts/goal-spec-openspec.py validate-quality-profile`.

## Backlog / Follow-ups

- [ ] [BACKLOG] Add a docs-only fixture that has no quality profiles at all.
