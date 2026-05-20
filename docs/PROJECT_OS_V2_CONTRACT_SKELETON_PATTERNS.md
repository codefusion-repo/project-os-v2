# Project OS v2 Contract Skeleton Patterns

## 1. Objective

Define the structure-only skeleton patterns for future Project OS v2 entity and relationship JSON contracts.

This document decides how future placeholder-safe skeletons should use the approved contract envelope, where family-specific payload fields belong, how relationship semantics stay normalized, and how skeletons remain fillable without looking complete.

This document does not create JSON contract files.

## 2. Scope

This issue is documentation-only and structure-only.

It defines future skeleton patterns for:

1. entity contracts
2. relationship contracts
3. family-specific payload placement
4. placeholder-safe field values
5. required vs optional payload fields
6. fillable but visibly incomplete skeletons
7. avoidance of hardcoded or fake operational values
8. alignment with the approved foundation, structure, and envelope documents
9. explicit non-implementation boundaries

The target future skeleton files are still out of scope. This document prepares the pattern those files should follow later.

## 3. Relationship to foundation / structure / envelope docs

This document depends on and does not replace:

- `docs/PROJECT_OS_V2_FOUNDATION_DESIGN.md`
- `docs/PROJECT_OS_V2_CONTRACT_STRUCTURE.md`
- `docs/PROJECT_OS_V2_CONTRACT_ENVELOPE.md`
- `fuentes/Modelo-de-entidades-base.txt`
- `fuentes/Modelo-base-con-definiciones-y-atributos-normalizados.txt`
- `fuentes/Relaciones-principales-y-cardinalidad.txt`

Foundation decisions preserved here:

- Entities store their own normalized attributes.
- `Relación` owns compatibility, permission, requirement, dependency, sequencing, and restriction semantics.
- `WorkflowStep` is a reusable process block.
- `Workflow` composes `WorkflowStep` through `Relación`.
- Workflow-specific order lives in `Relación.orden`.
- `WorkflowStep` delegates `Actor` and `Rol` through `Relación`.
- A `WorkflowStep` can participate in many `Workflow` contracts.
- GitHub remains live evidence.
- Markdown remains human design/reference until equivalent reviewed contracts exist.

Structure decisions preserved here:

- Future contract root is `contracts/`.
- Future file shape is `contracts/<entity_family>/<contract_id>.json`.
- Future ID shape is `<entity_family>.<slug>.v<major>`.
- One file represents one contract version.
- Family directories are singular, lower_snake_case, ASCII-only, and unaccented.
- Relationship contracts live under `contracts/relacion/`.

Envelope decisions preserved here:

- Future contracts use the common envelope fields `id`, `entity_family`, `contract_kind`, `version`, `status`, `schema_ref`, `descripcion`, `source_refs`, and `payload`.
- Envelope metadata and payload data must not duplicate each other.
- Entity-specific attributes live in `payload`.
- Relationship endpoints, relationship type, cardinality, required flag, and order live in `payload`.
- Skeleton values must be placeholder-safe and no-population.

## 4. Skeleton pattern purpose

Skeletons are future fillable contract shells. They should make the intended structure visible while proving that no real Project OS v2 content has been populated yet.

A valid future skeleton pattern should:

- show the approved envelope shape
- show which base entity family owns the contract
- show whether the contract is an entity contract or relationship contract
- expose the payload fields that a later population issue may fill
- keep unknown scalar values as `null`
- keep intentionally empty lists as `[]`
- avoid empty strings
- avoid realistic fake data
- avoid copied issue, PR, comment, review, commit, branch, or validation state
- avoid populated actors, roles, workflows, workflow steps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, and contracts

Skeletons are not sample business content. They are structural placeholders.

## 5. Entity skeleton pattern

An entity skeleton describes one base entity family using the approved envelope.

Future entity skeletons should follow this generic pattern:

- `id` uses `<entity_family>.<slug>.v<major>`.
- `entity_family` is the lower_snake_case token for the base entity family.
- `contract_kind` is `entity`.
- `version` uses the object form decided in this document.
- `status` starts as `draft` unless a later issue explicitly changes the status policy.
- `schema_ref` remains `null` until a future schema reference is approved.
- `descripcion` is the contract-level description and remains `null` in empty skeletons.
- `source_refs` is `[]` unless a later issue intentionally attaches references.
- `payload` contains only attributes owned by the entity family.

