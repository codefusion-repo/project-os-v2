# MOS-3.1 — Draft next issue from traceability

MOSDLC operation `draft-next-issue-from-traceability` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Infer the next single implementation issue from live traceability and roadmap evidence, then draft a Human PM command bundle.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Identify the single next outcome that is best supported by roadmap and traceability evidence.

**Variables**
- Required: — (none)
- Optional: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.6, MOS-3.9. Next: MOS-3.4. Recommended: MOS-3.4.
