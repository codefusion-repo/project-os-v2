# PM Variables

This document explains the PM variable system used in operations and templates. Variables are input selectors for operations, not authorization boundaries.

## Syntax
- **Placeholder Syntax**: `<VARIABLE_NAME>` (e.g. `<ISSUE_NUMBER>`)
- **Override Syntax**: `VARIABLE_NAME=VALUE` (e.g. `ISSUE_NUMBER=123` or `ISSUE_NUMBER=#123`)

## Types of Variables
- **Required Variables**: Must be provided for the operation to proceed. Missing variables will resolve to `status.needs_context` or `status.needs_pm_decision`.
- **Optional Variables**: Can be provided to customize behavior.
- **Inferred Variables**: Values that may be inferred from live state (e.g., current branch, open issues).

## Precedence Rules
1. Explicit PM-provided variables in the current message have highest precedence.
2. Filled template values come next.
3. Live GitHub/git evidence may be used only when the operation requires live state.

## Normalization & Conflict Rules
- Issue and PR variables accept either `123` or `#123`. Human-facing references always render as `#123`.
- Missing required variables resolve to `status.needs_context` or `status.needs_pm_decision`.
- Conflicting variables must be surfaced; do not silently choose one.

## Secret-Safety Rules
Variables must **never** carry secrets, tokens, credentials, `.env` values, cookies, session tokens, private keys, or secret-looking values. If a variable contains a secret, the system will fail closed.

## Examples
- `ISSUE_NUMBER=#305 TARGET_REPOSITORY=codefusion-repo/project-os-v2`
- `PM_QUESTION=What should we do with #286?`
- `FEEDBACK_PM_HUMANO=Please adjust the wording in the PR.`
