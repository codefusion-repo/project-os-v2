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

{{roadmap_state: present <verified owner/repo#N> | missing. The roadmap is
optional live evidence, never an adoption prerequisite. When missing, do not
invent a number or store one as durable adapter configuration.}}

## Browser adoption state

{{browser_adoption_state: ready | drift | missing. The browser adapter is
PM-applied and need not exist as a repo file.}}

## Terminal adoption state

{{terminal_adoption_state: ready | drift | missing.}}

## Browser adapter draft

{{Complete PM-applicable BROWSER_CHAT.md draft, or a note that it is already up
to date. Do not paste secrets or live state.}}

## Terminal adapter findings

{{Drift, missing files, or target-owned notes for AGENTS.md/CLAUDE.md/GEMINI.md;
routes and summary, no secrets.}}

## Route prompt state

{{route_prompt_state: not_needed | blocked_on_target_scope | drafted. A
write-capable route prompt requires the live unit bounded by target, adapter
scope, and branch, plus branch preflight, validation, and exact PM approval on
delivery; it requires no prior roadmap or issue and never invents the scope.}}

## Manual PM actions

- {{What the PM applies or delivers by hand: paste the browser adapter, deliver
  the route prompt, and create the roadmap with the bundle if they choose to.}}

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
