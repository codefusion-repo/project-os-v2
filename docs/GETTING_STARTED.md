# Getting Started with Project OS

## Existing Repository Adoption
1. Copy `adapters/AGENTS.target.md` into your repository as `AGENTS.md`.
2. Fill the placeholders (`TARGET_REPOSITORY`, `KERNEL_LOCAL_PATH`).
3. (Optional) Run `python3 -m tools.audit_target_adapters` to verify.

## New Project Bootstrap
1. Initialize a new git repository.
2. Adopt the kernel following the existing repository adoption steps.
3. Configure your initial roadmap issue.

## Browser Chat Setup
1. Use `templates/operations/00-browser-chat-activation.md` to start a session.
2. Browser chat acts as a draft-only actor that uses operations to prepare route-prompts or PM command bundles.

## Terminal Agent Setup
1. Use `templates/operations/01-terminal-agent-setup.md` to activate a terminal agent session.
2. The agent will read `AGENTS.md` and resolve the kernel automatically.

## PM Variable Invocation
Set variables directly in your message or via placeholders to control operation behavior.
Example: `ISSUE_NUMBER=42`
See `docs/PM_VARIABLES.md` for precedence and rules.

## GitHub Traceability
All live project state is stored in GitHub. Do not duplicate issue status, reviews, or branch state in local docs.

## What Project OS does NOT do
Project OS is not an installer, package manager, service, database, web app, or console implementation. It does not store state or grant permissions implicitly.
