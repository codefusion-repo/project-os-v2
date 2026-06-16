# PM Operations Catalog

Recurring PM/chat/agent operations expressed **over existing Project OS
semantics**. This catalog is the OC.0 deliverable that feeds the OC.1
implementation plan and the future Operations Console (`project-os-v2#274`).

It is not new kernel behavior. Every operation maps to existing
`kernel/workflows.json` workflows, `kernel/outputs.json` output contracts,
`kernel/actors.json` actors, and `kernel/evidence.json` evidence. The console
must consume these; it must not invent panel-specific workflows, actors, or
safety rules.

This file stores no live state. Issue/PR/branch/validation state is read live
from GitHub and git per `docs/TRACEABILITY_PROTOCOL.md`.

## Actor-model resolution (OC.0 decision)

`project-os-v2#274` lists four candidate actors. Capability comes from the
**execution surface**, never from a role (`kernel/actors.json`), and new kernel
entries require a named, observed failure (`docs/DESIGN.md`). On that basis:

- **`actor.reviewer_chat` — not added.** A reviewer chat is `actor.browser_chat`
  running `workflow.review_before_close`. It has identical surface capabilities
  (draft-only, no write); a separate actor would be a role parallel to a
  surface, which the kernel forbids. Route final PR review to
  `actor.browser_chat` under `workflow.review_before_close`
  (`templates/prompts/review-pr.md`).
- **`actor.security_reviewer` — not added.** Security review is a focus of
  `workflow.review_before_close` (or `workflow.review_only`) on the existing
  terminal or browser surface, not a new surface. PR bodies already carry a
  Security/Privacy section (`templates/pr.md`), and `boundary.security_privacy`
  always applies.
- **`actor.qa_human` / `actor.asset_creator` — not added yet.** A human QA
  tester and an asset creator are real task *recipients*, but they do not
  resolve the kernel as an execution surface; they receive a packet and return a
  verdict or assets. They are modeled here as console operations with a named
  human recipient. `project-os-v2#274` OC.7 explicitly routes any kernel/template
  change these gates need through a **separately scoped `project-os-v2` issue**
  when OC.7 implementation needs it. Adding them now would be a speculative
  kernel entry with no observed failure.

Net OC.0 kernel result: **no new actors, no new workflows.** The needs are met
by existing surfaces, existing workflows, output contracts, and this catalog.

## Authorization semantics

A PM-approved scoped route prompt, or manual PM execution of a scoped command
bundle, is approval evidence for that exact scope
(`kernel/execution_modes.json` `approval_note`; `kernel/evidence.json`
`evidence.pm_approval`). An agent does **not** re-request authorization for the
same route prompt or bundle unless **scope, actor, write type, target, risk, or
evidence changes materially**. Merge, closure, labels, tags, releases, settings,
and automation still each need separate exact PM approval
(`boundary.separate_pm_approval`); they are never implied by a route prompt or a
prior approval.

## Operations

Each operation names: the workflow it runs under, the executing actor, the
evidence it needs, the output contract it produces, and its PM-approval
behavior. "Draft-only" means `actor.browser_chat` produces a draft and a
copy-safe bundle; the write happens on a terminal surface or by PM execution.

Operations that emit `output.pm_command_bundle` (2, 7, 11) follow the one
canonical bundle source, `templates/commands/PM_COMMAND_BUNDLE.md`: default to
short, linear, copy-safe sequences; use a defensive/preflight-heavy bundle only
when the PM asks or live evidence is missing, stale, conflicting, unsafe, or not
yet reviewed. This catalog maps the operations; it does not restate bundle style.

