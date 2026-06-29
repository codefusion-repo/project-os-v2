# PM command bundle — canonical style

This is the **one canonical source** for how a browser chat drafts the copy-safe
command bundles a PM runs by hand (`output.pm_command_bundle`). Every other file
points here instead of restating these rules:

- `kernel/boundaries.json` (`boundary.copy_safe_commands`) keeps only the hard
  safety floor and points here for shape and style;
- `kernel/outputs.json` (`output.pm_command_bundle`) names the contract sections
  and points here;
- `templates/route-prompt.md` points here and to `output.pm_command_bundle` and
  never introduces separate command rules.

This is the single canonical command-bundle source: separate per-operation
command files with their own style, safety, formatting, preflight, verification,
heredoc, or shell-control-flow rules are not allowed. Worked examples belong
here, as sections below.

This file stores no live state. Exact issue/PR/branch/SHA values are read live
from GitHub and git at task time (`docs/TRACEABILITY_PROTOCOL.md`) and filled in
before the PM runs anything.

## Default shape: short, linear, copy-safe

The default PM bundle is a **short, linear, readable sequence the PM can copy and
run top to bottom**. After a `workflow.review_before_close` GO, the closeout is
just the few writes the review already authorized — not a program.

A default bundle has:

- a one-line prose statement of what it does and its scope (outside code blocks);
- exact repository, PR, issue, branch, and (when reviewed) head-SHA values — no
  placeholder a prior command already produced;
- one or, at most, a few command blocks in run order;
- a final verification line using supported fields only;
- one prose line of risk and rollback.

## Minimal safety (always kept, even in the simplest bundle)

- **Exact targets.** Real `--repo org/repo`, `#N`, branch, and path values.
- **Body files for long GitHub bodies.** Write closure/PR/issue prose to a file
  with a quoted heredoc delimiter that cannot appear in the body, then pass
  `--body-file`. Keeps long Markdown out of the executable line.
- **Head-SHA guard when a reviewed head SHA is available.** Pass
  `--match-head-commit <sha>` to `gh pr merge` so the merge aborts if the head
  moved since review.
- **Final verification.** End with read-only `gh`/`git` checks confirming the
  intended end state.
- **Supported GitHub CLI `--json` fields only.** Never emit unsupported
  pseudo-fields such as `stateReason`, `merged` or `isLatest`. Prefer verified fields:
  `state`, `isDraft`, `mergeable`, `mergeStateStatus`, `headRefName`,
  `headRefOid`, `mergedAt`, `closedAt`. When unsure, discover supported fields
  first (e.g. pass an invalid `--json` value to list them).
- **No nested triple-backtick fences.** Use a tilde-fenced outer block, or move
  inner fenced content to a body file.
- Keep scope, risk, and rollback in prose **outside** the executable blocks.

## Disallowed in a default bundle

Default PM bundles must **not** use:

- `exit`;
- `set -euo pipefail`;
- large `if`/`else` or `case` control flow;
- shell guards that stop, cut, or corrupt the terminal session;
- unnecessary repeated preflights after a `review_before_close` GO.

These turn a copy-safe sequence into a fragile shell program. A recent closeout
failed exactly this way: a guard compared `gh pr view --json mergeable` against
`true` while `gh` returned `MERGEABLE`, so the whole bundle aborted. A linear
sequence has no guard to misfire.

## When a defensive bundle is allowed

Generate a defensive / preflight-heavy bundle (extra checks, phasing, explicit
abort conditions) **only** when:

- the PM explicitly asks for a defensive or preflight-heavy bundle; or
- live evidence is missing, stale, conflicting, unsafe, or **not yet reviewed**
  (for example the PR head may move, draft state is unknown, or checks have not
  been read).

When defensive phasing is justified, still avoid `exit` and terminal-stopping
guards: phase the bundle (run, read output, fill the next value, run) and tell
the PM the exact condition to check between phases in prose.

## Examples (derived from the current kernel)

These examples are not a generic command cookbook. They cover the work that
emits `output.pm_command_bundle` today: `workflow.pm_intake`,
`workflow.review_before_close`, and `workflow.release_readiness` list
`output.pm_command_bundle` in their `allowed_output_refs`
(`kernel/workflows.json`). In practice this includes issue creation, reviewed
closeout, and release/tag bundles.

If a future kernel change makes other work emit `output.pm_command_bundle`, add
its example here with the evidence; do not invent command families outside the
model.

### Closeout — comment / ready / merge / close / cleanup

Scope: optionally comment on PR `#N`, optionally mark it ready, post closure
evidence on issue `#M`, merge with a closing reference, and clean up the branch. Risk: merge and
closure are not reversible by re-running; rollback is `git revert` of the merge
commit and reopening the issue. `{{REVIEWED_HEAD_SHA}}` is the `headRefOid` from
the review.

Optional — post a PR review comment first (only when there is one to post):

~~~sh
cat > /tmp/pr-comment.md <<'PR_COMMENT_END'
{{PR comment body}}
PR_COMMENT_END

gh pr comment {{#N}} --repo {{org/repo}} --body-file /tmp/pr-comment.md
~~~

Optional — mark the PR ready (only when it is a draft and the PM approved that
action):

~~~sh
gh pr ready {{#N}} --repo {{org/repo}}
~~~

Then write the closure comment (per `templates/artifacts.md`, Closure comment) to a body
file and run the closeout top to bottom:

~~~sh
cat > /tmp/closure-comment.md <<'CLOSURE_BODY_END'
{{closure comment following templates/artifacts.md (Closure comment)}}
CLOSURE_BODY_END

gh issue comment {{#M}} --repo {{org/repo}} --body-file /tmp/closure-comment.md

gh pr merge {{#N}} --repo {{org/repo}} --merge --delete-branch --match-head-commit {{REVIEWED_HEAD_SHA}} --body "Closes {{#M}}."

git -C {{local/path}} switch main
git -C {{local/path}} pull --ff-only origin main
git -C {{local/path}} branch -D {{work/branch}}
git -C {{local/path}} fetch --prune origin
~~~

The optional lines are variants, not a separate rule system: drop them when they
do not apply, keep the rest linear. Verify with supported fields only:
`gh pr view {{#N}} --repo {{org/repo}} --json state,mergedAt,headRefOid` shows
merged at the reviewed head; `gh issue view {{#M}} --repo {{org/repo}} --json
state,closedAt` shows `CLOSED`; local `main` is at the merge commit.

### Create an issue

The same create pattern serves any single-issue creation — the next roadmap
issue when none exists, or a follow-up issue from review findings — one canonical
pattern, no separate file per case.

Scope: creates one issue in `{{org/repo}}`. Rollback: close the issue. The
browser chat fills the body from `templates/artifacts.md` (Issue) and the exact repo/title;
the PM runs it.

~~~sh
cat > /tmp/issue-body.md <<'ISSUE_BODY_END'
{{issue body following templates/artifacts.md (Issue)}}
ISSUE_BODY_END

gh issue create --repo {{org/repo}} \
  --title "{{title}}" \
  --body-file /tmp/issue-body.md
~~~

Verify: the command prints the new issue URL; open it and confirm the body
rendered correctly.
