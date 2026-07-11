# MOS-0.3 — Adopt existing project

MOSDLC operation `adopt-existing-project` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval for target writes)

**Does:** Prepare an existing target repository for Project OS adoption, with any writes delegated only through exact PM approval.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft an adoption packet that names missing or drifted adapters and the exact adapter-only write scope.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.1. Next: MOS-0.5. Recommended: MOS-0.5.
