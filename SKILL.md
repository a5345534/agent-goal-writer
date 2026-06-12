---
name: agent-goal-writer
description: Self-contained OpenSpec authoring skill enhanced with BMAD-style discovery, elicitation, spec-kernel preservation, and validation gates. Use to turn a user goal into proposal.md, design.md, tasks.md, specs/**/spec.md, source-manifest.json, change-explainer.html, and review/archive-readiness checks. Not for converting OpenSpec into /goal DAGs.
license: MIT
---

# Agent Goal Writer

This skill writes **OpenSpec change packages** from a user goal/request.

It is self-contained. Do **not** load workspace-local OpenSpec authoring skills
for the normal workflow; all required authoring rules, templates, quality gates,
and fallback automation are in this skill folder. A target workspace may load
this skill, but should not copy or own a separate OpenSpec writing/planning
skill.

## Purpose

Turn a user goal, feature request, bugfix direction, product idea, or
architecture decision into a governed OpenSpec package:

```text
openspec/changes/<change-name>/
├── .openspec.yaml
├── proposal.md
├── design.md
├── tasks.md
├── source-manifest.json
├── change-explainer.html
└── specs/<capability>/spec.md
```

OpenSpec markdown/spec files are the source of truth. `change-explainer.html` is
only a companion review view.

## Absorbed OpenSpec authoring capabilities

This skill is the prompt-level owner for the complete OpenSpec authoring line:

- discovery / exploration before drafting;
- new-change proposal scaffolding;
- `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` writing;
- `source-manifest.json` refresh and validation;
- direct decision-review `change-explainer.html` generation without Open Design;
- review / validation of an existing change package;
- archive-readiness preflight checks.

Bundled helper scripts under this skill's `scripts/` directory provide the
automation for scaffolding, source manifests, explainer validation, and archive
preflight. External workflow packages or project-local `openspec/scripts/*` are
not part of the required writer-skill path.

## BMAD-inspired enhancements included

This skill borrows the useful planning patterns from BMAD-style workflows and
maps them into OpenSpec authoring:

- **Discovery before drafting**: brain dump, stakes calibration, working mode,
  concern scan.
- **Spec kernel**: every change must preserve Why, Capabilities, Constraints,
  Non-goals, and Success signal.
- **Elicitation loop**: optional structured second-pass methods such as
  pre-mortem, red-team, stakeholder lens, first principles, and assumption audit.
- **Load-bearing preservation**: every source claim that would change an
  implementation or verification decision must land in proposal/design/tasks/spec
  or be recorded as an open question/non-goal.
- **Quality rubric**: decision-readiness, done-ness clarity, scope honesty,
  downstream usability, boundary fit, and preservation.

## When to use

Use this skill when the user asks to:

- write a spec;
- draft an OpenSpec proposal;
- turn an implementation goal into OpenSpec;
- define requirements/scenarios before implementation;
- create or update `proposal.md`, `design.md`, `tasks.md`, or `specs/**/spec.md`;
- prepare an OpenSpec change for review or archive readiness.

Do **not** use this skill to convert OpenSpec into `/goal` or Goal DAG files.
That is a separate execution-planning concern.

## Inputs

- Target project root.
- User goal / feature request / bug report / architecture direction.
- Change name in kebab-case. If absent, derive one and confirm when ambiguous.
- Capability/spec name in kebab-case. If absent, derive from the owning module
  or cross-module capability.
- Optional mode: create, update, validate/review, explainer-only, or
  archive-preflight-only.

## Bundled automation contract

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. The skill
ships these helper entrypoints and they use only Python's standard library:

```bash
<skill-dir>/scripts/openspec-propose <change-name> --project-root <project-root> --capability <capability>
<skill-dir>/scripts/openspec-build-source-manifest <change-name> --project-root <project-root>
<skill-dir>/scripts/openspec-validate-source-manifest <change-name> --project-root <project-root>
<skill-dir>/scripts/openspec-validate-explainer <change-name> --project-root <project-root> --require-decision-review
<skill-dir>/scripts/openspec-archive-preflight <change-name> --project-root <project-root> --require-decision-review
```

Compatibility wrapper for projects or agents expecting the historical script
name:

```bash
<skill-dir>/scripts/check-change-explainer.sh <change-name> --project-root <project-root> --require-decision-review
```

