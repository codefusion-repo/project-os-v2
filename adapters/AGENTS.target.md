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

Standard metadata block. Keep these field names and order so agents and the
future Operations Console read adapters the same way across repositories.
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
`KERNEL_LOCAL_PATH`: read `manifest.json` and follow its
`resolution_sequence` exactly. The manifest is the canonical sequence; this
adapter only points to it. Fail closed per `boundary.fail_closed` if the kernel
is missing, ambiguous, or conflicting.

## Live state

Reconstruct project state from GitHub and git at task time, per the kernel
traceability protocol: current issue, linked PRs, the canonical roadmap issue
`{{#ROADMAP_ISSUE}}`, and `docs/decisions/` ADRs when present. Never trust
internal memory or durable files for live state.

## Project-specific notes

{{Optional: the few repo-specific facts an agent needs that the kernel cannot
know — build/validation commands, protected paths, domain boundaries. Keep
under ~15 lines, compact, non-live, and target-owned: no issue/PR/branch state,
no SHAs, no review status, no release status. Everything else belongs in the
kernel, the roadmap issue, or ADRs.}}
