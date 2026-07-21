# MOS-0.5 — Verify target adoption

MOSDLC operation `verify-target-adoption` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.target_adoption · mode.review_only · output.status_result (+output.adoption_packet, +output.route_prompt)
- Evidence: evidence.target_adoption
- PM approval: No (read-only/draft-only)

**Does:** Audit target adoption read-only, separating browser and terminal readiness, and draft repairs when appropriate.
**For:** To confirm that the target can operate safely.
**How:** Read adapters and target evidence without writing; audit browser and terminal separately.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Separate audit:** Report `browser_adoption_state` and `terminal_adoption_state` independently. When the browser adapter content is not supplied, do not claim its readiness: mark it as not supplied and return `status.needs_context`. Return a global GO only when both applicable surfaces are ready.

**Repair:** When the audit finds the browser adapter missing or outdated, include a corrected draft in the adoption packet. When findings require a terminal correction, draft a route prompt that delegates the repo-owned adapter repair to the terminal agent in `mode.delegated_commit_pr`, with branch preflight, validation, and exact PM approval. The live unit is the bounded target adoption — `TARGET_REPOSITORY`, the exact adapter scope, the branch, and `evidence.target_adoption` — and requires no prior roadmap or adoption issue; never invent the work unit or the scope.

**Deliver:** output.status_result (+output.adoption_packet, +output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.2, MOS-0.3 or MOS-0.4. Next: MOS-1.1 or MOS-1.10 depending on the project. Recommended: MOS-R.2.
