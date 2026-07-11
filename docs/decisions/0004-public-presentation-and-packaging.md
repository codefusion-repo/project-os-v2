# ADR 0004 - Project OS public presentation and packaging path

- Status: proposed; pending PM review for positioning, completeness, sources,
  language and absence of overclaiming. It becomes accepted only by explicit
  PM decision.
- Date: 2026-07-11
- Scope: issue #394; design-only decision on how Project OS should be
  presented, packaged and eventually published. No packaging, CLI, API,
  publication, tag or release is implemented by this ADR.
- Source basis: roadmap #274; issue #394 and its PM comment of 2026-07-11;
  ADR 0003 (`docs/decisions/0003-project-os-cli-adoption-model.md`); closed
  prerequisites #393, #377, #389, #390, #391 (compact Spanish surfaces), #409
  (English surface), #405/#407 (legacy migration and adapter compaction);
  deferred CLI design #369; current `README.md`, `project-os-es/` and
  `project-os-en/` surfaces and adapters; official documentation for OpenAI
  Agents SDK, LangGraph, Deep Agents and AutoGen as cited inline.
- Non-authorization: this ADR grants no permission to publish the repository,
  change its visibility, create tags or releases, implement a CLI, API/bridge,
  MCP tool, GPT action, OAuth/GitHub App, hosted service or marketplace
  listing, modify kernel ids, resolver behavior, authorization semantics,
  operations, templates or adapters, or collect credentials. Each of those
  requires its own scoped issue and exact PM approval.

## Context

