# AGENTS.md (target terminal adapter)

Copy the block below to the target as `AGENTS.md`, replace `{{PLACEHOLDERS}}`, and remove these copy instructions. Keep the portable references or replace them with literal absolute paths for a private single-machine adoption.

---

# AGENTS.md

AGENTS.md is the terminal bootloader for `{{ORG/REPO}}`. It is not a source of truth and grants no permission: generic behavior lives in `project-os-en/kernel/`, while target facts are reconstructed from live evidence.

## Repository identity

These paths and the adopted version are machine/adoption configuration, not live state. Preserve these fields and their order. The portable references are exactly `PROJECT_OS_TARGET_ROOT` for the target checkout and `PROJECT_OS_KERNEL_DIR` for the kernel; their absolute values live only in the local environment and never in this file.

PROJECT_NAME = {{PROJECT_NAME}}
REPOSITORY_NAME = {{ORG/REPO}}
REPOSITORY_LOCAL_PATH = $PROJECT_OS_TARGET_ROOT
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = en
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = $PROJECT_OS_KERNEL_DIR
KERNEL_VERSION_ADOPTED = {{adopted version or "tracks latest"}}

## Local configuration

The only normal way to configure the portable references is an untracked local
`.envrc` containing the absolute `PROJECT_OS_TARGET_ROOT` and
`PROJECT_OS_KERNEL_DIR` values. Load it manually and explicitly in your
terminal; it requires no additional tools. The fast path never runs `source`,
`eval`, or `.envrc`; without valid variables it fails closed before the
resolver.

## Kernel resolution

Before non-trivial work, read `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. When the kernel checkout is available in a terminal, the normal path is this short command. It is location-safe: it behaves identically from the target root or any subdirectory because it locates the script from the already-known kernel reference, without searching for it again:

```sh
python "$PROJECT_OS_KERNEL_DIR/../../tools/project_os_fast_path.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  [--change-class change_class.<id>] [--skill skill.<id>]
```

If your `AGENTS.md` uses a literal absolute path in `KERNEL_LOCAL_PATH` instead of the portable reference, substitute `$PROJECT_OS_KERNEL_DIR` with that same literal path in the command.

`tools/project_os_fast_path.py` is the single executable source: it fails closed
when it cannot establish a structurally coherent adoption and delegates exactly
once to `tools/project_os_resolve.py`. Bootloaders and adapters consume that
entrypoint; they do not provide alternative implementations.

The resolver accelerates resolution; the manifest remains canonical. Both provide shape only and never authorize an action. Follow resolved artifact, template, and skill references without copying their contracts here.

After resolution, open only the applicable template, requested skills, and Project OS, target, or live-evidence sources required by scope, validation, or source basis. PM-facing traceability is `Reviewed evidence` and its per-output equivalent. Every additional read must be justified by scope, validation, or source basis; do not recursively crawl Project OS by default.

## Live evidence

Reconstruct state from GitHub, git, the canonical target roadmap when one exists, and target ADRs when applicable. Do not store their numbers or any other live reference here. Fail closed under the resolved kernel when required kernel data, evidence, authority, or validation is missing or ambiguous.

## Target-specific notes

Add only stable build/validation commands, protected paths, domain or security constraints, PM-facing language, and target-specific escalation rules. Generic security, traceability, and validation policy remains in `project-os-en/docs/rules.md` and the resolved kernel.
