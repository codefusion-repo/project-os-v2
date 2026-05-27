# Project OS v2 Contract Structure

## 1. Objective

Define the structure-only layout and naming conventions for later, explicitly scoped Project OS v2 JSON contracts.

This document decides contract root, directory layout, naming convention, ID namespace, versioning, status, language, placeholder/null policy, examples policy, and no-population boundaries. It does not create populated JSON contracts.

## 2. Scope

This document is structure-only. It defines where later explicitly scoped contract files should live and how they should be named.

R0.01 updates this document as docs-only rebaseline work. It does not create contract data, JSON contract skeleton files, JSON schemas, validators, runtime behavior, parser behavior, automation, API, panel, runners, context packs, target-project artifacts, database/read-model direction, write authorization behavior, or Resolver behavior.

## R0.01 Roadmap Rebaseline Boundary

The active fixed roadmap source is GitHub issue #92. Issue #47 is historical/provenance, issue #91 is completed roadmap rebaseline evidence, and issue #90 is open/paused tooling-readiness evidence. This document must not imply that #47 remains the active roadmap.

Stage-scoped permissions apply:

- Planning issues do not create contracts.
- Docs issues may modify only approved docs.
- Contract population issues may create or update contracts only when explicitly scoped.
- Schema issues may create schemas only after schema strategy approval.
- Validator issues may create validators only after schema implementation.
- Loader, Resolver, runtime, panel, and write authorization remain blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.

Until Base v0.1 is certified dogfood-ready, Project OS v2 is still being built through project-os-supported bootstrap and migration. Migration/import/baseline population work must not be labeled as dogfood. Panel planning and implementation are excluded from the fixed backlog until Base v0.1 certification and dogfood pilot evidence justify later PM approval.

## 3. Canonical Contract Root

The canonical contract root path for future JSON contracts is:

```text
contracts/
```

The `contracts/` directory is not created by this document. Later issues should create or modify it only when the approved roadmap scope explicitly allows contract skeleton, schema, validator, or population work.

Later explicitly scoped manifest and index files should be named conceptually as root-level static support bundles:

```text
contracts/manifest.json
contracts/index.json
```

These names are reserved concepts only. Policy, manifest, index, and selector are non-entity static support bundles, not members of the 18 base entity families. They support Resolver discovery/reference behavior but do not implement runtime behavior, selector runtime, generated indexes, contract loader behavior, or Resolver implementation.

## 4. Directory Layout

The directory layout uses one singular entity-family directory per base entity family.

Directory names must be:

- lower_snake_case
- singular, not plural
- ASCII-only and unaccented
- based on the approved base entity family name
- stable once populated contracts exist

Future contract directories:

```text
contracts/
  resolver/
  actor/
  rol/
  workflow/
  workflow_step/
  accion/
  recurso/
  scope/
  fuente/
  evidencia/
  estado/
  limite/
  regla/
  variable/
  plantilla/
  artefacto/
  relacion/
  contrato/
```

This layout accounts for all 18 base entity families:

| Base entity family | Future directory |
| --- | --- |
| `Resolver` | `contracts/resolver/` |
| `Actor` | `contracts/actor/` |
| `Rol` | `contracts/rol/` |
| `Workflow` | `contracts/workflow/` |
| `WorkflowStep` | `contracts/workflow_step/` |
| `Acción` | `contracts/accion/` |
| `Recurso` | `contracts/recurso/` |
| `Scope` | `contracts/scope/` |
| `Fuente` | `contracts/fuente/` |
| `Evidencia` | `contracts/evidencia/` |
| `Estado` | `contracts/estado/` |
| `Límite` | `contracts/limite/` |
| `Regla` | `contracts/regla/` |
| `Variable` | `contracts/variable/` |
| `Plantilla` | `contracts/plantilla/` |
| `Artefacto` | `contracts/artefacto/` |
| `Relación` | `contracts/relacion/` |
| `Contrato` | `contracts/contrato/` |

## 5. Relationship Contract Location

Future relation contracts live under:

```text
contracts/relacion/
```

They should not be split into relation-specific directory trees such as `workflow_step_delega_actor/` or `workflow_compone_workflow_step/`.

Reason: `Relación` is one of the 18 base entity families. Keeping all relationship contracts under `relacion/` preserves the entity-family layout and avoids turning relationship types into a second directory model. Future manifest or index files may group relationship contracts by endpoint or relation type without changing canonical storage.

## 6. File Naming Convention

The file naming convention for future contract files is:

```text
contracts/<entity_family>/<contract_id>.json
```

Rules:

- File extension is `.json`.
- One file represents one contract version.
- File basename must equal the contract ID.
- File basename must be lower_ascii, dot-separated, and stable.
- The first namespace segment must match the entity-family directory name.
- Do not use spaces, uppercase letters, accents, or path separators in file names.

Non-canonical examples:

```text
contracts/actor/actor.placeholder_actor.v1.json
contracts/workflow_step/workflow_step.placeholder_step.v1.json
contracts/relacion/relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1.json
```

These examples are placeholder-safe and non-canonical. They are not real Project OS v2 contracts and must not be copied as populated data.

## 7. ID Namespace

The stable ID namespace convention for later explicitly scoped contracts is:

```text
<entity_family>.<slug>.v<major>
```

Examples:

```text
actor.placeholder_actor.v1
workflow_step.placeholder_step.v1
relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1
```

ID rules:

- `entity_family` must match the directory name.
- `slug` must be lower_ascii snake_case.
- `v<major>` must use a positive integer major version, such as `v1`.
- IDs must not contain spaces, accents, uppercase letters, or mutable state.
- IDs must not encode live GitHub status, execution results, timestamps, branch names, or target-project generated artifacts.
- IDs should remain stable across minor documentation edits.

