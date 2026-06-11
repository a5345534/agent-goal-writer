# agent-goal-writer

Standalone Pi skill folder for writing OpenSpec change packages from a user goal.

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
separate reference files to load for normal use.

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
pi --skill /home/shawn/projects/active/agent-goal-writer
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

## Relationship to nearby projects

- `openspec-workflow` owns reusable workflow scripts and adapters.
- `agent-goal-writer` is the prompt-level skill that tells an agent how to write,
  review, validate, and prepare OpenSpec artifacts from a user goal.
- Target workspaces should reference/load this skill rather than vendoring a
  workspace-local duplicate.
