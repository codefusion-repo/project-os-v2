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

Before non-trivial work, read `project-os-en/kernel/manifest.json` and follow its `resolution_sequence`. When the kernel checkout is available in a terminal, the normal path is this short command:

```sh
python tools/project_os_fast_path.py \
  --actor <actor> --workflow <workflow> --mode <mode> \
  [--change-class change_class.<id>] [--skill skill.<id>]
```

`tools/project_os_fast_path.py` is the single executable source of this logic: it locates the root `AGENTS.md` by walking up from the current directory, validates each candidate in full, and keeps walking up when the candidate is not the root bootloader coherent with the resolved target, so an intermediate `AGENTS.md` inside a subdirectory never stops the search. It reads the two persisted fields, accepts only the exact portable reference or an absolute literal, and checks structural kernel identity before the resolver; it does not use `eval`, does not expand arbitrary names, and invokes `tools/project_os_resolve.py` exactly once, propagating any non-zero exit code unchanged.

The block below is implementation/debugging documentation, not the daily interface: it reproduces the same upward search by delegating each candidate to `project_os_fast_path.py --agents-file`, useful when the short command is not reachable by a relative path from the current directory, or to audit the mechanism step by step:

```sh
select_target_bootloader() {
  AGENTS_FILE=$1
  KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
  case "$KERNEL_REF" in
    '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}') KERNEL_DIR="${PROJECT_OS_KERNEL_DIR:-}" ;;
    /*) case "$KERNEL_REF" in *'$'*) KERNEL_DIR= ;; *) KERNEL_DIR="$KERNEL_REF" ;; esac ;;
    *) KERNEL_DIR= ;;
  esac
  test -n "$KERNEL_DIR" || return 111
  PROJECT_OS_ROOT=$(dirname "$(dirname "$KERNEL_DIR")")
  test -f "$PROJECT_OS_ROOT/tools/project_os_fast_path.py" || return 111
  python "$PROJECT_OS_ROOT/tools/project_os_fast_path.py" --agents-file "$AGENTS_FILE" \
    --actor <actor> --workflow <workflow> --mode <mode> \
    [--change-class change_class.<id>] [--skill skill.<id>]
}
probe=$(pwd)
rc=111
while test "$rc" -eq 111; do
  if test -f "$probe/AGENTS.md"; then
    select_target_bootloader "$probe/AGENTS.md"
    rc=$?
  fi
  if test "$rc" -eq 111; then
    test "$probe" = / && { echo 'no root AGENTS.md coherent with the adopted target' >&2; exit 1; }
    probe=$(dirname "$probe")
  fi
done
test "$rc" -eq 0 || exit "$rc"
cd "$probe" || exit 1
```

Those checks are structural and demonstrable in scope: they require the selected `AGENTS.md` to be the resolved target's own, and they reject references outside the allowlist, relative paths, kernels located on another surface, and manifests that are unreadable, inactive, or in another language, without invoking the resolver when no ancestor satisfies them. Continuing the walk relaxes none of them: a candidate is accepted only when it satisfies every check itself, and the resolver runs once against the accepted candidate. They do not verify repository provenance, commit, signature, hash, or checkout integrity, so they are not a trust anchor: a local directory reproducing that structure remains executable. When a non-zero resolver exit code aborts the fast path, no later step is enabled.

The resolver accelerates resolution; the manifest remains canonical. Both provide shape only and never authorize an action. Follow resolved artifact, template, and skill references without copying their contracts here.

After resolution, open only the applicable template, requested skills, and Project OS, target, or live-evidence sources required by scope, validation, or source basis. PM-facing traceability is `Reviewed evidence` and its per-output equivalent. Every additional read must be justified by scope, validation, or source basis; do not recursively crawl Project OS by default.

## Live evidence

Reconstruct state from GitHub, git, the canonical target roadmap when one exists, and target ADRs when applicable. Do not store their numbers or any other live reference here. Fail closed under the resolved kernel when required kernel data, evidence, authority, or validation is missing or ambiguous.

## Target-specific notes

Add only stable build/validation commands, protected paths, domain or security constraints, PM-facing language, and target-specific escalation rules. Generic security, traceability, and validation policy remains in `project-os-en/docs/rules.md` and the resolved kernel.
