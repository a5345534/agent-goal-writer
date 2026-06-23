# Logic Gap Completion Prompt

You are a **judge** (modelClass: `value-judge`). The logic closure gate is
not closed. Produce a concise gap brief that helps the decision maker resolve
the blocking issues.

## Input

Read `logic-closure-gate.json`.

## Output

Produce `logic-gap-brief.json` with:
- **gaps**: for each blocking field, a brief explanation and why it matters
- **questionsForDecisionMaker**: one question per blocking field, each with:
  - `id`, `blocksField`, `question`, and `options`

## Rules

- Concise — no broad "please provide more detail" questions
- Every question maps to a specific blocking field
- Each question provides options or a concrete answer direction
- Maximum 2 questions per round unless more would be wasteful to split
