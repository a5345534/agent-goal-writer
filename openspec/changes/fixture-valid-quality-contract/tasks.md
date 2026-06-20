# Tasks: fixture-valid-quality-contract

## 1. Spec and Contract

- [x] 1.1 Update `quality-contract-valid` spec delta.
- [x] 1.2 Confirm affected APIs/events/data contracts (none — test fixture).
- [x] 1.3 Verify Execution Quality Contract and Engineering Quality sections are source-grounded in proposal.md and design.md.

## 2. Implementation

- [x] 2.1 Write proposal.md with explicit Execution Quality Contract.
- [x] 2.2 Write design.md with Engineering Quality section.
- [x] 2.3 Write tasks.md with quality profile validation task.

## 3. Verification

- [ ] 3.1 Run `scripts/goal-spec-openspec.py validate-quality-profile fixture-valid-quality-contract --project-root . --json`.
- [ ] 3.2 Confirm explicit profiles are detected.

## 4. Documentation / Closeout

- [x] 4.1 No user-visible docs change needed (test fixture only).
- [x] 4.2 Refresh `source-manifest.json` (includes quality profiles from Execution Quality Contract).
- [ ] 4.3 Run archive preflight when test coverage is complete.
- [x] 4.4 Validate quality profiles with `scripts/goal-spec-openspec.py validate-quality-profile`.

## Backlog / Follow-ups

- [ ] [BACKLOG] Add more fixture permutations once `validate-quality-profile` stabilizes.
