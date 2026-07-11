# MOS-3.10 — Analyze release readiness

MOSDLC operation `analyze-release-readiness` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.release_readiness · mode.review_only · output.status_result (+output.pm_command_bundle)
- Evidence: evidence.repo_state, evidence.validation_output
- PM approval: No (read-only)

**Does:** Analyze tag or release readiness from merged evidence and validation, and draft command bundles only when ready.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Assess whether merged scope, validation, known risks, notes, and version/tag intent support a tag or release.

**Variables**
- Required: — (none)
- Optional: TAG_NAME, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result (+output.pm_command_bundle). If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.9. Next: MOS-3.11, MOS-3.12. Recommended: MOS-3.11.
