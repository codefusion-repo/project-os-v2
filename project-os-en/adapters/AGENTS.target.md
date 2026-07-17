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

## Kernel resolution

Before non-trivial work, read `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. When the kernel checkout is available in a terminal, use this fast path. It reads the two persisted fields, accepts only the exact portable reference or an absolute literal, and validates kernel identity before the resolver; it does not use `eval` or expand arbitrary names:

```sh
TARGET_REF=$(sed -n 's/^REPOSITORY_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' AGENTS.md)
KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' AGENTS.md)
case "$TARGET_REF" in
  '$PROJECT_OS_TARGET_ROOT'|'${PROJECT_OS_TARGET_ROOT}')
    : "${PROJECT_OS_TARGET_ROOT:?set PROJECT_OS_TARGET_ROOT to the absolute target path}"
    TARGET_ROOT="$PROJECT_OS_TARGET_ROOT"
    ;;
  /*) case "$TARGET_REF" in *'$'*) exit 1 ;; esac; TARGET_ROOT="$TARGET_REF" ;;
  *) exit 1 ;;
esac
case "$KERNEL_REF" in
  '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}')
    : "${PROJECT_OS_KERNEL_DIR:?set PROJECT_OS_KERNEL_DIR to the absolute kernel path}"
    KERNEL_DIR="$PROJECT_OS_KERNEL_DIR"
    ;;
  /*) case "$KERNEL_REF" in *'$'*) exit 1 ;; esac; KERNEL_DIR="$KERNEL_REF" ;;
  *) exit 1 ;;
esac
case "$TARGET_ROOT" in /*) ;; *) exit 1 ;; esac
case "$KERNEL_DIR" in /*) ;; *) exit 1 ;; esac
case "$KERNEL_DIR" in */project-os-en/kernel) ;; *) exit 1 ;; esac
PROJECT_OS_ROOT="${KERNEL_DIR%/project-os-en/kernel}"
test -n "$PROJECT_OS_ROOT" || exit 1
test -d "$TARGET_ROOT" || exit 1
test -f "$KERNEL_DIR/manifest.json" || exit 1
test -f "$PROJECT_OS_ROOT/tools/project_os_resolve.py" || exit 1
python -c '
import json
import sys
try:
    payload = json.load(open(sys.argv[1], encoding="utf-8"))
    entries = payload.get("manifest") if isinstance(payload, dict) else None
    valid = (
        isinstance(entries, list) and len(entries) == 1
        and isinstance(entries[0], dict)
        and entries[0].get("key") == "manifest.kernel_es"
        and entries[0].get("language") == "en"
        and entries[0].get("active") is True
    )
except (OSError, UnicodeError, json.JSONDecodeError):
    valid = False
raise SystemExit(0 if valid else 1)
' "$KERNEL_DIR/manifest.json" || exit 1
python "$PROJECT_OS_ROOT/tools/project_os_resolve.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_DIR" [--skill skill.<id>]
cd "$TARGET_ROOT"
```

The resolver accelerates resolution; the manifest remains canonical. Both provide shape only and never authorize an action. Follow resolved artifact, template, and skill references without copying their contracts here. Use `context_plan` to distinguish internally loaded files, projected metadata, and referenced templates and skills; never treat it as proof of content delivered to the model.

After resolution, open only the applicable template, requested skills, and Project OS, target, or live-evidence sources required by scope, validation, or source basis. Report actual reads in the canonical source receipt, in the output envelope alongside the artifact, using repository-relative paths or live identifiers and reasons rather than absolute machine paths or full bodies. Every additional read needs a reason allowed by the contract; do not recursively crawl Project OS by default.

## Live evidence

Reconstruct state from GitHub, git, the canonical roadmap `{{#ROADMAP_ISSUE}}`, and target ADRs when applicable. Do not store it here. Fail closed under the resolved kernel when required kernel data, evidence, authority, or validation is missing or ambiguous.

## Target-specific notes

Add only stable build/validation commands, protected paths, domain or security constraints, PM-facing language, and target-specific escalation rules. Generic security, traceability, and validation policy remains in `project-os-en/docs/rules.md` and the resolved kernel.
