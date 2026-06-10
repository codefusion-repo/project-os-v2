# CLAUDE.md

CLAUDE.md is the Claude-specific adapter for `codefusion-repo/project-os-v2`.
It is a compact bootloader only.

Use `AGENTS.md` for repository-wide terminal-agent behavior. Resolve operating
behavior from `kernel/` (start at `kernel/manifest.json`, follow its
`resolution_sequence`). Reconstruct live project state from GitHub and git at
task time per `docs/TRACEABILITY_PROTOCOL.md`.

CLAUDE.md grants no write permission and stores no live state. Fail closed on
missing kernel files, missing evidence, ambiguous authority, or failed
validation.
