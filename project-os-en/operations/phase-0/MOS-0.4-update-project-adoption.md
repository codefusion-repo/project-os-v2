# MOS-0.4 — Update project adoption

MOSDLC operation `update-project-adoption` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval for target writes)

**Does:** Refreshes adapters from an already adopted target to the current kernel/catalog version.
**For:** Keep adoption aligned to the current kernel.
**How:** Same as adoption: draft plus delegated writing with exact approval.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5 or MOS-R.5. Next: MOS-0.5. Recommended: MOS-0.5.
