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
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval for target writes)

**Does:** Refresh adapters from an already adopted target to the current kernel/catalog version.
**For:** To keep adoption aligned to the current kernel.
**How:** Use the adoption flow: draft first, then write through a delegated route with exact approval.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.5 or MOS-R.5. Next: MOS-0.5. Recommended: MOS-0.5.
