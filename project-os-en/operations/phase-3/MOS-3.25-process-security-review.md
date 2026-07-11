# MOS-3.25 — Process security review

MOSDLC operation `process-security-review` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.status_result (+output.route_prompt, output.pm_command_bundle)
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only)

**Does:** Processes the result of a security review and classifies the safe route.
**For:** Convert security findings into correction or follow-up.
**How:** Classifies blockers and non-blockers without executing anything.

**Variables**
- Required: SECURITY_REVIEW_RESULT
- Optional: PR_NUMBER, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Strict security posture: describe sensitive surfaces only by variable name, command, path, or risk type; never expose secrets, `.env` values, tokens, or credentials.

**Deliver:** output.status_result (+output.route_prompt, output.pm_command_bundle). If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.23. Next: MOS-3.5, MOS-3.29 or MOS-3.7. Recommended: MOS-3.5 for blockers.
