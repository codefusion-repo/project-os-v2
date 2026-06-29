# Kernel Production-Readiness Audit

This is a read-only audit artifact. It inventories the current Project OS kernel
and connected operation surface, classifies recommendations for later PM
approval, and applies none of those recommendations.

## Production-Ready Definition

Project OS is production-ready when the kernel remains compact, every object has
one clear responsibility, routing is deterministic for each surface, permission
and output shape are never confused, live state is kept out of durable files, PM
operations are usable without inventing state, and the operation catalog is broad
enough to support future Browser Companion packaging without forking kernel
behavior.

## Audit Scope

Reviewed surfaces:

- `kernel/manifest.json`
- `kernel/statuses.json`
- `kernel/actors.json`
- `kernel/execution_modes.json`
- `kernel/boundaries.json`
- `kernel/evidence.json`
- `kernel/workflows.json`
- `kernel/outputs.json`
- `templates/operations/`
- `templates/artifacts.md`
- `templates/route-prompt.md`
- `templates/pm-command-bundle.md`
- `docs/DESIGN.md`
- `docs/TRACEABILITY_PROTOCOL.md`
- `docs/PM_OPERATIONS.md`
- `docs/GETTING_STARTED.md`
- `docs/PUBLIC_USAGE_MODEL.md`
- `docs/PM_VARIABLES.md`
- `docs/GITHUB_ACCESS.md`
- `README.md`
- `tools/validate_kernel.py`
- `tools/project_os_resolve.py`
- `tools/measure_resolution.py`
- `tools/audit_target_adapters.py`
- `tools/audit_traceability.py`
- `tests/`

## Kernel Inventory

Disposition values in this section use only `keep`, `merge`, `split`, `rename`,
`remove`, `add`, or `defer`.

### Manifest Objects

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.manifest` | Single resolution entrypoint for Project OS behavior. | All agents and docs. | Surface, workflow, mode, live evidence needs. | Resolution sequence, load order, strategy, source-of-truth map, size budget, non-authorization rule. | All kernel families. | Kernel-level. | keep |
| `manifest.load_order` | Declares deterministic family load order. | Resolver, validator, manual readers. | Kernel family filenames. | Ordered kernel read set. | All declared JSON families. | Kernel-level. | keep |
| `manifest.resolution_strategy` | Defines surface-aware routing, terminal fast path, browser manual path, fallback, and non-authorization. | Adapters, route prompts, resolver users, browser chat. | Actor surface and kernel availability. | Routing rule for how to resolve behavior. | `actor.terminal_agent`, `actor.browser_chat`, `actor.unknown`, `boundary.output_not_permission`. | Kernel-level. | keep |
| `manifest.resolution_sequence` | Canonical ordered resolution steps. | Manual readers and resolver parity tests. | Actor, mode, workflow, evidence, output selection. | One status from `kernel.statuses`. | Statuses, actors, boundaries, modes, evidence, workflows, outputs. | Kernel-level. | keep |
| `manifest.source_of_truth` | Separates stable behavior, live state, traceability, and adapters. | Agents and docs. | Repository layout. | Source-of-truth ownership map. | `docs/TRACEABILITY_PROTOCOL.md`, adapters, templates. | Kernel-level. | keep |
| `manifest.size_budget` | Keeps the kernel cheap to read. | Validator and PM review of kernel growth. | Total bytes of kernel files. | Hard and target byte budgets. | `tools/validate_kernel.py`. | Kernel-level. | keep |
| `manifest.non_authorization` | States that kernel resolution grants no authority. | All agents. | Resolved behavior and PM approval gates. | Non-permission guardrail. | `boundary.output_not_permission`. | Kernel-level. | keep |

### Actors

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.actors` | Defines execution surfaces and surface-based capability. | Manifest, resolver, adapters. | Execution surface. | Actor entries and actor-model note. | Boundaries and execution modes. | Kernel-level. | keep |
| `actor.human_pm` | Human decision owner for scope and privileged actions. | Agents reporting decisions or requesting approval. | Explicit PM decisions. | Approval or decision evidence. | `boundary.security_privacy`, `boundary.no_live_state_durable`. | Kernel-level. | keep |
| `actor.terminal_agent` | Repository-capable agent surface. | Terminal agents and route prompts. | Local checkout, live issue scope, PM approval, branch state, validation output. | Scoped edits, validation, commit, push, draft PR when mode permits. | Work-capable modes and write boundaries. | Kernel-level. | keep |
| `actor.browser_chat` | Draft-only browser surface. | Browser-chat adapter and operation prompts. | Provided context and live read access. | Draft issues, route prompts, reports, command bundles. | `mode.review_only`, draft-only and copy-safe boundaries. | Kernel-level. | keep |
| `actor.unknown` | Fail-closed surface for ambiguous execution context. | Manifest and resolver. | Unknown or untrusted surface. | No write-capable output. | `boundary.fail_closed`. | Kernel-level. | keep |

