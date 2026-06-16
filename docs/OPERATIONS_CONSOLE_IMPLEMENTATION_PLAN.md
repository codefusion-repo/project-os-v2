# Operations Console Implementation Plan

OC.1 turns the operations catalog into a compact implementation plan for the
future Operations Console. The plan consumes existing Project OS semantics from
`kernel/`, `docs/OPERATIONS_CATALOG.md`, and
`templates/commands/PM_COMMAND_BUNDLE.md`; it does not define new actors,
workflows, statuses, approval rules, or command-bundle rules.

This file stores no live state. Issue, PR, branch, review, validation, dogfood,
and decision state must still be read live from GitHub and git per
`docs/TRACEABILITY_PROTOCOL.md`.

## Planning rules

- GitHub remains the source of truth for project state, evidence, issues, PRs,
  branches, comments, reviews, and closure packets.
- The console may store operational queue state, audit records, runner health,
  and UI cache, but never durable project truth that cannot be reconstructed
  from GitHub.
- The server/API stays lightweight. The desktop runner executes local work over
  an outbound connection, with WebSocket primary transport and polling or
  reconciliation fallback.
- Claude CLI and Codex CLI execution happens locally on the PM computer through
  terminal sessions, not through model APIs or hosted agent runners.
- Route prompts and command bundles are bootloaders. Detailed scope stays in
  GitHub issues, and PM command-bundle shape stays in
  `templates/commands/PM_COMMAND_BUNDLE.md`.
- PM approval follows `kernel/execution_modes.json` `approval_note` and
  `kernel/evidence.json` `evidence.pm_approval`: exact scoped approval applies
  only to the same scope; material changes require re-resolution.
- Write-capable actions require explicit PM action, visible preflight, audit,
  verification, and the existing Project OS boundaries. Merge requires a
  reviewed head SHA guard.

## Phase disposition

OC.2 through OC.5 should remain as separate implementation issues because each
creates a different dependency layer. OC.6 should be split: preview generation
is useful and low risk before write-capable buttons, while gated writes need
their own issue. OC.7 should remain one issue for QA, asset, and security gates
because those gates share the same packet/display behavior. OC.8 should be
split between console dogfood instrumentation and the final Project OS
standardization decision.

The result is a nine-issue plan: eight issues in `codefusion-repo/project-os-console`
and one synthesis issue in `codefusion-repo/project-os-v2`. No target-repository
implementation issue is part of the console build plan; target dogfood work
requires separately scoped target issues chosen by the PM.

| Order | Phase | Target repository | Disposition | Dependency |
| --- | --- | --- | --- | --- |
| 1 | OC.2 | `codefusion-repo/project-os-console` | Keep | Empty repo exists through separate PM-controlled setup if needed. |
| 2 | OC.3 | `codefusion-repo/project-os-console` | Keep | OC.2 |
| 3 | OC.4 | `codefusion-repo/project-os-console` | Keep | OC.2 |
| 4 | OC.5 | `codefusion-repo/project-os-console` | Keep | OC.4 |
| 5 | OC.6A | `codefusion-repo/project-os-console` | Split from OC.6 | OC.3 |
| 6 | OC.6B | `codefusion-repo/project-os-console` | Split from OC.6 | OC.6A |
| 7 | OC.7 | `codefusion-repo/project-os-console` | Keep | OC.3 and OC.6A |
| 8 | OC.8A | `codefusion-repo/project-os-console` | Split from OC.8 | OC.5, OC.6B, OC.7 |
| 9 | OC.8B | `codefusion-repo/project-os-v2` | Split from OC.8 | OC.8A dogfood evidence |

## First issue to create

Create OC.2 first in `codefusion-repo/project-os-console` after the PM-created
repository exists. Repository creation itself is a separately scoped PM action;
no implementation agent should create the repository under this plan.

### OC.2 - Console foundation and Project OS configuration

Target repository:
`codefusion-repo/project-os-console`

