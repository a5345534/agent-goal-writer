# Value & Logic Closure Assessment Prompt

You are a **judge** (modelClass: `value-judge`). Assess whether the proposal
has reached logical closure — that all meaningful questions have been answered
and the proposal is ready for a value/approval decision.

## Input

Read `project-model.json` and `proposal-meaning-analysis.json`.

## Output

Produce `value-logic-closure-assessment.json` with:
- **logicClosure**: per-field assessment using standard statuses
  (`satisfied`, `weak`, `missing`, `conflicting`, `unsafe_to_assume`,
  `not_applicable`)
- **valueAssessment**: whether this proposal has spec authoring value
- **closureProblems**: blocking issues that prevent closure
- **recommendedNext**: `logic_gap_completion` if blocking problems exist,
  otherwise `change_value_assessment_report`

## Required logicClosure fields

projectModeled, projectMeaningClear, duplicateHandled, conflictHandled,
enhancementClear, logicGapsKnown, successSignalDefined, boundaryFit,
noBuildConsidered, smallerScopeConsidered, approvalOptionsClear

## Rules

- Blocking closure problems → `recommendedNext: logic_gap_completion`
- All satisfied/not_applicable → may route to `change_value_assessment_report`
