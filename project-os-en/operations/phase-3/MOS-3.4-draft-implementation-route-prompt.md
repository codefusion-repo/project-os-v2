# MOS-3.4 — Draft implementation route prompt

MOSDLC operation `draft-implementation-route-prompt` · Phase 3 — Implementation · Risk: low.
Common contract: `project-os-en/operations/README.md` (kernel resolution, live state, validation, non-authorization, fail-closed behavior, and secret safety).

- Surface: browser_chat → terminal_agent
- Kernel: workflow.pm_intake · mode.review_only · output.route_prompt
- Evidence: evidence.source_basis, evidence.repo_state
- PM approval: No for drafting. A draft does not authorize writing; a PM
  delivery with `PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`
  can satisfy exact PM approval only for what it declares.

**Does:** Draft the route-prompt to delegate the implementation of a live work
unit to a terminal agent.
**For:** To route implementation with the correct unit, class, scope, mode and evidence.
**How:** Use a compact bootloader referenced to the live unit: detail stays in
the unit and its records (issue or PR and comments when the target uses GitHub;
a change request, target record, or exact PM instruction when it does not), not
in the route prompt. Human inputs are `WORK_UNIT` when context does not already
identify the unit, `OPTIONAL_SKILL`, PM feedback or questions, the explicit
`/hydration` override, and the applicable exact authorization; they are not
derived metadata and authorize nothing. The rest of the metadata is reconstructed
from live evidence and shown resolved for inspection, not asked again. When the current invocation
already identifies that unit unambiguously —for example the issue MOS-3.1,
MOS-3.2, or MOS-3.8 just drafted in this session— do not ask for its locator
again. Browser chat reads the unit and its relations, reconstructs
`CHANGE_CLASS` from the scope, risk, and affected surfaces per the
`proportionality.change_class` contract, and resolves the related
roadmap, the existing PR when applicable, and the scoped branch
`work/<unit>-<slug>`. For a `change_class.small` admitted by target policy, the
exact PM instruction may be the live unit without an issue; for a class that
requires a formal unit, resolve the verifiable live unit or fail closed, never
substituting invented metadata. When deriving `SCOPE` and `OUT_OF_SCOPE`,
interpret the unit by intent: only authorization, identity, hard constraints,
scope, out of scope, and safety are literal; examples, tentative names, and
implementation proposals are advisory. Browser chat may
recommend an optional skill and infer `RECOMMENDED_TERMINAL_AGENT_FAMILY` from
the work. The recommendation is advisory, authorizes nothing, and may be
overridden by explicit PM feedback.

**Variables**
- Required: none
- Optional: WORK_UNIT, OPTIONAL_SKILL, PM_FEEDBACK_HUMANO, PM_QUESTION_HUMANO (`WORK_UNIT` is the single primary locator and is asked for only when the execution context does not already identify the live unit; `OPTIONAL_SKILL`, PM feedback, and PM questions are optional human inputs; none authorize an action)

**Derived metadata:** `CHANGE_CLASS`, `ROADMAP_ISSUE`,
`BRANCH_NAME`, the existing PR, and the remaining verifiable relations are not
manual wizard inputs nor fields the PM copies from GitHub: browser chat
reconstructs them from live evidence and shows them resolved in the route prompt
for the receiver's verification; it never invents them. `CHANGE_CLASS` belongs to
the unit and is preserved across intake, implementation, review, closeout, and
verification; it governs the material gates and the execution report density,
never the resolver hydration. `HYDRATION_LEVEL` is not derived from the class:
the resolver applies `compact` by default for every class, so without an override
the variable is omitted. It controls only the resolver's hydrated content: no
level changes gates, report density, or authority. The wizard captures the declared human
inputs and assists with `PM_AUTHORIZATION_STATUS`; it does not request the
class, the hydration, the roadmap, or the branch when they can be derived or omitted.
Hydration keeps a single override route: an explicit PM decision
—`/hydration <level>` in the wizard,
which writes it as `HYDRATION_LEVEL` in the INPUT block— may select any of the
three levels, with no ranking derived from the class. It is not a routine question:
without that explicit override the
variable is neither asked for nor carried. Only real material ambiguity —a
missing formal unit for a class that requires one, a scope that does not allow
determining the class with confidence, unverifiable relations, or a conflict
between live evidence and a later PM decision— returns `status.needs_context` or
`status.needs_pm_decision`.

**Inferred recommendation:** `RECOMMENDED_TERMINAL_AGENT_FAMILY` is browser-chat
advice based on the work; it is shown for inspection, never requested from the
PM, and never authorizes a tool or action.

**Authorization contract:** Browser chat only drafts and can never self-assign,
complete, change, or infer `granted`. A route prompt that is a draft, was not
delivered by the PM, or has `PM_AUTHORIZATION_STATUS` set to `pending` does not
authorize writing. When the PM delivers the route prompt with
`PM_AUTHORIZATION_STATUS` set to `granted for this exact scope and mode`, that delivery
satisfies `evidence.pm_approval` only for the declared repository, workflow,
mode, branch, and scope. The receiving agent must verify that match and the
remaining evidence; an absent, unknown, or inferred status fails closed. No additional GitHub comment is universally required, and the approval does not
cover merge, closure, tags, releases, deploys, settings, or any action outside
the declared mode.

**Conformance check:** Before delivery, compare the output with
`project-os-en/templates/route-prompt.md`. Compress it when it repeats detail
from the live unit or its records; keep a live-evidence reference instead of
copying bodies, acceptance criteria, source basis, checklists, or
implementation steps. Deliver
only one standard variable block, a 1-3 line `SCOPE`, and one following concrete
instruction. If that shape cannot be produced, fail closed with
`output.status_result`.

**Reproducible manual QA:** Use a live unit with extensive records. Verify that
the route prompt keeps only metadata, the live reference, the reconstructed class
and density, a brief scope, brief out-of-scope, and one
concrete instruction; that `SCOPE` has 1-3 lines; that it has no copied sections;
that no derivable value was asked of the PM; and that it instructs the receiving
agent to read live evidence.

**Deliver:** output.route_prompt. If evidence, scope, approval, or a conforming shape is missing or ambiguous, fail closed: report with `output.status_result` and return the decision to the PM.

**Connections:** Previous: MOS-1.7, MOS-3.1, MOS-3.2 or MOS-3.8, or an exact PM
instruction as the live unit of a `change_class.small`. Next: MOS-3.7 after the
PR. Recommended: MOS-3.7.
