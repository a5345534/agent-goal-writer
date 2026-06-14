# Tasks: clarify-value-gated-writer-workflow

## 1. Spec and Skill Contract

- [x] 1.1 Update `SKILL.md` purpose/workflow text to define the writer as a critical collaborator rather than an order-taker.
- [x] 1.2 Add the value-gated workflow stages before the current OpenSpec scaffold/write steps.
- [x] 1.3 Document the Value Challenge Gate, constructive disagreement protocol, no-build option, smaller-scope option, and `proceed_with_assumptions` path.
- [x] 1.4 Update the quality rubric so pre-spec quality is checked before `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` are written.
- [x] 1.5 Clarify that `.writer-workflow/changes/<change-name>/` is workspace-local operational state, while OpenSpec markdown/spec files remain the governed sources of truth.

## 2. Workflow Helper Script

- [x] 2.1 Add `scripts/agent-goal-writer-workflow` using only the Python standard library.
- [x] 2.2 Implement `init <change-name> --capability <capability>` to create workspace-local `.writer-workflow/changes/<change-name>/` artifacts.
- [x] 2.3 Implement `check <change-name>` for value-gate artifact completeness.
- [x] 2.4 Implement `gate <change-name> --pre-spec` to write `pre-spec-gate.json` with `blocked`, `pass`, or `proceed_with_assumptions`.
- [x] 2.5 Implement `write-spec <change-name>` so it fails unless the latest pre-spec gate status is `pass` or acknowledged `proceed_with_assumptions`.
- [x] 2.6 Return stable non-zero exit codes for blocked/missing-artifact/error states and machine-readable JSON status output for automation.

## 3. Artifact Templates and Preservation

- [x] 3.1 Add templates/reports for `value-gate.json`, `spec-kernel.md`, `status.json`, `pre-spec-gate.json`, and `write-spec-status.json` under `.writer-workflow/changes/<change-name>/`.
- [x] 3.2 Ensure templates distinguish problem, affected actor, value evidence, no-build alternative, smaller-scope alternative, non-goals, assumptions, open questions, and verification path.
- [x] 3.3 Ensure `proceed_with_assumptions` requires explicit user acknowledgement and lists unresolved assumptions/value risks.
- [x] 3.4 Ensure OpenSpec writing guidance requires value challenge outputs to land in `proposal.md` and `design.md`.

## 4. Tests and Validation

- [x] 4.1 Add script-level fixture-driven checks for `init` artifact creation.
- [x] 4.2 Add blocked-gate coverage for missing success signal, missing no-build alternative, missing non-goal, and unresolved blocker questions.
- [x] 4.3 Add passing-gate coverage for a complete spec kernel.
- [x] 4.4 Add `proceed_with_assumptions` coverage that fails without explicit acknowledgement and passes with acknowledgement.
- [x] 4.5 Add `write-spec` coverage proving OpenSpec writing cannot start before the gate passes.
- [x] 4.6 Add coverage that positional `<change-name>` uses `.writer-workflow/changes/<change-name>/` and can complete check/gate/write-spec.
- [x] 4.7 Run `scripts/test-workflow`.

## 5. Documentation and Closeout

- [x] 5.1 Update `README.md` to describe the new workflow helper and when to use it.
- [x] 5.2 Refresh `source-manifest.json`.
- [x] 5.3 Generate/update and validate `change-explainer.html` with the bundled writer helper.
- [x] 5.4 Run archive preflight after implementation tasks are complete.

## Backlog / Follow-ups

- [ ] [BACKLOG] Add richer semantic scoring or LLM-assisted pre-spec critique after deterministic artifact gating is working.
