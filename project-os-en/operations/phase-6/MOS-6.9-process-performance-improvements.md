# MOS-6.9 — Process performance improvements

MOSDLC operation `process-performance-improvements` · Phase 6 — Maintenance and improvements · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle, output.status_result)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process recommended performance improvements.
**For:** To turn recommendations into prioritized work.
**How:** Read the live review referenced by `REVIEW_SOURCE` and classify each
improvement into issues or follow-ups; a resolved classification delivers the
applicable route prompt or command bundle.

**Variables**
- Required: REVIEW_SOURCE
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the related issue or unit, the PR, the branch, the roadmap,
and the remaining verifiable relations are reconstructed from `REVIEW_SOURCE` and
shown resolved in the output; they are not manual inputs and are never invented.
Only a missing, unverifiable, or materially ambiguous source —several
incompatible sources equally active, or a material relation that cannot be
reconstructed— fails closed with output.status_result.

**Deliver:** output.route_prompt (+output.pm_command_bundle, output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.3. Next: MOS-3.8 or MOS-3.3. Recommended: MOS-3.3.
