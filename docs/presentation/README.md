# Public presentation: image policy and prepared repository metadata

Stage 1 preparation for issue #423 under ADR 0004 (docs-first content) as
amended by ADR 0005 (the publishing mechanism is a separate future public
repository; this repository stays private and internal-only).

Non-authorization: nothing in this document changes repository description,
metadata, settings or visibility, adds assets, or authorizes publication.
Every remote change keeps requiring its own exact, separate PM approval.

## Image and screenshot policy

Applies to any image added to this tree or reused by the future public
surface.

### Necessity gate

Add an image only where it reduces real onboarding friction. The candidate
spots named by the PM input on #394 and ADR 0004 are:

- browser project creation/configuration;
- GitHub connection;
- location of project instructions;
- adapter installation;
- operation selection;
- reading issue/PR evidence.

Text-first is the default: if a step is unambiguous in text, it gets no image.

### Sanitization checklist (blocking)

Every capture must be verified, before commit, to contain **none** of:

- private repositories or sensitive internal names;
- emails or personal data of third parties;
- tokens, cookies, credentials, `.env` values or secret-looking strings;
- signed URLs or production data/URLs.

A capture that cannot be produced or verified clean is not added — fail
closed; the text path must stand on its own.

### Accessibility

- Every image carries meaningful alt text describing what the reader needs
  from it, not just a filename.
- No information may exist only inside an image; the surrounding text must
  carry the same content.

### Update path

- Assets live under `docs/assets/` with stable, descriptive names.
- Each asset records, in the document that embeds it, the capture date and
  the UI/surface it shows.
- When a UI change makes a capture misleading, update it or remove it in the
  same unit of work that touches the affected guide; a wrong image is worse
  than no image.

### Status of the Stage 1 pass (issue #423)

No images were added: the onboarding steps that would benefit are
browser-side UI flows whose captures cannot be produced and
sanitization-verified from the terminal surface that implemented #423, and
the tutorial stands alone in text. Future images remain gated by this policy
and by the asset operations (`MOS-3.15`/`MOS-3.19`) with PM review.

## Prepared repository metadata (not applied)

Prepared wording for the *future public surface* defined by ADR 0005, to be
applied there only after that repository's own public-readiness gate and
exact PM approval. Nothing here is applied to `codefusion-repo/project-os-v2`.

- **Description (EN):** "Human-directed operating system for building real
  products with AI agents — a compact, agent-resolvable kernel of actors,
  modes, workflows, boundaries and evidence, with all live project state in
  GitHub."
- **Descripción (ES):** «Sistema operativo humano-dirigido para construir
  productos reales con agentes de IA: un kernel compacto resoluble por
  agentes — actores, modos, workflows, límites y evidencia — con todo el
  estado vivo del proyecto en GitHub.»
- **Suggested topics:** `ai-agents`, `developer-tools`, `sdlc`,
  `project-management`, `github-workflow`, `llm`, `human-in-the-loop`,
  `traceability`.
- **Positioning constraints (from ADR 0004):** never a bare "harness" (only
  qualified, e.g. "process harness"/"operating layer"); no autonomy claims;
  no framework-replacement claims; no unverified savings or price claims.

## Traceability

- Issue #423 (Stage 1 docs-first content), following ADR 0004 and ADR 0005.
- Related policy documents: `SECURITY.md`, `CONTRIBUTING.md`, `SUPPORT.md`,
  `CODE_OF_CONDUCT.md`, `docs/security/PUBLIC_READINESS_REVIEW.md`.
