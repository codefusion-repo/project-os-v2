# PM command bundle — canonical contract

This is the single canonical shape and style source for copy-safe PM command bundles. A bundle gives the Human PM commands to run; it never authorizes execution and never stores live state.

## Default shape

- State scope, target, expected effect, risk, and rollback in prose outside executable blocks.
- Use a short linear sequence with exact repository, issue, PR, branch, and environment targets.
- Use one fenced shell block per independently copyable action.
- Put long GitHub bodies in a temporary file created with a quoted heredoc and pass it through `--body-file`.
- End with final read-only verification using only supported `gh --json` fields.

Final read-only verification must confirm the intended target state without
performing another write.

## Prohibited by default

- Long chains joined with `&&` or `||`, nested shells, or commands that replace/cut the PM session.
- Nested triple-backtick fences, guessed targets, unsupported pseudo-fields, environment dumps, or secret values.
- Merge, closure, labels, tags, releases, settings, deployment, or secret-store changes without separate exact PM approval.
- Broad cleanup or recovery commands outside the scoped action.

## Compact examples

```sh
gh issue create --repo <owner/repo> --title <title> --body-file <body-file>
```

```sh
gh pr comment <pr-number> --repo <owner/repo> --body-file <comment-file>
```

```bash
cat > <comment-file> <<'PR_COMMENT_END'
<markdown body>
PR_COMMENT_END
```

```sh
gh pr merge <pr-number> --repo <owner/repo> --squash --match-head-commit <reviewed-head-sha>
```

```sh
gh pr view <pr-number> --repo <owner/repo> --json state,mergedAt,headRefOid
```

Writing blocks stay separate from verification. Rollback is prose unless an exact, separately approved rollback command is in scope.
