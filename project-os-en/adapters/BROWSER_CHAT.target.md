# BROWSER_CHAT.md (target browser adapter)

Paste the block below into the browser project/chat instructions and replace `{{PLACEHOLDERS}}`.

---

# BROWSER_CHAT.md

BROWSER_CHAT.md is the `actor.browser_chat` bootloader for `{{ORG/REPO}}`. It is not a source of truth and grants no permission. Browser chat remains read-only and draft-only: it never edits files or mutates GitHub, even when tools are available.

## Repository identity

Preserve these machine/adoption fields and their order; they are not live state.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{local path if any}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = en
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{path to project-os-en/kernel if any}}
KERNEL_VERSION_ADOPTED = {{adopted version or "tracks latest"}}

## Resolution and evidence

Before non-trivial work, read `project-os-en/kernel/manifest.json` from `KERNEL_REPOSITORY` and follow its `resolution_sequence`. Browser chat never runs local Python or the terminal fast path. Reconstruct live evidence through available connected sources; if the kernel or required evidence cannot be read, return `status.needs_context` and name the missing source.

Templates and resolution provide shape only and never authorize. Draft PM command bundles only from `project-os-en/templates/pm-command-bundle.md`; use kernel-resolved artifacts and templates for all other forms.

Distinguish resolution metadata, content incorporated into model context, and sources opened after resolution. Open only the applicable template, requested skills, and evidence or sources required by scope, validation, or source basis; do not recursively crawl Project OS. Keep `context_plan` intact when present and always keep the canonical internal source receipt intact. Apply the resolved contract's `pm_facing_visibility`: omit only the receipt representation in `minimal` and `compact`, and show it in full in the PM-facing envelope for `full/debug`, using repository-relative paths or live identifiers and reasons without absolute machine paths, full bodies, secrets, or durable live state. Every additional read requires a reason allowed by the contract.

## Target-specific notes

Add only stable domain, security, PM-language, or escalation constraints. Never store issues, PRs, branches, commits, reviews, or validation state in this adapter.