Why this exists:
The console needs a minimal TypeScript web/server foundation before it can
display Project OS state, manage a durable queue, or connect a local runner.
This issue creates only the foundation and Project OS configuration surface.

Objective:
Create a locally runnable responsive dashboard shell, lightweight server/API,
durable job-store foundation, GitHub integration skeleton, and audit-log model
with no runner execution and no GitHub mutation.

Source basis:

- Project OS Operations Console roadmap.
- `docs/OPERATIONS_CATALOG.md`.
- `kernel/manifest.json` and the current kernel files it resolves.
- `templates/commands/PM_COMMAND_BUNDLE.md`.

Scope:

- Scaffold the TypeScript app, responsive dashboard shell, server/API, local
  development scripts, and test setup.
- Add configuration for allowlisted repositories, local workspace mappings,
  GitHub integration settings, and runner connection settings without storing
  secrets in the repo.
- Add a durable queue/store abstraction and audit-log schema or model, but only
  enough for future issues to build on it.
- Add placeholder health and system-status views.
- Document the Project OS boundaries the app must preserve.

Out of scope:

- No runner job pickup, CLI execution, terminal sessions, model APIs, hosted
  runners, GitHub writes, PM action buttons, QA gate implementation, or target
  repository edits.

Consumed Project OS operations/workflows:
Implementation uses `workflow.issue_implementation`. Runtime support is
foundational for catalog operations 1-14, but this issue executes none of them.

Required evidence:
`evidence.issue_scope`, `evidence.branch_preflight`, `evidence.pm_approval`,
`evidence.repo_state`, and `evidence.validation_output`.

Output contracts consumed/displayed:
Prepare storage/display slots for `output.execution_report`,
`output.review_result`, `output.status_result`, `output.route_prompt`,
`output.pm_command_bundle`, `output.closure_comment`, `output.draft_issue`, and
`output.adoption_packet`; do not generate them yet.

PM approval behavior:
The issue approval authorizes only scoped repository edits in
`project-os-console`. It authorizes no target mutations, no GitHub writes by the
console, no runner execution, no secrets transfer, and no deployment.

Acceptance criteria:

- App and server run locally.
- Responsive shell displays health/system status.
- Durable store and audit-log foundations exist.
- Allowlist/config structure exists without committed secrets.
- Project OS boundaries are documented in the console repo.
- No runner execution or GitHub mutation exists.

Validation expectations:

- Run stack-native formatting, linting, type checks, unit tests, and build.
- Include at least one smoke test for the health/system-status route or view.
- Report `git status --short --branch`, current branch, latest commit, diff
  check, and all validation output in the PR.

Risk and rollback:
Risk is medium because this selects the console foundation. Rollback is
reverting the PR and, if the stack decision proves wrong, replacing the
foundation before later issues depend on it.

Dependencies/order:
First implementation issue. Requires only an existing empty or initialized
`codefusion-repo/project-os-console` repository and exact PM approval.

## Compact issue specs

### OC.3 - Read-only GitHub operations dashboard

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Show live read-only Project OS state for allowlisted repositories
  and recommend the next operation without mutating GitHub.
- Scope: GitHub read integration, repo allowlist view, roadmap issue display,
  open issue/PR display, branch or PR-head hints, latest reconstructible
  execution/review/closure evidence, missing-evidence states, and recommended
  next-operation cards.
- Out of scope: No job dispatch, no runner, no GitHub writes, no PM action
  buttons, no target edits, no project truth stored as database authority.
- Consumed operations/workflows: catalog operations 1 and 8;
  `workflow.review_only`; read-only evidence reconstruction for later
  `workflow.pm_intake` and `workflow.review_before_close` previews.
- Required evidence: `evidence.repo_state`, `evidence.source_basis`,
  `evidence.issue_scope` when an issue is selected, and missing-evidence
  reporting through `status.needs_context`.
- Output contracts consumed/displayed: `output.review_result`,
  `output.status_result`, `output.execution_report`, `output.closure_comment`,
  and read-only summaries of `output.route_prompt` and
  `output.pm_command_bundle` when reconstructible from GitHub.