Entity-owned attributes live under `payload`. Relationship semantics do not live inside entity payloads.

Entity payloads must not contain:

- relationship endpoints
- relationship cardinality
- relationship required flags
- workflow-specific step order
- compatibility, permission, requirement, dependency, sequencing, or restriction semantics
- copied attributes from related contracts
- live evidence state
- contract envelope metadata duplicated from the envelope

Documentation-only, non-canonical entity example:

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

This example is visibly artificial, placeholder-safe, and non-canonical. It must not be copied as real future contract content.

## 6. Relationship skeleton pattern

A relationship skeleton describes one `Relación` contract using the approved envelope.

Future relationship skeletons should follow this generic pattern:

- `id` uses `relacion.<slug>.v<major>`.
- `entity_family` is `relacion`.
- `contract_kind` is `relationship`.
- `version` uses the object form decided in this document.
- `status` starts as `draft` unless a later issue explicitly changes the status policy.
- `schema_ref` remains `null` until a future schema reference is approved.
- `descripcion` is the contract-level description and remains `null` in empty skeletons.
- `source_refs` is `[]` unless a later issue intentionally attaches references.
- `payload` stores relationship endpoints and relationship semantics.

Relationship endpoints live under `payload`:

- `origen_entidad`
- `origen_id`
- `destino_entidad`
- `destino_id`

Relationship semantics live under `payload`:

- `tipo_relacion`
- `cardinalidad`
- `requerido`
- `orden`

Relationship contracts own compatibility, permission, requirement, dependency, sequencing, and restriction semantics. Entity contracts must not duplicate those semantics.

Reusable `WorkflowStep` model preservation:

- `WorkflowStep` is a reusable process block.
- `Workflow` composes `WorkflowStep` through `Relación`.
- Workflow-specific order lives in `Relación.orden`.
- `WorkflowStep` delegates `Actor` and `Rol` through `Relación`.
- `WorkflowStep` can participate in many `Workflow` contracts.
- Workflow-specific required or optional state lives in `Relación.requerido`.
- Expected artifacts, next steps, next workflows, and delegated actors or roles are linked through `Relación`, not copied into the `WorkflowStep` payload.

Documentation-only, non-canonical relationship example:

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

This example is visibly artificial, placeholder-safe, and non-canonical. It must not be copied as real future contract content.

## 7. Base entity family coverage

Future skeletons must account for all 18 base entity families.

The table below defines the family token, contract kind, and payload ownership direction for future skeletons. Fields listed here are structural candidates after removing envelope metadata duplication. They are not populated values.

| Base entity family | `entity_family` | `contract_kind` | Payload ownership direction |
| --- | --- | --- | --- |
| `Resolver` | `resolver` | `entity` | `nombre`, `manifest_ref`, `policy_ref`, `input_schema_ref`, `output_schema_ref`, `fallback_estado_id` |
| `Actor` | `actor` | `entity` | `nombre`, `superficie_capacidad` |
| `Rol` | `rol` | `entity` | `nombre`, `lente_profesional` |
| `Workflow` | `workflow` | `entity` | `nombre`, `etapa_ciclo_vida`; workflow-specific `orden` belongs in relationship payloads |
| `WorkflowStep` | `workflow_step` | `entity` | `nombre`, `objetivo`, `condicion_base_avance`, `condicion_base_repeticion`, `condicion_base_bloqueo` |
| `Acción` | `accion` | `entity` | `nombre`, `tipo` |
| `Recurso` | `recurso` | `entity` | `tipo`, `nombre`, `ubicacion` |
| `Scope` | `scope` | `entity` | `nombre` |
| `Fuente` | `fuente` | `entity` | `tipo`, `nombre`, `ubicacion`, `nivel_autoridad`, `frescura_requerida` |
| `Evidencia` | `evidencia` | `entity` | `tipo`, `referencia`, `estado_verificacion`, `observado_en` as reference shape only, not copied mutable state |
| `Estado` | `estado` | `entity` | `nombre` |
| `Límite` | `limite` | `entity` | `nombre`, `tipo`, `severidad` |
| `Regla` | `regla` | `entity` | `nombre`, `condicion`, `comportamiento_esperado` |
| `Variable` | `variable` | `entity` | `nombre`, `tipo`, `valor_default`, `valores_permitidos` |
| `Plantilla` | `plantilla` | `entity` | `nombre`, `tipo`, `formato`, `secciones_requeridas` |
| `Artefacto` | `artefacto` | `entity` | `tipo`, `nombre`, `referencia` |
| `Relación` | `relacion` | `relationship` | `origen_entidad`, `origen_id`, `destino_entidad`, `destino_id`, `tipo_relacion`, `cardinalidad`, `requerido`, `orden` |
| `Contrato` | `contrato` | `entity` | `nombre`, `entidad_tipo`; `schema_ref`, `version`, and `estado` map to envelope fields when they have the same meaning |

