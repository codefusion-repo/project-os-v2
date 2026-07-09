# Proportional Validation Policy

Project OS uses proportional validation everywhere: kernel repository work,
agent route prompts, operation templates, reviews, target repositories, and
target adoption. Validation is evidence for the scoped risk, not a default
ritual.

This policy operationalizes `boundary.validation_discipline`.

## Global Rule

Agents run only the validation needed for the change and risk level. They do
not create or run broad tests by default for every docs change, prompt change,
template change, MOSDLC phase, target-repository change, or Project OS adoption
update.

If useful validation exists but should remain PM-executed, the agent drafts
copy-safe PM-run commands instead of running them. If acceptance depends on
human judgment, the agent reports manual PM validation instead of pretending an
automated check proves it.

## Validation Categories

Use one or more categories in route prompts, issue validation expectations,
execution reports, and review-before-close.

- **Agent-run required validation**: the agent runs scoped commands when the
  change touches deterministic or high-risk behavior.
- **PM-run drafted validation commands**: the agent drafts commands for the PM
  when validation is useful but requires PM timing, credentials, external
  services, paid resources, deployment context, production access, or hardware.
- **Manual PM validation or checklist**: the agent names the human check when
  acceptance depends on docs clarity, prompt copy, wizard wording, onboarding
  clarity, product judgment, UX feel, public-facing messaging, or content
  organization.
- **No automated validation needed**: allowed only when the change has no
  deterministic behavior or safety contract to check; the agent must say why.

## Mandatory Agent-Run Validation

Mandatory validation stays required for changes that touch:

- kernel JSON or kernel reference contracts;
- resolver or tooling behavior;
- command-bundle safety;
- traceability protocol behavior;
- authorization, write boundaries, branch gates, or review-before-close;
- security, privacy, secret handling, redaction, or logging risk;
- deployment, external services, environment readiness, or production-impacting
  behavior;
- data migrations, billing, storage, auth, payments, or production logic;
- deterministic workflow, output, evidence, adapter-audit, or route-prompt
  contracts.

For kernel JSON changes, run `python3 -m tools.validate_kernel`. For changed
deterministic contracts, run the smallest targeted tests that protect that
contract. Run a full suite only when shared kernel/tooling or broad test-suite
changes make the targeted evidence insufficient.

## Tests

Add or update automated tests only when they protect deterministic behavior,
regression risk, security/privacy boundaries, protocol contracts,
billing/storage logic, routing, stable UI state contracts, command safety,
resolver behavior, adapter adoption, or review/traceability contracts.

Do not add tests merely because a new phase, prompt, template, docs page, or
target project changed. Do not keep broad, duplicated, brittle,
implementation-detail, or confidence-theater tests. Remove, merge, or narrow
such tests when they are encountered inside the scoped issue.

## Target Repositories

Target repositories own their product, domain, runtime, build, deployment, and
validation truth. Project OS adapters may preserve target-owned validation
commands, but they must not impose Project OS-specific test suites or require
new target tests unless the target issue risk justifies them.

## Review Before Close

Review-before-close compares validation evidence against the linked issue's
scoped validation expectations and this policy. A review may accept scoped
PM-run command output, manual PM validation, or a justified no-automated-check
exception when broad agent-run validation was intentionally out of scope.

Review still fails closed when required deterministic, security, authorization,
traceability, deployment, secret-sensitive, kernel, resolver, or
production-impacting validation is missing or failed.
