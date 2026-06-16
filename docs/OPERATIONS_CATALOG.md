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

## Actor and gate decision matrix

`project-os-v2#274` lists four candidate actors. Capability comes from the
**execution surface**, never from a role (`kernel/actors.json`), and new kernel
entries require a named, observed failure (`docs/DESIGN.md`). The decision is:
**no new actors and no new workflows.**

| Candidate | Decision | Represented as | Kernel/template impact before OC.1 | Console consequence |
| --- | --- | --- | --- | --- |
| `actor.reviewer_chat` | Do not add actor. | Workflow focus on existing `actor.browser_chat` or `actor.terminal_agent` running `workflow.review_before_close` / `workflow.review_only`. | No new kernel object. `templates/prompts/review-pr.md` routes to one existing review-capable surface. | The console may label a review destination, but it must store the resolved Project OS actor as an existing surface. |
| `actor.qa_human` | Do not add actor; model as gate plus human recipient. | Operation 12 produces a QA-focused `output.review_result` packet for a human QA recipient. | No dedicated output contract or QA template before OC.1; the catalog shape below is enough for planning. | OC.7 may add UI tracking or a template only if dogfood shows repeated QA packet drift. QA verdict is evidence, not PM write authorization. |
| `actor.asset_creator` | Do not add actor; model as human/service recipient. | Operation 13 produces an asset-request-shaped `output.draft_issue` or follow-up packet. | No dedicated output contract or asset template before OC.1; `templates/issue.md` remains the canonical issue shape. | The console may track pending asset needs later; returned assets enter target repos only through their own scoped approval. |
| `actor.security_reviewer` | Do not add actor; model as review focus and possible gate. | Operation 14 produces a security-focused `output.review_result`; `boundary.security_privacy` always applies. | No dedicated output contract or security template before OC.1; `templates/pr.md` keeps the PR Security/Privacy section. | The console may route a security review to an existing surface; blocking findings can return `status.needs_pm_decision`. |

## Authorization semantics

The canonical route-prompt and command-bundle approval rule lives in
`kernel/execution_modes.json` `approval_note`, with approval evidence defined by
`kernel/evidence.json` `evidence.pm_approval`. In catalog terms: an exact
PM-approved scoped route prompt or command bundle is approval evidence for that
same scope; material changes require the agent to stop and re-resolve approval.
Merge, closure, labels, tags, releases, settings, and automation still each need
separate exact PM approval (`boundary.separate_pm_approval`); they are never
implied by a route prompt or a prior approval.

## Operations

Each operation names: the workflow it runs under, the executing actor, the
evidence it needs, the output contract it produces, and its PM-approval
behavior. "Draft-only" means `actor.browser_chat` produces a draft and a
copy-safe bundle; the write happens on a terminal surface or by PM execution.

Operations that emit `output.pm_command_bundle` (2, 7, 11) follow
`templates/commands/PM_COMMAND_BUNDLE.md`. This catalog maps the operations; the
command source owns bundle shape, style, examples, and defensive-bundle rules.

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
| 12 | Generate human QA checklist | `workflow.review_before_close` (QA-focused) | browser_chat (draft) → human QA recipient | `evidence.issue_scope`, `evidence.pr_diff` | `output.review_result` (QA checklist shape below) | QA verdict is gate evidence, not write authorization; PM owns merge/close. |
| 13 | Generate asset request | `workflow.pm_intake` | browser_chat (draft) → asset creator recipient | `evidence.source_basis`, `evidence.issue_scope` | `output.draft_issue` (asset-request shape below) | assets returned to the target repo under its own scoped approval. |
| 14 | Generate security review | `workflow.review_before_close` (security-focused) | terminal_agent / browser_chat | `evidence.issue_scope`, `evidence.pr_diff` | `output.review_result` (security shape below) | `boundary.security_privacy` always applies; security findings can gate merge via `status.needs_pm_decision`. |

## Gate packet shapes for OC.1 planning

These are catalog shapes over existing output contracts, not new templates or
kernel outputs. They give OC.1 enough structure to plan console operations while
avoiding speculative objects before implementation evidence exists.

- **Human QA checklist (`output.review_result`)** — scope and evidence reviewed;
  environment/device/build context when relevant; manual checklist; observed
  pass/fail results; blockers or follow-up recommendations; explicit statement
  that QA verdict is not PM write authorization.
- **Asset request (`output.draft_issue`)** — source basis; assets needed;
  constraints such as format, dimensions, style, licensing, and target repo;
  acceptance criteria; delivery path; out-of-scope; approval boundary for any
  target repo writes.
- **Security review (`output.review_result`)** — touched surfaces; data,
  secrets, auth, network, dependency, and deployment assumptions; findings by
  severity; required fixes or PM risk decisions; boundaries preserved.

Operations 12–14 are therefore ready for OC.1 planning without new actors,
workflows, output contracts, or standalone templates. If OC.7 dogfood shows
repeated packet drift, raise a separately scoped `project-os-v2` issue with the
observed failure before adding formal templates or output contracts.

## OC.1 use of this catalog

Use this catalog as the semantic input for OC.1: operation inventory, existing
workflow/output/evidence mappings, actor/gate decisions, and approval behavior.
It intentionally does not define console UI, API payloads, queue schemas,
runner behavior, database state, or button semantics; those belong to the future
console repository and must consume these Project OS semantics.

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
  outputs, docs, and prompts reference it instead of restating command rules.
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
