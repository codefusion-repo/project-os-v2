# CLAUDE.md (target-project adapter template)

Copy to a target repository as `CLAUDE.md` after `AGENTS.md` exists, replace
placeholders, delete this heading block.

---

# CLAUDE.md

CLAUDE.md is the Claude-specific adapter for `{{ORG/REPO}}`. It is a compact
bootloader only.

Use `AGENTS.md` for repository-wide terminal-agent behavior; it points to the
kernel manifest's surface-aware resolution, including the
`tools.project_os_resolve` terminal fast path. That command runs from
`REPOSITORY_LOCAL_PATH`, uses `.venv` when present, and passes `--kernel-dir`
for `KERNEL_LOCAL_PATH`. Resolve generic operating behavior from the kernel
referenced there, and live project state from GitHub and git at task time.

CLAUDE.md grants no write permission and stores no live state. Fail closed on
missing kernel, missing evidence, ambiguous authority, or failed validation.
