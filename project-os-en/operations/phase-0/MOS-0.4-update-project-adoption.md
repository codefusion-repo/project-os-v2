# MOS-0.4 — Update project adoption

<!-- project-os-operation
canonical_code: MOS-0.4
operation_id: update-project-adoption
aliases: MOS-R.10
deprecation: none
compatibility_reason: MOS-R.10 keeps historical compatible resolution without duplicating this operational contract.
-->

MOSDLC operation `update-project-adoption` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.route_prompt, +output.status_result)
- Evidence: evidence.target_adoption
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery of the route prompt with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the browser-first update of an already adopted target to the current kernel/catalog version.
**For:** To keep adoption aligned to the current kernel.
**How:** Use the adoption flow: a browser-first draft in `mode.review_only` plus a delegated write through a route prompt when confirmed terminal drift exists.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PROJECT_NAME, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, ADOPTION_ISSUE_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Browser adapter first:** Draft a complete `BROWSER_CHAT.md` update when drift exists against the canonical adapter; preserve its read-only and draft-only boundaries and do not require it as a repo file.

**Terminal drift and route prompt:** Report `terminal_adoption_state` and route only confirmed terminal drift. When a live work unit exists (`ADOPTION_ISSUE_NUMBER`), draft a route prompt that delegates the repo-owned adapter update to the terminal agent in `mode.delegated_commit_pr`, with branch preflight, validation, and exact PM approval; preserve target-owned notes and constraints and never invent the work unit.

**Deliver:** output.adoption_packet (+output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5 or MOS-R.5. Next: MOS-0.5. Recommended: MOS-0.5.
