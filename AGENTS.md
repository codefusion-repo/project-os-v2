# AGENTS.md

## Contract

AGENTS.md is the repository-wide terminal-agent adapter and bootloader for
`codefusion-repo/project-os-v2`.

This file is not the source of truth. The kernel in `kernel/` is the source of
truth for operating behavior. GitHub issues, PRs, commits, comments, and
reviews are the only live project state. This repository operates under its
own kernel (self-dogfood).

This file must stay compact and must not store live traceability.

## Repository identity

PROJECT_NAME = project-os-v2-min
REPOSITORY_NAME = codefusion-repo/project-os-v2
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
AGENT_INSTRUCTIONS_LANGUAGE = en
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = kernel
KERNEL_VERSION_ADOPTED = target-dogfood-baseline-2026-06-16

## Kernel resolution

Before non-trivial work, read `kernel/manifest.json` and follow its
`resolution_sequence` exactly. The manifest is the canonical sequence; this
adapter only points to it. Use only the four statuses in
`kernel/statuses.json`. Fail closed (`boundary.fail_closed`) if kernel files
are missing, ambiguous, or conflicting.

## Live state

Reconstruct state from GitHub at task time per
`docs/TRACEABILITY_PROTOCOL.md`: the current issue, linked PRs, and the
canonical Project OS Operations Console roadmap issue, resolved live from
GitHub. Never trust internal memory or durable files for live state.

## Validation

For any change in this repository run:

- `python3 -m tools.validate_kernel`
- `python3 -m pytest tests/ -q`

Report results per `output.execution_report`.
