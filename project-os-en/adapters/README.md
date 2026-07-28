# Compact English adapters

Adapters are copyable bootloaders containing adoption metadata, kernel pointers, and stable target constraints. The kernel, resolver, docs, and templates own generic behavior; adapters never authorize actions or store live state.

- `AGENTS.target.md` is the only complete terminal bootloader.
- `CLAUDE.target.md` and `GEMINI.target.md` are shims to `AGENTS.md`.
- `BROWSER_CHAT.target.md` is the separate `actor.browser_chat` bootloader: read-only, draft-only, and without the local Python fast path.

Replace placeholders and preserve metadata order. The shared terminal adapter uses only the allowlisted `$PROJECT_OS_TARGET_ROOT` and `$PROJECT_OS_KERNEL_DIR` references; define their absolute values in an untracked local `.envrc` and do not commit them. This is the only normal route: load it manually and explicitly in the terminal, with no additional tools. The fast path never runs `source`, `eval`, or `.envrc`; it fails closed without valid variables. A private adapter may retain literal absolute paths, including neutral mounts such as `/workspace/...`, but that is not the normal shared route. `$PWD`, other variables, variable composition, and arbitrary shell expansion are not accepted. Use `Target-specific notes` only for stable commands, protected paths, domain/security constraints, PM-facing language, and escalation rules. Do not copy kernel contracts into adapters.