### Execution Modes

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.execution_modes` | Defines how far a terminal task may proceed. | Resolver, route prompts, PM approvals. | PM-scoped mode. | Allowed/prohibited action envelope and evidence requirements. | Actors, boundaries, evidence. | Kernel-level. | keep |
| `mode.review_only` | Read, analyze, report; no writes. | Browser chat and terminal review tasks. | Live issue or repo evidence. | Reports, drafts, status. | `evidence.issue_scope` when scoped. | Kernel-level. | keep |
| `mode.local_implementation` | Scoped local edits and validation without commit/push/PR. | Terminal agent. | Issue scope, branch preflight, PM approval. | Local modified worktree and report. | Branch and approval evidence. | Kernel-level. | keep |
| `mode.delegated_commit_push` | Scoped edits, validation, commit, and push. | Terminal agent. | Issue scope, branch preflight, PM approval, validation output. | Pushed work branch and report. | Write boundaries and validation evidence. | Kernel-level. | keep |
| `mode.delegated_commit_pr` | Scoped edits, validation, commit, push, and draft PR. | Terminal agent. | Issue scope, branch preflight, PM approval, validation output. | Draft PR and execution report. | Write boundaries and validation evidence. | Kernel-level. | keep |

### Statuses

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.statuses` | Defines exactly one returned resolution status. | All agents, resolver, validator. | Resolution gates and evidence state. | Four canonical statuses and precedence. | Boundaries and evidence. | Kernel-level. | keep |
| `status.resolved` | Safe to proceed within selected workflow/mode/output shape. | All workflows. | All required gates satisfied. | Proceed signal without extra permission. | `boundary.output_not_permission`. | Kernel-level. | keep |
| `status.needs_context` | Obtainable evidence is missing. | Agents that can ask for or read evidence. | Missing issue, repo, branch, kernel, or validation context. | Context request. | Evidence missing-status fields. | Kernel-level. | keep |
| `status.needs_pm_decision` | PM judgment is required. | Agents encountering scope, priority, evidence, or risk decisions. | Material decision gap or conflict. | Decision request. | Human PM authority. | Kernel-level. | keep |
| `status.blocked` | Boundary, safety, approval, or validation gate prevents action. | All agents. | Boundary violation or missing blocking approval. | Stop result. | Boundaries and evidence. | Kernel-level. | keep |

