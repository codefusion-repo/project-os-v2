# PM command bundle — canonical contract

This is the single canonical source of shape and style for
`output.pm_command_bundle`. Other artifacts only reference it; they do not
repeat it or create alternative rules for PM-facing commands. It neither stores
live state nor authorizes actions: before drafting, read the repository, issue,
PR, branch, paths, and reviewed head SHA live.

## Closeout after GO

When `workflow.review_before_close` is resolved with a GO verdict over the
current unit and head, that GO is the closeout gate. Deliver the complete
bundle directly in the same response: ready if the PR is still a draft, merge
of the reviewed head, evidence and unit closure, branch cleanup, and final
read-only verification. Do not request a second round of PM approval for each
action or withhold parts of the bundle pending that approval.

The human PM executes the bundle; `browser_chat` only drafts it and never
executes ready, merge, closure, or cleanup. GO does not delegate execution to
the agent. Preserve operational conditions: exact targets, the reviewed head,
and cleanup only after confirming the merge. If evidence changes or the bundle
becomes stale, return to `workflow.review_before_close` before using it.

This delivery rule is exclusive to `workflow.review_before_close` with resolved
GO. Other consumers of `output.pm_command_bundle`, including
`workflow.pm_intake`, `workflow.release_readiness`, and `workflow.target_adoption`,
retain their exact approvals. It does not change authority for implementation,
correction, deploy, release, settings, or other workflows.

## Default shape

The default bundle is a short linear sequence that the PM can copy
and run from top to bottom. State scope, manual conditions, risk, and rollback
in prose outside executable blocks. Provide one, or at most a few, native
`bash` or `sh` blocks in order. Each block must be fully copyable with its
copy button and preserve valid shell bytes, including line breaks, backslashes,
and heredocs.

Use exact reviewed targets: `--repo`, PR/issue number, branch, paths, and,
when applicable, the head SHA. Use only `gh --json` fields confirmed to be
supported. End with read-only verification of the final state.

Writing blocks must not contain shell; neither may blockquotes, indented lists,
inline text, or other surfaces that can transform line breaks, backslashes, or
heredocs. Do not use nested fences.

## Prohibited by default

- Long chains joined with `&&` or `||`, command substitutions used as
  guards, and chained `test` commands that abort the remainder.
- `exit`, `set -e`, `set -u`, `set -o pipefail`, or equivalents.
- Large `if` or `case` blocks, loops, shell functions, or guards that cut
  off or corrupt the session.
- Redundant preflights after a resolved `workflow.review_before_close`.
- `gh pr view --comments` when a narrower query avoids GraphQL dependencies
  or unnecessary warnings.

A defensive or preflight-heavy bundle is allowed only when the PM explicitly
requests it, or when evidence is missing, stale, conflicting, or has not yet
been reviewed. In that case, separate it into phases and explain in prose what
the PM must verify between blocks. Never turn it into a self-aborting shell
program.

## Compact examples

Angle-bracket values are exact values read live while drafting, not data the PM
must discover by running the bundle.

Body-only replacement for an existing issue. This is the default route only
when replacing the complete body; `gh issue edit` remains allowed for labels,
assignees, milestones, or other properties. Risk: an incorrect target replaces
another issue's body; rollback: repeat the sequence with the reviewed previous
body.

```sh
cat > /tmp/issue-body.md <<'ISSUE_BODY_END'
<reviewed Markdown body>
ISSUE_BODY_END

gh api --method PATCH "repos/<owner>/<repo>/issues/<issue-number>" \
  -F "body=@/tmp/issue-body.md" --silent
gh api --method GET "repos/<owner>/<repo>/issues/<issue-number>" \
  --jq '{number,html_url,updated_at}'
```

Body-only replacement for an existing PR. This is the default route only when
replacing the complete body; `gh pr edit` remains allowed for reviewers, the
base branch, or other properties. Risk: an incorrect target replaces another
PR's body; rollback: repeat the sequence with the reviewed previous body.

```sh
cat > /tmp/pr-body.md <<'PR_BODY_END'
<reviewed Markdown body>
PR_BODY_END

gh api --method PATCH "repos/<owner>/<repo>/pulls/<pr-number>" \
  -F "body=@/tmp/pr-body.md" --silent
gh api --method GET "repos/<owner>/<repo>/pulls/<pr-number>" \
  --jq '{number,html_url,updated_at}'
```

Comment through a body file. Scope and rollback: publish only the reviewed
comment; human rollback is a later correction.

```sh
cat > /tmp/pr-comment.md <<'PR_COMMENT_END'
<reviewed Markdown body>
PR_COMMENT_END

gh pr comment <pr-number> --repo <owner/repo> --body-file /tmp/pr-comment.md
```

Mark a draft as ready. Include this only when evidence confirms it remains a
draft. Include it directly in closeout after resolved GO; outside that route,
exact PM approval is required for the transition.

```sh
gh pr ready <pr-number> --repo <owner/repo>
```

Merge a reviewed head. Risk: repeating the merge is irreversible; rollback:
revert the merge commit when applicable.

```bash
gh pr merge <pr-number> --repo <owner/repo> --merge --delete-branch \
  --match-head-commit <reviewed-head-sha> --body "Closes #<issue-number>."
```

Close the issue through a body file. In closeout after resolved GO, include
the evidence and explicit closure if the unit remains open after the merge.
Outside that route, exact approval for closure is required; merge does not
imply closure.

```sh
cat > /tmp/issue-close.md <<'ISSUE_CLOSE_END'
<reviewed closure evidence>
ISSUE_CLOSE_END

gh issue comment <issue-number> --repo <owner/repo> --body-file /tmp/issue-close.md
gh issue close <issue-number> --repo <owner/repo>
```

Update and clean up locally. Include this in the closeout bundle after GO with
the exact reviewed path and branch; the PM runs it only after confirming merge.

```sh
git -C <local-path> switch main
git -C <local-path> pull --ff-only origin main
git -C <local-path> branch -D <work-branch>
git -C <local-path> fetch --prune origin
```

Final read-only verification: this must be the bundle's last block.

```sh
gh pr view <pr-number> --repo <owner/repo> --json state,mergedAt,headRefOid
gh issue view <issue-number> --repo <owner/repo> --json state,closedAt
git -C <local-path> status --short --branch
```
