# Human Qa Checklist

## When to use it
Use this operation to human qa checklist.

## Canonical behavior
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Required Evidence**: `evidence.repo_state`

## Variables
- **Required**: `ISSUE_NUMBER`
- **Optional**: `NONE`
- **Inferred from live state**: Current state

## PM Input Placeholders
- <ISSUE_NUMBER>

## Example Invocation
```
HUMAN_QA_CHECKLIST
ISSUE_NUMBER=VALUE
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
A drafted artifact or execution report conforming to `output.status_result`.