Never report that automatic validation is unavailable merely because the target
workspace lacks `openspec/scripts/check-change-explainer.sh` or any external
workflow checkout. Use the bundled helper as the required validator. If a project
explicitly requires stricter local policy checks, run them only as additional
evidence after the bundled helper.

## Capability modes

Use the same skill for these OpenSpec planning/writing modes:

| Mode | Use when | Main output |
| --- | --- | --- |
| Create | no change package exists | complete active change package |
| Update | user gives new decisions for an existing change | reconciled markdown/spec/explainer sources |
| Validate / review | user asks whether a change is ready or coherent | findings plus suggested fixes |
| Explainer-only | markdown/specs exist but `change-explainer.html` is missing/stale | direct decision-review HTML companion |
| Archive preflight | implementation is complete and user asks for readiness evidence | preflight result, blockers, next steps |

## Authority rules

1. System/developer/workspace instructions outrank everything.
2. Target project `AGENTS.md`, governance docs, and `openspec/project.md` define
   placement and style rules.
3. Existing authoritative specs live under `openspec/specs/**/spec.md`.
4. Active changes live under `openspec/changes/<change-name>/`.
5. Archive history is historical evidence only; do not use it as current truth
   unless the user asks for history/rationale.
6. The generated explainer must never contradict markdown/spec sources.

## OpenSpec placement rules

- Cross-module and module-internal behavioral specs belong under root
  `openspec/specs/`.
- Module-internal capabilities should use a `<module>-<capability>` prefix when
  the target workspace requires it.
- Non-spec module docs belong under module-local `docs/{architecture,operations,runbooks}/`.
- Do not create retired `docs/superpowers/` material.
- Do not place module-specific domain entities or responsibilities into shared
  modules unless the current authoritative specs allow it.

## Workflow

### 1. Bootstrap project understanding

Before writing specs, identify:

- whether the target is a single repo or multi-repo workspace;
- which repo/module owns the behavior;
- existing specs that already cover the capability;
- boundaries, non-goals, and upstream/downstream interactions;
- validation commands expected by the project.

Use semantic/context search first when available. Then read only relevant
source-of-truth docs and existing specs.

### 2. Detect intent mode

Classify the user's request:

- **Create**: no existing OpenSpec change; write a new package.
- **Update**: existing change/spec receives a change signal; reconcile without
  silently overriding earlier decisions.
- **Validate**: critique the package without changing it unless asked.

If unclear, ask one short clarifying question.

### 3. Discovery before drafting

Run lightweight discovery unless the user explicitly requests a fast draft.
Get to a usable mode quickly; do not interrogate the user with a long form.

#### 3.1 Brain dump

Ask the user for:

- the raw goal in their own words;
- any existing inputs to read (tickets, docs, PRD, incident notes, design notes,
  code references, screenshots, API docs);
- what they almost forgot to mention.

If the user already pasted a lot of context, treat it as intake, then still ask
whether there is any missing context.

#### 3.2 Stakes calibration

Ask or infer the stakes:

- quick internal fix;
- internal workflow/tooling;
- user-visible product behavior;
- public API/event/data contract;
- regulated/security/production-sensitive change;
- architecture/module-boundary decision.

Higher stakes require deeper design, risk, verification, and review sections.

#### 3.3 Working mode

Offer two modes when the request is non-trivial:

- **Fast path**: batch gaps into one or two consolidated questions, then draft
  with `[ASSUMPTION]` tags where inference was necessary.
- **Coaching path**: walk the key sections together; use this for ambiguous,
  high-stakes, or user-visible product decisions.

If the user says to proceed, default to Fast path but preserve assumptions.

#### 3.4 Concern scan

Name the concerns present in the change. Examples:

- module ownership / boundary risk;
- API or event compatibility;
- data migration;
- security/privacy;
- compliance/regulatory traceability;
- frontend UX/routing;
- observability/operability;
- performance/SLA;
- rollback/deployment order;
- multi-agent or parallel implementation conflicts.

Use these concerns to decide which proposal/design/spec sections need depth.

### 4. Build the Spec Kernel

Before writing OpenSpec files, distill the request into this kernel. Keep it in
working notes or include it explicitly in `design.md` when useful.

