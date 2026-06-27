# Public Usage Model

Project OS operates as a minimal kernel with copy-in adapters and operation templates.

## The Kernel
The operating kernel (`kernel/*.json`) is the absolute source of truth for generic operating behavior (actors, modes, boundaries, workflows, evidence, outputs). It is immutable during task execution.

## Adapters
Adapters (e.g., `AGENTS.md`) point back to the kernel and define repository-wide terminal-agent behavior. They are bootloaders and never override the kernel.

## Templates and Operations
Templates (`templates/operations/`) are public-facing starting points for workflows. They define required variables and canonical behavior but do not duplicate kernel rules.

## GitHub as Source of Truth
All live project state (issues, PRs, review verdicts, branch state) lives ONLY in GitHub. Docs and templates must never store live state.

## PM Approval
Permission comes only from exact scoped PM approval plus kernel-resolved gates. Variables are input selectors and do not confer authorization. `PM_AUTHORIZATION_STATUS` must be explicit when a route prompt claims approval for write-capable work.

## Browser Chat vs Terminal Agent Responsibilities
- **Browser Chat**: Draft-only (`actor.browser_chat`). It drafts responses, route prompts, and PM command bundles. It cannot execute writes.
- **Terminal Agent**: Executes write-capable work (`actor.terminal_agent`) if routed and PM-authorized.
