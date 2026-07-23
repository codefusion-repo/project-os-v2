# Route prompt

Responsibility: route scoped work to another surface as a compact bootloader
referenced to a live unit, without pasting the full unit, its records, or
comments and without granting permission. Implementation detail remains in
live evidence.

The following block is the complete route prompt: it contains one standard
variable block and one concrete instruction at the end.

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo if different}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{path to kernel}}
WORK_UNIT = {{live unit reference: issue #N or PR #N when the target uses GitHub; otherwise the equivalent change request, target record, or exact PM instruction}}
CHANGE_CLASS = {{change_class.read | change_class.small | change_class.standard | change_class.critical}}
TARGET_ACTOR_TYPE = {{actor id}}
WORKFLOW = {{workflow id}}
EXECUTION_MODE = {{mode id}}
OUTPUT_CONTRACT = {{output id}}
OPTIONAL_SKILL = {{skill.<id> | none}}
HYDRATION_LEVEL = {{minimal | compact | full/debug}}
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1-3 lines; do not restate the live unit, its bodies, comments, acceptance criteria, source basis, or checklists}}
OUT_OF_SCOPE = {{plausible mistakes to avoid}}
EVIDENCE_REQUIRED = {{required evidence ids}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none with reason}}
BRANCH_NAME = work/{{unit}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{brief reason}}

{{One concrete instruction: re-resolve the kernel with the declared CHANGE_CLASS, read the required live evidence, and verify PM delivery, PM_AUTHORIZATION_STATUS, and the exact repository, workflow, mode, branch, and scope match; fail closed for a draft, missing delivery, `pending`, or absent, unknown, or inferred values, and implement, review, audit, or draft only the scoped work.}}
```

`WORK_UNIT` names the live unit of the resolved workflow. When the target uses
GitHub, it is usually a live issue or PR; when it does not, it carries the
equivalent live reference: a change request, a target record, or, for a
`change_class.small` admitted by target policy, the exact verifiable PM
instruction. In every case the reference must be live-verifiable and the
objective, scope, out of scope, acceptance criteria, and observable result must
be readable from it; it is never filled with an invented number or a durable
placeholder.

`CHANGE_CLASS` declares one class from the kernel's
`proportionality.change_class` contract. The receiving agent passes it to the
resolver (`--change-class`), which fails closed when the class is unknown or
incompatible with the workflow or mode and uses the class's contractual density
when `HYDRATION_LEVEL` is not declared; an explicit `HYDRATION_LEVEL` may keep or
raise that density, never reduce it. The class belongs to the unit and is
preserved across intake, implementation, review, closeout, and verification. The
class never authorizes anything.

When the route prompt corrects an already-reviewed PR (MOS-3.5), the block adds
`SOURCE_REVIEW` with the exact reference to the source review or comment and
`PR_NUMBER`. In that case browser chat reconstructs `PR_NUMBER`, `SOURCE_REVIEW`,
`CHANGE_CLASS`, and `HYDRATION_LEVEL` from the unit's live evidence —it does not
ask the PM— and shows them already resolved here so the receiver verifies the
contract; it returns the decision to the PM only on real material ambiguity. The
final instruction requires publishing exactly one append-only correction report
on that PR with the previous head, the corrected head, the `blocking-correction`
map, and confirmation that no merge or close happened, without editing the body
or any prior comment.

When drafting, read the live unit and its records (the issue or PR and its
comments when the target uses GitHub; the equivalent live evidence when it
does not), then reference that detail instead of copying it.
Do not add headings, sections, lists, checklists,
or implementation plans before or after the block: outside the variables, the
single final concrete instruction is the only permitted content. The receiving
agent re-resolves the kernel, reads live evidence, and fails closed when context,
authority, or validation is missing. Browser chat infers
`RECOMMENDED_TERMINAL_AGENT_FAMILY` as non-binding advice: Codex for code
implementation, Python tooling, migrations, refactors, and tests; Claude for
document synthesis, architecture review, or long-context prose; Gemini for
multimodal work or the Google ecosystem when it has a clear advantage; and
`none` when there is no meaningful advantage or evidence is insufficient.
Explicit PM feedback may override that recommendation. `OPTIONAL_SKILL`,
`HYDRATION_LEVEL`, and the recommended family do not grant permission or replace exact PM approval; they do not force a tool. `HYDRATION_LEVEL` controls how much
already-resolved contract content the resolver returns and selects the
contractual PM-facing receipt visibility: `compact` is the practical default,
`minimal` retains required boundaries, both hide only that representation, and
`full/debug` shows it in full for review, debugging, or audit. No level changes
the internal receipt or `context_plan`, reads live state, invents state, or changes
authority. The template and wizard do not grant permission by
themselves. A route prompt that is a draft, was not delivered by the PM, or has
`PM_AUTHORIZATION_STATUS=pending` does not authorize writing. When the PM
delivers the route prompt with
`PM_AUTHORIZATION_STATUS=granted for this exact scope and mode`, that delivery
satisfies `evidence.pm_approval` only for the declared repository, workflow,
mode, branch, and scope. The receiving agent must verify that match and the
remaining evidence; an absent, unknown, or inferred status fails closed. No additional GitHub comment is universally required. The agent can never
complete, change, or infer `granted`, and that approval does not cover merge,
closure, tags, releases, deploys, settings, or any action outside the declared
mode.
