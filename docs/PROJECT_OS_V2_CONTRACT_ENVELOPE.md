# Project OS v2 Contract Envelope

## 1. Objective

Define the structure-only base contract envelope for later, explicitly scoped Project OS v2 JSON contracts and the placeholder-safe skeleton policy that later skeleton or population issues must follow.

This document defines the shared wrapper and metadata boundary only. R0.01 updates it as docs-only rebaseline work. It does not create JSON contract files, populated contract data, JSON schemas, validators, runtime behavior, parser behavior, automation, API, panel, runners, context packs, target-project artifacts, database/read-model direction, write authorization behavior, or Resolver behavior.

## 2. Scope

Every later explicitly scoped contract file should use the same base envelope so contract identity, lifecycle metadata, source references, schema references, and payload placement are predictable.

This document is documentation-only and structure-only. It does not create:

- the `contracts/` directory
- contract skeleton files
- populated contract data
- schema files
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
- write authorization behavior
- Resolver behavior

## R0.01 Roadmap Rebaseline Boundary

The active fixed roadmap source is GitHub issue #92. Issue #47 is historical/provenance, issue #91 is completed roadmap rebaseline evidence, and issue #90 is open/paused tooling-readiness evidence. This document must not imply that #47 remains the active roadmap.

Stage-scoped permissions apply:

- Planning issues do not create contracts.
- Docs issues may modify only approved docs.
- Contract population issues may create or update contracts only when explicitly scoped.
- Schema issues may create schemas only after schema strategy approval.
- Validator issues may create validators only after schema implementation.
- Loader, Resolver, runtime, panel, and write authorization remain blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.

Under #92, schemas and validators happen after normalization and before Project OS inventory, mapping, and migration. Migrated baseline contracts are reviewed with schemas and validators before loader or Resolver work. Until Base v0.1 is certified dogfood-ready, Project OS v2 remains in project-os-supported bootstrap and migration; panel work is not part of the fixed execution backlog.

## 3. Base Contract Envelope Purpose

The base contract envelope is the common wrapper around future entity and relationship payloads.

The envelope should make every future contract answer the same metadata questions:

- What contract is this?
- Which base entity family does it belong to?
- Is it an entity contract or a relationship contract?
- Which major contract version does it represent?
- What lifecycle status does it have?
- Which future schema, if any, should describe its shape?
- Which source references explain why this contract exists?
- Where is the entity-specific or relationship-specific data stored?

The envelope is not the entity model itself. The envelope only formalizes contract identity and metadata so future tools and humans can locate, compare, review, and reason about contract files consistently.

## 4. Envelope vs Payload Boundary

The envelope vs payload boundary is mandatory.

Envelope responsibilities:

- store contract identity and metadata
- identify the base entity family through `entity_family`
- identify whether the contract payload describes an entity or a relationship through `contract_kind`
- carry version and lifecycle status metadata
- carry schema references as references only
- carry source references as references only
- provide the required `payload` container

Payload responsibilities:

- store entity-specific attributes for entity contracts
- store relationship endpoints, relationship type, cardinality, required flag, and order for relationship contracts
- preserve normalization rules from the foundation design
- keep entity attributes separate from relationship composition semantics

Boundary rules:

- The envelope must not duplicate payload attributes.
- The payload must not duplicate envelope metadata.
- `id` in the envelope is the contract ID, not a second copy of an entity-local attribute.
- `descripcion` in the envelope is the contract-level description. A future skeleton issue must avoid storing the same description again in payload.
- Live GitHub evidence must not be copied into envelope fields.
- GitHub issues, PRs, comments, commits, reviews, tags, branches, roadmap state, and validation outputs may be referenced later, but their mutable state must remain live evidence.
- `schema_ref` is a reference only. No schema files are created by this issue.

## 5. Required Envelope Fields

Later explicitly scoped contracts should use these required envelope fields.

