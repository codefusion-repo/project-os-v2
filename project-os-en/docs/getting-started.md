# Getting started with Project OS

**A short guide to a clean start: confirm the external prerequisites, choose
your surfaces, set up the browser, prepare a terminal only when you will
delegate, open the first session on live evidence, and run the full cycle —
delegate, review, correct, and close.**

## 1. External prerequisites

Project OS does not control these points. Have them ready first:

- **A target repo on GitHub.** The product you will adopt, implement, review,
  or audit.
- **A GitHub account with access to the target repo.** The required connected
  access is to the target: issues, PRs, diffs, and docs as the flow needs.
- **A browser chat with read-only GitHub/target access.** Recommended: ChatGPT
  with GitHub connected. Any browser surface works when it supports a
  project/chat with persistent instructions and can read the target repo.
- **A terminal/local setup with GitHub access to the target when you will
  delegate implementation.** It must read and write only what is approved;
  when the flow uses issues or PRs, it also needs issue/PR access on the
  target.
- **A readable Project OS repo.** Use it as the readable source of kernel,
  operations, adapters, and docs; never present it as a private requirement
  tied to a special account.
- **No secrets to start.** You need no `.env`, tokens, private keys, or
  production credentials to activate a session.

## 2. Surfaces

Capability follows the surface, not the role:

- **Human PM.** Decides scope, exact approvals, merge, issue close, labels,
  tags, releases, settings, secrets, and deployments.
- **Browser chat.** Good at drafting, reviewing, routing, and analysis. It
  stays read-only/draft-only even when the connected tool could write.
- **Terminal agent.** Runs delegated implementation: edits in scope,
  validates, commits/pushes, and opens a draft PR only with live evidence,
  the right branch, and exact PM approval.

Two repos appear in almost every flow:

- **The Project OS repo:** kernel, operations, adapters, and docs.
- **The target repo:** the product where work is adopted or executed. When
  developing Project OS itself, target and Project OS can be the same repo.

Name which repo plays each role when you ask an agent to work.

Besides the acting surface, choose the language surface by path: Spanish is
the default (`project-os-es/`); English is an explicit selection
(`project-os-en/`, or `--kernel-dir project-os-en/kernel` on the resolver).
There is no global selector and no persisted language preference.

## 3. Browser setup

Do this on the browser surface when you will use it to draft or review:

1. Use ChatGPT (recommended) or another browser surface that supports a
   project/chat with persistent instructions.
2. Load the Project OS instructions or the target's adapter when one exists;
   as the browser project/chat bootloader use
   [`project-os-en/adapters/BROWSER_CHAT.target.md`](../adapters/BROWSER_CHAT.target.md).
3. Connect or verify GitHub on that surface.
4. Confirm it can read the target repo; when applicable, confirm it can also
   read the Project OS repo.
5. When it cannot read required evidence, it must answer
   `status.needs_context` naming what is missing. It must never invent issue,
   PR, branch, diff, or roadmap state.

## 4. Terminal/local setup

Do this only when you will delegate implementation to a terminal agent:

1. Have the target repo cloned or the local workspace ready.
2. Verify `gh auth status` against the target repo.
3. Confirm issue and PR access on the target when the agent must read them,
   comment, or open PRs.
4. Have Python available when you will use the resolver.
5. Adopt or review the target's terminal adapter with
   [`project-os-en/adapters/AGENTS.target.md`](../adapters/AGENTS.target.md)
   and keep its portable references with `PROJECT_OS_TARGET_ROOT` and
   `PROJECT_OS_KERNEL_DIR` defined locally, or use literal absolute values in
   both fields for a private adoption.

Adoption is copy-based by design: copying the adapter into the target and
filling its identity fields is the complete install. The persisted
`$PROJECT_OS_TARGET_ROOT` and `$PROJECT_OS_KERNEL_DIR` references let the
adapter be shared without committing personal paths. Define their values only
in the local environment, for example with `export`, and verify adoption with
the auditor. A private single-machine adapter may instead use literal absolute
paths; a neutral mount such as `/workspace/...` is valid but not required.
`$PWD`, other variables, composed values, and placeholders fail closed. There
is no installer, package, or CLI; any future tooling has its own gate and is
not required to operate today.

