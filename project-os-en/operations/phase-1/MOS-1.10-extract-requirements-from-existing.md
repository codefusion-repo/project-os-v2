# MOS-1.10 — Extract requirements from existing

MOSDLC operation `extract-requirements-from-existing` · Phase 1 — Requirements, planning, and feasibility · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state, evidence.target_adoption
- PM approval: No (read-only)

**Does:** Identify real requirements from the code and docs of an existing project.
**For:** To adopt projects that never had formal Phase 1.
**How:** Read the repo target and reconstruct observable requirements.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-0.3. Next: MOS-1.11. Recommended: MOS-1.11.
