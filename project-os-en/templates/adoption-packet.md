# Adoption package

Responsibility: report an audit or draft of target adoption, separating browser
readiness from terminal readiness. It is draft-only: it never proves an
already-executed mutation; that evidence lives in `output.execution_report`. It
stores no live state and grants no permission.

```markdown
## Target repository

{{Target repository and PM-facing language.}}

## Kernel version

{{Declared version or tracks latest.}}

## Roadmap state

{{roadmap_state: present <verified owner/repo#N> | missing. When missing, do not
invent a number or fill {{#ROADMAP_ISSUE}} with durable placeholders.}}

## Browser adoption state

{{browser_adoption_state: ready | drift | missing. The browser adapter is
PM-applied and need not exist as a repo file.}}

## Terminal adoption state

{{terminal_adoption_state: ready | drift | missing | blocked_on_roadmap.}}

## Browser adapter draft

{{Complete PM-applicable BROWSER_CHAT.md draft, or a note that it is already up
to date. Do not paste secrets or live state.}}

## Terminal adapter findings

{{Drift, missing files, or target-owned notes for AGENTS.md/CLAUDE.md/GEMINI.md;
routes and summary, no secrets.}}

## Route prompt state

{{route_prompt_state: not_needed | blocked_on_roadmap | blocked_on_work_unit |
drafted. A write-capable route prompt requires a live roadmap and a live work
unit; neither is ever invented.}}

## Manual PM actions

- {{What the PM applies or delivers by hand: paste the browser adapter, create
  the roadmap with the bundle, deliver the route prompt.}}

## Agent actions

- {{What a terminal agent would execute only under a delivered route prompt with
  exact approval; the draft itself authorizes nothing.}}

## Target-owned constraints

{{Product, domain, build, validation, and constraints that remain in the target.}}

## Validation

- {{PM/agent validation and verification.}}

## Rollback

{{Restore previous adapters or revert the PR.}}
```
