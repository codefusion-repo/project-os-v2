# MOS-3.1 — Draft next issue from traceability

MOSDLC operation `draft-next-issue-from-traceability` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Infer the next real outcome from live traceability and roadmap and draft its creation.
**For:** To create the next unique issue without losing track of the roadmap.
**How:** Read live state and draft the issue-creation bundle for the Human PM.

When arriving from MOS-R.2, reuse intent, constraints, and source basis to
draft a single unit; do not ask the PM to capture them again. Creation remains
with the Human PM. For implementation intent, once the creation result is
live-verifiable, continue to MOS-3.4 per MOS-R.2 without another MOS selection
or redundant locator.

Before drafting, check whether a unit already exists for the outcome and
reuse it; do not create another for planning or handoff. For a sequential
roadmap, identify whether a predecessor exists; when it does, verify material
completion from live scope, criteria, PR, review/QA, validation, and closure: an isolated GO, merged
PR, or closed issue does not prove the outcome. If it remains materially open,
retain that unit and report the next safe step with `output.status_result`,
without drafting the next phase. Missing evidence fails closed. Once complete,
infer and draft a single unit for the next real outcome, reusing an existing
one if present; never an advance set merely enumerated from the roadmap.
Material priority ambiguity returns to the PM.

**Variables**
- Required: — (none)
- Optional: ROADMAP_ISSUE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.6 or the GO closure of MOS-3.7. Next: MOS-3.4. Recommended: MOS-3.4.
