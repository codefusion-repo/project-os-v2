# Command bundle: create an issue

Copy-safe bundle (`boundary.copy_safe_commands`). The browser chat fills the
body from `templates/issue.md` and the exact repo/title; the PM executes.

Scope: creates one issue in `{{org/repo}}`. Rollback: close the issue.

```sh
cat > /tmp/issue-body.md <<'BODY'
{{issue body following templates/issue.md}}
BODY

gh issue create --repo {{org/repo}} \
  --title "{{title}}" \
  --body-file /tmp/issue-body.md
```

Verify: the command prints the new issue URL; open it and confirm the body
rendered correctly.
