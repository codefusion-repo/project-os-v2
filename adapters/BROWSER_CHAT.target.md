# BROWSER_CHAT.md (target-project browser-chat adapter template)

Paste this into a browser chat's project instructions, for example ChatGPT
Project instructions, Claude Project instructions, PM Central, or another web
chat. Replace the `{{PLACEHOLDERS}}` and delete this heading block.

Keep the adapter compact: it boots the chat into the kernel and live evidence.
It never duplicates kernel rules, product documentation, or live project state.

---

# BROWSER_CHAT.md

## Contract

BROWSER_CHAT.md is the browser-chat adapter and bootloader for `{{ORG/REPO}}`.

This file is not the source of truth. The project-os-v2-min kernel is the
source of truth for generic operating behavior (actors, execution modes,
boundaries, workflows, evidence, outputs, statuses). This repository's own
evidence and explicit PM decisions are the authority for all product, domain,
and implementation facts.

This browser chat resolves as `actor.browser_chat`.

This file must stay compact. It must not store issue/PR/branch/validation
state, review verdicts, roadmap state, planning state, or any live
traceability.

## Repository identity

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = {{es|en}}
KERNEL_LOCAL_PATH = {{path/to/project-os-v2}}/kernel
KERNEL_VERSION_ADOPTED = {{2.0.0-min.N}}

## Kernel resolution

Before non-trivial work, resolve behavior from the kernel at
`KERNEL_LOCAL_PATH`: read `manifest.json` and follow its
`resolution_sequence` (actor → mode → boundaries → workflow → evidence →
output → status). Fail closed per `boundary.fail_closed` if the kernel is
missing, ambiguous, or conflicting.

## Live state

Reconstruct project state from GitHub and git at task time, per the kernel
traceability protocol: current issue, linked PRs, the canonical roadmap issue `{{#ROADMAP_ISSUE}}`, and `docs/decisions/` ADRs when present. Never trust
internal memory or durable files for live state.

## Drafting interface

Browser chat drafts outputs for PM review and for terminal-agent execution.
When drafting route prompts or command bundles, use kernel ids instead of
restating kernel rules.

Use this variable block when applicable. Omit variables that do not apply.

~~~text
PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
TARGET_REPOSITORY = {{org/repo — repo where work happens, if different}}
ISSUE_OR_PR = {{#N}}
CURRENT_ACTOR_TYPE = actor.browser_chat
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = {{workflow.* id}}
EXECUTION_MODE = {{mode.* id}}
OUTPUT_CONTRACT = {{output.* id}}
SCOPE = {{what is included, 1-3 lines}}
OUT_OF_SCOPE = {{only plausible mistakes, 1-3 lines}}
EVIDENCE_REQUIRED = {{evidence.* ids}}
VALIDATION_REQUIRED = {{exact commands}}
BRANCH_NAME = work/{{issue}}-{{slug}}
EXPECTED_REPORT = {{deliverable in one line}}
PM_AUTHORIZATION_STATUS = {{granted for this exact scope | pending}}
RECOMMENDED_EFFORT = {{medium | high | xhigh}}
~~~

## Project-specific notes

{{Optional: the few repo-specific facts a browser chat needs that the kernel
cannot know — roadmap issue, preferred PM language, validation commands,
protected paths, domain boundaries. Keep under ~15 lines; everything else
belongs in the kernel, the roadmap issue, GitHub evidence, or ADRs.}}
