# Command bundle: merge PR, close issue, clean up

Phased copy-safe bundle (`boundary.copy_safe_commands`): run phase 1, check
its output, then run phase 2. Fill exact numbers; no placeholders may remain.

Scope: merges PR {{#N}}, closes issue {{#M}}, deletes the work branch.
Risk: merge and closure are not reversible by re-running; rollback is
`git revert` of the merge commit and reopening the issue.

## Phase 1 — verify state

```sh
gh pr view {{#N}} --repo {{org/repo}} --json state,isDraft,mergeable,headRefName
gh pr checks {{#N}} --repo {{org/repo}}
```

Proceed only if: state OPEN, draft false (mark ready first if needed),
mergeable, checks passing or none configured.

## Phase 2 — merge, close, clean up

```sh
gh pr ready {{#N}} --repo {{org/repo}}
gh pr merge {{#N}} --repo {{org/repo}} --merge --delete-branch

cat > /tmp/closure-comment.md <<'BODY'
{{closure comment following templates/closure-comment.md}}
BODY

gh issue close {{#M}} --repo {{org/repo}} --comment-file /tmp/closure-comment.md

git -C {{local/path}} switch main
git -C {{local/path}} pull --ff-only
git -C {{local/path}} branch -d {{work/branch}}
```

Verify: `gh pr view {{#N}}` shows MERGED; `gh issue view {{#M}}` shows CLOSED
with the closure comment; local `main` is at the merge commit.