Resolver fast path for the adopted target:

```sh
AGENTS_FILE=
probe=$(pwd)
while :; do
  test -f "$probe/AGENTS.md" && { AGENTS_FILE="$probe/AGENTS.md"; break; }
  test "$probe" = / && break
  probe=$(dirname "$probe")
done
test -n "$AGENTS_FILE" || exit 1
TARGET_REF=$(sed -n 's/^REPOSITORY_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
KERNEL_REF=$(sed -n 's/^KERNEL_LOCAL_PATH[[:space:]]*=[[:space:]]*//p' "$AGENTS_FILE")
case "$TARGET_REF" in
  '$PROJECT_OS_TARGET_ROOT'|'${PROJECT_OS_TARGET_ROOT}')
    : "${PROJECT_OS_TARGET_ROOT:?set PROJECT_OS_TARGET_ROOT}"
    TARGET_ROOT="$PROJECT_OS_TARGET_ROOT"
    ;;
  /*) case "$TARGET_REF" in *'$'*) exit 1 ;; esac; TARGET_ROOT="$TARGET_REF" ;;
  *) exit 1 ;;
esac
case "$KERNEL_REF" in
  '$PROJECT_OS_KERNEL_DIR'|'${PROJECT_OS_KERNEL_DIR}')
    : "${PROJECT_OS_KERNEL_DIR:?set PROJECT_OS_KERNEL_DIR}"
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
test "$AGENTS_FILE" -ef "$TARGET_ROOT/AGENTS.md" || exit 1
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
  --kernel-dir "$KERNEL_DIR" [--skill skill.<id>] || exit $?
cd "$TARGET_ROOT" || exit 1
```

The same resolution consumes either persisted modality, without `eval` or
arbitrary name expansion, and behaves identically from the target root or any
of its subdirectories. The preceding checks are structural: they require the
read `AGENTS.md` to be the resolved target's own and reject references outside
the allowlist, relative paths, kernels on another surface, and manifests that
are unreadable, inactive, or in another language. They do not verify provenance,
signature, hash, or checkout integrity, so they are not a trust anchor. A
non-zero resolver exit code aborts the fast path with that same code and enables
no later step. Manual resolution of `project-os-en/kernel/manifest.json`
remains the canonical fallback. The resolver output never grants permission
and never reads GitHub/git on your behalf. Browser chat does not run local
Python; it reads the manifest through available sources and stays read-only
and draft-only.

### Hydration level

The resolver accepts `--hydration-level minimal|compact|full/debug`. When
omitted, it uses `compact`: the practical execution view without dumping the
whole contract. `minimal` retains the IDs, boundaries, evidence, outputs,
statuses, non-authorization, and secret safety needed to stop prohibited work.
`compact` adds concise mandatory guidance, the selected actor/workflow/mode,
and resolvable references. `full/debug` expands selected-resolution metadata
for review, debugging, or audit; it is not the normal mode and does not replace
the canonical manifest.

The response declares `hydration_level` and has these deterministic shapes:

- `minimal`: manifest/actor/mode/workflow identity, every applicable boundary,
  prohibited actions, required evidence, allowed outputs, and referenced statuses.
- `compact`: all of `minimal` plus concise mandatory rules, selected operating
  context, and artifact/template/skill references.
- `full/debug`: all of `compact` plus complete selected-resolution metadata,
  including active flags and internal audit links.

The resolver keeps `context_plan` intact at all three levels. During execution,
the executor always keeps the internal receipt and applies the canonical
`pm_facing_visibility` policy: it hides only the receipt's Markdown section in
`minimal` and `compact`, and shows it in full in `full/debug`. Bare `debug` is
not a valid alias.

```sh
python tools/project_os_resolve.py --actor actor.terminal_agent \
  --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
  --kernel-dir project-os-en/kernel --hydration-level full/debug
```

Within the resolver, the level changes returned content only: it does not read
GitHub/git, invent project state, or grant permission. The executor uses the
same selector only for the receipt's PM-facing presentation. Unknown values
fail closed. The canonical
Python parameter is `hydration_level`; `compact` remains a compatibility
alias. The pre-existing `--compact` flag only controls JSON indentation.
Measured sizes per level, with declared method and date, live in
[context-benchmark.md](context-benchmark.md).

