# MOS-3.3 — Draft a follow-up issue

MOSDLC operation `draft-follow-up-issue` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → human_pm
- Kernel: workflow.pm_intake · mode.review_only · output.pm_command_bundle
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (draft-only; the Human PM decides and runs the bundle)

**Does:** Draft a follow-up from any live source: an incomplete issue, a
review, a discipline audit, or a security review.
**For:** To defer pending work and non-blocking findings with traceability.
**How:** Isolate what is missing or deferred in a follow-up with its own
scope; the live source stays referenced, not copied. Apply the materiality gate
from `rule.economia_de_contexto` first: draft only when the source holds a
current, durable, actionable gap with an observable outcome, independent scope,
and a reason to defer it instead of discarding it. That an observation is
technically true or could be written as an issue is not enough: a historical,
informational, confirmatory observation, one already resolved by the normal
course, or a duplicate of live evidence produces no follow-up. Without durable,
actionable work, return no-action with `output.status_result`. Use at most one
primary locator: when the current invocation already identifies one unambiguous
live source —the review, audit, security review, or issue just worked on in this
session— do not ask for it again; when none exists, ask only for
`FOLLOW_UP_SOURCE` and reconstruct its relations from there.

**Variables**
- Required: none
- Optional: FOLLOW_UP_SOURCE, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO
  (`FOLLOW_UP_SOURCE` is the single primary locator —incomplete issue, review,
  audit or security-review result, or another live record— and is asked for only
  when the execution context does not already identify one unambiguous source;
  PM feedback and questions are context only and never authorize an action)

**Derived metadata:** the related issue or unit, the PR, the source review or
comment, the existing branch, and the relations between roadmap, unit, and
findings are reconstructed from the live source and shown resolved in the bundle
for the Human PM's verification; they are not manual inputs nor fields the PM
copies from GitHub, and they are never invented. Only real material ambiguity
—several incompatible sources equally active or an unverifiable
unit↔PR↔review relation— returns `status.needs_context` or
`status.needs_pm_decision`; a PM who did not retype a reconstructible identifier
never causes a fail-closed.

**Deliver:** output.pm_command_bundle. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-3.14, MOS-3.25 or MOS-3.31.
Next: MOS-3.4 when prioritized. Recommended: MOS-3.4.
