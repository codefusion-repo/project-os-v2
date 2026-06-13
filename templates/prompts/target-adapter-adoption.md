# Target adapter adoption issue and route

Use this from `workflow.target_adoption` when a target repository needs its
adapter files repointed to project-os-v2-min. It is a reusable pattern for
drafting the target issue and the browser-chat to terminal-agent route; it does
not authorize target writes by itself.

Keep target facts in the target issue and target repository. Do not copy live
issue/PR/branch/validation state into this Project OS template.

## Target issue body

Title:
`[Project OS] Repoint AGENTS.md and CLAUDE.md to project-os-v2-min`

Why this exists:
The target adapter files still point at a pre-v2 Project OS resolver, resolver
contract, or generic Project OS path. Repointing them lets agents resolve
generic operating behavior from `codefusion-repo/project-os-v2/kernel/manifest.json`
while preserving target-owned product, domain, runtime, and validation truth in
the target repository.

Objective:
Update only the target adapter files needed for Project OS adoption so terminal
agents and Claude-specific sessions bootstrap through project-os-v2-min.

Source basis:
- The target adoption or roadmap issue for `{{TARGET_REPOSITORY}}`.
- The target's current `AGENTS.md` and `CLAUDE.md` state, read live.
- `codefusion-repo/project-os-v2` adapter templates:
  `adapters/AGENTS.target.md` and `adapters/CLAUDE.target.md`.
- The project-os-v2-min kernel manifest:
  `codefusion-repo/project-os-v2/kernel/manifest.json`.

Scope:
- Update `AGENTS.md` to resolve generic operating behavior from
  `codefusion-repo/project-os-v2/kernel/manifest.json`.
- Update `CLAUDE.md` to defer repository-wide behavior to `AGENTS.md` and the
  same project-os-v2-min kernel.
- Preserve or add the target repository identity, default branch, work branch
  pattern, PM-facing language, and target validation commands.
- Preserve the canonical roadmap pointer when the target has one; if no
  canonical roadmap exists, state that in the target issue instead of inventing
  one.
- Remove stale pre-v2 resolver, resolver-contract, or generic Project OS path
  references from the adapter files.

Out of scope:
- No product, domain, runtime, build, deployment, or automation changes.
- No target roadmap rewrite unless separately scoped and approved.
- No labels, milestones, settings, releases, tags, merges, closures, or issue
  mutations beyond the exact PM-approved target issue action.
- No live traceability stored in durable target files.

Acceptance criteria:
- `AGENTS.md` and `CLAUDE.md` point agents to the project-os-v2-min kernel
  manifest path above.
- Adapter files stay compact bootloaders and do not duplicate kernel rules,
  product documentation, roadmap bodies, or live state.
- Target-owned product, domain, runtime, safety, and validation truth remains in
  the target repository, target roadmap issue, target ADRs, or target docs.
- The canonical roadmap pointer is preserved when one exists.
- Stale pre-v2 resolver-contract references are gone.
- File edits were performed only after exact PM approval for the target
  repository, issue, files, and mode.

Validation:
- `git status --short --branch`
- `git branch --show-current`
- `git log -1 --oneline`
- `git diff --check`
- The target repository's documented validation commands, if adapter-only
  changes require any.

Risk and rollback:
Risk is low if the change stays adapter-only. Rollback is restoring the previous
target `AGENTS.md` and `CLAUDE.md` versions from git.

Non-authorization:
This target issue authorizes no target writes, adapter edits, GitHub mutations,
merges, closures, labels, releases, settings changes, deployment, automation, or
product changes by itself. Exact PM approval is still required for the target
repository and action.

## Route prompt

Fill the variables, delete unused lines, paste into the terminal agent after
the PM has granted exact target authorization for this adapter-only work.

~~~text
PROJECT_NAME = {{TARGET_PROJECT_NAME}}
REPOSITORY_NAME = {{TARGET_REPOSITORY}}
TARGET_REPOSITORY = {{TARGET_REPOSITORY}}
ISSUE_OR_PR = {{#TARGET_ISSUE}}
CURRENT_ACTOR_TYPE = actor.browser_chat
TARGET_ACTOR_TYPE = actor.terminal_agent
WORKFLOW = workflow.issue_implementation
EXECUTION_MODE = {{mode.local_implementation | mode.delegated_commit_push | mode.delegated_commit_pr}}
OUTPUT_CONTRACT = output.execution_report
SCOPE = Adapter-only Project OS adoption: update AGENTS.md and CLAUDE.md so they point to codefusion-repo/project-os-v2/kernel/manifest.json, preserve target-owned product truth, preserve the canonical roadmap pointer when one exists, and remove stale pre-v2 resolver-contract references.
OUT_OF_SCOPE = No product/runtime/build/deployment changes; no automatic adapter migration; no labels, milestones, settings, releases, merges, closures, automation, or target mutations outside this exact adapter issue.
EVIDENCE_REQUIRED = evidence.issue_scope, evidence.branch_preflight, evidence.target_adoption, evidence.pm_approval, evidence.validation_output
VALIDATION_REQUIRED = git status --short --branch; git branch --show-current; git log -1 --oneline; git diff --check; {{target validation commands, if any}}
BRANCH_NAME = work/{{issue}}-project-os-adapter-adoption
EXPECTED_REPORT = Execution report with changed files, evidence reviewed, validation output, boundary preservation review, and statement that only target adapter files were modified.
PM_AUTHORIZATION_STATUS = {{granted for this exact target repository, issue, adapter files, and mode | pending}}
RECOMMENDED_EFFORT = medium

Implement ISSUE_OR_PR in TARGET_REPOSITORY only after resolving the target
adapter and project-os-v2-min kernel. Read the issue, current AGENTS.md,
current CLAUDE.md, linked PRs, current branch state, and canonical roadmap
issue live. Update only the scoped adapter files on BRANCH_NAME, validate,
and report per OUTPUT_CONTRACT. This prompt carries scope and shape only;
authorization is limited to PM_AUTHORIZATION_STATUS and does not permit any
other target mutation.
~~~