- PM approval behavior: None for read-only display. Any missing or conflicting
  state is shown as missing or conflicting, not guessed.
- Validation expectations: Mock GitHub API tests, dashboard rendering tests,
  no-secret config tests, lint/type/build checks, and read-only integration
  smoke where safe.
- Dependencies/order: After OC.2; feeds OC.6A previews and OC.7 gates.

### OC.4 - Desktop runner outbound bridge

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Connect a local PM desktop runner to the server through outbound
  transport and execute only a harmless diagnostic job.
- Scope: Durable server-side queue, runner registration, heartbeat, WebSocket
  primary transport, polling/reconciliation fallback, log streaming, result
  upload, cancellation, workspace allowlist, command allowlist, and diagnostic
  job UI.
- Out of scope: No Claude CLI, Codex CLI, arbitrary shell, GitHub writes,
  target repo edits, or model API integration.
- Consumed operations/workflows: Enables future terminal execution for catalog
  operations 3-7 and 9; implementation uses `workflow.issue_implementation`;
  diagnostic jobs return `output.status_result`-shaped results.
- Required evidence: `evidence.issue_scope`, `evidence.branch_preflight`,
  `evidence.pm_approval`, `evidence.repo_state`, and
  `evidence.validation_output`.
- Output contracts consumed/displayed: `output.status_result` for diagnostics,
  plus queue/result storage compatible with future `output.execution_report`
  and `output.review_result`.
- PM approval behavior: PM may trigger only the diagnostic job. The runner must
  reject non-allowlisted workspaces and commands.
- Validation expectations: Queue tests, runner reconnect tests, cancellation
  tests, allowlist enforcement tests, log-stream tests, lint/type/build checks,
  and a local loopback diagnostic smoke test.
- Dependencies/order: After OC.2; required before OC.5.

### OC.5 - Local Claude CLI and Codex CLI execution

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Run Claude CLI and Codex CLI locally through controlled terminal
  sessions using PM-local credentials and subscriptions.
- Scope: Provider abstraction for Claude CLI and Codex CLI, prompt-file
  execution, workspace/repo selection, terminal session lifecycle, transcript
  capture, execution-report capture, failure handling, environment isolation,
  and no-token-to-server guarantees.
- Out of scope: No model APIs, hosted runners, arbitrary browser shell, target
  repo mutation without scoped PM approval, or automatic merge/closure.
- Consumed operations/workflows: catalog operations 3, 4, 5, 6, and 9;
  `workflow.issue_implementation`, `workflow.review_before_close`,
  `workflow.review_only`, and `workflow.pm_intake`.
- Required evidence: `evidence.issue_scope`, `evidence.branch_preflight`,
  `evidence.pm_approval`, `evidence.repo_state`, and
  `evidence.validation_output`; the runner must surface missing evidence as
  `status.needs_context` or blocked approval as `status.blocked`.
- Output contracts consumed/displayed: `output.execution_report`,
  `output.review_result`, `output.status_result`, and `output.route_prompt`.
- PM approval behavior: PM-submitted route prompt or command bundle is approval
  evidence only for the exact scope. The UI must force re-approval if target,
  actor, write type, risk, or scope changes materially.
- Validation expectations: Provider adapter tests with fake CLIs, transcript
  capture tests, workspace/env isolation tests, failure-mode tests,
  lint/type/build checks, and a local dry-run smoke with mocked CLI commands.
- Dependencies/order: After OC.4; required before OC.8A dogfood.

### OC.6A - PM preview engine and copy-safe bundles

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Generate PM-readable previews for route prompts, draft issues,
  review requests, correction prompts, closure comments, adoption packets, and
  copy-safe command bundles without executing writes.
- Scope: Preview generation for catalog operations 2, 3, 4, 5, 7, 9, 10, and
  11; template-backed rendering; operation-specific evidence checks; missing
  evidence explanations; supported `gh --json` field handling; and preview
  history in the audit log.