```text
Why: <force behind the change>
Capabilities: <what users/systems must be able to do; WHAT, not HOW>
Constraints: <non-negotiables that bend design decisions>
Non-goals: <explicit out-of-scope items>
Success signal: <observable proof the change worked>
Assumptions: <inferences not directly confirmed>
Open questions: <human decisions still needed>
```

Kernel rules:

- Every capability needs an intent and a testable success statement.
- Capabilities describe WHAT; implementation HOW belongs in design decisions.
- A constraint must rule something out or force a design choice. Otherwise it is
  decorative and should be removed.
- At least one non-goal is expected for non-trivial changes.
- Success signal must be concrete enough to test, demo, or inspect.
- Preserve stable terms. If a domain noun appears, define it once in design or
  the spec and reuse it consistently.

### 5. Pick the change name and capability name

Change name rules:

- kebab-case;
- specific enough to survive review;
- starts with a verb when possible: `add-`, `fix-`, `move-`, `harden-`,
  `standardize-`, `deprecate-`, `replace-`, `split-`.

Capability/spec name rules:

- kebab-case;
- use an existing capability if the change modifies current behavior;
- create a new capability only when no existing spec owns the behavior;
- for module-internal behavior, include the owning module prefix when required.

### 6. Scaffold the OpenSpec change

Use the bundled skill helper first:

```bash
<skill-dir>/scripts/openspec-propose <change-name> --project-root <project-root> --capability <capability>
```

This creates the standard package, including `.openspec.yaml`,
`proposal.md`, `design.md`, `tasks.md`, `source-manifest.json`, and a starter
`specs/<capability>/spec.md`. Rewrite the generated markdown/spec content with
the source-grounded templates below; the scaffold is only a starting point.

Do not depend on any external scaffold tool being present. If a project
explicitly requires stricter local policy checks, run them only as additional
evidence after this bundled scaffold/write path.

### 7. Write `proposal.md`

`proposal.md` explains **why this change exists** and **what scope review is
approving**. Keep it concise and decision-oriented.

Template:

```markdown
# <change-name>

## Why

<Problem, user need, risk, opportunity, mandate, or architectural pressure.
Explain the current failure mode and why it matters now.>

## What Changes

- <Change 1>
- <Change 2>
- <Change 3>

## Impact

- Affected specs: `<capability>`
- Affected modules/repos: `<module-or-repo>`
- Affected APIs/events/data: `<surface or none>`
- Migration/deployment impact: `<impact or none>`
- User-visible impact: `<impact or none>`

## Non-Goals

- <Explicitly out-of-scope item>
- <Explicitly out-of-scope item>

## Success Signal

<Observable proof that the change achieved its goal.>

## Assumptions

- <[ASSUMPTION] item, or `None`>

## Open Questions

- [ ] <Question needing human decision, or `None`>
```

Rules:

- Do not hide risky scope in vague wording.
- Include non-goals when there is any chance of scope creep.
- If the user request is ambiguous, ask before writing irreversible scope.

### 8. Write `design.md`

`design.md` records the technical direction, trade-offs, and concern scan. It
should be sufficient for another agent/developer to implement without
re-litigating core decisions.

Template:

```markdown
# Design: <change-name>

## Context

<Current architecture/state and relevant constraints.>

## Spec Kernel

- Why: <why>
- Capabilities:
  - <capability intent + success>
- Constraints:
  - <constraint>
- Non-goals:
  - <non-goal>
- Success signal: <signal>

## Goals

- <Goal 1>
- <Goal 2>

## Non-Goals

- <Non-goal 1>
- <Non-goal 2>

## Concern Scan

| Concern | Relevance | Design response |
| --- | --- | --- |
| <concern> | <why it matters> | <how the design handles it> |

## Decisions

### D1. <Decision title>

**Choice**
<Selected design.>

**Rationale**
<Why this choice fits the constraints.>

**Alternatives considered**
- <Alternative>: <why rejected or deferred>

## Detailed Design

### Data / Contract Changes

<APIs, events, schemas, DB tables, DTOs, config, or `None`.>

### Execution Flow

<Step-by-step flow, sequence, ownership, and failure handling.>

### Module Boundaries

<Which module owns what; what must not move across boundaries.>

### Migration / Rollout

<Compatibility, data migration, deployment order, rollback.>

## Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| <risk> | <low/medium/high> | <mitigation> |

## Verification Plan

- <unit/schema validation>
- <integration/API validation>
- <manual/E2E validation>

## Load-Bearing Preservation Notes

- <Source claim> → <where it landed>
- <Dropped wrapper-only/prose content> → <why not load-bearing>
```

