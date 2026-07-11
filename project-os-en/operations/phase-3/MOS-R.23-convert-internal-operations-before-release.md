# MOS-R.23 — Convert internal operations before release

MOSDLC operation `convert-internal-operations-before-release` · Phase 3 — Implementation · Risk: high.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat a terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt (+output.draft_issue)
- Evidence: evidence.source_basis
- PM approval: No for drafting; exact approval is required to convert, hide, remove, or disable

**Does:** Draft internal-only surface conversion before public release.
**For:** To publish without exposing internal capabilities of the target.
**How:** Use the target's exposure inventory to produce a non-authorizing delegated route.

**Variables**
- Required: TARGET_REPOSITORY
- Optional: PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (PM feedback and questions are context only and never authorize an action)

**Safeguards**
- Safe options are remove, hide, disable, or convert; the specific choice may require the PM.
- Do not implement conversions or change packaging; this operation only drafts the route.
- Redact secrets and do not copy sensitive internal details outside their context.

**Deliver:** output.route_prompt (+output.draft_issue). In case of unreadable inventory, ambiguous disposition or missing approval for writing, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-R.22. Next: MOS-R.7 to re-verify publication. Recommended: MOS-R.7.
