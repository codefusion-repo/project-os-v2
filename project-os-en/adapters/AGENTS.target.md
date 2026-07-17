# AGENTS.md (target terminal adapter)

Copy the block below to the target as `AGENTS.md`, replace `{{PLACEHOLDERS}}`, and remove these copy instructions.

---

# AGENTS.md

AGENTS.md is the terminal bootloader for `{{ORG/REPO}}`. It is not a source of truth and grants no permission: generic behavior lives in `project-os-en/kernel/`, while target facts are reconstructed from live evidence.

## Repository identity

These paths and the adopted version are machine/adoption configuration, not live state. Preserve these fields and their order.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = {{absolute path to target repo}}
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = en
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{absolute path to project-os-v2/project-os-en/kernel}}
KERNEL_VERSION_ADOPTED = {{adopted version or "tracks latest"}}

## Kernel resolution

Before non-trivial work, read `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. When the kernel checkout is available in a terminal, use this fast path:

```sh
KERNEL_DIR="{{absolute path to project-os-v2/project-os-en/kernel}}"
PROJECT_OS_ROOT="${KERNEL_DIR%/project-os-en/kernel}"
python "$PROJECT_OS_ROOT/tools/project_os_resolve.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_DIR" [--skill skill.<id>]
```

The resolver accelerates resolution; the manifest remains canonical. Both provide shape only and never authorize an action. Follow resolved artifact, template, and skill references without copying their contracts here. Use `context_plan` to distinguish internally loaded files, projected metadata, and referenced templates and skills; never treat it as proof of content delivered to the model.

After resolution, open only the applicable template, requested skills, and Project OS, target, or live-evidence sources required by scope, validation, or source basis. Report actual reads in the canonical source receipt, in the output envelope alongside the artifact, using repository-relative paths or live identifiers and reasons rather than absolute machine paths or full bodies. Every additional read needs a reason allowed by the contract; do not recursively crawl Project OS by default.

## Live evidence

Reconstruct state from GitHub, git, the canonical roadmap `{{#ROADMAP_ISSUE}}`, and target ADRs when applicable. Do not store it here. Fail closed under the resolved kernel when required kernel data, evidence, authority, or validation is missing or ambiguous.

## Target-specific notes

Add only stable build/validation commands, protected paths, domain or security constraints, PM-facing language, and target-specific escalation rules. Generic security, traceability, and validation policy remains in `project-os-en/docs/rules.md` and the resolved kernel.