- Out of scope: No GitHub mutation, no runner execution, no merge/close buttons,
  no labels/releases/settings/deployments, and no target repo edits.
- Consumed operations/workflows: `workflow.pm_intake`,
  `workflow.review_before_close`, `workflow.release_readiness`, and
  `workflow.target_adoption` as preview sources.
- Required evidence: `evidence.source_basis`, `evidence.issue_scope`,
  `evidence.pr_diff`, `evidence.review_evidence`,
  `evidence.closure_evidence`, `evidence.repo_state`, and
  `evidence.target_adoption` as required by each selected operation.
- Output contracts consumed/displayed: `output.draft_issue`,
  `output.route_prompt`, `output.pm_command_bundle`,
  `output.closure_comment`, `output.review_result`, `output.status_result`,
  and `output.adoption_packet`.
- PM approval behavior: Previews are shape only. Copying, sending, or executing
  a preview is a separate PM action; preview generation grants no write
  permission.
- Validation expectations: Snapshot tests for generated previews, command-bundle
  safety tests, unsupported `gh --json` field regression tests, missing-evidence
  tests, lint/type/build checks, and no nested-fence rendering checks.
- Dependencies/order: After OC.3; should land before OC.6B.

### OC.6B - Gated GitHub actions and closeout verification

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Turn approved previews into explicit PM action buttons for the
  common closeout loop: comment, mark ready, merge, close, cleanup, and verify.
- Scope: Per-action preflight, explicit PM confirmation, audit entries,
  PR comment, issue comment, mark-ready, merge with reviewed head SHA, close
  issue when separately approved, safe local/remote branch cleanup, and
  read-only post-action verification.
- Out of scope: No automatic action chaining without PM confirmation, no labels,
  releases, settings, deployments, arbitrary `gh` commands, or bypass of
  review-before-close.
- Consumed operations/workflows: catalog operations 7 and 8;
  `workflow.release_readiness`, `workflow.pm_intake`, and
  `workflow.review_only`.
- Required evidence: `evidence.review_evidence`,
  `evidence.closure_evidence`, `evidence.repo_state`,
  `evidence.validation_output`, and exact PM approval for each write-capable
  action.
- Output contracts consumed/displayed: `output.pm_command_bundle`,
  `output.closure_comment`, `output.review_result`, and
  `output.status_result`.
- PM approval behavior: Each write action requires an explicit PM click and
  confirmation. Merge requires `--match-head-commit` semantics or equivalent
  API guard. Closure, labels, releases, settings, and automation remain separate
  approvals.
- Validation expectations: Mock GitHub mutation tests, head-SHA guard tests,
  idempotent verification tests, permission-boundary tests, audit-log tests,
  lint/type/build checks, and a no-real-mutation dry run in CI.
- Dependencies/order: After OC.6A; should land after review-before-close
  previews are reliable.

### OC.7 - Human QA, asset, and security gates

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Make human QA, asset requests, and security review visible,
  actionable gates without adding new Project OS actors or workflows.
- Scope: QA checklist cards, UI/mobile/manual smoke checklist support,
  Unity/gameplay checklist support, asset request packets, security review
  packets, pass/fail gate evidence, blocker display, and follow-up issue
  preview generation.
- Out of scope: No target repo asset commits, no dedicated new kernel actors,
  no new output contracts, no automatic merge block override, and no external
  asset-service automation.
- Consumed operations/workflows: catalog operations 12, 13, 14, and 11;
  `workflow.review_before_close` and `workflow.pm_intake`.
- Required evidence: `evidence.issue_scope`, `evidence.pr_diff`,
  `evidence.review_evidence`, and `evidence.source_basis`.
- Output contracts consumed/displayed: QA and security use
  `output.review_result`; asset and follow-up requests use
  `output.draft_issue`; blocker states use `output.status_result`.
- PM approval behavior: QA/security verdicts are gate evidence, not write
  authorization. Asset delivery and target repo writes require their own scoped
  target approval.
- Validation expectations: Gate-state tests, checklist rendering tests,
  follow-up issue preview tests, security/privacy redaction tests,
  lint/type/build checks, and manual responsive UI smoke.
