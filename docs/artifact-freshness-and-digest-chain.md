# Artifact Freshness and Digest Chain

The Spec Ideation Authoring Flow enforces artifact freshness through a
SHA-256 digest chain. Every downstream artifact records digests of its
load-bearing inputs.

## Required artifacts

All downstream artifacts must carry `inputDigests`:

- `proposal-meaning-analysis.json`
- `value-logic-closure-assessment.json`
- `logic-closure-gate.json`
- `logic-gap-brief.json`
- `clarification-response.json`
- `change-value-assessment-report.json`
- `openspec-authoring-approval-gate.json`
- `spec-kernel.json`
- `pre-spec-gate.json`
- `write-spec-status.json`
- `package-review.json`
- `handoff-ready.json`

## Digest format

### JSON artifacts

SHA-256 over **canonical JSON**:
- Object keys sorted
- UTF-8 encoding
- Trailing newline ignored
- Whitespace formatting ignored

### Markdown / OpenSpec sources

SHA-256 over **exact UTF-8 file content**.

## Fail-closed behavior

If any upstream input digest changes after a downstream artifact is generated:

1. The downstream artifact is considered stale
2. Gates depending on it fail
3. Writer must not proceed
4. Approval must be re-issued or regenerated from current inputs
