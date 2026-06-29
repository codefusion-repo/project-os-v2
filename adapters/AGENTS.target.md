# AGENTS.md (target-project adapter template)

Copy this file to a target repository as `AGENTS.md`, replace the
`{{PLACEHOLDERS}}`, and delete this heading block. Keep the adapter compact:
it boots agents into the kernel and the live evidence; it never duplicates
kernel content, product documentation, or live project state.

---

# AGENTS.md

## Contract

AGENTS.md is the repository-wide terminal-agent adapter and bootloader for
`{{ORG/REPO}}`.

This file is not the source of truth. The project-os-v2-min kernel is the
source of truth for generic operating behavior (actors, execution modes,
boundaries, workflows, evidence, outputs, statuses). This repository's own
evidence and explicit PM decisions are the authority for all product, domain,
and implementation facts.

This file must stay compact. It must not store issue/PR/branch/validation
state, review verdicts, roadmap state, planning state, or any live
traceability.

## Repository identity

Standard metadata block. Keep these field names and order so agents and any
future tooling read adapters the same way across repositories.
`REPOSITORY_LOCAL_PATH`, `KERNEL_LOCAL_PATH`, and `KERNEL_VERSION_ADOPTED` are
per-machine/adoption configuration, not live project state.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{absolute local path to this repo, e.g. $HOME/projects/.../repo}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = {{es|en}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{absolute local path to the kernel, e.g. $HOME/projects/.../project-os-v2/kernel}}
KERNEL_VERSION_ADOPTED = {{adopted kernel version e.g. 2.0.0-min.1, or "tracks latest"}}

## Kernel resolution

Before non-trivial work, resolve behavior from the kernel at
`KERNEL_LOCAL_PATH` by following `manifest.json`'s `resolution_sequence` exactly.
`manifest.json` is the canonical resolution source and owns surface-aware routing
through its `resolution_strategy`; this adapter only points to it and defines no
competing resolution order. On this terminal surface the manifest's default is
the resolver fast path from the checkout
`python3 -m tools.project_os_resolve --actor <actor> --workflow <workflow> --mode <mode>`,
with manual `manifest.json` resolution as the canonical fallback.

Resolution shapes behavior only and grants no permission
(`boundary.output_not_permission`). Fail closed per `boundary.fail_closed` if the
kernel is missing, ambiguous, or conflicting.

## Live state

Reconstruct target project state for `REPOSITORY_NAME` from GitHub and git at
task time, per `KERNEL_REPOSITORY`'s traceability protocol: current issue,
linked PRs, the canonical roadmap issue `{{#ROADMAP_ISSUE}}`, and the target
repo's `docs/decisions/` ADRs when present. Never trust internal memory or
durable files for live state.

## Project-specific notes

Security / project constraints:
- Follow target-specific security practices; for web/API/user-facing changes,
  consider OWASP secure-coding risks such as auth, authorization, sessions,
  input validation, file uploads, redirects, dependency risk, and admin surfaces.
- Never print, paste, commit, upload, summarize, quote, or expose `.env`,
  `.env.*`, private keys, API tokens, OAuth/client secrets, database URLs,
  cookies, session tokens, JWTs, production credentials, payment-provider keys,
  SSH/GPG keys, CI secrets, or secret-looking values.
- Treat sensitive values as unsafe even in tests, logs, screenshots, shell output,
  GitHub comments, PR bodies, validation reports, and copied command output.
- Redact sensitive values as `[REDACTED]`; report only file paths, variable names,
  and risk type.
- Do not run broad environment/config dumps such as `env`, `printenv`, `set`,
  framework config dumps, or CI secret-context dumps unless the PM explicitly
  scopes a safe redacted diagnostic.
- Do not modify secret stores, rotate keys, change production credentials, edit
  deployment secrets, or touch payment/auth production settings without separate
  exact PM approval.
- Keep build commands, protected paths, domain constraints, and validation notes
  here when they are stable and target-owned; never store issue/PR/branch state,
  SHAs, review status, release status, or live validation results.
