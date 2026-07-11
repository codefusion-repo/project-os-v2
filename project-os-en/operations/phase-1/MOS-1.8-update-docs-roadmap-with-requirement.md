# MOS-1.8 — Update docs roadmap with requirement

MOSDLC operation `update-docs-roadmap-with-requirement` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: Yes (exact approval for the file write only)

**Does:** Update documentation and roadmap with an accepted requirement.
**For:** To maintain docs and roadmap as the only truth of scope.
**How:** Draft documentation and roadmap changes; write only with exact approval.

**Variables**
- Required: DESCRIPTION
- Optional: ROADMAP_ISSUE, DOC_TARGET, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.route_prompt (+output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.7. Next: MOS-3.1. Recommended: MOS-3.1.
