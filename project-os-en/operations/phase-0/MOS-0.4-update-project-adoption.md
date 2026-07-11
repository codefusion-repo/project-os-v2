# MOS-0.4 — Update project adoption

MOSDLC operation `update-project-adoption` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval for target writes)

**Does:** Refresh an already adopted target repository to the current Project OS adoption standard.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft an adoption-update packet with exact adapter-only changes and an update checklist.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5, MOS-R.5. Next: MOS-0.5. Recommended: MOS-0.5.