Rules:

- Record decisions, not just implementation notes.
- Make ownership and boundaries explicit.
- Include rollback/migration when behavior, data, deployment, or public contract
  changes.

### 9. Write `tasks.md`

`tasks.md` is the implementation checklist. It should be actionable and
verifiable.

Template:

```markdown
# Tasks: <change-name>

## 1. Spec and Contract

- [ ] 1.1 Update `<capability>` spec delta.
- [ ] 1.2 Confirm affected APIs/events/data contracts.

## 2. Implementation

- [ ] 2.1 <Implementation step>
- [ ] 2.2 <Implementation step>

## 3. Verification

- [ ] 3.1 Run `<command>`.
- [ ] 3.2 Verify `<behavior>`.

## 4. Documentation / Closeout

- [ ] 4.1 Update relevant docs if user-visible behavior, API contracts,
  deployment, module responsibility, or cross-module interaction changed.
- [ ] 4.2 Refresh `source-manifest.json`.
- [ ] 4.3 Validate `change-explainer.html` if required.
- [ ] 4.4 Run archive preflight when implementation is complete.

## Backlog / Follow-ups

- [ ] [BACKLOG] <deferred item with rationale, or omit section>
```

Rules:

- Every task should have a clear done condition.
- Do not include speculative tasks that are not required by the proposal/design.
- Use `[BACKLOG]` only for explicit non-blocking follow-ups.
- Unchecked non-backlog tasks are archive blockers.

### 10. Write `specs/<capability>/spec.md`

Spec deltas describe required behavior. Use RFC 2119 style (`SHALL`, `MUST`,
`MAY`, `SHOULD`) and scenario blocks.

Template:

```markdown
# <capability> Specification

## Purpose

<One paragraph describing what this capability owns.>

## Requirements

### Requirement: <requirement title>

<Normative behavior. Use SHALL/MUST for required behavior.>

#### Scenario: <scenario title>

- **GIVEN** <initial state>
- **WHEN** <action/event>
- **THEN** <expected result>
- **AND** <additional expected result>
```

Quality rules:

- Requirements are behavioral contracts, not implementation tasks.
- Each requirement should have at least one scenario.
- Scenarios should be testable.
- Avoid vague words like “support”, “handle”, or “improve” unless followed by
  observable outcomes.
- Do not duplicate an existing authoritative requirement; modify or extend the
  owning capability instead.
- Preserve terminology consistently. If the same concept appears under multiple
  names, choose one term and mention the alias only once if necessary.

### 11. Optional structured elicitation pass

For high-stakes or ambiguous sections, offer an elicitation menu after drafting a
section. Apply the chosen lens, show the improvement, and ask whether to apply
it before editing the document.

Suggested menu:

```text
Advanced Elicitation Options
Choose a number, r to reshuffle, or x to proceed:
1. Pre-mortem Analysis: imagine this change failed and identify preventions.
2. Red Team vs Blue Team: attack and defend the proposal/design.
3. Stakeholder Lens Rotation: inspect user/operator/security/dev/reviewer views.
4. First Principles: strip assumptions and rebuild the requirement.
5. Boundary & Edge Case Sweep: test nulls, max/min, auth, retries, concurrency.
r. Reshuffle with other methods.
x. Proceed.
```

Other useful methods:

- Assumption Audit: list assumptions, rate confidence/impact, shore up weak ones.
- Second-Order Thinking: trace downstream consequences.
- Inversion: ask what would guarantee failure.
- Comparative Analysis Matrix: score alternatives against explicit criteria.
- Architecture Decision Review: force choice, rationale, alternatives, trade-offs.
- Source Triangulation: require multiple source types for risky claims.

Rules:

- Do not apply elicitation changes silently.
- Keep the section source-grounded. If a method reveals a gap, record an open
  question instead of inventing an answer.
- Return to the main workflow after the user accepts, rejects, or skips.

### 12. Load-bearing preservation pass

Before validation, walk the source material claim by claim.

A claim is load-bearing if an implementer, reviewer, or verifier would make a
different decision without it.

