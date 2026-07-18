# Route prompt

Responsibility: route scoped work to another surface as a compact,
issue-referential bootloader, without pasting the full issue, PR, or comments
and without granting permission. Implementation detail remains in live evidence.

The following block is the complete route prompt: it contains one standard
variable block and one concrete instruction at the end.

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo if different}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{path to kernel}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = {{actor id}}
WORKFLOW = {{workflow id}}
EXECUTION_MODE = {{mode id}}
OUTPUT_CONTRACT = {{output id}}
OPTIONAL_SKILL = {{skill.<id> | none}}
HYDRATION_LEVEL = {{minimal | compact | full/debug}}
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1-3 lines; do not restate the issue, PR, bodies, comments, acceptance criteria, source basis, or checklists}}
OUT_OF_SCOPE = {{plausible mistakes to avoid}}
EVIDENCE_REQUIRED = {{required evidence ids}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none with reason}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{brief reason}}

{{One concrete instruction: re-resolve the kernel, read the required live evidence, and verify PM delivery, PM_AUTHORIZATION_STATUS, and the exact repository, workflow, mode, branch, and scope match; fail closed for a draft, missing delivery, `pending`, or absent, unknown, or inferred values, and implement, review, audit, or draft only the scoped work.}}
```

When drafting, read the live issue or PR and its comments, then reference that
detail instead of copying it. Do not add headings, sections, lists, checklists,
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
