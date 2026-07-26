# MOS-3.5 — Draft correction route prompt

MOSDLC operation `draft-correction-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No (the route prompt does not authorize; writing requires exact PM approval)

**Does:** Draft the correction route-prompt of a live work unit from findings
with a `blocking-correction` disposition.
**For:** To correct only material breaches without expanding the original scope.
**How:** Encapsulate only `blocking-correction` findings in a delegated
correction route; `non-blocking-follow-up` findings defer to MOS-3.3, and
`preference`, `accepted-risk`, and `invalid-finding` force no changes. Human
inputs are `WORK_UNIT`, `OPTIONAL_SKILL`, PM feedback or questions, the explicit
`/hydration` override, and the applicable exact authorization; they are not
derived metadata and authorize nothing. The rest of the metadata is reconstructed
from live evidence and shown resolved for inspection, not asked again. Browser
chat reads the live unit and its relations, locates the existing
PR when applicable, reads its full conversation, selects the latest active review
with unresolved `blocking-correction` findings and incorporates its later PM
addenda as part of the same source basis, reconstructs or preserves the unit's
`CHANGE_CLASS`, and derives `HYDRATION_LEVEL` from that class (`full/debug` for
`change_class.critical`). With those resolved values it fills `WORK_UNIT`,
`SOURCE_REVIEW`, `PR_NUMBER`, `CHANGE_CLASS`, and `HYDRATION_LEVEL` in the route
prompt so the terminal receiver verifies the contract; it never invents them. When
a single active review with unresolved `blocking-correction` findings exists, it
selects it automatically; it returns `status.needs_pm_decision` or
`status.needs_context` only on real material ambiguity —two incompatible reviews
equally active, an unverifiable unit↔PR relation, materially truncated comments,
insufficient evidence to determine the class, or a real contradiction between the
review and a later PM decision—, never because the PM did not retype an ID, a
class, or a level that can be reconstructed. The route prompt requires the
executing agent to publish exactly one append-only correction report on that PR
that references the source review, records the previous and corrected heads, maps
each `blocking-correction` to its outcome, identifies the commits or range and the
real validation, states remaining work, and confirms no merge or close happened,
without editing the body or any prior comment. Findings travel by intent: the
material breach and its observable criterion are binding; the reviewer's wording
and solution proposals are advisory. Browser chat may recommend an optional skill
and infer `RECOMMENDED_TERMINAL_AGENT_FAMILY` from the work. The recommendation is
advisory, authorizes nothing, and may be overridden by explicit PM feedback.

**Variables**
- Required: WORK_UNIT
- Optional: OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (the skill, PM
  feedback, and PM questions are optional human inputs and never authorize an
  action)

**Derived metadata:** `SOURCE_REVIEW`, `PR_NUMBER`, `CHANGE_CLASS`, and
`HYDRATION_LEVEL` are not manual wizard inputs nor fields the PM copies from
GitHub: browser chat reconstructs them from live evidence and shows them resolved
in the route prompt for the receiver's verification. `HYDRATION_LEVEL` accepts
`minimal`, `compact`, or `full/debug`, is derived from the reconstructed
`CHANGE_CLASS`, and never drops below its contractual density; it controls only
the resolver's hydrated content and no level returns `context_plan` or adds a
receipt block. The wizard captures the declared human inputs and assists with
`PM_AUTHORIZATION_STATUS`; it does not request `SOURCE_REVIEW`, `PR_NUMBER`,
`CHANGE_CLASS`, or the default density when they can be derived. As in MOS-3.4,
the density keeps a single explicit override route —`/hydration <level>` in the
wizard, written as `HYDRATION_LEVEL` in the INPUT
block— that may keep or raise it, never reduce it, and that is never asked
routinely.

**Inferred recommendation:** `RECOMMENDED_TERMINAL_AGENT_FAMILY` is browser-chat
advice based on the work; it is shown for inspection, never requested from the
PM, and never authorizes a tool or action.

**Deliver:** output.route_prompt. If evidence, scope, or approval is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-3.7, MOS-3.25 or MOS-4.4, only with
`blocking-correction` findings. Next: MOS-3.7. Recommended: MOS-3.7.