- Dependencies/order: After OC.3 and OC.6A; before OC.8A dogfood.

### OC.8A - Dogfood console loops and evidence capture

- Target repository: `codefusion-repo/project-os-console`.
- Objective: Use the console on real Project OS work and capture enough
  evidence to decide whether to standardize, iterate, or kill the console loop.
- Scope: Dogfood against `project-os-v2` and PM-selected target repositories,
  at least one execution-report loop, one review-before-close loop, one
  PM action preview or button flow, one QA/asset/security gate, cost/friction
  notes, missing-evidence cases, and security observations.
- Out of scope: No target repo edits except through separately scoped target
  issues, no merge/closure without PM action, no roadmap decision recorded in
  the console database, and no standardization decision inside this repo.
- Consumed operations/workflows: catalog operations 1-14 as applicable;
  `workflow.issue_implementation`, `workflow.review_before_close`,
  `workflow.review_only`, `workflow.pm_intake`, and
  `workflow.release_readiness`.
- Required evidence: Live GitHub evidence for every dogfood loop, plus
  `evidence.validation_output`, `evidence.review_evidence`, and
  `evidence.closure_evidence` when those flows are exercised.
- Output contracts consumed/displayed: `output.execution_report`,
  `output.review_result`, `output.status_result`, `output.closure_comment`,
  `output.pm_command_bundle`, `output.route_prompt`, and `output.draft_issue`.
- PM approval behavior: PM chooses dogfood target repositories and approves each
  write-capable action in that target's own scope. If target selection is not
  named at execution time, return `status.needs_pm_decision`.
- Validation expectations: End-to-end dogfood notes in the PR, regression tests
  for any defects found, normal stack validation, and manual responsive UI
  smoke on desktop and mobile viewport sizes.
- Dependencies/order: After OC.5, OC.6B, and OC.7.

### OC.8B - Standardization, iteration, or kill decision

- Target repository: `codefusion-repo/project-os-v2`.
- Objective: Record the Project OS decision after dogfood: standardize the
  console loop, iterate with scoped follow-ups, or kill/re-scope the roadmap.
- Scope: Review dogfood evidence from GitHub, compare against roadmap kill
  criteria, identify security/QA misses, decide whether local runner execution
  reduced PM work, and draft follow-up issues or an ADR if the decision must
  outlive the issue.
- Out of scope: No console implementation, no target repo edits, no merge or
  issue closure by the implementation agent, no labels/releases/settings, and
  no durable storage of live dogfood state in repo docs.
- Consumed operations/workflows: catalog operations 1, 8, and 11;
  `workflow.review_only`, `workflow.pm_intake`, and
  `workflow.release_readiness`.
- Required evidence: `evidence.repo_state`, `evidence.review_evidence`,
  `evidence.validation_output`, `evidence.closure_evidence`, and the live
  dogfood issues/PRs selected by the PM.
- Output contracts consumed/displayed: `output.review_result`,
  `output.draft_issue`, `output.pm_command_bundle`, and `output.status_result`;
  use `templates/adr.md` only if a durable decision record is separately scoped.
- PM approval behavior: The PM owns the standardize/iterate/kill decision.
  Missing target selection, unclear risk acceptance, or competing evidence
  returns `status.needs_pm_decision`.
- Validation expectations: `python -m tools.validate_kernel`, `pytest -q`,
  `git diff --check`, and any doc checks required by the scoped change.
- Dependencies/order: Final issue after OC.8A dogfood evidence exists.

## Repository placement

- `codefusion-repo/project-os-console`: OC.2, OC.3, OC.4, OC.5, OC.6A,
  OC.6B, OC.7, and OC.8A.
- `codefusion-repo/project-os-v2`: OC.8B synthesis decision, and any future
  kernel/template/catalog change that dogfood evidence proves necessary.
- Target repositories: no console implementation issues. Dogfood target work
  uses normal target Project OS issues with separate PM approval.