General de-duplication rules for this table:

- Source `id` maps to envelope `id`, not to payload.
- Source `versión` maps to envelope `version`, not to payload.
- Source `descripción` maps to envelope `descripcion` unless a later family-specific issue approves a distinct payload meaning.
- Source relationship attributes belong to relationship payloads, not to entity payloads.
- Source status-like contract metadata maps to envelope `status` when it has the same meaning.
- Source schema references map to envelope `schema_ref` when they have the same meaning.

## 8. Version field decision

Future skeletons should use object form for the envelope `version` field:

```json
{
  "major": 1
}
```

Decision:

- This is the version field decision for future skeletons.
- Use `version.major` as a positive integer.
- `version.major` must match the `v<major>` suffix in `id`.
- For `actor.placeholder_actor.v1`, the skeleton version is `{ "major": 1 }`.
- Do not use string form such as `"v1"` for envelope `version`.
- Keep the `v` prefix in the contract ID only.
- Do not add minor, patch, revision, date, branch, issue, PR, or commit fields to `version` in the skeleton pattern.

Reasoning:

- The ID already carries the human-readable `v<major>` suffix.
- The object form gives future tools an unambiguous numeric major version without parsing `"v1"`.
- The object form leaves room for a later, explicitly scoped decision about minor or revision metadata.
- A structural major value such as `1` is not operational content and is placeholder-safe when it matches the placeholder ID.

If a later issue cannot safely assign a major version, it must not invent an ID with a version suffix. Once an ID uses `.v1`, `version.major` must be `1`.

## 9. Description ownership rule

The envelope field `descripcion` owns the contract-level description.

Rule:

- Envelope `descripcion` = contract-level description.
- Payload must not repeat the same description.
- A payload description-like field is allowed only when a family-specific issue defines a distinct meaning that is not the contract-level description.

Examples of distinct meanings that would need explicit future approval:

- a source freshness explanation that is not the contract description
- a rule behavior explanation that is separate from the contract description
- a template section note that belongs to template structure rather than contract metadata

Until such a distinct meaning is approved, future skeletons should leave envelope `descripcion` as `null` and omit generic payload `descripcion` fields.

This prevents the source-model `descripción` attribute from being copied twice into both the envelope and payload.

## 10. Placeholder-safe values

Future skeletons must use placeholder-safe values only.

Allowed placeholder-safe values:

- `null` for intentionally unknown scalar values
- `[]` for intentionally empty lists
- `{}` only for required object containers when the child field set is intentionally deferred
- visibly artificial placeholder IDs when an envelope `id` is structurally required
- `draft` for initial skeleton `status` unless a later issue changes the policy
- `version.major` as the integer matching the ID suffix

Disallowed values:

- empty strings
- realistic fake names
- fake but plausible actors, roles, workflows, workflow steps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, or contracts
- copied GitHub issue body text
- copied PR body text
- copied comment text
- copied review text
- copied commit metadata
- copied validation output
- live issue, PR, branch, review, tag, or validation state captured as static data
- populated operational content
- target-project artifacts

