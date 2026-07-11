# Compact English adapters

Adapters are copyable bootloaders containing adoption metadata, kernel pointers, and stable target constraints. The kernel, resolver, docs, and templates own generic behavior; adapters never authorize actions or store live state.

- `AGENTS.target.md` is the only complete terminal bootloader.
- `CLAUDE.target.md` and `GEMINI.target.md` are shims to `AGENTS.md`.
- `BROWSER_CHAT.target.md` is the separate `actor.browser_chat` bootloader: read-only, draft-only, and without the local Python fast path.

Replace placeholders and preserve metadata order. Use `Target-specific notes` only for stable commands, protected paths, domain/security constraints, PM-facing language, and escalation rules. Do not copy kernel contracts into adapters.