When drafting outputs, the resolver may expose artifacts with a
`required_template`; use that template from
[`project-os-en/templates/`](../templates/README.md) as the output's shape,
never as permission. When the PM asks or a route prompt recommends a skill,
pass it with `--skill`; the resolver returns it as `requested_skills`,
referenced by `required_skill` under
[`project-os-en/skills/`](../skills/), with no extra authority.

## 5. First session

1. **Choose the surface.** Browser chat drafts, reviews, and routes; the
   terminal agent runs delegated implementation; the Human PM keeps merge,
   close, settings, secrets, and deployments.
2. **Activate browser chat with
   [MOS-0.1](../operations/phase-0/MOS-0.1-activate-browser-session.md),
   declaring `TARGET_REPOSITORY` in `owner/repo` format.** MOS-0.1 asks for
   the target before resolving the initial state and rebuilds
   `evidence.repo_state` only against that repository; when the target is
   missing, invalid, or unreadable, it returns `status.needs_context` without
   using another connected repository.
3. **Verify adoption when a target exists with
   [MOS-0.5](../operations/phase-0/MOS-0.5-verify-target-adoption.md),** which
   audits browser and terminal readiness separately and only returns a global GO
   when both applicable surfaces are ready. When the target has not adopted
   Project OS yet, use
   [MOS-0.2](../operations/phase-0/MOS-0.2-bootstrap-new-project.md) on a new
   project or
   [MOS-0.3](../operations/phase-0/MOS-0.3-adopt-existing-project.md) on an
   existing one: both are browser-first and first draft a PM-applicable browser
   adapter (without blocking startup on a missing roadmap), then route adapter
   writes to the terminal agent in `mode.delegated_commit_pr` through a route
   prompt with exact PM approval.
4. **Use
   [MOS-0.6](../operations/phase-0/MOS-0.6-handoff-session-context.md) only
   when the session is incoherent, exhausted, or needs handoff.**
5. **Pick the next lifecycle-phase operation** from the catalog
   [`operations/README.md`](../operations/README.md) and the day-to-day cycle
   in [rhythm.md](rhythm.md).
6. **Optionally generate local prompts** with
   `python tools/operation_prompt_wizard.py --language en` (or answer its
   one-time `es/en` question; Spanish stays the default). The selection is
   session-only, does not execute the chosen work, and never adopts a
   language on the target.

## 6. Delegate, review, correct, and close

The full cycle of one unit of work, once the session is active:

1. **Delegate the implementation.** Draft the route prompt with
   [MOS-3.4](../operations/phase-3/MOS-3.4-draft-implementation-route-prompt.md)
   (the wizard captures `HYDRATION_LEVEL`; `compact` is the default) and hand
   it to the terminal agent. The agent re-resolves the kernel, verifies
   preflight, live scope, and exact PM approval, implements only the scope,
   validates, and opens a draft PR. The route prompt shapes and never
   authorizes by itself.
2. **Review the PR first.** Use
   [MOS-3.7](../operations/phase-3/MOS-3.7-review-pr-before-close.md): compare
   the unit of work against the diff, the final files, the reported
   validation, and the risks. Reports and bodies are claims until verified
   against live evidence.
3. **Correct inside the same issue/PR.** When review finds gaps, draft the
   correction with
   [MOS-3.5](../operations/phase-3/MOS-3.5-draft-correction-route-prompt.md)
   on the same branch and the same PR; do not open new units to correct live
   scope.
4. **Close and verify post-merge.** Merge and close always belong to the
   Human PM:
   [MOS-3.6](../operations/phase-3/MOS-3.6-draft-closeout-commands.md) drafts
   the copy-safe closeout commands and
   [MOS-3.9](../operations/phase-3/MOS-3.9-verify-post-merge.md) verifies the
   real post-merge outcome on live evidence.

Stop with the resolved status whenever the kernel, scope, authority, evidence,
or validation is missing or ambiguous.

**Next:** read [rules.md](rules.md), then [rhythm.md](rhythm.md).
