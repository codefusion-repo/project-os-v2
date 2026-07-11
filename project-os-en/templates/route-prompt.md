# Route prompt

```text
PROJECT_NAME = {{name}}
REPOSITORY_NAME = {{org/repo}}
TARGET_REPOSITORY = {{org/repo when different}}
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = {{path to kernel}}
ISSUE_OR_PR = {{#N}}
TARGET_ACTOR_TYPE = {{actor id}}
WORKFLOW = {{workflow id}}
EXECUTION_MODE = {{mode id}}
OUTPUT_CONTRACT = {{output id}}
OPTIONAL_SKILL = {{skill.<id> | none}}
RECOMMENDED_TERMINAL_AGENT_FAMILY = {{Codex | Claude | Gemini | none}}
SCOPE = {{1–3 lines, not the full issue body}}
OUT_OF_SCOPE = {{plausible mistakes to avoid}}
EVIDENCE_REQUIRED = {{required evidence ids}}
VALIDATION_REQUIRED = {{agent-run | PM-run | manual PM | none with reason}}
BRANCH_NAME = work/{{issue}}-{{slug}}
PM_AUTHORIZATION_STATUS = {{pending | granted for this exact scope and mode}}
{{Concrete instruction: implement, review, audit, or draft only the scoped work.}}
```
