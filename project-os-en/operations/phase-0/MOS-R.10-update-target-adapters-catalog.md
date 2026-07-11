# MOS-R.10 — Update target adapters catalog

MOSDLC operation `update-target-adapters-catalog` · Phase 0 — Adoption · Risk: medium.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.target_adoption · mode.delegated_commit_pr · output.adoption_packet (+output.route_prompt)
- Evidence: evidence.target_adoption, evidence.branch_preflight, evidence.pm_approval, evidence.validation_output
- PM approval: Yes (exact approval to write in the target)

**Does:** Update adapters of a target to a new catalog/kernel version.
**For:** Propagate catalog upgrades without massive drift.
**How:** Draft the adoption package and delegate route; the writing requires exact approval, preflight and proportional validation.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.adoption_packet (+output.route_prompt). In case of missing adoption, version, approval, preflight or validation, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.5 or MOS-0.4. Next: MOS-0.5 per updated target. Recommended: MOS-0.5.