Skeletons should be fillable but visibly incomplete. A reviewer should be able to see every intended field that needs later population, while also seeing that no field has been silently filled with invented content.

## 11. Required vs optional payload fields

Envelope required fields are defined by the envelope document. This section defines how future skeleton issues should treat payload fields.

Required payload fields:

- are fields needed to express the normalized shape of the entity or relationship family
- should appear in skeletons even when their values are `null` or `[]`
- must use placeholder-safe values until population is approved
- must not duplicate envelope metadata
- must not carry relationship semantics in entity contracts

Optional payload fields:

- may be omitted when they are not part of the minimum normalized family shape
- may be included only when a later issue explains why they remove ambiguity
- must use `null` or `[]` when included but intentionally unfilled
- must not become a second envelope
- must not become a hidden relationship model inside an entity payload

For relationship skeletons, the minimum required payload field set should include:

- `origen_entidad`
- `origen_id`
- `destino_entidad`
- `destino_id`
- `tipo_relacion`
- `cardinalidad`
- `requerido`
- `orden`

For entity skeletons, the minimum required payload field set should be family-specific and derived from the base entity model after applying the de-duplication rules in this document.

If a field does not apply to a family, a future skeleton issue should either omit it or explicitly define the null semantics for that family. It must not use an empty string to hide uncertainty.

## 12. Non-canonical examples policy

Examples are allowed only inside documentation.

Examples must be:

- placeholder-safe
- explicitly non-canonical
- visibly artificial
- not copied as real future contract content
- not populated operational data
- limited to explaining skeleton shape, payload placement, version shape, description ownership, and placeholder policy

Examples must not define real Project OS v2 actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, Resolver behavior, or operational decisions.

The example IDs in this document use `placeholder_*` tokens only to explain structure. They are not reserved IDs and are not future contract content.

## 13. Markdown scaffolding lifecycle

Markdown design documents are temporary scaffolding for contract design.

Current role:

- Markdown explains decisions for humans.
- Markdown records the reasoning behind contract structure, envelope, and skeleton patterns.
- Markdown helps review the model before JSON contracts exist.

Later role, after equivalent JSON contracts exist and are reviewed:

- `contracts/**` becomes the canonical stable structure for entity and relationship contracts.
- Markdown remains human reference and historical design context.
- AI should read `Resolver` and selected contracts/relationships, not Markdown docs, as the operational source.
- Markdown must not become a parallel contract system.
- Markdown must not duplicate live operational evidence or contract data.

This issue does not create archive behavior, migration behavior, loaders, or archival rules. It only states the lifecycle expectation for documentation versus future contracts.

## 14. No-population rule

The no-population rule is mandatory.

This document does not create real populated data for:

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

Future skeletons must not contain real actors, roles, workflows, workflow steps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, or contracts until later population issues explicitly approve that content.

No copied GitHub issue, PR, comment, review, commit, or validation state is allowed as skeleton payload content.

## 15. Explicit non-implementation boundaries

This issue explicitly does not create or implement:

- JSON contract files
- populated contract data
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
- context packs
- context-pack output or context-pack loading
- target-project artifacts
- database/read-model direction
- projection architecture
- write authorization behavior
- Resolver behavior
- actual skeleton files
- manifest shape
- index shape
- selector shape
- contract loader behavior
- workflow composition
- relationship population

This document defines structure-only skeleton patterns. It does not introduce execution, loading, validation, generation, UI, storage, or authorization behavior.

## 16. Readiness for first JSON skeleton issue

This document is intended to let the first JSON skeleton issue proceed without re-deciding:

- entity skeleton pattern
- relationship skeleton pattern
- family-specific payload placement rules
- envelope vs payload boundary
- `contract_kind` values
- valid `entity_family` placement for entity and relationship contracts
- `version` object shape
- `descripcion` ownership
- placeholder-safe values
- required vs optional payload field treatment
- non-canonical examples policy
- Markdown scaffolding lifecycle
- no-population rule

The first JSON skeleton issue should still decide concrete file creation scope, exact placeholder IDs, exact family-by-family payload field lists, and whether source references are attached as references. It must not populate real operational values unless a later population issue explicitly scopes that work.