### Boundaries

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.boundaries` | Holds hard rules inherited through resolution. | All agents and resolver output. | Actor, mode, workflow, evidence state. | Blocking or decision gates. | Statuses, actors, workflows. | Kernel-level. | keep |
| `boundary.branch_preflight` | Requires branch/worktree/HEAD evidence before local writes, commit, push, or PR. | Terminal agents. | Git branch, status, HEAD. | Safe branch gate or blocked status. | `evidence.branch_preflight`. | Kernel-level. | keep |
| `boundary.no_main_edits` | Prevents edits directly on the default branch. | Terminal agents. | Current branch and dirty state. | Blocked recovery state if unsafe. | Branch preflight. | Kernel-level. | keep |
| `boundary.draft_only_browser` | Prevents browser chat from mutating files, git, or GitHub. | Browser chat. | Surface resolution. | Draft-only behavior. | `actor.browser_chat`. | Kernel-level. | keep |
| `boundary.separate_pm_approval` | Requires exact approval for privileged actions and target artifacts. | All write-capable flows. | PM approval evidence. | Stop or proceed within exact scope. | `evidence.pm_approval`. | Kernel-level. | keep |
| `boundary.review_before_close` | Requires code-backed review before closure evidence is drafted. | Review-before-close workflow. | Linked issue, PR diff, final files, validation. | Review gate. | `workflow.review_before_close`, `evidence.pr_diff`. | Kernel-level. | keep |
| `boundary.no_live_state_durable` | Forbids durable files from storing live project state. | All docs, adapters, templates, kernel changes. | Proposed durable content. | Block on live-state leakage. | Traceability protocol. | Kernel-level. | keep |
| `boundary.no_invented_state` | Forbids invented git, GitHub, validation, review, or approval state. | All agents. | Live evidence availability. | Needs-context or blocked result. | Evidence system. | Kernel-level. | keep |
| `boundary.security_privacy` | Forbids exposing secrets or sensitive values. | All agents and outputs. | File/output/log content. | Redaction or blocked result. | Security notes and review prompts. | Kernel-level. | keep |
| `boundary.fail_closed` | Stops on ambiguity, missing evidence, source conflicts, failed validation, or missing approval. | All agents. | Gate and evidence state. | Non-resolved status. | Status precedence. | Kernel-level. | keep |
| `boundary.output_not_permission` | Keeps output contracts, prompts, and resolver output from granting authority. | All agents and templates. | Output or route shape. | Non-authorization rule. | Manifest and outputs. | Kernel-level. | keep |
| `boundary.implementation_discipline` | Requires complete scoped implementation without unrelated rewrites or under-implementation. | Terminal agents and reviewers. | Issue scope, implementation evidence. | Write/review discipline gate. | Issue implementation and review workflows. | Kernel-level. | keep |
| `boundary.primary_path_discipline` | Prevents fallback paths that hide or bypass root-cause fixes. | Terminal agents and reviewers. | Implementation path and error handling evidence. | Primary-path gate. | Issue implementation, review, discipline audit. | Kernel-level. | keep |
| `boundary.validation_discipline` | Requires proportional validation and honest manual-validation reporting. | Terminal agents and reviewers. | Changed behavior and validation evidence. | Validation gate. | Execution report and review outputs. | Kernel-level. | keep |
| `boundary.code_clarity` | Keeps comments/docstrings focused on non-obvious intent and tradeoffs. | Terminal agents editing code. | Proposed code changes. | Clarity gate. | Implementation workflows. | Kernel-level. | keep |
| `boundary.copy_safe_commands` | Defines the hard floor for PM-facing command bundles. | Browser chat and PM command-bundle output. | Draft command bundle. | Copy-safety gate. | `templates/pm-command-bundle.md`. | Kernel-level with detail in template. | keep |

### Evidence

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.evidence` | Defines evidence requirements and missing statuses. | Workflows, modes, resolver, agents. | Live GitHub, git, and command output. | Evidence gates. | Statuses and workflows. | Kernel-level. | keep |
| `evidence.issue_scope` | Live issue/PR scope, objective, and acceptance basis. | Issue implementation and review. | Current GitHub issue or PR. | Scope gate. | Traceability protocol. | Kernel-level. | keep |
| `evidence.source_basis` | Prior decisions, issues, PRs, ADRs, or PM context a task builds on. | PM intake, asset/security prompts. | Live source basis. | Source-context gate. | Traceability protocol. | Kernel-level. | keep |
| `evidence.branch_preflight` | Current branch, worktree, and HEAD before local writes. | Terminal implementation modes. | Git commands. | Branch-safety gate. | Branch boundaries. | Kernel-level. | keep |
| `evidence.repo_state` | Live file, branch, diff, or history context. | Review-only, audits, release readiness, handoff. | Git and GitHub reads. | Repository-context gate. | Traceability protocol. | Kernel-level. | keep |
| `evidence.pm_approval` | Exact PM approval for scoped writes or command bundles. | Write-capable modes. | Current PM decision or issue/PR-recorded decision. | Approval gate. | Execution modes approval note. | Kernel-level. | keep |
| `evidence.validation_output` | Real validation commands and results. | Implementation, review, release readiness. | Test/lint/check output. | Done/readiness gate. | Validation discipline. | Kernel-level. | keep |
| `evidence.pr_diff` | Changed files, diff, and final head files when needed. | Review-before-close. | PR diff and file content. | Code-backed review gate. | Review-before-close boundary. | Kernel-level. | keep |
| `evidence.review_evidence` | Review findings or verdict recorded on PR/issue. | No current kernel workflow requires it directly. | Review records. | Potential review-state gate. | Traceability tooling concept. | Move into workflow/tool docs unless wired. | merge |
| `evidence.closure_evidence` | Closure packet evidence for completed work. | No current kernel workflow requires it directly. | Closure comments. | Potential closure gate. | Traceability tooling concept. | Move into traceability docs/tool docs unless wired. | merge |
| `evidence.target_adoption` | Target adapter/adoption evidence. | Target adoption workflow. | Target adapters, metadata, roadmap anchor, notes, validation commands, audit findings. | Adoption gate. | Adoption packet output and adapter auditor. | Kernel-level. | keep |