For each load-bearing claim, ensure it landed in one of:

- `proposal.md` for why/scope/impact/non-goals;
- `design.md` for decisions, constraints, risks, migration, boundaries;
- `tasks.md` for implementation/verification work;
- `specs/**/spec.md` for normative behavior and scenarios;
- `Open Questions` when unresolved.

Wrapper-only content, rhetoric, duplicate prose, and process metadata can be
dropped, but record important drops in `design.md` preservation notes when the
choice may be questioned later.

### 13. Refresh `source-manifest.json`

After writing markdown/spec files, refresh and validate the manifest with the
bundled helper:

```bash
<skill-dir>/scripts/openspec-build-source-manifest <change-name> --project-root <project-root>
<skill-dir>/scripts/openspec-validate-source-manifest <change-name> --project-root <project-root>
```

Never skip the manifest gate solely because the target workspace lacks
`openspec/scripts/*`. If a project explicitly requires stricter local policy
checks, run them only as additional evidence after the bundled manifest gate.

### 14. Generate `change-explainer.html`

For create and update modes, generate `change-explainer.html` directly from
OpenSpec sources. It is part of the standard OpenSpec change package and is not
a substitute for markdown/specs.

#### Non-negotiable decision-review gate

The output is a **decision-review explainer**, not a generic summary page. A
tool or wrapper returning `ok` is not sufficient proof of success. Success means
the final `change-explainer.html` passes the bundled strict validator (and any
stricter target-project validator when present) and visibly contains the
governed decision-review affordances defined by this skill and project policy.

Do **not** use these shortcuts as the generation path when decision-review HTML
is required:

- `openspec_workflow` / `openspec-workflow` `generate-explainer` with the
  template backend or unspecified backend;
- `openspec-workflow --backend template`;
- copied fixed/basic summary templates that only extract Why / What / Impact /
  Scope;
- any generated file missing
  `<meta name="openspec-explainer-mode" content="decision-review">`.

These paths may produce responsive HTML and may pass loose presentation checks,
but they are known to regress to basic companion pages. If such a file is
created accidentally, discard or rewrite it before declaring the task complete.

#### Direct generation workflow

For Beyourself-style explainers:

1. Refresh source manifest:

   ```bash
   <skill-dir>/scripts/openspec-build-source-manifest <change-name> --project-root <project-root>
   ```

   If the target project has a context-preparation helper, it may be used as an
   optional convenience, but the writer skill does not depend on it.

2. Use the governed explainer rules in this section as the prompt contract. If
   the target project also provides `openspec/prompts/opendesign-change-explainer.md`,
   read it in full and apply any stricter project-local requirements. The
   historical file name may mention Open Design; the prompt rules still apply to
   direct agent generation.

3. Read `openspec/changes/<change-name>/source-manifest.json`, then read every
   file listed in its `sources` array, typically:

   - `proposal.md` — why, what changes, impact, scope;
   - `design.md` — context, goals, decisions, risks, migration;
   - `tasks.md` — implementation plan, tasks, backlog;
   - `specs/*/spec.md` — spec deltas.

4. Write a single self-contained HTML file directly in this agent session:

   ```text
   openspec/changes/<change-name>/change-explainer.html
   ```

Required explainer qualities:

- self-contained HTML, no CDN/remote assets;
- `<html lang="zh-Hant">`;
- `<meta name="openspec-explainer-mode" content="decision-review">`;
- responsive layout, not a fixed 1920×1080 slide stage;
- Traditional Chinese reader-facing prose;
- primary navigation or equivalent segmented navigation;
- before/after comparison when source-grounded;
- source-grounded architecture/flow visual, preferably inline SVG;
- decision points with options, trade-offs, recommendation, risks, confidence;
- implementation slices with acceptance criteria, dependencies, and rollback
  notes when source-grounded;
- verification plan;
- risk register and high-risk filter;
- copyable implementation/review/verification agent prompts;
- copy controls for decision summary and task JSON export when source-grounded.

Before validation, inspect the HTML as prose. If it reads like a generic static
summary page, rewrite it; do not rely on validators alone.

Strict Beyourself validation:

```bash
<skill-dir>/scripts/openspec-validate-explainer <change-name> --project-root <project-root> --require-decision-review
```

