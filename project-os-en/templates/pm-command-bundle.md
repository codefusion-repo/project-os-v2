# PM command bundle — canonical contract

This is the single canonical source of shape and style for
`output.pm_command_bundle`. Other artifacts only reference it; they do not
repeat it or create alternative rules for PM-facing commands. It neither stores
live state nor authorizes actions: before drafting, read the repository, issue,
PR, branch, paths, and reviewed head SHA live.

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

Comment through a body file. Scope and rollback: publish only the reviewed
comment; human rollback is a later correction.

```sh
cat > /tmp/pr-comment.md <<'PR_COMMENT_END'
<reviewed Markdown body>
PR_COMMENT_END

gh pr comment <pr-number> --repo <owner/repo> --body-file /tmp/pr-comment.md
```

Mark a draft as ready. Include this only when evidence confirms it remains a
draft and exact PM approval exists for that transition.

```sh
gh pr ready <pr-number> --repo <owner/repo>
```

Merge a reviewed head. Risk: repeating the merge is irreversible; rollback:
revert the merge commit when applicable.

```bash
gh pr merge <pr-number> --repo <owner/repo> --merge --delete-branch \
  --match-head-commit <reviewed-head-sha> --body "Closes #<issue-number>."
```

Close the issue through a body file. Include this only with exact approval for
closure; merge does not imply closure.

```sh
cat > /tmp/issue-close.md <<'ISSUE_CLOSE_END'
<reviewed closure evidence>
ISSUE_CLOSE_END

gh issue comment <issue-number> --repo <owner/repo> --body-file /tmp/issue-close.md
gh issue close <issue-number> --repo <owner/repo>
```

Update and clean up locally. Include this only after merge is confirmed and the
exact path and branch have been reviewed.

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
