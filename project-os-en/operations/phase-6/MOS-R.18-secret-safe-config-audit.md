# MOS-R.18 — Secret safe config audit

MOSDLC operation `secret-safe-config-audit` · Phase 6 — Maintenance and improvements · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat / terminal_agent
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state
- PM approval: No (read-only and redacted audit by design)

**Does:** Audit environment/config risks without exposing secrets.
**For:** Detect insecure configuration, risky defaults or compromised secrets without copying values.
**How:** Review repo configuration surfaces and report only path, variable name and risk type.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Never open, paste, summarize, or reconstruct secret values; always use `[REDACTED]`.
- Do not run `env`, `printenv`, `set`, framework dumps, or CI secret contexts.
- Do not rotate keys, edit configuration, mutate secret stores, or touch deployment secrets.

**Deliver:** output.status_result. For unreadable surfaces, return `status.needs_context`; if a live secret is exposed, return `status.blocked`.

**Connections:** Previous: MOS-6.1 or maintenance audit. Next: MOS-3.3 for detected risk. Recommended: MOS-3.3.
