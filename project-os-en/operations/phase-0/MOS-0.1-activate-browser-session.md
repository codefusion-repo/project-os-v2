# MOS-0.1 — Activate browser session

MOSDLC operation `activate-browser-session` · Phase 0 — Adoption · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat
- Kernel: workflow.review_only · mode.review_only · output.status_result
- Evidence: evidence.repo_state (the exact target in a bound session; only the
  resolved kernel's live repository in an unbound session)
- PM approval: No (read-only)

**Does:** Establish the PM draft-only session in browser chat by resolving the kernel manifest, with or without a selected target.
**For:** To start any MOSDLC cycle with correct boundaries and context, and with an unambiguous target whenever one already exists.
**How:** Resolve the kernel and activate one of two explicit session states based
on `TARGET_REPOSITORY`, which is an optional primary locator and not a
requirement to start.

With `TARGET_REPOSITORY`: activate the session bound to the exact target, rebuild
`evidence.repo_state` exclusively against it, and report the initial status
naming the reviewed target.

Without `TARGET_REPOSITORY`: activate the unbound, read-only, draft-only session
and declare explicitly that no target is selected yet. Do not read, pick, or
infer any connected repository. To satisfy `workflow.review_only` minimum
`evidence.repo_state`, record only the live state of the resolved
`KERNEL_REPOSITORY` used to read the manifest; that evidence neither turns the
kernel into a target nor permits inspecting another repository. Do not return
`status.needs_context` merely for starting without a repository. The unbound
session grants no authority and never
lets a target-specific operation skip its evidence: before running any operation
that genuinely depends on repository state, require or derive an unambiguous
target, and fail closed with `status.needs_context` when such an operation
requires one and it cannot be identified.

**Variables**
- Required: — (none)
- Optional: TARGET_REPOSITORY, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (`TARGET_REPOSITORY` is the primary locator in canonical `owner/repo` format and is asked for only when the PM wants to bind the session to a target; PM feedback and questions are context only and never authorize an action)

**Deliver:** output.status_result. Always name the activated session state —bound to an exact target or explicitly unbound. Return `status.needs_context` naming the missing evidence when the PM declares a `TARGET_REPOSITORY` that does not match `owner/repo`, cannot be resolved or read through the connected sources, or whose available evidence belongs to another repository; never silently use another connected repository, and the session remains read-only and draft-only in both states. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: -. Next: MOS-0.2, MOS-0.3, MOS-0.5. Recommended: MOS-0.5 if there is a target adopted; MOS-0.2 or MOS-0.3 if not.