For future relation contracts, the ID should include enough endpoint/type information to be understandable without loading the file body. The exact relation slug pattern can be refined in the relationship skeleton issue, but it must remain inside the `relacion.*.vN` namespace.

## 8. Versioning

The versioning convention is major-versioned contract identity:

```text
<entity_family>.<slug>.v1
<entity_family>.<slug>.v2
```

Rules:

- `v1` is the first major version of a contract.
- A breaking semantic or structural change creates a new major version and therefore a new file.
- Non-breaking edits may update the contract body in place only if the future envelope defines how minor revision metadata is represented.
- The file path is part of contract identity and must not move casually after population begins.
- Versioning is for contract identity, not runtime release behavior.

This issue does not define JSON envelope fields for minor version metadata.

## 9. Contract Status

Future contract status values should be lower_ascii lifecycle tokens:

```text
draft
review
approved
deprecated
archived
```

Rules:

- New placeholder-safe skeletons should start as `draft` unless a later issue decides otherwise.
- `approved` means approved as contract data, not executed behavior.
- `deprecated` keeps the old contract readable but signals replacement.
- `archived` signals historical retention.
- Status values do not implement validation, routing, loading, permissions, or write authorization.

## 10. Language Policy

Directory names and file names use ASCII lower_snake_case.

Field names in future JSON contracts should use Spanish domain vocabulary from the foundation model, normalized to ASCII lower_snake_case for tool compatibility. Approved English entity terms already present in the model remain English.

Examples of canonical field-token normalization for future JSON:

| Foundation label | Future JSON field token |
| --- | --- |
| `descripción` | `descripcion` |
| `versión` | `version` |
| `Acción` | `accion` |
| `Límite` | `limite` |
| `Relación` | `relacion` |
| `condición_base_avance` | `condicion_base_avance` |
| `ubicación` | `ubicacion` |
| `estado_verificación` | `estado_verificacion` |
| `tipo_relación` | `tipo_relacion` |
| `WorkflowStep` | `workflow_step` |
| `Scope` | `scope` |

Human documentation may keep Spanish accents for readability. JSON keys, directory names, file names, and ID tokens should avoid accents.

## 11. Placeholder/Null Policy

The placeholder/null policy for future skeleton work is:

- Use `null` only for unknown, intentionally unfilled scalar values.
- Use empty arrays for intentionally empty lists.
- Avoid empty strings because they are ambiguous.
- Do not invent realistic actor, role, workflow, step, rule, limit, evidence, source, template, artifact, relationship, or resolver values as placeholders.
- Placeholder tokens must be visibly non-real, for example `placeholder_actor`, `placeholder_step`, or `example_only`.
- Placeholder examples inside documentation must be explicitly marked non-canonical.
- Future skeleton files must not contain populated operational content until entity-family population issues approve it.

This policy prevents placeholder data from becoming accidental canonical contract data.

## 12. Examples Policy

Examples in this document and future structure documents must be:

- documentation-only
- placeholder-safe
- non-canonical
- visibly artificial
- limited to explaining layout, naming, ID namespace, versioning, and placeholder policy

Examples must not define real Project OS v2 actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, Resolver behavior, or operational decisions.

## 13. No-Population Rule

The no-population rule is mandatory.

This issue does not create `Resolver` contract data and does not implement `Resolver` behavior.

This issue does not create real populated data for:

- `Actor`
- `Rol`
- `Workflow`
- `WorkflowStep`
- `Acción`
- `Recurso`
- `Scope`
- `Fuente`
- `Evidencia`
- `Estado`
- `Límite`
- `Regla`
- `Variable`
- `Plantilla`
- `Artefacto`
- `Relación`
- `Contrato`

The only new artifact in this issue is this structure-only Markdown specification.

## 14. Relationship To Foundation Design

The foundation design remains the human reference for:

- normalized base entities
- reusable `WorkflowStep` composition
- `Relación` as owner of compatibility, permission, requirement, dependency, sequencing, and restriction
- `Resolver` as the future single AI read entrypoint
- GitHub as live evidence
- Markdown as human reference

This document converts the foundation direction into future storage layout and naming decisions. It does not change the entity model or relationship model.

When JSON contracts are introduced later, the future contract files should become the canonical stable structure for entity and relationship data. Markdown should continue to explain decisions, not duplicate live contract data.

## 15. Explicit Non-Implementation Boundaries

This issue explicitly does not implement:

- populated JSON contracts
- JSON contract skeleton files
- JSON schemas
- validators
- validator implementation
- schema implementation
- runtime behavior
- parser behavior
- automation
- API
- panel
- runners
- context-pack output or context-pack loading
- target-project artifacts
- database/read-model direction
- projection architecture
- write authorization
- Resolver behavior
- manifest shape
- index shape
- selector shape
- contract loader behavior
- workflow composition
- relationship population

Schemas and validators are not created by this document. Under the #92 roadmap, schemas and validators happen after normalization and before Project OS inventory, mapping, and migration. Migrated baseline contracts are reviewed with schemas and validators before loader or Resolver work.

## 16. Roadmap Readiness

This document is intended to let later explicitly scoped contract work proceed without re-deciding:

- contract root
- directory layout
- entity-family directory naming style
- singular directory names
- Spanish/English naming policy
- file extension
- one file per contract version
- relation contract location
- ID namespace
- versioning
- status tokens
- placeholder/null policy
- examples policy
- no-population rule

The next roadmap item after R0.01 is R0.02 roadmap hygiene. Contract creation, schema work, validator work, loader behavior, Resolver behavior, runtime behavior, panel work, and write authorization remain unavailable unless a later explicit roadmap ID or PM-approved amendment scopes them.
