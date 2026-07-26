# MOS-3.14 — Process audit result

<!-- project-os-operation
canonical_code: MOS-3.14
operation_id: process-audit-result
aliases: MOS-6.11
deprecation: none
compatibility_reason: MOS-6.11 keeps its historical code-improvement entry point and resolves this canonical contract for any audit or review referenced by REVIEW_SOURCE.
-->

MOSDLC operation `process-audit-result` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.pm_command_bundle, output.status_result)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the result of any audit or review (traceability, discipline,
maintenance analysis, or other) and classify the safe route.
**For:** To convert findings into concrete actions without fragmenting the
processing by originating review type.
**How:** Classify each finding with its verifiable disposition and route it to
correction (`blocking-correction` → MOS-3.5), follow-up (`non-blocking-follow-up`
→ MOS-3.3), or no-op (`preference`, `accepted-risk`, `invalid-finding`); a
resolved classification delivers the applicable route prompt or command bundle.
The origin travels as a live reference in `REVIEW_SOURCE`; the operation does not
depend on the originating review type.

**Variables**
- Required: REVIEW_SOURCE
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the related issue or unit, the PR, the branch, the roadmap,
and the remaining verifiable relations are reconstructed from `REVIEW_SOURCE` and
shown resolved in the output for the receiver to verify; they are not manual
inputs nor fields the PM copies from GitHub, and they are never invented. Only a
missing, unverifiable, or materially ambiguous source —several incompatible
sources equally active, or a material relation that cannot be reconstructed—
returns `status.needs_context` or `status.needs_pm_decision`; a reconstructible
identifier the PM did not retype never fails closed.

**Deliver:** output.route_prompt (+output.pm_command_bundle, output.status_result). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.13, MOS-3.24, or another audit. Next: MOS-3.5 or MOS-3.3. Recommended: MOS-3.3 for non-blocking.
