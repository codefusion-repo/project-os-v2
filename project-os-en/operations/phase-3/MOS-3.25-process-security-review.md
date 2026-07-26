# MOS-3.25 — Process security review

MOSDLC operation `process-security-review` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Process the security-review result and classify the safe route.
**For:** To convert security findings into correction or follow-up.
**How:** Classify blockers and non-blockers without executing anything.

**Variables**
- Required: SECURITY_REVIEW_RESULT
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Derived metadata:** the related issue or unit, the PR, the branch, and the
remaining verifiable relations are reconstructed from `SECURITY_REVIEW_RESULT`
and shown resolved in the output for the receiver to verify; they are not
manual inputs nor fields the PM copies from GitHub, and they are never
invented. Only real material ambiguity —several incompatible sources equally
active, or an unverifiable relation— returns `status.needs_context` or
`status.needs_pm_decision`; a reconstructible identifier the PM did not retype
never fails closed.

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.23. Next: MOS-3.5, MOS-3.3 or MOS-3.7. Recommended: MOS-3.5 for blockers.
