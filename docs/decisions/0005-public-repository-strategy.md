# ADR 0005 - Public repository strategy and GitHub surfaces

- Status: accepted by explicit PM decision (issue #422 PM comment). This ADR
  records the architecture decision that resolves B4 for this repository and
  amends the Stage 1 mechanism of ADR 0004
  (`docs/decisions/0004-public-presentation-and-packaging.md`). Amended by
  the PM decision on issue #424 (Option B) with a bounded exception for one
  internal annotated handoff tag; see
  [Amendment 1](#amendment-1--bounded-internal-handoff-tag-exception-issue-424).
- Date: 2026-07-13
- Scope: issue #422; architecture decision on the public repository strategy,
  the source of truth, the treatment of GitHub surfaces (issues, PRs,
  comments, reviews, history) and the downstream interpretation of Stage 1,
  #423 and #424. No repository is created, transferred, copied or published
  by this ADR; no visibility, settings, tags or releases change.
- Source basis: issue #422 and its PM decision comment; ADR 0004; Stage 0
  public-readiness review (`docs/security/PUBLIC_READINESS_REVIEW.md`,
  including its B4 section and findings F-04, F-05, F-06); roadmap #274;
  B1 resolution (#419 / PR #420); B2/B3 resolution (#421 / PR #425);
  follow-up issues #423 and #424.
- Non-authorization: this ADR grants no permission to create the new
  repository, copy or transfer content, change visibility or settings,
  implement the CLI, modify the demo projects, create tags or releases,
  publish Project OS, or close #422. Each of those requires its own scoped
  unit of work and exact, separate PM approval.

## Context

ADR 0004 adopted a staged, docs-first path whose Stage 1 mechanism was to
publish **this** repository (`codefusion-repo/project-os-v2`) once the
Stage 0 gate passed and the PM approved publication exactly. The Stage 0
review (#417 / PR #418) returned `GO_WITH_BLOCKERS`: the tree is clean and
the history holds no real credentials, but four governance/coverage blockers
remained. B1 (license) was resolved by #419; B2 (security policy) and B3
(contribution/support policy) were resolved by #421. B4 stayed open: a
visibility change on this repository would expose issues, pull requests,
comments, reviews, descriptions and metadata that the Stage 0 gate never
audited, plus the documented historical exposures F-04 (synthetic secret
fixture in history), F-05 (internal project name in history) and F-06
(personal name and emails in commit metadata).

The Stage 0 review also registered a candidate PM direction for B4: keep
this repository as the internal baseline and create a new public repository
instead of publishing this one. That direction modifies the Stage 1
mechanism of ADR 0004 and therefore required this durable architecture
decision. Issue #422 evaluated three alternatives: (A) publish the current
repository, (B) create a new repository later as the public surface, (C)
keep Project OS internal-only. The PM decision comment on #422 selected
alternative B with exact terms; this ADR records that decision.

## Decision

### 1. Current repository: internal-only

`codefusion-repo/project-os-v2` stays **private and internal-only**. It will
not be published, its visibility will not change, and it will not be the
repository where CLI development continues. Once development starts in the
new repository, this repository remains as CodeFusion's internal operational
baseline, with no continuous synchronization and no backports from the new
surface.

### 2. New repository: `agent-os-cli`

A new repository named **`agent-os-cli`** will be created later. It will
contain the same functional base of Project OS — kernel, operations,
templates, adapters, tooling and documentation — and the CLI will be
developed on that base. The new repository:

- is created initially as **private**;
- will later become the public surface of Project OS and its CLI;
- does **not** inherit issues, pull requests, comments, reviews or any other
  historical GitHub conversations from the current repository;
- **keeps the audited git and content base** of the project, with the PM
  explicitly accepting the documented historical risks F-04, F-05 and F-06;
- is subject to **its own public-readiness audit** before any visibility
  change.

### 3. Source of truth and transition

After the transition, **the new repository is the source of truth** for
Project OS and the CLI. The current repository is neither a second
development branch nor a synchronized replica. The relationship is:

`current internal baseline → single transition to the new repository →
future development only in the new repository`

There is **no bidirectional synchronization** and no backporting to the
frozen internal baseline.

### 4. External contributions

The new repository keeps the policy already decided in B2/B3 (#421):
community contributions accepted; issue-first process; Spanish or English;
`work/*` branches; proportional validation; draft PR and
review-before-close; inbound=outbound under Apache-2.0; no CLA or DCO;
Contributor Covenant 3.0; best-effort support without SLA. Contributions are
filed and resolved in the new repository and are not backported to the
internal baseline.

### 5. Ownership and releases

CodeFusion SpA owns and is responsible for the new repository, its policies
and its releases. The PM — founder and sole owner of CodeFusion — is the
only release approver until other maintainers are expressly designated.
No tag, release, visibility change or publication is authorized by this
decision; each transition requires exact, separate PM approval.

### 6. Dogfood gate

The projects currently identified for dogfood are `ecommerce-demo`,
`portfolio-demo`, `inventory-demo` and `rental-demo` — the current batch,
not a permanent statement about all future projects. Their adaptation,
improvement iterations and the confirmation that the dogfood gate is done
are managed and confirmed later by the PM and are outside the scope of #422.
**Publication of the new repository stays blocked until the PM confirms the
required dogfood is complete.**

### 7. Demo project licensing (intent)

The intent is to license those four demo projects under the same model as
Project OS: Apache License 2.0. Each repository requires its own traceable
unit of work to verify ownership, year, provenance, `NOTICE` needs and exact
license application. #422 modifies none of those repositories.

### 8. Resolution of B4

**B4 is resolved for `codefusion-repo/project-os-v2`** because:

- the current repository will not be published;
- its historical GitHub surfaces (issues, PRs, comments, reviews, metadata)
  will not be migrated to the public repository;
- the future public surface is a different repository;
- that repository has its own security, privacy and public-readiness gate.

Resolving B4 does not by itself complete publication and does not authorize
creating the new repository. The Stage 0 review records this resolution in
its B4 update section.

## Downstream interpretation: Stage 1, #423 and #424

The PM sequence is preserved:

`#422 → #423 → #424 → close roadmap #274 → start the new repository and CLI
development`

To keep that sequence without contradicting the decision not to publish the
current repository, ADR 0004's Stage 1 is reinterpreted as follows:

- **Stage 1 (docs-first public reference)** keeps its content — positioning,
  messaging, README/tutorial improvements, reproducible context benchmark —
  but its **publishing mechanism is no longer this repository**. The
  docs-first surface becomes public through `agent-os-cli` after that
  repository's own public-readiness gate and exact PM approval.
- **#423** prepares documentation and onboarding that are **reusable by the
  future public surface**; it does not publish anything from this
  repository.
- **#424** remains the **release-readiness and handoff gate**. It creates no
  public tag, no GitHub Release and no release in the current repository;
  under
  [Amendment 1](#amendment-1--bounded-internal-handoff-tag-exception-issue-424)
  it may culminate in **one internal annotated handoff tag** in this
  repository, gated by exact, separate PM approval. The effective public tag
  and release are executed later **in the new repository**, from an exact
  commit of that repository, with separate PM approval.
- The later gates of ADR 0004 are preserved: the new repository's own
  public-readiness audit before any visibility change, the dogfood
  confirmation gate, and exact, separate PM approvals for repository
  creation, content transition, visibility, tags, releases and publication.

## Alternatives evaluated

- **A. Publish the current repository** (ADR 0004's original Stage 1
  mechanism). Requires auditing or explicitly accepting all historical
  GitHub surfaces (issues, PRs, comments, reviews, metadata) plus the
  exposure of internal history and tags (F-04, F-05, F-06, F-10). Rejected:
  the unaudited-surfaces gap is material, the exposures are avoidable, and
  the audit cost buys no product value that the new-repository path does not
  also provide.
- **B. New repository as the future public surface.** Avoids publishing
  unaudited GitHub surfaces entirely; carries the audited git/content base
  with F-04/F-05/F-06 explicitly accepted; gives the CLI a clean home with
  its own gate. Cost: a single transition and a second readiness audit —
  accepted. **Selected.**
- **C. Internal-only forever.** Valid under ADR 0004 but closes the public
  path the roadmap still aims at. Not selected; internal-only remains the
  permanent state **of this repository only**.

## Risks

Accepted risks (PM decision on #422):

- F-04, F-05, F-06 travel with the git base into the new repository (secret
  scanning noise from a synthetic fixture; internal project name in history;
  personal name/emails in commit metadata).
- A frozen internal baseline diverges from the public surface by design; the
  single-transition rule and the no-backport rule make that divergence
  intentional rather than accidental.

Not accepted (out of scope of this decision, each blocked on its own gate):

- publishing any unaudited GitHub surface;
- creating, transferring or publishing any repository without exact PM
  approval;
- any tag, release, settings or visibility change;
- CLI implementation or demo project changes.

## Consequences

This repository's publication question is closed: it stays internal-only,
and B4 is resolved without exposing any unaudited surface. Stage 1 keeps its
docs-first content but loses its original publishing mechanism; #423 and
#424 remain in sequence as preparation and handoff gates. The public future
of Project OS moves to `agent-os-cli`, which must pass its own
public-readiness audit and dogfood confirmation before any visibility
change. Roadmap #274 can close after #423 and #424 without any publication
having occurred.

Rollback is reverting this ADR (and the paired B4 update in the Stage 0
review). No remote state changes as a result of this decision.

## Amendment 1 — bounded internal handoff tag exception (issue #424)

- Date: 2026-07-14
- Status: accepted by explicit PM decision on issue #424 (Option B). This
  amendment changes only the tag treatment of this ADR for the current
  repository; it replaces the earlier reading of #424 as a "first public
  release tag" gate.
- Source basis: issue #424 (re-scoped body recording the PM's Option B
  decision); issue #423 / PR #427 (Stage 1 documentation completed);
  roadmap #274; readiness and handoff package
  (`docs/release/INTERNAL_HANDOFF_READINESS.md`).
- Non-authorization: this amendment permits the tag **conceptually**; it
  authorizes nothing. Creating and pushing the tag requires exact, separate
  PM approval of the final name, message and SHA.

### Exception

`codefusion-repo/project-os-v2` may carry **exactly one annotated internal
handoff tag** that marks the final kernel baseline before the single
transition to `agent-os-cli`. The exception is bounded as follows:

- The tag is an **internal marker only**: it is not public, it is not a
  GitHub Release, and it does not announce, publish or version Project OS
  for any external audience.
- The tag must be **annotated** (not lightweight). Its name and message must
  state unambiguously that it is an internal handoff marker and not a public
  release; the name must not collide with any existing ref and must not
  follow a public-release-looking naming scheme.
- The target commit is fixed **only after** the #424 amendment and readiness
  work is merged into `main` and final validation and CI are green on that
  head. The fixed commit must belong to `main` and match the validated
  state. The SHA is never fixed in advance.
- Once pushed, the tag is not moved, reused or deleted; a mistake is
  corrected with a **new** tag under a new exact PM approval, and any
  deletion would require its own exact PM approval and separate
  communication.
- The tag is **not** an authorization to create `agent-os-cli`, transfer or
  copy content, change visibility or settings, implement the CLI, publish
  anything, or close #424 or roadmap #274. Each of those remains gated by
  its own exact, separate PM approval.

### What does not change

Every other clause of this ADR stays in force: this repository remains
private, internal-only and — after the transition — frozen as CodeFusion's
internal baseline; `agent-os-cli` remains the future public surface and,
after the transition, the **only** source of truth for Project OS and the
CLI; the transition remains **single**, with no bidirectional
synchronization and no backports; and the later gates of ADR 0004 (the new
repository's own public-readiness audit, the dogfood confirmation gate, and
exact, separate PM approvals for repository creation, content transition,
visibility, tags, releases and publication) are preserved unchanged.

Rollback of this amendment is documentary only: reverting it does not
delete, move or reuse a tag that already exists.