Compatibility command for agents expecting the historical script name:

```bash
OPENSPEC_CHANGE_EXPLAINER_REQUIRE_DECISION_REVIEW=1 \
  <skill-dir>/scripts/check-change-explainer.sh <change-name> --project-root <project-root>
```

Expected strict output includes `status=ok` plus individual decision-review
checks for primary navigation, before/after, decision points, implementation
slices, verification plan, risk register, high-risk filter, copy controls, task
JSON export, implementation/review/verification agent prompts, SVG visual, and
responsive/mobile-tablet-desktop layout. If validation fails, fix the issues and
re-validate. Do not report completion until the strict validator passes.

If a project explicitly requires stricter local policy checks, run them only as
additional evidence after the bundled strict validator has passed; never replace
or skip the bundled validator.

Clean up generated context temp files if optional project-local helpers created
them:

```bash
rm -f temp/explainer-contexts/<change-name>-context.md
```

Guardrails:

- Do not introduce requirements, promises, risks, or migrations absent from
  source files.
- Do not create `planning-brief.json` or `visual-script.json` for this path.
- Do not ask Open Design discovery questions or emit `question-form` blocks.
- If a section cannot be grounded in source files, mark it not applicable or
  source-unspecified rather than inventing content.

### 15. Quality validation rubric

Run this rubric before handing off. Fix issues when the source supports a fix;
otherwise record assumptions/open questions.

#### Decision-readiness

- Are trade-offs surfaced honestly?
- Are decisions stated as decisions?
- Are open questions real, not hidden answers?
- Would a reviewer know what they are approving?

#### Done-ness clarity

- Does each requirement/scenario have observable outcomes?
- Are vague words replaced with thresholds, states, or examples?
- Do tasks have clear done conditions?
- Does the verification plan prove the success signal?

#### Scope honesty

- Are non-goals explicit?
- Are assumptions tagged and indexed in proposal/design?
- Are deferred items marked `[BACKLOG]` with rationale?
- Is scope creep blocked at module/API/data boundaries?

#### Downstream usability

- Can an implementer find ownership, files/modules, constraints, and validators?
- Can a tester derive tests from scenarios?
- Are terms consistent across proposal/design/tasks/spec?
- Are cross-references valid?

#### Boundary fit

- Does the spec shape fit the change type?
- Small fix: not over-formalized.
- API/event/data change: contract and compatibility are explicit.
- Regulatory/security change: traceability and risk are explicit.
- UX/user-visible change: user journey and acceptance behavior are explicit.

#### Preservation

- Every load-bearing source claim landed somewhere.
- Dropped content was non-load-bearing or recorded as intentionally omitted.
- Existing authoritative specs were extended, not contradicted.

### 16. Archive-readiness check

Only run archive preflight as readiness evidence. Do not archive unless the user
explicitly asks to close/archive.

Run the bundled archive preflight first:

```bash
<skill-dir>/scripts/openspec-archive-preflight <change-name> --project-root <project-root> --require-decision-review
```

If a project explicitly requires stricter local policy checks, run them only as
additional evidence after the bundled archive preflight; never replace or skip
the bundled preflight.

Treat as blockers unless policy says otherwise:

- unchecked tasks not marked `[BACKLOG]` / explicitly deferred;
- missing or stale `source-manifest.json`;
- missing or invalid required `change-explainer.html`;
- failing spec/explainer/layout validation;
- archive target already exists.

## Output contract

When done, report:

- change path;
- files created/updated;
- capability/spec name(s);
- validations run and results;
- skipped validations and why;
- assumptions and open questions;
- quality-rubric verdict;
- recommended next step: review, implement, revise, or archive readiness.

## Hard guardrails

- Do not convert the change into `/goal` or Goal DAG output from this skill.
- Do not invent requirements absent from user input or source evidence.
- Do not hide ambiguity; ask a clarifying question or put it in Open Questions.
- Do not create implementation tasks that contradict module boundaries.
- Do not create docs in retired paths such as `docs/superpowers/`.
- Do not treat `change-explainer.html` as authoritative over markdown/specs.
- Do not claim validation is unavailable only because the target repo lacks
  `openspec/scripts/*`; use the bundled writer helper.
- Do not archive without explicit user instruction.
- Do not use archive history as current authority unless asked for historical
  rationale.
