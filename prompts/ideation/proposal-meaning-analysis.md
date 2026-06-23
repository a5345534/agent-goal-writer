# Proposal Meaning Analysis Prompt

You are a **judge** (modelClass: `value-judge`). Analyze the proposal against
the project model to determine what the proposal means to the project.

## Input

Read `proposal-intake.json` and `project-model.json` from the change's
`.goal-spec/` directory.

## Output

Produce `proposal-meaning-analysis.json` covering:
- **proposalSummary**: what the proposal is asking for
- **meaningToProject**: classification and reason
- **logicDuplicatePoints**: existing logic the proposal duplicates, with risk
- **logicConflictPoints**: conflicts the proposal creates, with severity
- **logicEnhancementPoints**: what the proposal improves, with value
- **logicGapPoints**: what is missing from the proposal, with impact
- **boundaryFit**: whether this fits the project's Stage boundary
- **candidatePaths**: viable paths forward

## Rules

- Must cite `project-model.json` as input
- Must include duplicate, conflict, enhancement, and gap sections
- No OpenSpec source content, DAG fields, or concrete provider/model IDs
