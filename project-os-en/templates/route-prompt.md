# Route prompt

Responsibility: route scoped work to another surface without pasting the full
issue or granting permission.

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
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1-3 lines, not the full issue body}}
OUT_OF_SCOPE = {{plausible mistakes to avoid}}
EVIDENCE_REQUIRED = {{required evidence ids}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none with reason}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
recommended_effort: {{medium|high|xhigh}} - {{brief reason}}

{{Concrete instruction: implement, review, audit, or draft only the scoped work.}}
```

The receiving agent re-resolves the kernel, reads live evidence, and fails closed
when context, authority, or validation is missing. Browser chat infers
`RECOMMENDED_TERMINAL_AGENT_FAMILY` as non-binding advice: Codex for code
implementation, Python tooling, migrations, refactors, and tests; Claude for
document synthesis, architecture review, or long-context prose; Gemini for
multimodal work or the Google ecosystem when it has a clear advantage; and
`none` when there is no meaningful advantage or evidence is insufficient.
Explicit PM feedback may override that recommendation. `OPTIONAL_SKILL` and
the recommended family do not grant permission, replace exact PM approval, or
force a tool.

This prompt does not authorize writing.
