# ADR 0003 - Project OS CLI deferral and primary Spanish kernel sequencing

- Status: deferred by PM sequencing; not accepted for CLI implementation.
- Date: 2026-07-09
- Scope: issue #369 and PR #404; design-only decision for a future
  `project-os-cli` adoption model after required Project OS surface
  consolidation.
- Source basis: roadmap #274; issue #369; PR #404 review correction; downstream
  public-presentation issue #394; `docs/DESIGN.md`;
  `docs/GETTING_STARTED.md`; `docs/GITHUB_ACCESS.md`;
  `docs/PUBLIC_USAGE_MODEL.md`; current `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `adapters/*.target.md`, and MOSDLC operation templates.
- Non-authorization: this ADR grants no permission to implement a CLI, migrate
  project surfaces, move legacy files, rewrite adapters, translate Project OS,
  package Project OS, mutate target repositories, create API/bridge/OAuth/GitHub
  App behavior, change public release state, change resolver behavior, change
  kernel ids, change authorization semantics, or collect credentials.

## Context

Issue #369 asked Project OS to evaluate a future `project-os-cli` per-project
installation and onboarding model. The first PR #404 draft accepted an internal,
dogfood-first CLI direction too early. PM validation rejected that sequencing.

The PM sequencing decision is now stricter: Project OS must first consolidate
around `project-os-es` as the primary connected kernel surface, move legacy/root
surfaces aside, compact adapters on that new base, and only then translate the
compact connected version to English. CLI design and implementation come after
those prerequisites, and #394 public presentation/packaging comes after the CLI
question is re-evaluated from that cleaner base.

This ADR therefore resolves #369 as a deferral decision, not as approval to
implement or adopt a CLI now.

## Decision

`project-os-cli` is not accepted for implementation now.

The durable decision is:

- defer CLI/adoption implementation until Project OS has a consolidated
  `project-os-es` primary surface;
- make `project-os-es` completeness, connectivity, and resolver correctness the
  immediate prerequisite work;
- move legacy/root Project OS surfaces aside only in a later scoped migration
  issue, not in this PR;
- compact adapters after the `project-os-es`-derived base exists, using that
  base as the source for active adapter behavior;
- translate the compact connected surface to English before CLI/public
  presentation work;
- later design a CLI with language selection and CRUD support for editable
  Project OS entities;
- keep #394 public presentation and packaging downstream of this sequence.

No CLI path is accepted for immediate implementation by this ADR. No adapter
rewrite, migration, translation, resolver change, kernel id change, public
package, API/bridge, MCP, GPT action, OAuth/GitHub App, hosted service, release
automation, target-repo mutation, write-capable API, or authorization semantic
change is approved.

## PM Sequencing

The required sequence is exactly:

1. Audit whether project-os-es is complete and connected enough to become the primary kernel surface.
2. Test the Spanish resolver and confirm it resolves current workflows/entities correctly.
3. Migrate all legacy/root Project OS surfaces to a `legacy-project-os` folder.
4. Leave active root/new-version structure derived from what is currently inside project-os-es.
5. Create a follow-up issue to compact adapters using project-os-es as the base.
6. Translate the compact connected version to English.
7. Later design/implement CLI with language selection and CRUD for editable Project OS entities.
8. Then revisit #394 / public presentation and packaging.

This issue and PR perform none of those implementation steps. They only record
the sequencing decision and future design constraints.

## Alternatives Considered

| Option | Result | Reason |
| --- | --- | --- |
| Manual adapters only | Deferred as the long-term model | It remains the current fallback, but it does not solve drift or onboarding friction. |
| Canonical templates only, no CLI | Deferred | Useful after the `project-os-es` base exists, but not enough to decide before consolidation. |
| Global public CLI package now | Rejected now | Public packaging is premature before Spanish primary-surface consolidation, English translation, and #394 review. |
| Per-project private CLI dogfood now | Rejected now | It would build adoption tooling on an unstable surface before the PM-approved `project-os-es` migration sequence. |
| Hosted/API/bridge onboarding | Deferred | It remains downstream of kernel/operations quality and must not replace the local kernel/GitHub source-of-truth model. |
| Deferral plus project-os-es-first sequencing | Selected decision | It resolves #369 by preventing premature CLI approval and establishing the prerequisite follow-up sequence. |

## What Belongs Where

### Adapters

Future compact adapters should contain only the smallest durable information
needed to boot an agent on a specific surface:

- repository identity: project name, repository name, repository local path,
  default branch, work branch pattern, PM-facing language, and target type when
  useful;
- Project OS reference: `KERNEL_REPOSITORY`, `KERNEL_LOCAL_PATH`, and a
  version/adoption policy field;
- kernel-resolution instruction: follow `kernel/manifest.json` and, for terminal
  surfaces, use the resolver fast path when available;
- live-state instruction: read GitHub and git at task time, not memory or
  durable notes;
- short target-owned notes: stable build commands, validation commands,
  protected paths, domain constraints, security constraints, PM-facing language,
  and target-specific escalation notes.

Adapter compaction should happen after the active root/new-version structure is
derived from `project-os-es`, and before or alongside later English/CLI work. It
should not be coupled to a first CLI prototype.

### Kernel, Resolver, Docs, And Templates

These layers continue to own generic behavior and reusable shape:

- `kernel/*.json`: actors, workflows, execution modes, evidence, outputs,
  boundaries, statuses, resolution strategy, and non-authorization rules;
- resolver tooling: deterministic acceleration of manifest resolution, never a
  source of truth and never a permission grant;
- traceability, validation, and context-economy docs: detailed generic policies;
- templates: canonical route, command-bundle, operation, and adapter shapes.

The immediate prerequisite is to prove that the Spanish resolver and
`project-os-es` surface resolve current workflows/entities correctly before
moving root surfaces or redesigning adoption tooling.

### Never Duplicate In Adapters

Adapters must never duplicate or store:

- live issue, PR, branch, commit, review, CI, validation, roadmap status, release
  readiness, or planning state;
- kernel behavior definitions such as full boundary text, output contracts,
  evidence definitions, status semantics, workflow steps, or mode permission
  matrices;
- MOSDLC operation catalogs or operation bodies;
- traceability, validation, or context-economy policy details beyond compact
  pointers;
- secrets, secret-looking examples, tokens, cookies, `.env` values, database
  URLs, JWTs, private keys, OAuth/client secrets, CI secrets, payment keys, or
  production credentials;
- GitHub auth material, credential setup state, or generated tokens.

## Surface References To The Private Kernel

Until the PM-approved migration sequence is implemented in later issues, current
surface references remain descriptive design guidance only.

Future `AGENTS.md` should remain the primary terminal-agent adapter. It should
reference the private kernel with explicit metadata:

- `KERNEL_REPOSITORY` naming the private Project OS repository;
- `KERNEL_LOCAL_PATH` pointing to the local kernel directory used on that
  machine;
- `KERNEL_VERSION_ADOPTED` as a policy field, not live state.

Future `CLAUDE.md` and `GEMINI.md` should remain surface-specific shims that
point to `AGENTS.md` and the same kernel reference instead of restating
behavior.

Browser-chat instructions should say they cannot run the terminal resolver. They
should resolve by reading the manifest and referenced kernel files from the
Project OS repository when available. If the browser-chat surface cannot read
the private kernel or target evidence, it must return `status.needs_context` and
name the missing source.

No adapter should imply that a private kernel reference grants repository write
permission. Resolution shapes behavior; PM approval and live evidence authorize
only the specific operation.

## Future CLI Design Constraints

The later CLI design may evaluate:

- target adoption and verification commands;
- adapter rendering and compact-adapter upgrades;
- kernel path discovery and version-policy checks;
- operation wizard exposure;
- redacted GitHub CLI readiness checks;
- rollback guidance for generated adoption artifacts;
- language selection so Spanish and English surfaces can be chosen explicitly;
- CRUD for editable Project OS entities, where appropriate, including
  boundaries, habilidades, reglas_operativas, workflows, outputs, evidence, and
  statuses.

CRUD support is future-only and must be designed conservatively. Any editable
entity support must include schema validation, safe diffs before writes,
redaction, no secret collection, no direct authorization bypass, no hidden
workflow engine, no write-capable API by implication, and no kernel id or
authorization semantic changes without separate PM approval.

The CLI should prefer referencing the kernel over copying it. Vendoring a full
kernel into every target remains a drift risk and should not be the default.

## Operation Wizard Exposure

A future operation wizard should be exposed as a guided selector over existing
MOSDLC operation templates and flow docs, not an execution engine.

The wizard may ask:

- whether the user is adopting, planning, implementing, reviewing, validating,
  deploying, maintaining, or handing off;
- whether the acting surface is human PM, browser chat, or terminal agent;
- which repository and issue/PR are in scope;
- whether the user needs a draft, route prompt, review, validation plan, or
  PM-run command bundle.

The wizard should output the next operation template path, required variables,
required live evidence, and safe next step. It should not mutate GitHub or run
terminal-agent implementation work unless a later scoped issue explicitly
implements such behavior under existing kernel gates.

## Safe GitHub Setup Support

A future CLI may safely support GitHub setup by detecting and explaining
existing local tooling:

- detect whether `gh` is installed;
- run `gh auth status` only when the user asks for the check or a later approved
  design allows a safe explicit flag;
- report account, host, repository, and scope category without printing tokens;
- verify read access to Project OS and target repositories;
- verify that the current git remote matches the target repository;
- explain how the human can run `gh auth login` or grant least-privilege access.

The CLI must not collect tokens, create OAuth apps, create GitHub Apps, store
credentials, request organization-wide access by default, mutate repository
settings, create secrets, rotate secrets, or implement write-capable GitHub auth.
Any future write integration beyond normal local `git`/`gh` use requires a
separate security design and PM approval.

## CLI Versus Future API/Bridge

CLI can only be reconsidered after the PM sequencing prerequisites. If later
approved, it may solve local adoption, adapter generation, kernel path
verification, operation selection, and safe local GitHub readiness checks.

API/bridge remains deferred. It is needed only if future evidence shows a model
client needs remote kernel resolution, live evidence packets, or operation
discovery without local checkout access. A first bridge, if ever approved,
should be read-only and should consume the kernel and GitHub evidence rather
than duplicate them.

Deferred to future API/bridge or #394:

- public package positioning and release channel;
- hosted service or remote runner;
- OAuth, GitHub App, MCP, GPT action, or marketplace integration;
- write-capable API;
- public docs/marketing language;
- comparison with external agent frameworks;
- public support, licensing, and security review.

## Recommended Follow-Up Issues

1. Audit `project-os-es` completeness/connectivity as the primary kernel
   surface.
2. Validate Spanish resolver completeness and current workflow/entity
   resolution.
3. Migrate legacy/root Project OS surfaces to `legacy-project-os`.
4. Compact adapters on the new `project-os-es`-derived base.
5. Translate the compact connected surface to English.
6. Design CLI v2 with language selection and CRUD for editable Project OS
   entities.
7. Revisit #394 public presentation and packaging after those prerequisites.

## PM Decisions Required Before Implementation

- Whether the audit proves `project-os-es` is complete and connected enough to
  become the primary kernel surface.
- What Spanish resolver validation is sufficient before root migration.
- Exact migration scope and rollback plan for moving legacy/root surfaces aside.
- Final active root/new-version structure derived from `project-os-es`.
- Adapter compaction standard on the new base.
- English translation acceptance criteria.
- Future CLI implementation language, distribution shape, language-selection
  model, and editable-entity CRUD boundary.
- Whether any future GitHub status check may call `gh auth status`
  automatically or only after an explicit user flag.

## Consequences

This decision prevents premature CLI adoption and makes `project-os-es`-first
consolidation the next architectural priority. It preserves the kernel as the
source of generic behavior, GitHub as live state, and target repositories as the
source of target-specific facts.

Issue #394 must wait. It should later consume the output of this sequence,
including the compact Spanish primary surface, English translation, and any
later CLI design, instead of using this ADR as evidence that public CLI
packaging or adoption tooling is approved.

Rollback is deleting this ADR. No runtime, migration, adapter rewrite,
translation, CLI, CRUD command, package, API, bridge, target repo, credential,
GitHub auth, public release, resolver behavior, kernel id, or authorization
semantic state changes as a result of this design-only correction.