| Field | Required | Purpose | Placeholder-safe skeleton value |
| --- | --- | --- | --- |
| `id` | Yes | Stable contract ID using `<entity_family>.<slug>.v<major>`. The file basename must match it when files are created later. | Visibly artificial placeholder ID such as `actor.placeholder_actor.v1`. |
| `entity_family` | Yes | Base entity-family directory token from the contract structure document. | A valid family token when the skeleton family is known. |
| `contract_kind` | Yes | Distinguishes `entity` payloads from `relationship` payloads. | `entity` or `relationship`, never a real workflow decision. |
| `version` | Yes | Contract version metadata. The major version must align with the `v<major>` suffix in `id`. | A structural value such as major version `1`, or `null` where a later skeleton issue intentionally leaves it unassigned. |
| `status` | Yes | Contract lifecycle status. | `draft` for future placeholder-safe skeletons unless a later issue decides otherwise. |
| `schema_ref` | Yes | Reference to a future schema or schema identifier. | `null` until a schema reference is explicitly approved. |
| `descripcion` | Yes | Contract-level human description. | `null` until real content is approved. |
| `source_refs` | Yes | References to source documents, issues, PRs, comments, or other authority records. | `[]` when no approved references are intentionally attached. |
| `payload` | Yes | Container for entity-specific or relationship-specific data. | Object with placeholder-safe fields, using `null` for unknown scalars and `[]` for intentionally empty lists. |

The required fields above are the minimum common envelope. Future skeleton issues may refine child shapes such as the exact `version` object, but they should not move entity attributes or relationship endpoints into envelope metadata.

## 6. Optional Envelope Fields

Future issues may add optional envelope fields only when they remove real ambiguity and preserve the envelope vs payload boundary.

Recommended optional fields:

| Field | Purpose | Placeholder-safe skeleton value |
| --- | --- | --- |
| `nombre` | Optional short contract display name if needed for review. | `null` until approved. |
| `aliases` | Optional alternative IDs or historical labels. | `[]` unless intentionally populated later. |
| `supersedes` | Optional list of contract IDs superseded by this contract. | `[]` unless intentionally populated later. |
| `superseded_by` | Optional replacement contract ID for deprecated contracts. | `null` unless intentionally populated later. |
| `review_refs` | Optional references to review records. | `[]` and references only, never copied review bodies. |

Optional fields must not become a second payload. If an optional field describes Actor capability, Workflow order, relationship endpoints, evidence bodies, limit severity, rule behavior, resource location, or template sections, it belongs in `payload` or a related contract, not in the envelope.

## 7. Entity-Specific Payload Placement

For entity contracts, `payload` stores normalized attributes owned by the entity family.

Examples of entity payload ownership:

- `Actor` payload owns base execution surface capability fields.
- `Rol` payload owns professional lens fields.
- `Workflow` payload owns lifecycle/process composition identity fields, not execution behavior.
- `WorkflowStep` payload owns reusable objective and base transition condition fields.
- `Fuente` payload owns source identity and authority fields.
- `Evidencia` payload owns evidence reference shape, not copied mutable GitHub state.
- `Límite` payload owns limit type and severity fields.
- `Regla` payload owns rule condition and expected behavior fields.
- `Plantilla` payload owns template type, format, and required sections.
- `Artefacto` payload owns artifact type, name, and reference fields.

Entity payloads must not own compatibility, permission, requirement, dependency, sequencing, restriction, relationship endpoints, relationship cardinality, contract status, schema references, source references, or live operational state.

When a normalized source attribute has the same conceptual meaning as a required envelope field, the future skeleton issue must map it once, not duplicate it. For example, contract identity belongs in envelope `id`; contract-level description belongs in envelope `descripcion`; entity-family placement belongs in envelope `entity_family`.

## 8. Relationship-Specific Payload Placement

For relationship contracts, `entity_family` should be `relacion` and `contract_kind` should be `relationship`.

Relationship payloads store relationship-specific data such as:

- `origen_entidad`
- `origen_id`
- `destino_entidad`
- `destino_id`
- `tipo_relacion`
- `cardinalidad`
- `requerido`
- `orden`

