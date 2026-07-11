# MOS-R.18 — Secret safe config audit

MOSDLC operation `secret-safe-config-audit` · Phase 6 — Production readiness and maintenance · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only and redacted audit by design)

**Does:** Audit environment and configuration risk for the target project reporting only file paths, variable names, and risk types, never values.
**For:** Complete this lifecycle outcome through the selected workflow with explicit evidence and boundaries.
**How:** Read-only, redacted-by-design scan of environment and configuration risk: committed secrets, secret-looking values, unsafe defaults, missing env templates, and overexposed configuration.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Never open, paste, summarize, or reconstruct secret values; always use `[REDACTED]`.
- Do not run `env`, `printenv`, `set`, framework dumps, or CI secret contexts.
- Do not rotate keys, edit configuration, mutate secret stores, or touch deployment secrets.

**Deliver:** output.status_result. If required evidence, scope, or approval is missing or ambiguous, fail closed with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-6.1. Next: MOS-3.3. Recommended: MOS-3.3.
