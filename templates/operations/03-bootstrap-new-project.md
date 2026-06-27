# Bootstrap New Project

## When to use it
Use this operation to bootstrap new project.

## Canonical behavior
- **Workflow**: `workflow.target_adoption`
- **Execution Mode**: `mode.delegated_commit_pr`
- **Output Contract**: `output.adoption_packet`
- **Required Evidence**: `evidence.target_adoption`

## Variables
- **Required**: `TARGET_REPOSITORY`
- **Optional**: `NONE`
- **Inferred from live state**: Current state

## PM Input Placeholders
- <TARGET_REPOSITORY>

## Example Invocation
```
BOOTSTRAP_NEW_PROJECT
TARGET_REPOSITORY=VALUE
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
A drafted artifact or execution report conforming to `output.adoption_packet`.
