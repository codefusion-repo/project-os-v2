# ADR 0003 - Project OS CLI adoption model and minimal adapters

- Status: accepted
- Date: 2026-07-09
- Scope: issue #369; design-only decision for a future `project-os-cli`
  adoption model.
- Source basis: roadmap #274; issue #369; downstream public-presentation issue
  #394; `docs/DESIGN.md`; `docs/GETTING_STARTED.md`;
  `docs/GITHUB_ACCESS.md`; `docs/PUBLIC_USAGE_MODEL.md`; current
  `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `adapters/*.target.md`, and MOSDLC
  operation templates.
- Non-authorization: this ADR grants no permission to implement a CLI, package
  Project OS, mutate target repositories, create API/bridge/OAuth/GitHub App
  behavior, change public release state, or collect credentials.

## Context

Project OS currently adopts a repository through compact adapters such as
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and browser-chat instructions. Those
adapters bootstrap an agent into the Project OS kernel and target repository
evidence. They are useful, but manual copying creates drift risk: adapters can
grow into duplicated kernel behavior, target repos can carry stale route
instructions, and new users must learn the kernel, operations, GitHub access,
and per-surface adapter rules at the same time.

Roadmap #274 makes kernel and MOSDLC operation quality the immediate priority.
It also defers bridge/API and public packaging until internal dogfood proves the
kernel and operation catalog are stable. Issue #369 asks whether a
per-project `project-os-cli` adoption model should exist and how it should
generate, update, and keep adapters as kernel-resolving bootloaders. Issue #394
is downstream: it should consume this decision when evaluating public
presentation and packaging, not run in parallel or absorb this scope.

## Decision

Project OS should move toward an internal, dogfood-first per-project adoption
CLI, but not a public package or hosted integration yet.

The primary model is:

- a local `project-os` command, run from a target repository or pointed at one;
- installed or invoked from the private Project OS checkout during dogfood;
- responsible for `init`/`adopt`/`verify`/`upgrade`/`doctor`/`operations` style
  adoption workflows;
- responsible for rendering canonical minimal adapters from templates and
  target metadata;
- not responsible for replacing kernel resolution, storing live state, running
  a hidden workflow engine, or implementing GitHub auth.

Adapters should become minimal bootloaders. Adapter minimization should be
designed as part of CLI design, then implemented before or with the first CLI
prototype so the CLI has canonical templates to render. The current manual
adapter model can remain until that follow-up exists; this ADR does not rewrite
adapters.

The CLI should reference a private Project OS kernel checkout during internal
use. It should not vendor the kernel into every target repository by default.
It should not copy kernel JSON into adapters. It may optionally support a
read-only local cache of the Project OS repository later, but the source of
truth remains the Project OS repository plus `kernel/manifest.json`.

## Adoption Timing

Recommended timing: **later, as the next internal dogfood implementation path
after this decision and adapter-template minimization**.

Do not public-package the CLI now. The internal CLI should exist to reduce
manual adoption friction and validate Project OS against real targets. Public
installation, public docs positioning, package registry release, API/bridge,
MCP, GPT action, OAuth app, GitHub App, or hosted service work must wait for
separate issues and PM approval.

## Alternatives Considered

| Option | Result | Reason |
| --- | --- | --- |
| Manual adapters only | Rejected as primary path | Lowest implementation cost, but it preserves drift and onboarding friction. It is acceptable as a fallback. |
| Canonical templates only, no CLI | Rejected as primary path | Better than manual free-form adapters, but still makes users copy, fill, verify, and upgrade by hand. |
| Global public CLI package now | Rejected for now | Premature public packaging creates support, security, and versioning burden before internal dogfood stabilizes adoption. |
| Per-project private CLI dogfood | Accepted | Best fit for current roadmap: improves adoption while preserving private-kernel, GitHub-native, no-hidden-engine boundaries. |
| Hosted/API/bridge onboarding | Deferred | Useful only after kernel and operations quality are proven; not needed to solve adapter drift. |

## What Belongs Where

### Adapters

Adapters should contain only the smallest durable information needed to boot an
agent on a specific surface:

- repository identity: project name, repository name, repository local path,
  default branch, work branch pattern, PM-facing language, and target type when
  useful;
- Project OS reference: `KERNEL_REPOSITORY`, `KERNEL_LOCAL_PATH`, and an
  adoption/version policy such as a tag, branch, or "tracks latest" for
  internal dogfood;
- kernel-resolution instruction: follow `kernel/manifest.json` and, for terminal
  surfaces, use the resolver fast path when available;
- live-state instruction: read GitHub and git at task time, not memory or
  durable notes;
- short target-owned notes: stable build commands, validation commands,
  protected paths, domain constraints, security constraints, PM-facing language,
  and target-specific escalation notes.

### Kernel, Resolver, Docs, And Templates

These layers own generic behavior and reusable shape:

- `kernel/*.json`: actors, workflows, execution modes, evidence, outputs,
  boundaries, statuses, resolution strategy, and non-authorization rules;
- `tools.project_os_resolve`: terminal-only deterministic acceleration of
  manifest resolution, never a source of truth and never a permission grant;
- `docs/TRACEABILITY_PROTOCOL.md`, `docs/VALIDATION_POLICY.md`, and
  `docs/CONTEXT_ECONOMY.md`: detailed generic policies;
- `templates/`: canonical route, command-bundle, operation, and adapter shapes;
- future CLI templates: render minimal adapters from canonical templates and a
  target metadata file instead of hand-maintained prose.

### Never Duplicate In Adapters

Adapters must never duplicate or store:

- live issue, PR, branch, commit, review, CI, validation, roadmap status, release
  readiness, or planning state;
- kernel behavior definitions such as full boundary text, output contracts,
  evidence definitions, status semantics, workflow steps, or mode permission
  matrices;
- MOSDLC operation catalogs or operation bodies;
- `docs/VALIDATION_POLICY.md`, `docs/TRACEABILITY_PROTOCOL.md`, or
  `docs/CONTEXT_ECONOMY.md` details beyond compact pointers;
- secrets, secret-looking examples, tokens, cookies, `.env` values, database
  URLs, JWTs, private keys, OAuth/client secrets, CI secrets, payment keys, or
  production credentials;
- GitHub auth material, credential setup state, or generated tokens.

## Surface References To The Private Kernel

`AGENTS.md` should be the primary terminal-agent adapter. It should reference
the private kernel with explicit metadata:

- `KERNEL_REPOSITORY` naming the private Project OS repository, currently
  `codefusion-repo/project-os-v2`;
- `KERNEL_LOCAL_PATH` pointing to the local kernel directory used on that
  machine;
- `KERNEL_VERSION_ADOPTED` as a policy field, not live state.

`CLAUDE.md` and `GEMINI.md` should remain surface-specific shims that point to
`AGENTS.md` and the same kernel reference instead of restating behavior.

Browser-chat instructions should say they cannot run the terminal resolver.
They should resolve by reading `kernel/manifest.json` and the referenced kernel
files from the Project OS repository when available. If the browser-chat surface
cannot read the private kernel or target evidence, it must return
`status.needs_context` and name the missing source.

No adapter should imply that a private kernel reference grants repository write
permission. Resolution shapes behavior; PM approval and live evidence authorize
only the specific operation.

## Kernel Location, Install, And Update Model

The CLI should support this internal sequence:

1. Discover an existing Project OS checkout through explicit flags first:
   `--kernel-dir`, `--project-os-dir`, or a target metadata file created by a
   prior adoption.
2. If no explicit path is provided, check conservative local defaults such as a
   sibling/private CodeFusion checkout path. Discovery must be explainable and
   must fail closed when ambiguous.
3. For internal dogfood, offer to clone or update the private Project OS
   repository only with explicit PM/user confirmation. The CLI must not hide git
   network operations or silently switch versions.
4. Store only non-secret adoption metadata in the target, for example an
   adoption metadata file under a `.project-os` directory, if a future
   implementation issue approves that file. It may include repository names,
   local relative references where safe, selected surfaces, target type,
   PM-facing language, default branch, roadmap issue, adapter template version,
   and kernel version policy. It must not store tokens or live issue/PR state.
5. `project-os upgrade` should update the private Project OS checkout only when
   requested, then re-render adapters from templates and show a diff before
   writing. It should preserve target-owned note blocks.
6. `project-os verify` should confirm that adapters point to a readable kernel,
   the manifest validates, the selected surfaces exist, GitHub evidence can be
   read when configured, and no adapter contains forbidden duplicated live state
   or secret-looking values.

The CLI should prefer referencing the kernel over copying it. Vendoring a full
kernel into every target creates fork and drift risk. A future pinned-cache mode
may be considered only if internal dogfood shows offline or cross-machine
adoption cannot work otherwise.

## Proposed Commands

- `project-os init`: create Project OS metadata for a new target repository and
  render initial adapters.
- `project-os adopt`: adopt an existing target repository, ask the adoption
  questions, and render minimal adapters.
- `project-os verify`: validate target adoption, kernel readability, adapter
  minimality, and GitHub evidence access where configured.
- `project-os upgrade`: update/re-render adapters from canonical templates and
  optionally update the local Project OS checkout after explicit confirmation.
- `project-os doctor`: diagnose missing kernel paths, unreadable GitHub sources,
  stale adapters, invalid metadata, or unsafe duplicated content.
- `project-os operations`: expose the MOSDLC operation wizard and recommend the
  next operation from repository state and user intent, without becoming a
  hidden workflow engine.
- `project-os github status`: detect `gh`, report authenticated account and
  repository access in redacted form, and explain missing access.
- `project-os rollback`: restore prior adapter versions from a local backup or
  print a clear manual rollback plan. This is safer than `uninstall` as the
  first implementation target.

## Adoption Questions

The installer should ask only durable, non-secret questions:

- project name and target repository name;
- target repository local path;
- default branch and work branch pattern;
- PM-facing language;
- target type, such as product, library, infrastructure, or Project OS itself;
- canonical roadmap issue, if one already exists;
- selected agent surfaces: terminal `AGENTS.md`, Claude, Gemini, browser chat;
- whether GitHub is available, and whether the user wants `gh` detection;
- Project OS kernel path, repository, and version policy.

The installer must not ask for tokens, `.env` values, production credentials,
OAuth/client secrets, database URLs, cookies, JWTs, or CI secrets.

## Operation Wizard Exposure

The operation wizard should be exposed through `project-os operations`. It
should be a guided selector over existing MOSDLC operation templates and flow
docs, not an execution engine.

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

The CLI may safely support GitHub setup by detecting and explaining existing
local tooling:

- detect whether `gh` is installed;
- run `gh auth status` only when the user asks for the check;
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

CLI can solve:

- local target adoption;
- adapter generation and update;
- kernel path discovery and verification;
- MOSDLC operation selection;
- redacted GitHub CLI readiness checks;
- internal dogfood feedback collection through normal GitHub issues.

API/bridge is still needed only if future evidence shows a model client needs
remote kernel resolution, live evidence packets, or operation discovery without
local checkout access. A first bridge, if ever approved, should be read-only and
should consume the kernel and GitHub evidence rather than duplicate them.

Deferred to future API/bridge or #394:

- public package positioning and release channel;
- hosted service or remote runner;
- OAuth, GitHub App, MCP, GPT action, or marketplace integration;
- write-capable API;
- public docs/marketing language;
- comparison with external agent frameworks;
- public support, licensing, and security review.

## Recommended Follow-Up Issues

1. Adapter minimization implementation: create canonical minimal adapter
   templates and a target-owned note preservation strategy.
2. Internal CLI prototype: implement `project-os adopt`, `verify`, `doctor`, and
   adapter rendering against the minimized templates, with no public packaging.
3. CLI operations wizard prototype: expose operation selection over current
   MOSDLC templates without creating a hidden workflow engine.
4. GitHub setup safety design: define exactly what `project-os github status`
   may inspect and how it redacts output before any implementation.
5. #394 public presentation: consume this ADR after MOSDLC compact surfaces,
   English translation, legacy cleanup, dogfood results, and public-readiness
   review are strong enough.

## PM Decisions Required Before Implementation

- Whether the first CLI is a Python script/module in this repository, a separate
  private package, or another internal distribution shape.
- Whether target metadata such as an adoption file under `.project-os` is
  approved, and which fields it may store.
- Whether the kernel version policy for internal targets is "tracks latest",
  branch-based, tag-based, or pinned to a commit/tag.
- Which adapter surfaces are required for the first prototype.
- Whether `project-os upgrade` may run git fetch/pull on the private Project OS
  checkout or only report the required command for the PM.
- Whether `project-os github status` may call `gh auth status` automatically or
  only after an explicit user flag.
- Which target repository should be the first dogfood adoption target.

## Consequences

This decision reduces adapter drift by making the CLI responsible for rendering
and verifying minimal bootloaders from canonical templates. It preserves the
kernel as the source of generic behavior, GitHub as live state, and target repos
as the source of target-specific facts.

It also constrains sequencing: #394 should wait for this ADR and later consume
its recommendation as the CLI/adoption input to public presentation. #394 should
not infer that public CLI packaging, API/bridge, OAuth/GitHub App, MCP, GPT
action, hosted service, or release automation exists or is approved.

Rollback is deleting this ADR. No runtime, package, API, bridge, target repo,
credential, GitHub auth, public release, or adapter rewrite state changes as a
result of this design-only issue.
