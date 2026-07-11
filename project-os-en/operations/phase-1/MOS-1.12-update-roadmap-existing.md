# MOS-1.12 — Update roadmap existing

MOSDLC operation `update-roadmap-existing` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.draft_issue (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: Yes (only the bundled GitHub write, run by the Human PM)

**Does:** Update or plan the general roadmap of an existing project.
**For:** Give direction by phases to adopted projects.
**How:** Draft creation or update of the roadmap issue for the Human PM.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: SOURCE_DOCS, ROADMAP_ACTION, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.draft_issue (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.11. Next: MOS-3.1. Recommended: MOS-3.1.