Project OS now has the base that ADR 0003 required before this decision could
be evaluated honestly: `project-os-es` is the consolidated primary surface
(#405), adapters are compacted on that base (#407), the compact Spanish
surfaces are done (#377, #389, #390, #391), the English parallel surface
exists (#409), and the accepted MOSDLC operation templates are in place
(#393). The remaining prerequisite named by #394 that is **not** done is a
dedicated security/secrets/public-readiness review. ADR 0003 placed CLI design
(#369 follow-up) before revisiting #394; the PM authorization for this issue
supersedes that ordering for the decision itself, and this ADR keeps the CLI
deferred, so no CLI dependency is created.

Issue #394 asks which of eight presentation/packaging paths fits Project OS as
it actually exists: a human-directed, GitHub-native operating layer for
AI-assisted development — kernel contracts, MOSDLC operations, evidence,
proportional validation, PM decisions and traceability — not a runtime, not an
autonomous agent, not a workflow engine.

The PM comment on #394 adds constraints this ADR incorporates: position
Project OS as a human-directed operating system for building products with AI
agents; distinguish learner/"vibe coding" and experienced-team audiences
without ridiculing either; recommend a reproducible context/token benchmark
instead of unverified savings claims; avoid unverified subscription-price
claims; evaluate tutorial/onboarding and images as follow-up work that
improves the existing quick start rather than duplicating it; and keep tags,
packages and releases out of this issue.

## Decision

Adopt a **staged path** whose first public form is a **docs-first public
reference with GitHub-native operating-layer positioning** (options 2 + 3
below, with option 1 as the publishing mechanism and option 4 as the existing
copy-based adoption mechanism). Everything execution-shaped — CLI, API/bridge,
GPT/MCP/action packaging — stays deferred. "Internal-only" is the correct
*current* state but is not recommended as the end state: the repository stays
private until the Stage 0 gate below passes **and** the PM approves publication
exactly. Passing the gate does not itself publish anything, and the PM may
still decide against publication at that point.

### Stages

- **Stage 0 — Public-readiness gate (required, not yet done).** A scoped
  security/secrets/licensing/public-readiness review of the full tree and
  history-exposure posture. Nothing is published before this passes and the PM
  approves publication exactly.
- **Stage 1 — Docs-first public reference.** Publish the repository as-is in
  mechanism (public GitHub repo, manual copy-based adoption of
  `project-os-es/adapters/*.target.md` and `project-os-en/`), with a polished
  bilingual README, the messaging in this ADR, an improved quick
  start/tutorial building on `project-os-es/docs/empezar.md`, approved images
  where they reduce real friction, and the reproducible context benchmark
  published with dates and tooling declared. No installer, no API, no new tag
  required to be public. Internal tags already exist (the `project-os-lab-v*`
  series, latest `project-os-lab-v0.3.0`, plus dogfood baseline tags); the
  first *public release* tag is a separate release-readiness issue.
- **Stage 2 — Validate with users, then reconsider tooling.** Only after
  Stage 1 evidence (adoption friction reports, questions, dogfood on real
  targets) reopen, in this order and each as its own design issue: CLI
  onboarding (per ADR 0003 constraints), read-only API/bridge (per #274),
  GPT/MCP/action packaging. None is approved by this ADR.

### Positioning rule

Project OS presents itself as a **human-directed operating system / operating
layer for building software with AI agents**, anchored in concrete GitHub
workflows: issues, PRs, evidence, validation, review-before-close, decisions.
The word "harness" may be used only with an explicit qualifier such as
"process harness" or "operating layer", never bare: LangChain's Deep Agents
already uses "agent harness" for a **runtime** wrapper (tool loop, planning,
subagents), which is exactly what Project OS is not. "PM simulator" is not
adopted as positioning: it undersells the traceability/QA value and risks
implying that product, engineering, QA or security judgment is replaced.

### Messaging candidates (for PM review, Stage 1 finalizes wording)

- **One-line pitch (ES):** «Project OS es un sistema operativo humano-dirigido
  para construir productos reales con agentes de IA, preservando contexto,
  calidad, trazabilidad y control.»
- **One-line pitch (EN):** "Project OS is a human-directed operating system
  for building real products with AI agents, preserving context, quality,
  traceability and control."
- **Short README pitch:** "A compact, portable operating kernel that tells any
  AI agent *how to behave* on your project — actors, modes, workflows,
  boundaries, evidence, outputs and statuses — while all live project state
  stays in GitHub. Any agent can resume a project cold by resolving the kernel
  and reading GitHub; nothing depends on one chat's memory." (This is the
  existing root README opening, kept as the canonical base.)
- **What it is:** an editable, open, bilingual (ES default / EN explicit) set
  of kernel JSON contracts, MOSDLC operation prompts, templates, adapters and
  docs that structure AI-assisted development around scoped issues, exact PM
  approval, branch preflight, proportional validation, review-before-close,
  secret safety and GitHub-native traceability.
- **What it is not:** not an automatic coding agent; not a hosted runner or
  runtime; not a workflow engine; not a write-capable API; not an Operations
  Console; not a replacement for OpenAI Agents SDK, LangGraph/Deep Agents,
  AutoGen/Microsoft Agent Framework, Claude Code, Codex or GitHub. It is the
  process layer those tools operate under.

## Options evaluated

1. **Public repository only.** Lowest cost; but with no curated entry path the
   kernel/operations model is hard to grasp; high abandonment risk. Subsumed
   into Stage 1 as the mechanism, not the presentation.
2. **Docs-first public reference.** Polished README, quickstart, lifecycle
   guide, examples, benchmark. Highest value-to-cost ratio today: the compact
   ES/EN surfaces and existing docs (`empezar.md`, `reglas.md`, `ritmo.md`,
   `operaciones/README.md`) mean this is an improvement pass, not new
   infrastructure. Activation risk is real but is exactly what Stage 2
   validates. **Selected for Stage 1.**
3. **GitHub-native agent harness positioning.** Correct as *positioning* —
   Project OS's differentiation is precisely the operating/process layer — but
   the bare word "harness" now collides with Deep Agents' runtime usage.
   **Selected as positioning with the qualifier rule above.**
4. **Template/adapters package.** Copy-based adapter adoption already exists
   and stays the mechanism. A versioned *package* (registry artifact) adds
   drift and support burden without evidence of demand. Not selected as a
   separate deliverable; version-drift handling belongs to the deferred CLI
   design.
5. **CLI onboarding path.** Deferred, unchanged from ADR 0003: premature
   packaging, auth complexity and support burden before public docs have been
   validated with any external user. Stage 2 candidate.
6. **Read-only API/bridge later.** Deferred per #274: only if future evidence
   shows a model client needs remote kernel resolution or evidence packets
   without checkout access; must not duplicate GitHub connectors. Stage 2+.
7. **GPT/MCP/action package later.** Deferred: auth, secret safety, write
   authority and support burden are all unresolved; also depends on bridge
   decisions. Stage 2+, last.
8. **Internal-only / not ready.** Accurate today (Stage 0 gate not passed) but
   wrong as an end state: the roadmap's direction is Project OS for target
   projects generally, the surfaces are consolidated and bilingual, and the
   remaining gaps are a readiness review and presentation polish — both
   nameable, scoped work. Selected only as the interim state.

### Decision matrix

Scores: 1 (poor) – 5 (strong) for user value, roadmap fit and timing; 1 (high)
– 5 (low) for cost, security risk, support burden and adoption friction, so
higher is always better.

| Option | User value | Impl. cost | Security risk | Support burden | Adoption friction | Roadmap fit (#274/ADR 0003) | Timing | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Public repo only | 2 | 5 | 4 | 4 | 1 | 3 | 4 | Mechanism only |
| 2. Docs-first reference | 4 | 4 | 4 | 4 | 3 | 5 | 5 | **Stage 1** |
| 3. Harness positioning | 4 | 5 | 5 | 4 | 3 | 5 | 5 | **Stage 1 (qualified term)** |
| 4. Template/adapters package | 3 | 3 | 4 | 2 | 3 | 3 | 2 | Existing copy flow only |
| 5. CLI onboarding | 4 | 2 | 3 | 2 | 4 | 2 (deferred by ADR 0003) | 2 | Stage 2 candidate |
| 6. Read-only API/bridge | 3 | 2 | 2 | 2 | 3 | 2 (deferred by #274) | 1 | Stage 2+ |
| 7. GPT/MCP/action package | 3 | 1 | 1 | 1 | 4 | 2 | 1 | Stage 2+, last |
| 8. Internal-only | 1 (external) | 5 | 5 | 5 | 1 | 2 as end state | 3 | Interim state only |

## Audiences and value

- **People learning or vibe coding.** Value: understanding what changed and
  why; catching errors an implementation agent missed; using browser chat
  (read-only, draft-only) to review, ask, adjust scope and draft corrections;
  learning debugging and QA from concrete evidence; continuing work without
  depending on a previous chat's memory. Public language must be respectful
  of this audience — Project OS is a structured *complement* to how they
  already work, never mockery of it.
- **Experienced developers and small teams.** Value: explicit scope and
  transitions; independent review between implementation and closeout; clear
  summaries of changes, risks and validation; GitHub-native traceability;
  proportional validation; explicit authorization; freedom to switch agents
  and providers without losing context to a single tool or context window.
- Secondary audiences (PM/founder, open-source maintainer, AI-assisted
  agency, internal engineering team) map onto the two above; Stage 1 messaging
  targets the two primary ones and lets Stage 2 evidence say whether a
  secondary audience deserves dedicated material.

**Versus vibe coding:** vibe coding optimizes for speed inside one
conversation and loses scope, rationale and reviewability when the window
closes. Project OS keeps speed (agents still implement) but moves scope,
decisions, evidence and validation into durable GitHub traceability, so any
session — or any different agent — can pick up, review or correct the work.
The human keeps technical responsibility; agents are never presented as
working unsupervised.

**Subscription-cost framing:** the ability to alternate agents/providers when
one window or quota is exhausted may be presented as an *operational*
advantage. No prices or savings amounts are published unless the follow-up
docs work verifies provider, plan, currency/country, taxes, included limits,
consultation date and current terms, and presents them as dated comparable
scenarios, never permanent promises.

## Comparison with agent frameworks/runtimes

Project OS complements these systems: they define how an agent *executes*
(loops, tools, handoffs, state); Project OS defines how a *project* is run
when agents do the executing (scope, authority, evidence, validation,
traceability). A team could use any of them as the implementation surface
under Project OS discipline. Sources consulted 2026-07-11.

| | Project OS | OpenAI Agents SDK | LangGraph / Deep Agents | AutoGen |
| --- | --- | --- | --- | --- |
| Layer | Process/operating layer over GitHub | Agent runtime ("agentic AI apps… very few abstractions") | Low-level orchestration runtime / "batteries-included agent harness" on top of it | Multi-agent framework (AgentChat/Core/Studio) |
| Core primitives | Actors, modes, workflows, boundaries, evidence, outputs, statuses, operations | Agents, handoffs, guardrails, sessions, tracing | Graphs, state, durable execution, human-in-the-loop; Deep Agents adds planning, subagents, virtual filesystem | Conversational agents, event-driven core, extensions |
| Executes code / runs agents | **No** — humans and existing agent tools execute | Yes | Yes | Yes |
| Project source of truth | GitHub (issues, PRs, reviews, commits) | Not defined by the SDK; Sessions persist conversation/run history (runtime state) | Not defined by the framework; checkpointers persist thread-scoped graph state (runtime state) | Not defined by the framework; save/load persists agent/team model context (runtime state) |
| Authorization model | Exact PM approval, fail-closed gates, non-authorization of outputs | Guardrails (validation, not authority) | Human-in-the-loop interrupts/permissions | Human-in-the-loop patterns |
| Status | Active, internal dogfood | Active (OpenAI) | Active (LangChain) | Maintenance mode; successor is Microsoft Agent Framework |

What these frameworks persist is **runtime/session state** — conversation or
run history ([OpenAI Agents SDK sessions](https://openai.github.io/openai-agents-python/sessions/):
"Sessions stores conversation history for a specific session"), thread-scoped
graph checkpoints ([LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence):
"short-term, thread-scoped memory"), or agent/team model context
([AutoGen state management](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)).
None of them defines where the *project's* durable state — scope, decisions,
evidence, validation — lives; that is left to the application. Project OS
fixes that project source of truth in GitHub, which is a different layer, not
a competing feature.

Official sources: [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/),
[LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
("a low-level orchestration framework and runtime for building, managing, and
deploying long-running, stateful agents"),
[Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview)
and [repository](https://github.com/langchain-ai/deepagents) ("the
batteries-included agent harness"),
[AutoGen docs](https://microsoft.github.io/autogen/stable/index.html) and
[AutoGen → Microsoft Agent Framework migration guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/).
Public comparison material must restate the maintenance status of AutoGen
with a checked date and must never claim Project OS replaces any of these.

## Reproducible context benchmark (recommended, not run here)

Stage 1 docs must publish a benchmark, produced by the follow-up docs issue,
comparing for the **same** `(actor, workflow, mode)` tuple:

- resolver `--hydration-level minimal`;
- resolver `--hydration-level compact`;
- resolver `--hydration-level full/debug`;
- a monolithic baseline: a single `AGENTS.md`-style document that inlines the
  rules, workflow, boundaries and skills that tuple actually needs —
  constructed from the real kernel content, not an arbitrary "1000 lines".

Method requirements: measure bytes, characters and tokens; declare tokenizer,
tool, version and measurement date; separate selected-kernel content from
live state; document what information each alternative preserves; verify the
reduction drops no boundaries, evidence, outputs, statuses, non-authorization
or secret-safety content; and never claim universal savings from a single
model or tokenizer. Reproducible core:

```sh
python tools/project_os_resolve.py --actor actor.terminal_agent \
  --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
  --kernel-dir project-os-es/kernel --hydration-level <level> | wc -c
```

plus a declared tokenizer pass over the same outputs and the baseline file at
a named commit.

## Tutorial, onboarding and images (Stage 1 content, follow-up scope)

The follow-up docs issue improves the existing quick start
(`project-os-es/docs/empezar.md`, root `README.md`) — it must not create a
second incompatible guide — covering the PM's thirteen onboarding steps from
browser-chat setup through post-merge verification, split browser vs
terminal. Images are added only where they reduce real friction (browser
project setup, GitHub connection, adapter installation, operation selection,
reading issue/PR evidence), with alt text, a maintainable update path, and no
private repos, sensitive names, tokens, emails, cookies, credentials, `.env`
values, signed URLs or production data in any capture.

## What must be completed before public presentation

| Prerequisite (#394) | Status at 2026-07-11 |
| --- | --- |
| #393 accepted operation templates | Closed |
| Compact Spanish surfaces (#377, #389, #390, #391) | Closed |
| English translation of compact surface (#409) | Closed |
| Legacy cleanup (#405 migration, #407 adapter compaction) | Closed |
| Security/secrets/public-readiness review | **Pending — Stage 0 gate** |
| Stage 1 presentation/onboarding docs | **Pending — follow-up issue** |

## Recommended follow-up issues (not created or implemented here)

1. `security: public-readiness review of tree, history exposure and licensing`
   — the Stage 0 gate: secret/sensitive-content sweep, license decision,
   history-exposure posture, support/contribution policy; blocking for any
   visibility change.
2. `docs: implementar presentación pública y onboarding visual` — bilingual
   README/pitches per this ADR, audience benefits, improved browser/terminal
   tutorial, reproducible context benchmark with declared tokenizer and date,
   approved images, language/accessibility/secret-safety review.
3. `release: revisar readiness y crear el primer tag` — depends on 1 and 2:
   security and licensing re-check, version definition (taking into account
   the existing internal tags, latest `project-os-lab-v0.3.0`, so "primer tag"
   means the first public release tag), changelog/release notes, final
   validation, rollback, and exact PM approval for tag and release.
4. (Stage 2, evidence-gated) reopen CLI onboarding design under ADR 0003
   constraints; then read-only API/bridge; then GPT/MCP/action packaging —
   each only with adoption evidence and its own PM decision.

## Consequences

Project OS gets a single public story — a human-directed, GitHub-native
operating layer for AI-assisted development — that matches what the code
actually does today, with a concrete two-issue path (readiness review, then
presentation docs) toward a possible public repository — publication itself
stays conditional on the Stage 0 outcome and an exact PM approval — and no
premature commitment to CLI/API/packaging. It prohibits publishing before the
Stage 0 gate, bare
"harness" claims, autonomy claims, unverified savings/price claims, and any
tag/release inside the docs work. Accepted tradeoffs: activation may be
modest without an installer (Stage 2 exists to measure exactly that), and the
comparison matrix requires periodic re-verification against official sources.

Rollback is reverting this ADR. No runtime, package, API, kernel, resolver,
operation, template, adapter, target repo, credential, visibility, tag or
release state changes as a result of this design-only decision.
