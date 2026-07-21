# MOS-0.3 — Adopt existing project

MOSDLC operation `adopt-existing-project` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.adoption_packet (+output.route_prompt, +output.status_result)
- Evidence: evidence.target_adoption
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery of the route prompt with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the browser-first adoption of an existing repo: a complete browser adapter and an audit of the terminal state.
**For:** To adopt an existing project as a target.
**How:** Browser chat resolves the kernel in `mode.review_only`, drafts the browser adapter, and audits the terminal adapters; writing is delegated by the route prompt.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PROJECT_NAME, KERNEL_VERSION_ADOPTED, ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Browser adapter first:** Always produce a complete PM-applicable `BROWSER_CHAT.md` draft. It is PM-applied and need not be stored inside the target repo; keep its read-only and draft-only boundaries.

**Adoption packet and route prompt:** Report `browser_adoption_state` and `terminal_adoption_state` separately. Produce the draft-only adoption packet and a route prompt that delegates the repo-owned adapter bootstrap to the terminal agent in `mode.delegated_commit_pr`, with branch preflight, validation, and exact PM approval. The live unit is the bounded target adoption — `TARGET_REPOSITORY`, the exact adapter scope, the branch, and `evidence.target_adoption` — and requires no prior roadmap or adoption issue; an existing roadmap is optional evidence. Never invent the work unit or the scope.

**Deliver:** output.adoption_packet (+output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
