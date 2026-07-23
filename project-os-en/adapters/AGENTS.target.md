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

Before non-trivial work, read `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. When the kernel checkout is available in a terminal, use this fast path. It locates the root `AGENTS.md` by walking up from the current directory: it validates each candidate in full and keeps walking up when the candidate is not the root bootloader coherent with the resolved target, so an intermediate `AGENTS.md` inside a subdirectory never stops the search. It reads the two persisted fields, accepts only the exact portable reference or an absolute literal, and checks structural kernel identity before the resolver; it does not use `eval`, does not expand arbitrary names, and propagates any non-zero resolver exit code unchanged:

```sh
select_target_bootloader() {
  AGENTS_FILE=$1
  TARGET_REF=$(sed -n 's/^REPOSITORY_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  case "$TARGET_REF" in
    '$PROJECT_OS_TARGET_ROOT'|'${PROJECT_OS_TARGET_ROOT}')
      test -n "${PROJECT_OS_TARGET_ROOT:-}" || return 1
      TARGET_ROOT="$PROJECT_OS_TARGET_ROOT"
      ;;
    /*) case "$TARGET_REF" in *'$'*) return 1 ;; esac; TARGET_ROOT="$TARGET_REF" ;;
    *) return 1 ;;
  esac
  case "$KERNEL_REF" in
    '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}')
      test -n "${PROJECT_OS_KERNEL_DIR:-}" || return 1
      KERNEL_DIR="$PROJECT_OS_KERNEL_DIR"
      ;;
    /*) case "$KERNEL_REF" in *'$'*) return 1 ;; esac; KERNEL_DIR="$KERNEL_REF" ;;
    *) return 1 ;;
  esac
  case "$TARGET_ROOT" in /*) ;; *) return 1 ;; esac
  case "$KERNEL_DIR" in /*) ;; *) return 1 ;; esac
  case "$KERNEL_DIR" in */project-os-en/kernel) ;; *) return 1 ;; esac
  PROJECT_OS_ROOT="${KERNEL_DIR%/project-os-en/kernel}"
  test -n "$PROJECT_OS_ROOT" || return 1
  test -d "$TARGET_ROOT" || return 1
  test "$AGENTS_FILE" -ef "$TARGET_ROOT/AGENTS.md" || return 1
  test -f "$KERNEL_DIR/manifest.json" || return 1
  test -f "$PROJECT_OS_ROOT/tools/project_os_resolve.py" || return 1
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
' "$KERNEL_DIR/manifest.json" || return 1
}
AGENTS_FILE=
probe=$(pwd)
while :; do
  if test -f "$probe/AGENTS.md" && select_target_bootloader "$probe/AGENTS.md"; then
    break
  fi
  AGENTS_FILE=
  test "$probe" = / && break
  probe=$(dirname "$probe")
done
test -n "$AGENTS_FILE" || {
  echo 'no root AGENTS.md coherent with the adopted target' >&2
  exit 1
}
python "$PROJECT_OS_ROOT/tools/project_os_resolve.py" \
  --actor <actor> --workflow <workflow> --mode <mode> \
  --kernel-dir "$KERNEL_DIR" [--change-class change_class.<id>] [--skill skill.<id>] || exit $?
cd "$TARGET_ROOT" || exit 1
```

Those checks are structural and demonstrable in scope: they require the selected `AGENTS.md` to be the resolved target's own, and they reject references outside the allowlist, relative paths, kernels located on another surface, and manifests that are unreadable, inactive, or in another language, without invoking the resolver when no ancestor satisfies them. Continuing the walk relaxes none of them: a candidate is accepted only when it satisfies every check itself, and the resolver runs once against the accepted candidate. They do not verify repository provenance, commit, signature, hash, or checkout integrity, so they are not a trust anchor: a local directory reproducing that structure remains executable. When a non-zero resolver exit code aborts the fast path, no later step is enabled.

The resolver accelerates resolution; the manifest remains canonical. Both provide shape only and never authorize an action. Follow resolved artifact, template, and skill references without copying their contracts here. Use `context_plan` to distinguish internally loaded files, projected metadata, and referenced templates and skills; never treat it as proof of content delivered to the model.

After resolution, open only the applicable template, requested skills, and Project OS, target, or live-evidence sources required by scope, validation, or source basis. Keep `context_plan` and the canonical internal source receipt intact with the actual reads. Apply the resolved contract's `pm_facing_visibility`: omit only the receipt representation in `minimal` and `compact`, and show it in full in the PM-facing envelope for `full/debug`, using repository-relative paths or live identifiers and reasons rather than absolute machine paths or full bodies. Every additional read needs a reason allowed by the contract; do not recursively crawl Project OS by default.

## Live evidence

Reconstruct state from GitHub, git, the canonical target roadmap when one exists, and target ADRs when applicable. Do not store their numbers or any other live reference here. Fail closed under the resolved kernel when required kernel data, evidence, authority, or validation is missing or ambiguous.

## Target-specific notes

Add only stable build/validation commands, protected paths, domain or security constraints, PM-facing language, and target-specific escalation rules. Generic security, traceability, and validation policy remains in `project-os-en/docs/rules.md` and the resolved kernel.