These fields belong in `payload`, not in envelope metadata.

Relationship payloads are where Project OS v2 preserves compatibility, permission, requirement, dependency, sequencing, restriction, workflow-specific order, and workflow-specific required/optional state. Entity contracts must not copy those relationship semantics into their own payloads.

## 9. Placeholder-Safe Values

Future skeletons must be fillable and visibly incomplete.

Placeholder-safe values:

- use `null` for intentionally unknown scalar values
- use `[]` for intentionally empty lists
- use visibly artificial placeholder tokens when a structural ID is required
- use `draft` for initial skeleton status unless a later issue changes the status policy
- keep payload fields unfilled until population is explicitly approved

Unsafe placeholder values:

- realistic fake names
- real actors
- real roles
- real workflows
- real limits
- real rules
- real sources
- real evidence
- real templates
- real artifacts
- real relationships
- copied issue bodies, PR bodies, comments, review text, commit metadata, validation output, branch state, or roadmap state
- empty strings

Placeholder tokens should be obviously non-real, for example `placeholder_actor`, `placeholder_step`, `placeholder_origen`, `placeholder_destino`, or `example_only`.

## 10. Null and Empty Arrays Policy

The null and empty arrays policy is:

- Use `null` for intentionally unknown scalar values.
- Use `[]` for intentionally empty lists.
- Avoid empty strings because they do not say whether the value is unknown, intentionally blank, or accidentally omitted.
- Do not use realistic fake strings to make a skeleton look complete.
- Do not use populated operational content as placeholder material.
- Required object containers such as `payload` may exist while their child fields remain `null` or `[]`.

For future skeletons, `null` means "known field, intentionally not filled yet." It must not mean "field does not apply." A later skeleton issue may define family-specific rules for fields that do not apply.

## 11. Status Handling

Future contract status values should follow the structure document:

```text
draft
review
approved
deprecated
archived
```

Status is envelope metadata only.

Status rules:

- New placeholder-safe skeletons should start as `draft` unless a later issue decides otherwise.
- `review` means the contract data is being reviewed.
- `approved` means approved as contract data, not executed behavior.
- `deprecated` keeps an older contract readable while signaling replacement.
- `archived` signals historical retention.
- Status values do not implement validation, routing, loading, permissions, execution, or write authorization.

## 12. Version Handling

Version handling follows the structure document:

- Contract IDs use `<entity_family>.<slug>.v<major>`.
- One file represents one contract version.
- The file basename must match the contract ID.
- The envelope `version` metadata must align with the `v<major>` suffix in `id`.
- Breaking semantic or structural changes create a new major version and a new file.
- Versioning is for contract identity, not runtime release behavior.

This document does not define minor revision metadata. A future issue may add minor or revision metadata only if it preserves the required major-version identity rule.

## 13. Source and Reference Handling

`source_refs` stores references only.

Allowed future reference types may include:

- source document path references
- GitHub issue references
- GitHub PR references
- GitHub comment references
- GitHub commit references
- GitHub branch references
- GitHub review references
- validation references
- contract ID references
- external authority references approved by a later issue

Rules:

- Do not copy live GitHub evidence into `source_refs`.
- Do not copy issue bodies, PR bodies, comments, reviews, validation output, branch state, roadmap state, or mutable status values into envelope fields.
- Do not use `source_refs` to replace `Fuente` or `Evidencia` contracts.
- Use `[]` when no references are intentionally attached.
- Use references to explain provenance, not to store operational state.

`Fuente` and `Evidencia` contracts are stable references/categories, not live snapshots. Issue, PR, branch, commit, review, validation, and roadmap state must be checked live when needed.

## 14. Schema Reference Handling

`schema_ref` is a reference only.

Rules:

- `schema_ref` may be `null` until schemas are explicitly approved.
- A non-null `schema_ref` should identify a future schema or schema family by reference.
- `schema_ref` does not create a schema file.
- `schema_ref` does not imply validators exist.
- `schema_ref` does not define parser behavior.
- This document creates no schema files and no validator behavior. Under #92, schema issues happen after normalization and validator issues happen after schema implementation.

