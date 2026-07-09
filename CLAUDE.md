# CLAUDE.md

CLAUDE.md is the Claude-specific adapter for `codefusion-repo/project-os-v2`. It is a compact bootloader only.

Use `AGENTS.md` for repository-wide terminal-agent behavior; it points to the
active Spanish kernel manifest resolution, including the
`project-os-es/tools/resolver.py` terminal fast path. That command runs from
`REPOSITORY_LOCAL_PATH`, uses `.venv` when present, and passes `--kernel-dir`
for `KERNEL_LOCAL_PATH`. Resolve generic operating behavior from the kernel
referenced there, and live project state from GitHub and git at task time.
`legacy-project-os/` is archival and never an active resolution source.

CLAUDE.md grants no write permission and stores no live state. Fail closed on
missing kernel, missing evidence, ambiguous authority, or failed validation.