| # | Operation | Workflow | Actor | Evidence | Output | PM approval |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Review roadmap and determine next issue | `workflow.review_only` | browser_chat / terminal_agent | `evidence.repo_state`, `evidence.source_basis` | `output.review_result` | none (read-only) |
| 2 | Create next roadmap issue when none exists | `workflow.pm_intake` | browser_chat (draft) | `evidence.source_basis` | `output.draft_issue` + `output.pm_command_bundle` | PM runs the create bundle (`templates/commands/PM_COMMAND_BUNDLE.md`, create example) |
| 3 | Route next roadmap issue | `workflow.pm_intake` | browser_chat (draft) | `evidence.source_basis`, `evidence.issue_scope` | `output.route_prompt` | route prompt = scope only; PM grants exact authorization |
| 4 | Route a specific issue | `workflow.pm_intake` | browser_chat (draft) | `evidence.issue_scope` | `output.route_prompt` | as #3 (`templates/prompts/route-issue-to-terminal-agent.md`) |
| 5 | Route final PR review to a reviewer surface | `workflow.review_before_close` | browser_chat (draft route) → browser_chat/terminal_agent (review) | `evidence.issue_scope`, `evidence.pr_diff` | `output.route_prompt` → `output.review_result` | review is read-only; no merge/close |
| 6 | Execute review-before-close | `workflow.review_before_close` | terminal_agent / browser_chat | `evidence.issue_scope`, `evidence.pr_diff`, `evidence.validation_output` | `output.review_result` (+ `output.closure_comment` draft) | verdict only; merge/close stay with PM |
| 7 | Generate comment/ready/merge/close/cleanup bundle | `workflow.pm_intake` / `workflow.release_readiness` | browser_chat (draft) | `evidence.repo_state`, `evidence.review_evidence`, `evidence.closure_evidence` | `output.pm_command_bundle` (+ `output.closure_comment`) | PM executes; bundle = approval for that exact bundle (`templates/commands/PM_COMMAND_BUNDLE.md`, closeout example) |
| 8 | Verify post-merge / post-close state | `workflow.review_only` | browser_chat / terminal_agent | `evidence.repo_state` | `output.review_result` or `output.status_result` | none (read-only; copy-safe `gh` reads only) |
| 9 | Draft correction prompt for blockers / non-blockers | `workflow.pm_intake` | browser_chat (draft) | `evidence.pr_diff`, `evidence.review_evidence` | `output.route_prompt` | scope = listed findings only (`templates/prompts/correction-agent.md`) |
| 10 | Draft Project instructions + activation chat for a target | `workflow.target_adoption` | browser_chat (draft) | `evidence.target_adoption` | `output.adoption_packet` | adapter writes need exact target PM approval (`templates/prompts/target-adapter-adoption.md`) |
| 11 | Create follow-up issue from review findings | `workflow.pm_intake` | browser_chat (draft) | `evidence.review_evidence`, `evidence.source_basis` | `output.draft_issue` + `output.pm_command_bundle` | PM runs the create bundle (`templates/commands/PM_COMMAND_BUNDLE.md`, create example) |
| 12 | Generate human QA checklist | `workflow.review_before_close` (QA-focused) | browser_chat (draft) → human QA recipient | `evidence.issue_scope`, `evidence.pr_diff` | `output.review_result` (QA checklist shape) | QA verdict is not write authorization; PM owns merge/close. Formal QA kernel objects, if needed, are scoped separately at OC.7. |
| 13 | Generate asset request | `workflow.pm_intake` | browser_chat (draft) → asset creator recipient | `evidence.source_basis`, `evidence.issue_scope` | `output.draft_issue` (asset-request shape) | assets returned to the target repo under its own scoped approval; OC.7 may scope formal objects separately. |
| 14 | Generate security review | `workflow.review_before_close` (security-focused) | terminal_agent / browser_chat | `evidence.issue_scope`, `evidence.pr_diff` | `output.review_result` (security focus) | `boundary.security_privacy` always applies; security findings can gate merge via `status.needs_pm_decision`. |

Operations 12–14 are documented as console operations now; they introduce no
kernel actors, workflows, or outputs in OC.0. If OC.7 implementation shows a
real gap these patterns cannot close, raise a separately scoped `project-os-v2`
issue with the observed failure, per the kernel's anti-bureaucracy rule.

## Layering: where each kind of thing belongs

- **Kernel (`kernel/*.json`)** — stable, generic operating behavior only:
  actors (surfaces), execution modes, boundaries, workflows, evidence,
  output-contract shapes, statuses. Versioned and validated. No live state, no
  permission grants, no panel/runner specifics.
- **Adapter (`AGENTS.md`, `CLAUDE.md`, `adapters/`)** — compact per-repo
  bootloaders: repository identity, local/kernel paths, kernel version adopted,
  a pointer to the canonical roadmap, and a short Project-specific notes block.
  No kernel rule duplication, no live traceability.
- **Templates (`templates/`)** — reusable output and prompt shapes (issue, PR,
  closure comment, route prompts, command bundles, roadmap, ADR). Shape only;
  shape never grants permission. PM command-bundle style lives in exactly one
  canonical source, `templates/commands/PM_COMMAND_BUNDLE.md`; the kernel,
  outputs, docs, prompts, and the other command templates reference it instead
  of restating command rules.
- **Roadmap issue** — one canonical roadmap per project: what comes next and
  why. Superseded, not mutated into a status store.
- **ADR (`templates/adr.md`)** — decisions that outlive issues, stored in the
  repository that owns the decision.
- **Target docs / target repo** — all product, domain, runtime, build, and
  validation truth for a target. The kernel never stores target product facts.
- **Future console behavior (`project-os-console`)** — UI, server, durable job
  queue, desktop runner, previews, and gated action buttons. The console
  *consumes* the layers above; it must not re-implement Project OS semantics or
  become a second source of truth. Durable project state stays in GitHub.

## Non-authorization

This catalog authorizes no writes by itself. Every write-capable action requires
a separate scoped issue, live evidence, kernel-resolved gates, exact PM
approval, validation, and review-before-close where applicable.