## 15. No-Population Rule

The no-population rule is mandatory.

This document does not populate real values for:

- `Resolver`
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

Future skeletons must avoid real actors, roles, workflows, limits, rules, sources, evidence, templates, artifacts, relationships, operational decisions, and target-project artifacts until a later population issue explicitly approves that scope.

## 16. Non-Canonical Example Policy

Examples are allowed only inside documentation.

Examples must be:

- placeholder-safe
- explicitly non-canonical
- visibly artificial
- not copied as real future contract content
- not populated operational data
- limited to explaining the envelope, payload placement, placeholder policy, and schema-reference policy

Examples must not define real Project OS v2 actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, Resolver behavior, or operational decisions.

## 17. Non-Canonical Entity Example

This example is documentation-only, placeholder-safe, and non-canonical. It must not be copied as real future contract content.

```json
{
  "id": "actor.placeholder_actor.v1",
  "entity_family": "actor",
  "contract_kind": "entity",
  "version": {
    "major": 1
  },
  "status": "draft",
  "schema_ref": null,
  "descripcion": null,
  "source_refs": [],
  "payload": {
    "nombre": null,
    "superficie_capacidad": null
  }
}
```

The example keeps contract metadata in the envelope and entity-specific fields in `payload`. It uses placeholder tokens, `null`, and empty arrays only.

## 18. Non-Canonical Relationship Example

This example is documentation-only, placeholder-safe, and non-canonical. It must not be copied as real future contract content.

```json
{
  "id": "relacion.placeholder_origen.placeholder_tipo.placeholder_destino.v1",
  "entity_family": "relacion",
  "contract_kind": "relationship",
  "version": {
    "major": 1
  },
  "status": "draft",
  "schema_ref": null,
  "descripcion": null,
  "source_refs": [],
  "payload": {
    "origen_entidad": null,
    "origen_id": null,
    "destino_entidad": null,
    "destino_id": null,
    "tipo_relacion": null,
    "cardinalidad": null,
    "requerido": null,
    "orden": null
  }
}
```

The example keeps relationship endpoints and cardinality in `payload`, not in envelope metadata.

## 19. Alignment With Contract Structure

This document aligns with `docs/PROJECT_OS_V2_CONTRACT_STRUCTURE.md`:

- Future contract root remains `contracts/`.
- Future file shape remains `contracts/<entity_family>/<contract_id>.json`.
- Future contract ID shape remains `<entity_family>.<slug>.v<major>`.
- One file represents one contract version.
- Entity-family directories remain singular, lower_snake_case, ASCII-only, and unaccented.
- Future relationship contracts remain under `contracts/relacion/`.
- Status tokens remain `draft`, `review`, `approved`, `deprecated`, and `archived`.
- Placeholder/null policy remains skeleton-first and no-population.
- Examples remain documentation-only, placeholder-safe, and non-canonical.

Valid `entity_family` values are:

```text
resolver
actor
rol
workflow
workflow_step
accion
recurso
scope
fuente
evidencia
estado
limite
regla
variable
plantilla
artefacto
relacion
contrato
```

## 20. Roadmap Readiness

This document is intended to let later explicitly scoped skeleton, schema, validator, and population work proceed without re-deciding:

- base envelope purpose
- envelope vs payload boundary
- required envelope fields
- optional envelope fields
- entity payload placement
- relationship payload placement
- placeholder-safe skeleton policy
- null and empty arrays policy
- status handling
- version handling
- source/reference handling
- schema reference handling
- no-population rule
- non-canonical example policy
- alignment with the approved contract structure

The next roadmap item after R0.01 is R0.02 roadmap hygiene. Contract creation, schema work, validator work, loader behavior, Resolver behavior, runtime behavior, panel work, and write authorization remain unavailable unless a later explicit roadmap ID or PM-approved amendment scopes them.
