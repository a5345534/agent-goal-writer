# agent-goal-writer

Standalone Pi skill folder for writing OpenSpec change packages from a user goal. It includes bundled helper scripts so target workspaces do not need to vendor `openspec/scripts/*` or depend on a neighboring `openspec-workflow` checkout for normal validation.

## What it provides

`agent-goal-writer` is a self-contained OpenSpec authoring skill. Workspaces may
load this external skill, but should not copy/own separate OpenSpec writing or
planning skills for the same workflow. It writes and validates the normal
OpenSpec artifacts:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/**/spec.md`
- `source-manifest.json`
- `change-explainer.html` when the target project requires it

It also covers update/review/explainer-only/archive-preflight modes for an
existing OpenSpec change package.

The skill keeps all authoring instructions directly in `SKILL.md`; there are no
separate reference files to load for normal use. Automation needed by the skill
is bundled under `scripts/` and uses only Python's standard library.

## BMAD-inspired improvements

The skill incorporates BMAD-style planning practices adapted for OpenSpec:

- discovery before drafting: brain dump, stakes calibration, working mode, concern scan;
- spec kernel: Why, Capabilities, Constraints, Non-goals, Success signal;
- optional elicitation loop: pre-mortem, red-team, stakeholder lens, first principles, edge cases;
- load-bearing preservation pass so source claims are not silently lost;
- quality rubric for decision-readiness, done-ness clarity, scope honesty, downstream usability, boundary fit, and preservation.

## What it is not

This skill is **not** for converting OpenSpec into `/goal` or Goal DAG files.
It is for writing the OpenSpec specification/change package itself.

## Use with Pi

Load directly:

```bash
pi --skill <path-to-agent-goal-writer>
```

Or install/load from GitHub after publication:

```bash
pi install git:github.com/a5345534/agent-goal-writer
```

Or add it to Pi settings as a skill path/package path.

## Typical use

```text
/skill:agent-goal-writer write an OpenSpec change for <goal>
```

Expected output is an OpenSpec change under:

```text
openspec/changes/<change-name>/
```

## Bundled helpers

Run these from the skill directory, or resolve them relative to `SKILL.md` when
the skill is installed by Pi:

```bash
scripts/openspec-propose <change-name> --project-root <target-root> --capability <capability>
scripts/openspec-build-source-manifest <change-name> --project-root <target-root>
scripts/openspec-validate-source-manifest <change-name> --project-root <target-root>
scripts/openspec-validate-explainer <change-name> --project-root <target-root> --require-decision-review
scripts/openspec-archive-preflight <change-name> --project-root <target-root> --require-decision-review
```

Compatibility wrapper:

```bash
scripts/check-change-explainer.sh <change-name> --project-root <target-root> --require-decision-review
```

## Relationship to nearby projects

- `agent-goal-writer` owns the prompt-level workflow and the fallback automation
  needed to scaffold, refresh manifests, validate explainers, and run archive
  preflight checks.
- External workflow packages or project-local `openspec/scripts/*` are not part
  of the required writer-skill path. If a project explicitly requires stricter
  local policy checks, treat those checks as additional evidence after the
  bundled helpers have passed.
- Target workspaces should reference/load this skill rather than vendoring a
  workspace-local duplicate.
