# MOS-1.6 — Plan project roadmap

MOSDLC operation `plan-project-roadmap` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: Yes (only the bundled GitHub write, run by the Human PM)

**Does:** Plan the general roadmap of the project from stable documentation.
**For:** Organize work by phases and outcomes.
**How:** Draft the issue body roadmap or creation bundle for the Human PM.

**Variables**
- Required: SOURCE_DOCS
- Optional: TARGET_REPOSITORY, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.draft_issue (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.5. Next: MOS-3.1 or MOS-3.2. Recommended: MOS-3.1.
