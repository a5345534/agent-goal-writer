# OpenSpec Authoring Approval Gate

The OpenSpec Authoring Approval Gate is the formal checkpoint before OpenSpec
writing may begin. It records an explicit approval decision from an authorized
approver.

## Gate purpose

- Approve OpenSpec authoring — not implementation execution
- Separate the decision to write specs from the decision to execute code
- Enforce artifact freshness by referencing the current value report digest

## Allowed decisions

| Decision | Effect |
|----------|--------|
| `continue_discussion` | Loop back to assessment or gap completion |
| `abandon_proposal` | Terminal — no OpenSpec package |
| `accept_no_build_recommendation` | Terminal — no OpenSpec package, preserve rationale |
| `approve_smaller_scope_openspec_authoring` | Writer proceeds within `approvedScope` |
| `approve_openspec_authoring` | Writer proceeds with full scope |

## Forbidden

- `execute_implementation` or any implementation-implying language
- Stale report digest — gate must reference current change value report digest

## Approver types

- `human`
- `role`
- `orchestrator`
- `policy`
