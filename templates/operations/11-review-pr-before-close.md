# Review Pr Before Close

## When to use it
Use this operation to review pr before close.

## Canonical behavior
- **Workflow**: `workflow.review_before_close`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.closure_comment`
- **Required Evidence**: `evidence.pr_diff, evidence.review_evidence`

## Variables
- **Required**: `PR_NUMBER`
- **Optional**: `NONE`
- **Inferred from live state**: Current state

## PM Input Placeholders
- <PR_NUMBER>

## Example Invocation
```
REVIEW_PR_BEFORE_CLOSE
PR_NUMBER=VALUE
```

## Responsibilities
- **Browser Chat**: Drafts outputs referencing canonical templates (`templates/route-prompt.md` or `templates/pm-command-bundle.md`).
- **Terminal Agent**: Executes write-capable work if routed and authorized with `PM_AUTHORIZATION_STATUS`.
- **Exact PM Approval Required**: Yes, for any writes or state changes.

## Out of scope
- Role-based actors or new actor ids.
- Live state in templates.
- Duplicating command-bundle rules outside `templates/pm-command-bundle.md`.
- Duplicating route-prompt rules outside `templates/route-prompt.md`.

## Expected Result
A drafted artifact or execution report conforming to `output.closure_comment`.
