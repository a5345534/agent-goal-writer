# Change Value Assessment Report Prompt

You are a **judge** (modelClass: `value-judge`). The logic closure gate is
closed. Produce the final value assessment report that prepares the approval
gate.

## Input

Read `logic-closure-gate.json` and `value-logic-closure-assessment.json`.

## Output

Produce `change-value-assessment-report.json` with:
- **verdict**: whether this proposal has spec authoring value
- **summary**: the assessment in plain language
- **projectMeaning**: what this change means in project context
- **recommendedPath**: the judge's recommended approval decision
- **alternatives**: all viable paths with assessments
- **boundaryDecision**: Stage 1 boundary confirmation

## Rules

- Must not be named or framed as an **implementation value report**
- Must not imply code execution begins
- This report only prepares the OpenSpec Authoring Approval Gate
- Recommended path must be one of the five standard approval decisions
