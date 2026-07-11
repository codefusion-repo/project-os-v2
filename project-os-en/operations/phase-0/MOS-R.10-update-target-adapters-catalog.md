# MOS-R.10 — Update target adapters catalog

MOSDLC operation `update-target-adapters-catalog` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval to write in the target)

**Does:** Update a target project's adapters to a new catalog/kernel version through a delegated, exactly approved write route.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Draft the adoption update packet for the target; the terminal-agent write requires separate exact PM approval for writing in that target, branch preflight, proportional validation, and a draft PR.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.5, MOS-0.4. Next: MOS-0.5. Recommended: MOS-0.5.
