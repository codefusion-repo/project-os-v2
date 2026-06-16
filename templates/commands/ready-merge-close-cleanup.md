# Command bundle: merge PR, close issue, clean up

Phased copy-safe bundle (`boundary.copy_safe_commands`): run phase 1, check
its output, copy the exact PR head SHA into phase 2, then run phase 2. Fill
exact numbers, paths, branch names, and `EXPECTED_HEAD_SHA`; no placeholders may
remain.

Scope: merges PR {{#N}}, closes issue {{#M}}, deletes the work branch.
Risk: merge and closure are not reversible by re-running; rollback is
`git revert` of the merge commit and reopening the issue.

## Phase 1 — verify state

~~~sh
gh pr view {{#N}} --repo {{org/repo}} --json state,isDraft,mergeable,mergeStateStatus,headRefName,headRefOid
gh pr checks {{#N}} --repo {{org/repo}}
~~~

Proceed only if: state OPEN, mergeable, and checks passing or none configured.
If `isDraft` is true, phase 2 must mark the PR ready before merge. Copy
`headRefOid` exactly as `EXPECTED_HEAD_SHA` for phase 2. Do not merge if the PR
head changes between review and merge.

## Phase 2 — ready, merge, close, clean up

If phase 1 shows `isDraft: true`, mark the PR ready first:

~~~sh
gh pr ready {{#N}} --repo {{org/repo}}
~~~

Re-check the PR head immediately before merging. The output `headRefOid` must
still equal `EXPECTED_HEAD_SHA`.

~~~sh
gh pr view {{#N}} --repo {{org/repo}} --json state,isDraft,mergeable,mergeStateStatus,headRefName,headRefOid
~~~

~~~sh
gh pr merge {{#N}} --repo {{org/repo}} --merge --delete-branch --match-head-commit {{EXPECTED_HEAD_SHA}}

cat > /tmp/closure-comment.md <<'CLOSURE_BODY_END'
{{closure comment following templates/closure-comment.md}}
CLOSURE_BODY_END

gh issue close {{#M}} --repo {{org/repo}} --comment-file /tmp/closure-comment.md

git -C {{local/path}} switch main
git -C {{local/path}} pull --ff-only
git -C {{local/path}} branch -d {{work/branch}}
~~~

Verify with supported fields only: `gh pr view {{#N}} --repo {{org/repo}}
--json state,mergedAt,headRefOid` shows merged state for the expected head;
`gh issue view {{#M}} --repo {{org/repo}} --json state,closedAt` shows CLOSED;
local `main` is at the merge commit.