### Workflows

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.workflows` | Defines reusable workflow profiles. | Resolver, route prompts, operations. | Requested task type. | Required evidence and allowed outputs. | Evidence and output families. | Kernel-level. | keep |
| `workflow.review_only` | Analysis, audits, design review, questions, and findings. | Browser chat and terminal reviewers. | `evidence.repo_state`. | `output.review_result`, `output.status_result`. | Review/status outputs. | Kernel-level. | keep |
| `workflow.issue_implementation` | Scoped GitHub issue implementation. | Terminal agents. | Issue scope, branch preflight, PM approval, validation output. | Execution report or status. | Implementation, primary-path, validation boundaries. | Kernel-level. | keep |
| `workflow.review_before_close` | Code-backed review before PM merge or closure. | Browser chat or terminal reviewers. | Issue scope, PR diff, validation output. | Review result, closure comment, PM command bundle, status. | Review-before-close boundary. | Kernel-level. | keep |
| `workflow.implementation_discipline_audit` | Read-only implementation-quality audit. | Browser chat or terminal reviewers. | Repo state, optional issue/PR/path evidence from operation. | Review result, status, draft issue. | Implementation, primary-path, validation boundaries. | Kernel-level. | keep |
| `workflow.pm_intake` | Turns PM input into draft issues, route prompts, or decision requests. | Browser chat. | Source basis. | Draft issue, route prompt, PM command bundle, status. | Templates and PM variables. | Kernel-level. | keep |
| `workflow.design_asset` | Drafts prompt for an external design recipient. | Browser chat. | Repo state and source basis. | Asset prompt or status. | Asset output and recipient-not-actor rule. | Kernel-level for now. | keep |
| `workflow.security_revision` | Drafts OWASP-based prompt for an external security recipient. | Browser chat. | Repo state and source basis. | Security review prompt or status. | Security output and secret-redaction rules. | Kernel-level but naming is inconsistent. | rename |
| `workflow.release_readiness` | Assesses readiness for tag or release and drafts PM bundles when scoped. | Browser chat. | Repo state and validation output. | Review result, PM command bundle, status. | Release/tag operation templates. | Kernel-level. | keep |
| `workflow.handoff` | Transfers work between sessions without durable state drift. | Browser chat. | Repo state. | Handoff packet or status. | Traceability protocol. | Kernel-level. | keep |
| `workflow.target_adoption` | Audits or bootstraps target repository adoption. | Browser chat and terminal agents. | Target adoption evidence. | Adoption packet, execution report, status. | Adapter templates and adapter auditor. | Kernel-level. | keep |

### Outputs

| Object | Function | Consumer | Inputs or evidence | Outputs | Dependencies | Placement | Disposition |
|---|---|---|---|---|---|---|---|
| `kernel.outputs` | Defines output contracts and reminds that shape grants no permission. | All workflows. | Selected workflow and evidence. | Required sections and rules. | Boundaries and templates. | Kernel-level. | keep |
| `output.execution_report` | Reports implementation work and validation. | Terminal agents. | Scope, files changed, validation, risks, commit/PR refs when applicable. | Execution report. | Issue implementation workflow. | Kernel-level. | keep |
| `output.review_result` | Reports review or analysis findings. | Review-only, review-before-close, audits. | Scope, evidence, comparison, findings, risks. | Review result. | Review workflows. | Kernel-level. | keep |
| `output.closure_comment` | Defines issue closure reconstruction packet. | Review-before-close. | Completion, validation, exceptions, boundaries, references. | Closure comment draft. | `templates/artifacts.md`. | Kernel-level shape with template detail. | keep |
| `output.draft_issue` | Defines draft issue shape. | PM intake and discipline audits. | Source basis, scope, acceptance, validation, risk. | Draft issue. | `templates/artifacts.md`. | Kernel-level shape with template detail. | keep |
| `output.route_prompt` | Defines route prompt shape. | PM intake and browser chat. | Scope variables, evidence requirements, validation commands. | Route prompt. | `templates/route-prompt.md`. | Kernel-level shape with template detail. | keep |
| `output.pm_command_bundle` | Defines PM command-bundle shape. | PM intake, review closeout, release readiness. | Live exact targets and command intent. | Copy-safe command bundle. | `templates/pm-command-bundle.md`, copy-safe boundary. | Kernel-level shape with template detail. | keep |
| `output.asset_prompt` | Defines external design-recipient prompt shape. | Design asset workflow. | Source context, asset objective, dimensions, constraints. | Asset prompt. | Recipient-not-actor model. | Kernel-level while workflow exists. | keep |
| `output.security_review_prompt` | Defines external OWASP review-recipient prompt shape. | Security revision workflow. | Security surfaces, OWASP areas, redaction rules. | Security review prompt. | Security/privacy boundary. | Kernel-level while workflow exists. | keep |
| `output.handoff_packet` | Defines session-transfer packet shape. | Handoff workflow. | Current live links, verified vs assumed, next steps, decisions, boundaries. | Handoff packet. | Traceability protocol. | Kernel-level, never durable state. | keep |
| `output.adoption_packet` | Defines target adoption packet shape. | Target adoption workflow. | Target repo, adoption state, adapter diff/draft, checklist, target-owned notes. | Adoption packet. | Adapter templates and target adoption evidence. | Kernel-level. | keep |
| `output.status_result` | Defines non-resolved status report shape. | All workflows. | Missing/conflicting/blocking evidence. | Status result. | Statuses and fail-closed boundary. | Kernel-level. | keep |

## Operation Surface Inventory

| Operation | Function | Kernel mapping | Finding | Disposition |
|---|---|---|---|---|
| `templates/operations/00-browser-chat-activation.md` | Establishes draft-only browser-chat context. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Correctly routes writes to route prompts or PM bundles. | keep |
| `templates/operations/01-adopt-project-os-in-existing-target.md` | Drafts/adopts target adapters. | `workflow.target_adoption`, `mode.delegated_commit_pr`, `output.adoption_packet`. | Correct adapter-only boundary. | keep |
| `templates/operations/02-bootstrap-new-project.md` | Drafts initial adoption for new target repo. | `workflow.target_adoption`, `mode.review_only`, `output.adoption_packet`. | Correctly stays draft-only. | keep |
| `templates/operations/03-verify-target-adoption.md` | Audits target adoption read-only. | `workflow.target_adoption`, `mode.review_only`, `output.status_result`. | Correctly separates verify from upgrade. | keep |
| `templates/operations/04-draft-create-issue-command-from-description.md` | Converts PM description into issue-create bundle. | `workflow.pm_intake`, `mode.review_only`, `output.pm_command_bundle`. | Covers description-to-issue, not docs-from-description. | keep |
| `templates/operations/05-review-project-state-and-misalignment.md` | Finds roadmap/issues/code misalignment. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Useful PM diagnostic. | keep |
| `templates/operations/06-draft-create-next-issue-command-from-traceability.md` | Drafts one next issue from live traceability. | `workflow.pm_intake`, `mode.review_only`, `output.pm_command_bundle`. | Too narrow for bounded roadmap-to-issues batches. | split |
| `templates/operations/07-draft-issue-implementation-route-prompt.md` | Drafts implementation route prompt. | `workflow.pm_intake`, `mode.review_only`, `output.route_prompt`. | Correctly issue-referential. | keep |
| `templates/operations/08-draft-review-correction-route-prompt.md` | Drafts correction route prompt from feedback. | `workflow.pm_intake`, `mode.review_only`, `output.route_prompt`. | Correct same-branch/same-scope constraint. | keep |
| `templates/operations/09-review-pr-before-close-and-draft-package.md` | Reviews PR and drafts closeout package if resolved. | `workflow.review_before_close`, `mode.review_only`, `output.review_result` plus PM bundle. | Correct code-backed review gate. | keep |
| `templates/operations/10-draft-pr-closeout-and-cleanup-command.md` | Drafts closeout/cleanup bundle from live state. | `workflow.review_before_close`, `mode.review_only`, `output.pm_command_bundle`. | Correctly says bundle does not replace review. | keep |
| `templates/operations/11-verify-post-merge-state.md` | Verifies default branch and issue state after merge. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Read-only sanity check. | keep |
| `templates/operations/12-analyze-release-or-tag-readiness.md` | Assesses release/tag readiness. | `workflow.release_readiness`, `mode.review_only`, `output.status_result`. | Correctly stops before tag/release. | keep |
| `templates/operations/13-draft-create-release-tag-command.md` | Drafts tag command bundle. | `workflow.release_readiness`, `mode.review_only`, `output.pm_command_bundle`. | Separate PM authority preserved. | keep |
| `templates/operations/14-audit-target-adapters.md` | Audits adapter drift read-only. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Tool-backed target diagnostic. | keep |
| `templates/operations/15-audit-issue-pr-traceability.md` | Audits issue/PR traceability read-only. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Tool-backed traceability diagnostic. | keep |
| `templates/operations/16-review-idea-as-system-feature.md` | Reviews an idea as a system feature. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Covers idea review; debate variant can reuse this first. | keep |
| `templates/operations/17-draft-handoff-package-for-new-session.md` | Drafts handoff packet. | `workflow.handoff`, `mode.review_only`, `output.handoff_packet`. | Correctly says never store packet durably. | keep |
| `templates/operations/18-draft-human-qa-checklist.md` | Drafts external QA checklist. | `workflow.review_only`, `mode.review_only`, `output.status_result`. | Recipient-not-actor model preserved. | keep |
| `templates/operations/19-request-external-design-assets.md` | Drafts design asset prompt. | `workflow.design_asset`, `mode.review_only`, `output.asset_prompt`. | Specialized workflow/output are usable but may be kernel-heavy. | defer |
| `templates/operations/20-request-owasp-security-review.md` | Drafts OWASP security review prompt. | `workflow.security_revision`, `mode.review_only`, `output.security_review_prompt`. | Strong redaction posture; workflow id naming should be revisited. | rename |
| `templates/operations/21-draft-create-follow-up-from-review-command.md` | Drafts follow-up issue from review finding. | `workflow.pm_intake`, `mode.review_only`, `output.pm_command_bundle`. | Correctly separates deferred from blocking findings. | keep |
| `templates/operations/22-record-adr-decision.md` | Drafts ADR and optional route prompt to write file. | `workflow.pm_intake`, `mode.review_only`, `output.route_prompt`. | Correct route for durable decision docs. | keep |
| `templates/operations/23-upgrade-kernel-adoption-in-target.md` | Drafts target adapter upgrade. | `workflow.target_adoption`, `mode.delegated_commit_pr`, `output.adoption_packet`. | Correct adapter-only update path. | keep |
| `templates/operations/24-draft-create-github-release-command.md` | Drafts GitHub Release command bundle. | `workflow.release_readiness`, `mode.review_only`, `output.pm_command_bundle`. | Distinct from tag-only operation. | keep |
| `templates/operations/25-audit-implementation-discipline-gaps.md` | Audits implementation-discipline gaps. | `workflow.implementation_discipline_audit`, `mode.review_only`, `output.review_result`. | Correctly anchors findings to kernel boundary, not style manifestos. | keep |

## Connected Surface Findings

| Surface | Finding | Recommendation | Category | Follow-up issue? |
|---|---|---|---|---|
| Kernel manifest | The manifest cleanly owns routing, load order, fallback, and non-authorization. | Preserve it as the only entrypoint; do not reintroduce competing adapter resolution orders. | keep | no |
| Actor model | The four actors are execution surfaces, not roles. Tests guard role-actor drift. | Keep the surface-only model. Route QA, security, and design to recipient/workflow/output concepts. | keep | no |
| Execution modes | Modes are kernel-critical and appear in manifest load order. | Keep modes in every future kernel audit checklist even when an issue summary lists only actors/statuses/boundaries/evidence/workflows/outputs. | keep | no |
| Evidence | `evidence.review_evidence` and `evidence.closure_evidence` are unreferenced by current kernel workflows. | Merge these concepts into `evidence.repo_state`, `evidence.validation_output`, traceability docs, or wire them to a workflow before keeping them as kernel objects. | merge | yes |
| Workflow naming | `workflow.security_revision` is less clear than the output and operation names, which describe a security review prompt. | Rename to a security-review-oriented id only with compatibility handling and PM approval. | rename | yes |
| Command-bundle docs | `templates/pm-command-bundle.md` says only PM intake and release readiness emit command bundles, but review-before-close also emits them. | Remove or replace that stale sentence and add a small catalog-to-template alignment check. | remove | yes |
| Operation coverage | Current operations cover idea review, description-to-issue, and single-next-issue from traceability. | Add missing operation templates for conversation-to-docs, docs-to-roadmap, and docs-from-description. | add | yes |
| Roadmap-to-issues | Operation `06` intentionally drafts exactly one next issue. | Split the use case into single-next-issue and bounded roadmap-to-issues with an explicit count or scope limit. | split | yes |
| Design asset routing | `workflow.design_asset` is specialized and currently useful, but it may be more kernel than needed if more recipient-prompt workflows appear. | Defer merging into a generic recipient-prompt or PM-intake pattern until there is repeated evidence. | defer | no |
| Test surface | Tests protect important invariants but many assertions depend on exact prose fragments. | Split semantic invariants from phrase-level regression checks so docs can be compacted without weakening behavior. | split | yes |
| Validator scope | `tools.validate_kernel` correctly validates only kernel JSON. Operation/catalog alignment is guarded mostly by tests. | Keep the validator narrow; add operation validation only after repeated drift or as a separate read-only diagnostic. | defer | no |
| Browser Companion packaging | Measurement tooling projects a future stable context but creates no package. | Defer packaging until operation gaps are approved and resolved; do not fork kernel behavior. | defer | no |
| Runtime/API/service ideas | No audited gap requires a runtime, service, daemon, API server, GitHub App, OAuth integration, or automation. | Keep Project OS as read/resolve/draft/execute-via-agent behavior, not a service. | keep | no |

## Candidate Use Cases

| Candidate | Current coverage | Recommended shape | New kernel object? | Category | Follow-up issue? |
|---|---|---|---|---|---|
| Idea debate / idea review | `templates/operations/16-review-idea-as-system-feature.md` handles idea review. | Keep as an operation using `workflow.review_only` and `output.status_result`; add a debate variant only as operation wording if PM wants a two-sided format. | No. | keep | no |
| Conversation-to-docs | No first-class operation. | Add operation template that turns PM-provided conversation context into a draft doc or route prompt for terminal file creation under exact approval. | No; reuse `workflow.pm_intake`, `output.route_prompt`, and `output.draft_issue` where appropriate. | add | yes |
| Docs-to-roadmap | No first-class operation. | Add operation template that reads stable docs and drafts a roadmap issue body or update command bundle for PM execution. | No; reuse `workflow.pm_intake` and `output.pm_command_bundle`. | add | yes |
| Roadmap-to-issues with count/scope limit | Operation `06` creates exactly one next issue. | Split or add a bounded batch operation with `ISSUE_COUNT_LIMIT` or `SCOPE_LIMIT`, still one outcome per issue. | No; reuse `workflow.pm_intake` and `output.pm_command_bundle`. | split | yes |
| Docs-from-description | Description-to-issue exists; ADR-from-decision exists. | Add operation template that drafts docs content from a PM description and routes terminal file creation only after exact approval. | No; reuse `workflow.pm_intake` and `output.route_prompt`. | add | yes |
| External recipient prompts beyond design/security | Design and security have specialized workflows/outputs. | Defer a generic recipient-prompt abstraction until a third repeated recipient type proves duplication. | Not now. | defer | no |

## Readiness Assessment

The kernel is close to production-ready for terminal-agent and browser-chat
operation. Its strongest properties are the single manifest entrypoint, the
surface-only actor model, explicit non-authorization, strict live-state
boundaries, and a compact validator/resolver/tool split.

The main production-readiness gaps are not architectural. They are operation
coverage and drift-control issues:

- Some PM transformation use cases should become operation templates before any
  packaging work.
- A few kernel objects or names should be reconciled before they become
  compatibility commitments.
- The command-bundle documentation has one stale ownership claim.
- The tests should continue guarding behavior, but some phrase coupling should be
  split from semantic invariants.

No recommendation in this report should be applied without a separate scoped PM
implementation issue and approval.
